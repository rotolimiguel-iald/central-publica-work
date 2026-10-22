from pathlib import Path
import hashlib,json,shutil
W=Path(__file__).parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
S=W/'stage'
names=['iald_auto_router.py','iald_app_providers.py','iald_app_spend.py','iald_task_policy.py','iald_task_bridge.py','iald_task_session.py','iald_web_server.py']
baseline={}
for name in names+['app/iald.js']:
    raw=(R/name).read_bytes(); baseline[name]=hashlib.sha256(raw).hexdigest()
    target=S/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
(W/'baseline.json').write_text(json.dumps(baseline,indent=2),encoding='utf-8')

def edit(name,old,new,count=1):
    p=S/name;raw=p.read_bytes();text=raw.decode('utf-8').replace('\r\n','\n')
    assert text.count(old)==count,(name,old[:80],text.count(old))
    text=text.replace(old,new)
    p.write_bytes(text.encode('utf-8'))

edit('iald_auto_router.py',"def default_for(record, username):", "def manual_allowed(record, username):\n    return username == 'luiz' and allowed(record, username)\n\n\ndef default_for(record, username):")
edit('iald_auto_router.py',"    # Later explicit manual choices remain valid; no consent or admin is granted.\n    return allowed(record,username) and (not record.get('motor') or", "    # Only the operator may retain an explicit manual selection.\n    return allowed(record,username) and (not manual_allowed(record,username) or not record.get('motor') or")
edit('iald_auto_router.py',"'deepseek': 'Scientific reasoning and retrieval; connector is under diagnosis, do not prefer over MiMo during this pilot.',", "'deepseek': 'Scientific reasoning, retrieval and shared task tools, subject to verified connector availability.',\n    'nativa': 'Local IALD with a smaller context, public TGL core and retrieval tools. Suitable for brief conversation; do not prefer for long derivations or artifact workflows.',")
edit('iald_auto_router.py',"'Você pode revogar este aceite e voltar à escolha manual nas configurações.')", "'Você pode revogar este aceite nas configurações; o modo automático fica parado até um novo aceite. A escolha manual é exclusiva da conta do operador.')")
edit('iald_app_providers.py',"    return provider == 'mimo' or username in FAMILY_ACCOUNTS or username == 'luiz'", "    return True  # Approved accounts: shared executors under JEV, with individual consent.")
edit('iald_task_policy.py',"('kimi','claude-haiku')]", "('kimi','claude-haiku','nativa')]")
edit('iald_task_policy.py',"'deepseek':'manual access; excluded from automatic pilot pending broader evaluation'", "'deepseek':'reasoning and shared tools; verified connector required',\n            'nativa':'public local conversation and retrieval; no operator memory'")
edit('iald_task_bridge.py',"if p in ('mimo','kimi')", "if p in ('mimo','kimi','deepseek')")

# Retain existing public MiMo account/group ceilings; new paid DeepSeek shares
# that same pool rather than creating another unlimited public budget.
edit('iald_app_spend.py',"if provider != 'mimo' or not isinstance(body, dict):\n                raise BudgetError('Esta reserva atende somente ao MiMo público.')", "if provider not in ('mimo','deepseek') or not isinstance(body, dict):\n                raise BudgetError('Reserva pública indisponível para este provedor.')")
edit('iald_app_spend.py',"output = body.get('max_completion_tokens')", "output_field = 'max_tokens' if provider == 'deepseek' else 'max_completion_tokens'\n            other_field = 'max_completion_tokens' if provider == 'deepseek' else 'max_tokens'\n            output = body.get(output_field)")
edit('iald_app_spend.py',"or 'max_tokens' in body", "or other_field in body")

