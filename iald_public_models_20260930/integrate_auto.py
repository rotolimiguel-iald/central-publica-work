from pathlib import Path
import ast,json,hashlib
W=Path(__file__).resolve().parent;S=W/'stage';R=Path(r'C:\IALD\projetos_pyhton\IALD')
pins=json.loads((W/'pins.json').read_bytes())
raw=(R/'iald_motores.py').read_bytes();pins['iald_motores.py']=hashlib.sha256(raw).hexdigest();s=raw.decode()
s=s.replace('MOTORES = (NATIVA, OPENAI, CLAUDE) + AVALIACAO','AUTO = "automatico"\nMOTORES = (NATIVA, OPENAI, CLAUDE, AUTO) + AVALIACAO')
s=s.replace('EXTERNOS = (OPENAI, CLAUDE) + AVALIACAO','EXTERNOS = (OPENAI, CLAUDE, AUTO) + AVALIACAO')
s=s.replace('PROVEDORES = {OPENAI:', 'PROVEDORES = {AUTO: "TypeSafe (JEV)", OPENAI:')
s=s.replace('**{p: "consentimento_ia_" + p for p in AVALIACAO}', 'AUTO: "consentimento_ia_jev_router", **{p: "consentimento_ia_" + p for p in AVALIACAO}')
s=s.replace('return {OPENAI: OPENAI, CLAUDE: CLAUDE,', 'return {AUTO: AUTO, "typesafe (jev)": AUTO, OPENAI: OPENAI, CLAUDE: CLAUDE,')
s=s.replace('def texto_do_consentimento(provedor=OPENAI):','def texto_do_consentimento(provedor=OPENAI):\n    if _motor_do_provedor(provedor) == AUTO:\n        from iald_auto_router import consent_text\n        return consent_text()')
ast.parse(s);(S/'iald_motores.py').write_bytes(s.encode())

s=(S/'iald_web_server.py').read_text('utf-8')
s=s.replace('import iald_app_providers as app_providers','import iald_app_providers as app_providers\nimport iald_auto_router as app_router')
assert 'import iald_auto_router as app_router' in s
s=s.replace('def _motor_efetivo(registro, username):','def _motor_efetivo(registro, username):\n    if isinstance(registro, dict) and registro.get("motor") == app_router.AUTO:\n        return app_router.AUTO')
s=s.replace('    modelo_ext = iald_motores.modelo_para(registro, MOTORES_CFG)\n    opcoes = []', '    modelo_ext = iald_motores.modelo_para(registro, MOTORES_CFG)\n    opcoes = []\n    if app_router.allowed(registro, usuario):\n        opcoes.append(dict(id=app_router.AUTO,rotulo="IALD Automática",provedor=app_router.PROVIDER,\n            detalhe="JEV escolhe o modelo · piloto pessoal",disponivel=app_router.available()))')
s=s.replace('"claude-sonnet", *app_providers.MODELS)', '"claude-sonnet", app_router.AUTO, *app_providers.MODELS)')
# Selection and consent enforce a server-only grant, including stale/forged records.
s=s.replace('        if option in app_providers.MODELS and not app_providers.allowed', '        if option == app_router.AUTO and not app_router.allowed(conta, username):\n            return jsonify({"error":"Piloto automático exclusivo do operador."}),403\n        if option in app_providers.MODELS and not app_providers.allowed')
s=s.replace('        if aceito:\n            if alvo in app_providers.MODELS', '        if aceito:\n            if alvo == app_router.AUTO and not app_router.allowed(conta, username):\n                return jsonify({"error":"Piloto automático exclusivo do operador."}),403\n            if alvo in app_providers.MODELS')
s=s.replace('    plano = iald_motores.plano_de(registro)\n    if motor in app_providers.MODELS:', '''    plano = iald_motores.plano_de(registro)
    if motor == app_router.AUTO:
        return jsonify(dict(motor=motor,motor_selecao=motor,modelo='jev-1.13.0',rotulo='IALD Automática',
            provedor=app_router.PROVIDER,plano=plano,cota=None,
            disponivel=app_router.allowed(registro,username) and app_router.available(),
            pode_escolher=True,opcoes=_opcoes_de_motor(registro,username),limites=app_router.limits(),
            consentimento=_consentimento_do_motor(registro,motor),consentimentos=_consentimentos_registrados(registro)))
    if motor in app_providers.MODELS:''')
