# -*- coding: utf-8 -*-
"""gerar_candidato_v377.py -- gera o um.py CANDIDATO v377 a partir da v376 SELADA (NUNCA escreve o canonico). Molde: gerar_candidato_v376.py.
Ordens do operador (30/09/2026): «pode rodar»; «essa lei chama-se dissipacao [dephasing = lei do fluxo = vazamento]»; «nao precisa nomear como hipotese, vc consegue
realizar a prova e cunhar»; «o leitor e a sombra»; «defina fisica»; «destranque tudo [...] utilizar a bancada a fundo»; «buscar o desvio de betatgl».
(1) KERNEL EMBUTIDO: TGLExt.lean e TGL/Audit.lean mudam; entram TGLExt/PhysicsIsTheReading.lean e TGLExt/TheFlowLawD1a.lean (kernel_src = ../v376/kernel_src).
(2) PATCHES (count(old) == 1): bandeiras ext_pir_ (10) + ext_dis_ (15) e escada; ledger de pedras; UM_VERSION v377; runtime (4 modulos); registro; artigo PT/EN
    (paragrafos v377 «Ao lado (v377)»); selo (uma leitura, string); ERRATA AO LADO no modulo de Coma v39 (chave flow_layer_status_v377 ao lado da antiga); homonimos."""
import ast, hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
KS = os.path.join(os.path.dirname(HERE), "v376", "kernel_src")
CRLF = "\r\n"
AP = json.load(open(sorted(os.path.join(os.path.dirname(HERE), "v376", f) for f in os.listdir(os.path.join(os.path.dirname(HERE), "v376"))
                          if f.startswith("APLICADO_AO_CANONICO_"))[-1], encoding="utf-8"))
SHA0 = AP["um_py_novo"]["sha16"]
raw = open(UM, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico nao e a v376 selada"
T = raw.decode("utf-8")
RT = open(os.path.join(HERE, "v377_runtime.py"), encoding="utf-8").read()
V6 = os.path.join(os.path.dirname(HERE), "v376")
RT6_FIRST = open(os.path.join(V6, "v376_runtime.py"), encoding="utf-8").read().splitlines()[0]
PT6_FIRST = open(os.path.join(V6, "artigo_pt_v376.pysnip"), encoding="utf-8").read().splitlines()[0]
EN6_FIRST = open(os.path.join(V6, "artigo_en_v376.pysnip"), encoding="utf-8").read().splitlines()[0]

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
assert new == ["TGLExt/PhysicsIsTheReading.lean", "TGLExt/TheFlowLawD1a.lean"], new
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


NOMES = json.load(open(os.path.join(HERE, "AUDIT_NOMES_v377.json"), encoding="utf-8"))
PIR = ["ext_pir_J_I_smul_kernel_proved", "ext_pir_J_inner_kernel_proved", "ext_pir_the_mirror_conjugates_the_reading_kernel_proved",
       "ext_pir_reader_real_of_selfAdjoint_kernel_proved", "ext_pir_the_shadow_is_the_reader_weighted_by_the_reading_kernel_proved",
       "ext_pir_the_reader_is_the_shadow_of_the_one_kernel_proved", "ext_pir_physics_kernel_checked", "ext_pir_physics_is_real_kernel_proved",
       "ext_pir_one_mem_physics_kernel_proved", "ext_pir_the_ground_state_defines_the_physics_kernel_proved"]
DIS = ["ext_dis_register_kernel_checked", "ext_dis_leakVerb_kernel_checked", "ext_dis_survivingWeight_kernel_checked", "ext_dis_leakFraction_kernel_checked",
       "ext_dis_H0local_kernel_checked", "ext_dis_survivingWeight_pos_kernel_proved", "ext_dis_survivingWeight_eq_kernel_proved", "ext_dis_the_flow_law_D1a_kernel_proved",
       "ext_dis_leakFraction_eq_kernel_proved", "ext_dis_beta_zero_recovers_lcdm_kernel_proved", "ext_dis_local_exceeds_background_kernel_proved",
       "ext_dis_compounded_exceeds_linear_kernel_proved", "ext_dis_the_flow_law_is_the_leak_kernel_proved", "ext_dis_the_flow_law_with_the_physical_arrow_kernel_proved",
       "ext_dis_the_dissipation_law_kernel_proved"]
FLAGS = list(zip(PIR, NOMES["PhysicsIsTheReading"])) + list(zip(DIS, NOMES["TheFlowLawD1a"]))
assert len(FLAGS) == 25 and len({f for f, _ in FLAGS}) == 25
for f, nm in FLAGS:   # a bandeira NOMEIA a declaracao (posicao a posicao, conferido pelo nome)
    assert nm.split(".")[-1].lower().replace("_", "") in f.lower().replace("_", ""), (f, nm)
assert set(re.findall(r'"(ext_(?:pir|dis)_[A-Za-z0-9_]+)"', RT)) == set(f for f, _ in FLAGS)
for f, _ in FLAGS:
    assert f not in T, f
A01 = '    "ext_wio_the_whole_is_one_kernel_proved": "TGLExt.TheWholeIsOne.the_whole_is_one",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v377 (30/09/2026, a lei da dissipacao provada; a fisica e a leitura): pir (10), dis (15)" + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +25 (ext_pir_ 10, ext_dis_ 15).")
A02 = '        "ext_wio_the_whole_is_one_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v377: a fisica e a leitura (10), a lei da dissipacao (15)" + CRLF
    + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +25 (5874 -> 5899).")
A03 = '    ("v376", "TheWholeIsOne", "TGLExt/TheWholeIsOne.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v377 (30/09/2026): a fisica e a leitura (o leitor e a sombra do Um); a lei da dissipacao, provada (dephasing = lei do fluxo = vazamento)" + CRLF
    + '    ("v377", "PhysicsIsTheReading", "TGLExt/PhysicsIsTheReading.lean", None, None),' + CRLF
    + '    ("v377", "TheFlowLawD1a", "TGLExt/TheFlowLawD1a.lean", None, None),' + CRLF, "_ESQUELETO_STONES: +2 pedras v377.")
