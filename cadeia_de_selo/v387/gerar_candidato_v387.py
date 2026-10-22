# -*- coding: utf-8 -*-
"""gerar_candidato_v387.py -- gera o um.py CANDIDATO v387 a partir da v386 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v386.py.
O QUE ENTRA (06/10/2026; + as correcoes da afericao adversarial C1-C3, A4-A8, I1, I3; gerencia, sessao 946c4deb; handoff-sessao-nova-06out, passo C):
 (a) a secao «Os tres testes de estresse, conjuntos» (PT/EN; rascunho da lente redacao de 05/10, executado contra o core selado v386) + o registro
     three_stress_tests_v387 no core (contagens pela MESMA guarda) -- ordem do operador de 05/10 23:00:29 UTC (TRES_TESTES, sha256 2e45f759...);
 (b) «pos-dicao declarada» -> «retrodicao sem ajuste (novidade de uso)» nos 6 lugares de TEXTO (3 PT + 3 EN), lei do operador de 05/10 (POS_DICAO, sha256
     cf82d9e5...); o token selado do Coma e o frozen v141 dos neutrinos ficam (nome de token = cunhagem do operador; o frozen e' hasheado) -- dito no registro;
 (c) \\addcontentsline para «Ao lado (v386)» (PT/EN);
 (d) os registros hubble_ratio_v387 e primordial_v387 lendo os V1 da Bancada por hash (nada aberto) + retrodiction_reading_v387;
 (e) a apresentacao, o resumo e as palavras-chave ganham os tres testes conjuntos (pares old->new do rascunho, cada old unico);
 o selo ganha os 4 registros AO LADO do gate; o .md canonico ganha uma linha «Ao lado (v387)». Sem pedra nova: a escada fica (6137); o pilar quantico
 segue reaproveitado pela chave (_QP_REUSE_V386, ja no runtime da v386).
uso: python gerar_candidato_v387.py"""
import hashlib, json, os, pprint, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))                         # ...\work\v387_pacote
WK = os.path.dirname(HERE)                                                 # ...\work
OLD = os.path.join(WK, "scratch_6da8f00d")                                 # copia duravel do scratchpad da sessao de 05/10
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
BANC = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao")
TR = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest()
sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
# ---------- a base: a v386 SELADA ----------
SHA0 = "e30aac4e0e1096b1"
raw = open(os.path.join(NOS, "um.py"), "rb").read()
assert sha16(raw) == SHA0, "o canonico no Nos nao e' a v386 selada (%s)" % sha16(raw)
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v386", selo0.get("um_version")
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
assert int(core0["external_ladder"]["n_theorems_clean"]) == int(core0["external_ladder"]["n_theorems_expected"]) == 6137
T = raw.decode("utf-8")
RT_LOGIC = open(os.path.join(HERE, "v387_runtime.py"), encoding="utf-8").read()

