from pathlib import Path

root = Path(__file__).parent / 'stage'

def change(text, old, new, count=1):
    if text.count(old) != count:
        raise ValueError(f'Unexpected occurrence count for {old[:90]!r}: {text.count(old)}')
    return text.replace(old, new, count)

p = root / 'iald_motores.py'
s = p.read_text(encoding='utf-8')
s = change(s, '    "gpt-5-nano": (0.05, 0.005, 0.40),', '    "gpt-5-nano": (0.05, 0.005, 0.40),\n    "gpt-4.1-nano": (0.10, 0.025, 0.40),')
s = change(s, '        self.janela = 32768', '        self.janela = 32768\n        self.memoria_modo = "prompt"\n        self.atlas_path = ""\n        self.kernel_bundle = ""')
s = change(s, '        janela=numero("IALD_OPENAI_JANELA", 32768, int, 16384),', '        janela=numero("IALD_OPENAI_JANELA", 32768, int, 16384),\n        memoria_modo=texto("IALD_MEMORIA_MODO", "prompt"),\n        atlas_path=texto("IALD_ATLAS_PATH"),\n        kernel_bundle=texto("IALD_KERNEL_BUNDLE"),')
s = change(s, '    if esforco and not cfg.esforco_recusado(modelo):', '    if esforco and not modelo.startswith("gpt-4.1") and not cfg.esforco_recusado(modelo):')
s = change(s, '        "do operador."', '        "do operador sem a ferramenta correspondente. Consultas ao Atlas e ao kernel "\n        "só podem ser afirmadas quando suas ferramentas retornarem evidências nesta conversa."')
p.write_bytes(s.encode('utf-8'))

p = root / 'iald_web_server.py'
s = p.read_text(encoding='utf-8')
s = change(s, 'import iald_motores  # noqa: E402', '''import iald_motores  # noqa: E402
import iald_kernel  # noqa: E402
import iald_memoria_canonica  # noqa: E402
import iald_orcamento  # noqa: E402
''')
marker = 'LIMITE_OPENAI = iald_motores.JanelaDePedidos(MOTORES_CFG.pedidos_por_minuto, 60.0)'
s = change(s, marker, marker + '''
MEMORIA_EXTERNA = None
KERNEL_EXTERNO = None
ERRO_MEMORIA_EXTERNA = ""
GUARDA_OPENAI = None
_TRAVA_GUARDA_OPENAI = threading.Lock()
if MOTORES_CFG.memoria_modo != "prompt":
    try:
        MEMORIA_EXTERNA = iald_memoria_canonica.CanonicalMemory(
            MOTORES_CFG.atlas_path, MOTORES_CFG.memoria_modo)
        KERNEL_EXTERNO = iald_kernel.KernelCatalog(MOTORES_CFG.kernel_bundle)
        MEMORIA_EXTERNA.snapshot()
    except (ValueError, OSError) as exc:
        ERRO_MEMORIA_EXTERNA = str(exc)
        print("[motores] memória/kernel indisponíveis: " + str(exc), flush=True)


def _guarda_openai():
    global GUARDA_OPENAI
    with _TRAVA_GUARDA_OPENAI:
        if GUARDA_OPENAI is None:
            GUARDA_OPENAI = iald_orcamento.SpendingGuard(
                RAZAO_OPENAI.caminho + ".reservas.sqlite3", RAZAO_OPENAI.caminho)
        return GUARDA_OPENAI


def _contexto_externo():
    if MOTORES_CFG.memoria_modo == "prompt":
        return PROMPT_EXTERNO, {"mode": "prompt", "context_sha256": PROMPT_EXTERNO_SHA}
    if ERRO_MEMORIA_EXTERNA or MEMORIA_EXTERNA is None or KERNEL_EXTERNO is None:
        raise ValueError("A memória canônica ou o kernel integral estão indisponíveis.")
    return MEMORIA_EXTERNA.prompt(PROMPT_EXTERNO, KERNEL_EXTERNO)
''')
s = change(s, '    if not PROMPT_EXTERNO:\n', '''    if MOTORES_CFG.memoria_modo != "prompt":
        try:
            _contexto_externo()
        except (ValueError, OSError):
            return "A memória canônica ou o kernel integral não puderam ser validados; o envio externo está bloqueado."
    known_windows = {"gpt-5-nano": 400000, "gpt-4.1-nano": 1047576}
    if modelo in known_windows and MOTORES_CFG.janela > known_windows[modelo]:
        return "A janela configurada excede a capacidade documentada do modelo."
    if not PROMPT_EXTERNO:
''')
s = change(s, '    usar_agente = bool(permitidas) and not tem_imagem and _precisa_ferramentas(ultima)', '''    if cfg.memoria_modo != "prompt":
        permitidas += iald_kernel.tool_definitions() + iald_memoria_canonica.tool_definitions()
    usar_agente = bool(permitidas) and not tem_imagem and (
        cfg.memoria_modo != "prompt" or _precisa_ferramentas(ultima))''')