m = re.search(r'^UM_VERSION = "v376"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v376"') == 1
add("V04_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v377"   # v377 (30/09/2026): a CONSTANTE UNICA de versao -- carimba os .md emitidos e o selo (regra da linhagem completa); v376 em 28/09' + CRLF,
    "UM_VERSION = 'v377'.")
assert T.count(RT6_FIRST) == 1
add("V05_runtime", "G_RUNTIME", RT6_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT6_FIRST,
    "runtime: prove_physics_is_the_reading_v377, prove_the_dissipation_law_v377, prove_bancada_fases_v377, prove_final_stone_reading_v377; _v377_sha256_full, _v377_num, _V377_GUARDA.")
reg = []
for key, fn, rot in (("physics_is_the_reading_v377", "prove_physics_is_the_reading_v377", "a fisica e a leitura (o leitor e a sombra do Um)"),
                     ("the_dissipation_law_v377", "prove_the_dissipation_law_v377", "a lei da dissipacao, provada"),
                     ("bancada_fases_v377", "prove_bancada_fases_v377", "as tres fases da Bancada (30/09), por hash"),
                     ("final_stone_reading_v377", "prove_final_stone_reading_v377", "a leitura das pedras do operador")):
    reg.append('    core["%s"] = %s(core.get("omega_I", 1.0), core)   # v377: %s' % (key, fn, rot))
    reg.append('    print("   [v377] %s: %%s" %% core["%s"]["verdict"])' % (rot, key))
A06 = '    print("   [v376] Tetelestai, a conferencia consumativa refeita: %s" % core["tetelestai_conference_v376"]["verdict"])' + CRLF
add("V06_registro", "G_RUNTIME", A06, A06 + CRLF.join(reg) + CRLF, "core: +4 chaves v377 (depois da conferencia v376).")
pt = open(os.path.join(HERE, "artigo_pt_v377.pysnip"), encoding="utf-8").read()
assert T.count(PT6_FIRST) == 1
add("V07_artigo_PT", "G_ARTIGO", PT6_FIRST, crlf(pt.rstrip("\n") + "\n") + PT6_FIRST, "artigo PT: paragrafo 'Ao lado (v377)' (E10 errata Coma/duas crises; a fisica e a leitura; as tres fases; E11 errata D1 V3; o desvio como foco).")
en = open(os.path.join(HERE, "artigo_en_v377.pysnip"), encoding="utf-8").read()
assert T.count(EN6_FIRST) == 1
add("V08_artigo_EN", "G_ARTIGO", EN6_FIRST, crlf(en.rstrip("\n") + "\n") + EN6_FIRST, "artigo EN: paragrafo 'Beside (v377)'.")
A09 = '            "um_version": UM_VERSION,' + CRLF
add("V09_selo", "G_SELO", A09, A09 + '            # v377 (30/09/2026) -- LEITURA, ao lado; nenhum valor do gate muda' + CRLF
    + '            "the_dissipation_law_reading_v377": "OPERATOR_INPUT_2026_09_30__THE_LAW_IS_CALLED_DISSIPATION_DEPHASING_EQ_FLOW_LAW_EQ_LEAK__PROVE_AND_COIN_NOT_A_NAMED_HYPOTHESIS__'
    + 'FLOW_LAW_D1A_TYPED_AS_IMPLICATION_IN_KERNEL_TheFlowLawD1a__THE_READER_IS_THE_SHADOW_OF_THE_ONE_PhysicsIsTheReading__TGL_EQ_PHYSICS_AS_IDENTITY_OF_READINGS_ONTO__'
    + 'R_MAP_RATIFIED_EFFECTIVE_PERMANENCE_IS_VERB__THREE_BENCH_PHASES_READ_BY_HASH__D1_V3_TENSION_CONDITIONAL_ON_R_MAP_ERRATUM_BESIDE__DEVIATION_FROM_BETA_AS_FOCUS__GATE_UNTOUCHED",' + CRLF,
    "selo: +1 leitura (string) v377.")