s=s.replace('    if motor in app_providers.MODELS:\n        return app_providers.limits(motor)', '    if motor == app_router.AUTO:\n        return app_router.limits()\n    if motor in app_providers.MODELS:\n        return app_providers.limits(motor)')
s=s.replace('        motor, registro = _motor_do_usuario(conta)\n        if motor in app_providers.MODELS:', '''        motor, registro = _motor_do_usuario(conta)
        if motor == app_router.AUTO:
            return jsonify(dict(id='automatico:jev',short='IALD Automática',label='JEV seleciona o executor',
                motor=motor,online=app_router.allowed(registro,conta) and app_router.available(),
                n_ctx=1048576,vision=False,consentimento_dado=iald_motores.consentiu(registro,motor)))
        if motor in app_providers.MODELS:''')
s=s.replace('    if motor_ctx in app_providers.MODELS:', '    if motor_ctx == app_router.AUTO:\n        return jsonify(app_router.limits())\n    if motor_ctx in app_providers.MODELS:')
s=s.replace('        if motor_conta in app_providers.MODELS:', '''        if motor_conta == app_router.AUTO:
            if subpath != 'chat/completions':
                return jsonify({'error':'Este modo atende somente ao chat.'}),403
            return _chat_automatico(req_json,user,registro_conta,is_stream,tokens_in)
        if motor_conta in app_providers.MODELS:''')
handler='''def _chat_automatico(req_json,user,registro,is_stream,tokens_in):
    if not app_router.allowed(registro,user):
        return _sse_aviso('Piloto automático não liberado para esta conta.','motor_indisponivel')
    consent=_consentimento_do_motor(registro,app_router.AUTO)
    if not consent['dado']:
        return _sse_aviso('Leia e aceite o aviso do modo automático.','consentimento_ia',
            dict(versao=consent['versao'],provedor=consent['provedor'],detalhe=consent['texto']))
    if not is_stream or not isinstance(req_json,dict):
        return jsonify({'error':'Envie chat com stream: true.'}),400
    try:
        client=req_json.get('messages')
        app_providers.wire_messages(client,'routing_validation')
        candidates=[]
        for row in _opcoes_de_motor(registro,user):
            key=row['id']
            if key not in app_router.DESCRIPTIONS or not row.get('disponivel'):continue
            # Do not route automatically through the provider currently under diagnosis.
            if key=='deepseek':continue
            consent_provider='claude' if key.startswith('claude-') else key
            if iald_motores.consentiu(registro,consent_provider):candidates.append(key)
        if not candidates:raise ValueError('No consented executor')
        chosen,receipt=app_router.choose(client[-1]['content'],candidates)
        # Recheck permissions/consent after the router returns, before generation.
        current=load_users_estrito().get(user,{})
        if not app_router.allowed(current,user) or not iald_motores.consentiu(current,app_router.AUTO):
            raise PermissionError('Access revoked')
        if chosen not in {r['id'] for r in _opcoes_de_motor(current,user) if r.get('disponivel')}:
            raise PermissionError('Executor revoked')
        selected=dict(current,motor=chosen)
        if chosen.startswith('claude-'):
            selected.update(CLAUDE_ROUTES.select(chosen,current,user))
            return _chat_claude(req_json,user,selected,is_stream,tokens_in)
        if chosen in app_providers.MODELS:
            return _chat_avaliacao(req_json,user,selected,is_stream,chosen)
        if chosen=='openai':
            response=_chat_openai(req_json,user,selected,is_stream,tokens_in)
            if response is not None:return response
        raise ValueError('No compatible executor')
    except (ValueError,PermissionError,OSError,KeyError,TypeError,RuntimeError):
        return _sse_aviso('Não foi possível concluir a escolha automática. Selecione um modelo manualmente; não houve reenvio para outro executor.','motor_indisponivel')


'''
s=s.replace('def _chat_avaliacao(',handler+'def _chat_avaliacao(',1)
s=s.replace('    return jsonify(APP_EVALUATION.report())','    result=APP_EVALUATION.report()\n    result["routing"]=app_router.report()\n    result["jev"]="Piloto pessoal: JEV escolhe somente entre executores autorizados e consentidos; sem repetição após envio."\n    return jsonify(result)')
ast.parse(s);(S/'iald_web_server.py').write_bytes(s.encode())
pins['iald_auto_router.py']=None
(W/'pins.json').write_bytes(json.dumps(pins,indent=2).encode())
print('Auto pilot staged; production unchanged')