s = change(s, '''    try:
        para_openai, info = iald_motores.montar_mensagens(
            mensagens, PROMPT_EXTERNO, modelo, nomes, cfg.janela, teto_saida,''', '''    try:
        prompt_externo, memoria_info = _contexto_externo()
        para_openai, info = iald_motores.montar_mensagens(
            mensagens, prompt_externo, modelo, nomes, cfg.janela, teto_saida,''')
s = change(s, '        chave_cache="iald-" + PROMPT_EXTERNO_SHA[:16])\n    conta = iald_motores.ContaDoPedido(RAZAO_OPENAI, user, modelo, cfg.precos(modelo))', '''        chave_cache="iald-" + memoria_info["context_sha256"][:16])
    try:
        conta = iald_orcamento.ReservedAccount(
            _guarda_openai(), iald_motores.ContaDoPedido(RAZAO_OPENAI, user, modelo, cfg.precos(modelo)),
            cfg, user, admin, modelo)
    except Exception:
        return _sse_aviso("O controle de reservas de uso está indisponível; nenhuma chamada foi enviada.", "limite")''')
s = change(s, '''                                      ferramentas=permitidas, operator_authorized=False, motor=adaptador)
            finally:''', '''                                      ferramentas=permitidas, operator_authorized=False, motor=adaptador)
            except (iald_orcamento.BudgetError, iald_memoria_canonica.MemoryUnavailable) as exc:
                yield from _sse_aviso(str(exc), "limite").response
            except Exception as exc:
                print("[motores] falha do agente: " + iald_motores.mascarar(exc), flush=True)
                yield from _sse_aviso("Falha no serviço externo; o registro de uso foi preservado.", "falha_motor").response
            finally:''')
s = change(s, '''                    conta.iniciar_chamada(payload)
                    try:''', '''                    try:
                        conta.iniciar_chamada(payload)''')
s = change(s, '                        if not enviou and exc.status != 502:', '                        if not enviou and exc.status in (400, 401, 403, 404, 413, 422, 429):')
s = change(s, '''                    except Exception as exc:          # noqa: BLE001 — rede, timeout''', '''                    except (iald_orcamento.BudgetError, iald_memoria_canonica.MemoryUnavailable) as exc:
                        texto = str(exc)
                    except Exception as exc:          # noqa: BLE001 — rede, timeout''')
s = change(s, '''    if tool_name == "search_web":''', '''    if tool_name.startswith("iald_kernel_") or tool_name.startswith("iald_atlas_"):
        try:
            if tool_name.startswith("iald_kernel_"):
                if KERNEL_EXTERNO is None:
                    raise ValueError("Kernel integral indisponível.")
                result = iald_kernel.execute_tool(KERNEL_EXTERNO, tool_name, arguments)
            else:
                if MEMORIA_EXTERNA is None:
                    raise ValueError("Atlas canônico indisponível.")
                methods = {"iald_atlas_search": MEMORIA_EXTERNA.search, "iald_atlas_read": MEMORIA_EXTERNA.read}
                if tool_name not in methods or not isinstance(arguments, dict):
                    raise ValueError("Consulta canônica inválida.")
                result = methods[tool_name](**arguments)
            return json.dumps(result, ensure_ascii=False)
        except (ValueError, OSError, TypeError) as exc:
            return json.dumps({"status": "UNAVAILABLE", "error": str(exc)}, ensure_ascii=False)

    if tool_name == "search_web":''')
s = change(s, '                if len(result) > AGENT_MAX_RESULT_CHARS:', '                if (len(result) > AGENT_MAX_RESULT_CHARS\n                        and not tool_name.startswith(("iald_kernel_", "iald_atlas_"))):')
s = change(s, '''        for tipo, valor in _linhas_do_stream(
                lambda: req_lib.post(destino, json=payload, headers=cabecalhos,
                                     stream=True, timeout=600)):''', '''        def model_lines():
            if motor is None:
                yield from _linhas_do_stream(lambda: req_lib.post(
                    destino, json=payload, headers=cabecalhos, stream=True, timeout=600))
            else:
                try:
                    yield from iald_motores.linhas_com_espera(lambda: req_lib.post(
                        destino, json=payload, headers=cabecalhos, stream=True,
                        timeout=(10, motor.cfg.timeout)), intervalo=AGENT_KEEPALIVE_SEC)
                except iald_motores.ErroProvedor as exc:
                    if exc.status in (400, 401, 403, 404, 413, 422, 429):
                        motor.conta.descartar_ultima_chamada()
                    yield ("erro", iald_motores.mensagem_ao_usuario(exc))
        for tipo, valor in model_lines():''')
s = change(s, '''        "uso_por_dia_utc": resumo, "erro": erro,''', '''        "uso_por_dia_utc": resumo, "erro": erro,
        "memoria_modo": cfg.memoria_modo,
        "kernel": KERNEL_EXTERNO.status() if KERNEL_EXTERNO else None,
        "reservas_de_gasto": GUARDA_OPENAI.summary() if GUARDA_OPENAI else [],''')
p.write_bytes(s.encode('utf-8'))

p = root / 'requirements.txt'
p.write_bytes(p.read_bytes() + b'\n# Token count for the complete canonical context (OpenAI o200k_base).\ntiktoken==0.14.0\n')
print('Staged memory, whole-kernel tools and per-call reservations integrated.')
