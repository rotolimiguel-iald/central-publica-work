# -*- coding: utf-8 -*-
"""_fechar_retomada_construtor_v411.py -- (claude-construtor-v411, retomada, 12/11/2026, fim da sessao do principal) grava, LENDO do disco: (1) PRONTO_PARA_GERAR_v411.json (backup de bytes antes) com o estado da cadeia
REAL no momento (o candidato, o ensaio, o que passou, o que falta, o campo p2_ao_lado_da_v387 e de onde o rotulo e' lido, a sequencia cadeia_v411.sh); (2) um deposito na fila da memoria (pasta do construtor; so' acrescimo);
(3) uma ANOTACAO na rota cadeia.preparacao_v411 do Mapa de Rotas; (4) a transition ACOM da referencia SESSION_REFERENCE_prep_v411.json. Nada no Nos. uso: python -B -X utf8 _fechar_retomada_construtor_v411.py"""
import datetime, glob, hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
PY = sys.executable
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
J = lambda p: json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
agora = datetime.datetime.now(); TS = agora.strftime("%Y%m%d_%H%M%S")
CM = J(DL.MANIFESTO_ARQ) or {}; EN = J(DL.saida("ensaio_a_seco_v411.json")) or {}; PC = J(DL.saida("PRECONDICOES_v411.json")) or {}; CIT = J(DL.saida("conferir_citacoes_v411.json")) or {}
TO = J(os.path.join(HERE, "TESTE_H0DN_OFFLINE_v411.json")) or {}; PRON = J(os.path.join(DL.ENSAIO_DIR, "PRONTO_PARA_O_POS_RITO.json")); PREP = J(DL.saida("PREPARACAO_v411_PRONTA.json"))
cand16 = sha(DL.CANDIDATO_ARQ)[:16] if os.path.exists(DL.CANDIDATO_ARQ) else None
_marca = "[A ADAPTAR v" + "411]"
marcados = sorted(os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "**", "*"), recursive=True) if os.path.isfile(p_) and ".bak_" not in p_ and os.sep + "bump" + os.sep not in p_
                  and not p_.endswith((".json", ".txt", ".diff", ".log", ".npz", ".lean", ".md")) and os.path.basename(p_) not in ("_bump_copia_v411.py", "p00_precondicoes_v411.py") and _marca in open(p_, "rb").read().decode("utf-8", "replace"))
