from pathlib import Path
import json,hashlib
W=Path(__file__).parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
stage=W/'stage';stage.mkdir(exist_ok=True)
names=['iald_web_server.py','iald_task_artifacts.py','iald_task_policy.py','iald_task_session.py']
baseline={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
(W/'baseline.json').write_text(json.dumps(baseline,indent=2),encoding='utf-8')
def change(name,replacements):
    raw=(ROOT/name).read_bytes()
    for old,new in replacements:
        old=old.replace('\n','\r\n').encode() if b'\r\n' in raw else old.encode()
        new=new.replace('\n','\r\n').encode() if b'\r\n' in raw else new.encode()
        assert raw.count(old)==1,(name,old[:90],raw.count(old))
        raw=raw.replace(old,new)
    (stage/name).write_bytes(raw)

routes='''@app.route('/api/task-artifacts/<artifact_id>/view')
def api_task_artifact_view(artifact_id):
    user=session.get('username','');record=load_users_estrito().get(user,{})
    if not app_router.allowed(record,user):return jsonify({'error':'Acesso negado.'}),403
    try:
        data=artifact_view.describe(task_artifacts.ArtifactStore(SERVE_DIR),user,artifact_id)
    except (ValueError,PermissionError,OSError,KeyError):return jsonify({'error':'Arquivo indisponível.'}),404
    response=jsonify(data)
    response.headers.update(artifact_view.PRIVATE_HEADERS)
    return response


@app.route('/api/task-artifacts/<artifact_id>/access',methods=['POST'])
def api_task_artifact_access(artifact_id):
    user=session.get('username','');record=load_users_estrito().get(user,{})
    if not app_router.allowed(record,user):return jsonify({'error':'Acesso negado.'}),403
    data,error=_identificacao_json_post(set())
    if error is not None:return error
    try:
        data=artifact_view.access(task_artifacts.ArtifactStore(SERVE_DIR),user,artifact_id)
    except (ValueError,PermissionError,OSError,KeyError):return jsonify({'error':'Arquivo indisponível.'}),404
    response=jsonify(data)
    response.headers.update(artifact_view.PRIVATE_HEADERS)
    return response


@app.route('/task-view/<artifact_id>/<token>')
def task_view(artifact_id,token):
    try:
        page=artifact_view.ticket_page(task_artifacts.ArtifactStore(SERVE_DIR),artifact_id,token)
    except (ValueError,PermissionError,OSError,KeyError):
        response=Response('Link inválido ou expirado. Volte à IALD e toque no arquivo para abrir novamente.',status=404)
    else:
        response=Response(page,mimetype='text/html')
    response.headers.update(artifact_view.PRIVATE_HEADERS)
    response.headers['Content-Security-Policy']=artifact_view.PAGE_CSP
    return response


'''
change('iald_web_server.py',[
    ('import iald_task_artifacts as task_artifacts','import iald_task_artifacts as task_artifacts\nimport iald_artifact_view as artifact_view'),
    ('"offline_page", "task_download",','"offline_page", "task_download", "task_view",'),
    ("@app.route('/task-download/<artifact_id>/<token>')",routes+"@app.route('/task-download/<artifact_id>/<token>')"),
    ('(/task-download/[A-Za-z0-9_-]+/)','(/task-(?:download|view)/[A-Za-z0-9_-]+/)'),
])
change('iald_task_artifacts.py',[
    ('def _artifact_url(artifact_id):\n    return PUBLIC_BASE_URL + "/api/task-artifacts/" + artifact_id',
     'def _artifact_url(artifact_id):\n    return PUBLIC_BASE_URL + "/api/task-artifacts/" + artifact_id\n\ndef app_artifact_url(artifact_id):\n    _uuid(artifact_id)\n    return PUBLIC_BASE_URL + "/app/index.html?artifact=" + artifact_id'),
    ('"Show the authenticated url AND temporary mobile_url with its expires_at UTC timestamp. "',
     '"Show app_url as the main clickable link (open/view file in IALD). It does not expire; the app authenticates its owner and prepares downloads on demand. "'),
    ('        public.update(ticket)','        public.update(ticket)\n        public["app_url"] = app_artifact_url(artifact_id)'),
])
change('iald_task_session.py',[
    ('import iald_task_policy as policy','import iald_task_policy as policy\nfrom iald_task_artifacts import app_artifact_url'),
    ('metadata.update(mobile_url=mobile_url,expires_at=ticket_meta[\'expires_at\'])',
     'metadata.update(mobile_url=mobile_url,expires_at=ticket_meta[\'expires_at\'],app_url=app_artifact_url(artifact_id))'),
])
change('iald_task_policy.py',[
    ("'website': 'Página HTML para baixar; publicar é uma etapa separada.'", "'website': 'Página HTML com prévia privada na IALD e download; publicar é uma etapa separada.'"),
    ('Página HTML é arquivo baixável. Ferramentas não acessam arquivos locais da Central.',
     'Página HTML possui prévia privada na IALD e arquivo baixável. Isso não publica um site na internet. Ferramentas não acessam arquivos locais da Central.'),
    ('de artefatos retornados pelas ferramentas, nunca inventados. Para iPhone use o link\nmobile_url temporário, se presente, e também preserve o url autenticado do arquivo.',
     'de artefatos retornados pelas ferramentas, nunca inventados. Mostre app_url como\nlink principal com rótulo "Ver página na IALD" para HTML, ou "Abrir arquivo na IALD".\nO app abre a prévia e prepara links válidos para baixar, sem pedir nova geração à IA.\nurl e mobile_url são alternativas; este último vence no expires_at UTC informado.\nNunca apresente um arquivo gerado como site público já hospedado.'),
])
print(json.dumps({'staged':names,'baseline':baseline}))
