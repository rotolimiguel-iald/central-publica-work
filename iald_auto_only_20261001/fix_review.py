from pathlib import Path
S=Path(__file__).parent/'stage'
def edit(name,old,new,count=1):
 p=S/name;t=p.read_text(encoding='utf-8');assert t.count(old)==count,(name,old[:90],t.count(old));p.write_text(t.replace(old,new),encoding='utf-8')
p='iald_app_providers.py'
edit(p,"account_key='operator', spending=None, task_control=None):", "account_key='operator', spending=None, task_control=None, authorize=None):")
edit(p,"                    result = adapter(provider).execute(prompt, cancel=cancel)", "                    if authorize is not None:authorize()\n                    result = adapter(provider).execute(prompt, cancel=cancel)")
edit(p,"active_response, record, started, http_post, spending)", "active_response, record, started, http_post, spending, authorize)")
edit(p,"record, started, http_post, spending=None):", "record, started, http_post, spending=None, authorize=None):")
edit(p,"                if spending is not None: spending.before(provider, body, bound)", "                if authorize is not None:authorize()\n                if spending is not None: spending.before(provider, body, bound)")
edit(p,"                response = (http_post or requests.post)", "                if authorize is not None:authorize()\n                response = (http_post or requests.post)")
edit('iald_task_bridge.py',"spending=spending_factory(chosen) if spending_factory else None)", "spending=spending_factory(chosen) if spending_factory else None,authorize=lambda:auth(chosen))")
s='iald_web_server.py'
for name in ('_chat_openai','_chat_claude'):
 edit(s,f'def {name}(req_json, user, registro, is_stream, tokens_in, *, task_scope=None):',f'def {name}(req_json, user, registro, is_stream, tokens_in, *, task_scope=None, dispatch_check=None):')
for motor in ('OPENAI','CLAUDE'):
 edit(s,f'iald_motores.{motor}, task_scope=task_scope)',f'iald_motores.{motor}, task_scope=task_scope, dispatch_check=dispatch_check)')
edit(s,'def _chat_externo(req_json, user, registro, is_stream, tokens_in, motor=iald_motores.OPENAI, *, task_scope=None):','def _chat_externo(req_json, user, registro, is_stream, tokens_in, motor=iald_motores.OPENAI, *, task_scope=None, dispatch_check=None):')
edit(s,'def _chat_avaliacao(req_json, user, registro, is_stream, motor, *, task_scope=None):','def _chat_avaliacao(req_json, user, registro, is_stream, motor, *, task_scope=None, dispatch_check=None):')
edit(s,'    reason = app_providers.availability(motor)\n',"    dispatch_check = dispatch_check or _dispatch_guard(user,motor,False)\n    try:dispatch_check()\n    except PermissionError:return _sse_aviso('Acesso ou consentimento revogado.','motor_indisponivel')\n    reason = app_providers.availability(motor)\n")
edit(s,'        task_control=task_scope.control if task_scope else None)\n    return Response(flow', '        task_control=task_scope.control if task_scope else None,authorize=dispatch_check)\n    return Response(flow')
for call in ("_chat_claude(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope)","_chat_avaliacao(req_json,user,selected,is_stream,chosen,task_scope=task_scope)","_chat_openai(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope)"):
 edit(s,call,call[:-1]+',dispatch_check=_dispatch_guard(user,chosen,True))')
# Guard the agent transport and direct external send; leave the payload intact.
edit(s,'    claude = motor == iald_motores.CLAUDE\n    razao =',"    dispatch_check = dispatch_check or _dispatch_guard(user,motor,False)\n    try:dispatch_check()\n    except PermissionError:return _sse_aviso('Acesso ou consentimento revogado.','motor_indisponivel')\n    claude = motor == iald_motores.CLAUDE\n    razao =")
# Insert the guard at the public agent invocation, identified by task control.
t=(S/s).read_text(encoding='utf-8');start=t.index('def _chat_externo(');end=t.index('\ndef _limites_da_conta',start)
part=t[start:end]
needle='yield from agent_loop('
pos=part.index(needle);close=part.index('\n',pos)
# Keyword at the beginning avoids depending on the existing formatting below.
part=part[:pos]+part[pos:].replace('yield from agent_loop(', 'yield from agent_loop(',1)
# Find the task-control keyword in that agent call only.
agent_end=part.index('task_control=task_scope.control if task_scope else None',pos)
part=part[:agent_end]+part[agent_end:].replace('task_control=task_scope.control if task_scope else None','verificar_payload=lambda _:dispatch_check(), task_control=task_scope.control if task_scope else None',1)
part=part.replace('                            for pedaco in iald_motores.transmitir(', '                            enviar_verificado = fazer\n                            def fazer():\n                                dispatch_check()\n                                return enviar_verificado()\n                            for pedaco in iald_motores.transmitir(')
(S/s).write_text(t[:start]+part+t[end:],encoding='utf-8')

