# -*- coding: utf-8 -*-
# [v410, 10/11/2026, claude-construtor-v410, a servico da gerencia c1; ADITIVOS 1 e 2 a ordem do conserto unico: a custodia da v410 e' AUTOMATICA]
"""teste_gatilho_custodia_sem_candidato_v410.py -- o teste POSSIVEL SEM CANDIDATO e SEM RITO do passo FINAL do orquestrador, S9_gatilho_custodia (orquestrador\\pos_treino_v410.py), em SANDBOX:
monta, numa pasta temporaria, um Nos sintetico (um.py, selo, core, stdout do rito e o HANDOFF com o paragrafo «O que e'», os sete textos e os dois blocos do README, montados pela MESMA parte do gerador do handoff
que compoe os textos), um pacote sintetico (ESPERADOS, horarios do rito, o recibo dos textos, a revisao de terceiro) e um ESTADO com todos os passos feitos; e roda a funcao REAL do orquestrador com os caminhos do sandbox.
 POSITIVO: o gatilho e' escrito (no sandbox), inteiro, com os valores lidos; rodar de novo nao reescreve; e, como no S6d, o HANDOFF INTEIRO (com o cabecalho do gerador, os sete textos, a secao README e os dois blocos) passa no portao do G1, na D59 e na D65.
 NEGATIVOS (o gatilho NAO e' escrito e o motivo fica registrado): um passo anterior falso; um passo anterior ausente; o portao do G1 nao limpo no S6d; o HANDOFF sem um bloco do README; o HANDOFF com marcador sem par;
 o HANDOFF mudado depois do S6d; o pino do selo diferente do um.py; o selo de outra versao; a escada nao exata; o trailer do rito diferente de RITO_RC=0; a revisao de terceiro nao aprovada; o recibo com o bloco do README diferente;
 o recibo sem as guardas limpas; e um gatilho que ja' exista (nao e' sobrescrito).
SEGURANCA: o gatilho de verdade (work\\cadeia_de_selo\\v410\\ORDEM_HANDOFF_CUSTODIA_v410.md) NUNCA e' escrito por este teste: o destino e' sempre dentro da pasta temporaria (conferido), o ESTADO e o log do orquestrador
sao os do sandbox, e o teste confere no fim que o gatilho de verdade nao apareceu. Com --nos-emulado <pasta> e --esperados <arquivo> (os harness) o selo, o um.py, o core e o stdout vem do Nos EMULADO do harness (copias) e o ESPERADOS e' o do harness (so' leitura); o HANDOFF de base e' o que o fechar gravou
no Nos emulado ou, com --handoff-base <arquivo>, o texto do handoff que o harness rendeu; os textos da custodia e os dois blocos do README sao acrescentados aqui, pela MESMA funcao do gerador (montar_blocos).
uso: python -B -X utf8 teste_gatilho_custodia_sem_candidato_v410.py <pasta_temporaria> [--nos-emulado <pasta> --esperados <arquivo> [--handoff-base <arquivo>]]      rc 0 = passou; rc 1 = reprovou."""
import copy, hashlib, importlib.util, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(PKG))), "tools")); sys.path.insert(0, PKG)
from custodia_g1 import textos as TX  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
import delta_v410 as DL  # noqa: E402
if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
    print(__doc__); sys.exit(2)
