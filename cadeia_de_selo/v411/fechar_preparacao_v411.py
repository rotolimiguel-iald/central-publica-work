# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] so' adaptado (ato da gerencia, nao executado pelo construtor): a rota lida do registro da abertura (o da gerencia, ou o do construtor de 12/11); a prosa da v411 montada do PRONTA e do delta (nenhum modulo novo; o teste aberto e recalculado; a moldura; as ressalvas; E41 a E43); o revisor (D109); o slug de 12/11; RECUSA no ensaio e sem pronta = true
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] so' a PROSA da anotacao e do deposito: a v410 agora e' IALD2 e A Escala (D82 a D87), com o H0DN x BG1 pré-registrado e o recibo documental HMS/13 (D80); dois modulos; os nomes RATIFICADOS (D74 e D87); a excecao D80 ao veto da pasta do Kimi; segue ato da gerencia, NAO executado pelo adaptador
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_conferidores_v410.py] o registro ABERTO do Mapa e' um objeto, nao lista (o [0] quebrava); segue ato da gerencia, nao executado pelo construtor
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] so' adaptado (ato da gerencia, nao executado pelo construtor): a prosa da v410 (Mapa, fila, ACOM: a moldura da D64 e as ressalvas), o revisor pela D69, o slug de 06/11; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""fechar_preparacao_v411.py -- o fim da preparacao, depois de gerar_relatorio_v411.py: (1) a ANOTACAO de fechamento da rota do Mapa de Rotas aberta pela preparacao (o rota_id e' LIDO do registro que a abriu: registro_mapa_prep_v411_ABERTA.json, se a gerencia o gravou, ou registro_mapa_construtor_v411.json, o da abertura pelo construtor em 12/11: a rota cadeia.preparacao_v411),
Tudo LE PREPARACAO_v411_PRONTA.json: nenhum hash e' digitado aqui. Idempotente por marcador (.FECHADA_<sha16 do PRONTA>): uma segunda rodada com o mesmo PRONTA nao repete nada. Molde: fechar_preparacao_v410.py, adaptado em 12/11/2026 a v411 pelo fork B do claude-construtor-v411 (nenhum modulo novo; o registro h0dn_bg1_v411; nenhuma chave antiga muda).
FAIL-CLOSED ANTES de qualquer efeito: exige PREPARACAO_v411_PRONTA.json com pronta = true (e nao o ensaio do topo proposto), a SESSION_REFERENCE_prep_v411.json (a inscricao ACOM da preparacao), o registro da abertura da rota e os artefatos que a anotacao cita; sem eles PARA sem efeito.
NAO foi executado na adaptacao (ato do gerente, depois do gerar_relatorio_v411.py e da revisao de terceiro).
uso: python -I -B -X utf8 fechar_preparacao_v411.py"""
import hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
if os.environ.get("V411_ENSAIO_TOPO_PROPOSTO") == "1":   # (v411) o ensaio do topo proposto depura a cadeia: nao e' preparacao
    raise SystemExit("RECUSO: modo de ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1): nada vai ao Mapa, a fila nem a ACOM")
import importlib.util as _ilu
_sp_dl = _ilu.spec_from_file_location("delta_v411_fechar", os.path.join(HERE, "delta_v411.py")); DL = _ilu.module_from_spec(_sp_dl); _sp_dl.loader.exec_module(DL)   # (v411) a moldura e as listas, LIDAS do DESENHO pelo delta
PR = os.path.join(HERE, "PREPARACAO_v411_PRONTA.json"); J = json.load(open(PR, encoding="utf-8")); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
MARCA = os.path.join(HERE, ".FECHADA_" + S)
if os.path.exists(MARCA):
    print("ja fechada para este PRONTA:", S); sys.exit(0)
assert J.get("pronta") is True and not J.get("ensaio_topo_proposto"), ("FAIL-CLOSED: a preparacao nao esta' pronta", J.get("falta"))
PY = r"C:\Python314\python.exe"
REF_ = os.path.join(HERE, "SESSION_REFERENCE_prep_v411.json")
ABERTA_ = os.path.join(HERE, "registro_mapa_prep_v411_ABERTA.json")
if not os.path.exists(ABERTA_):   # (v411) a rota da preparacao foi aberta pelo construtor, em 12/11, por este registro
    ABERTA_ = os.path.join(HERE, "registro_mapa_construtor_v411.json")
for _n_ in (REF_, ABERTA_, os.path.join(HERE, "RELATORIO_PREPARACAO_v411.md"), os.path.join(HERE, "PLANO_v411.md")):
    assert os.path.exists(_n_), ("FAIL-CLOSED: falta %s -- nao registro no Mapa, nao deposito na fila e nao transiciono a ACOM (a inscricao ACOM e a rota da preparacao v411 sao ato da gerencia)" % os.path.basename(_n_))
_ab0 = json.load(open(ABERTA_, encoding="utf-8")); _ab = _ab0[0] if isinstance(_ab0, list) else _ab0   # (o registro da abertura e' UM objeto; aceita-se a lista, como na v409)
ROTA = _ab["rota_id"]; REFS = list(_ab.get("refs") or [])   # a rota e as rotas-mae sao LIDAS do registro que a gerencia abriu: nada digitado
MEM = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "memoria.py")
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
port = J["portoes"]; p_ok = [k for k, v in port.items() if v]; p_no = [k for k, v in port.items() if not v]
fpt = lambda x_: ("%.2f" % x_).replace(".", ",").replace("-", "\u2212") if isinstance(x_, (int, float)) and not isinstance(x_, bool) else "n/d"
_pri = (J.get("h0dn") or {}).get("primario") or {}; _cef = (J.get("h0dn") or {}).get("cefeidas_livres") or {}
MOLDURA = DL.FRASE_MOLDURA_V411_PT % (fpt(_pri.get("z_null")), fpt(_pri.get("z_tgl")), _pri.get("ramo", "n/d"), fpt(_cef.get("z_null")), _cef.get("ramo", "n/d"))
res = ("candidato %s (%s B, base v410 %s); pronta=%s; portoes que passaram: %s; que nao passaram: %s; kernel recibo %s (%s modulo novo: o kernel e' o da v410); ESPERADOS %s; p00 %s (%s/%s; pendentes: %s); ensaio a seco %s; escada %s; %s bandeiras novas" % (
    J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], ", ".join(p_ok), ", ".join(p_no) or "nenhum", J["kernel_recibo"]["sha16"], J.get("n_modulos_novos"), J["esperados_sha16"], J["p00"]["sha16"], J["p00"]["passaram"], J["p00"]["n"], len(J["p00"].get("pendentes") or []), J["ensaio_a_seco"]["veredito"], J["escada"], J["n_bandeiras_novas"]))
# (1) o Mapa
anot = [{"tipo": "ANOTACAO", "rota_id": ROTA, "estatuto": "REAL", "olhou_dados": False,
         "titulo": "v411 preparada (o teste H0DN x BG1 aberto e recalculado no rito; nenhum modulo novo): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,
         "proximo_passo": "revisao de terceiro (o Sonnet, D109: uma rodada de conserto e uma conferencia unica; quem constroi nao aprova); depois o orquestrador pos_treino_v411 instala, roda o rito e a cadeia ate' o HANDOFF; a rota da versao selada sera a da v411",
         "nota": "quem constroi nao aprova: " + J["nao_revisado_por_terceiro"], "artefatos": [PR, os.path.join(HERE, "RELATORIO_PREPARACAO_v411.md"), os.path.join(HERE, "PLANO_v411.md")], "refs": REFS}]
ja = os.path.join(HERE, "registro_mapa_preparacao_v411_ANOTACAO.json")
tmp = ja + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(anot, ensure_ascii=False, indent=1)); os.replace(tmp, ja)
r1 = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "registrar", ja, "--quem", "claude-construtor-v411"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, r1.stdout[-240:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
# (2) a fila da memoria
txt = ("v411 (o teste decisivo: H0DN x BG1 aberto uma vez, depois do commit publico do pre-registro; a emenda e o resultado RECALCULADO no rito pelo registro %s, a partir dos bytes embutidos; nenhum modulo novo de kernel) preparada em 12/11/2026 por claude-construtor-v411 para a gerencia c1 (nada instalado; o rito nao rodou). " % DL.FECHO_REGISTRO + res + ".\n\n"
       + "O teste, do registro (" + str((J.get("h0dn") or {}).get("origem_dos_numeros")) + "): " + MOLDURA + ". O que o teste nao decide: " + "; ".join(DL.NAO_DECIDE_RESUMO_PT) + ". As sete ressalvas: "
       + "; ".join("%d %s" % (i_ + 1, r_) for i_, r_ in enumerate(DL.RESSALVAS_ROTULOS_PT)) + ". As erratas ao lado, em nome proprio da gerencia c1: " + ", ".join(DL.ERRATAS_IDS_V411)
       + ". P = nP " + DL.D10.FRASE_QUALIFICADOR_PT + " (D64 e D84 da v410).\n\n"
       "Avisos para a gerencia:\n" + "\n".join("- " + a for a in J["avisos"]) + "\n\nQuem constroi nao aprova: " + J["nao_revisado_por_terceiro"] + ".\n")
ta = os.path.join(HERE, "DEPOSITO_PREPARACAO_v411.md")
tmp = ta + ".tmp"; open(tmp, "w", encoding="utf-8").write(txt); os.replace(tmp, ta)
r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-construtor-v411", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v411-preparada-12nov", "--casa", "Central de Patentes", "--slug", "v411-preparada-12nov",
                     "--fonte", PR, "--fonte", os.path.join(HERE, "RELATORIO_PREPARACAO_v411.md"), "--texto-arquivo", ta], capture_output=True, text=True, encoding="utf-8")
print("fila:", r2.returncode, (r2.stdout + r2.stderr)[-300:].replace("\n", " "))
assert r2.returncode == 0, r2.stdout + r2.stderr
# (3) a transicao ACOM (revisao lida agora; evento estavel pelo sha16 do PRONTA)
ref = REF_; CLI = [PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MEMORIA_IALD", "session_memory.py")]
g = subprocess.run(CLI, input=json.dumps({"operation": "get", "reference": ref}), capture_output=True, text=True, encoding="utf-8"); rev = json.loads(g.stdout)["result"]["revision"]
req = {"operation": "transition", "reference": ref, "expected_revision": rev, "event_id": "prep-v411-fechada-" + S, "actor": {"id": "claude-construtor-v411", "kind": "agent"},
       "changes": {"records": [{"id": "prep_v411_fechada_" + S, "kind": "fact", "statute": "REAL", "text": res, "sources": [{"kind": "artifact", "ref": PR}]}], "flow": {"phase": "entregue_a_gerencia", "next_action": "a gerencia e o orquestrador pos-treino decidem a partir de PREPARACAO_v411_PRONTA.json"}}}
r3 = subprocess.run(CLI, input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8")
print("acom:", r3.returncode, r3.stdout[:160])
assert r3.returncode == 0, r3.stdout + r3.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("preparacao fechada:", S)
