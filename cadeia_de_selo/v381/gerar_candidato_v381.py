# -*- coding: utf-8 -*-
"""gerar_candidato_v381.py -- gera o um.py CANDIDATO v381 a partir da v380 SELADA (NUNCA escreve o canonico). Molde: gerar_candidato_v379.py (versao com kernel).
Cunhagem do operador (02/10/2026): «Betatgl é a regra matriz, a regra matriz é: havendo traço há sinal [...] o critério de parada é a lei matriz, ou seja, o TETELESTAI»;
ratificacao: «É exatamente isso».
(1) KERNEL EMBUTIDO: TGLExt.lean e TGL/Audit.lean mudam; entra TGLExt/TheMatrixRule.lean (kernel_src = ../v376/kernel_src, o sandbox da linhagem).
(2) PATCHES (count(old) == 1): bandeiras ext_tmr_ (22) e escada; ledger de pedras; UM_VERSION v381; runtime (1 modulo); registro; artigo PT/EN
    (paragrafos «Ao lado (v381)»); selo (uma leitura, string); homonimos. Nove patches; nenhuma chave de modulo antigo e tocada."""
import ast, hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
KS = os.path.join(os.path.dirname(HERE), "v376", "kernel_src")
CRLF = "\r\n"
V0 = os.path.join(os.path.dirname(HERE), "v380")
AP = json.load(open(sorted(os.path.join(V0, f) for f in os.listdir(V0) if f.startswith("APLICADO_AO_CANONICO_"))[-1], encoding="utf-8"))
SHA0 = AP["um_py_novo"]["sha16"]
raw = open(UM, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico nao e a v380 selada"
T = raw.decode("utf-8")
RT = open(os.path.join(HERE, "v381_runtime.py"), encoding="utf-8").read()
RT0_FIRST = open(os.path.join(V0, "v380_runtime.py"), encoding="utf-8").read().splitlines()[0]
PT0_FIRST = open(os.path.join(V0, "artigo_pt_v380.pysnip"), encoding="utf-8").read().splitlines()[0]
EN0_FIRST = open(os.path.join(V0, "artigo_en_v380.pysnip"), encoding="utf-8").read().splitlines()[0]

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
assert new == ["TGLExt/TheMatrixRule.lean"], new
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


NOMES = json.load(open(os.path.join(HERE, "AUDIT_NOMES_v381.json"), encoding="utf-8"))
TMR = ["ext_tmr_TracoHaSinal_kernel_checked", "ext_tmr_traco_ha_sinal_kernel_proved", "ext_tmr_SinalHaRegistro_kernel_checked", "ext_tmr_sinal_ha_registro_kernel_proved", "ext_tmr_RegistroHaNome_kernel_checked", "ext_tmr_registro_ha_nome_kernel_proved",
       "ext_tmr_NomeHaDistincao_kernel_checked", "ext_tmr_nome_ha_distincao_kernel_proved", "ext_tmr_DistincaoHaOperacao_kernel_checked", "ext_tmr_distincao_ha_operacao_kernel_proved",
       "ext_tmr_OperacaoHaParametrizacao_kernel_checked", "ext_tmr_operacao_ha_parametrizacao_kernel_proved", "ext_tmr_ParametrizacaoHaEmergencia_kernel_checked",
       "ext_tmr_parametrizacao_ha_emergencia_kernel_proved", "ext_tmr_EmergenciaHaQuantizacao_kernel_checked", "ext_tmr_emergencia_ha_quantizacao_kernel_proved",
       "ext_tmr_QuantizacaoHaEspectro_kernel_checked", "ext_tmr_quantizacao_ha_espectro_kernel_proved", "ext_tmr_CustoPago_kernel_checked", "ext_tmr_the_cost_is_paid_kernel_proved",
       "ext_tmr_the_law_precedes_the_charge_kernel_proved", "ext_tmr_chainOrder_kernel_checked", "ext_tmr_chain_has_ten_names_kernel_proved", "ext_tmr_the_matrix_rule_kernel_proved"]
FLAGS = list(zip(TMR, NOMES["TheMatrixRule"]))
assert len(FLAGS) == 24 and len({f for f, _ in FLAGS}) == 24 and len(NOMES["TheMatrixRule"]) == 24
for f, nm in FLAGS:   # a bandeira e o nome EXATO da declaracao, posicao a posicao
    assert f.replace("ext_tmr_", "").rsplit("_kernel_", 1)[0] == nm.split(".")[-1], (f, nm)
assert set(re.findall(r'"(ext_tmr_[A-Za-z0-9_]+)"', RT)) == set(f for f, _ in FLAGS)
for f, _ in FLAGS:
    assert f not in T, f
A01 = '    "ext_ter_the_elementary_reason_kernel_proved": "TGLExt.TheElementaryReason.the_elementary_reason",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v381 (02/10/2026, a regra matriz: dez nomes, nove elos (oito «havendo» ditos + a radicalizacao pela Meia-Nat), num so termo; a clausula aberta sinal -> registro = a radicalizacao pela Meia-Nat; o criterio de parada e o custo pago): tmr (24)" + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +24 (ext_tmr_).")
A02 = '        "ext_ter_the_elementary_reason_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v381: a regra matriz (24)" + CRLF
    + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +24 (5942 -> 5966).")
A03 = '    ("v379", "TheElementaryReason", "TGLExt/TheElementaryReason.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v381 (02/10/2026): a regra matriz -- os dez nomes na ordem do operador, cada elo por termo; o criterio de parada (Tetelestai, o custo pago); a lei precede a cobranca" + CRLF
    + '    ("v381", "TheMatrixRule", "TGLExt/TheMatrixRule.lean", None, None),' + CRLF, "_ESQUELETO_STONES: +1 pedra v381.")