TMP = os.path.abspath(sys.argv[1]); os.makedirs(TMP, exist_ok=True)
arg = lambda n_: (os.path.abspath(sys.argv[sys.argv.index(n_) + 1]) if n_ in sys.argv else None)
NOS_EMU, ESP_EMU, HBASE = arg("--nos-emulado"), arg("--esperados"), arg("--handoff-base"); EMULADO = bool(NOS_EMU and ESP_EMU); assert EMULADO or not (NOS_EMU or ESP_EMU or HBASE), "o modo emulado pede --nos-emulado E --esperados"
GATILHO_REAL = os.path.join(PKG, "ORDEM_HANDOFF_CUSTODIA_v410.md"); assert os.path.normcase(TMP) != os.path.normcase(PKG) and not os.path.normcase(GATILHO_REAL).startswith(os.path.normcase(TMP) + os.sep), "a pasta temporaria nao pode ser a do pacote"
HAVIA_GATILHO_REAL = os.path.exists(GATILHO_REAL); GATILHO_REAL_SHA = hashlib.sha256(open(GATILHO_REAL, "rb").read()).hexdigest() if HAVIA_GATILHO_REAL else None
SB = os.path.join(TMP, "gatilho_custodia_sandbox"); shutil.rmtree(SB, ignore_errors=True)
NOS = os.path.join(SB, "nos"); PK = os.path.join(SB, "pk"); CENV = os.path.join(SB, "cen_vazio"); DEST = os.path.join(SB, "ORDEM_HANDOFF_CUSTODIA_v410.md")
for d_ in (NOS, os.path.join(PK, "pos_rito"), os.path.join(PK, "revisao_terceiro"), CENV):
    os.makedirs(d_)
sha = lambda b_: hashlib.sha256(b_).hexdigest()
rd = lambda p_: open(p_, "rb").read()


def wr(p_, b_):
    if isinstance(b_, str):
        b_ = b_.encode("utf-8")
    open(p_ + ".tmp", "wb").write(b_); os.replace(p_ + ".tmp", p_)


# ---------------------------------------------------------------- os textos: a MESMA parte do gerador do handoff que os compoe (como teste_textos_custodia_sem_candidato_v410.py), com numeros SINTETICOS
src = open(os.path.join(HERE, "textos_custodia_handoff_v410.py"), encoding="utf-8").read().replace("\r\n", "\n")
i0 = src.index("REV_EN = "); i1 = src.index("# ------------------------------------------------------------------ 3. as guardas")
FJ = json.load(open(os.path.join(PKG, "kernel", "FLAGS_v410.json"), encoding="utf-8"))
NF_I = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.IALD2"); NF_A = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.AEscala")
ESP_REAL = json.load(open(os.path.join(PKG, "ESPERADOS_v410.json"), encoding="utf-8"))
# ---------------------------------------------------------------- o Nos e o pacote do sandbox
if EMULADO:   # o Nos EMULADO do harness: o um.py, o selo, o core e o stdout sao os dele (copias); o HANDOFF e' o que o fechar gravou la' (se houver), com os textos da custodia acrescentados aqui
    for n_ in ("um.py", "um_absoluto_selo.json", "um_absoluto.json"):
        shutil.copyfile(os.path.join(NOS_EMU, n_), os.path.join(NOS, n_))
    ESP = json.load(open(ESP_EMU, encoding="utf-8"))
    PIN = sha(rd(os.path.join(NOS, "um.py")))[:16]
    wr(os.path.join(NOS, "rodada_v410_stdout.txt"), rd(os.path.join(NOS_EMU, "rodada_v410_stdout.txt")) if os.path.exists(os.path.join(NOS_EMU, "rodada_v410_stdout.txt")) else "EMULADO pelo teste do gatilho\nRITO_RC=0\n")
    wr(os.path.join(PK, "ESPERADOS_v410.json"), json.dumps(ESP, ensure_ascii=False))
    ESC = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]["external_ladder"]["n_theorems_expected"]
