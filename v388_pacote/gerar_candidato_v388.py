# -*- coding: utf-8 -*-
"""gerar_candidato_v388.py -- gera o um.py CANDIDATO v388 a partir da v387 SELADA no Nos (NUNCA escreve o canonico). Moldes: gerar_candidato_v386.py (kernel, bandeiras,
escada) e gerar_candidato_v387.py (pinos, registros, artigo). Ordem do operador de 06/10/2026 via a sessao c1 («vamos em frente, haja v388 e abra a fase 9»):
 (a) registro beta_runs_bounded_below_v388 (a cunhagem por sha256; beta0 em runtime; beta(M_Z) on-shell do Teorema da Escala e MS-bar ao lado; a errata forma x numero);
 (b) a pedra TGLExt/TheCouplingRunsBoundedBelow.lean (17 nomes; compilada e auditada no sandbox work\\v388_kernel\\kernel_src -- copia de bytes do tgl_kernel do Nos,
     porque o sandbox antigo perdeu os pacotes da Mathlib; dito) + TGLExt.lean (+1 import) + TGL/Audit.lean (+17 #print axioms), fiada na escada;
 (c) registro hubble_ratio_opening_v388 (o RESULTADO da Fase 9 por hash; a funcao congelada reexecutada);
 (d) o artigo PT/EN: «Ao lado (v388)» + addcontentsline, antes da secao dos tres testes da v387; selo e .md canonico.
uso: python gerar_candidato_v388.py"""
import ast, hashlib, json, os, pprint, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.dirname(HERE)
KD = os.path.join(WK, "v388_kernel"); KS = os.path.join(KD, "kernel_src")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
BANC = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao")
MEMF = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "beta-escalar-limitado-inferiormente-06out.md")
TR = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
SHA0 = "64c899f86d8d32e1"
raw = open(os.path.join(NOS, "um.py"), "rb").read()
assert sha16(raw) == SHA0, "o canonico no Nos nao e' a v387 selada (%s)" % sha16(raw)
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == "v387"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E387 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E387 == 6137
T = raw.decode("utf-8")
T0 = T   # o texto ORIGINAL da v387: as linhas citadas contam sobre ele, nao sobre o T depois do patch do kernel (afericao C1)
RT_LOGIC = open(os.path.join(HERE, "v388_runtime.py"), encoding="utf-8").read()

# ---------- (b) o kernel do sandbox: build verde, sem sorry, os 17 nomes no trio ----------
LOG = open(os.path.join(KD, "build_full.log"), encoding="utf-8", errors="replace").read()
assert re.search(r"(?m)^rc=0$", LOG) and re.search(r"(?m)^rc_build=0$", LOG) and re.search(r"(?m)^rc_audit=0$", LOG), "o build/auditoria do sandbox nao terminou verde"
assert not re.search(r"(?m)^error:|: error:", LOG), "ha linhas de erro no log"
assert "declaration uses 'sorry'" not in LOG
AX = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    AX.setdefault(m.group(1), [])
NOMES = [l.strip() for l in open(os.path.join(KD, "AUDIT_NOMES_v388.txt"), encoding="utf-8") if l.strip()]
assert len(NOMES) == 17
QN = ["TGLExt.TheCouplingRunsBoundedBelow." + n for n in NOMES]
fora = [q for q in QN if q not in AX or not set(AX[q]) <= TRIO]
assert not fora, ("declaracao da pedra fora do trio ou sem linha no relatorio", fora)
DEFS = {"alphaOfChi", "betaOfChi"}   # definicoes: _kernel_checked (o padrao da casa: ext_wio_coupling_of_alpha_kernel_checked) -- afericao C2
FLAGS = [("ext_cpl_%s_kernel_%s" % (n, "checked" if n in DEFS else "proved"), q) for n, q in zip(NOMES, QN)]
for f, _ in FLAGS:
    assert f not in T, f
STONE = "TGLExt/TheCouplingRunsBoundedBelow.lean"
lines = T.splitlines(keepends=True)
i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]; assert len(i0) == 1; i0 = i0[0]; j = i0 + 1
while lines[j].rstrip("\r\n") != "}":
    j += 1
off0 = sum(len(l) for l in lines[:i0]); blk = "".join(lines[i0:j + 1])
dnode = ast.parse(blk).body[0].value; blines = blk.splitlines(keepends=True); bstart = [0]
for l in blines:
    bstart.append(bstart[-1] + len(l))
