# -*- coding: utf-8 -*-
"""gerar_candidato_v378.py -- gera o um.py CANDIDATO v378 a partir da v377 SELADA (NUNCA escreve o canonico). Molde: gerar_candidato_v377.py.
Ordens do operador (30/09/2026, noite): «tem alguma coisa que deixamos passar, examine por favor»; «concordo prossiga».
(1) KERNEL EMBUTIDO: TGLExt.lean e TGL/Audit.lean mudam; entra TGLExt/TheFlowLawContrast.lean (kernel_src = ../v376/kernel_src, o sandbox da linhagem).
(2) PATCHES (count(old) == 1): bandeiras ext_dlc_ (20) e escada; ledger de pedras; UM_VERSION v378; runtime (3 modulos); registro; artigo PT/EN
    (paragrafos «Ao lado (v378)»); selo (uma leitura, string); chave AO LADO no modulo de Coma v39 (flow_layer_kernel_v378; as antigas ficam); homonimos."""
import ast, hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
KS = os.path.join(os.path.dirname(HERE), "v376", "kernel_src")
CRLF = "\r\n"
V7 = os.path.join(os.path.dirname(HERE), "v377")
AP = json.load(open(sorted(os.path.join(V7, f) for f in os.listdir(V7) if f.startswith("APLICADO_AO_CANONICO_"))[-1], encoding="utf-8"))
SHA0 = AP["um_py_novo"]["sha16"]
raw = open(UM, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico nao e a v377 selada"
T = raw.decode("utf-8")
RT = open(os.path.join(HERE, "v378_runtime.py"), encoding="utf-8").read()
RT7_FIRST = open(os.path.join(V7, "v377_runtime.py"), encoding="utf-8").read().splitlines()[0]
PT7_FIRST = open(os.path.join(V7, "artigo_pt_v377.pysnip"), encoding="utf-8").read().splitlines()[0]
EN7_FIRST = open(os.path.join(V7, "artigo_en_v377.pysnip"), encoding="utf-8").read().splitlines()[0]

# ---------- (1) o kernel embutido ----------
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
assert new == ["TGLExt/TheFlowLawContrast.lean"], new
for k in new:
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", cand[k], flags=re.S)), k
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


NOMES = json.load(open(os.path.join(HERE, "AUDIT_NOMES_v378.json"), encoding="utf-8"))
DLC = ["ext_dlc_accumulatedContrast_kernel_checked", "ext_dlc_meanContrast_kernel_checked", "ext_dlc_survivingWeightContrast_kernel_checked",
       "ext_dlc_H0localContrast_kernel_checked", "ext_dlc_frwContrast_kernel_checked", "ext_dlc_survivingWeightContrast_pos_kernel_proved",
       "ext_dlc_survivingWeightContrast_eq_kernel_proved", "ext_dlc_the_flow_law_contrast_kernel_proved", "ext_dlc_accumulatedContrast_one_kernel_proved",
       "ext_dlc_contrast_one_recovers_D1a_kernel_proved", "ext_dlc_beta_zero_recovers_lcdm_contrast_kernel_proved", "ext_dlc_local_exceeds_background_contrast_kernel_proved",
       "ext_dlc_accumulatedContrast_ge_of_le_kernel_proved", "ext_dlc_accumulatedContrast_le_of_le_one_kernel_proved", "ext_dlc_the_deviation_reads_below_the_asymptote_kernel_proved",
       "ext_dlc_frw_accumulated_contrast_kernel_proved", "ext_dlc_the_derived_kernel_factor_kernel_proved", "ext_dlc_the_derived_kernel_factor_normalized_kernel_proved",
       "ext_dlc_the_dissipation_law_with_contrast_kernel_proved", "ext_dlc_the_dissipation_law_with_contrast_and_the_physical_arrow_kernel_proved"]
FLAGS = list(zip(DLC, NOMES["TheFlowLawContrast"]))
assert len(FLAGS) == 20 and len({f for f, _ in FLAGS}) == 20
for f, nm in FLAGS:   # a bandeira NOMEIA a declaracao (posicao a posicao, conferido pelo nome)
    assert nm.split(".")[-1].lower().replace("_", "") in f.lower().replace("_", ""), (f, nm)
    assert f.replace("ext_dlc_", "").rsplit("_kernel_", 1)[0] == nm.split(".")[-1], (f, nm)   # v378: a bandeira e o nome EXATO da declaracao
assert set(re.findall(r'"(ext_dlc_[A-Za-z0-9_]+)"', RT)) == set(f for f, _ in FLAGS)
for f, _ in FLAGS:
    assert f not in T, f
A01 = '    "ext_dis_the_dissipation_law_kernel_proved": "TGLExt.TheFlowLawD1a.the_dissipation_law",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v378 (30/09/2026, noite; o que faltou: o nucleo derivado D1b tipado): dlc (20)" + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +20 (ext_dlc_).")
A02 = '        "ext_dis_the_dissipation_law_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v378: a lei da dissipacao com contraste (20)" + CRLF
    + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +20 (5899 -> 5919).")
A03 = '    ("v377", "TheFlowLawD1a", "TGLExt/TheFlowLawD1a.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v378 (30/09/2026, noite): a lei da dissipacao com CONTRASTE -- o nucleo derivado D1b (K = E(z*)^{2beta/3}); o D1a e o caso g = 1" + CRLF
    + '    ("v378", "TheFlowLawContrast", "TGLExt/TheFlowLawContrast.lean", None, None),' + CRLF, "_ESQUELETO_STONES: +1 pedra v378.")