else:
    UM = b"# um.py SINTETICO do teste do gatilho da custodia (nao e' o candidato)\n"; PIN = sha(UM)[:16]; wr(os.path.join(NOS, "um.py"), UM)
    GATE = ESP_REAL["qg_closure_gate_verdict_v409"]; ESC = int(ESP_REAL["escada"][1])
    ESP = {"candidato_sha16": PIN, "escada": [ESC, ESC], "qg_closure_gate_verdict_v409": GATE}
    wr(os.path.join(NOS, "um_absoluto_selo.json"), json.dumps({"um_version": "v410", "timestamp": "2026-11-11 00:00:00", "fail_closed_selftest": "FAIL_CLOSED_SELFTEST_PASSED", "qg_closure_verdict": GATE, "sha256": {"um.py": sha(UM)}}))
    wr(os.path.join(NOS, "um_absoluto.json"), json.dumps({"core": {"external_ladder": {"n_theorems_clean": ESC, "n_theorems_expected": ESC}, "qg_closure": {"gate": {"verdict": GATE}}}}))
    wr(os.path.join(NOS, "rodada_v410_stdout.txt"), "SINTETICO do teste do gatilho\nFAIL_CLOSED_SELFTEST_PASSED\nRITO_RC=0\n")
    wr(os.path.join(PK, "ESPERADOS_v410.json"), json.dumps(ESP))
N = {"modulos": DL.N_BUNDLE, "modulos_ok": DL.N_BUNDLE, "bandeiras": NF_I + NF_A, "bandeiras_iald2": NF_I, "bandeiras_aescala": NF_A, "ancoras": len(DL.ANCORAS), "ancoras_aescala": len(DL.ANCORAS_AESCALA), "nomes_aescala": len(DL.NOMES_AESCALA), "nomes_novos": len(DL.NOMES_NOVOS_AESCALA), "campos_novos": len(DL.CAMPOS_NOVOS_AESCALA),
     "ea_checks": DL.N_CHECKS_AESCALA, "hm_checks": DL.N_CHECKS_HMS13, "fontes": DL.HMS13_CAMPOS["fontes_primarias"], "calibradores": DL.HMS13_CAMPOS["calibradores"], "checks": DL.N_CHECKS_FECHO, "const": 12345, "teor": 6789, "falas": DL.N_FALAS_V410, "escada_a": 12187, "escada_b": int(ESC),
     "pin": PIN, "respostas": len(DL.RESPOSTAS_DO_OPERADOR), "inst_n": DL.INSTANCIA_SIM["n"], "inst_atr": 2 ** DL.INSTANCIA_SIM["n"], "inst_sol": 1, "nao_sol": 0, "per": "06 a 10/11/2026", "n_trecho": len(DL.VERBATIM_SO_O_TRECHO), "h0dn_checks": DL.N_CHECKS_H0DN, "h0dn_pinos": DL.N_PINOS_FREEZE_R2 + 2, "h0dn_ramos": 6, "h0dn_p1": "00,0 %", "h0dn_p2": "00,0 %"}   # (valores SINTETICOS: nenhum numero daqui vai a texto publicado)
G = {"REV": {"aprovada": True, "candidato_sha16": PIN}, "N": N, "DL": DL, "GF": GF, "TX": TX, "re": re}
exec(compile(src[i0:i1], "textos_custodia_handoff_v410.py[textos]", "exec"), G)
TEXTOS, BLOCOS = G["TEXTOS"], G["BLOCOS_README"]; RF, RS = dict(BLOCOS)["README_FRENTE"], dict(BLOCOS)["README_O_QUE_SAI"]
GUARDAS, FALHAS = G["guardas_dos_textos"](TEXTOS + [("README_EVIDENTE", G["README_EVIDENTE"])] + BLOCOS, {PIN})
assert not FALHAS, ("os textos sinteticos nao passam nas guardas (ver teste_textos_custodia_sem_candidato_v410.py)", FALHAS[:2])
if EMULADO and (HBASE or os.path.exists(os.path.join(NOS_EMU, "HANDOFF_v410_CUSTODIA.md"))):
    BASE_H = rd(HBASE or os.path.join(NOS_EMU, "HANDOFF_v410_CUSTODIA.md")).decode("utf-8").replace("\r\n", "\n").rstrip("\n"); ORIGEM_H = ("o texto do handoff que o harness rendeu (--handoff-base)" if HBASE else "o HANDOFF que o fechar gravou no Nos emulado do harness")
    assert "INICIO_README_FRENTE_v410" not in BASE_H and "INICIO_TITULO_EN_v410" not in BASE_H, "o HANDOFF de base ja' traz os textos da custodia"