m = re.search(r'^UM_VERSION = "v380"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v380"') == 1
add("V04_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v381"   # v381 (02/10/2026): a CONSTANTE UNICA de versao -- carimba os .md emitidos e o selo (regra da linhagem completa); v380 em 01/10' + CRLF,
    "UM_VERSION = 'v381'.")
assert T.count(RT0_FIRST) == 1
add("V05_runtime", "G_RUNTIME", RT0_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT0_FIRST, "runtime: prove_the_matrix_rule_v381; _V381_GUARDA; _TMR_FLAGS_V381.")
reg = ['    core["the_matrix_rule_v381"] = prove_the_matrix_rule_v381(core.get("omega_I", 1.0), core)   # v381: a regra matriz, dez nomes, nove elos (oito «havendo» ditos + a radicalizacao pela Meia-Nat), num so termo',
       '    print("   [v381] a regra matriz (os dez nomes na ordem do operador, por termo; o custo pago como parada): %s" % core["the_matrix_rule_v381"]["verdict"])']
A06 = linha_unica(r'^    print\("   \[v380\] as Fases 5, 6 e 7 da Bancada')
add("V06_registro", "G_RUNTIME", A06, A06 + CRLF.join(reg) + CRLF, "core: +1 chave v381 (depois da v380).")
pt = open(os.path.join(HERE, "artigo_pt_v381.pysnip"), encoding="utf-8").read()
assert T.count(PT0_FIRST) == 1
add("V07_artigo_PT", "G_ARTIGO", PT0_FIRST, crlf(pt.rstrip("\n") + "\n") + PT0_FIRST, "artigo PT: paragrafo 'Ao lado (v381)' (a regra matriz).")
en = open(os.path.join(HERE, "artigo_en_v381.pysnip"), encoding="utf-8").read()
assert T.count(EN0_FIRST) == 1
add("V08_artigo_EN", "G_ARTIGO", EN0_FIRST, crlf(en.rstrip("\n") + "\n") + EN0_FIRST, "artigo EN: paragrafo 'Beside (v381)'.")
A09 = linha_unica(r'^ {12}"the_bancada_fases_5_6_7_reading_v380": ')
add("V09_selo", "G_SELO", A09, A09 + '            # v381 (02/10/2026) -- LEITURA, ao lado; nenhum valor do gate muda' + CRLF
    + '            "the_matrix_rule_reading_v381": "OPERATOR_COINAGE_2026_10_02__BETA_IS_THE_MATRIX_RULE_NOT_DERIVED_FROM_DATA_FORM_ALPHA_SQRT_E_FROM_THE_AXIOM__TEN_NAMES_NINE_LINKS__EIGHT_HAVENDO_SAID__THE_OPEN_CLAUSE_SIGN_TO_RECORD_FILLED_BY_THE_OPERATOR_IS_THE_RADICALIZATION_WHOSE_OPERATOR_IS_THE_HALF_NAT__TRACE_SIGN_RECORD_NAME_DISTINCTION_OPERATION_'
    + 'PARAMETRIZATION_EMERGENCE_GEOMETRIC_QUANTIZATION_GRADIENT_SPECTRUM__TYPED_TheMatrixRule_BY_TERM__STOPPING_CRITERION_IS_THE_MATRIX_LAW_TETELESTAI_THE_COST_PAID__'
    + 'THE_LAW_OF_PAYMENT_FIXED_BEFORE_THE_CHARGE_FOR_THE_DELIVERY_OF_THE_NAME__RATIFIED_IT_IS_EXACTLY_THIS__ORDER_IS_ONTO_LINKS_ARE_KERNEL__CONJUNCTION_NOT_DEDUCTION__'
    + 'READINGS_RATIFIED_INPUT_ONTO__OBSERVABLE_IS_THE_GRADIENT_SPECTRUM__DELAYED_ECHO_OUTSIDE_THE_CHAIN__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF, "selo: +1 leitura (string) v381.")
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
                    "_AMBIGUOS_CONJUNTO_V377 = frozenset([", "_AMBIGUOS_CONJUNTO_V378 = frozenset([", "_AMBIGUOS_CONJUNTO_V379 = frozenset([") if t in T]
