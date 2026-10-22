# -*- coding: utf-8 -*-
"""gerar_candidato_v382.py -- gera o um.py CANDIDATO v382 a partir da v381 SELADA (NUNCA escreve o canonico). Molde: gerar_candidato_v381.py (versao com kernel).
A chave do operador (02/10/2026, tarde): «O último elo incide no hamiltoniano oculto. O custo está no reflexo, o pagamento está na face no rosto, no nome»; a ratificacao
de R1-R6 e a correcao «a TGL não é semi ela é ótica»; a ordem «isso mesmo, prossiga».
(1) KERNEL EMBUTIDO: TGLExt.lean e TGL/Audit.lean mudam; entram TGLExt/TheLedgerOfCharges.lean e TGLExt/ThePsionAndTheViscosity.lean (kernel_src = ../v376/kernel_src).
(2) PATCHES (count(old) == 1): bandeiras ext_loc_ (19) + ext_psv_ (13) e escada; ledger de pedras (+2); UM_VERSION v382; runtime (1 modulo, com os sha256 do
    pre-registro LIDOS dos arquivos); registro; artigo PT/EN («Ao lado (v382)»); selo (uma leitura, string); homonimos. Nenhuma chave de modulo antigo e tocada."""
import ast, hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
KS = os.path.join(os.path.dirname(HERE), "v376", "kernel_src")
CRLF = "\r\n"
V0 = os.path.join(os.path.dirname(HERE), "v381")
AP = json.load(open(sorted(os.path.join(V0, f) for f in os.listdir(V0) if f.startswith("APLICADO_AO_CANONICO_"))[-1], encoding="utf-8"))
SHA0 = AP["um_py_novo"]["sha16"]
raw = open(UM, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico nao e a v381 selada"
T = raw.decode("utf-8")
RT = open(os.path.join(HERE, "v382_runtime.py"), encoding="utf-8").read()
RT0_FIRST = open(os.path.join(V0, "v381_runtime.py"), encoding="utf-8").read().splitlines()[0]
PT0_FIRST = open(os.path.join(V0, "artigo_pt_v381.pysnip"), encoding="utf-8").read().splitlines()[0]
EN0_FIRST = open(os.path.join(V0, "artigo_en_v381.pysnip"), encoding="utf-8").read().splitlines()[0]
# os sha256 do pre-registro, LIDOS dos arquivos (nunca digitados), entram no runtime no lugar dos marcadores
# (V1.3: supersede o V1.2, o V1.1 e o V1 pelos achados das tres afericoes da v382, antes de qualquer estimador ou dado novo; mapa seq 275 -> 276 -> 279 -> 282, ERRATAs ao lado)
PREREG = {"json": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.json",
          "md": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.md"}
assert all(RT.count('"path": "%s"' % p) == 1 for p in PREREG.values()), "os caminhos do pre-registro no runtime nao sao os do gerador"
PREREG_SHA = {k: hashlib.sha256(open(p, "rb").read()).hexdigest() for k, p in PREREG.items()}
assert RT.count("__PREREG_JSON_SHA256__") == 1 and RT.count("__PREREG_MD_SHA256__") == 1
RT = RT.replace("__PREREG_JSON_SHA256__", PREREG_SHA["json"]).replace("__PREREG_MD_SHA256__", PREREG_SHA["md"])
_PJ = json.load(open(PREREG["json"], encoding="utf-8"))
assert _PJ.get("identificador") == "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_3" and len(_PJ.get("cobrancas") or []) == 20
_ECO = _PJ["eco_como_copia_atrasada"]; assert _ECO["pares"] == 9 and _ECO["extintos"] + _ECO["inconclusivos"] == 9
_ECO_TOK = "DELAYED_ECHO_OUTSIDE_THE_CHAIN_%d_OF_%d_PAIRS_EXTINGUISHED_%d_INCONCLUSIVE_NOT_THE_RULE" % (_ECO["extintos"], _ECO["pares"], _ECO["inconclusivos"])
# 4a verificacao (R-2): «FALSIFIED so onde a lei do canal o admite» -- a contagem LIDA do V1.3 (n_canal_futuro_com_falsified), conferida contra as vinte cobrancas
_NC = len(_PJ["cobrancas"]); _NCF = _PJ.get("n_canal_futuro_com_falsified")
assert isinstance(_NCF, int) and not isinstance(_NCF, bool) and _NCF == sum(1 for c in _PJ["cobrancas"] if c.get("canal_futuro_com_falsified") is True) and 0 < _NCF < _NC
_FW_TOK = "FALSIFIED_WHERE_THE_READING_LAW_ADMITS_%d_OF_%d_CHANNELS" % (_NCF, _NC)

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
assert new == ["TGLExt/TheLedgerOfCharges.lean", "TGLExt/ThePsionAndTheViscosity.lean"], new
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


NOMES = json.load(open(os.path.join(HERE, "AUDIT_NOMES_v382.json"), encoding="utf-8"))
_rt_ns = {}
exec(compile("import re\n" + "\n".join(l for l in RT.splitlines() if l.startswith(("_LOC_FLAGS_V382", "_PSV_FLAGS_V382")) or l.startswith("    \"ext_")), "<flags>", "exec"), _rt_ns)
LOC = list(_rt_ns["_LOC_FLAGS_V382"]); PSV = list(_rt_ns["_PSV_FLAGS_V382"])
FLAGS = list(zip(LOC, NOMES["TheLedgerOfCharges"])) + list(zip(PSV, NOMES["ThePsionAndTheViscosity"]))
assert len(FLAGS) == 32 and len({f for f, _ in FLAGS}) == 32 and len(NOMES["TheLedgerOfCharges"]) == 19 and len(NOMES["ThePsionAndTheViscosity"]) == 13
for f, nm in FLAGS:   # a bandeira e o nome EXATO da declaracao, posicao a posicao
    pfx = "ext_loc_" if f.startswith("ext_loc_") else "ext_psv_"
    assert f.replace(pfx, "").rsplit("_kernel_", 1)[0] == nm.split(".")[-1], (f, nm)
assert set(re.findall(r'"(ext_(?:loc|psv)_[A-Za-z0-9_]+)"', RT)) == set(f for f, _ in FLAGS)
for f, _ in FLAGS:
    assert f not in T, f
A01 = '    "ext_tmr_the_matrix_rule_kernel_proved": "TGLExt.TheMatrixRule.the_matrix_rule",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v382 (02/10/2026, a chave: o ultimo elo incide no Hamiltoniano oculto; o custo no reflexo, o pagamento na face; a TGL e otica, le os dois lados): loc (19) + psv (13)" + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +32 (ext_loc_ 19, ext_psv_ 13).")
A02 = '        "ext_tmr_the_matrix_rule_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v382: o livro de cobrancas (19) + o psion e a viscosidade (13)" + CRLF
    + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +32 (5966 -> 5998).")
A03 = '    ("v381", "TheMatrixRule", "TGLExt/TheMatrixRule.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v382 (02/10/2026): o livro de cobrancas (a otica: os dois lados se leem; nenhum desfecho move a regra) e o psion com a viscosidade" + CRLF
    + '    ("v382", "TheLedgerOfCharges", "TGLExt/TheLedgerOfCharges.lean", None, None),' + CRLF
    + '    ("v382", "ThePsionAndTheViscosity", "TGLExt/ThePsionAndTheViscosity.lean", None, None),' + CRLF, "_ESQUELETO_STONES: +2 pedras v382.")
m = re.search(r'^UM_VERSION = "v381"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v381"') == 1
add("V04_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v382"   # v382 (02/10/2026): a CONSTANTE UNICA de versao -- carimba os .md emitidos e o selo (regra da linhagem completa); v381 em 02/10' + CRLF,
    "UM_VERSION = 'v382'.")
assert T.count(RT0_FIRST) == 1
add("V05_runtime", "G_RUNTIME", RT0_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT0_FIRST, "runtime: prove_the_ledger_of_charges_v382; _V382_GUARDA; _V382_FLAGS; _V382_PREREG com sha256 lidos.")
reg = ['    core["the_ledger_of_charges_v382"] = prove_the_ledger_of_charges_v382(core.get("omega_I", 1.0), core)   # v382: o livro de cobrancas (a otica; nenhum desfecho move a regra), o psion e a viscosidade, o pre-registro dos dois lados por hash',
       '    print("   [v382] o livro de cobrancas (os dois lados; nenhum desfecho move a regra), o psion e a viscosidade, o pre-registro por hash: %s" % core["the_ledger_of_charges_v382"]["verdict"])']
A06 = linha_unica(r'^    print\("   \[v381\] a regra matriz')
add("V06_registro", "G_RUNTIME", A06, A06 + CRLF.join(reg) + CRLF, "core: +1 chave v382 (depois da v381).")
pt = open(os.path.join(HERE, "artigo_pt_v382.pysnip"), encoding="utf-8").read()
assert T.count(PT0_FIRST) == 1
add("V07_artigo_PT", "G_ARTIGO", PT0_FIRST, crlf(pt.rstrip("\n") + "\n") + PT0_FIRST, "artigo PT: paragrafo 'Ao lado (v382)' (o livro de cobrancas e a viscosidade).")
en = open(os.path.join(HERE, "artigo_en_v382.pysnip"), encoding="utf-8").read()
assert T.count(EN0_FIRST) == 1
add("V08_artigo_EN", "G_ARTIGO", EN0_FIRST, crlf(en.rstrip("\n") + "\n") + EN0_FIRST, "artigo EN: paragrafo 'Beside (v382)'.")
A09 = linha_unica(r'^ {12}"the_matrix_rule_reading_v381": ')
add("V09_selo", "G_SELO", A09, A09 + '            # v382 (02/10/2026) -- LEITURA, ao lado; nenhum valor do gate muda (o nome do degrau final e PROPOSTO ao lado, nao aplicado)' + CRLF
    + '            "the_ledger_of_charges_reading_v382": "OPERATOR_KEY_2026_10_02__THE_LAST_LINK_INCIDES_ON_THE_HIDDEN_HAMILTONIAN__THE_COST_IS_IN_THE_REFLECTION_THE_PAYMENT_IS_IN_THE_FACE_THE_NAME__KEY_AND_OPTICS_INPUT_ONTO__R1_TO_R6_RATIFIED_INPUT_ONTO__'
    + 'THE_TGL_IS_OPTICS_NOT_SEMI_READS_BOTH_SIDES__TYPED_TheLedgerOfCharges_AND_ThePsionAndTheViscosity_BY_TERM_TRIVIAL_STATED_AS_TRIVIAL__ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME__' + _FW_TOK + '__NONE_MOVES_THE_RULE__'
    + 'THE_GATE_DOES_NOT_READ_THE_LEDGER_BY_THE_RUNTIME_PROBES__PSION_NORM_ONE_ZERO_OF_THE_MINIMAL_LOCK_ON_THE_HIDDEN_HAMILTONIAN__SPEC_S_THETA_TO_HMINMIC_NO_TERM__VISCOSITY_RULE_TIMES_CONTRAST_NAME_ONTO__'
    + 'FINAL_STEP_NAME_PROPOSED_BESIDE_TETELESTAI_CONSUMMATED_PAYMENT_IN_THE_FACE_THE_NAME__PREREGISTRATION_OF_BOTH_SIDES_V1_3_BY_HASH_TWENTY_CHARGES_PHASE6_AND_AMENDMENT_RULES_READ_IN_ORDER__R4_FROZEN_SET_NO_FALSIFIED_SAME_SOURCE_AS_THE_GATE__'
    + 'F2_BY_THE_MEASUREMENT_SYSTEMATIC__F1_D1B_ONE_SIDED__F4_FROZEN_KILL_RULE__BRANCH_B_CLOSED__' + _ECO_TOK + '__THREE_AUDITS_AND_THE_VERIFICATION_OF_THE_DISPOSITIONS_ACCEPTED__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF, "selo: +1 leitura (string) v382.")
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
                    "_AMBIGUOS_CONJUNTO_V377 = frozenset([", "_AMBIGUOS_CONJUNTO_V378 = frozenset([", "_AMBIGUOS_CONJUNTO_V379 = frozenset([", "_AMBIGUOS_CONJUNTO_V381 = frozenset([") if t in T]