else:
    BASE_H = ("# HANDOFF v410 — CUSTÓDIA (SINTÉTICO do teste do gatilho)\n\n**O que é:** `um.py` **v410** `%s` (%s B) sobre a v409 `%s`; %d/%d; COMPLETA; rc 0; selftest PASSED; gate intocado; conferidor sintético. Selo `2026-11-11 00:00:00`."
              % (PIN, format(os.path.getsize(os.path.join(NOS, "um.py")), ","), "0" * 16, ESC, ESC)); ORIGEM_H = "sintetico"
# o CABECALHO dos textos da custodia e' o do proprio gerador (a mesma expressao, lida do fonte): o acrescimo fica como o do S6d (o handoff sem a quebra final + o cabecalho + os blocos)
i2 = src.index("cab = (", i1); i3 = src.index("blocos = montar_blocos(", i2); Gc = {}; exec(compile(src[i2:i3], "textos_custodia_handoff_v410.py[cab]", "exec"), Gc); CAB = Gc["cab"]; assert CAB.startswith("\n\n**Textos da custódia") and CAB.endswith("\n")
HANDOFF = BASE_H + CAB + G["montar_blocos"](TEXTOS, G["README_EVIDENTE"], BLOCOS, "v410")
HP = os.path.join(NOS, "HANDOFF_v410_CUSTODIA.md"); wr(HP, HANDOFF)
REC_P = os.path.join(PK, "pos_rito", "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json")
REC = {"handoff": HP, "sha16_depois": sha(rd(HP))[:16], "textos": dict(TEXTOS), "readme_evidente": G["README_EVIDENTE"], "readme_frente": RF, "readme_frente_bytes_utf8": len(RF.encode("utf-8")), "readme_o_que_sai": RS, "guardas": GUARDAS, "_sintetico": "teste do gatilho"}
wr(REC_P, json.dumps(REC, ensure_ascii=False, indent=1))
REV_P = os.path.join(PK, "revisao_terceiro", "REVISAO_TERCEIRO_v410.json"); REVJ = {"aprovada": True, "candidato_sha16": PIN, "revisor": "sintetico (teste do gatilho)", "achados": [{"sev": "BAIXO", "onde": "sintetico"}]}
wr(REV_P, json.dumps(REVJ, ensure_ascii=False))
wr(os.path.join(PK, "rito_horarios_v410.txt"), "00:00:00\n01:30:00\n")
# ---------------------------------------------------------------- o orquestrador REAL, com o ESTADO, o log e o gatilho padrao desviados para o sandbox
spec = importlib.util.spec_from_file_location("pos_treino_v410_teste_do_gatilho", os.path.join(PKG, "orquestrador", "pos_treino_v410.py")); O = importlib.util.module_from_spec(spec); spec.loader.exec_module(O)
from pathlib import Path  # noqa: E402
assert str(O.GATILHO) == GATILHO_REAL, "o caminho do gatilho no orquestrador nao e' o esperado"
O.ESTADO = Path(SB) / "ESTADO.json"; O.LOG = Path(SB) / "orquestrador.log"; O.GATILHO = Path(SB) / "NAO_USAR_o_gatilho_padrao_foi_desviado.md"; O.NOS = Path(NOS)
ESTADO0 = {"passos": {k_: {"ok": True, "quando": "2026-11-11T00:00:00"} for k_ in O.PASSOS_ANTES_DO_GATILHO}, "inicio": "2026-11-11T00:00:00", "pid": 0}
ESTADO0["passos"]["S4_rito"]["trailer"] = "RITO_RC=0"; ESTADO0["passos"]["S6b_aplicar"].update(evento="1500", hash="0123456789abcdef"); ESTADO0["passos"]["S6d_textos_custodia"].update(portao_g1_handoff_inteiro="limpo", recibo=os.path.basename(REC_P))
ok = True; RES = {"modo": "emulado" if EMULADO else "sintetico", "handoff_de_base": ORIGEM_H, "casos": {}}


