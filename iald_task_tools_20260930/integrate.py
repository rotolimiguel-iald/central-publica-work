"""Prepare exact server integration in staging, refusing ambiguous replacements."""
from pathlib import Path
import ast,json
W=Path(__file__).resolve().parent; S=W/'stage'
def change(name,edits):
    p=S/name;raw=p.read_bytes();text=raw.decode('utf-8')
    for old,new in edits:
        old=old.replace('\n','\r\n') if '\r\n' in text else old
        new=new.replace('\n','\r\n') if '\r\n' in text else new
        assert text.count(old)==1,(name,old[:100],text.count(old))
        text=text.replace(old,new)
    ast.parse(text);p.write_bytes(text.encode('utf-8'))

change('iald_auto_router.py',[
    ('import uuid\n','import uuid\nimport iald_task_policy as task_policy\n'),
    ("    context,source=memory_slice(root)\n", "    task=task_policy.classify(prompt)\n    candidates=task_policy.eligible_managers(candidates,task)\n    if not candidates:raise ValueError('no_tool_capable_manager')\n    context,source=memory_slice(root)\n"),
    ("'criteria':{k:DESCRIPTIONS[k] for k in candidates}","'criteria':task_policy.executor_criteria(candidates,DESCRIPTIONS,task)"),
    ("'candidates':list(candidates),'calls':[]", "'candidates':list(candidates),'task_category':task,'calls':[]"),
])
# Delegation needs text-only workers too. A trusted keyword (never HTTP input)
# distinguishes selecting an implementation worker from the user-facing manager.
change('iald_auto_router.py',[
    ('post=None,validation_probe=False):','post=None,validation_probe=False,worker=False):'),
    ('candidates=task_policy.eligible_managers(candidates,task)','candidates=list(candidates) if worker else task_policy.eligible_managers(candidates,task)'),
])
change('iald_task_bridge.py',[("args['objective'],candidates)","args['objective'],candidates,worker=True)")])

change('iald_app_providers.py',[
    ('import uuid\n','import uuid\nfrom iald_task_session import NAMES as TASK_TOOL_NAMES\n'),
    ("in TOOL_NAMES]\n        names =", "in (TOOL_NAMES | TASK_TOOL_NAMES)]\n        names ="),
    ('        for round_no in range(MAX_ROUNDS):','        rounds = 8 if names & TASK_TOOL_NAMES else MAX_ROUNDS\n        for round_no in range(rounds):'),
    ("if round_no == MAX_ROUNDS-1 else 'auto'", "if round_no == rounds-1 else 'auto'"),
    ('if not calls or round_no == MAX_ROUNDS-1:', 'if not calls or round_no == rounds-1:'),
    ("'rotulo': 'Consultando fontes da TGL',\n                                     'loop': round_no+1, 'max_loops': MAX_ROUNDS", "'rotulo': ('Executando etapa da tarefa' if name in TASK_TOOL_NAMES else 'Consultando fontes da TGL'),\n                                     'loop': round_no+1, 'max_loops': rounds"),
    ("'rotulo': 'Fonte consultada', 'chars': len(result)","'rotulo': ('Etapa concluída' if name in TASK_TOOL_NAMES else 'Fonte consultada'), 'chars': len(result)"),
])

bridge='''
def _new_app_task_scope(user):
    # Created only by the authenticated automatic route, not a body flag.
    def authorize(provider='task'):
        current=load_users_estrito().get(user,{})
        if not app_router.allowed(current,user) or not iald_motores.consentiu(current,app_router.AUTO):
            raise PermissionError('Pilot access revoked')
        if provider not in ('task',app_router.AUTO) and not iald_motores.consentiu(current,provider):
            raise PermissionError('Provider consent missing')
        if provider in app_providers.MODELS and not app_providers.allowed(current,user,provider):
            raise PermissionError('Provider unavailable for account')
        return current
    def options():
        current=authorize()
        return [row['id'] for row in _opcoes_de_motor(current,user)
                if row.get('disponivel') and iald_motores.consentiu(current,'claude' if row['id'].startswith('claude-') else row['id'])]
    def sandbox_config():
        current=authorize('claude')
        current=dict(current,**CLAUDE_ROUTES.select('claude-haiku',current,user))
        return CLAUDE_ROUTES.configuration(current,user)
    return task_bridge.make_scope(root=SERVE_DIR,user=user,authorize=authorize,options=options,
        package=CLAUDE_ROUTES.package,evaluation=APP_EVALUATION,providers=app_providers,router=app_router,
        sandbox_config=sandbox_config,client_factory=iald_motor_claude.cliente_para,
        guard_factory=lambda:_guarda_do_motor(iald_motores.CLAUDE),ledger=RAZAO_CLAUDE)


@app.route('/api/task-capabilities')
def api_task_capabilities():
    user=session.get('username','');record=load_users_estrito().get(user,{})
    if not app_router.allowed(record,user):return jsonify({'error':'Piloto não liberado.'}),403
    return jsonify(task_policy.capabilities())


@app.route('/api/task-artifacts/<artifact_id>')
def api_task_artifact(artifact_id):
    user=session.get('username','');record=load_users_estrito().get(user,{})
    if not app_router.allowed(record,user):return jsonify({'error':'Acesso negado.'}),403
    try:
        path,meta=task_artifacts.ArtifactStore(SERVE_DIR).resolve(user,artifact_id)
    except (ValueError,PermissionError,OSError,KeyError):return jsonify({'error':'Arquivo indisponível.'}),404
    response=send_file(path,as_attachment=True,download_name=meta['filename'],mimetype='application/octet-stream')
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Content-Security-Policy']="sandbox; default-src 'none'"
    response.headers['Cache-Control']='private, no-store'
    return response


'''

