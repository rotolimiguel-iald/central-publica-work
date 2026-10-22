"""Create a reviewable server/client integration copy; never edit production."""
from pathlib import Path
from datetime import datetime
import ast,hashlib,json
W=Path(__file__).resolve().parent;ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
raw=(ROOT/'iald_web_server.py').read_bytes();text=raw.decode('utf-8');nl='\r\n' if '\r\n' in text else '\n'
text=text.replace('\r\n','\n')

def replace_function(name,source):
    global text
    tree=ast.parse(text);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name]
    assert len(nodes)==1
    n=nodes[0];lines=text.splitlines(keepends=True)
    text=''.join(lines[:n.lineno-1])+source.strip()+'\n'+''.join(lines[n.end_lineno:])

def change(old,new):
    global text
    assert text.count(old)==1,(old[:100],text.count(old))
    text=text.replace(old,new,1)

helpers='''
from claude_route_bridge import RouteBridge
from claude_memory_package import load_package
from claude_guarded_transport import post_guarded
from claude_profiles import HAIKU as _HAIKU_PROFILE
from claude_haiku_messages import assemble as _assemble_haiku_messages
from claude_native_counter import count_native_request as _count_haiku_native_request
from claude_native_account import NativeAccount as _HaikuNativeAccount

def _load_haiku_package():
    return load_package(os.path.join(SERVE_DIR, ".iald_runtime", "haiku"))

CLAUDE_ROUTES = RouteBridge(motors=iald_motores, base_config=CLAUDE_CFG,
    package_loader=_load_haiku_package, enabled=str(_segredo("IALD_HAIKU_ATIVO", "0")) == "1",
    public_daily_usd=_segredo("IALD_HAIKU_PUBLICO_USD_DIA", ""),
    public_group_daily_usd=_segredo("IALD_HAIKU_GRUPO_USD_DIA", ""))

def _claude_policy(registro, username):
    from claude_server_selection import policy_for
    return policy_for(registro, username, **CLAUDE_ROUTES.policy_flags(username))

def _motor_selection_id(motor, registro, username):
    if motor != iald_motores.CLAUDE:
        return motor
    try:
        return CLAUDE_ROUTES.selection_id(registro, username)
    except (ValueError, PermissionError, OSError):
        return "claude"
'''
change('def _cfg_do_motor(motor):',helpers+'\n\ndef _cfg_do_motor(motor):')
replace_function('_cfg_do_motor','''
def _cfg_do_motor(motor, registro=None, username=None):
    if motor == iald_motores.CLAUDE:
        return CLAUDE_ROUTES.configuration(registro, username or session.get("username", ""))
    return MOTORES_CFG
''')
replace_function('_motor_efetivo','''
def _motor_efetivo(registro, username):
    # A saved Claude selection remains Claude even if temporarily unavailable;
    # the send boundary refuses it instead of silently switching providers.
    if isinstance(registro, dict) and registro and registro.get("motor") == iald_motores.CLAUDE:
        return iald_motores.CLAUDE
    return iald_motores.escolher_motor(registro, MOTORES_CFG, usuario=username, contas_claude=_contas_claude())
''')
replace_function('_opcoes_de_motor','''
def _opcoes_de_motor(registro, usuario=None):
    if not isinstance(registro, dict) or not registro or _conta_bloqueada(registro):
        return []
    modelo_ext = iald_motores.modelo_para(registro, MOTORES_CFG)
    opcoes = []
    if iald_motores.pode_usar_nativa(registro):
        opcoes.append({"id": "nativa", "rotulo": _modelo_nativo_resposta()["rotulo"],
                       "detalhe": "Servidor da IALD", "disponivel": True})
    opcoes.append({"id": "openai", "rotulo": iald_motores.rotulo_do_modelo(modelo_ext),
                   "detalhe": "OpenAI · " + modelo_ext,
                   "disponivel": not _motor_externo_indisponivel(modelo_ext)})
    opcoes.extend(CLAUDE_ROUTES.options(registro, usuario))
    return opcoes
''')
replace_function('api_motor_escolha','''
def api_motor_escolha():
    username = session.get("username", "")
    if not request.is_json:
        return jsonify({"error": "Envie application/json."}), 415
    option = str((_corpo_json() or {}).get("motor") or "").strip().lower()
    if option not in ("nativa", "openai", "claude", "claude-haiku", "claude-sonnet"):
        return jsonify({"error": "Modelo inválido."}), 400
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        conta = usuarios.get(username)
        if not conta or _conta_bloqueada(conta):
            return jsonify({"error": "Conta indisponível."}), 403
        if option.startswith("claude"):
            try:
                fields = CLAUDE_ROUTES.select(option, conta, username)
                # Validate the selected profile, including its configured price.
                CLAUDE_ROUTES.configuration(dict(conta, **fields), username)
            except (ValueError, PermissionError, OSError):
                return jsonify({"error": "Esse modelo não está disponível para esta conta."}), 409
        else:
            if option == "nativa" and not iald_motores.pode_usar_nativa(conta):
                return jsonify({"error": MSG_SEM_ACESSO_NATIVA}), 403
            if option not in {o["id"] for o in _opcoes_de_motor(conta, username) if o["disponivel"]}:
                return jsonify({"error": "Esse modelo está indisponível agora."}), 409
            fields = {"motor": option}
        conta.update(fields)
        save_users(usuarios)
        motor = _motor_efetivo(conta, username)
        consentimento = (_consentimento_do_motor(conta, motor) if motor in iald_motores.EXTERNOS
                         else {"necessario": False})
        selection = _motor_selection_id(motor, conta, username)
    auth_log("MOTOR_ESCOLHA", username, "motor=" + selection)
    return jsonify({"ok": True, "motor": motor, "motor_selecao": selection,
                    "consentimento_dado": consentimento.get("dado", False), "consentimento": consentimento})
''')
# Propagate the trusted account to existing status/cost configuration lookups.
text=text.replace('_cfg_do_motor(motor)', '_cfg_do_motor(motor, registro)')
text=text.replace('_cfg_do_motor(motor_ctx)', '_cfg_do_motor(motor_ctx, registro_ctx)')
text=text.replace('"pode_escolher": iald_motores.pode_usar_nativa(registro),',
                  '"pode_escolher": len(_opcoes_de_motor(registro, username)) > 1,')