def roda(e_, destino=DEST):
    assert os.path.normcase(os.path.abspath(destino)).startswith(os.path.normcase(SB) + os.sep), "o destino do gatilho tem de estar DENTRO do sandbox"
    return O.s9_gatilho_custodia(e_, nos=NOS, pk=PK, destino=destino, cen_g1=CENV)


# ---------------------------------------------------------------- o que o S6d faz antes do gatilho: o HANDOFF INTEIRO (a base, o cabecalho, os sete textos, a secao README e os dois blocos) no portao do G1, na D59 e na D65 (os hashes conhecidos sao os do proprio texto)
_hex = lambda n_, s_: set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{%d}(?![0-9a-fA-F])" % n_, s_))
v6 = [str(x_) for x_ in TX.portao(HANDOFF, _hex(16, HANDOFF) | _hex(64, HANDOFF), rotulo="HANDOFF_v410_CUSTODIA.md")]
if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", HANDOFF) or (re.search(r"(?i)kimi", HANDOFF) and not re.search(r"(?i)h0dn", HANDOFF)):
    v6.append("D59: o handoff traz o que fica fora dos textos")
if any(x_.lower() in HANDOFF.lower() for x_ in DL.FORA_D65):
    v6.append("D65: o handoff traz o que fica fora dos textos")
vcab = [str(list(x_)) for x_ in GF.violacoes(CAB)] + [str(x_) for x_ in TX.portao(CAB, _hex(16, HANDOFF) | _hex(64, HANDOFF), rotulo="cabecalho")]
s6d_ok = not v6 and not vcab
print("COMO NO S6d: o HANDOFF INTEIRO (%s; %d B; com o cabecalho do gerador, os sete textos, a secao README e os dois blocos do README) passa no portao do G1, na D59 e na D65, e o cabecalho passa nas guardas: %s%s" % (ORIGEM_H, len(HANDOFF.encode("utf-8")), s6d_ok, "" if s6d_ok else " " + str((v6 + vcab)[:3])[:600]))
ok = ok and s6d_ok; RES["casos"]["positivo: o HANDOFF inteiro no portao do G1, na D59 e na D65, como no S6d"] = {"ok": s6d_ok, "violacoes": (v6 + vcab)[:5], "handoff_bytes": len(HANDOFF.encode("utf-8"))}
# ---------------------------------------------------------------- POSITIVO
e = copy.deepcopy(ESTADO0); r = roda(e); txt = rd(DEST).decode("utf-8") if os.path.exists(DEST) else ""
pub = os.path.join(os.path.dirname(os.path.dirname(PKG)), "cunhagens_13out", "OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt")
p9 = e["passos"].get("S9_gatilho_custodia", {})
pos = bool(r is True and txt and p9.get("ok") is True and p9.get("gatilho_escrito") is True and p9.get("sha16") == sha(txt.encode("utf-8"))[:16] and txt.startswith("# ORDEM DE HANDOFF DA GERÊNCIA c1 À SESSÃO DE CUSTÓDIA — v410 SELADA (")
           and all(s_ in txt for s_ in ("## A ordem do operador", "## O estado, lido em ", "## O que entrou (para a custódia saber o que publica)", "## O que é da custódia, na ordem", "## Notas"))
           and PIN in txt and ("escada **%d/%d**" % (ESC, ESC)) in txt and "`FAIL_CLOSED_SELFTEST_PASSED`" in txt and "`RITO_RC=0`" in txt and sha(rd(HP))[:16] in txt and sha(rd(REC_P))[:16] in txt and sha(rd(REV_P))[:16] in txt
           and sha(rd(pub))[:16] in txt and ('--publicar --ordem "%s"' % pub) in txt and ("«%s»" % O.TRECHO_PUBLICACAO) in txt and O.TRECHO_PUBLICACAO in rd(pub).decode("utf-8") and DL.FRASE_ORDEM_V410 in txt
           and ("`README_FRENTE_v410`, %d bytes em UTF-8" % len(RF.encode("utf-8"))) in txt and "`README_O_QUE_SAI_v410`" in txt and dict(TEXTOS)["ARCO_PT"] in txt and "custodiar.py planejar --versao v410 --seco" in txt and "custodiar.py auditar --versao v410" in txt
           and "O teste H0DN × BG1 NÃO foi aberto" in txt and ("%d nomes da pedra `AEscala` seguem [DECLARADO pela autoria]" % len(DL.NOMES_DECLARADOS_PELA_AUTORIA_AESCALA)) in txt and "“accreditation”" in txt and "NOT_FALSIFIED nunca é CONFIRMED" in txt
           and not GF.violacoes(txt) and not TX.portao(txt, set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", txt)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", txt)), rotulo="gatilho") and not os.path.exists(DEST + ".tmp"))
