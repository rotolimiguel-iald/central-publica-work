# -*- coding: utf-8 -*-
"""gerar_candidato_v385.py -- gera o um.py CANDIDATO v385 a partir da v384 SELADA no Nos (NUNCA escreve o canonico). Moldes: gerar_candidato_v383.py
(o kernel embutido, as bandeiras, a escada, o livro das pedras) e gerar_candidato_v384.py (o runtime, o artigo, o selo).
AS CUNHAGENS E ORDENS DO OPERADOR (05/10/2026; verbatim no Atlas e na memoria): o Um e' POSTO (inscrito pelo observador: echo 1 | python um.py), nao
postulado -- etiqueta [POSTO]; o degrau final do gate chama-se AXIOMA (ao lado do gate, que NAO muda); o Axioma e' o modo zero de peso 1, o escuro; a
testemunha falsa e' a testemunha estatica, o zero absoluto; nao ha observador nao conjugado; «sim para tudo»: a pedra do fluxo, o embutir (auditar) do
TheDarkSplit, o pilar rodado INTEIRO sob o mesmo V1 (a reprodutibilidade); «agora sim, concordo com tudo, prossiga».
(1) KERNEL EMBUTIDO: o da v384 + TGLExt/TheAxiomAndTheFalseWitness.lean (nova) + TGLExt.lean e TGL/Audit.lean (mudam); kernel_src = ../v376/kernel_src,
    compilado e auditado ali (v385/kernel/build_full.log: build rc 0, auditoria rc 0, 10129 declaracoes, todas no trio, zero sorry, 29/29 bandeiras -- lidos de kernel/sandbox_raiz_v385.json).
(2) PATCHES (count(old) == 1): bandeiras ext_axm_ (22) + ext_dks_ (7) e escada (+29, lida do core da v384); livro das pedras (+1); UM_VERSION v385; runtime v385;
    a leitura do resultado anterior do pilar logo depois do lancamento; o registro (a reprodutibilidade e o Axioma) depois do pilar; o artigo PT/EN
    («Ao lado (v385)», antes do trecho da v384); o selo (uma leitura, o nome do degrau final lido do kernel, os dois registros); a errata ao lado no md
    canonico («posto», nao «postulado irredutivel»); a etiqueta [POSTO] na lista de estatutos permitidos.
uso: python gerar_candidato_v385.py"""
import ast, hashlib, json, os, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
KS = os.path.join(SP, "v376", "kernel_src")
V4 = os.path.join(SP, "v384")
CRLF = "\r\n"
AP4 = sorted(f for f in os.listdir(V4) if f.startswith("APLICADO_AO_CANONICO_") and f.endswith(".json"))
assert AP4, "o registro da instalacao da v384 nao foi achado"
AP4 = json.load(open(os.path.join(V4, AP4[-1]), encoding="utf-8"))
SHA0 = AP4["um_py_novo"]["sha16"]
raw = open(os.path.join(NOS, "um.py"), "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico no Nos nao e' a v384 selada (%s)" % SHA0
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v384", selo0.get("um_version")
T = raw.decode("utf-8")
RT = open(os.path.join(HERE, "v385_runtime.py"), encoding="utf-8").read()
RT4_FIRST = open(os.path.join(V4, "v384_runtime.py"), encoding="utf-8").read().splitlines()[0]
PT4_FIRST = open(os.path.join(V4, "artigo_pt_v384.pysnip"), encoding="utf-8").read().splitlines()[0]
EN4_FIRST = open(os.path.join(V4, "artigo_en_v384.pysnip"), encoding="utf-8").read().splitlines()[0]
KREP = json.load(open(os.path.join(HERE, "kernel", "sandbox_raiz_v385.json"), encoding="utf-8"))
assert KREP["sorry_warnings"] == 0 and KREP["fora_do_trio"] == {} and KREP["bandeiras_ok"] == len(KREP["bandeiras"]) == 29 and all(KREP["bandeiras"].values()), "o kernel do sandbox nao fechou"
assert open(os.path.join(HERE, "kernel", "build_full.log"), encoding="utf-8", errors="replace").read().count("rc_build=0") == 1

# ---------- (1) o kernel embutido (o molde da v383) ----------
lines = T.splitlines(keepends=True)
i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]
assert len(i0) == 1
i0 = i0[0]; j = i0 + 1
while lines[j].rstrip("\r\n") != "}":
    j += 1
