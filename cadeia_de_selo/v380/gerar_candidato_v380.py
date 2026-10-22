# -*- coding: utf-8 -*-
"""gerar_candidato_v380.py -- gera o um.py CANDIDATO v380 a partir da v379 SELADA (NUNCA escreve o canonico). Molde: gerar_candidato_v379.py, SEM kernel novo.
Ordens do operador (01/10/2026): o SH0ES na Bancada; «o teste da transformada radical com as ondas gravitacionais e ecos»; «todo esse banco de dados novo (gweco) ... ja o
vincule a bancada»; «estude tudo que eu ja fiz e ja escrevemos e resolva os problemas que faltam».
(1) KERNEL: INALTERADO (conferido: nenhum arquivo .lean muda, nenhum entra). (2) PATCHES (count(old) == 1): UM_VERSION v380; runtime (1 modulo: prove_bancada_fases_5_6_7_v380);
registro; artigo PT/EN («Ao lado (v380)»); selo (uma leitura, string); selo EV-06 (as chaves da conjunta V3 e do D1 V3 real, auditoria 28/09). Sete patches; nenhuma chave antiga e tocada."""
import ast, hashlib, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
KS = os.path.join(os.path.dirname(HERE), "v376", "kernel_src")
CRLF = "\r\n"
V9 = os.path.join(os.path.dirname(HERE), "v379")
AP = json.load(open(sorted(os.path.join(V9, f) for f in os.listdir(V9) if f.startswith("APLICADO_AO_CANONICO_"))[-1], encoding="utf-8"))
SHA0 = AP["um_py_novo"]["sha16"]
raw = open(UM, "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico nao e a v379 selada"
T = raw.decode("utf-8")
RT = open(os.path.join(HERE, "v380_runtime.py"), encoding="utf-8").read()
RT9_FIRST = open(os.path.join(V9, "v379_runtime.py"), encoding="utf-8").read().splitlines()[0]
PT9_FIRST = open(os.path.join(V9, "artigo_pt_v379.pysnip"), encoding="utf-8").read().splitlines()[0]
EN9_FIRST = open(os.path.join(V9, "artigo_en_v379.pysnip"), encoding="utf-8").read().splitlines()[0]

# ---------- (1) o kernel: INALTERADO ----------
lines = T.splitlines(keepends=True)
i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]
assert len(i0) == 1
i0 = i0[0]; j = i0 + 1
while lines[j].rstrip("\r\n") != "}":
    j += 1
blk = "".join(lines[i0:j + 1])
old_d = ast.literal_eval(blk.split("=", 1)[1].strip())
cand = {}
for top in ("TGL", "TGLExt"):
    for root, dirs, files in os.walk(os.path.join(KS, top)):
        for f in files:
            if f.endswith(".lean"):
                p = os.path.join(root, f); rel = os.path.relpath(p, KS).replace("\\", "/")
                cand[rel] = open(p, "r", encoding="utf-8", newline="").read()
changed = sorted(k for k in old_d if k in cand and cand[k] != old_d[k])
new = sorted(k for k in cand if k not in old_d)
assert changed == [] and new == [], ("o kernel do sandbox difere do embutido -- a v380 e SEM kernel novo", changed, new)
KERNEL_MANIFEST = {"changed": {}, "new": {}, "n_entries": len(old_d), "unchanged": True}

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


m = re.search(r'^UM_VERSION = "v379"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v379"') == 1
add("V04_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v380"   # v380 (01/10/2026): a CONSTANTE UNICA de versao -- carimba os .md emitidos e o selo (regra da linhagem completa); v379 em 01/10 (manha)' + CRLF,
    "UM_VERSION = 'v380'.")
assert T.count(RT9_FIRST) == 1
assert "def prove_bancada_fases_5_6_7_v380(" in RT and "prove_bancada_fases_5_6_7_v380" not in T
add("V05_runtime", "G_RUNTIME", RT9_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT9_FIRST, "runtime: prove_bancada_fases_5_6_7_v380 (leitura por hash das Fases 5, 6 (V3, V4, diag), 7, do banco e das erratas ao lado).")
reg = ['    core["bancada_fases_5_6_7_v380"] = prove_bancada_fases_5_6_7_v380(core.get("omega_I", 1.0), core)   # v380: as Fases 5, 6 e 7 da Bancada, o banco de GW e as erratas ao lado, por hash',
       '    print("   [v380] as Fases 5, 6 e 7 da Bancada (SH0ES; ECO V3, V4 e V5; cronometros com covariancia), o banco de GW e 6+1+1 erratas ao lado, por hash: %s" % core["bancada_fases_5_6_7_v380"]["verdict"])']