print("POSITIVO: tudo feito, o HANDOFF com os sete marcadores e os dois blocos do README, o portao limpo no S6d -> o gatilho e' escrito, inteiro, com os valores lidos, e passa na guarda das frases e no portao do G1: %s (%d B)" % (pos, len(txt.encode("utf-8"))))
ok = ok and pos; RES["casos"]["positivo"] = {"ok": pos, "bytes": len(txt.encode("utf-8")), "sha16": sha(txt.encode("utf-8"))[:16], "motivo_se_falhou": p9.get("motivo") or p9.get("erro")}
if pos:
    wr(os.path.join(SB, "GATILHO_RENDIDO_NO_SANDBOX.md"), txt)   # (copia para leitura; o nome nao e' o do gatilho)
    m0 = os.path.getmtime(DEST); r2 = roda(e); idem = bool(r2 is True and rd(DEST).decode("utf-8") == txt and os.path.getmtime(DEST) == m0)
    print("POSITIVO, de novo: o passo ja' feito nao reescreve o gatilho: %s" % idem); ok = ok and idem; RES["casos"]["positivo_de_novo"] = {"ok": idem}
# ---------------------------------------------------------------- NEGATIVOS: o gatilho NAO e' escrito e o motivo fica registrado
H0, R0, V0 = rd(HP), rd(REC_P), rd(REV_P); S0 = rd(os.path.join(NOS, "um_absoluto_selo.json")); C0 = rd(os.path.join(NOS, "um_absoluto.json")); T0 = rd(os.path.join(NOS, "rodada_v410_stdout.txt"))


def restaura():
    wr(HP, H0); wr(REC_P, R0); wr(REV_P, V0); wr(os.path.join(NOS, "um_absoluto_selo.json"), S0); wr(os.path.join(NOS, "um_absoluto.json"), C0); wr(os.path.join(NOS, "rodada_v410_stdout.txt"), T0)
    if os.path.exists(DEST):
        os.remove(DEST)


def recibo_do(hb_, **muda):
    j_ = json.loads(R0.decode("utf-8")); j_["sha16_depois"] = sha(hb_)[:16]; j_.update(muda); return json.dumps(j_, ensure_ascii=False, indent=1)


def _sem_bloco(i_):
    t_ = H0.decode("utf-8"); a_ = t_.index("\n<!-- INICIO_%s_v410 -->" % i_); b_ = t_.index("<!-- FIM_%s_v410 -->\n" % i_) + len("<!-- FIM_%s_v410 -->\n" % i_); return (t_[:a_] + t_[b_:]).encode("utf-8")


def _selo(**muda):
    j_ = json.loads(S0.decode("utf-8")); j_.update(muda); return json.dumps(j_, ensure_ascii=False, default=str)


def _core_escada():
    j_ = json.loads(C0.decode("utf-8")); j_["core"]["external_ladder"]["n_theorems_clean"] = int(ESC) - 1; return json.dumps(j_, ensure_ascii=False, default=str)


def n_passo_falso(e_):
    e_["passos"]["S5_cadeia_0_10"]["ok"] = False