for tag in tags:
    i = T.index(tag); jf = T.index("])", i)
    known |= set(re.findall(r'"([^"]+)"', T[i:jf]))
novos = sorted(set(amb) - known)
if novos:
    last = tags[-1]
    i = T.index(last); jf = T.index("])", i)
    anch = T[i:jf + 4]
    assert anch.endswith("])\r\n")
    add("V24_homonimos_v382", "G_PEDRAS", anch, anch + "    # v382 -- homonimos NOVOS das pedras v382, NOMEADOS por script, nunca silenciados.\r\n"
        "    _AMBIGUOS_CONJUNTO_V382 = frozenset([\r\n" + "".join('        "%s",\r\n' % n for n in novos) + "    ])\r\n", "IALD index: +_AMBIGUOS_CONJUNTO_V382 (%d)." % len(novos))
    uni = " | ".join(t.split(" = ")[0] for t in tags)
    old_chk = 'bool(set(ix["ambiguos"]) <= (%s))' % uni
    add("V25_homonimos_check", "G_PEDRAS", old_chk, 'bool(set(ix["ambiguos"]) <= (%s | _AMBIGUOS_CONJUNTO_V382))' % uni, "IALD index: o check de ambiguos passa a incluir V382.")
for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue
    nw = p["new"]
    assert not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", nw.replace("NOT_FALSIFIED", "")), (p["id"], "CONFIRMED")
    assert not re.search(r"(?<!AP)PROVED_BY", nw), (p["id"], "PROVED_BY")
    assert "TGL_PROVED" not in nw and "CONSCIOUSNESS_PROVED" not in nw, p["id"]
ast.parse(T)
out = os.path.join(HERE, "um_v382_candidato.py")
b = T.encode("utf-8")
open(out + ".tmp", "wb").write(b); os.replace(out + ".tmp", out)
meta = {"um_py_base": SHA0, "candidato_sha16": hashlib.sha256(b).hexdigest()[:16], "kernel": KERNEL_MANIFEST,
        "n_patches": len(patches), "homonimos_novos": novos, "n_bandeiras": len(FLAGS), "preregistro_sha256": PREREG_SHA}
json.dump({"meta": meta, "patches": patches}, open(os.path.join(HERE, "patches_v382.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(FLAGS, open(os.path.join(HERE, "BANDEIRAS_v382.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(json.dumps({k: meta[k] for k in ("candidato_sha16", "n_patches", "n_bandeiras")}, ensure_ascii=False), "homonimos novos:", novos, "| kernel:", KERNEL_MANIFEST["changed"], KERNEL_MANIFEST["new"], "| prereg:", {k: v[:16] for k, v in PREREG_SHA.items()})