charpos = lambda ln, cb: bstart[ln - 1] + len(blines[ln - 1].encode("utf-8")[:cb].decode("utf-8"))
old_d = ast.literal_eval(blk.split("=", 1)[1].strip())
spans = {ast.literal_eval(k): (charpos(v.lineno, v.col_offset), charpos(v.end_lineno, v.end_col_offset)) for k, v in zip(dnode.keys, dnode.values)}
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
assert rd(os.path.join(KD, "TGLExt.lean.ANTES_v388")) == old_d["TGLExt.lean"], "o TGLExt.lean embutido na v387 nao e' byte a byte o ANTES do sandbox"
assert rd(os.path.join(KD, "Audit.lean.ANTES_v388")) == old_d["TGL/Audit.lean"], "o TGL/Audit.lean embutido na v387 nao e' byte a byte o ANTES do sandbox"
assert STONE not in old_d
new_root = rd(os.path.join(KS, "TGLExt.lean")); new_audit = rd(os.path.join(KS, "TGL", "Audit.lean")); stone = rd(os.path.join(KS, *STONE.split("/")))
assert new_root.startswith(old_d["TGLExt.lean"].rstrip("\r\n")) and "import TGLExt.TheCouplingRunsBoundedBelow" in new_root and len(new_root) - len(old_d["TGLExt.lean"]) < 60
assert new_audit.startswith(old_d["TGL/Audit.lean"].rstrip("\r\n")) and all(("#print axioms " + q) in new_audit for q in QN)
assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", stone, flags=re.S))
cand = dict(old_d); cand["TGLExt.lean"] = new_root; cand["TGL/Audit.lean"] = new_audit
nb = blk
for k in sorted(("TGLExt.lean", "TGL/Audit.lean"), key=lambda k: -spans[k][0]):
    a, b = spans[k]; nb = nb[:a] + repr(cand[k]) + nb[b:]
fim = nb.rstrip("\r\n"); assert fim.endswith("}")
nb = fim[:-1] + "    %r: %s,%s" % (STONE, repr(stone), CRLF) + "}" + nb[len(fim):]
cand[STONE] = stone
T = T[:off0] + nb + T[off0 + len(blk):]
assert ast.literal_eval(nb.split("=", 1)[1].strip()) == cand
KERNEL = {"changed": {"TGLExt.lean": [sha16(old_d["TGLExt.lean"].encode()), sha16(new_root.encode())], "TGL/Audit.lean": [sha16(old_d["TGL/Audit.lean"].encode()), sha16(new_audit.encode())]},
          "new": {STONE: sha16(stone.encode())}, "build_log_sha16": sha16(LOG.encode("utf-8", "replace")), "n_axiom_report": len(AX), "sandbox": KS}

# ---------- (a) os verbatins do operador (transcrito; a memoria por sha256) ----------
MSGS = []
for ln in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(ln)
    except ValueError:
        continue
    if d.get("isCompactSummary") or d.get("isMeta") or d.get("type") != "user":
        continue
    c = d.get("message", {}).get("content"); tx = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    MSGS += [(d.get("timestamp"), t) for t in tx if t]
memb = open(MEMF, "rb").read(); memt = memb.decode("utf-8")
VERB = {}
for k, chave in (("beta_escalar_1327", "nós derivamos completamente a constante da estrutura fina"), ("dicotomia_1348", "como que chama aquela razão matemática")):
    hits = [(ts, t.strip()) for ts, t in MSGS if t.strip().startswith(chave)]
    assert hits, ("verbatim nao achado no transcrito", k)
    ts, t = hits[0]
    assert t in memt, ("o verbatim do transcrito nao esta na memoria (copia)", k)
    VERB[k] = {"text": t, "sha256": sha256(t.encode("utf-8")), "bytes": len(t.encode("utf-8")), "quando_utc": ts}
BETA_ESCALA = {"memoria": {"path": MEMF.replace("\\", "/"), "sha256": sha256(memb), "bytes": len(memb)}, "verbatins": VERB}
# o 1/alpha(M_Z) on-shell do Teorema da Escala, LIDO do texto selado (PT) por regex; o MS-bar [KNOWN] ao lado
m = re.search(r"\$1/\\alpha\(M_Z\)=(\d+)\{,\}(\d+)\$ contra \$(\d+)\{,\}(\d+)\$ da literatura", T0)
assert m, "o 1/alpha(M_Z) do Teorema da Escala nao foi achado no texto"
ln_mz = T0[:m.start()].count("\n") + 1
ALPHA_MZ = {"on_shell_inv": float("%s.%s" % (m.group(1), m.group(2))), "on_shell_fonte": "um.py v387, linha %d (Teorema da Escala, PT: recomputado a um laco com dependencia de massa exata), lido por regex pelo gerador; o rotulo on-shell nao esta na fonte" % ln_mz,
            "literatura_on_shell_inv": float("%s.%s" % (m.group(3), m.group(4))), "msbar_inv": 127.95,
            "msbar_estatuto": "[KNOWN — literatura (PDG, alpha-hat MS-bar em M_Z), NAO conferido em disco; o numero usado pela memoria do adendo]"}
