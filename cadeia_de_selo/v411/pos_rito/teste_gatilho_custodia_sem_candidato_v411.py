# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411-posrito] REESCRITO para a v411: o HANDOFF do sandbox e' feito pelo S6d DE VERDADE (textos_custodia_handoff_v411.main) e o gatilho confere os marcadores da prosa e os da abertura do H0DN; o corpo da v410 (README_FRENTE/README_O_QUE_SAI) fica no .bak.
"""teste_gatilho_custodia_sem_candidato_v411.py -- o teste POSSIVEL SEM CANDIDATO e SEM RITO do passo FINAL do orquestrador, S9_gatilho_custodia (orquestrador\\pos_treino_v411.py), em SANDBOX
(C:\\t\\k411c\\ensaio_topo_proposto\\pos_rito_gatilho\\): um Nos SINTETICO (um.py falso e o selo dele; o core com o registro h0dn_bg1_v411 do ensaio offline, a Fase 9 V2, as bandeiras, a escada e o gate da v410 selada, e,
SINTETICOS, kh_n1_cobertura_v411 e cunhagens_v411; o diario com o cabecalho; o stdout com o trailer; o HANDOFF com o «O que e'», ao qual o S6d de verdade anexa os textos) e um pacote sintetico (ESPERADOS, horarios,
revisao aprovada). POSITIVO: o gatilho e' escrito no sandbox, inteiro, com os valores lidos, e passa nas guardas; rodar de novo nao reescreve. NEGATIVOS (NAO escreve e registra o motivo): passo falso ou ausente; portao
nao limpo; o HANDOFF sem um texto da abertura (README_RITOS) ou da prosa (COMMIT); marcador sem par; HANDOFF mudado depois do S6d; selo com outro pino, de outra versao ou sem o selftest; escada nao exata; trailer
diferente de RITO_RC=0; revisao nao aprovada; o recibo com outro texto ou com guarda suja; o recibo ausente; os horarios ausentes; um gatilho que ja' exista. SEGURANCA: o gatilho de verdade nunca e' escrito.
rc 0 = passou."""
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; PKG = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(PKG))
import textos_custodia_handoff_v411 as TC  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
from custodia_g1 import textos as TX  # noqa: E402