change('return jsonify({"motor": motor, "provedor": iald_motores.PROVEDORES[motor], "modelo": modelo,',
       'return jsonify({"motor": motor, "motor_selecao": _motor_selection_id(motor, registro, username), "provedor": iald_motores.PROVEDORES[motor], "modelo": modelo,')
change('cfg = iald_motores.config_da_conta(CLAUDE_CFG if claude else MOTORES_CFG, registro)',
'''try:
        cfg = (CLAUDE_ROUTES.configuration(registro, user) if claude
               else iald_motores.config_da_conta(MOTORES_CFG, registro))
    except (ValueError, PermissionError, OSError):
        return _sse_aviso("Modelo Claude indisponível para esta conta.", "motor_indisponivel")
    haiku = claude and cfg.modelo == _HAIKU_PROFILE.model''')
change('if claude and (gratuito or not iald_motores.pode_usar_claude(registro, user, _contas_claude())):',
       'if claude and not CLAUDE_ROUTES.options(registro, user):')
change('motivo = _motor_externo_indisponivel(modelo, CLAUDE_CFG) if claude else _motor_externo_indisponivel(modelo)',
       'motivo = _motor_externo_indisponivel(modelo, cfg) if claude else _motor_externo_indisponivel(modelo)')
change('prompt_externo, memoria_info = _contexto_externo(public=gratuito)',
'''if haiku:
                haiku_package = CLAUDE_ROUTES.package()
                prompt_externo = haiku_package.prefix
                memoria_info = {"context_sha256": haiku_package.measurement.prefix_sha256, "scope": "HAIKU_MEASURED_PUBLIC"}
                cfg.janela = _HAIKU_PROFILE.window
            else:
                prompt_externo, memoria_info = _contexto_externo(public=gratuito)''')