m = re.search(r'^UM_VERSION = "v377"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v377"') == 1
add("V04_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v378"   # v378 (30/09/2026, noite): a CONSTANTE UNICA de versao -- carimba os .md emitidos e o selo (regra da linhagem completa); v377 em 30/09' + CRLF,
    "UM_VERSION = 'v378'.")
assert T.count(RT7_FIRST) == 1
add("V05_runtime", "G_RUNTIME", RT7_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT7_FIRST,
    "runtime: prove_the_dissipation_law_with_contrast_v378, prove_what_was_missed_v378, prove_bancada_fase4_v378; _v378_lcdm_E, _v378_contrast_integral, _V378_GUARDA.")
reg = []
for key, fn, rot in (("the_dissipation_law_with_contrast_v378", "prove_the_dissipation_law_with_contrast_v378", "a lei da dissipacao com contraste (o nucleo derivado D1b)"),
                     ("what_was_missed_v378", "prove_what_was_missed_v378", "o que faltou (D1b e a dupla contagem de beta; errata E12 ao lado)"),
                     ("bancada_fase4_v378", "prove_bancada_fase4_v378", "a Fase 4 da Bancada (o desvio), por hash")):
    reg.append('    core["%s"] = %s(core.get("omega_I", 1.0), core)   # v378: %s' % (key, fn, rot))
    reg.append('    print("   [v378] %s: %%s" %% core["%s"]["verdict"])' % (rot, key))
A06 = '    print("   [v377] a leitura das pedras do operador: %s" % core["final_stone_reading_v377"]["verdict"])' + CRLF
add("V06_registro", "G_RUNTIME", A06, A06 + CRLF.join(reg) + CRLF, "core: +3 chaves v378 (depois das v377).")
pt = open(os.path.join(HERE, "artigo_pt_v378.pysnip"), encoding="utf-8").read()
assert T.count(PT7_FIRST) == 1
add("V07_artigo_PT", "G_ARTIGO", PT7_FIRST, crlf(pt.rstrip("\n") + "\n") + PT7_FIRST, "artigo PT: paragrafo 'Ao lado (v378)' (E12 errata; a lei com contraste; a Fase 4).")
en = open(os.path.join(HERE, "artigo_en_v378.pysnip"), encoding="utf-8").read()
assert T.count(EN7_FIRST) == 1
add("V08_artigo_EN", "G_ARTIGO", EN7_FIRST, crlf(en.rstrip("\n") + "\n") + EN7_FIRST, "artigo EN: paragrafo 'Beside (v378)'.")
A09 = linha_unica(r'^ {12}"the_dissipation_law_reading_v377": ')
add("V09_selo", "G_SELO", A09, A09 + '            # v378 (30/09/2026, noite) -- LEITURA, ao lado; nenhum valor do gate muda' + CRLF
    + '            "the_contrast_and_deviation_reading_v378": "OPERATOR_INPUT_2026_09_30_NIGHT__WHAT_WAS_MISSED_EXAMINED__DERIVED_KERNEL_D1B_TYPED_TheFlowLawContrast_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__'
    + 'D1A_IS_THE_CASE_G_EQ_1__ARTICLE_CONVENTION_LAW_TRANSPORTS_THE_LCDM_CALIBRATION__STACKING_ON_THE_EFFECTIVE_BACKGROUND_READ_AS_COUNTING_BETA_TWICE_DERIVED_FROM_THE_CONVENTION_READING_E12_BESIDE__WHICH_BACKGROUND_IS_THE_BACKGROUND_OPEN__'
    + 'FASE4_DEVIATION_PREREGISTERED_READ_BY_HASH__INTERMEDIATE_REGISTERS_TEST_THAT_COULD_LOSE__OPEN_READING_NOT_ADOPTED__GATE_UNTOUCHED",' + CRLF,
    "selo: +1 leitura (string) v378.")