A10 = '        "flow_layer_status": "CONJECTURE_DECLARED (camada REAL declarada insuficiente: %.2f%%)" % E1_shift_pct,' + CRLF
add("V10_coma_errata_ao_lado", "G_RUNTIME", A10, A10
    + '        # v377 (30/09/2026) ERRATA AO LADO: a lei do fluxo D1a foi PROVADA como implicacao no kernel (TGLExt.TheFlowLawD1a); a chave antiga fica como estava (historico)' + CRLF
    + '        "flow_layer_status_v377": "TYPED_AS_IMPLICATION_IN_KERNEL__TGLExt.TheFlowLawD1a.the_dissipation_law__H0LOCAL_EQ_H0CMB_TIMES_1PZSTAR_POW_BETA__REGISTER_LN_1PZ_AND_COST_BETA_PER_NAT__NOT_A_CONFIRMATION__THE_OLD_KEY_STAYS_BESIDE",' + CRLF,
    "modulo de Coma v39: flow_layer_status_v377 ao lado (a antiga CONJECTURE_DECLARED fica).")
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
tags = [t for t in ("_AMBIGUOS_CONJUNTO_V369 = frozenset([", "_AMBIGUOS_CONJUNTO_V372 = frozenset([", "_AMBIGUOS_CONJUNTO_V375 = frozenset([", "_AMBIGUOS_CONJUNTO_V376 = frozenset([") if t in T]
for tag in tags:
    i = T.index(tag); jf = T.index("])", i)
    known |= set(re.findall(r'"([^"]+)"', T[i:jf]))
novos = sorted(set(amb) - known)
if novos:
    last = tags[-1]
    i = T.index(last); jf = T.index("])", i)
    anch = T[i:jf + 4]
    assert anch.endswith("])\r\n")
    add("V24_homonimos_v377", "G_PEDRAS", anch, anch + "    # v377 -- homonimos NOVOS das pedras v377, NOMEADOS por script, nunca silenciados.\r\n"
        "    _AMBIGUOS_CONJUNTO_V377 = frozenset([\r\n" + "".join('        "%s",\r\n' % n for n in novos) + "    ])\r\n", "IALD index: +_AMBIGUOS_CONJUNTO_V377 (%d)." % len(novos))
    uni = " | ".join(t.split(" = ")[0] for t in tags)
    old_chk = 'bool(set(ix["ambiguos"]) <= (%s))' % uni
    add("V25_homonimos_check", "G_PEDRAS", old_chk, 'bool(set(ix["ambiguos"]) <= (%s | _AMBIGUOS_CONJUNTO_V377))' % uni, "IALD index: o check de ambiguos passa a incluir V377.")
for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue
    nw = p["new"]
    assert not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", nw.replace("NOT_FALSIFIED", "")), (p["id"], "CONFIRMED")
    assert not re.search(r"(?<!AP)PROVED_BY", nw), (p["id"], "PROVED_BY")
    assert "TGL_PROVED" not in nw and "CONSCIOUSNESS_PROVED" not in nw, p["id"]
ast.parse(T)
out = os.path.join(HERE, "um_v377_candidato.py")
b = T.encode("utf-8")
open(out + ".tmp", "wb").write(b); os.replace(out + ".tmp", out)
meta = {"um_py_base": SHA0, "candidato_sha16": hashlib.sha256(b).hexdigest()[:16], "kernel": KERNEL_MANIFEST,
        "n_patches": len(patches), "homonimos_novos": novos, "n_bandeiras": len(FLAGS)}
json.dump({"meta": meta, "patches": patches}, open(os.path.join(HERE, "patches_v377.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(FLAGS, open(os.path.join(HERE, "BANDEIRAS_v377.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(json.dumps({k: meta[k] for k in ("candidato_sha16", "n_patches", "n_bandeiras")}, ensure_ascii=False), "homonimos novos:", novos)
