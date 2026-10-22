"""Flask adapter; coordinator must place upload guard before global body guard."""
from private_media_store import MAX_RAW_BYTES,MAX_CHAT_JSON_BYTES,MediaError,MediaUnavailable


def register_private_media(app,store,*,host_scope,authenticate_csrf,upload_eligible):
    """Callbacks authenticate server scope; picker/upload grants no model consent.

    host_scope(conversation_id) verifies account generation AND owner-scoped valid conversation namespace; first upload need not have a job.
    upload_eligible(scope) checks access/rate/storage policy, not paid dispatch.
    MiMo2/Auto3, wallet and revocation remain at actual dispatch, never autogrant.
    """
    from flask import request,jsonify
    # Parent owns _RequisicaoIALD property glue. Never assign request limit here:
    # its current production property is read-only. Verify exact bound below.
    @app.before_request
    def private_media_upload_guard():
        if request.path!='/api/private-media' or request.method!='POST':return
        if authenticate_csrf() is not True:return jsonify(error='Authentication/CSRF required'),403
        if request.content_length is None:return jsonify(error='Content-Length required'),411
        if not 0<request.content_length<=MAX_RAW_BYTES:return jsonify(error='Upload exceeds server media byte limit',max_media_bytes=MAX_RAW_BYTES),413
        if request.max_content_length!=MAX_RAW_BYTES:
            return jsonify(error='Upload route limit not active; upload disabled'),503

    @app.post('/api/private-media')
    def private_media_upload():
        try:
            scope=host_scope(request.args.get('conversation_id'))
            if upload_eligible(scope) is not True:return jsonify(error='Private media upload unavailable'),403
            result=store.put(request.stream,scope=scope,mime=request.mimetype,content_length=request.content_length)
            return jsonify(result),201
        except MediaUnavailable:return jsonify(error='Media unavailable'),404
        except (MediaError,ValueError):return jsonify(error='Media validation or storage admission refused; history unchanged'),400

    @app.get('/api/private-media/<media_ref>')
    def private_media_metadata(media_ref):
        try:
            if authenticate_csrf() is not True:return jsonify(error='Authentication required'),403
            scope=host_scope(request.args.get('conversation_id'))
            return jsonify(store.metadata(media_ref,scope)),200
        except (MediaError,ValueError):return jsonify(error='Media unavailable'),404

    # No public/private raw download route. No automatic expiration/deletion.
    return {'upload_guard':private_media_upload_guard,'max_chat_json_bytes':MAX_CHAT_JSON_BYTES}
