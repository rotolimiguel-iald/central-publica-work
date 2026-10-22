from pathlib import Path
import hashlib,json
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
p=ROOT/'iald_web_server.py';raw=p.read_bytes();source=raw.decode('utf-8')
needle='if __name__ == "__main__":'
assert source.count(needle)==1
source=source.replace(needle,'''# Chat jobs retain encrypted output while the mobile WebView is suspended.
import iald_chat_jobs
import iald_notification_runtime
def _push_token_expiry(token):
    _, issued = _serializador_token().loads(token, max_age=TOKEN_APP_MAX_AGE, return_timestamp=True)
    return issued.timestamp() + TOKEN_APP_MAX_AGE

NOTIFY_RESPONSE, PURGE_PUSH = iald_notification_runtime.register(
    app, SERVE_DIR, ORIGENS_APP, load_users_estrito, _conta_bloqueada, token_expiry=_push_token_expiry)
def _chat_account_generation(username):
    record = load_users_estrito().get(username)
    if not record:
        raise iald_chat_jobs.JobError('Não autenticado.', 401)
    material = 'iald-account:' + username + ':' + str(record.get('created', 'legacy'))
    return hashlib.sha256(material.encode('utf-8')).hexdigest()

CHAT_JOBS = iald_chat_jobs.register(app, SERVE_DIR, notify=NOTIFY_RESPONSE,
                                     account_key=_chat_account_generation)


'''+needle)
needle='        del usuarios[username]\n        save_users(usuarios)'
assert source.count(needle)==1
source=source.replace(needle,'        CHAT_JOBS().purge(username)\n        PURGE_PUSH(username)\n'+needle)
needle='        del USERS[username]\n        save_users(USERS)'
assert source.count(needle)==1
source=source.replace(needle,'        CHAT_JOBS().purge(username)\n        PURGE_PUSH(username)\n'+needle)
(W/'server'/'iald_web_server.py').write_bytes(source.encode('utf-8'))
(W/'baseline_server.json').write_text(json.dumps({p.name:hashlib.sha256(raw).hexdigest()}),encoding='utf-8')
compile(source,str(p),'exec')
print('Server staged; production unchanged.')
