"""Two-file stage. No runtime imports, credentials, requests or source writes."""
import json,hashlib,difflib
from pathlib import Path
S=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
files=[]
def stage(name,transform):
 p=R/name;raw=p.read_bytes();text=p.read_text(encoding='utf-8');new=transform(text);compile(new,str(S/name),'exec')
 with (S/name).open('xb') as f:f.write(new.encode())
 with (S/(name+'.diff')).open('x',encoding='utf-8') as f:f.write(''.join(difflib.unified_diff(text.splitlines(True),new.splitlines(True),fromfile=str(p),tofile=str(S/name))))
 files.append({'source':str(p),'source_sha256':hashlib.sha256(raw).hexdigest(),'staged':str(S/name),'staged_sha256':hashlib.sha256(new.encode()).hexdigest()})
def once(text,old,new):
 assert text.count(old)==1,(old[:80],text.count(old));return text.replace(old,new)
POLICY='''
NEW_AV_ERROR = 'Novos anexos de áudio e vídeo estão indisponíveis. Imagens, documentos e histórico permanecem acessíveis.'
NEW_AV_CODE = 'new_audio_video_disabled'


def _audio_video(value, depth=0):
    # Inspect typed payloads, not quoted/embedded JSON or old conversation turns.
    if depth > 32:
        raise ValueError('Attachment structure exceeds admission depth')
    if isinstance(value, str):
        return value.lstrip().lower().startswith(('data:audio/', 'data:video/'))
    if isinstance(value, list):
        return any(_audio_video(v, depth + 1) for v in value)
    if not isinstance(value, dict):
        return False
    kind = str(value.get('type', '')).lower()
    if kind in ('input_audio', 'audio', 'audio_url', 'input_video', 'video', 'video_url', 'iald_media'):
        return True
    if any(k in value and value[k] is not None for k in
            ('input_audio', 'audio_url', 'video_url', 'input_video')):
        return True
    mime = str(value.get('mime', value.get('mime_type', value.get('media_type', '')))).lower()
    if mime.startswith(('audio/', 'video/')):
        return True
    return any(_audio_video(v, depth + 1) for v in value.values())


def has_new_audio_video(payload):
    if not isinstance(payload, dict):
        return False  # Existing JSON/schema guards remain authoritative.
    messages = payload.get('messages')
    if isinstance(messages, list) and messages and isinstance(messages[-1], dict):
        latest = messages[-1]
        if latest.get('role') == 'user' and _audio_video(latest.get('content')):
            return True
    # Legacy top-level attachment envelopes are new input, never history.
    if any(k in payload and payload[k] is not None for k in
            ('audio', 'input_audio', 'audio_url', 'video', 'input_video', 'video_url')):
        return True
    return any(_audio_video(payload[k]) for k in ('attachments', 'files') if k in payload)

'''
def routes(text):
 text=once(text,'\n\ndef register_private_media', '\n'+POLICY+'\ndef register_private_media')
 start=text.index("        if request.content_length is None:return")
 end=text.index("\n    @app.get('/api/private-media/<media_ref>')",start)
 replacement='''        # This binary endpoint only creates new audio/video custody.
        # Authenticate partition first; never read/store/probe the rejected body.
        return jsonify(error=NEW_AV_ERROR,code=NEW_AV_CODE),415

    @app.before_request
    def new_audio_video_post_guard():
        if request.method != 'POST' or request.path.rstrip('/') not in (
                '/api/chat-jobs', '/v1/chat/completions', '/v1/completions'):
            return
        if not request.is_json:
            return  # Existing route/body guards reject unsupported envelopes.
        try:
            blocked = has_new_audio_video(request.get_json(silent=True))
        except ValueError:
            return jsonify(error='Estrutura de anexo inválida.'),400
        if blocked:
            return jsonify(error=NEW_AV_ERROR,code=NEW_AV_CODE),415

    @app.post('/api/private-media')
    def private_media_upload():
        return jsonify(error=NEW_AV_ERROR,code=NEW_AV_CODE),415
'''
 return text[:start]+replacement+text[end:]
def providers(text):
 text=once(text,"label='DeepSeek V4.1 Flash'","label='DeepSeek V4.1 Flash (1017)', model_version='DeepSeek-V4.1-Flash-1017'")
 text=once(text,"rates=(0.30, 0.006, 1.20), price_source=", "rates=(0.30, 0.006, 1.20), rates_off_peak=(0.15, 0.003, 0.60),\n        estimate_policy='peak_upper_estimate_not_invoice', price_verified_on='2026-10-21',\n        release_note='2026-10-17: API e tarifas inalteradas; ganhos de eficiência declarados pelo fornecedor',\n        price_source=")
 return text
stage('private_media_routes.py',routes);stage('iald_app_providers.py',providers)
with (S/'SOURCE_PLAN.json').open('x',encoding='utf-8') as f:json.dump({'status':'STAGED_NOT_INSTALLED','files':files},f,ensure_ascii=False,indent=2)
print(json.dumps({'files':len(files)}))