A06 = '    print("   [v379] a Razao Elementar (E = C x I x K > 0 = beta, por termo): %s" % core["the_elementary_reason_v379"]["verdict"])' + CRLF
add("V06_registro", "G_RUNTIME", A06, A06 + CRLF.join(reg) + CRLF, "core: +1 chave v380 (depois da v379).")
pt = open(os.path.join(HERE, "artigo_pt_v380.pysnip"), encoding="utf-8").read()
assert T.count(PT9_FIRST) == 1
add("V07_artigo_PT", "G_ARTIGO", PT9_FIRST, crlf(pt.rstrip("\n") + "\n") + PT9_FIRST, "artigo PT: paragrafo 'Ao lado (v380)'.")
en = open(os.path.join(HERE, "artigo_en_v380.pysnip"), encoding="utf-8").read()
assert T.count(EN9_FIRST) == 1
add("V08_artigo_EN", "G_ARTIGO", EN9_FIRST, crlf(en.rstrip("\n") + "\n") + EN9_FIRST, "artigo EN: paragrafo 'Beside (v380)'.")
A09 = linha_unica(r'^ {12}"the_elementary_reason_reading_v379": ')
add("V09_selo", "G_SELO", A09, A09 + '            # v380 (01/10/2026) -- LEITURA, ao lado; nenhum valor do gate muda' + CRLF
    + '            "the_bancada_fases_5_6_7_reading_v380": "OPERATOR_ORDERS_2026_10_01__SH0ES_IN_THE_BENCH__ECHO_V3_THE_RADICAL_TRANSFORM_244_BBH_O1_O4_THREE_READINGS_TWO_DELAY_LAWS__'
    + 'KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW_WITH_BLIND_O4_SUBSAMPLE__MAY_INCONCLUSIVE_SYSTEMATICS__AMENDMENT_V4_NOT_BLIND_STATED__AMENDMENT_V5_DEC2025_ARCHIVE_LAW_DECLARED_BLIND_TO_THE_NEW_DELAY_ONLY_RADICAL_PAIR_FALSIFIED_DOC_PAIR_UNDERPOWERED__TWO_PIPELINE_DEVIATIONS_STATED__CC_COVARIANCE_MORESCO2020_WEAKENS_PHASES_4_5_READINGS__'
    + 'GW_BANK_RESIDENT_IN_THE_BENCH__ERRATA_BESIDE_6_AUDIT_PLUS_V378_1_PLUS_NOTE_1__PAIR_FALSIFIED_NOT_THE_THEORY__DELAY_LAW_AND_GRAVITON_WEIGHT_ARE_THE_OPERATORS_TO_DECIDE__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF,
    "selo: +1 leitura (string) v380.")
A10 = '            "joint_coincidence_result_verdict": (core.get("joint_coincidence_result") or {}).get("verdict"),  # v352: a medida; nao gateia' + CRLF
add("V10_selo_EV06", "G_SELO", A10, A10
    + '            "joint_coincidence_result_v3_verdict": (core.get("joint_coincidence_result_v3") or {}).get("verdict"),  # v380 (auditoria 28/09, EV-06): a conjunta V3 no selo; nao gateia' + CRLF
    + '            "d1_camb_v3_real_v366_verdict": (core.get("d1_camb_v3_real_v366") or {}).get("verdict"),  # v380 (EV-06): o D1 V3 real (v366) no selo; nao gateia' + CRLF,
    "selo: +2 chaves (conjunta V3; D1 V3 real) -- EV-06.")
for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue
    nw = p["new"]
    assert not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", nw.replace("NOT_FALSIFIED", "")), (p["id"], "CONFIRMED")
    assert not re.search(r"(?<!AP)PROVED_BY", nw), (p["id"], "PROVED_BY")
    assert "TGL_PROVED" not in nw and "CONSCIOUSNESS_PROVED" not in nw, p["id"]
ast.parse(T)
out = os.path.join(HERE, "um_v380_candidato.py")
b = T.encode("utf-8")
open(out + ".tmp", "wb").write(b); os.replace(out + ".tmp", out)
meta = {"um_py_base": SHA0, "candidato_sha16": hashlib.sha256(b).hexdigest()[:16], "kernel": KERNEL_MANIFEST, "n_patches": len(patches), "homonimos_novos": [], "n_bandeiras": 0}
json.dump({"meta": meta, "patches": patches}, open(os.path.join(HERE, "patches_v380.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump([], open(os.path.join(HERE, "BANDEIRAS_v380.json"), "w", encoding="utf-8"))
print(json.dumps({k: meta[k] for k in ("candidato_sha16", "n_patches", "n_bandeiras")}, ensure_ascii=False), "kernel inalterado:", KERNEL_MANIFEST["unchanged"])
