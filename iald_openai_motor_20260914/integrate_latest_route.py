from pathlib import Path
import os
import re

root = Path(__file__).parent
path = root/'stage/iald_web_server.py'
text = path.read_text(encoding='utf-8')
pattern = r'(?ms)^<<<<<<< .*?\n.*?^=======\n(.*?)^>>>>>>> [^\n]*\n'
text, n = re.subn(pattern, lambda m: m.group(1), text)
assert n == 1
start = text.index('def _chat_openai(')
end = text.index('\n\n@app.route("/api/motor"', start)
route = text[start:end]

def change(old, new):
    global route
    assert route.count(old) == 1, old[:100]
    route = route.replace(old, new, 1)

change('    cfg = MOTORES_CFG', '    import copy\n    cfg = copy.copy(MOTORES_CFG)')
change('    limites = iald_motores.limites_do_plano(cfg, plano)      # já lido sem erro pela permissão',
'''    limites = iald_motores.limites_do_plano(cfg, plano)
    cfg.cota_usuario_usd = cfg.cota_operador_usd = limites["usd_dia"]
    if gratuito:
        cfg.janela = min(cfg.janela, 32768)
'''.rstrip())
change('''        usar_agente = limites["agente"] and bool(permitidas) and not tem_imagem and _precisa_ferramentas(ultima)''',
'''        # Canonical retrieval is part of the IALD memory, including the free tier.
        # Plan flags still govern general-purpose web tools.
        if not limites["agente"]:
            permitidas = []
        if cfg.memoria_modo != "prompt":
            permitidas += iald_kernel.tool_definitions() + iald_memoria_canonica.tool_definitions()
        usar_agente = bool(permitidas) and (cfg.memoria_modo != "prompt" or
                         (not tem_imagem and _precisa_ferramentas(ultima)))''')
change('''            para_openai, info = iald_motores.montar_mensagens(
                mensagens, PROMPT_EXTERNO, modelo, nomes, cfg.janela, teto_saida, instrucao)''',
'''            prompt_externo, memoria_info = _contexto_externo()
            para_openai, info = iald_motores.montar_mensagens(
                mensagens, prompt_externo, modelo, nomes, cfg.janela, teto_saida, instrucao)''')
change('chave_cache="iald-" + PROMPT_EXTERNO_SHA[:16]', 'chave_cache="iald-" + memoria_info["context_sha256"][:16]')
change('''        conta = iald_motores.ContaDoPedido(
            RAZAO_OPENAI, user, modelo, cfg.precos(modelo), chave_cota=chave_cota, plano=plano,
            prefixo_tokens=iald_motores.prefixo_tokens_estimado(para_openai))''',
'''        try:
            conta = iald_orcamento.ReservedAccount(
                _guarda_openai(), iald_motores.ContaDoPedido(
                    RAZAO_OPENAI, user, modelo, cfg.precos(modelo), chave_cota=chave_cota, plano=plano,
                    prefixo_tokens=iald_motores.prefixo_tokens_estimado(para_openai)),
                cfg, user, admin, modelo, quota_key=chave_cota,
                group=plano, group_limit=cfg.cota_global_gratuito_usd if gratuito else None)
        except Exception:
            return _sse_aviso("O controle de reservas de uso está indisponível; nenhuma chamada foi enviada.", "limite")''')
change('''            adaptador = iald_motores.AdaptadorAgente(cfg, base, url, cabecalhos, conta)''',
'''            exigir_consulta = cfg.memoria_modo != "prompt" and bool(re.search(
                r"\\b(localiz\\w*|procur\\w*|busqu\\w*|pesquis\\w*|consult\\w*|verifi\\w*|confira|conferir|leia|ler)\\b", ultima))
            adaptador = iald_motores.AdaptadorAgente(cfg, base, url, cabecalhos, conta,
                                                   exigir_consulta=exigir_consulta)''')
change('''                                          max_voltas=GRATUITO_MAX_VOLTAS_AGENTE if gratuito else None)
                finally:
                    conta.fechar()''',
'''                                          max_voltas=(GRATUITO_MAX_VOLTAS_AGENTE
                                              if gratuito and cfg.memoria_modo == "prompt" else None))
                except (iald_orcamento.BudgetError, iald_memoria_canonica.MemoryUnavailable) as exc:
                    yield from _sse_aviso(str(exc), "limite").response
                except Exception as exc:
                    print("[motores] falha do agente: " + iald_motores.mascarar(exc), flush=True)
                    yield from _sse_aviso("Falha no serviço externo; o registro de uso foi preservado.", "falha_motor").response
                finally:
                    conta.fechar()''')
change('''                        conta.iniciar_chamada(payload)
                        try:''', '''                        try:
                            conta.iniciar_chamada(payload)''')
change('''                            if not enviou and exc.status != 502:''',
'''                            if not enviou and exc.status in (400, 401, 403, 404, 413, 422, 429):''')
change('''                        except Exception as exc:          # noqa: BLE001 — rede, timeout''',
'''                        except (iald_orcamento.BudgetError, iald_memoria_canonica.MemoryUnavailable) as exc:
                            texto = str(exc)
                        except Exception as exc:          # noqa: BLE001 — rede, timeout''')
text = text[:start] + route + text[end:]
compile(text, str(path), 'exec')
temporary = path.with_suffix('.tmp')
temporary.write_bytes(text.encode('utf-8'))
os.replace(temporary,path)
print('Latest route integrated; source server unchanged.')
