"""Owner-scoped native push sidecar. No environment reads, workers or automatic retries.

notify(owner, job_id) is an internal ChatJobs completion callback, NOT an HTTP route.
Provider acceptance does not establish delivery. See CONTRACT.md before integration.
"""
from contextlib import contextmanager
from contextvars import ContextVar
import ctypes
from ctypes import wintypes
from dataclasses import dataclass, field
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import sqlite3
import threading
import time
import uuid

APP_ID = 'br.ia.IALD'
CHANNEL_ID = 'iald_responses_v1'
MAX_DEVICES = 10
SAFE_STATES = frozenset(('accepted', 'rejected', 'invalid_token', 'uncertain', 'blocked_configuration'))
_SENDING_PRIVATE = ContextVar('iald_push_private_transport', default=False)


class _ProviderLogFilter(logging.Filter):
    def filter(self, record): return not _SENDING_PRIVATE.get()


_PROVIDER_LOG_FILTER = _ProviderLogFilter()


@contextmanager
def _private_transport_logs():
    # HTTPX INFO includes the APNs token URL; HTTP/2 DEBUG can include bearer headers.
    # Filter this synchronous send's context only, preserving unrelated thread logs.
    for name in ('httpx','httpcore.connection','httpcore.http2','httpcore.http11',
                 'hpack.hpack','hpack.table','h2.connection'):
        logging.getLogger(name).addFilter(_PROVIDER_LOG_FILTER)
    for name, logger in list(logging.Logger.manager.loggerDict.items()):
        if isinstance(logger,logging.Logger) and name.split('.')[0] in ('httpx','httpcore','h2','hpack'):
            logger.addFilter(_PROVIDER_LOG_FILTER)
    marker = _SENDING_PRIVATE.set(True)
    try: yield
    finally: _SENDING_PRIVATE.reset(marker)


class PushError(Exception):
    def __init__(self, code, status=400):
        super().__init__(code)
        self.code, self.status = code, status


def _id(value):
    try:
        if not isinstance(value, str) or str(uuid.UUID(value)) != value:
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise PushError('invalid_id') from None
    return value


def _key(value, namespace):
    if not isinstance(value, str) or not value or len(value) > 1024:
        raise PushError('authentication_required', 401)
    return hashlib.sha256((namespace + ':' + value).encode()).hexdigest()


def _valid_token(token, platform):
    if not isinstance(token, str): return False
    if platform == 'ios': return bool(re.fullmatch(r'[a-fA-F0-9]{32,512}', token)) and len(token) % 2 == 0
    return bool(re.fullmatch(r'[A-Za-z0-9_:.-]{16,4096}', token))


class WindowsCipher:
    """DPAPI current-user scope; UI forbidden, no plaintext fallback."""
    def __init__(self):
        if os.name != 'nt': raise PushError('dpapi_unavailable', 503)
        class Blob(ctypes.Structure):
            _fields_ = [('size', wintypes.DWORD), ('data', ctypes.POINTER(ctypes.c_byte))]
        self.Blob = Blob
        self.crypt = ctypes.WinDLL('crypt32', use_last_error=True)
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.kernel.LocalFree.argtypes = [ctypes.c_void_p]
        self.kernel.LocalFree.restype = ctypes.c_void_p
        for name in ('CryptProtectData', 'CryptUnprotectData'):
            fn = getattr(self.crypt, name)
            fn.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.c_void_p,
                           ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
            fn.restype = wintypes.BOOL

    def _transform(self, raw, decrypt=False):
        if not isinstance(raw, bytes): raise PushError('invalid_cipher_input', 503)
        source = ctypes.create_string_buffer(raw)
        incoming = self.Blob(len(raw), ctypes.cast(source, ctypes.POINTER(ctypes.c_byte)))
        outgoing = self.Blob()
        fn = self.crypt.CryptUnprotectData if decrypt else self.crypt.CryptProtectData
        if not fn(ctypes.byref(incoming), None, None, None, None, 1, ctypes.byref(outgoing)):
            raise PushError('storage_cipher_failed', 503)
        try: return ctypes.string_at(outgoing.data, outgoing.size)
        finally: self.kernel.LocalFree(ctypes.cast(outgoing.data, ctypes.c_void_p))

    def seal(self, raw): return self._transform(raw)
    def open(self, raw): return self._transform(raw, True)


