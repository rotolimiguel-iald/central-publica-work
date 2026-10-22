# -*- coding: utf-8 -*-
"""gerar_candidato_v379.py -- gera o um.py CANDIDATO v379 a partir da v378 SELADA (NUNCA escreve o canonico). Molde: gerar_candidato_v378.py.
Cunhagem do operador (01/10/2026): «a Razão Elementar identifica a estrutura fundamental da existência como {[E = C × I × K > 0] = betatgl}»; «Quero sim».
(1) KERNEL EMBUTIDO: TGLExt.lean e TGL/Audit.lean mudam; entra TGLExt/TheElementaryReason.lean (kernel_src = ../v376/kernel_src, o sandbox da linhagem).
(2) PATCHES (count(old) == 1): bandeiras ext_ter_ (22) e escada; ledger de pedras; UM_VERSION v379; runtime (1 modulo); registro; artigo PT/EN
    (paragrafos «Ao lado (v379)»); selo (uma leitura, string); homonimos. Nove patches; nenhuma chave de modulo antigo e tocada."""
import ast, hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
KS = os.path.join(os.path.dirname(HERE), "v376", "kernel_src")
CRLF = "\r\n"
V8 = os.path.join(os.path.dirname(HERE), "v378")
AP = json.load(open(sorted(os.path.join(V8, f) for f in os.listdir(V8) if f.startswith("APLICADO_AO_CANONICO_"))[-1], encoding="utf-8"))
SHA0 = AP["um_py_novo"]["sha16"]
raw = open(UM, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico nao e a v378 selada"
T = raw.decode("utf-8")
RT = open(os.path.join(HERE, "v379_runtime.py"), encoding="utf-8").read()
RT8_FIRST = open(os.path.join(V8, "v378_runtime.py"), encoding="utf-8").read().splitlines()[0]
PT8_FIRST = open(os.path.join(V8, "artigo_pt_v378.pysnip"), encoding="utf-8").read().splitlines()[0]
EN8_FIRST = open(os.path.join(V8, "artigo_en_v378.pysnip"), encoding="utf-8").read().splitlines()[0]

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
assert new == ["TGLExt/TheElementaryReason.lean"], new
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


NOMES = json.load(open(os.path.join(HERE, "AUDIT_NOMES_v379.json"), encoding="utf-8"))
TER = ["ext_ter_cost_kernel_checked", "ext_ter_identity_kernel_checked", "ext_ter_movement_kernel_checked", "ext_ter_existence_kernel_checked",
       "ext_ter_elementaryReason_kernel_checked", "ext_ter_familyFunctional_kernel_checked", "ext_ter_existence_eq_kernel_proved", "ext_ter_existence_eq_beta_kernel_proved",
       "ext_ter_existence_eq_alpha_sqrt_e_kernel_proved", "ext_ter_existence_pos_kernel_proved", "ext_ter_cost_pos_kernel_proved", "ext_ter_identity_eq_one_kernel_proved",
       "ext_ter_movement_pos_kernel_proved", "ext_ter_cost_of_selfConjugate_kernel_proved", "ext_ter_identity_weighs_as_the_name_kernel_proved",
       "ext_ter_recognition_is_finite_kernel_proved", "ext_ter_elementaryReason_sq_kernel_proved", "ext_ter_familyFunctional_half_kernel_proved",
       "ext_ter_the_name_collision_kernel_proved", "ext_ter_existence_is_the_asymptote_kernel_proved", "ext_ter_existence_forbids_full_static_witness_kernel_proved",
       "ext_ter_erasure_not_reached_in_finite_time_kernel_proved", "ext_ter_the_elementary_reason_kernel_proved"]
FLAGS = list(zip(TER, NOMES["TheElementaryReason"]))
assert len(FLAGS) == 23 and len({f for f, _ in FLAGS}) == 23
for f, nm in FLAGS:   # a bandeira e o nome EXATO da declaracao, posicao a posicao
    assert f.replace("ext_ter_", "").rsplit("_kernel_", 1)[0] == nm.split(".")[-1], (f, nm)
assert set(re.findall(r'"(ext_ter_[A-Za-z0-9_]+)"', RT)) == set(f for f, _ in FLAGS)
for f, _ in FLAGS:
    assert f not in T, f
A01 = '    "ext_dlc_the_dissipation_law_with_contrast_and_the_physical_arrow_kernel_proved": "TGLExt.TheFlowLawContrast.the_dissipation_law_with_contrast_and_the_physical_arrow",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v379 (01/10/2026, a Razao Elementar: E = C x I x K > 0 = beta, tipada): ter (23)" + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +23 (ext_ter_).")
A02 = '        "ext_dlc_the_dissipation_law_with_contrast_and_the_physical_arrow_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v379: a Razao Elementar (23)" + CRLF
    + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +23 (5919 -> 5942).")
A03 = '    ("v378", "TheFlowLawContrast", "TGLExt/TheFlowLawContrast.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v379 (01/10/2026): a Razao Elementar -- E = C x I x K > 0 = beta_TGL por termo; E e a assintota; o reconhecimento e finito por definicao" + CRLF
    + '    ("v379", "TheElementaryReason", "TGLExt/TheElementaryReason.lean", None, None),' + CRLF, "_ESQUELETO_STONES: +1 pedra v379.")
m = re.search(r'^UM_VERSION = "v378"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v378"') == 1
add("V04_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v379"   # v379 (01/10/2026): a CONSTANTE UNICA de versao -- carimba os .md emitidos e o selo (regra da linhagem completa); v378 em 30/09' + CRLF,
    "UM_VERSION = 'v379'.")