off0 = sum(len(l) for l in lines[:i0])
blk = "".join(lines[i0:j + 1])
dnode = ast.parse(blk).body[0].value
blines = blk.splitlines(keepends=True)
bstart = [0]
for l in blines:
    bstart.append(bstart[-1] + len(l))


def charpos(lineno, col_bytes):
    l = blines[lineno - 1]
    return bstart[lineno - 1] + len(l.encode("utf-8")[:col_bytes].decode("utf-8"))


old_d = ast.literal_eval(blk.split("=", 1)[1].strip())
spans = {ast.literal_eval(k): (charpos(v.lineno, v.col_offset), charpos(v.end_lineno, v.end_col_offset)) for k, v in zip(dnode.keys, dnode.values)}
cand = {}
for top in ("TGL", "TGLExt"):
    for root, dirs, files in os.walk(os.path.join(KS, top)):
        for f in files:
            if f.endswith(".lean"):
                p = os.path.join(root, f); rel = os.path.relpath(p, KS).replace("\\", "/")
                cand[rel] = open(p, "r", encoding="utf-8", newline="").read()
for f in ("TGL.lean", "TGLExt.lean", "lakefile.toml", "lake-manifest.json", "lean-toolchain"):
    if os.path.exists(os.path.join(KS, f)):
        cand[f] = open(os.path.join(KS, f), "r", encoding="utf-8", newline="").read()
for k in old_d:
    if k not in cand and not k.endswith(".lean"):
        cand[k] = old_d[k]
assert [k for k in old_d if k not in cand] == []
changed = sorted(k for k in old_d if cand[k] != old_d[k])
new = sorted(k for k in cand if k not in old_d)
assert set(changed) == {"TGLExt.lean", "TGL/Audit.lean"}, changed
assert new == ["TGLExt/TheAxiomAndTheFalseWitness.lean"], new
for k in new:
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", cand[k], flags=re.S)), k
# a mudanca dos dois arquivos e' SO acrescimo (a raiz ganha um import; a auditoria ganha 2 imports no topo e as linhas no fim)
assert cand["TGLExt.lean"].startswith(old_d["TGLExt.lean"].rstrip("\n")) and cand["TGLExt.lean"].rstrip("\n").endswith("import TGLExt.TheAxiomAndTheFalseWitness")
_a0 = old_d["TGL/Audit.lean"]; _a1 = cand["TGL/Audit.lean"]
assert _a1.startswith("import TGLExt.TheAxiomAndTheFalseWitness\nimport TGLExt.TheDarkSplit\n") and _a1[len("import TGLExt.TheAxiomAndTheFalseWitness\nimport TGLExt.TheDarkSplit\n"):].startswith(_a0.rstrip("\n"))
nb = blk
for k in sorted(changed, key=lambda k: -spans[k][0]):
    a, b = spans[k]
    nb = nb[:a] + repr(cand[k]) + nb[b:]
fim = nb.rstrip("\r\n")
assert fim.endswith("}")
nb = fim[:-1] + "".join("    %r: %s,%s" % (k, repr(cand[k]), CRLF) for k in new) + "}" + nb[len(fim):]
T = T[:off0] + nb + T[off0 + len(blk):]
assert ast.literal_eval(nb.split("=", 1)[1].strip()) == cand
KERNEL_MANIFEST = {"changed": {k: [hashlib.sha256(old_d[k].encode()).hexdigest()[:16], hashlib.sha256(cand[k].encode()).hexdigest()[:16]] for k in changed},
                   "new": {k: hashlib.sha256(cand[k].encode()).hexdigest()[:16] for k in new}, "n_entries": len(cand)}

# ---------- (2) os patches ----------
patches = []