change('return iald_motor_claude.post_como_openai(cfg, payload, prefixo=prompt_externo,',
'''if haiku:
                    response, decision = post_guarded(iald_motor_claude, cfg, payload,
                        requested_model=modelo, server_policy=_claude_policy(registro, user),
                        prefix=prompt_externo, memory=haiku_package.measurement,
                        state=estado_claude, timeout=timeout)
                    return response
                return iald_motor_claude.post_como_openai(cfg, payload, prefixo=prompt_externo,''')
# Validate measured Haiku memory rather than the unrelated larger Sonnet prefix.
change('    if MOTORES_CFG.memoria_modo != "prompt":\n        try:\n            _contexto_externo()',
'''    if claude and modelo == _HAIKU_PROFILE.model:
        try:
            CLAUDE_ROUTES.package()
        except (ValueError, OSError, KeyError):
            return "A memória medida do Haiku está indisponível."
        return "" if cfg.precos(modelo) is not None else "Preço do Haiku não configurado."
    if MOTORES_CFG.memoria_modo != "prompt":
        try:
            _contexto_externo()''')
# The effective account model also drives the public badge.
change('modelo = iald_motores.modelo_para(registro, CLAUDE_CFG)\n            return jsonify',
       'active_cfg = CLAUDE_ROUTES.configuration(registro, conta)\n            modelo = iald_motores.modelo_para(registro, active_cfg)\n            return jsonify')
change('"online": not _motor_externo_indisponivel(modelo, CLAUDE_CFG),',
       '"online": not _motor_externo_indisponivel(modelo, active_cfg),')
change('"n_ctx": iald_motores.janela_do_plano(CLAUDE_CFG, iald_motores.plano_de(registro)),',
       '"n_ctx": active_cfg.janela,')
replace_function('admin_definir_motor','''
def admin_definir_motor(username):
    check = require_admin()
    if check:
        return check
    option = str((request.get_json(silent=True) or {}).get("motor", "")).strip().lower()
    if option not in ("", "nativa", "openai", "claude", "claude-haiku", "claude-sonnet"):
        return jsonify({"error": "Modelo inválido."}), 400
    username = username.strip().lower()
    with _TRAVA_USUARIOS:
        usuarios = _carregar_usuarios_para_escrita()
        conta = usuarios.get(username)
        if not conta:
            return jsonify({"error": "Conta não encontrada."}), 404
        if option.startswith("claude"):
            try:
                fields = CLAUDE_ROUTES.select(option, conta, username)
                CLAUDE_ROUTES.configuration(dict(conta, **fields), username)
            except (PermissionError, ValueError, OSError):
                return jsonify({"error": "Modelo não disponível para esta conta."}), 409
            conta.update(fields)
        elif option == "nativa":
            if not iald_motores.pode_usar_nativa(conta):
                return jsonify({"error": "Acesso à IALD Nativa não liberado."}), 409
            conta["motor"] = option
        elif option:
            conta["motor"] = option
        else:
            conta.pop("motor", None)
            conta.pop("modelo_claude", None)
        save_users(usuarios)
        efetivo = _motor_efetivo(conta, username)
    auth_log("ADMIN_MOTOR", session.get("username", "?"), "user=" + username + " model=" + (option or "regra-geral"))
    return jsonify({"ok": True, "motor": conta.get("motor", ""), "motor_efetivo": efetivo,
                    "motor_selecao": _motor_selection_id(efetivo, conta, username)})
''')
change('"claude_permitido": iald_motores.pode_usar_claude(data, username, _contas_claude()),',
       '"claude_permitido": bool(CLAUDE_ROUTES.options(data, username)),')
change('cfg = iald_motores.config_da_conta(_cfg_do_motor(motor, registro), registro)',
'''try:
        cfg = iald_motores.config_da_conta(_cfg_do_motor(motor, registro, username), registro)
    except (PermissionError, ValueError, OSError):
        return {"erro": "Configuração do modelo indisponível."}''')
change('cfg = _cfg_do_motor(motor, registro)\n    try:\n        lim = iald_motores.limites_do_plano(cfg, plano)',
       'try:\n        cfg = _cfg_do_motor(motor, registro)\n        lim = iald_motores.limites_do_plano(cfg, plano)')
change('except (ValueError, TypeError, KeyError) as exc:\n        return {"agente": False',
       'except (PermissionError, OSError, ValueError, TypeError, KeyError) as exc:\n        return {"agente": False')