ERRATA = ("onde o artigo diz «α observa-se, não se deriva», lê-se, AO LADO: o que se deriva é a FORMA (α como índice de escala da fronteira; β como a sua conjugação), "
          "não o NÚMERO, que continua lido do CODATA; o texto antigo fica como registro (v388, 06/10/2026, em nome da gerência)")
# ---------- (c) a Fase 9 aberta: os arquivos por hash ----------
F9A = os.path.join(BANC, "fase9_hubble_abertura"); F9V = os.path.join(BANC, "preregistro_fase9_hubble")
res = sorted(f for f in os.listdir(F9A) if f.startswith("RESULTADO_FASE9_V1_") and f.endswith(".json")); assert len(res) == 1, res
files = {}
for k, p in (("resultado_json", os.path.join(F9A, res[0])), ("resultado_md", os.path.join(F9A, res[0][:-5] + ".md")), ("poder", os.path.join(F9A, "PODER_FASE9_ANTES_DE_ABRIR.json")),
             ("runner", os.path.join(F9A, "rodar_fase9_v1.py")), ("runner_antes", os.path.join(F9A, "RUNNER_ANTES_DE_ABRIR.json")), ("v1_json", os.path.join(F9V, "PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json"))):
    b = open(p, "rb").read(); files[k] = {"path": p, "sha256": sha256(b), "bytes": len(b)}
RJ = json.load(open(files["resultado_json"]["path"], encoding="utf-8"))
assert RJ["runner_sha256"] == files["runner"]["sha256"] == json.load(open(files["runner_antes"]["path"], encoding="utf-8"))["runner_sha256"]
RECP = os.path.join(F9A, "RECALCULO_AO_LADO_v388.json"); _rb = open(RECP, "rb").read(); _rj = json.loads(_rb.decode("utf-8"))
RECALC = {"path": RECP, "sha256": sha256(_rb), "bytes": len(_rb), "convergido_n200": _rj["convergido_n200"], "erro_n25_n35": _rj["erro_n25_n35"]}
FASE9 = {"files": files, "v1_spec_sha256": RJ["V1"]["spec_sha256"], "funcao_sha256": RJ["V1"]["funcao_sha256"], "runner_sha256": RJ["runner_sha256"], "veredito_lido": RJ["veredito"]}

PINS = ("# ====================== v388 (06/10/2026) -- OS PINOS: lidos dos artefatos por script (gerar_candidato_v388.py), nunca digitados ======================\n"
        "# as 17 bandeiras da pedra TGLExt/TheCouplingRunsBoundedBelow.lean (auditadas no sandbox); os 2 verbatins do operador (transcrito, por sha256, com o carimbo) e a\n"
        "# memoria por sha256; o 1/alpha(M_Z) on-shell lido do Teorema da Escala selado e o MS-bar [KNOWN] ao lado; a errata forma x numero; os arquivos da Fase 9 aberta\n"
        "# por hash. beta nunca literal; o gate nao se move.\n"
        "_CPL_FLAGS_V388 = [\n" + "".join("    %r,\n" % f for f, _ in FLAGS) + "]\n"
        + "_V388_BETA_ESCALA = " + pprint.pformat(BETA_ESCALA, width=150, sort_dicts=False) + "\n"
        + "_V388_ALPHA_MZ = " + pprint.pformat(ALPHA_MZ, width=150, sort_dicts=False) + "\n"
        + "_V388_ERRATA_FORMA_NUMERO = %r\n" % ERRATA
        + "_V388_FASE9_RES = " + pprint.pformat(FASE9, width=150, sort_dicts=False) + "\n"
        + "_V388_FASE9_RECALCULO = " + pprint.pformat(RECALC, width=150, sort_dicts=False) + "\n")