def add(pid, grupo, old, new_, selo):
    global T
    assert T.count(old) == 1, (pid, T.count(old))
    T = T.replace(old, new_)
    patches.append({"id": pid, "grupo": grupo, "old": old, "new": new_, "o_que_muda": selo})


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def linha_unica(prefixo_regex):
    m = re.search(prefixo_regex + r"[^\r\n]*\r\n", T, re.M)
    assert m and T.count(m.group(0)) == 1, prefixo_regex
    return m.group(0)


NOMES = json.load(open(os.path.join(HERE, "kernel", "AUDIT_NOMES_v385.json"), encoding="utf-8"))
_rt_ns = {}
exec(compile("\n".join(l for l in RT.splitlines() if l.startswith(("_AXM_FLAGS_V385", "_DKS_FLAGS_V385", "]")) or l.startswith("    \"ext_")), "<flags>", "exec"), _rt_ns)
AXM = list(_rt_ns["_AXM_FLAGS_V385"]); DKS = list(_rt_ns["_DKS_FLAGS_V385"])
FLAGS = list(zip(AXM, NOMES["TheAxiomAndTheFalseWitness"])) + list(zip(DKS, NOMES["TheDarkSplit"]))
assert len(AXM) == len(NOMES["TheAxiomAndTheFalseWitness"]) == 22 and len(DKS) == len(NOMES["TheDarkSplit"]) == 7 and len(FLAGS) == 29 and len({f for f, _ in FLAGS}) == 29
for f, nm in FLAGS:   # a bandeira e' o nome EXATO da declaracao, posicao a posicao
    pfx = "ext_axm_" if f.startswith("ext_axm_") else "ext_dks_"
    assert f.replace(pfx, "").rsplit("_kernel_", 1)[0] == nm.split(".")[-1], (f, nm)
    assert f not in T, f
    assert KREP["bandeiras"].get(f) is True, f
A01 = '    "ext_psv_the_psion_and_the_viscosity_kernel_proved": "TGLExt.ThePsionAndTheViscosity.the_psion_and_the_viscosity",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v385 (05/10/2026; o Axioma e a testemunha falsa -- os dois pontos fixos da leitura -- e a auditoria do TheDarkSplit): axm (%d) + dks (%d)" % (len(AXM), len(DKS)) + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +%d (ext_axm_ %d, ext_dks_ %d)." % (len(FLAGS), len(AXM), len(DKS)))
A02 = '        "ext_psv_the_psion_and_the_viscosity_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v385: o Axioma e a testemunha falsa (%d) + o TheDarkSplit auditado (%d)" % (len(AXM), len(DKS)) + CRLF
    + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +%d." % len(FLAGS))
A03 = '    ("v382", "ThePsionAndTheViscosity", "TGLExt/ThePsionAndTheViscosity.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v385 (05/10/2026): o Axioma e a testemunha falsa -- os dois pontos fixos da leitura; o posto e' o zero modular; o nome do degrau final" + CRLF
    + '    ("v385", "TheAxiomAndTheFalseWitness", "TGLExt/TheAxiomAndTheFalseWitness.lean", None, None),' + CRLF, "ledger de pedras: +1 (TheAxiomAndTheFalseWitness).")
m = re.search(r'^UM_VERSION = "v384"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v384"') == 1
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v385"   # v385 (05/10/2026): a CONSTANTE UNICA de versao -- o Axioma e a testemunha falsa; o Um posto; a reprodutibilidade do pilar; v384 em 03-04/10' + CRLF,
    "UM_VERSION = 'v385'.")
assert T.count(RT4_FIRST) == 1
add("W02_runtime", "G_RUNTIME", RT4_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT4_FIRST,
    "runtime v385: as bandeiras (29), o Axioma (o nome lido do kernel), a leitura do resultado anterior do pilar, a reprodutibilidade.")
A04 = linha_unica(r'^    _QP_ST_V384 = quantum_pillar_start_v384\(\)')
add("W03_anterior", "G_RUNTIME", A04, A04 + "    _QP_PREV_V385 = quantum_pillar_previous_v385(_QP_ST_V384)   # v385: le, logo depois de lancar o trabalhador (antes que o calculo novo possa substitui-lo), o resultado que o cache guardou da rodada anterior (mesma chave), para a reprodutibilidade" + CRLF,
    "main: logo depois do lancamento do pilar, le o resultado anterior do cache (antes de a rodada nova o substituir).")