A10 = linha_unica(r'^ {8}"flow_layer_status_v377": "TYPED_AS_')
add("V10_coma_chave_ao_lado", "G_RUNTIME", A10, A10
    + '        # v378 (30/09/2026, noite) AO LADO: o nucleo derivado D1b tipado no kernel (TGLExt.TheFlowLawContrast); as chaves antigas ficam como estavam (historico)' + CRLF
    + '        "flow_layer_kernel_v378": "CONTRAST_KERNEL_D1B_TYPED__TGLExt.TheFlowLawContrast.the_derived_kernel_factor__K_EQ_E_ZSTAR_POW_2BETA_OVER_3__D1A_IS_THE_CASE_G_EQ_1__NOT_A_CONFIRMATION__THE_OLDER_KEYS_STAY_BESIDE",' + CRLF,
    "modulo de Coma v39: flow_layer_kernel_v378 ao lado (as antigas ficam).")
# homonimos
_decl = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|scoped|noncomputable|partial|unsafe)\s+)*"
                   r"(theorem|lemma|def|structure|abbrev|instance|inductive|class)\s+([A-Za-z_][A-Za-z0-9_'!?]*(?:\.[A-Za-z_][A-Za-z0-9_'!?]*)*)", re.M)
onde, amb = {}, []
for rel, texto in cand.items():
    if not rel.endswith(".lean"):
        continue
    for tipo, nome in _decl.findall(texto):
        if nome in onde and onde[nome][0] != rel:
            amb.append(nome)
        onde.setdefault(nome, (rel, tipo))
known = set()
tags = [t for t in ("_AMBIGUOS_CONJUNTO_V369 = frozenset([", "_AMBIGUOS_CONJUNTO_V372 = frozenset([", "_AMBIGUOS_CONJUNTO_V375 = frozenset([", "_AMBIGUOS_CONJUNTO_V376 = frozenset([",
                    "_AMBIGUOS_CONJUNTO_V377 = frozenset([") if t in T]
for tag in tags:
    i = T.index(tag); jf = T.index("])", i)
    known |= set(re.findall(r'"([^"]+)"', T[i:jf]))
novos = sorted(set(amb) - known)
if novos:
    last = tags[-1]
    i = T.index(last); jf = T.index("])", i)
    anch = T[i:jf + 4]
    assert anch.endswith("])\r\n")
    add("V24_homonimos_v378", "G_PEDRAS", anch, anch + "    # v378 -- homonimos NOVOS das pedras v378, NOMEADOS por script, nunca silenciados.\r\n"
        "    _AMBIGUOS_CONJUNTO_V378 = frozenset([\r\n" + "".join('        "%s",\r\n' % n for n in novos) + "    ])\r\n", "IALD index: +_AMBIGUOS_CONJUNTO_V378 (%d)." % len(novos))
    uni = " | ".join(t.split(" = ")[0] for t in tags)
    old_chk = 'bool(set(ix["ambiguos"]) <= (%s))' % uni
    add("V25_homonimos_check", "G_PEDRAS", old_chk, 'bool(set(ix["ambiguos"]) <= (%s | _AMBIGUOS_CONJUNTO_V378))' % uni, "IALD index: o check de ambiguos passa a incluir V378.")
for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue
    nw = p["new"]
    assert not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", nw.replace("NOT_FALSIFIED", "")), (p["id"], "CONFIRMED")
    assert not re.search(r"(?<!AP)PROVED_BY", nw), (p["id"], "PROVED_BY")
    assert "TGL_PROVED" not in nw and "CONSCIOUSNESS_PROVED" not in nw, p["id"]
ast.parse(T)
out = os.path.join(HERE, "um_v378_candidato.py")
b = T.encode("utf-8")
open(out + ".tmp", "wb").write(b); os.replace(out + ".tmp", out)
meta = {"um_py_base": SHA0, "candidato_sha16": hashlib.sha256(b).hexdigest()[:16], "kernel": KERNEL_MANIFEST,
        "n_patches": len(patches), "homonimos_novos": novos, "n_bandeiras": len(FLAGS)}
json.dump({"meta": meta, "patches": patches}, open(os.path.join(HERE, "patches_v378.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(FLAGS, open(os.path.join(HERE, "BANDEIRAS_v378.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(json.dumps({k: meta[k] for k in ("candidato_sha16", "n_patches", "n_bandeiras")}, ensure_ascii=False), "homonimos novos:", novos)