def n_passo_ausente(e_):
    del e_["passos"]["S8_nativa"]


def n_portao_sujo(e_):
    e_["passos"]["S6d_textos_custodia"]["portao_g1_handoff_inteiro"] = {"HANDOFF_v410_CUSTODIA.md": ["violacao sintetica"]}


NEG = [("um passo anterior FALSO (S5_cadeia_0_10)", n_passo_falso, None, "passo anterior nao feito ou falso"),
       ("um passo anterior AUSENTE (S8_nativa)", n_passo_ausente, None, "passo anterior nao feito ou falso"),
       ("o portao do G1 nao limpo no S6d", n_portao_sujo, None, "o portao do G1 nao rodou limpo no S6d"),
       ("o HANDOFF sem o bloco README_FRENTE", None, lambda: (wr(HP, _sem_bloco("README_FRENTE")), wr(REC_P, recibo_do(_sem_bloco("README_FRENTE")))), "os dois blocos do README"),
       ("o HANDOFF sem o bloco README_O_QUE_SAI", None, lambda: (wr(HP, _sem_bloco("README_O_QUE_SAI")), wr(REC_P, recibo_do(_sem_bloco("README_O_QUE_SAI")))), "os dois blocos do README"),
       ("o HANDOFF sem um dos sete textos (COMMIT)", None, lambda: (wr(HP, _sem_bloco("COMMIT")), wr(REC_P, recibo_do(_sem_bloco("COMMIT")))), "os sete marcadores"),
       ("o HANDOFF com marcador sem par", None, lambda: (wr(HP, H0 + b"\n<!-- INICIO_SOLTO_v410 -->\n"), wr(REC_P, recibo_do(H0 + b"\n<!-- INICIO_SOLTO_v410 -->\n"))), "marcador com problema"),
       ("o HANDOFF mudado depois do S6d", None, lambda: wr(HP, H0 + b"\numa linha a mais, depois do portao\n"), "nao e' o que o S6d gravou"),
       ("o pino do selo diferente do um.py", None, lambda: wr(os.path.join(NOS, "um_absoluto_selo.json"), _selo(sha256={"um.py": "f" * 64})), "nao sao o mesmo"),
       ("o selo de outra versao", None, lambda: wr(os.path.join(NOS, "um_absoluto_selo.json"), _selo(um_version="v409")), "nao e' o da v410"),
       ("o selo sem FAIL_CLOSED_SELFTEST_PASSED", None, lambda: wr(os.path.join(NOS, "um_absoluto_selo.json"), _selo(fail_closed_selftest="FAIL_CLOSED_SELFTEST_FAILED")), "FAIL_CLOSED_SELFTEST_PASSED"),
       ("a escada do core nao exata", None, lambda: wr(os.path.join(NOS, "um_absoluto.json"), _core_escada()), "a escada do core"),
       ("o trailer do rito diferente de RITO_RC=0", None, lambda: wr(os.path.join(NOS, "rodada_v410_stdout.txt"), "x\nRITO_RC=1\n"), "o trailer do rito"),
       ("a revisao de terceiro nao aprovada", None, lambda: wr(REV_P, json.dumps(dict(REVJ, aprovada=False))), "a revisao de terceiro nao esta' aprovada"),
       ("a revisao de terceiro de outro candidato", None, lambda: wr(REV_P, json.dumps(dict(REVJ, candidato_sha16="0" * 16))), "a revisao de terceiro nao esta' aprovada"),
       ("o recibo do S6d com outro README_FRENTE", None, lambda: wr(REC_P, recibo_do(H0, readme_frente=RF + " x")), "nao sao os do recibo"),
       ("o recibo do S6d sem as guardas limpas no README_FRENTE", None, lambda: wr(REC_P, recibo_do(H0, guardas=dict(GUARDAS, README_FRENTE=dict(GUARDAS["README_FRENTE"], portao_g1=["violacao sintetica"])))), "limpos nas guardas"),
       ("o recibo do S6d ausente", None, lambda: os.remove(REC_P), "o recibo dos textos da custodia"),
       ("os horarios do rito ausentes", None, lambda: os.rename(os.path.join(PK, "rito_horarios_v410.txt"), os.path.join(PK, "rito_horarios_v410.txt.fora")), "os horarios do rito")]