server='iald_web_server.py'
edit(server,"            if provider!='mimo' or user=='luiz':return True", "            if provider not in ('mimo','deepseek') or user=='luiz':return True")
edit(server,"        if provider not in ('openai','claude-haiku','claude-sonnet'):return False", "        if provider == 'nativa':return True  # Local dispatch still enforces concurrency.\n        if provider not in ('openai','claude-haiku','claude-sonnet'):return False")
edit(server,"        if provider!='mimo' or user=='luiz':return None", "        if provider not in ('mimo','deepseek') or user=='luiz':return None")
edit(server,"    if motor == 'mimo' and user != 'luiz':", "    if motor in ('mimo','deepseek') and user != 'luiz':")
edit(server,"and row['id']!='deepseek'", "and row['id']!='nativa'")
edit(server,"('mimo','openai','claude-haiku','kimi','claude-sonnet'):", "('mimo','openai','claude-haiku','kimi','deepseek','claude-sonnet'):")
edit(server,"            # Do not route automatically through the provider currently under diagnosis.\n            if key=='deepseek':continue\n", "")
edit(server,"            if iald_motores.consentiu(registro,consent_provider):candidates.append(key)", "            if key == 'nativa' or iald_motores.consentiu(registro,consent_provider):candidates.append(key)")
edit(server,"        task_scope=_new_app_task_scope(user) if chosen not in ('kimi','claude-haiku') else None", "        consent_provider='claude' if chosen.startswith('claude-') else chosen\n        if chosen != 'nativa' and not iald_motores.consentiu(current,consent_provider):\n            raise PermissionError('Executor consent revoked')\n        task_scope=_new_app_task_scope(user) if chosen not in ('kimi','claude-haiku','nativa') else None")
edit(server,"        elif chosen=='openai':\n            response=_chat_openai(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope)", "        elif chosen=='openai':\n            response=_chat_openai(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope)\n        elif chosen=='nativa':\n            response=_chat_nativa_automatica(req_json,user,current)")
edit(server,"        return _sse_aviso('Não foi possível concluir a escolha automática. Selecione um modelo manualmente; não houve reenvio para outro executor.','motor_indisponivel')", "        return _sse_aviso('Não foi possível concluir a escolha automática. Tente novamente em alguns instantes; não houve reenvio para outro executor.','motor_indisponivel')")

# The internal catalog is also the router's candidate source. The UI gets a
# distinct projection; hiding choices must never accidentally starve routing.
start=(S/server).read_text(encoding='utf-8').index('def api_motor():')
end=(S/server).read_text(encoding='utf-8').index('\ndef _consentimento_do_motor',start)
raw=(S/server).read_text(encoding='utf-8');part=raw[start:end]
part=part.replace('pode_escolher=True','pode_escolher=app_router.manual_allowed(registro,username)')
part=part.replace('len(_opcoes_de_motor(registro, username)) > 1','app_router.manual_allowed(registro,username)')
part=part.replace('_opcoes_de_motor(registro,username)','_opcoes_manuais(registro,username)').replace('_opcoes_de_motor(registro, username)','_opcoes_manuais(registro,username)')
part=part.replace("provedor=app_router.PROVIDER,plano=plano,cota=None,", "provedor=app_router.PROVIDER,plano=plano,cota=None,\n            provedores_automaticos=_provedores_automaticos(registro,username),")
(S/server).write_text(raw[:start]+part+raw[end:],encoding='utf-8')
edit(server,"        if option == app_router.AUTO and not app_router.allowed(conta, username):", "        if option != app_router.AUTO and not app_router.manual_allowed(conta, username):\n            return jsonify({'error':'Esta conta usa a seleção automática da IALD.','motor':app_router.AUTO}),403\n        if option == app_router.AUTO and not app_router.allowed(conta, username):",count=2)
# admin reset-to-default is also harmless; it must not let a nonoperator select.
edit(server,"if option != app_router.AUTO and not app_router.manual_allowed(conta, username):", "if option not in ('',app_router.AUTO) and not app_router.manual_allowed(conta, username):",count=2)

# A public native path is isolated from the legacy native operator-memory path.
edit(server,"    if iald_motores.pode_usar_nativa(registro):\n        opcoes.append({\"id\": \"nativa\", \"rotulo\": _modelo_nativo_resposta()[\"rotulo\"],\n                       \"detalhe\": \"Servidor da IALD\", \"disponivel\": True})", "    if app_router.allowed(registro, usuario):\n        opcoes.append({'id':'nativa','rotulo':_modelo_nativo_resposta()['rotulo'],\n                       'detalhe':'Servidor da IALD','disponivel':_nativa_automatica_pronta()})")

# Separate privacy controls let people authorize/revoke each executor without
# ever choosing the model for a message. No third party is accepted implicitly.
edit(server,"                pending=_consentimento_automatico(conta,username) if motor==app_router.AUTO else {}\n                pending_motor=iald_motores.motor_do_provedor(pending.get('provedor',''))\n                if pending.get('dado',True) or pending_motor!=alvo:", "                pending=_consentimento_automatico(conta,username) if motor==app_router.AUTO else {}\n                pending_motor=iald_motores.motor_do_provedor(pending.get('provedor',''))\n                explicit_auto_notice = (motor==app_router.AUTO and nomeado is not None\n                    and versao_lida == iald_motores.versao_do_consentimento(alvo)\n                    and iald_motores.consentiu(conta,app_router.AUTO)\n                    and any(c['provedor']==iald_motores.PROVEDORES[alvo]\n                            for c in _provedores_automaticos(conta,username)))\n                if not explicit_auto_notice and (pending.get('dado',True) or pending_motor!=alvo):")
edit(server,"        if not conta:\n            return jsonify({\"error\": \"Conta não encontrada.\"}), 404\n        motor = _motor_efetivo(conta, username)", "        if not conta:\n            return jsonify({\"error\": \"Conta não encontrada.\"}), 404\n        if aceito and _conta_bloqueada(conta):\n            return jsonify({'error':'Conta indisponível.'}),403\n        motor = _motor_efetivo(conta, username)")