guard='''def _dispatch_guard(user,executor,automatic):
    def check():
        current=load_users_estrito().get(user,{})
        if not app_router.allowed(current,user):raise PermissionError('Account access revoked')
        if automatic and not iald_motores.consentiu(current,app_router.AUTO):
            raise PermissionError('Automatic consent revoked')
        provider='claude' if executor.startswith('claude-') else executor
        if provider=='nativa':
            if MODERACAO_LIGADA and not iald_motores.consentiu(current,'openai'):
                raise PermissionError('Moderation consent missing')
        elif not iald_motores.consentiu(current,provider):raise PermissionError('Executor consent revoked')
        if provider in app_providers.MODELS and not app_providers.allowed(current,user,provider):
            raise PermissionError('Executor access revoked')
        if executor=='claude-sonnet' and user!='luiz':raise PermissionError('Operator only')
        return current
    return check


'''
edit(s,'def _opcoes_manuais(registro, usuario):',guard+'def _opcoes_manuais(registro, usuario):')
edit(s,"    offered={row['id'] for row in _opcoes_de_motor(registro,user)\n        if row.get('disponivel') and row['id'] in app_router.DESCRIPTIONS and row['id']!='nativa'}", "    offered={row['id'] for row in _opcoes_de_motor(registro,user)\n        if row.get('disponivel') and row['id'] in app_router.DESCRIPTIONS}\n    if 'nativa' in offered and (not MODERACAO_LIGADA or iald_motores.consentiu(registro,'openai')):return router_consent\n    offered.discard('nativa')")
edit(s,"            consent_provider='claude' if key.startswith('claude-') else key", "            if key=='nativa' and MODERACAO_LIGADA and not iald_motores.consentiu(registro,'openai'):continue\n            consent_provider='claude' if key.startswith('claude-') else key")
edit(s,"        payload,definitions,check=_prepare_native_payload(payload,'app')", "        dispatch_check=_dispatch_guard(user,'nativa',True)\n        dispatch_check()\n        if MODERACAO_LIGADA:\n            decision=iald_motores.moderar_textos([profile]+[m['content'] for m in messages[1:]],\n                req_lib.post,MOTORES_CFG.url_base,MOTORES_CFG.chave,cache=_CACHE_MODERACAO)\n            if decision.get('bloquear'):return _sse_aviso(iald_motores.MENSAGEM_MODERACAO_BLOQUEIO,'moderacao')\n            if not decision.get('ok') and MODERACAO_FALHA=='bloquear':\n                return _sse_aviso(MSG_MODERACAO_INDISPONIVEL,'moderacao_indisponivel')\n            if decision.get('acolher'):messages[0]['content']+='\\n'+iald_motores.INSTRUCAO_ACOLHIMENTO\n        payload,definitions,context_check=_prepare_native_payload(payload,'app')\n        def check(current):\n            dispatch_check()\n            measured=context_check(current)\n            dispatch_check()\n            return measured")
edit(s,"        response=Response(generate(),content_type='text/event-stream',headers={'Cache-Control':'no-cache','X-Accel-Buffering':'no'})", "        flow=generate()\n        if MODERACAO_LIGADA and iald_motores.plano_de(registro)==iald_motores.GRATUITO:\n            flow=_moderar_resposta_sse(flow,user,MOTORES_CFG,authorize=dispatch_check)\n        response=Response(flow,content_type='text/event-stream',headers={'Cache-Control':'no-cache','X-Accel-Buffering':'no'})")
edit(s,'def _moderar_resposta_sse(fluxo, user, cfg):','def _moderar_resposta_sse(fluxo, user, cfg, *, authorize=None):')
edit(s,'        r = iald_motores.moderar_textos(texto,', '        if authorize is not None:authorize()\n        r = iald_motores.moderar_textos(texto,') if '        r = iald_motores.moderar_textos(texto,' in (S/s).read_text(encoding='utf-8') else None
# Actual implementation uses a one-item list.
edit(s,'        r = iald_motores.moderar_textos([texto],','        if authorize is not None:authorize()\n        r = iald_motores.moderar_textos([texto],')
edit(s,'fluxo = _moderar_resposta_sse(fluxo, user, cfg_moderacao)','fluxo = _moderar_resposta_sse(fluxo, user, cfg_moderacao, authorize=dispatch_check)')
edit('app/iald.js',"  const doMotor = S.motor && S.motor.consentimento;", "  if (S.motor && Array.isArray(S.motor.provedores_automaticos) && j.provedor) {\n    for (const item of S.motor.provedores_automaticos) {\n      if (item.provedor === j.provedor) item.dado = aceito;\n    }\n  }\n  const doMotor = S.motor && S.motor.consentimento;")
print('Review corrections staged')