_ns = {}; exec(compile(PINS, "<pins>", "exec"), _ns)
assert _ns["_V388_BETA_ESCALA"] == BETA_ESCALA and _ns["_V388_FASE9_RES"] == FASE9 and _ns["_CPL_FLAGS_V388"] == [f for f, _ in FLAGS]
open(os.path.join(HERE, "v388_pins.py") + ".tmp", "w", encoding="utf-8", newline="\n").write(PINS); os.replace(os.path.join(HERE, "v388_pins.py") + ".tmp", os.path.join(HERE, "v388_pins.py"))
RT = PINS.rstrip("\n") + "\n\n\n" + RT_LOGIC
ast.parse(RT)
_logica = PINS[:PINS.index("_V388_BETA_ESCALA = ")] + PINS[PINS.index("_V388_ALPHA_MZ = "):] + RT_LOGIC
assert not re.search(r"α²|α\^2|alpha\^2|alpha²", _logica)
assert not GUARDA.search(_logica.replace('"CONF" + "IRMED', "").replace('"TGL_PRO" + "VED"', "").replace('PRO" + "VED_BY', ""))

# ---------- os patches ----------
patches = []


def add(pid, grupo, old, new_, o_que):
    global T
    assert T.count(old) == 1, (pid, T.count(old))
    T = T.replace(old, new_); patches.append({"id": pid, "grupo": grupo, "o_que_muda": o_que})


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def linha_unica(rx):
    m_ = re.search(rx + r"[^\r\n]*\r\n", T, re.M); assert m_ and T.count(m_.group(0)) == 1, rx; return m_.group(0)


A01 = '    "ext_dks_the_iald_selector_separates_the_sectors_kernel_proved": "TGLExt.the_iald_selector_separates_the_sectors",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v388 (06/10/2026; o acoplamento corre com a escala, limitado inferiormente): cpl (%d)" % len(FLAGS) + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +%d (ext_cpl_)." % len(FLAGS))
A02 = '        "ext_dks_the_iald_selector_separates_the_sectors_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v388: o acoplamento corre com a escala (%d)" % len(FLAGS) + CRLF + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +%d." % len(FLAGS))
A03 = '    ("v386", "TheVerbSelectsTheAction", "TGLExt/TheVerbSelectsTheAction.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v388 (06/10/2026): o acoplamento corre com a escala, limitado inferiormente (alpha = sech(chi/2); o piso no infravermelho; a dicotomia; a Meia-Nat ponto fixo)" + CRLF
    + '    ("v388", "TheCouplingRunsBoundedBelow", "TGLExt/TheCouplingRunsBoundedBelow.lean", None, None),' + CRLF, "ledger de pedras: +1.")
patches.append({"id": "V04_kernel", "grupo": "G_PEDRAS", "o_que_muda": "kernel embutido: +1 pedra; TGLExt.lean (+1 import) e TGL/Audit.lean (+17 #print axioms), conferidos byte a byte contra os ANTES."})
m = re.search(r'^UM_VERSION = "v387"[^\r\n]*' + CRLF, T, re.M); assert m
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v388"   # v388 (06/10/2026): a CONSTANTE UNICA de versao -- beta corre com a escala, limitado inferiormente (a pedra); a Fase 9 aberta pela funcao congelada; v387 em 06/10' + CRLF, "UM_VERSION = 'v388'.")
A_P = linha_unica(r"^# ====================== v387 \(06/10/2026\) -- OS PINOS:")
add("W02_runtime", "G_RUNTIME", A_P, crlf(RT.rstrip("\n") + "\n\n\n") + A_P, "runtime v388: os pinos + beta_runs_bounded_below_v388 + hubble_ratio_opening_v388.")
A_R = linha_unica(r'^    print\("   \[v387\] os tres testes de estresse, conjuntos')
reg = []
for key, call, msg in (("beta_runs_bounded_below_v388", "beta_runs_bounded_below_v388(core)", "beta corre com a escala, limitado inferiormente (a pedra; o piso no infravermelho)"),
                       ("hubble_ratio_opening_v388", "hubble_ratio_opening_v388(core)", "a Fase 9 aberta pela funcao congelada (o resultado por hash; a funcao reexecutada)")):
    reg += ['    try:   # v388: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito',
            '        core["%s"] = %s   # v388 [ao lado do gate]' % (key, call),
            '    except Exception as _e388:',
            '        core["%s"] = {"verdict": "TGL_%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e388)[:400], "does_not_gate_core": True}' % (key, key.upper()),
            '    print("   [v388] %s: %%s" %% core["%s"]["verdict"])' % (msg, key)]
