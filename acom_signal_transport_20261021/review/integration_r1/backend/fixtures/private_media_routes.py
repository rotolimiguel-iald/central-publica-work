"""Flask adapter; coordinator must place upload guard before global body guard."""
import hmac
import re
from private_media_store import MAX_RAW_BYTES,MAX_CHAT_JSON_BYTES,MediaError,MediaUnavailable,media_scope_token


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


def register_private_media(app,store,*,host_scope,authenticate_csrf,upload_eligible):
    """Callbacks authenticate server scope; picker/upload grants no model consent.

    host_scope(conversation_id) verifies account generation AND owner-scoped valid conversation namespace; first upload need not have a job.
    upload_eligible(scope) checks access/rate/storage policy, not paid dispatch.
    MiMo2/Auto3, wallet and revocation remain at actual dispatch, never autogrant.
    """
    from flask import request,jsonify,g
    def checked_scope():
        # Partition CAS only: authoritative identity always comes from host auth.
        values=request.args.getlist("expected_media_scope")
        if len(values)!=1 or re.fullmatch(r"[0-9a-f]{32}",values[0]) is None:
            raise MediaError("Expected media partition required")
        scope=host_scope(request.args.get("conversation_id"))
        token=media_scope_token(scope)
        if not hmac.compare_digest(values[0],token):
            raise MediaError("Account context changed")
        return scope,token
    # Parent owns _RequisicaoIALD property glue. Never assign request limit here:
    # its current production property is read-only. Verify exact bound below.
    @app.before_request
    def private_media_upload_guard():
        if request.path!='/api/private-media' or request.method!='POST':return
        if authenticate_csrf() is not True:return jsonify(error='Authentication/CSRF required'),403
        try:g.private_media_scope,g.private_media_token=checked_scope()
        except (MediaError,ValueError):return jsonify(error='Media account context mismatch; refresh capabilities'),403
        # This binary endpoint only creates new audio/video custody.
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

    @app.get('/api/private-media/<media_ref>')
    def private_media_metadata(media_ref):
        try:
            if authenticate_csrf() is not True:return jsonify(error='Authentication required'),403
            try:scope,token=checked_scope()
            except (MediaError,ValueError):return jsonify(error='Media account context mismatch; refresh capabilities'),403
            return jsonify(dict(store.metadata(media_ref,scope),media_scope=token)),200
        except (MediaError,ValueError):return jsonify(error='Media unavailable'),404

    # No public/private raw download route. No automatic expiration/deletion.
    return {'upload_guard':private_media_upload_guard,'max_chat_json_bytes':MAX_CHAT_JSON_BYTES}