for tag in tags:
    i = T.index(tag); jf = T.index("])", i)
    known |= set(re.findall(r'"([^"]+)"', T[i:jf]))
novos = sorted(set(amb) - known)
if novos:
    last = tags[-1]
    i = T.index(last); jf = T.index("])", i)
    anch = T[i:jf + 4]
    assert anch.endswith("])\r\n")
    add("V24_homonimos_v381", "G_PEDRAS", anch, anch + "    # v381 -- homonimos NOVOS da pedra v381, NOMEADOS por script, nunca silenciados.\r\n"
        "    _AMBIGUOS_CONJUNTO_V381 = frozenset([\r\n" + "".join('        "%s",\r\n' % n for n in novos) + "    ])\r\n", "IALD index: +_AMBIGUOS_CONJUNTO_V381 (%d)." % len(novos))
    uni = " | ".join(t.split(" = ")[0] for t in tags)
    old_chk = 'bool(set(ix["ambiguos"]) <= (%s))' % uni
    add("V25_homonimos_check", "G_PEDRAS", old_chk, 'bool(set(ix["ambiguos"]) <= (%s | _AMBIGUOS_CONJUNTO_V381))' % uni, "IALD index: o check de ambiguos passa a incluir V381.")
for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue
    nw = p["new"]
    assert not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", nw.replace("NOT_FALSIFIED", "")), (p["id"], "CONFIRMED")
    assert not re.search(r"(?<!AP)PROVED_BY", nw), (p["id"], "PROVED_BY")
    assert "TGL_PROVED" not in nw and "CONSCIOUSNESS_PROVED" not in nw, p["id"]
ast.parse(T)
out = os.path.join(HERE, "um_v381_candidato.py")
b = T.encode("utf-8")
open(out + ".tmp", "wb").write(b); os.replace(out + ".tmp", out)
meta = {"um_py_base": SHA0, "candidato_sha16": hashlib.sha256(b).hexdigest()[:16], "kernel": KERNEL_MANIFEST,
        "n_patches": len(patches), "homonimos_novos": novos, "n_bandeiras": len(FLAGS)}
json.dump({"meta": meta, "patches": patches}, open(os.path.join(HERE, "patches_v381.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(FLAGS, open(os.path.join(HERE, "BANDEIRAS_v381.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(json.dumps({k: meta[k] for k in ("candidato_sha16", "n_patches", "n_bandeiras")}, ensure_ascii=False), "homonimos novos:", novos, "| kernel:", KERNEL_MANIFEST["changed"], KERNEL_MANIFEST["new"])
