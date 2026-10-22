"""Private attachment custody: opaque refs, scoped metadata, DPAPI at rest.

No model calls, HTTP fetching or background expiry deletion. Host authenticates
scope and conversation; a username in a JSON request is never authentication.
"""
import base64
from contextlib import closing
from dataclasses import dataclass
import hashlib
import io
import json
import math
from pathlib import Path
import re
import secrets
import shutil
import sqlite3
import struct
import time

MAX_BASE64_BYTES=50_000_000
MAX_RAW_BYTES=37_499_904  # ((50,000,000 - 128 header bytes) // 4) * 3.
MAX_CHAT_JSON_BYTES=2_000_000
MAX_PROVIDER_JSON_BYTES=64_000_000
PART_TYPE='iald_media'


class MediaError(ValueError):pass
class MediaUnavailable(MediaError):pass


@dataclass(frozen=True)
class Scope:
    owner: str
    generation: str
    conversation: str

    def validate(self):
        if any(not isinstance(v,str) or not 1<=len(v)<=256 for v in (self.owner,self.generation,self.conversation)):
            raise MediaError('Authenticated media scope required')
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}',self.conversation):raise MediaError('Invalid conversation')
        return self


def json_bytes(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()


def media_scope_token(scope):
    """Client storage partition only; not authentication, credential or bearer."""
    if not isinstance(scope,Scope):raise MediaError('Host scope required')
    scope.validate()
    return sha(json_bytes(['iald.media.client-scope/v1',scope.owner,scope.generation]))[:32]


def client_capabilities(scope):
    return {'media_scope':media_scope_token(scope),'max_media_bytes':MAX_RAW_BYTES,
        'max_encoded_bytes':MAX_BASE64_BYTES,'encoded_header_margin':128,
        'retention':'until_explicit_conversation_or_account_delete','expires_at':None,
        'partition_is_authentication':False}


class PrivateMediaStore:
    def __init__(self,root,*,authorize_scope,validate_media,cipher=None,clock=time.time,
                 owner_quota=1_000_000_000,conversation_quota=500_000_000,uploads_per_minute=8,max_active_uploads=4):
        if not callable(authorize_scope) or not callable(validate_media):raise MediaError('Host media guards required')
        self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True)
        self.blobs=self.root/'blobs';self.blobs.mkdir(exist_ok=True)
        self.db_path=self.root/'media.sqlite3';self.authorize_scope=authorize_scope
        self.validate_media=validate_media;self.clock=clock
        self.owner_quota=owner_quota;self.conversation_quota=conversation_quota
        self.uploads_per_minute=uploads_per_minute;self.max_active_uploads=max_active_uploads
        if cipher is None:
            from iald_chat_jobs import WindowsCipher
            cipher=WindowsCipher()
        self.cipher=cipher
        with closing(self._db()) as db:
            db.execute('''CREATE TABLE IF NOT EXISTS media(
                id TEXT PRIMARY KEY,owner TEXT NOT NULL,generation TEXT NOT NULL,conversation TEXT NOT NULL,
                metadata TEXT NOT NULL,bytes INTEGER NOT NULL,expires REAL,status TEXT NOT NULL,created REAL NOT NULL)''')
            db.execute('CREATE INDEX IF NOT EXISTS media_scope ON media(owner,generation,conversation)')

    def _db(self):return sqlite3.connect(self.db_path,timeout=15,isolation_level=None)

    def _scope(self,scope):
        if not isinstance(scope,Scope):raise MediaError('Authenticated media scope required')
        scope.validate()
        if self.authorize_scope(scope) is not True:raise MediaUnavailable('Media unavailable in this scope')

    def _id(self,value):
        if not isinstance(value,str) or not re.fullmatch(r'[0-9a-f]{32}',value):raise MediaUnavailable('Media unavailable in this scope')
        return value

    def _row(self,db,media_ref,scope):
        self._scope(scope)
        row=db.execute('SELECT metadata,expires,status FROM media WHERE id=? AND owner=? AND generation=? AND conversation=?',
            (self._id(media_ref),scope.owner,scope.generation,scope.conversation)).fetchone()
        if row is None:raise MediaUnavailable('Media unavailable in this scope')
        if row[2]!='active':raise MediaUnavailable('Media explicitly removed')
        if row[1] is not None and row[1]<=self.clock():raise MediaUnavailable('Media expired; upload again explicitly')
        metadata=json.loads(row[0])
        if metadata['media_ref']!=media_ref:raise MediaUnavailable('Media metadata integrity failure')
        d=metadata.get('duration_seconds')
        if isinstance(d,bool) or not isinstance(d,(int,float)) or not math.isfinite(d) or d<=0:
            raise MediaUnavailable('Invalid stored media duration')
        if type(metadata.get('bytes'))is not int or not 0<metadata['bytes']<=MAX_RAW_BYTES:
            raise MediaUnavailable('Invalid stored media size')
        if metadata.get('kind')=='video':
            if any(type(metadata.get(k))is not int or not 0<metadata[k]<=65536 for k in ('width','height')) or metadata['width']*metadata['height']>67_108_864:
                raise MediaUnavailable('Invalid stored video dimensions')
        return metadata

    def put(self,stream,*,scope,mime,content_length):
        self._scope(scope) # BEFORE reading request stream.
        if type(content_length) is not int or not 0<content_length<=MAX_RAW_BYTES:raise MediaError('Upload length required; exceeds declared server byte cap')
        if not isinstance(mime,str) or mime not in ('audio/wav','audio/mpeg','audio/flac','audio/ogg','audio/mp4','video/mp4','video/quicktime','video/x-msvideo','video/x-ms-wmv'):
            raise MediaError('Unsupported media MIME')
        if shutil.disk_usage(self.root).free<2*content_length+64_000_000:raise MediaError('Insufficient private media disk space')
        # Reserve quota with exclusive DB transaction; all reservations count.
        ident=secrets.token_hex(16);expires=None
        with closing(self._db()) as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                owner=db.execute("SELECT coalesce(sum(bytes),0) FROM media WHERE owner=? AND generation=? AND status IN ('active','uploading')",(scope.owner,scope.generation)).fetchone()[0]
                conv=db.execute("SELECT coalesce(sum(bytes),0) FROM media WHERE owner=? AND generation=? AND conversation=? AND status IN ('active','uploading')",(scope.owner,scope.generation,scope.conversation)).fetchone()[0]
                recent=db.execute('SELECT count(*) FROM media WHERE owner=? AND generation=? AND created>?',(scope.owner,scope.generation,self.clock()-60)).fetchone()[0]
                active=db.execute("SELECT count(*) FROM media WHERE status='uploading'").fetchone()[0]
                if recent>=self.uploads_per_minute or active>=self.max_active_uploads:raise MediaError('Private media upload rate/concurrency limit reached')
                if owner+content_length>self.owner_quota or conv+content_length>self.conversation_quota:raise MediaError('Private media storage quota reached; explicitly manage attachments')
                db.execute('INSERT INTO media VALUES(?,?,?,?,?,?,?,?,?)',(ident,scope.owner,scope.generation,scope.conversation,'{}',content_length,expires,'uploading',self.clock()))
                db.commit()
            except BaseException:db.rollback();raise
        path=self.blobs/(ident+'.bin');temp=self.blobs/(ident+'.tmp')
        try:
            chunks=[];remaining=content_length
            while remaining:
                value=stream.read(min(1024*1024,remaining))
                if not isinstance(value,bytes) or not value:raise MediaError('Incomplete upload')
                if len(value)>remaining:raise MediaError('Upload exceeds declared size')
                chunks.append(value);remaining-=len(value)
            if stream.read(1):raise MediaError('Upload exceeds declared size')
            raw=b''.join(chunks);chunks.clear()
            facts=self.validate_media(raw,mime) # Authoritative probe, never client metadata.
            duration=facts['duration_seconds'];kind=mime.split('/')[0]
            if isinstance(duration,bool) or not isinstance(duration,(int,float)) or not math.isfinite(duration) or duration<=0:raise MediaError('Invalid measured duration')
            if facts.get('kind')!=kind:raise MediaError('Measured media type mismatch')
            metadata=dict(type=PART_TYPE,media_ref=ident,kind=kind,mime=mime,bytes=len(raw),
                duration_seconds=duration,sha256=sha(raw),expires_at=expires,
                width=facts.get('width'),height=facts.get('height'),has_audio=facts.get('has_audio',kind=='audio'))
            if type(metadata['has_audio'])is not bool:raise MediaError('Invalid measured audio presence')
            for key in ('width','height'):
                value=metadata[key]
                if kind=='video' and (type(value)is not int or not 0<value<=65536):raise MediaError('Invalid measured video dimensions')
            if kind=='video' and metadata['width']*metadata['height']>67_108_864:raise MediaError('Video dimensions exceed local decoder pixel safety bound')
            header=json_bytes({'scope':scope.__dict__,'metadata':metadata})
            encrypted=self.cipher.seal(struct.pack('!I',len(header))+header+raw)
            with temp.open('xb') as target:target.write(encrypted)
            temp.rename(path)
            with closing(self._db()) as db:
                db.execute("UPDATE media SET metadata=?,status='active' WHERE id=? AND status='uploading'",(json_bytes(metadata).decode(),ident))
            return metadata
        except BaseException:
            for item in (temp,path):
                if item.is_file():item.unlink()
            with closing(self._db()) as db:db.execute("UPDATE media SET status='upload_failed' WHERE id=?",(ident,))
            raise

    def metadata(self,media_ref,scope):
        with closing(sqlite3.connect(self.db_path.as_uri()+'?mode=ro',uri=True)) as db:
            db.execute('PRAGMA query_only=ON')
            return self._row(db,media_ref,scope)

    def read(self,media_ref,scope,expected_sha256):
        with closing(self._db()) as db:
            db.execute('BEGIN')
            metadata=self._row(db,media_ref,scope)
            if metadata['sha256']!=expected_sha256:raise MediaUnavailable('Media hash mismatch')
            # All ownership/auth/generation/conversation/hash checks precede blob I/O.
            path=self.blobs/(self._id(media_ref)+'.bin')
            if path.stat().st_size>MAX_RAW_BYTES+1_000_000:raise MediaUnavailable('Invalid media storage size')
            decrypted=self.cipher.open(path.read_bytes())
            if len(decrypted)<4:raise MediaUnavailable('Invalid encrypted media envelope')
            size=struct.unpack('!I',decrypted[:4])[0]
            if not 0<size<=65536:raise MediaUnavailable('Invalid encrypted media envelope')
            envelope=json.loads(decrypted[4:4+size]);raw=decrypted[4+size:]
            if envelope!={'scope':scope.__dict__,'metadata':metadata} or len(raw)!=metadata['bytes'] or sha(raw)!=expected_sha256:
                raise MediaUnavailable('Media custody integrity failure')
            return raw,metadata

    def _revoke(self,scope,*,all_conversations=False):
        self._scope(scope)
        with closing(self._db()) as db:
            db.execute('BEGIN IMMEDIATE')
            query='owner=? AND generation=?';args=[scope.owner,scope.generation]
            if not all_conversations:query+=' AND conversation=?';args.append(scope.conversation)
            rows=db.execute('SELECT id FROM media WHERE '+query,args).fetchall()
            db.execute("UPDATE media SET status='revoked' WHERE "+query,args)
            db.commit()
        removed=0
        for row in rows:
            path=self.blobs/(self._id(row[0])+'.bin')
            if path.exists():path.unlink();removed+=1
        return {'status':'revoked','blobs_removed':removed,'conversation_history_modified':False}

    def revoke_conversation(self,scope):return self._revoke(scope)
    def revoke_account_generation(self,scope):
        # Host must separately authorize account deletion; normal upload scope is insufficient.
        raise MediaError('Use explicit privileged account deletion adapter')

    def revoke_account(self,scope,*,authorize_account_deletion):
        if not callable(authorize_account_deletion) or authorize_account_deletion(scope.owner,scope.generation) is not True:
            raise MediaUnavailable('Account deletion authorization required')
        return self._revoke(scope,all_conversations=True)