add("W04_registro", "G_RUNTIME", A_R, A_R + CRLF.join(reg) + CRLF, "core: +2 chaves v388.")
PT8 = open(os.path.join(HERE, "artigo_pt_v388.pysnip"), encoding="utf-8").read(); EN8 = open(os.path.join(HERE, "artigo_en_v388.pysnip"), encoding="utf-8").read()
for sn in (PT8, EN8):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn)
    assert not re.search(r"α²|α\^2|alpha\^2|alpha²|\\alpha\^2", sn) and not GUARDA.search(sn)
P7 = os.path.join(WK, "v387_pacote")
PT7_FIRST = open(os.path.join(P7, "artigo_pt_v387_tres_testes.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN7_FIRST = open(os.path.join(P7, "artigo_en_v387_tres_testes.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
add("W05_artigo_PT", "G_ARTIGO", PT7_FIRST, crlf(PT8.rstrip("\n") + "\n") + PT7_FIRST, "artigo PT: «Ao lado (v388)», antes dos tres testes da v387.")
add("W06_artigo_EN", "G_ARTIGO", EN7_FIRST, crlf(EN8.rstrip("\n") + "\n") + EN7_FIRST, "artigo EN: «Beside (v388)», before the v387 three tests.")
A_S = linha_unica(r'^ {12}"retrodiction_reading_v387": \{k_: ')
_sel = ["            # v388 (06/10/2026) -- beta corre com a escala, limitado inferiormente; a Fase 9 aberta: registros AO LADO do gate; nenhum valor do gate muda",
        '            "beta_runs_bounded_below_v388": {k_: (core.get("beta_runs_bounded_below_v388") or {}).get(k_) for k_ in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "missing_flags", "verbatim", "verbatim_ok", "memory_file", "beta0", "beta0_ok", "alpha_MZ", "beta_MZ_on_shell", "beta_MZ_msbar", "erratum_beside")},',
        '            "hubble_ratio_opening_v388": {k_: (core.get("hubble_ratio_opening_v388") or {}).get(k_) for k_ in ("verdict", "all_verified", "files_ok", "spec_ok", "funcao_ok", "same_verdict", "verdict_of_the_frozen_function", "counterfactual_with_sources_NOT_a_verdict", "numbers", "files", "runner_sha256")},']
add("W07_selo", "G_SELO", A_S, A_S + CRLF.join(_sel) + CRLF, "selo: +2 registros v388.")
A_M = linha_unica(r'^    md\.append\("> \*\*Ao lado \(v387, 06/10/2026\):\*\*')
add("W08_md", "G_ARTIGO", A_M, A_M + '    md.append("> **Ao lado (v388, 06/10/2026):** β corre com a escala, limitado inferiormente — a pedra `TheCouplingRunsBoundedBelow` (17 nomes; o piso no infravermelho; a dicotomia; a Meia-Nat ponto fixo; `beta_runs_bounded_below_v388`); '
    + 'a constante da fronteira segue β₀ (o Teorema da Escala), β(μ) é a leitura de bulk; errata ao lado: deriva-se a forma, não o número. A Fase 9 ABERTA pela função congelada (`hubble_ratio_opening_v388`; o veredito reexecutado). O gate não muda.\\n\\n")' + CRLF, "md canonico: a linha «Ao lado (v388)».")
for f in ("beta_runs_bounded_below_v388", "hubble_ratio_opening_v388"):
    assert T.count("def %s(" % f) == 1 and T.count('core["%s"] = ' % f) == 2, f
for f, _ in FLAGS:
    assert T.count('"%s"' % f) == 2 and T.count("'%s'" % f) == 1, f
b = T.encode("utf-8"); ast.parse(T)
out = os.path.join(HERE, "um_v388_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v387_sha16": SHA0, "escada": [E387, E387 + len(FLAGS)], "kernel": KERNEL,
       "flags": [f for f, _ in FLAGS], "nomes": QN, "pins_sha16": sha16(PINS.encode("utf-8")), "verbatins": {k: {x: v[x] for x in ("sha256", "bytes", "quando_utc")} for k, v in VERB.items()},
       "memoria_sha256": BETA_ESCALA["memoria"]["sha256"], "alpha_MZ": ALPHA_MZ, "fase9": {k: v["sha256"] for k, v in files.items()}, "patches": patches,
       "snips": {"pt8": sha16(PT8.encode()), "en8": sha16(EN8.encode())}}
open(os.path.join(HERE, "CANDIDATO_v388.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(os.path.join(HERE, "CANDIDATO_v388.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v388.json"))
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v387_sha16", "escada", "kernel", "verbatins", "alpha_MZ")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(patches), [p["id"] for p in patches])