NOS_REAL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
SB = Path(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_gatilho")
GATILHO_REAL = PKG / "ORDEM_HANDOFF_CUSTODIA_v411.md"
HAVIA = GATILHO_REAL.exists(); HAVIA_SHA = hashlib.sha256(GATILHO_REAL.read_bytes()).hexdigest() if HAVIA else None
sha = lambda b: hashlib.sha256(b).hexdigest()
if SB.exists():
    shutil.rmtree(SB)
NOS, PK = SB / "nos", SB / "pk"; DEST = SB / "ORDEM_HANDOFF_CUSTODIA_v411.md"; CENV = SB / "cen_vazio"; CENV.mkdir(parents=True)


def wr(p, b):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    b = b.encode("utf-8") if isinstance(b, str) else b
    open(str(p) + ".tmpw", "wb").write(b); os.replace(str(p) + ".tmpw", p)


CORE10 = json.loads((NOS_REAL / "um_absoluto.json").read_bytes().decode("utf-8"))["core"]
SELO10 = json.loads((NOS_REAL / "um_absoluto_selo.json").read_bytes().decode("utf-8"))
REG = json.loads((PKG / "TESTE_H0DN_OFFLINE_v411_registro.json").read_bytes().decode("utf-8"))
UM = b"# um.py de ENSAIO do gatilho (nao e' o um.py da v411)\n"; PIN = sha(UM)
core = {k: copy.deepcopy(CORE10[k]) for k in ("teste_de_veracidade_fase9_v397", "kernel_formalization", "external_ladder", "qg_closure", "estatuto_da_prova_v391")}
core["h0dn_bg1_v411"] = copy.deepcopy(REG); core["kh_n1_cobertura_v411"] = copy.deepcopy(CORE10["kh_n1_cobertura_v410"])
core["cunhagens_v411"] = {"verbatim": {"fala_%d" % i: {"quando": "12/11/2026 (ensaio)"} for i in range(TC.DL.N_FALAS_V411)}}
ESC = core["external_ladder"]["n_theorems_clean"]; GATE = core["qg_closure"]["gate"]["verdict"]
assert GATE == SELO10.get("qg_closure_verdict")
selo = {"um_version": "v411", "sha256": {"um.py": PIN}, "fail_closed_selftest": "FAIL_CLOSED_SELFTEST_PASSED", "timestamp": "2026-11-12 23:59:59", "qg_closure_verdict": GATE}
wr(NOS / "um.py", UM); wr(NOS / "um_absoluto.json", json.dumps({"core": core}, ensure_ascii=False)); wr(NOS / "um_absoluto_selo.json", json.dumps(selo, ensure_ascii=False))
wr(NOS / "MEMORIA_DA_LINHAGEM.md", "# diario de ENSAIO\n\n## 12/11/2026 — **v411 SELADA** `%s` — O teste decisivo (v411): nenhum módulo novo, escada %d → %d (ENSAIO)\n" % (PIN[:16], ESC, ESC))
wr(NOS / "rodada_v411_stdout.txt", "rito de ENSAIO\nRITO_RC=0\n")
wr(NOS / "HANDOFF_v411_CUSTODIA.md", "# HANDOFF v411 — CUSTÓDIA (ENSAIO do gatilho)\n\n**O que é:** `um.py` **v411** `%s` (%d B) sobre a v410 `5d9497a721c3589e`; %d/%d; COMPLETA; rc 0; selftest PASSED; gate intocado; ensaio.\n\nCorpo de ensaio.\n"
   % (PIN[:16], len(UM), ESC, ESC))
wr(PK / "ESPERADOS_v411.json", json.dumps({"candidato_sha16": PIN[:16], "origem_sha16": "5d9497a721c3589e", "escada": [ESC, ESC], "qg_closure_gate_verdict_v410": GATE, "vereditos_novos_v411": {"h0dn_bg1_v411": REG["verdict"]}}))
wr(PK / "rito_horarios_v411.txt", "00:00:00\n01:30:00\n")
REVJ = {"aprovada": True, "candidato_sha16": PIN[:16], "revisor": "sintetico (teste do gatilho)", "achados": [{"sev": "BAIXO", "onde": "sintetico"}]}
REV_P = PK / "revisao_terceiro" / "REVISAO_TERCEIRO_v411.json"; wr(REV_P, json.dumps(REVJ))
rc = TC.main(NOS, PK, PK / "pos_rito"); assert rc == 0, "o S6d de ensaio nao passou"
HP = NOS / "HANDOFF_v411_CUSTODIA.md"; REC_P = PK / "pos_rito" / TC.NOME_RECIBO
HANDOFF = HP.read_text(encoding="utf-8")

spec = importlib.util.spec_from_file_location("pos_treino_v411_teste_do_gatilho", str(PKG / "orquestrador" / "pos_treino_v411.py")); O = importlib.util.module_from_spec(spec); spec.loader.exec_module(O)
assert str(O.GATILHO) == str(GATILHO_REAL)
O.ESTADO = SB / "ESTADO.json"; O.LOG = SB / "orquestrador.log"; O.GATILHO = SB / "NAO_USAR_o_gatilho_padrao_foi_desviado.md"; O.NOS = NOS
E0 = {"passos": {k: {"ok": True, "quando": "2026-11-12T00:00:00"} for k in O.PASSOS_ANTES_DO_GATILHO}, "inicio": "2026-11-12T00:00:00", "pid": 0}
E0["passos"]["S4_rito"]["trailer"] = "RITO_RC=0"; E0["passos"]["S6b_aplicar"].update(evento="1700", hash="0123456789abcdef"); E0["passos"]["S6d_textos_custodia"].update(portao_g1_handoff_inteiro="limpo")
RES = {"casos": {}}; ok = True


def roda(e, destino=DEST):
    assert os.path.normcase(str(destino)).startswith(os.path.normcase(str(SB)) + os.sep)
    return O.s9_gatilho_custodia(e, nos=NOS, pk=PK, destino=destino, cen_g1=CENV)


# ---- como no S6d: o HANDOFF INTEIRO no portao do G1, na D59 e na D65
_hex = lambda n, s: set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{%d}(?![0-9a-fA-F])" % n, s))
v6 = [str(x) for x in TX.portao(HANDOFF, _hex(16, HANDOFF) | _hex(64, HANDOFF), rotulo="HANDOFF")]
c = not v6; ok &= c; RES["casos"]["o HANDOFF inteiro no portao do G1 (como no S6d)"] = {"ok": c, "violacoes": v6[:3]}
# ---- POSITIVO
e = copy.deepcopy(E0); r = roda(e); txt = DEST.read_text(encoding="utf-8") if DEST.exists() else ""; p9 = e["passos"].get("S9_gatilho_custodia", {})
rec = json.loads(REC_P.read_text(encoding="utf-8"))
pos = bool(r is True and txt and p9.get("gatilho_escrito") is True and p9.get("sha16") == sha(txt.encode("utf-8"))[:16] and txt.startswith("# ORDEM DE HANDOFF DA GERÊNCIA c1 À SESSÃO DE CUSTÓDIA — v411 SELADA (")
           and all(s in txt for s in ("## A ordem do operador", "## O estado, lido em ", "## O que entrou (para a custódia saber o que publica)", "## O que é da custódia, na ordem", "## Notas"))
           and PIN[:16] in txt and ("escada **%d/%d**" % (ESC, ESC)) in txt and "`RITO_RC=0`" in txt and sha(HP.read_bytes())[:16] in txt and sha(REC_P.read_bytes())[:16] in txt and sha(REV_P.read_bytes())[:16] in txt
           and O.AUT_FRASE in txt and ("«%s»" % O.TRECHO_REGRA) in txt and O.TRECHO_REGRA in O.REGRA_PERMANENTE.read_text(encoding="utf-8") and sha(O.REGRA_PERMANENTE.read_bytes())[:16] in txt
           and ("«%s»" % O.TRECHO_CONTEUDO) in txt and O.TRECHO_CONTEUDO in O.ORDEM_DO_CONTEUDO.read_text(encoding="utf-8") and sha(O.ORDEM_DO_CONTEUDO.read_bytes())[:16] in txt
           and "--ordem" not in txt and "ORDEM DE PUBLICA" not in txt.upper() and "custodiar.py executar --versao v411 --publicar`" in txt
           and rec["textos"]["ARCO_PT"] in txt and "O teste H0DN × BG1 foi aberto UMA vez em 12/11/2026" in txt and "NOT_FALSIFIED nunca é CONFIRMED" in txt
           and not GF.violacoes(txt) and not TX.portao(txt, _hex(16, txt) | _hex(64, txt), rotulo="gatilho") and not Path(str(DEST) + ".tmp").exists())
ok &= pos; RES["casos"]["positivo"] = {"ok": pos, "bytes": len(txt.encode("utf-8")), "motivo_se_falhou": p9.get("motivo") or p9.get("erro")}
print("POSITIVO:", pos, (p9.get("motivo") or p9.get("erro") or "")[:600] if not pos else "")
if pos:
    wr(SB / "GATILHO_RENDIDO_NO_SANDBOX.md", txt)
    m0 = os.path.getmtime(DEST); r2 = roda(e); idem = bool(r2 is True and DEST.read_text(encoding="utf-8") == txt and os.path.getmtime(DEST) == m0); ok &= idem; RES["casos"]["positivo de novo nao reescreve"] = {"ok": idem}
# ---- NEGATIVOS
H0, R0, V0 = HP.read_bytes(), REC_P.read_bytes(), REV_P.read_bytes(); S0 = (NOS / "um_absoluto_selo.json").read_bytes(); C0 = (NOS / "um_absoluto.json").read_bytes(); T0 = (NOS / "rodada_v411_stdout.txt").read_bytes()


def restaura():
    wr(HP, H0); wr(REC_P, R0); wr(REV_P, V0); wr(NOS / "um_absoluto_selo.json", S0); wr(NOS / "um_absoluto.json", C0); wr(NOS / "rodada_v411_stdout.txt", T0)
    if (PK / "rito_horarios_v411.txt.fora").exists():
        os.replace(PK / "rito_horarios_v411.txt.fora", PK / "rito_horarios_v411.txt")
    if DEST.exists():
        DEST.unlink()


def recibo_do(hb, **muda):
    j = json.loads(R0.decode("utf-8")); j["sha16_depois"] = sha(hb)[:16]; j.update(muda); return json.dumps(j, ensure_ascii=False)


def sem(i):
    t = H0.decode("utf-8"); a = t.index("\n<!-- INICIO_%s_v411 -->" % i); b = t.index("<!-- FIM_%s_v411 -->\n" % i) + len("<!-- FIM_%s_v411 -->\n" % i); return (t[:a] + t[b:]).encode("utf-8")


def selo_(**m):
    j = json.loads(S0.decode("utf-8")); j.update(m); return json.dumps(j)


def core_escada():
    j = json.loads(C0.decode("utf-8")); j["core"]["external_ladder"]["n_theorems_clean"] = ESC - 1; return json.dumps(j, ensure_ascii=False)


tx0 = json.loads(R0.decode("utf-8"))["textos"]; g0 = json.loads(R0.decode("utf-8"))["guardas"]
NEG = [("um passo anterior FALSO", lambda e: e["passos"]["S5_cadeia_0_10"].__setitem__("ok", False), None, "passo anterior nao feito ou falso"),
       ("um passo anterior AUSENTE", lambda e: e["passos"].pop("S8_nativa"), None, "passo anterior nao feito ou falso"),
       ("o portao do G1 nao limpo no S6d", lambda e: e["passos"]["S6d_textos_custodia"].__setitem__("portao_g1_handoff_inteiro", {"x": ["sintetico"]}), None, "o portao do G1 nao rodou limpo"),
       ("o HANDOFF sem README_RITOS", None, lambda: (wr(HP, sem("README_RITOS")), wr(REC_P, recibo_do(sem("README_RITOS")))), "faltam"),
       ("o HANDOFF sem COMMIT", None, lambda: (wr(HP, sem("COMMIT")), wr(REC_P, recibo_do(sem("COMMIT")))), "faltam"),
       ("o HANDOFF sem ESTATUTO_P2_EN", None, lambda: (wr(HP, sem("ESTATUTO_P2_EN")), wr(REC_P, recibo_do(sem("ESTATUTO_P2_EN")))), "faltam"),
       ("o HANDOFF com marcador sem par", None, lambda: (wr(HP, H0 + b"\n<!-- INICIO_SOLTO_v411 -->\n"), wr(REC_P, recibo_do(H0 + b"\n<!-- INICIO_SOLTO_v411 -->\n"))), "marcador com problema"),
       ("o HANDOFF mudado depois do S6d", None, lambda: wr(HP, H0 + b"\numa linha a mais\n"), "nao e' o que o S6d gravou"),
       ("o pino do selo diferente do um.py", None, lambda: wr(NOS / "um_absoluto_selo.json", selo_(sha256={"um.py": "f" * 64})), "nao sao o mesmo"),
       ("o selo de outra versao", None, lambda: wr(NOS / "um_absoluto_selo.json", selo_(um_version="v410")), "nao e' o da v411"),
       ("o selo sem o selftest", None, lambda: wr(NOS / "um_absoluto_selo.json", selo_(fail_closed_selftest="FAIL_CLOSED_SELFTEST_FAILED")), "FAIL_CLOSED_SELFTEST_PASSED"),
       ("a escada nao exata", None, lambda: wr(NOS / "um_absoluto.json", core_escada()), "a escada do core"),
       ("o trailer do rito RITO_RC=1", None, lambda: wr(NOS / "rodada_v411_stdout.txt", "x\nRITO_RC=1\n"), "o trailer do rito"),
       ("a revisao nao aprovada", None, lambda: wr(REV_P, json.dumps(dict(REVJ, aprovada=False))), "a revisao de terceiro nao esta' aprovada"),
       ("o recibo com outro painel", None, lambda: wr(REC_P, recibo_do(H0, textos=dict(tx0, README_PAINEL_H0DN=tx0["README_PAINEL_H0DN"] + " x"))), "nao sao os do recibo"),
       ("o recibo com a conferencia da custodia suja", None, lambda: wr(REC_P, recibo_do(H0, guardas=dict(g0, README_STATUS_5SIGMA=dict(g0["README_STATUS_5SIGMA"], custodia_h0dn=["sintetico"])))), "limpos nas guardas"),
       ("o recibo ausente", None, lambda: REC_P.unlink(), "o recibo dos textos da custodia"),
       ("os horarios ausentes", None, lambda: os.replace(PK / "rito_horarios_v411.txt", PK / "rito_horarios_v411.txt.fora"), "os horarios do rito")]
for nome, me, mf, quer in NEG:
    restaura(); e = copy.deepcopy(E0)
    if me:
        me(e)
    if mf:
        mf()
    r = roda(e); p9 = e["passos"].get("S9_gatilho_custodia", {}); mot = " | ".join(str(x) for x in (p9.get("motivo") or [p9.get("erro") or ""]))
    c = bool(r is False and not DEST.exists() and p9.get("gatilho_escrito") is False and quer in mot); ok &= c
    RES["casos"]["negativo: " + nome] = {"ok": c, "motivo": mot[:300], "esperava": quer}
    if not c:
        print("NEGATIVO FALHOU:", nome, "|", mot[:300])
restaura()
# (D174) um gatilho cujo texto traga --ordem tem de ser RECUSADO: so' neste caso o render e' trocado, e volta
_rend = O._gatilho_render; O._gatilho_render = lambda d_: _rend(d_) + "\nexecutar com --ordem x\n"
e = copy.deepcopy(E0); r = roda(e); p9 = e["passos"].get("S9_gatilho_custodia", {}); O._gatilho_render = _rend
c = bool(r is False and not DEST.exists() and "--ordem" in " | ".join(str(x) for x in (p9.get("motivo") or []))); ok &= c; RES["casos"]["negativo: gatilho com --ordem e' recusado (D174)"] = {"ok": c, "motivo": str(p9.get("motivo"))[:300]}
restaura()
wr(DEST, "um gatilho que ja' estava la'\n"); e = copy.deepcopy(E0); r = roda(e); p9 = e["passos"].get("S9_gatilho_custodia", {})
c = bool(r is False and DEST.read_bytes() == b"um gatilho que ja' estava la'\n" and "ja' existe" in " | ".join(str(x) for x in (p9.get("motivo") or []))); ok &= c; RES["casos"]["negativo: gatilho ja' existente nao e' sobrescrito"] = {"ok": c}
DEST.unlink()
seg = bool(GATILHO_REAL.exists() == HAVIA and (not HAVIA or sha(GATILHO_REAL.read_bytes()) == HAVIA_SHA)); ok &= seg; RES["seguranca_gatilho_real_intocado"] = seg
RES.update(tudo_passou=bool(ok), n_casos=len(RES["casos"]), n_negativos=sum(1 for k in RES["casos"] if k.startswith("negativo")), sandbox=str(SB))
wr(SB / "TESTE_GATILHO_CUSTODIA_v411.json", json.dumps(RES, ensure_ascii=False, indent=1))
print("RESULTADO:", "PASSOU" if ok else "REPROVOU", "| casos:", RES["n_casos"], "| negativos:", RES["n_negativos"], "| saida:", SB / "TESTE_GATILHO_CUSTODIA_v411.json")
sys.exit(0 if ok else 1)