A05 = linha_unica(r'^    print\("   \[v384\] o pilar quantico \(o sistema aberto')
reg = ['    try:   # v385 (afericao de codigo, nota 10): uma excecao aqui vira registro NAO comparado, dito -- nunca derruba o rito depois do pilar',
       '        core["quantum_pillar_reproducibility_v385"] = quantum_pillar_reproducibility_v385(_QP_PREV_V385, core["quantum_pillar_v384"])   # v385: a reprodutibilidade, campo a campo [COMPUTED]',
       '    except Exception as _e385:',
       '        core["quantum_pillar_reproducibility_v385"] = {"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_RUNTIME_ERROR__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED", "compared": False, "why": repr(_e385)[:400], "status": "[COMPUTED]", "does_not_gate_core": True}',
       '    print("   [v385] a reprodutibilidade do pilar quantico (a rodada desta versao contra a guardada pela anterior, mesma chave): %s" % core["quantum_pillar_reproducibility_v385"]["verdict"])',
       '    try:   # v385 (afericao de codigo, nota 10): uma excecao aqui vira o Axioma NAO selado, dito (all_verified False: vai ao balde dos nao selados)',
       '        core["the_axiom_v385"] = the_axiom_v385(core)   # v385: o Axioma e a testemunha falsa -- as declaracoes da v385 verificadas pelo kernel desta rodada e o nome do degrau final lido do kernel',
       '    except Exception as _e385:',
       '        core["the_axiom_v385"] = {"verdict": "TGL_THE_AXIOM_V385__NOT_SEALED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e385)[:400], "does_not_gate_core": True}',
       '    print("   [v385] o Axioma e a testemunha falsa (os dois pontos fixos da leitura; o posto e o zero modular; o degrau final do gate chama-se Axioma, ao lado do gate): %s" % core["the_axiom_v385"]["verdict"])']
add("W04_registro", "G_RUNTIME", A05, A05 + CRLF.join(reg) + CRLF, "core: +2 chaves v385 (depois do pilar, antes do artigo).")
pt = open(os.path.join(HERE, "artigo_pt_v385.pysnip"), encoding="utf-8").read()
A06 = PT4_FIRST + CRLF
add("W05_artigo_PT", "G_ARTIGO", A06, crlf(pt.rstrip("\n") + "\n") + A06, "artigo PT: «Ao lado (v385): o Axioma e a testemunha falsa», antes do trecho da v384.")
en = open(os.path.join(HERE, "artigo_en_v385.pysnip"), encoding="utf-8").read()
A07 = EN4_FIRST + CRLF
add("W06_artigo_EN", "G_ARTIGO", A07, crlf(en.rstrip("\n") + "\n") + A07, "artigo EN: «Beside (v385): the Axiom and the false witness», before the v384 text.")
A08 = linha_unica(r'^ {12}"quantum_pillar_v384": \{k_: ')
add("W07_selo", "G_SELO", A08, A08 + "            # v385 (05/10/2026) -- o AXIOMA e a TESTEMUNHA FALSA: registro proprio AO LADO do gate; o nome do degrau final lido do kernel; nenhum valor do gate muda" + CRLF
    + '            "the_axiom_reading_v385": "OPERATOR_COINAGES_AND_RATIFIED_READINGS_2026_10_05__THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED_TAG_POSTO__THE_AXIOM_IS_THE_ZERO_MODE_OF_WEIGHT_ONE_THE_DARK__'
    + 'THE_FALSE_WITNESS_IS_THE_STATIC_WITNESS_THE_ABSOLUTE_ZERO__NO_UNCONJUGATED_OBSERVER_CONJUGATION_IS_THE_NATURE_OF_THE_VERB__THE_READING_HAS_TWO_FIXED_POINTS__'
    + 'THE_POST_IS_THE_MODULAR_ZERO__FINAL_STEP_NAMED_AXIOMA_BESIDE_THE_GATE__THE_RUN_FACTS_ARE_IN_THE_COMPUTED_RECORDS_NOT_IN_THIS_STRING__'
    + 'READINGS_ARE_INPUT_ONTO__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF
    + '            "final_step_name_v385": (core.get("the_axiom_v385") or {}).get("final_step_name_from_kernel"),' + CRLF
    + '            "the_axiom_v385": {k_: (core.get("the_axiom_v385") or {}).get(k_) for k_ in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "missing_flags", "final_step_name", "final_step_name_from_kernel", "final_step_name_matches_kernel", "tag_for_omega_I")},' + CRLF
    + '            "quantum_pillar_reproducibility_v385": {k_: (core.get("quantum_pillar_reproducibility_v385") or {}).get(k_) for k_ in ("verdict", "compared", "n_fields", "n_numeric_fields", "n_differ", "max_scaled_diff", "max_rel_diff_finite", "n_nonfinite_differ", "d128_excluded", "inputs", "env", "same_pillar_verdict", "previous", "this_run", "why")},' + CRLF,
    "selo: +1 leitura, +1 nome do degrau final (lido do kernel) e +2 registros, ao lado do gate.")
