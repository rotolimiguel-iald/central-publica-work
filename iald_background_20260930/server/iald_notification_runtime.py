"""Bind native notifications to the existing authenticated app and local vault.

Credential imports are a separate, operator-authorized provisioning step. This
module does not create provider keys, accounts, or subscriptions on import.
"""
import hashlib
import json
from pathlib import Path
import threading
import time
import sqlite3
import sys
import iald_chat_push as push


class Credentials:
    def __init__(self, path):
        self.path=Path(path);self.lock=threading.Lock();self.cached_stamp=None
        self.apns=None;self.fcm=None;self._access='';self._access_until=0

    def load(self):
        with self.lock:
            stamp=self.path.stat().st_mtime_ns if self.path.is_file() else None
            if stamp==self.cached_stamp:return self.apns,self.fcm
            self.apns,self.fcm=None,None
            self._access='';self._access_until=0
            try:
                data=json.loads(push.WindowsCipher().open(self.path.read_bytes()))
                apple=data.get('apns')
                if apple:
                    pem=apple['private_key'].encode('ascii')
                    self.apns=push.APNs(apple['key_id'],apple['team_id'],lambda:pem)
                google=data.get('fcm')
                if google:
                    # Closures retain keys only in the server process; never in app assets.
                    self.fcm=push.FCM(google['project_id'],lambda:self.google_token(google))
                self.cached_stamp=stamp
            except Exception:
                self.apns,self.fcm=None,None
            return self.apns,self.fcm

    def google_token(self, config):
        with self.lock:
            if self._access and time.time()<self._access_until:return self._access
            import jwt
            import requests
            now=int(time.time());account=config['client_email']
            if not account.endswith('@'+config['project_id']+'.iam.gserviceaccount.com'):
                raise push.PushError('fcm_auth_unavailable',503)
            assertion=jwt.encode({'iss':account,'scope':'https://www.googleapis.com/auth/firebase.messaging',
                                  'aud':'https://oauth2.googleapis.com/token','iat':now,'exp':now+3600},
                                 config['private_key'],algorithm='RS256')
            try:
                with requests.Session() as client:
                    client.trust_env=False
                    response=client.post('https://oauth2.googleapis.com/token',data={
                        'grant_type':'urn:ietf:params:oauth:grant-type:jwt-bearer','assertion':assertion},
                        timeout=(10,15),allow_redirects=False)
                    response.raise_for_status();result=response.json()
                token=result['access_token'];duration=int(result['expires_in'])
                if not isinstance(token,str) or not 60<=duration<=3600:raise ValueError()
                self._access,self._access_until=token,time.time()+duration-60
                return token
            except Exception:raise push.PushError('fcm_auth_unavailable',503) from None


class PushAuthorization:
    """Only fingerprints and expirations; no password hashes or bearer credentials."""
    def __init__(self, directory, store):
        self.path=Path(directory)/'authorization.sqlite3'
        self.store=store;self.lock=threading.RLock()

    def _database(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        db=sqlite3.connect(self.path,timeout=10)
        db.execute('CREATE TABLE IF NOT EXISTS authority(owner TEXT,scope TEXT,sid TEXT,expires REAL,PRIMARY KEY(owner,sid))')
        return db

    @staticmethod
    def owner_key(owner):return hashlib.sha256(('push-owner:'+owner).encode()).hexdigest()

    def scope(self, owner, record, sid=None, expires=None):
        version=json.dumps([owner,record.get('created','legacy'),record.get('password_hash','')])
        scope=hashlib.sha256(version.encode()).hexdigest();key=self.owner_key(owner)
        with self.lock:
            db=self._database()
            try:
                with db:
                    for old_scope,old_sid,until in db.execute('SELECT scope,sid,expires FROM authority WHERE owner=?',(key,)).fetchall():
                        if old_scope!=scope or until<=time.time():
                            self.store().revoke_session(old_scope,old_sid)
                            db.execute('DELETE FROM authority WHERE owner=? AND sid=?',(key,old_sid))
                    if sid is not None:
                        if not isinstance(expires,(int,float)) or expires<=time.time():
                            raise push.PushError('native_authentication_expired',401)
                        db.execute('INSERT OR REPLACE INTO authority VALUES(?,?,?,?)',(key,scope,sid,expires))
                return scope
            finally:db.close()

    def purge(self, owner):
        with self.lock:
            db=self._database()
            try:
                with db:
                    key=self.owner_key(owner)
                    for (scope,) in db.execute('SELECT DISTINCT scope FROM authority WHERE owner=?',(key,)).fetchall():
                        self.store().purge(scope)
                    db.execute('DELETE FROM authority WHERE owner=?',(key,))
            finally:db.close()


def register(app, root, origins, load_users, account_blocked, token_expiry=None):
    from flask import request,session,g,jsonify
    dependencies=Path(root)/'.iald_runtime'/'push_dependencies'
    if dependencies.is_dir() and str(dependencies) not in sys.path:
        sys.path.append(str(dependencies))
    directory=Path(root)/'.iald_runtime'/'native_push'
    credentials=Credentials(directory/'credentials.dpapi')

    def identity():
        authorization=request.headers.get('Authorization','')
        if not getattr(g,'app_bearer',False) or not authorization.startswith('Bearer '):
            raise push.PushError('native_authentication_required',401)
        token=authorization[7:].strip()
        if not token:raise push.PushError('native_authentication_required',401)
        owner=session.get('username','');record=load_users().get(owner)
        if not record or account_blocked(record):raise push.PushError('native_authentication_required',401)
        sid=hashlib.sha256(token.encode()).hexdigest()
        # Production supplies the expiration read by the existing signed-token verifier.
        until=token_expiry(token) if token_expiry else time.time()+3600
        return authority.scope(owner,record,sid,until),sid

    get_store=push.register(app,directory,authenticate=identity,
        csrf_check=lambda:request.is_json and request.headers.get('Origin','') in ('',*origins))
    authority=PushAuthorization(directory,get_store)

    @app.route('/api/native-push/status')
    def native_push_status():
        apple,google=credentials.load()
        return jsonify(ios=apple is not None,android=google is not None,
                       message='Ative os avisos para saber quando a resposta estiver pronta.')

    def notify(owner, job_id):
        record=load_users().get(owner)
        if not record or account_blocked(record):return
        store=get_store();store.apns,store.fcm=credentials.load()
        return store.notify(authority.scope(owner,record),job_id)

    def purge(owner):authority.purge(owner)

    def revoke_current():
        try:
            owner,sid=identity();get_store().revoke_session(owner,sid)
        except push.PushError:pass

    @app.before_request
    def logout_push():
        if request.path=='/logout' and getattr(g,'app_bearer',False):revoke_current()

    app.extensions['iald_notification_runtime']={'notify':notify,'purge':purge,'revoke_current':revoke_current}
    return notify,purge