ensaio_ok = EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == cand16
out = {"contrato": "PRONTO_PARA_GERAR_v411", "quando": agora.isoformat(timespec="seconds"), "agente": "claude-construtor-v411 (retomada; principal + forks A, B e C)", "topo_ratificado_presente": os.path.exists(DL.TOPO_RATIFICADO_ARQ),
       "topo_ratificado_sha256": DL.TOPO_SHA256,
       "estado": ("CADEIA REAL EM CURSO: o candidato de verdade existe (do TOPO_RATIFICADO_v411.json); o ensaio a seco %s; o fork C segue a cadeia (esperados, conferidores, diff e pinos, instalar/rito, p00, PRONTO_PARA_O_POS_RITO, fim_de_cadeia B20, purga, relatorio)"
                  % ("TUDO PASSOU" if ensaio_ok else "AINDA NAO PASSOU para este candidato (ultimo veredito: %s)" % str(EN.get("veredito"))[:160])),
       "candidato": {"arquivo": DL.CANDIDATO_ARQ, "sha16": cand16, "manifesto_sha16": CM.get("sha16"), "n_patches": CM.get("n_patches"), "verbatins_embutidos": CM.get("verbatins_embutidos"), "topo": CM.get("topo")},
       "scripts_com_a_marca_de_copia_mecanica": marcados, "n_marcados": len(marcados),
       "registro_h0dn_bg1_v411": {"offline_n_ok": TO.get("n_ok"), "offline_TUDO_PASSOU": TO.get("TUDO_PASSOU"), "p2_ok": TO.get("p2_ok")},
       "campo_novo_p2_ao_lado_da_v387": {"onde": "core['h0dn_bg1_v411']['p2_ao_lado_da_v387'] (e no resumo do selo, selo['h0dn_bg1_v411']['p2_ao_lado_da_v387'])", "chaves": ["rotulo", "rotulo_e_proposta", "rotulo_de", "rotulo_selado_da_v387", "registro_selado", "canal", "nota"],
                                         "rotulo_lido_de": DL.P2_ROTULO_DE, "rotulo": DL.P2_ROTULO, "rotulo_selado_da_v387_lido_de": "o trecho do veredito de core['three_stress_tests_v387'] que contem P2_NOT_DETERMINED (nunca digitado; o veredito selado nao muda)",
                                         "preenchido_so_quando": "o registro passa e o ramo primario recalculado e' o do molde (BRANCH_4); em recusa, nulo", "checagem": "DENTRO da c14 (N_CHECKS_FECHO segue 16): o rotulo selado traz o token e o campo novo nao o altera"},
       "chaves_congeladas_com_a_g1": "nao renomeadas; acrescentadas so': p2_ao_lado_da_v387 (registro e selo)",
       "listas": {"falas": DL.N_FALAS_V411, "textos_da_gerencia_citados": len(DL.TEXTOS_DA_GERENCIA_CITADOS), "decisoes": list(DL.DECISOES_V411), "erratas": DL.ERRATAS_IDS_V411, "marcadores_do_topo": len(DL.MARCADORES_V411 or {})},
       "citacoes": {"ok_do_um_py": CIT.get("ok_do_um_py"), "ok_do_pos_rito": CIT.get("ok_do_pos_rito"), "pedido": "pos_rito\\blocos_custodia_v411.py (outra frente): aspas angulares em comentarios e mensagens; ver PEDIDOS_ENTRE_FRENTES_v411.md"},
       "p00": {"veredito": PC.get("veredito"), "n_falhas": PC.get("n_falhas"), "pendentes": [x_.get("checagem") for x_ in PC.get("pendentes") or []]},
       "pronto_para_o_pos_rito": {"arquivo": os.path.join(DL.ENSAIO_DIR, "PRONTO_PARA_O_POS_RITO.json"), "existe": PRON is not None},
       "preparacao_pronta": {"arquivo": DL.saida("PREPARACAO_v411_PRONTA.json"), "existe": PREP is not None, "pronta": (PREP or {}).get("pronta")},
       "artefato_de_ensaio_do_topo_proposto": {"pasta": DL.ENSAIO_DIR, "nota": "fica como esta', fora de work; NAO e' candidato"},
       "sequencia_exata": {"script": "cadeia_v411.sh", "sha16": sha(os.path.join(HERE, "cadeia_v411.sh"))[:16], "uso": "sh ./cadeia_v411.sh (REAL; exige TOPO_RATIFICADO_v411.json); V411_ENSAIO_TOPO_PROPOSTO=1 para o ensaio do topo proposto"},
       "interpretacoes_para_a_gerencia": [
           "o fork C fez a fonte AUSENTE de um marcador do topo (None no core) virar a frase visivel de que o resultado nao e' dito, em vez de levantar (o artigo inteiro cairia); valor nao finito, marcador que sobra e o livro que nao sustenta a frase seguem PARAR",
           "o conferir_citacoes separa os escopos (rc 2 = so' o pos-rito reprova); o ensaio e o fim_de_cadeia aceitam esse pendente; o relatorio final exige os dois",
           "a guarda de material privado do p00 sobre o candidato: nenhuma ocorrencia a mais que no um.py selado da v410 (2 = 2, so' contagens); o texto novo segue varrido limpo",
           "as aspas da fala do autor no quadro vem de constantes (_V411_AB, _V411_FE); a citacao renderizada e' verbatim (conferida por bytes)",
           "a traducao EN do item da fala do autor e do titulo/frases EN do quadro e' do construtor (marcada para a revisao)"],
       "da_gerencia": ["revisao de terceiro", "fechar_preparacao_v411.py e acom_inscrever_prep_v411.py (adaptados, nao executados)", "pino_memoria_py_v411.py e a folga do MEMORY.md", "a tarefa agendada", "o S3, o rito, a custodia"]}
p = os.path.join(HERE, "PRONTO_PARA_GERAR_v411.json")
if os.path.exists(p):
    open(p + ".bak_" + TS, "wb").write(open(p, "rb").read())
b = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("PRONTO_PARA_GERAR:", sha(p)[:16])
# (2) o deposito na fila
FILA = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-construtor-v411")
fontes = [p_ for p_ in (p, os.path.join(HERE, "cadeia_v411.sh"), DL.MANIFESTO_ARQ, os.path.join(HERE, "DESENHO_v411.md"), os.path.join(HERE, "PEDIDOS_ENTRE_FRENTES_v411.md")) if os.path.exists(p_)]
txt = ("v411, RETOMADA do claude-construtor-v411 (12/11/2026): a E43 ao lado (as seis aberturas da Escala nao trocadas na renderizacao); o aditivo do P2 (campo p2_ao_lado_da_v387, rotulo lido de TOPO_RATIFICADO_v411.json; "
       "checagem dentro da c14; o token selado da v387 nao muda); o topo ratificado (12 marcadores dirigidos pela tabela do arquivo, fail-closed do livro, a fala do autor no quadro, F65 com os nomes fixos da convencao dos 5 sigma; "
       "11 falas; D159 a D173); os scripts da cadeia adaptados de verdade pelos forks A, B e C (marcados restantes: %d); o candidato REAL %s; ensaio a seco: %s. Pendentes: o que o fork C ainda roda, as citacoes do pos-rito "
       "(outra frente) e os atos da gerencia. O gate nao se move; provado e' validade, nao creditacao.\n") % (len(marcados), cand16, "TUDO PASSOU" if ensaio_ok else "em curso")
cab = ("---\nquem: claude-construtor-v411\ncasa: Central de Patentes\ntipo: project\nestatuto: REAL\nalvo_sugerido: novo:v411-preparacao-retomada-12nov\ndepositado_em: %s\nfontes:\n" % agora.astimezone().isoformat(timespec="seconds")
       + "".join("  - %s  sha256:%s\n" % (p_, sha(p_)) for p_ in fontes) + "---\n")
dst = os.path.join(FILA, TS + "_v411-preparacao-retomada-12nov.md"); assert not os.path.exists(dst)
bd = (cab + txt).encode("utf-8"); open(dst + ".tmp", "wb").write(bd); assert os.path.getsize(dst + ".tmp") == len(bd); os.replace(dst + ".tmp", dst); print("deposito:", dst)
# (3) a anotacao no Mapa de Rotas (a guarda do Mapa recusa a palavra da creditacao: "conferiu")
reg = {"tipo": "ANOTACAO", "rota_id": "cadeia.preparacao_v411", "texto": ("[REAL, lido dos artefatos] retomada do construtor: a cadeia REAL comecou do TOPO_RATIFICADO_v411.json (sha16 %s); candidato %s; o registro offline 16/16 com o P2 ao lado; "
                                                                           "11 falas, D159 a D173, E41 a E43; o ensaio a seco %s; citacoes: escopo do um.py limpo, o do pos-rito pendente da outra frente; o fork C segue ate o relatorio. "
                                                                           "Nao refazer: o kernel do k411c (medido); o recibo do kernel complementado so' por medicao.") % ((DL.TOPO_SHA256 or "")[:16], cand16, "conferiu TUDO PASSOU" if ensaio_ok else "em curso"),
       "artefatos": [p_ for p_ in (p, os.path.join(HERE, "cadeia_v411.sh")) if os.path.exists(p_)]}
ja = os.path.join(HERE, "registro_mapa_retomada_v411.json"); open(ja, "w", encoding="utf-8").write(json.dumps(reg, ensure_ascii=False, indent=1))
r = subprocess.run([PY, "-B", "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py"), "registrar", ja, "--quem", "claude-construtor-v411"], capture_output=True, text=True, encoding="utf-8")
print("mapa rc", r.returncode, (r.stdout or r.stderr)[-300:])
# (4) a transition ACOM (referencia propria)
ref = os.path.join(HERE, "SESSION_REFERENCE_prep_v411.json")
req = {"operation": "transition", "reference": ref, "expected_revision": None, "event_id": "construtor-v411-retomada-" + TS,
       "q": {"records": [{"text": txt.strip(), "source": p, "status": "REAL"}]}, "p": {"phase": "cadeia_real_em_curso", "next_action": "fork C: esperados, conferidores, PRONTO_PARA_O_POS_RITO, fim_de_cadeia B20, purga, relatorio; gerencia: revisao de terceiro e atos"}}
rj = os.path.join(HERE, "acom_prep_%s_transition.request.json" % TS); open(rj, "w", encoding="utf-8").write(json.dumps(req, ensure_ascii=False))
ra = subprocess.run([PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MEMORIA_IALD", "session_memory.py")], input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8")
open(os.path.join(HERE, "acom_prep_%s_transition.receipt.json" % TS), "w", encoding="utf-8").write(ra.stdout or ra.stderr or "")
print("acom rc", ra.returncode, (ra.stdout or ra.stderr)[:300])