for nome, mut_e, mut_f, espera in NEG:
    restaura()
    if os.path.exists(os.path.join(PK, "rito_horarios_v410.txt.fora")):
        os.rename(os.path.join(PK, "rito_horarios_v410.txt.fora"), os.path.join(PK, "rito_horarios_v410.txt"))
    e = copy.deepcopy(ESTADO0)
    if mut_e:
        mut_e(e)
    if mut_f:
        mut_f()
    r = roda(e); p9 = e["passos"].get("S9_gatilho_custodia", {}); mot = " | ".join(str(x_) for x_ in (p9.get("motivo") or [p9.get("erro") or ""]))
    c_ = bool(r is False and not os.path.exists(DEST) and not os.path.exists(DEST + ".tmp") and p9.get("ok") is False and p9.get("gatilho_escrito") is False and espera in mot)
    print("NEGATIVO %-58s o gatilho NAO foi escrito e o motivo ficou registrado: %s" % (nome + ":", c_)); ok = ok and c_
    RES["casos"]["negativo: " + nome] = {"ok": c_, "motivo_registrado": mot[:300], "esperava": espera}
restaura()
if os.path.exists(os.path.join(PK, "rito_horarios_v410.txt.fora")):
    os.rename(os.path.join(PK, "rito_horarios_v410.txt.fora"), os.path.join(PK, "rito_horarios_v410.txt"))
# um gatilho que ja' exista NAO e' sobrescrito
wr(DEST, "um gatilho que ja' estava la'\n"); e = copy.deepcopy(ESTADO0); r = roda(e); p9 = e["passos"].get("S9_gatilho_custodia", {})
c_ = bool(r is False and rd(DEST) == b"um gatilho que ja' estava la'\n" and p9.get("ok") is False and "ja' existe" in " | ".join(str(x_) for x_ in (p9.get("motivo") or [])))
print("NEGATIVO %-58s nao e' sobrescrito e o passo nao se da' por feito: %s" % ("um gatilho que ja' exista:", c_)); ok = ok and c_; RES["casos"]["negativo: um gatilho que ja' exista"] = {"ok": c_}
os.remove(DEST)
# ---------------------------------------------------------------- SEGURANCA: o gatilho de verdade nao apareceu (nem mudou), e o ESTADO e o log do orquestrador de verdade nao foram tocados por este teste
seg = bool(os.path.exists(GATILHO_REAL) == HAVIA_GATILHO_REAL and (not HAVIA_GATILHO_REAL or sha(rd(GATILHO_REAL)) == GATILHO_REAL_SHA) and os.path.exists(os.path.join(SB, "ESTADO.json")) and os.path.exists(os.path.join(SB, "orquestrador.log")))
print("SEGURANCA: o gatilho de verdade (%s) nao foi escrito nem mudado por este teste; o ESTADO e o log usados foram os do sandbox: %s" % (os.path.basename(GATILHO_REAL), seg)); ok = ok and seg
RES.update(tudo_passou=bool(ok), n_casos=len(RES["casos"]), n_negativos=sum(1 for k_ in RES["casos"] if k_.startswith("negativo")), seguranca=seg, sandbox=SB, readme_frente_bytes_utf8=len(RF.encode("utf-8")))
wr(os.path.join(TMP, "TESTE_GATILHO_CUSTODIA_v410.json"), json.dumps(RES, ensure_ascii=False, indent=1))
print("RESULTADO:", "PASSOU" if ok else "REPROVOU", "| modo:", RES["modo"], "| casos:", RES["n_casos"], "| negativos:", RES["n_negativos"])
sys.exit(0 if ok else 1)