def contains_refs(messages):
    return any(isinstance(m,dict) and isinstance(m.get('content'),list) and
        any(isinstance(p,dict) and p.get('type')==PART_TYPE for p in m['content']) for m in messages)


def reject_worker_media(messages,*,provider,worker=False):
    if contains_refs(messages) and (provider!='mimo' or worker is not False):
        raise MediaError('Private media requires authenticated MiMo manager; no worker/nonMiMo dispatch')


def resolve_media_metadata(messages,*,store,scope,provider='mimo',worker=False):
    """Metadata only, scoped SELECTs; zero blob opens/decrypts. No network checks."""
    runtime=PrivateMediaRuntime(store,scope,authorize_dispatch=lambda:False,worker=worker)
    reject_worker_media(messages,provider=provider,worker=worker)
    canonical=runtime.canonicalize(messages,provider=provider)
    result=[]
    for message in canonical:
        for part in message.get('content',[]) if isinstance(message.get('content'),list) else []:
            if part.get('type')==PART_TYPE:
                result.append({**part,'encoded_bytes_upper':4*((part['bytes']+2)//3)+128})
    return result


class PrivateMediaRuntime:
    """Host-created request scope, captured explicitly into the provider thread."""
    def __init__(self,store,scope,*,authorize_dispatch,worker=False):
        if not callable(authorize_dispatch):raise MediaError('Host dispatch authorization required')
        self.store=store;self.scope=scope;self.authorize_dispatch=authorize_dispatch;self.worker=worker

    def canonical_part(self,part):
        if not isinstance(part,dict) or part.get('type')!=PART_TYPE:raise MediaError('Invalid private media reference')
        if set(part)-{'type','media_ref','kind','mime','bytes','duration_seconds','sha256','expires_at','width','height','has_audio'}:
            raise MediaError('Unexpected media reference fields')
        actual=self.store.metadata(part.get('media_ref'),self.scope)
        if part.get('sha256')!=actual['sha256']:raise MediaUnavailable('Media hash mismatch')
        if any(value!=actual.get(key) for key,value in part.items()):raise MediaError('Client media facts differ from authoritative metadata')
        return actual

    def canonicalize(self,messages,*,provider='mimo'):
        reject_worker_media(messages,provider=provider,worker=self.worker)
        try:size=len(json_bytes(messages))
        except (ValueError,TypeError):raise MediaError('Invalid nonfinite or unserializable media request') from None
        if size>MAX_CHAT_JSON_BYTES:raise MediaError('Chat JSON request exceeds explicit byte budget; use private upload')
        import copy
        result=copy.deepcopy(messages)
        for message in result:
            if isinstance(message.get('content'),list):
                for i,part in enumerate(message['content']):
                    if isinstance(part,dict) and part.get('type')==PART_TYPE:
                        if message.get('role')!='user':raise MediaError('Private media only permitted in user history')
                        message['content'][i]=self.canonical_part(part)
        return result

    def metrics_view(self,messages):
        """Host-only compatibility projection for existing modality ledger stamp."""
        result=self.canonicalize(messages)
        for message in result:
            if not isinstance(message.get('content'),list):continue
            for i,part in enumerate(message['content']):
                if part.get('type')==PART_TYPE:
                    kind='input_audio' if part['kind']=='audio' else 'video_url'
                    message['content'][i]={'type':kind,kind:{'data' if kind=='input_audio' else 'url':'private-reference:'+part['media_ref']}}
        return result

    def admit(self,body,maximum,window=1048576):
        messages=self.canonicalize(body['messages'])
        text_bytes=len(json_bytes({**body,'messages':messages}))
        estimated=0;encoded=0
        for message in messages:
            for part in message.get('content',[]) if isinstance(message.get('content'),list) else []:
                if part.get('type')!=PART_TYPE:continue
                d=part['duration_seconds']
                audio=math.ceil(d*6.25) if part['has_audio'] else 0
                # Official video default2fps; upper estimate per sampled frame,
                # not an exact vendor tokenizer or a guarantee of charged usage.
                video=min(2048,max(2,math.ceil(d*2)))*304 if part['kind']=='video' else 0
                estimated+=math.ceil((audio+video)*1.25)+512
                encoded+=4*((part['bytes']+2)//3)+128
        used=text_bytes+estimated
        reserve=min(maximum,window-used-4096-128)
        if reserve<min(16384,maximum):raise MediaError('Text plus modality estimate exceeds context; TGL/history preserved')
        if text_bytes+encoded+1024>MAX_PROVIDER_JSON_BYTES:raise MediaError('Final MiMo HTTP body exceeds64MB request budget')
        return {'input_bound':used,'output_reserve':reserve,'text_utf8_bytes':text_bytes,
            'media_estimated_tokens':estimated,'estimation':'conservative_local_estimate_not_provider_count',
            'provider_http_bytes_upper':text_bytes+encoded+1024}

    def expand(self,body,*,provider):
        reject_worker_media(body['messages'],provider=provider,worker=self.worker)
        if provider!='mimo':raise MediaError('Only MiMo can resolve private media')
        if self.authorize_dispatch() is not True:raise MediaUnavailable('Consent/wallet/permission revoked before media dispatch')
        import copy
        result=copy.deepcopy(body)
        result['messages']=self.canonicalize(body['messages'],provider=provider)
        for message in result['messages']:
            if not isinstance(message.get('content'),list):continue
            for i,part in enumerate(message['content']):
                if part.get('type')!=PART_TYPE:continue
                raw,metadata=self.store.read(part['media_ref'],self.scope,part['sha256'])
                uri='data:'+metadata['mime']+';base64,'+base64.b64encode(raw).decode('ascii')
                if len(uri.encode())>MAX_BASE64_BYTES:raise MediaError('Full data URI exceeds50MB decimal')
                kind='input_audio' if metadata['kind']=='audio' else 'video_url'
                field='data' if kind=='input_audio' else 'url'
                message['content'][i]={'type':kind,kind:{field:uri}}
        if len(json_bytes(result))>MAX_PROVIDER_JSON_BYTES:raise MediaError('Final MiMo HTTP request exceeds byte budget')
        return result