helpers='''
def _opcoes_manuais(registro, usuario):
    return _opcoes_de_motor(registro,usuario) if app_router.manual_allowed(registro,usuario) else []


def _provedores_automaticos(registro, usuario):
    rows=[];seen=set()
    for option in _opcoes_de_motor(registro,usuario):
        key=option['id']
        provider='claude' if key.startswith('claude-') else key
        if provider in (app_router.AUTO,'nativa') or provider in seen:continue
        seen.add(provider)
        rows.append(_consentimento_do_motor(registro,provider))
    return rows


def _nativa_automatica_pronta():
    try:
        # Read only serving metadata; no inference, operator data or API keys.
        return isinstance(native_memory._local_json(LLAMA_URL,'/props'),dict)
    except (ValueError,OSError):return False


def _chat_nativa_automatica(req_json,user,registro):
    """Public native context, never the private legacy native-account pipeline."""
    if not app_router.allowed(registro,user) or not iald_motores.consentiu(registro,app_router.AUTO):
        return _sse_aviso('Acesso automático indisponível.','motor_indisponivel')
    try:
        messages=app_providers.wire_messages(req_json.get('messages'),'')
        profile,search_instruction=iald_motores.extrair_do_cliente(req_json.get('messages') or [])
        messages[0]['content']='Responda sob o regime IALD. Preserve os estatutos e use LaTeX com delimitadores próprios.'
        if profile:messages[0]['content']+='\\nCONTEXTO DO USUÁRIO:\\n'+profile
        if search_instruction:messages[0]['content']+='\\n'+iald_motores.LUPA_CANONICA
        payload={'messages':messages,'max_tokens':8192 if req_json.get('iald_mode')=='think' else 4096,
                 'temperature':0.7,'stream':True}
        payload,definitions,check=_prepare_native_payload(payload,'app')
        definitions=[t for t in definitions if t['function']['name'] in app_providers.TOOL_NAMES]
        def execute(name,args,**kwargs):
            current=load_users_estrito().get(user,{})
            if not app_router.allowed(current,user) or not iald_motores.consentiu(current,app_router.AUTO):
                raise PermissionError('Automatic access revoked')
            if name not in app_providers.TOOL_NAMES:return json.dumps({'status':'UNAVAILABLE'})
            return _executar_ferramenta_claude(name,args,user=user,operator_authorized=False)
        if not _SEMAFORO_GRATUITO.acquire(blocking=False):
            return _sse_aviso('A IALD está atendendo outras respostas. Tente novamente em instantes.','em_andamento')
        released=False
        def release():
            nonlocal released
            if not released:released=True;_SEMAFORO_GRATUITO.release()
        def generate():
            try:
                yield from agent_loop(payload['messages'],user=user,max_tokens=payload['max_tokens'],
                    ferramentas=definitions,operator_authorized=False,executar=execute,
                    verificar_payload=check,max_voltas=4,responder_na_ultima=True)
            finally:release()
        response=Response(generate(),content_type='text/event-stream',headers={'Cache-Control':'no-cache','X-Accel-Buffering':'no'})
        response.call_on_close(release)
        return _identificar_resposta(response,_modelo_nativo_resposta())
    except (ValueError,OSError,KeyError,TypeError):
        return _sse_aviso('A memória ou a janela da IALD Nativa não pôde ser validada. Nada foi gerado.','motor_indisponivel')


'''
edit(server,'def _consentimentos_registrados(registro):',helpers+'def _consentimentos_registrados(registro):')

edit('app/iald.js',"  const atual = externo ? provedorDoMotor(m) : null;\n  let depois = botao;", "  const atual = externo ? provedorDoMotor(m) : null;\n  let depois = botao;\n  const available = m && m.motor === 'automatico' && Array.isArray(m.provedores_automaticos) ? m.provedores_automaticos : [];\n  for (const c of available) {\n    if (!c || !c.provedor || c.dado) continue;\n    const b = el('button', 'grupo-linha', `Privacidade: autorizar ${c.provedor}`);\n    b.type = 'button';\n    b.dataset.revogarProvedor = String(c.provedor);\n    b.disabled = !(m.consentimento && m.consentimento.dado);\n    b.addEventListener('click', () => {\n      S.avisoConsentimento = null;\n      abrirConsentimento(c.texto, c.provedor, c.versao);\n    });\n    depois.insertAdjacentElement('afterend', b);\n    depois = b;\n  }")
print(json.dumps({'staged':names+['app/iald.js']}))