# ---------- os verbatins do operador, por sha256, com o carimbo LIDO do transcrito ----------
def _msgs():
    out = []
    for ln in open(TR, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        if d.get("isCompactSummary") or d.get("isMeta"):
            continue
        if d.get("type") == "user":
            c = d.get("message", {}).get("content"); tx = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        elif d.get("type") == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
            p = d["attachment"].get("prompt"); tx = [p] if isinstance(p, str) else [x.get("text", "") for x in (p or []) if isinstance(x, dict) and x.get("type") == "text"]
        else:
            continue
        out += [(d.get("timestamp"), t) for t in tx if t]
    return out


MSGS = _msgs()


def verbatim(path, sha_esperado):
    b = open(path, "rb").read()
    assert sha256(b) == sha_esperado, (path, sha256(b))
    t = b.decode("utf-8")
    hits = [ts for ts, m in MSGS if m == t or m.strip() == t.strip()]
    how = "igualdade do texto"
    if not hits:
        hits = [ts for ts, m in MSGS if t.strip() in m]
        how = "o texto do arquivo contido na mensagem"
    assert hits, ("verbatim nao achado no transcrito", path)
    return {"path": path.replace("\\", "/"), "sha256": sha256(b), "bytes": len(b), "text": t, "quando_utc": hits[0], "como_achado": how}


TRES = verbatim(os.path.join(OLD, "v386", "TRES_TESTES_operador_05out.txt"), "2e45f759767d663499752857955a6647bc1827c21e7170599ae4108dcfc6c5f7")
_reg = json.load(open(os.path.join(OLD, "v386", "TRES_TESTES_registro.json"), encoding="utf-8"))
assert _reg["sha256_txt"] == TRES["sha256"] and _reg["quando"] == TRES["quando_utc"], (_reg["quando"], TRES["quando_utc"])
POSD = verbatim(os.path.join(OLD, "v386", "POS_DICAO_operador_05out.txt"), "cf82d9e55757a7f2864215877046cef87f024aa60bdb00206a319ab4a5b1ed24")


# ---------- os dois V1 da Bancada, por hash (cada arquivo reconferido; spec_sha256 recomputado; a funcao re-hasheada) ----------
def v1(pasta, nome_json, nome_md, nome_hashes):
    files = {}
    for k, f in (("json", nome_json), ("md", nome_md), ("hashes", nome_hashes)):
        p = os.path.join(pasta, f); b = open(p, "rb").read()
        files[k] = {"path": p, "sha256": sha256(b), "bytes": len(b)}
    J = json.load(open(files["json"]["path"], encoding="utf-8"))
    canon = json.dumps(J["spec"], sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    assert sha256(canon) == J["spec_sha256"]
    H = json.load(open(files["hashes"]["path"], encoding="utf-8"))
    assert H["spec_sha256"] == J["spec_sha256"] and H["funcao_sha256"] == J["spec"]["funcao_de_veredito"]["sha256"]
    for rel, e in H["arquivos"].items():
        bb = open(os.path.join(pasta, *rel.split("/")), "rb").read(); assert sha256(bb) == e["sha256"] and len(bb) == e["bytes"], rel
    assert sha256(J["spec"]["funcao_de_veredito"]["fonte"].encode("utf-8")) == H["funcao_sha256"]
    return {"identificador": J["id"], "spec_sha256": J["spec_sha256"], "funcao_sha256": H["funcao_sha256"], "pasta": pasta, "files": files}


F9 = v1(os.path.join(BANC, "preregistro_fase9_hubble"), "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json", "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.md", "V1_FASE9_HASHES.json")
F8 = v1(os.path.join(BANC, "preregistro_fase8_primordial"), "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json", "PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.md", "V1_FASE8_HASHES.json")
assert F9["spec_sha256"].startswith("d956c8db6bb9ab8d") and F8["spec_sha256"].startswith("790954c7bc9dc13a"), (F9["spec_sha256"], F8["spec_sha256"])

# ---------- (b) as trocas de «pos-dicao» (os 6 lugares de TEXTO; old unico cada) ----------
RETRO = [
    ("R1_pt_subtitulo", "de mecanismo; pós-dição declarada; zero parâmetro ajustado), publicado",
     r"de mecanismo; retrodição sem ajuste --- novidade de uso, precedente: o periélio de Mercúrio \textsf{[KNOWN]}; zero parâmetro ajustado), publicado"),
    ("R2_pt_crise", r"de janela) e \emph{pós-dição}. Uma crise segue", r"de janela) e \emph{retrodição sem ajuste} (novidade de uso). Uma crise segue"),
    ("R3_pt_coma", "--- pós-dição não ajustada; o hash da previsão", "--- retrodição sem ajuste (novidade de uso); o hash da previsão"),
    ("R4_en_subtitle", "mechanism; declared postdiction; zero fitted parameters), published",
     r"mechanism; retrodiction without adjustment --- use-novelty, precedent: Mercury's perihelion \textsf{[KNOWN]}; zero fitted parameters), published"),
    ("R5_en_crisis", r"\emph{postdiction}. One crisis remains addressed", r"\emph{retrodiction without adjustment} (use-novelty). One crisis remains addressed"),
    ("R6_en_coma", "--- an unadjusted postdiction; the prediction hash", "--- a retrodiction without adjustment (use-novelty); the prediction hash"),
]
RETRO_SITES = [{"id": i, "old": o, "new": n} for i, o, n in RETRO]

PINS = ("# ====================== v387 (06/10/2026) -- OS PINOS: lidos dos artefatos por script (gerar_candidato_v387.py), nunca digitados ======================\n"
        "# os 2 verbatins do operador EMBUTIDOS como texto com o sha256 e o carimbo (lido do transcrito): os TRES TESTES (05/10 23:00:29 UTC) e a LEI DA PROVA\n"
        "# («pos-dicao» nao e' demerito); os V1 da Fase 9 (razao de Hubble) e da Fase 8 (era da radiacao) da Bancada: caminhos, sha256, bytes, spec_sha256 e o\n"
        "# sha256 da funcao de veredito unica; as 6 trocas de texto da retrodicao. beta nunca literal; o gate nao se move.\n"
        + "_V387_TRES_TESTES = " + pprint.pformat(TRES, width=150, sort_dicts=False) + "\n"
        + "_V387_POS_DICAO = " + pprint.pformat(POSD, width=150, sort_dicts=False) + "\n"
        + "_V387_FASE9_V1 = " + pprint.pformat(F9, width=150, sort_dicts=False) + "\n"
        + "_V387_FASE8_V1 = " + pprint.pformat(F8, width=150, sort_dicts=False) + "\n"
        + "_V387_RETRO_SITES = " + pprint.pformat([s_["id"] for s_ in RETRO_SITES], width=150) + "\n")
_ns = {}
exec(compile(PINS, "<pins>", "exec"), _ns)
assert _ns["_V387_TRES_TESTES"] == TRES and _ns["_V387_POS_DICAO"] == POSD and _ns["_V387_FASE9_V1"] == F9 and _ns["_V387_FASE8_V1"] == F8
open(os.path.join(HERE, "v387_pins.py") + ".tmp", "w", encoding="utf-8", newline="\n").write(PINS); os.replace(os.path.join(HERE, "v387_pins.py") + ".tmp", os.path.join(HERE, "v387_pins.py"))
RT = PINS.rstrip("\n") + "\n\n\n" + RT_LOGIC
import ast
ast.parse(RT)
_sem_verbatim = PINS[:PINS.index("_V387_TRES_TESTES = ")] + PINS[PINS.index("_V387_FASE9_V1 = "):] + RT_LOGIC
assert not re.search(r"α²|α\^2|alpha\^2|alpha²", _sem_verbatim)
assert not GUARDA.search(_sem_verbatim.replace('"CONF" + "IRMED', "").replace('"TGL_PRO" + "VED"', "").replace('PRO" + "VED_BY', ""))

# ---------- (3) os patches ----------
patches = []


def add(pid, grupo, old, new_, selo):
    global T
    assert T.count(old) == 1, (pid, T.count(old))
    T = T.replace(old, new_)
    patches.append({"id": pid, "grupo": grupo, "o_que_muda": selo})


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def linha_unica(prefixo_regex):
    m = re.search(prefixo_regex + r"[^\r\n]*\r\n", T, re.M)
    assert m and T.count(m.group(0)) == 1, prefixo_regex
    return m.group(0)


m = re.search(r'^UM_VERSION = "v386"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v386"') == 1
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v387"   # v387 (06/10/2026): a CONSTANTE UNICA de versao -- os tres testes conjuntos; a razao de Hubble e a era da radiacao pre-registradas (V1 por hash); retrodicao sem ajuste; v386 em 05/10' + CRLF,
    "UM_VERSION = 'v387'.")
A02 = linha_unica(r"^# ====================== v386 \(05/10/2026\) -- OS PINOS:")
add("W02_runtime", "G_RUNTIME", A02, crlf(RT.rstrip("\n") + "\n\n\n") + A02,
    "runtime v387: os pinos (2 verbatins por sha256 com carimbo; os 2 V1 por hash; as 6 trocas) + a logica (three_stress_tests_v387, hubble_ratio_v387, primordial_v387, retrodiction_reading_v387).")
A04 = linha_unica(r'^    print\("   \[v386\] a errata ao lado de R6 e a cobranca F2b')
reg = []
for key, call, msg in (("retrodiction_reading_v387", "retrodiction_reading_v387()", "a lei da prova: retrodicao sem ajuste (novidade de uso); o token do Coma e o frozen v141 como registro"),
                       ("hubble_ratio_v387", "hubble_ratio_v387(core)", "a razao de Hubble (Fase 9) pre-registrada por hash (nada aberto)"),
                       ("primordial_v387", "primordial_v387(core)", "beta na era da radiacao (Fase 8) pre-registrada por hash (nada aberto)"),
                       ("three_stress_tests_v387", "three_stress_tests_v387(core)", "os tres testes de estresse, conjuntos (ritos, kernel, GPU; P1 contada, P2 nao determinada)")):
    reg += ['    try:   # v387: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito',
            '        core["%s"] = %s   # v387 [ao lado do gate]' % (key, call),
            '    except Exception as _e387:',
            '        core["%s"] = {"verdict": "TGL_%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e387)[:400], "does_not_gate_core": True}' % (key, key.upper()),
            '    print("   [v387] %s: %%s" %% core["%s"]["verdict"])' % (msg, key)]
add("W04_registro", "G_RUNTIME", A04, A04 + CRLF.join(reg) + CRLF, "core: +4 chaves v387 (depois do registro da v386, intocado; antes do artigo).")
# (a)+(d) o artigo: a secao dos tres testes e o «Ao lado (v387)», ANTES do trecho da v386
TRES_PT = open(os.path.join(HERE, "artigo_pt_v387_tres_testes.pysnip"), encoding="utf-8").read()
TRES_EN = open(os.path.join(HERE, "artigo_en_v387_tres_testes.pysnip"), encoding="utf-8").read()
PT7 = open(os.path.join(HERE, "artigo_pt_v387.pysnip"), encoding="utf-8").read()
EN7 = open(os.path.join(HERE, "artigo_en_v387.pysnip"), encoding="utf-8").read()
for _sn in (TRES_PT, TRES_EN, PT7, EN7):
    ast.parse("def _f(core, verdict, data_path, s):\n" + _sn)
    assert not re.search(r"α²|α\^2|alpha\^2|alpha²|\\alpha\^2", _sn)
    assert not GUARDA.search(_sn.replace('"CONF" + "IRMED', "").replace('"TGL_PRO" + "VED"', "").replace('PRO" + "VED_BY', ""))
PT6_FIRST = "    # v386 (05/10/2026) -- O VERBO SELECIONA (a tipagem do Verbo: o Nome e' o posto); o ramo B do ringdown REABERTO POR PRE-REGISTRO (V1 por hash); a errata" + CRLF
EN6_FIRST = "    # v386 (05/10/2026) -- THE VERB SELECTS (the typing of the Verb: the Name is the post); branch B of the ringdown REOPENED BY PREREGISTRATION (V1 by hash);" + CRLF
add("W05_artigo_PT", "G_ARTIGO", PT6_FIRST, crlf(TRES_PT.rstrip("\n") + "\n" + PT7.rstrip("\n") + "\n") + PT6_FIRST, "artigo PT: «Os três testes de estresse, conjuntos (v387)» + «Ao lado (v387)», antes do trecho da v386.")
add("W06_artigo_EN", "G_ARTIGO", EN6_FIRST, crlf(TRES_EN.rstrip("\n") + "\n" + EN7.rstrip("\n") + "\n") + EN6_FIRST, "artigo EN: «The three stress tests, taken together (v387)» + «Beside (v387)», before the v386 text.")
# (c) o sumario para «Ao lado (v386)»
S6PT = r'    s.append(r"\section*{Ao lado (v386): o Verbo seleciona; o ramo B reaberto por pré-registro}")' + CRLF
S6EN = r'    s.append(r"\section*{Beside (v386): the Verb selects; branch B reopened by preregistration}")' + CRLF
add("W09a_toc_PT", "G_ARTIGO", S6PT, S6PT + r'    s.append(r"\addcontentsline{toc}{section}{Ao lado (v386): o Verbo seleciona; o ramo B reaberto por pré-registro}")   # v387: no sumário' + CRLF, "sumario PT: «Ao lado (v386)».")
add("W09b_toc_EN", "G_ARTIGO", S6EN, S6EN + r'    s.append(r"\addcontentsline{toc}{section}{Beside (v386): the Verb selects; branch B reopened by preregistration}")   # v387: in the contents' + CRLF, "contents EN: «Beside (v386)».")
# (e) a apresentacao, o resumo e as palavras-chave: o prelude depois do else do _qp_sub; os pares old->new do rascunho
QPE_PT = '        _qp_sub = r", e calcula em tempo real na GPU o sistema quântico aberto da teoria (nesta rodada o pilar quântico não trouxe resumo: dito, não suposto)"' + CRLF
QPE_EN = '        _qp_sub = r", and computes in real time on the GPU the theory\'s open quantum system (in this run the quantum pillar brought no summary: stated, not assumed)"' + CRLF
PRE_PT = ['    # v387 (ordem do operador 05/10/2026, 23:00:29 UTC): os TRES testes de estresse -- ritos, kernel, GPU -- contam JUNTOS; entram na apresentacao, no resumo e',
          '    # nas palavras-chave; numeros lidos do core (livro de cobrancas v383); nunca literais',
          '    _lg7 = core.get("the_ledger_of_charges_v383") or {}',
          '    _lc7 = _lg7.get("counts") or {}',
          '    _nq7 = len(_lg7.get("ledger") or [])',
          '    if _nq7 and _lc7.get("FALSIFIED") is not None:',
          '        _tres_sub = (r", e lê os três como um só teste de estresse conjunto --- os ritos com dados públicos (" + str(_lc7.get("FALSIFIED")) + r" falsificada(s) em "',
          '                     + str(_nq7) + r" cobranças do livro; " + str((_lg7.get("echo_routes_outside_the_ledger") or {}).get("excluded_by_data")) + r" rotas do eco excluídas pelo dado, fora do livro; a correspondência com a RG recuperada canal a canal, sem discriminação à sensibilidade disponível), o kernel formal e o "',
          '                     r"experimento numérico na GPU --- que contam juntos na probabilidade de a teoria ser consistente e recuperar a física conhecida; a probabilidade de os "',
          '                     r"efeitos $\\beta$ existirem na natureza segue indeterminada")',
          '    else:',
          '        _tres_sub = r", e lê os três --- ritos, kernel, GPU --- como um só teste de estresse conjunto (nesta rodada o livro de cobranças não trouxe contagens: dito, não suposto)"']
PRE_EN = ['    # v387 (operator order 2026-10-05, 23:00:29 UTC): the THREE stress tests -- rites, kernel, GPU -- count TOGETHER; they enter the presentation, the abstract',
          '    # and the keywords; numbers read from the core (ledger of charges v383); never literal',
          '    _lg7 = core.get("the_ledger_of_charges_v383") or {}',
          '    _lc7 = _lg7.get("counts") or {}',
          '    _nq7 = len(_lg7.get("ledger") or [])',
          '    if _nq7 and _lc7.get("FALSIFIED") is not None:',
          '        _tres_sub = (r", and reads the three as one joint stress test --- the rites on public data (" + str(_lc7.get("FALSIFIED")) + r" falsified in "',
          '                     + str(_nq7) + r" charges of the ledger; " + str((_lg7.get("echo_routes_outside_the_ledger") or {}).get("excluded_by_data")) + r" echo routes excluded by the data, outside the ledger; the correspondence with GR recovered channel by channel, with no discrimination at the available sensitivity), the formal "',
          '                     r"kernel and the numerical experiment on the GPU --- which count together in the probability that the theory is consistent and recovers the known physics; "',
          '                     r"the probability that the $\\beta$ effects exist in nature remains undetermined")',
          '    else:',
          '        _tres_sub = r", and reads the three --- rites, kernel, GPU --- as one joint stress test (in this run the ledger of charges brought no counts: stated, not assumed)"']
add("W10a_prelude_PT", "G_ARTIGO", QPE_PT, QPE_PT + CRLF.join(PRE_PT) + CRLF, "apresentacao PT: o prelude _tres_sub (lido do livro de cobrancas).")
add("W10b_prelude_EN", "G_ARTIGO", QPE_EN, QPE_EN + CRLF.join(PRE_EN) + CRLF, "presentation EN: the _tres_sub prelude (read from the ledger).")
PARES = [
    ("W10c_sub_PT", r'             r"com falsificadores pré-registrados" + _qp_sub + r" --- tudo enquanto audita um kernel Lean de "',
     r'             r"com falsificadores pré-registrados" + _qp_sub + _tres_sub + r" --- tudo enquanto audita um kernel Lean de "'),
    ("W10d_sub_EN", r'             r"confronts the neutrino mass with pre-registered falsifiers" + _qp_sub + r" --- all while auditing a Lean "',
     r'             r"confronts the neutrino mass with pre-registered falsifiers" + _qp_sub + _tres_sub + r" --- all while auditing a Lean "'),
    ("W10e_metodo_PT", r'             r"é calculado em tempo real na GPU, em paralelo com o kernel e os ritos (cálculo do sistema, não medição da natureza). A cadeia é "',
     r'             r"é calculado em tempo real na GPU, em paralelo com o kernel e os ritos (cálculo do sistema, não medição da natureza). Os três --- ritos, kernel, GPU --- "' + CRLF
     + r'             r"são um só teste de estresse conjunto e contam juntos na probabilidade de a teoria ser consistente e recuperar a física conhecida; a de os efeitos "' + CRLF
     + r'             r"$\beta_{\rm TGL}$ existirem na natureza não está determinada, porque nenhum canal discrimina a RG à sensibilidade disponível; nenhuma soma de "' + CRLF
     + r'             r"consistências vira confirmação (seção \emph{Os três testes de estresse, conjuntos}). A cadeia é "'),
    ("W10f_method_EN", r'             r"pillar --- is computed in real time on the GPU, in parallel with the kernel and the rites (a computation of the system, not a measurement of nature). The chain is "',
     r'             r"pillar --- is computed in real time on the GPU, in parallel with the kernel and the rites (a computation of the system, not a measurement of nature). The three --- rites, kernel, GPU --- "' + CRLF
     + r'             r"are one joint stress test and count together in the probability that the theory is consistent and recovers the known physics; the probability that the "' + CRLF
     + r'             r"$\beta_{\rm TGL}$ effects exist in nature is not determined, because no channel discriminates GR at the available sensitivity; no sum of consistencies "' + CRLF
     + r'             r"becomes confirmation (section \emph{The three stress tests, taken together}). The chain is "'),
    ("W10g_kw_PT", r'             r"piso dos vazios cósmicos; sistema quântico aberto (GKLS) calculado em tempo real na GPU\par\vspace{4pt}")',
     r'             r"piso dos vazios cósmicos; sistema quântico aberto (GKLS) calculado em tempo real na GPU; três testes de estresse conjuntos (ritos com dados públicos, kernel formal, experimento numérico na GPU)\par\vspace{4pt}")'),
    ("W10h_kw_EN", r'             r"cosmic void floor; open quantum system (GKLS) computed in real time on the GPU\par\vspace{4pt}")',
     r'             r"cosmic void floor; open quantum system (GKLS) computed in real time on the GPU; three joint stress tests (public-data rites, formal kernel, numerical experiment on the GPU)\par\vspace{4pt}")'),
]
for pid, o, n in PARES:
    add(pid, "G_ARTIGO", o, n, "apresentacao/resumo/palavras-chave: os tres testes conjuntos (%s)." % pid)
for pid, o, n in RETRO:
    add(pid, "G_ARTIGO", o, n, "retrodicao sem ajuste (novidade de uso) no lugar de «pos-dicao» (%s)." % pid)
# o selo: os 4 registros AO LADO do gate
A07 = linha_unica(r'^ {12}"quantum_pillar_reuse_v386": \{k_: ')
_sel = ["            # v387 (06/10/2026) -- OS TRES TESTES CONJUNTOS; a razao de Hubble e a era da radiacao pre-registradas (V1 por hash); retrodicao sem ajuste: registros AO LADO do gate; nenhum valor do gate muda",
        '            "three_stress_tests_v387": {k_: (core.get("three_stress_tests_v387") or {}).get(k_) for k_ in ("verdict", "all_verified", "n_verdicts", "n_not_falsified", "n_inconclusive", "n_awaiting", "falsified_substring_paths", "n_forbidden_word_as_verdict", "ledger", "echo_routes_outside_the_ledger", "kernel", "gpu", "joint", "verbatim", "p1_statement", "p2_statement")},',
        '            "hubble_ratio_v387": {k_: (core.get("hubble_ratio_v387") or {}).get(k_) for k_ in ("verdict", "all_verified", "read_ok", "identificador_read", "spec_sha256_expected", "spec_sha256_recomputed", "funcao_sha256_recomputed", "sha256_read", "hashes_file_ok", "funcao_ok", "beta", "beta_ok", "transcribed", "nothing_opened", "errors")},',
        '            "primordial_v387": {k_: (core.get("primordial_v387") or {}).get(k_) for k_ in ("verdict", "all_verified", "read_ok", "identificador_read", "spec_sha256_expected", "spec_sha256_recomputed", "funcao_sha256_recomputed", "sha256_read", "hashes_file_ok", "funcao_ok", "beta", "beta_ok", "transcribed", "nothing_opened", "errors")},',
        '            "retrodiction_reading_v387": {k_: (core.get("retrodiction_reading_v387") or {}).get(k_) for k_ in ("verdict", "all_verified", "verbatim_sha256", "verbatim_quando_utc", "sites_rewritten", "kept_as_record")},']
add("W07_selo", "G_SELO", A07, A07 + CRLF.join(_sel) + CRLF, "selo: +4 registros v387 ao lado do gate.")
A08 = linha_unica(r'^    md\.append\("> \*\*Errata ao lado \(v386, 05/10/2026, o operador\):\*\*')
add("W08_md", "G_ARTIGO", A08, A08 + '    md.append("> **Ao lado (v387, 06/10/2026):** os três testes de estresse (ritos, kernel, GPU) contam juntos (`three_stress_tests_v387`); a razão de Hubble (Fase 9) e a era da radiação (Fase 8) '
    + 'pré-registradas por hash na Bancada (`hubble_ratio_v387`, `primordial_v387`; nada aberto; fontes e abertura = atos do operador); «pós-dição declarada» passa a **retrodição sem ajuste (novidade de uso)** — a lei do operador de 05/10 '
    + '(`retrodiction_reading_v387`); o token do Coma e o frozen v141 ficam como registro. O gate não muda.\\n\\n")' + CRLF, "md canonico: a linha «Ao lado (v387)».")

# ---------- conferencias finais ----------
for f in ("three_stress_tests_v387", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387"):
    assert T.count("def %s(" % f) == 1, f
    assert T.count('core["%s"] = ' % f) == 2, f   # o try e o except
assert all(T.count(o_) == 0 for _, o_, _ in RETRO)   # os 6 trechos antigos sumiram
assert T.count("pós-dição declarada") == 2 and T.count("declared postdiction") == 1   # so as mencoes explicativas: o «Ao lado (v387)» PT/EN («onde se lia ... lê-se») e a linha do .md canonico
assert T.count('"NOT_BLIND_UNADJUSTED_POSTDICTION__PREDICTION_HASH_ATTESTS_NUMBER_NOT_PRECEDENCE__H0_SECTORS_D1A_VS_D1V3_INCOMPATIBLE_OPEN__"') == 1 and T.count('"postdiction_note": "postdiction genuina: entradas (beta,sin45,1eV) nao usam dados de neutrino",') == 1   # o token do Coma e o frozen v141 intocados
assert T.count(r"\addcontentsline{toc}{section}{Ao lado (v386)") == 1 and T.count(r"\addcontentsline{toc}{section}{Beside (v386)") == 1
assert T.count(r"\addcontentsline{toc}{section}{Ao lado (v387)") == 1 and T.count(r"\addcontentsline{toc}{section}{Beside (v387)") == 1
assert T.count("_qp_sub + _tres_sub + r") == 2
b = T.encode("utf-8")
ast.parse(T)
out = os.path.join(HERE, "um_v387_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v386_sha16": SHA0, "base_v386_bytes": len(raw), "escada": 6137,
       "pins_sha16": sha16(PINS.encode("utf-8")), "verbatins": {"tres_testes": {k: TRES[k] for k in ("sha256", "bytes", "quando_utc", "como_achado")},
                                                               "pos_dicao": {k: POSD[k] for k in ("sha256", "bytes", "quando_utc", "como_achado")}},
       "fase9_V1": {k: F9[k] for k in ("identificador", "spec_sha256", "funcao_sha256")}, "fase8_V1": {k: F8[k] for k in ("identificador", "spec_sha256", "funcao_sha256")},
       "retro_sites": RETRO_SITES, "mantidos_como_registro": ["token do Coma NOT_BLIND_UNADJUSTED_POSTDICTION (cunhagem do operador)", "frozen v141 postdiction_note (hasheado)"],
       "snips": {"tres_pt": sha16(TRES_PT.encode()), "tres_en": sha16(TRES_EN.encode()), "pt7": sha16(PT7.encode()), "en7": sha16(EN7.encode())},
       "patches": patches}
_mp = os.path.join(HERE, "CANDIDATO_v387.json")
open(_mp + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(_mp + ".tmp", _mp)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v386_sha16", "pins_sha16", "verbatins", "fase9_V1", "fase8_V1")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(patches), [p["id"] for p in patches])