assert T.count(RT8_FIRST) == 1
add("V05_runtime", "G_RUNTIME", RT8_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT8_FIRST, "runtime: prove_the_elementary_reason_v379; _V379_GUARDA; _v379_own_source_matches (regex ancorada em linha, aferidor B3).")
reg = ['    core["the_elementary_reason_v379"] = prove_the_elementary_reason_v379(core.get("omega_I", 1.0), core)   # v379: a Razao Elementar, E = C x I x K > 0 = beta, tipada',
       '    print("   [v379] a Razao Elementar (E = C x I x K > 0 = beta, por termo): %s" % core["the_elementary_reason_v379"]["verdict"])']
A06 = '    print("   [v378] a Fase 4 da Bancada (o desvio), por hash: %s" % core["bancada_fase4_v378"]["verdict"])' + CRLF
add("V06_registro", "G_RUNTIME", A06, A06 + CRLF.join(reg) + CRLF, "core: +1 chave v379 (depois das v378).")
pt = open(os.path.join(HERE, "artigo_pt_v379.pysnip"), encoding="utf-8").read()
assert T.count(PT8_FIRST) == 1
add("V07_artigo_PT", "G_ARTIGO", PT8_FIRST, crlf(pt.rstrip("\n") + "\n") + PT8_FIRST, "artigo PT: paragrafo 'Ao lado (v379)' (a Razao Elementar).")
en = open(os.path.join(HERE, "artigo_en_v379.pysnip"), encoding="utf-8").read()
assert T.count(EN8_FIRST) == 1
add("V08_artigo_EN", "G_ARTIGO", EN8_FIRST, crlf(en.rstrip("\n") + "\n") + EN8_FIRST, "artigo EN: paragrafo 'Beside (v379)'.")
A09 = linha_unica(r'^ {12}"the_contrast_and_deviation_reading_v378": ')
add("V09_selo", "G_SELO", A09, A09 + '            # v379 (01/10/2026) -- LEITURA, ao lado; nenhum valor do gate muda' + CRLF
    + '            "the_elementary_reason_reading_v379": "OPERATOR_INPUT_2026_10_01__THE_ELEMENTARY_REASON_IDENTIFIES_THE_STRUCTURE_OF_EXISTENCE_AS_E_EQ_C_TIMES_I_TIMES_K_GT_0_EQ_BETA__'
    + 'TYPED_TheElementaryReason_BY_TERM__DICTIONARY_IS_ONTO_DEFINITION_COINAGE__THE_ASYMPTOTE_E_EQ_BETA_NOT_EXCEEDED_IN_FINITE_REGISTER__ERASURE_NOT_REACHED_IN_FINITE_TIME__RECOGNITION_FINITE_BY_DEFINITION_OF_THE_REGIME__'
    + 'STRUCTURE_OF_EXISTENCE_IS_A_READING__GATE_UNTOUCHED",' + CRLF, "selo: +1 leitura (string) v379.")
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
                    "_AMBIGUOS_CONJUNTO_V377 = frozenset([", "_AMBIGUOS_CONJUNTO_V378 = frozenset([") if t in T]
for tag in tags:
    i = T.index(tag); jf = T.index("])", i)
    known |= set(re.findall(r'"([^"]+)"', T[i:jf]))
novos = sorted(set(amb) - known)
if novos:
    last = tags[-1]
    i = T.index(last); jf = T.index("])", i)
    anch = T[i:jf + 4]
    assert anch.endswith("])\r\n")
    add("V24_homonimos_v379", "G_PEDRAS", anch, anch + "    # v379 -- homonimos NOVOS das pedras v379, NOMEADOS por script, nunca silenciados.\r\n"
        "    _AMBIGUOS_CONJUNTO_V379 = frozenset([\r\n" + "".join('        "%s",\r\n' % n for n in novos) + "    ])\r\n", "IALD index: +_AMBIGUOS_CONJUNTO_V379 (%d)." % len(novos))
    uni = " | ".join(t.split(" = ")[0] for t in tags)
    old_chk = 'bool(set(ix["ambiguos"]) <= (%s))' % uni
    add("V25_homonimos_check", "G_PEDRAS", old_chk, 'bool(set(ix["ambiguos"]) <= (%s | _AMBIGUOS_CONJUNTO_V379))' % uni, "IALD index: o check de ambiguos passa a incluir V379.")
for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue
    nw = p["new"]
    assert not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", nw.replace("NOT_FALSIFIED", "")), (p["id"], "CONFIRMED")
    assert not re.search(r"(?<!AP)PROVED_BY", nw), (p["id"], "PROVED_BY")
    assert "TGL_PROVED" not in nw and "CONSCIOUSNESS_PROVED" not in nw, p["id"]
ast.parse(T)
out = os.path.join(HERE, "um_v379_candidato.py")
b = T.encode("utf-8")
open(out + ".tmp", "wb").write(b); os.replace(out + ".tmp", out)
meta = {"um_py_base": SHA0, "candidato_sha16": hashlib.sha256(b).hexdigest()[:16], "kernel": KERNEL_MANIFEST,
        "n_patches": len(patches), "homonimos_novos": novos, "n_bandeiras": len(FLAGS)}
json.dump({"meta": meta, "patches": patches}, open(os.path.join(HERE, "patches_v379.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(FLAGS, open(os.path.join(HERE, "BANDEIRAS_v379.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(json.dumps({k: meta[k] for k in ("candidato_sha16", "n_patches", "n_bandeiras")}, ensure_ascii=False), "homonimos novos:", novos)