change('"janela": iald_motores.janela_do_plano(cfg, plano), "imagens": imagens}',
       '"janela": cfg.janela if cfg.modelo == _HAIKU_PROFILE.model else iald_motores.janela_do_plano(cfg, plano), "imagens": imagens}')
change('cfg = _cfg_do_motor(motor, registro)\n    modelo = iald_motores.modelo_para(registro, cfg)',
'''try:
        cfg = _cfg_do_motor(motor, registro, username)
    except (PermissionError, ValueError, OSError):
        return jsonify({"motor": motor, "motor_selecao": _motor_selection_id(motor, registro, username),
                        "provedor": iald_motores.PROVEDORES[motor], "disponivel": False,
                        "erro": "Memória ou configuração do modelo indisponível.",
                        "pode_escolher": len(_opcoes_de_motor(registro, username)) > 1,
                        "opcoes": _opcoes_de_motor(registro, username), "plano": plano,
                        "cota": {"erro": "Modelo indisponível."},
                        "limites": {"agente": False, "pensar": False, "max_saida": 0, "janela": 0},
                        "consentimento": _consentimento_do_motor(registro, motor),
                        "consentimentos": _consentimentos_registrados(registro)})
    modelo = iald_motores.modelo_para(registro, cfg)''')
change('active_cfg = CLAUDE_ROUTES.configuration(registro, conta)\n            modelo =',
'''try:
                active_cfg = CLAUDE_ROUTES.configuration(registro, conta)
            except (PermissionError, ValueError, OSError):
                return jsonify({"id": "claude:unavailable", "short": "IALD · Claude indisponível",
                                "motor": motor, "online": False, "n_ctx": 0})
            modelo =''')
change('''            para_openai, info = iald_motores.montar_mensagens(
                mensagens, prompt_externo, modelo, nomes, cfg.janela, teto_saida, instrucao,
                provedor=iald_motores.PROVEDORES[motor])''',
'''            if haiku:
                para_openai, info = _assemble_haiku_messages(
                    iald_motores, mensagens, prompt_externo, modelo, nomes, instrucao)
            else:
                para_openai, info = iald_motores.montar_mensagens(
                    mensagens, prompt_externo, modelo, nomes, cfg.janela, teto_saida, instrucao,
                    provedor=iald_motores.PROVEDORES[motor])''')
change('''        def prefixo_da_cota(msgs):''',
'''        native_count_cache = {}
        estado_claude = iald_motor_claude.EstadoClaude() if claude else None
        def count_haiku_wire(wire):
            identity = hashlib.sha256(json.dumps(wire, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if identity not in native_count_cache:
                try:
                    client = iald_motor_claude.cliente_para(cfg).with_options(max_retries=0)
                    native_count_cache[identity] = _count_haiku_native_request(client, wire)
                except Exception as exc:
                    raise iald_memoria_canonica.MemoryUnavailable("Contagem de contexto Haiku indisponível; nenhuma geração iniciada.") from exc
            return native_count_cache[identity]

        def tokens_para_saldo(payload):
            if not haiku:
                return _tokens_do_payload_para_saldo(payload)
            wire = iald_motor_claude.converter_pedido(cfg, payload, prefixo=prompt_externo, estado=estado_claude)
            wire.pop("output_config", None)
            wire["thinking"] = {"type": "disabled"}
            return count_haiku_wire(wire)

        def prefixo_da_cota(msgs):''')
change('''            estimado = iald_motores.prefixo_tokens_estimado(msgs)
            return math.ceil''',
'''            if haiku:
                # Same measured minimal-request baseline used by the package;
                # extra profile/history/tools are counted in the full request.
                return haiku_package.measurement.permanent_tokens
            estimado = iald_motores.prefixo_tokens_estimado(msgs)
            return math.ceil''')
change('return max(0, _tokens_do_payload_para_saldo(amostra) - prefixo)',
       'return max(0, tokens_para_saldo(amostra) - prefixo)')