@dataclass(repr=False)
class APNs:
    key_id: str
    team_id: str
    private_key: object = field(repr=False)  # Callable returning PEM bytes; never a path.
    topic: str = APP_ID
    _jwt: str = field(default='', init=False, repr=False)
    _issued: int = field(default=0, init=False, repr=False)
    _lock: object = field(default_factory=threading.Lock, init=False, repr=False)

    def bearer(self):
        if (not re.fullmatch(r'[A-Z0-9]{10}', self.key_id) or
            not re.fullmatch(r'[A-Z0-9]{10}', self.team_id) or self.topic != APP_ID or
            not callable(self.private_key)):
            raise PushError('apns_configuration_invalid', 503)
        with self._lock:
            now = int(time.time())
            if self._jwt and 0 <= now - self._issued < 2400: return self._jwt
            try:
                import jwt
                value = jwt.encode({'iss': self.team_id, 'iat': now}, self.private_key(),
                                   algorithm='ES256', headers={'kid': self.key_id})
                if not isinstance(value, str): raise ValueError()
            except Exception:
                raise PushError('apns_signing_unavailable', 503) from None
            self._jwt, self._issued = value, now
            return value


@dataclass(repr=False)
class FCM:
    project_id: str
    access_token: object = field(repr=False)  # Parent supplies a fresh OAuth2 bearer; never legacy server key.

    def bearer(self):
        if not re.fullmatch(r'[a-z][a-z0-9-]{4,61}[a-z0-9]', self.project_id):
            raise PushError('fcm_configuration_invalid', 503)
        try: value = self.access_token()
        except Exception: raise PushError('fcm_auth_unavailable', 503) from None
        if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9._~-]{16,8192}', value):
            raise PushError('fcm_auth_unavailable', 503)
        return value


class HTTP2Transport:
    """One bounded HTTPS request. Fixed hosts only; no redirects, proxies or SDK retries."""
    def prepare(self):
        try:
            import httpx
            import h2  # noqa: F401 - fail before a dispatch receipt if HTTP/2 is unavailable.
        except ImportError: raise PushError('http2_transport_unavailable', 503) from None

    def send(self, *, url, headers, payload):
        import httpx
        with httpx.Client(http2=True, http1=False, trust_env=False, follow_redirects=False,
                          timeout=httpx.Timeout(10.0),
                          transport=httpx.HTTPTransport(http2=True, http1=False, retries=0,
                                                        trust_env=False)) as client:
            with _private_transport_logs():
                with client.stream('POST', url, headers=headers, json=payload) as response:
                    raw = bytearray()
                    for chunk in response.iter_bytes(chunk_size=1024):
                        if len(raw) + len(chunk) > 8192: raise PushError('provider_response_too_large', 502)
                        raw.extend(chunk)
                    # Returned only internally; never persist headers, request, URL, body or bearer.
                    return response.status_code, bytes(raw)


def _public(row):
    return {'id': row['id'], 'platform': row['platform'], 'environment': row['environment'],
            'registered': row['token'] is not None, 'revoked': bool(row['revoked'])}