change('iald_web_server.py',[
    ('Flask, request, Response, send_from_directory,','Flask, request, Response, send_from_directory, send_file,'),
    ('import iald_auto_router as app_router','import iald_auto_router as app_router\nimport iald_task_policy as task_policy\nimport iald_task_session as task_session\nimport iald_task_artifacts as task_artifacts\nimport iald_task_bridge as task_bridge'),
    ('def _chat_automatico(req_json,user,registro,is_stream,tokens_in):',bridge+'def _chat_automatico(req_json,user,registro,is_stream,tokens_in):'),
    ('        selected=dict(current,motor=chosen)','        task_scope=_new_app_task_scope(user)\n        selected=dict(current,motor=chosen)'),
    ('return _chat_claude(req_json,user,selected,is_stream,tokens_in)','return _chat_claude(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope)'),
    ('return _chat_avaliacao(req_json,user,selected,is_stream,chosen)','return _chat_avaliacao(req_json,user,selected,is_stream,chosen,task_scope=task_scope)'),
    ('response=_chat_openai(req_json,user,selected,is_stream,tokens_in)','response=_chat_openai(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope)'),
    ('def _chat_openai(req_json, user, registro, is_stream, tokens_in):','def _chat_openai(req_json, user, registro, is_stream, tokens_in, *, task_scope=None):'),
    ('return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.OPENAI)','return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.OPENAI, task_scope=task_scope)'),
    ('def _chat_claude(req_json, user, registro, is_stream, tokens_in):','def _chat_claude(req_json, user, registro, is_stream, tokens_in, *, task_scope=None):'),
    ('return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.CLAUDE)','return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.CLAUDE, task_scope=task_scope)'),
    ('def _chat_avaliacao(req_json, user, registro, is_stream, motor):','def _chat_avaliacao(req_json, user, registro, is_stream, motor, *, task_scope=None):'),
    ('def _chat_externo(req_json, user, registro, is_stream, tokens_in, motor=iald_motores.OPENAI):','def _chat_externo(req_json, user, registro, is_stream, tokens_in, motor=iald_motores.OPENAI, *, task_scope=None):'),
    ("        if search_instruction: note += '\\n'+iald_motores.LUPA_CANONICA", "        if task_scope: note += '\\n'+task_policy.INSTRUCTIONS\n        if search_instruction: note += '\\n'+iald_motores.LUPA_CANONICA"),
    ("        if motor == 'kimi':\n            # The official", "        if task_scope and motor != 'kimi':definitions += task_scope.tools\n        if motor == 'kimi':\n            # The official"),
    ("        lambda name, args: _executar_ferramenta_claude(name, args, user=user, operator_authorized=False),", "        lambda name, args: (task_scope.execute(name,args) if task_scope and name in task_session.NAMES else\n            _executar_ferramenta_claude(name, args, user=user, operator_authorized=False)),"),
    ('        usar_agente = bool(permitidas) and (haiku or cfg.memoria_modo', '        if task_scope:\n            permitidas += task_scope.tools\n            instrucao += "\\n"+task_policy.INSTRUCTIONS\n        usar_agente = bool(permitidas) and (task_scope is not None or haiku or cfg.memoria_modo'),
    ('            def gerar():\n                try:\n                    yield from agent_loop(para_openai',
     '''            if task_scope:
                original_executor=executor or execute_public_tool
                def task_executor(name,args,**kwargs):
                    if name in task_session.NAMES:return json.dumps(task_scope.execute(name,args),ensure_ascii=False)
                    return original_executor(name,args,**kwargs)
                executor=task_executor

            def gerar():
                try:
                    yield from agent_loop(para_openai'''),
])
print(json.dumps({'status':'STAGED','modules':['iald_web_server.py','iald_auto_router.py','iald_app_providers.py']}))