A09 = r'    md.append("## O fundamento-raiz: 1 = 1  →  1 = HAJA LUZ\n")' + CRLF
add("W08_md_posto", "G_ARTIGO", A09, A09 + '    md.append("> **Errata ao lado (v385, 05/10/2026, o operador):** o Um não é postulado — é **posto**: inscrito pelo observador externo no comando '
    + r'(`echo 1 | python um.py`; o programa trava sem ele). Etiqueta `[POSTO]`. Onde abaixo se lê «o postulado irredutível» ou «o postulado `ω(I)=1`», leia-se *posto*. O degrau final do gate chama-se **Axioma** (ao lado do gate, que não muda).\n\n")' + CRLF,
    "md canonico: a errata ao lado («posto», nao «postulado irredutivel») e o nome do degrau final.")
add("W09_etiqueta_posto", "G_REGUA", '"[LEGAL]", "[DECLARADO]", "[REFUTADO]")', '"[LEGAL]", "[DECLARADO]", "[REFUTADO]", "[POSTO]")',
    "_ESTATUTOS_PERMITIDOS: +[POSTO] (a etiqueta do operador para omega(I) = 1).")
assert "_QP_PREV_V385" in T and T.count("def the_axiom_v385(") == 1
b = T.encode("utf-8")
ast.parse(T)
h16 = hashlib.sha256(b).hexdigest()[:16]
out = os.path.join(HERE, "um_v385_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
# a escada da v384, LIDA do core selado (nao mais o literal), e a ORDEM DO OPERADOR da v385, LIDA do transcrito (afericao de codigo, nota 9)
_C384 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]["external_ladder"]
_E384 = int(_C384["n_theorems_expected"]); assert int(_C384["n_theorems_clean"]) == _E384
_TR = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
_ORD = None
for _ln in open(_TR, encoding="utf-8", errors="replace"):
    try:
        _d = json.loads(_ln)
    except ValueError:
        continue
    if _d.get("type") == "user":
        _c = _d.get("message", {}).get("content")
        for _t in ([_c] if isinstance(_c, str) else [x.get("text", "") for x in (_c or []) if isinstance(x, dict) and x.get("type") == "text"]):
            if (_t or "").strip().startswith("agora sim, concordo com tudo, prossiga"):
                _ORD = {"verbatim": _t.strip(), "quando": _d.get("timestamp"), "transcrito": _TR, "lido_por": "gerar_candidato_v385.py (mensagem achada pelo comeco)"}
assert _ORD, "a ordem do operador da v385 nao foi achada no transcrito"
man = {"candidato": out, "sha16": h16, "bytes": len(b), "base_v384_sha16": SHA0, "kernel": KERNEL_MANIFEST, "escada": [_E384, _E384 + len(FLAGS)],
       "ordem_do_operador": _ORD,
       "patches": [{k: p[k] for k in ("id", "grupo", "o_que_muda")} for p in patches], "flags": [f for f, _ in FLAGS]}
_mp = os.path.join(HERE, "CANDIDATO_v385.json")
open(_mp + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(_mp + ".tmp", _mp)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v384_sha16", "kernel", "escada")}, ensure_ascii=False, indent=1))
print("patches:", [p["id"] for p in patches])
