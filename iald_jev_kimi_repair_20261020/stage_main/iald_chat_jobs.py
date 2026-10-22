"""Durable, owner-scoped chat delivery. A network disconnect is not cancellation.

The provider runs exactly once in a server thread. Reconnects read encrypted
events; process restarts mark unfinished jobs interrupted, never resubmit them.
Prompts and authentication are kept in memory only. Events expire after 7 days;
idempotency receipts remain as tombstones until account deletion.
"""
import codecs
import iald_app_memory as app_memory
from contextlib import contextmanager
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import threading
import time
import uuid

TERMINAL = frozenset(('completed', 'failed', 'cancelled', 'interrupted'))
MAX_EVENT_BYTES = 16 * 1024 * 1024
RETENTION = 7 * 86400


class JobError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


class WindowsCipher:
    """DPAPI user scope: no plaintext fallback and no new exportable key."""
    def __init__(self):
        if os.name != 'nt':
            raise RuntimeError('Windows DPAPI is required for chat storage')
        class Blob(ctypes.Structure):
            _fields_ = [('size', wintypes.DWORD), ('data', ctypes.POINTER(ctypes.c_char))]
        self.Blob = Blob
        self.crypt = ctypes.WinDLL('crypt32', use_last_error=True)
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.kernel.LocalFree.argtypes = [ctypes.c_void_p]
        self.kernel.LocalFree.restype = ctypes.c_void_p

    def transform(self, value, decrypt=False):
        buf = ctypes.create_string_buffer(value)
        src = self.Blob(len(value), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
        out = self.Blob()
        fn = self.crypt.CryptUnprotectData if decrypt else self.crypt.CryptProtectData
        if not fn(ctypes.byref(src), None, None, None, None, 1, ctypes.byref(out)):
            raise OSError('Chat storage encryption failed')
        try:
            return ctypes.string_at(out.data, out.size)
        finally:
            self.kernel.LocalFree(ctypes.cast(out.data, ctypes.c_void_p))

    def seal(self, value): return self.transform(value)
    def open(self, value): return self.transform(value, True)


def owner_key(user):
    if not isinstance(user, str) or not user:
        raise JobError('Não autenticado.', 401)
    return hashlib.sha256(('iald-chat-job:' + user).encode()).hexdigest()


def validate_id(value):
    try:
        result = str(uuid.UUID(str(value)))
    except (ValueError, TypeError, AttributeError):
        raise JobError('Identificador inválido.') from None
    if result != value:
        raise JobError('Identificador inválido.')
    return result


def sse_events(chunks):
    decoder = codecs.getincrementaldecoder('utf-8')()
    buffer, parts = '', []
    for chunk in chunks:
        buffer += decoder.decode(chunk) if isinstance(chunk, bytes) else str(chunk)
        if len(buffer) > MAX_EVENT_BYTES:
            raise JobError('Evento excedeu o tamanho suportado.', 413)
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            line = line.rstrip('\r')
            if line.startswith('data:'):
                parts.append(line[5:].removeprefix(' '))
            elif not line and parts:
                yield '\n'.join(parts)
                parts = []
    buffer += decoder.decode(b'', final=True)
    if buffer.startswith('data:'):
        parts.append(buffer[5:].strip())
    if parts:
        yield '\n'.join(parts)


class ChatJobs:
    def __init__(self, directory, cipher=None, notify=None, max_active=8):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        self.path = directory / 'jobs.sqlite3'
        self.cipher = cipher or WindowsCipher()
        self.notify = notify
        self.max_active = max_active
        self.lock = threading.RLock()
        self.controls = {}
        self.active_owners = {}
        with self.db() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS jobs(
                    id TEXT PRIMARY KEY, owner TEXT NOT NULL, digest TEXT NOT NULL,
                    conversation_id TEXT NOT NULL, status TEXT NOT NULL,
                    created REAL NOT NULL, updated REAL NOT NULL, acknowledged INTEGER DEFAULT 0,
                    cancel_requested INTEGER DEFAULT 0, seq INTEGER DEFAULT 0,
                    size INTEGER DEFAULT 0, error TEXT, expired INTEGER DEFAULT 0);
                CREATE INDEX IF NOT EXISTS jobs_owner ON jobs(owner,created);
                CREATE TABLE IF NOT EXISTS events(job TEXT NOT NULL,seq INTEGER NOT NULL,data BLOB NOT NULL,
                    PRIMARY KEY(job,seq));
            ''')
            db.execute("UPDATE jobs SET status='interrupted',error=?,updated=? WHERE status IN ('queued','running')",
                       ('O servidor reiniciou antes da conclusão. O pedido não foi reenviado.', time.time()))
        self.cleanup()

    @contextmanager
    def db(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA secure_delete=ON')
            with db: yield db
        finally:
            db.close()

    def cleanup(self):
        with self.lock, self.db() as db:
            db.execute('DELETE FROM events WHERE job IN (SELECT id FROM jobs WHERE updated<? AND status NOT IN (\'queued\',\'running\'))', (time.time()-RETENTION,))
            db.execute("UPDATE jobs SET expired=1,size=0 WHERE updated<? AND status NOT IN ('queued','running')", (time.time()-RETENTION,))

    def _row(self, db, owner, job_id):
        row = db.execute('SELECT * FROM jobs WHERE id=? AND owner=?', (job_id, owner_key(owner))).fetchone()
        if not row:
            raise JobError('Resposta não encontrada.', 404)
        return row

    @staticmethod
    def _public(row):
        return {key: row[key] for key in ('id', 'conversation_id', 'status', 'created', 'updated',
                                         'cancel_requested', 'error', 'expired')}

    def submit(self, owner, payload, produce, *, admit=None):
        job_id = validate_id(payload.get('request_id'))
        body = dict(payload)
        body.pop('request_id')
        conv = body.get('iald_conv')
        if not isinstance(conv, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', conv):
            raise JobError('Conversa inválida.')
        if body.get('stream') is not True or not isinstance(body.get('messages'), list) or not body['messages']:
            raise JobError('Envie mensagens com stream: true.')
        if len(body['messages']) > 1000 or any(not isinstance(m, dict) for m in body['messages']):
            raise JobError('Mensagens inválidas.')
        canonical = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
        if len(canonical) > 20 * 1024 * 1024:
            raise JobError('Mensagem excede o tamanho suportado.', 413)
        digest = hashlib.sha256(canonical).hexdigest()
        key = owner_key(owner)
        self.cleanup()
        with self.lock, self.db() as db:
            old = db.execute('SELECT * FROM jobs WHERE id=?', (job_id,)).fetchone()
            if old:
                if old['owner'] != key: raise JobError('Resposta não encontrada.', 404)
                if old['digest'] != digest: raise JobError('Este envio já existe com outro conteúdo.', 409)
                return self._public(old)
            if key in self.active_owners.values() or db.execute("SELECT 1 FROM jobs WHERE owner=? AND status IN ('queued','running')", (key,)).fetchone():
                raise JobError('Uma resposta sua já está em andamento. Abra essa conversa para acompanhar.', 409)
            if max(len(self.controls), db.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]) >= self.max_active:
                raise JobError('Há muitas respostas em andamento. Aguarde um momento.', 429)
            if db.execute('SELECT count(*) FROM jobs WHERE owner=? AND created>?', (key,time.time()-60)).fetchone()[0] >= 20:
                raise JobError('Muitos pedidos. Aguarde um momento.', 429)
            if db.execute('SELECT coalesce(sum(size),0) FROM jobs WHERE owner=?', (key,)).fetchone()[0] > 128*1024*1024:
                raise JobError('Armazenamento temporário ocupado. Limpe respostas antigas.', 429)
            if db.execute('SELECT coalesce(sum(size),0) FROM jobs').fetchone()[0] > 2*1024**3:
                raise JobError('Armazenamento temporário indisponível.', 503)
            now = time.time()
            db.execute('INSERT INTO jobs(id,owner,digest,conversation_id,status,created,updated) VALUES(?,?,?,?,?,?,?)',
                       (job_id,key,digest,conv,'queued',now,now))
            result = self._public(self._row(db, owner, job_id))
            stop = threading.Event()
            self.controls[job_id] = stop
            self.active_owners[job_id] = key
        if admit is not None:
            try:
                admit(job_id, body)
            except Exception:
                self._finish(job_id, 'failed', 'A memória recusou a admissão; nenhum reenvio automático.')
                with self.lock:
                    self.controls.pop(job_id, None); self.active_owners.pop(job_id, None)
                raise JobError('A memória da atividade precisa de conferência.', 409) from None
        thread = threading.Thread(target=self._run, args=(owner,job_id,produce,body,stop), daemon=True,
                                  name='iald-chat-'+job_id[:8])
        try:
            thread.start()
        except Exception:
            self._finish(job_id,'failed','Não foi possível iniciar esta resposta.')
            with self.lock:
                self.controls.pop(job_id,None);self.active_owners.pop(job_id,None)
            raise JobError('Não foi possível iniciar esta resposta.',503) from None
        return result

    def append(self, job_id, data):
        raw = data.encode('utf-8')
        sealed = self.cipher.seal(raw)
        withdrawn = False
        try: withdrawn = json.loads(data).get('iald_aviso',{}).get('retirar_resposta') is True
        except (ValueError, AttributeError): pass
        with self.lock, self.db() as db:
            row = db.execute('SELECT seq,size,expired FROM jobs WHERE id=?',(job_id,)).fetchone()
            if not row or row['expired']: raise InterruptedError('Deleted')
            if (0 if withdrawn else row['size']) + len(sealed) > MAX_EVENT_BYTES:
                raise JobError('Resposta excedeu o armazenamento temporário.')
            if withdrawn: db.execute('DELETE FROM events WHERE job=?',(job_id,))
            seq = row['seq']+1
            db.execute('INSERT INTO events VALUES(?,?,?)',(job_id,seq,sealed))
            db.execute('UPDATE jobs SET seq=?,size=?,updated=? WHERE id=?',
                       (seq,(0 if withdrawn else row['size'])+len(sealed),time.time(),job_id))

    def _finish(self, job_id, status, error=None):
        with self.lock, self.db() as db:
            db.execute('UPDATE jobs SET status=?,error=?,updated=? WHERE id=?',(status,error,time.time(),job_id))

    def _run(self, owner, job_id, produce, body, stop):
        status, error, done, warned, has_answer = 'failed', None, False, False, False
        source = None
        try:
            self._finish(job_id,'running')
            if stop.is_set(): raise InterruptedError()
            source = produce(body, stop)
            for event in sse_events(source):
                if stop.is_set(): raise InterruptedError()
                if event.strip() == '[DONE]':
                    done = True
                else:
                    try:
                        obj = json.loads(event)
                        warned = warned or bool(obj.get('iald_aviso') or obj.get('error'))
                        has_answer = has_answer or any(bool(c.get('delta',{}).get('content')) for c in obj.get('choices',[]))
                    except (ValueError,AttributeError): pass
                self.append(job_id,event)
                if done: break
            if not done: raise RuntimeError('Missing stream terminator')
            if warned:
                status, error = 'failed', 'A resposta terminou com uma falha registrada; o pedido foi preservado, sem reenvio.'
            else:
                status = 'completed'
        except InterruptedError:
            status,error = 'cancelled','Resposta interrompida a seu pedido.'
        except Exception:
            status,error = 'failed','A geração foi interrompida. O pedido não foi reenviado automaticamente.'
        finally:
            if source is not None:
                try: source.close()
                except Exception: pass
            if stop.is_set(): status,error='cancelled','Resposta interrompida a seu pedido.'
            self._finish(job_id,status,error)
            activity_binding = getattr(produce, 'activity_binding', None)
            if activity_binding is not None:
                try:
                    activity_binding.checkpoint('chat_job.' + job_id + '.' + status,
                        {'job_id': job_id, 'request_id': activity_binding.request_id,
                         'status': status, 'automatic_retry': False})
                    if status != 'completed': activity_binding.uncertain()
                except Exception:
                    # The existing durable job remains terminal; memory failure
                    # is explicit and cannot grant a new provider execution.
                    self._finish(job_id, 'failed', 'Retorno custodiado; conciliação da memória pendente.')
            with self.lock:
                self.controls.pop(job_id,None);self.active_owners.pop(job_id,None)
        if status == 'completed' and has_answer and not warned and self.notify:
            try: self.notify(owner,job_id)
            except Exception: pass  # Stored answer remains available if push delivery fails.

    def get(self, owner, job_id, after=0, limit=200):
        validate_id(job_id)
        if not isinstance(after,int) or after<0: raise JobError('Cursor inválido.')
        self.cleanup()
        with self.lock, self.db() as db:
            row = self._row(db,owner,job_id)
            if row['expired']: raise JobError('Esta resposta temporária expirou.',410)
            data = db.execute('SELECT seq,data FROM events WHERE job=? AND seq>? ORDER BY seq LIMIT ?',
                              (job_id,after,limit)).fetchall()
            result = self._public(row)
        events, size = [], 0
        for item in data:
            text = self.cipher.open(item['data']).decode()
            if events and size+len(text)>256000: break
            events.append({'seq':item['seq'],'data':text});size+=len(text)
        cursor = events[-1]['seq'] if events else after
        result.update(events=events,cursor=cursor,has_more=cursor<row['seq'])
        return result

    def list(self, owner):
        self.cleanup()
        with self.lock, self.db() as db:
            rows=db.execute('SELECT * FROM jobs WHERE owner=? AND acknowledged=0 AND expired=0 ORDER BY created DESC LIMIT 100',
                            (owner_key(owner),)).fetchall()
        return [self._public(row) for row in rows]

    def cancel(self, owner, job_id):
        with self.lock, self.db() as db:
            row=self._row(db,owner,validate_id(job_id))
            if row['status'] not in TERMINAL:
                db.execute('UPDATE jobs SET cancel_requested=1 WHERE id=?',(job_id,))
                if job_id in self.controls: self.controls[job_id].set()
            return self._public(self._row(db,owner,job_id))

    def ack(self, owner, job_id):
        with self.lock, self.db() as db:
            row=self._row(db,owner,validate_id(job_id))
            if row['status'] not in TERMINAL: raise JobError('Resposta ainda em andamento.',409)
            db.execute('UPDATE jobs SET acknowledged=1 WHERE id=?',(job_id,))

    def purge(self, owner, conversation=None):
        with self.lock, self.db() as db:
            where='owner=?';args=[owner_key(owner)]
            if conversation is not None: where+=' AND conversation_id=?';args.append(conversation)
            ids=[r[0] for r in db.execute('SELECT id FROM jobs WHERE '+where,args)]
            for job_id in ids:
                if job_id in self.controls: self.controls[job_id].set()
                db.execute('DELETE FROM events WHERE job=?',(job_id,))
            # Conversation deletion keeps a tombstone, preventing uncertain sends repeating.
            if conversation is None: db.execute('DELETE FROM jobs WHERE '+where,args)
            else: db.execute("UPDATE jobs SET status='cancelled',expired=1,acknowledged=1,size=0 WHERE "+where,args)


def register(app, root, notify=None, account_key=owner_key):
    from flask import request, session, jsonify, g
    manager, init_lock = [], threading.Lock()

    def store():
        with init_lock:
            if not manager:
                manager.append(ChatJobs(Path(root)/'.iald_runtime'/'chat_jobs',notify=notify))
        return manager[0]

    app.extensions['iald_chat_jobs'] = store

    def result(fn):
        try: response=jsonify(fn())
        except JobError as exc: response=jsonify(error=str(exc));response.status_code=exc.status
        response.headers['Cache-Control']='private, no-store'
        return response

    @app.route('/api/chat-jobs/session')
    def chat_jobs_session():
        return result(lambda:{'account':account_key(session.get('username',''))})

    @app.route('/api/chat-jobs',methods=['GET','POST'])
    def chat_jobs_collection():
        user=session.get('username','')
        if request.method=='GET': return result(lambda:{'account':account_key(user),'jobs':store().list(user)})
        if not request.is_json: return jsonify(error='Envie application/json.'),415
        data=request.get_json(silent=True)
        if not isinstance(data,dict): return jsonify(error='Envie um objeto JSON.'),400
        if data.pop('account',None) != account_key(user):
            return jsonify(error='A conta mudou. Entre novamente antes de enviar.'),409
        # Authentication is revalidated by existing middleware inside the worker.
        principal = account_key(user)
        snapshot=dict(session)
        headers={k:request.headers[k] for k in ('Authorization','Origin','X-IALD-Context','User-Agent') if k in request.headers}

        def produce(body, stop):
            with app.test_request_context('/v1/chat/completions',method='POST',json=body,headers=headers):
                session.update(snapshot)
                if account_key(user) != principal:
                    raise PermissionError('Account generation changed before worker dispatch')
                g.iald_wallet_job_id = data['request_id']
                g.iald_activity_binding = produce.activity_binding
                response=app.full_dispatch_request()
                try:
                    if response.status_code!=200 or response.mimetype!='text/event-stream':
                        raise RuntimeError('Chat rejected before stream')
                    for piece in response.response:
                        if stop.is_set():
                            control=getattr(response,'iald_task_control',None)
                            if control is not None: control.cancel.set()
                            raise InterruptedError()
                        yield piece
                finally:
                    response.close()

        def admit(job_id, body):
            # Client key only selects an idempotent job. The server derives and
            # persists the activity request identity under this account generation.
            request_id = 'job_' + app_memory.digest(principal + ':' + job_id)
            binding = app_memory.begin(root, principal, body['iald_conv'], body['messages'], request_id)
            binding.checkpoint('chat_job.' + job_id + '.queued',
                {'job_id': job_id, 'request_id': request_id, 'status': 'queued', 'automatic_retry': False})
            produce.activity_binding = binding

        response=result(lambda:store().submit(user,data,produce,admit=admit))
        if response.status_code==200: response.status_code=202
        return response

    @app.route('/api/chat-jobs/<job_id>')
    def chat_jobs_item(job_id):
        def read():
            try: cursor=int(request.args.get('after','0'))
            except ValueError: raise JobError('Cursor inválido.') from None
            return store().get(session.get('username',''),job_id,cursor)
        return result(read)

    @app.route('/api/chat-jobs/<job_id>/<action>',methods=['POST'])
    def chat_jobs_action(job_id,action):
        if not request.is_json: return jsonify(error='Envie application/json.'),415
        def run():
            user=session.get('username','')
            if action=='cancel': return store().cancel(user,job_id)
            if action=='ack': store().ack(user,job_id);return {'ok':True}
            raise JobError('Ação não encontrada.',404)
        return result(run)

    @app.route('/api/chat-jobs/conversations/<conversation>/delete',methods=['POST'])
    def chat_jobs_delete_conversation(conversation):
        if not request.is_json: return jsonify(error='Envie application/json.'),415
        return result(lambda:(store().purge(session.get('username',''),conversation) or {'ok':True}))

    return store