change('while entrada + iald_motores.SALDO_MINIMO_TOKENS > saldo_inicial and len(para_openai) > 2:',
       'while not haiku and entrada + iald_motores.SALDO_MINIMO_TOKENS > saldo_inicial and len(para_openai) > 2:')
change('                _tokens_do_payload_para_saldo))', '                tokens_para_saldo))')
# Haiku gets the exact seven public tools that were measured, never the private
# Atlas or inherited operator tools. Actual tool results remain public-only.
change('''        permitidas = _ferramentas_externas(cfg, limites, superficie, gratuito)
        usar_agente''',
'''        permitidas = ((iald_kernel.tool_definitions() + iald_fontes_publicas.tool_definitions()
                       + iald_core_indexado.tool_definitions()) if haiku
                      else _ferramentas_externas(cfg, limites, superficie, gratuito))
        usar_agente''')
change('''            if gratuito:
                executor = _executar_ferramenta_gratuito
            elif claude:''',
'''            if claude:
                executor = _executar_ferramenta_claude
            elif gratuito:
                executor = _executar_ferramenta_gratuito
            elif claude:''')
change('''            elif claude:
                executor = _executar_ferramenta_claude          # o Atlas sem §V, §VI e §X
''', '')
change('''                        state=estado_claude, timeout=timeout)''',
       '''                        state=estado_claude, timeout=timeout, counter=count_haiku_wire)''')
change('''            estado_claude = iald_motor_claude.EstadoClaude()

            def enviar''', '''            def enviar''')
old_accounts = '''            legado = iald_motores.ContaDoPedido(
                razao, user, modelo, cfg.precos(modelo), chave_cota=chave_cota, plano=plano,
                prefixo_tokens=prefixo,
                # 21/09/2026 (revisão de custo): chamada sem usage no razão do claude × fator_tokens,
                # como o guarda de reservas a liquida (1.0 na OpenAI: como antes)
                fator_tokens=cfg.fator_tokens if claude else 1.0)
            conta = iald_orcamento.ReservedAccount(
                _guarda_do_motor(motor), legado, cfg, user, admin, modelo, quota_key=chave_cota,
                group=plano, group_limit=cfg.cota_global_gratuito_usd if gratuito else None)'''
new_accounts = '''            if haiku:
                conta = legado = _HaikuNativeAccount(motors=iald_motores, budget=iald_orcamento,
                    guard=_guarda_do_motor(motor), ledger=razao, cfg=cfg, user=user, admin=admin,
                    model=modelo, quota_key=chave_cota, plan=plano, prefix_tokens=prefixo,
                    count_request=tokens_para_saldo)
            else:
''' + '\n'.join('    ' + line for line in old_accounts.splitlines())
change(old_accounts, new_accounts)
from integrate_haiku_context import patch_server, patch_client
text = patch_server(text)
ast.parse(text)
out=W/('claude_routes_stage_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));out.mkdir()
server=(text.replace('\n',nl)).encode('utf-8')
with (out/'iald_web_server.py').open('xb')as f:f.write(server)
jsraw=(ROOT/'app/iald.js').read_bytes();js=jsraw.decode('utf-8')
assert js.count('const atual = S.motor && S.motor.motor;')==1
js=js.replace('const atual = S.motor && S.motor.motor;', 'const atual = S.motor && (S.motor.motor_selecao || S.motor.motor);')
assert js.count('|| m.motor === motor ||')==1
js=js.replace('|| m.motor === motor ||','|| (m.motor_selecao || m.motor) === motor ||')
js=patch_client(js)
with (out/'iald.js').open('xb')as f:f.write(js.encode('utf-8'))
receipt={'status':'STAGED_NOT_DEPLOYED','original_server_sha256':hashlib.sha256(raw).hexdigest(),
 'server_sha256':hashlib.sha256(server).hexdigest(),'original_js_sha256':hashlib.sha256(jsraw).hexdigest(),
 'js_sha256':hashlib.sha256(js.encode()).hexdigest(),
 'remaining':['Admin model route/status review','Quota estimate/native count interaction','History truncation review','Flask extracted route regression tests','Deployment approval audit and restart','Native asset sync and distribution']}
with (out/'receipt.json').open('x',encoding='utf-8')as f:json.dump(receipt,f,indent=2)
print(out)