class PushStore:
    def __init__(self, directory, cipher=None, apns=None, fcm=None, transport=None):
        self.cipher = cipher if cipher is not None else WindowsCipher()
        self.apns, self.fcm = apns, fcm
        self.transport = transport if transport is not None else HTTP2Transport()
        self.lock = threading.RLock()
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.path = directory / 'native_push.sqlite3'
        with self.db() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS bindings(
                  id TEXT PRIMARY KEY, owner TEXT NOT NULL, session TEXT NOT NULL,
                  installation TEXT NOT NULL, platform TEXT NOT NULL, environment TEXT NOT NULL,
                  token BLOB, token_hash TEXT, revoked INTEGER NOT NULL DEFAULT 0,
                  created REAL NOT NULL, updated REAL NOT NULL);
                CREATE INDEX IF NOT EXISTS bindings_owner ON bindings(owner,session,revoked);
                CREATE TABLE IF NOT EXISTS receipts(
                  binding TEXT NOT NULL, job TEXT NOT NULL, event TEXT NOT NULL,
                  state TEXT NOT NULL, http_status INTEGER, created REAL NOT NULL, updated REAL NOT NULL,
                  PRIMARY KEY(binding,job));
            ''')
        # 'dispatching' is reported as uncertain on reads. Never replay it after a restart.

    @contextmanager
    def db(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA secure_delete=ON')
            with db: yield db
        finally: db.close()

    def bind(self, owner, session_id, installation_id, platform, environment):
        owner, session_id = _key(owner, 'push-owner'), _key(session_id, 'push-session')
        installation = _key(_id(installation_id), 'push-installation')
        if (platform, environment) not in (('ios','development'), ('ios','production'), ('android','fcm')):
            raise PushError('invalid_platform')
        with self.lock, self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('''SELECT * FROM bindings WHERE owner=? AND session=? AND installation=?
                                AND platform=? AND environment=? AND revoked=0''',
                             (owner,session_id,installation,platform,environment)).fetchone()
            if row: return _public(row)
            if db.execute('SELECT count(*) FROM bindings WHERE owner=? AND revoked=0',(owner,)).fetchone()[0] >= MAX_DEVICES:
                raise PushError('device_limit',429)
            if db.execute('SELECT count(*) FROM bindings WHERE owner=? AND created>?',
                          (owner,time.time()-86400)).fetchone()[0] >= 100:
                raise PushError('registration_rate_limit',429)
            now, binding = time.time(), str(uuid.uuid4())
            db.execute('INSERT INTO bindings(id,owner,session,installation,platform,environment,created,updated) VALUES(?,?,?,?,?,?,?,?)',
                       (binding,owner,session_id,installation,platform,environment,now,now))
            return _public(db.execute('SELECT * FROM bindings WHERE id=?',(binding,)).fetchone())

    def _binding(self, db, owner, session_id, binding):
        row = db.execute('SELECT * FROM bindings WHERE id=? AND owner=? AND session=?',
                         (_id(binding),_key(owner,'push-owner'),_key(session_id,'push-session'))).fetchone()
        if row is None: raise PushError('binding_not_found',404)
        return row

    def save_token(self, owner, session_id, binding, token, provider):
        with self.lock, self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            row = self._binding(db,owner,session_id,binding)
            if row['revoked']: raise PushError('binding_revoked',409)
            if provider != ('apns' if row['platform']=='ios' else 'fcm') or not _valid_token(token,row['platform']):
                raise PushError('invalid_token')
            if row['platform']=='ios': token = token.lower()
            digest = hashlib.sha256((row['platform']+':'+row['environment']+':'+token).encode()).hexdigest()
            try: sealed = self.cipher.seal(token.encode())
            except Exception: raise PushError('storage_cipher_failed',503) from None
            if not isinstance(sealed,bytes) or not sealed: raise PushError('storage_cipher_failed',503)
            # A token can belong to only the latest authenticated binding on this device.
            db.execute('UPDATE bindings SET revoked=1,token=NULL,token_hash=NULL,updated=? WHERE token_hash=? AND id!=?',
                       (time.time(),digest,binding))
            db.execute('UPDATE bindings SET token=?,token_hash=?,updated=? WHERE id=?',
                       (sealed,digest,time.time(),binding))
            return {'registered': True}

    def revoke(self, owner, session_id, binding):
        with self.lock, self.db() as db:
            self._binding(db,owner,session_id,binding)
            db.execute('UPDATE bindings SET revoked=1,token=NULL,token_hash=NULL,updated=? WHERE id=?',(time.time(),binding))
        return {'revoked': True}

    def revoke_session(self, owner, session_id):
        with self.lock, self.db() as db:
            db.execute('UPDATE bindings SET revoked=1,token=NULL,token_hash=NULL,updated=? WHERE owner=? AND session=?',
                       (time.time(),_key(owner,'push-owner'),_key(session_id,'push-session')))

    def purge(self, owner):
        with self.lock, self.db() as db:
            key = _key(owner,'push-owner')
            db.execute('DELETE FROM receipts WHERE binding IN (SELECT id FROM bindings WHERE owner=?)',(key,))
            db.execute('DELETE FROM bindings WHERE owner=?',(key,))

    def _prepare(self, row, job, event):
        try:
            token = self.cipher.open(row['token']).decode('ascii')
            if not _valid_token(token,row['platform']): raise ValueError()
            data = {'schema_version':'1','event':'iald.response_ready','event_id':event,
                    'job_id':job,'binding_id':row['id']}
            alert = {'title':'IALD','body':'Sua resposta está pronta.'}
            if row['platform']=='ios':
                if self.apns is None: raise ValueError()
                bearer = self.apns.bearer()
                host = 'api.sandbox.push.apple.com' if row['environment']=='development' else 'api.push.apple.com'
                url = 'https://'+host+'/3/device/'+token
                headers = {'authorization':'bearer '+bearer,'apns-topic':APP_ID,'apns-push-type':'alert',
                           'apns-priority':'10','apns-id':event,'apns-expiration':str(int(time.time())+3600)}
                payload = {'aps':{'alert':alert,'sound':'default'},**data}
            else:
                if self.fcm is None: raise ValueError()
                bearer = self.fcm.bearer()
                url = 'https://fcm.googleapis.com/v1/projects/'+self.fcm.project_id+'/messages:send'
                headers = {'authorization':'Bearer '+bearer}
                payload = {'message':{'token':token,'notification':alert,'data':data,
                           'android':{'priority':'high','ttl':'3600s','notification':{
                               'channel_id':CHANNEL_ID,'icon':'ic_stat_iald','tag':event,'sound':'default'}}}}
            self.transport.prepare()
            return dict(url=url,headers=headers,payload=payload)
        except Exception: raise PushError('push_configuration_unavailable',503) from None

    def notify(self, owner, job_id):
        """Called after completed, committed, eligible ChatJobs output. At most once per binding/job."""
        _id(job_id)
        with self.lock, self.db() as db:
            rows = db.execute('SELECT * FROM bindings WHERE owner=? AND revoked=0 AND token IS NOT NULL LIMIT ?',
                              (_key(owner,'push-owner'),MAX_DEVICES)).fetchall()
        results = []
        for row in rows:
            event, now = str(uuid.uuid4()), time.time()
            with self.lock, self.db() as db:
                db.execute('BEGIN IMMEDIATE')
                current = db.execute('SELECT * FROM bindings WHERE id=?',(row['id'],)).fetchone()
                if current is None or current['revoked'] or current['token_hash'] != row['token_hash']: continue
                if db.execute('SELECT 1 FROM receipts WHERE binding=? AND job=?',(row['id'],job_id)).fetchone(): continue
                db.execute('INSERT INTO receipts VALUES(?,?,?,?,?,?,?)',
                           (row['id'],job_id,event,'preparing',None,now,now))
            try: request = self._prepare(row,job_id,event)
            except PushError:
                self._finish(row['id'],job_id,'blocked_configuration',None)
                results.append({'state':'blocked_configuration'}); continue
            with self.lock, self.db() as db:
                current = db.execute('SELECT * FROM bindings WHERE id=?',(row['id'],)).fetchone()
                if current is None or current['revoked'] or current['token_hash'] != row['token_hash']:
                    db.execute('UPDATE receipts SET state=?,updated=? WHERE binding=? AND job=?',
                               ('revoked',time.time(),row['id'],job_id)); continue
                db.execute('UPDATE receipts SET state=?,updated=? WHERE binding=? AND job=?',
                           ('dispatching',time.time(),row['id'],job_id))
            # Dispatch receipt is committed BEFORE any provider request. Never auto-retry.
            state, http_status = 'uncertain', None
            try:
                code, body = self.transport.send(**request)
                if type(code) is not int or not 100 <= code <= 599: raise ValueError()
                http_status = code
                state = 'accepted' if code == 200 else 'rejected'
                if row['platform']=='ios' and code == 410: state = 'invalid_token'
                if row['platform']=='android' and code == 404 and isinstance(body,bytes) and len(body)<=8192:
                    try:
                        details = json.loads(body).get('error',{}).get('details',[])
                        if isinstance(details,list) and any(isinstance(d,dict) and
                          d.get('@type')=='type.googleapis.com/google.firebase.fcm.v1.FcmError' and
                          d.get('errorCode')=='UNREGISTERED' for d in details): state='invalid_token'
                    except (ValueError,AttributeError,TypeError): pass
            except Exception: pass  # Never stringify/log provider exceptions (often contain token URLs).
            finally: request = None
            self._finish(row['id'],job_id,state,http_status)
            if state=='invalid_token':
                with self.lock, self.db() as db:
                    db.execute('UPDATE bindings SET revoked=1,token=NULL,token_hash=NULL,updated=? WHERE id=? AND token_hash=?',
                               (time.time(),row['id'],row['token_hash']))
            results.append({'state':state,'http_status':http_status})
        return {'attempts':results}

    def _finish(self,binding,job,state,http_status):
        if state not in SAFE_STATES: raise PushError('invalid_receipt',503)
        with self.lock, self.db() as db:
            db.execute('UPDATE receipts SET state=?,http_status=?,updated=? WHERE binding=? AND job=?',
                       (state,http_status,time.time(),binding,job))

    def receipts(self, owner, job_id):
        with self.lock, self.db() as db:
            rows = db.execute('''SELECT r.state,r.http_status,r.created,r.updated FROM receipts r
              JOIN bindings b ON b.id=r.binding WHERE b.owner=? AND r.job=? LIMIT ?''',
                              (_key(owner,'push-owner'),_id(job_id),MAX_DEVICES)).fetchall()
        return [{**dict(row),'state':'uncertain' if row['state'] in ('preparing','dispatching') else row['state']}
                for row in rows]


def register(app, directory, *, authenticate, csrf_check, ios_environment='production',
             cipher=None, apns=None, fcm=None, transport=None):
    """Lazy Flask routes. authenticate() -> (owner, stable authenticated session_id).

    csrf_check() must return exactly True for mutating requests, including native clients.
    Parent MUST call revoke_session before logout/session expiry and purge on account deletion.
    """
    from flask import request, jsonify
    if ios_environment not in ('development','production') or not callable(authenticate) or not callable(csrf_check):
        raise PushError('invalid_route_configuration',503)
    manager, lock = [], threading.Lock()

    def store():
        with lock:
            if not manager: manager.append(PushStore(directory,cipher,apns,fcm,transport))
        return manager[0]
    app.extensions['iald_chat_push'] = store

    def run(fn):
        try:
            identity = authenticate()
            if not isinstance(identity,(tuple,list)) or len(identity)!=2: raise PushError('authentication_required',401)
            owner,sid = identity
            _key(owner,'push-owner'); _key(sid,'push-session')
            if csrf_check() is not True: raise PushError('request_not_authorized',403)
            if request.content_length is not None and request.content_length>8192: raise PushError('request_too_large',413)
            if not request.is_json: raise PushError('json_required',415)
            raw = request.stream.read(8193)
            if len(raw)>8192: raise PushError('request_too_large',413)
            try: body=json.loads(raw)
            except (ValueError,UnicodeError): raise PushError('invalid_json') from None
            if not isinstance(body,dict): raise PushError('invalid_json')
            response=jsonify(fn(owner,sid,body))
        except PushError as exc:
            response=jsonify(error=exc.code); response.status_code=exc.status
        except Exception:
            response=jsonify(error='push_unavailable'); response.status_code=503
        response.headers['Cache-Control']='private, no-store'
        return response

    @app.route('/api/native-push/revoke-session',methods=['POST'])
    def native_push_revoke_session():
        def revoke(owner,sid,body):
            if body: raise PushError('invalid_revoke_request')
            store().revoke_session(owner,sid)
            return {'revoked':True}
        return run(revoke)

    @app.route('/api/native-push/bindings',methods=['POST'])
    def native_push_bind():
        def bind(owner,sid,body):
            if set(body)!={'installation_id','platform','consent'} or body['consent'] is not True:
                raise PushError('explicit_consent_required')
            platform=body['platform']
            return store().bind(owner,sid,body['installation_id'],platform,
                                ios_environment if platform=='ios' else 'fcm')
        return run(bind)

    @app.route('/api/native-push/bindings/<binding>/token',methods=['PUT'])
    def native_push_token(binding):
        def save(owner,sid,body):
            if set(body)!={'token','provider'}: raise PushError('invalid_token_request')
            return store().save_token(owner,sid,binding,body['token'],body['provider'])
        return run(save)

    @app.route('/api/native-push/bindings/<binding>',methods=['DELETE'])
    def native_push_revoke(binding):
        def revoke(owner,sid,body):
            if body: raise PushError('invalid_revoke_request')
            return store().revoke(owner,sid,binding)
        return run(revoke)

    return store
