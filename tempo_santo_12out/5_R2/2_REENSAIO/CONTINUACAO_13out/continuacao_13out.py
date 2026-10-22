# -*- coding: utf-8 -*-
"""continuacao_13out.py -- F1.TEMPO R2, REENSAIO: CONTINUACAO de 13/10/2026 (reensaiador otico, subagente c1).
Nao reensaia: o ensaio com veredito e a tentativa_002 de 12/10 (20:25 local, 1032,6 s depois do FREEZE_R2) e o seu
recibo de 20:28. Esta continuacao (a) confere por script os FREEZE e os hashes do recibo contra o disco; (b) refaz de
forma INDEPENDENTE (codigo proprio, sem importar o runner) os numeros-chave de T9.o'(c) e O-f' nos dois caminhos e os
compara com o RESULTADO_REENSAIO_R2.json; (c) toma a impressao digital do tgl_kernel (so leitura) e grava o recibo.
Escreve SO em 5_R2/2_REENSAIO/CONTINUACAO_13out. beta NUNCA literal: lido dos bytes do um.py (l.5557; conferido com l.95).
Uso: python -B -E -P -X utf8 continuacao_13out.py"""
import hashlib, json, math, os, re, subprocess, sys
from datetime import datetime, timezone
from fractions import Fraction
import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
assert os.path.basename(HERE) == "CONTINUACAO_13out" and os.path.basename(os.path.dirname(HERE)) == "2_REENSAIO"
REENS = os.path.dirname(HERE); R2 = os.path.dirname(REENS); W = os.path.dirname(R2)
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
T0 = datetime.now(timezone.utc).isoformat()


def sha(p):
    b = open(p, "rb").read()
    return hashlib.sha256(b).hexdigest(), len(b)


def wjson(name, obj):
    p = os.path.join(HERE, name)
    assert os.path.abspath(p).startswith(HERE)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)
    return p


# (a) FREEZE e ADENDO congelados
ESP = {
    "FREEZE_R2": (os.path.join(R2, "0_ADENDO", "FREEZE_R2.json"), "0737f608505afdb5122e9c9154a2d99e18d6fe12a84ead9ab890b825e8065de5", 4982),
    "ADENDO_R2.json": (os.path.join(R2, "0_ADENDO", "ADENDO_R2.json"), "b9568befdcc200f8a3983273a11168fd803a006c04338bd22b6da769bfb3e67f", 60427),
    "ADENDO_R2.md": (os.path.join(R2, "0_ADENDO", "ADENDO_R2.md"), "ab13c0f27a7f4cf5e0a568db2fb0f7c5f32fc813a1d735fec9ddd72db38da7e4", 42114),
    "FREEZE_R1": (os.path.join(W, "1_PREREGISTRO", "FREEZE.json"), "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b", 5986),
    "tolerancia_uniforme_r2.py (normativa)": (os.path.join(R2, "0_ADENDO", "scripts", "tolerancia_uniforme_r2.py"), "7d68e42a9eec62e1655305aa98c810ad26b0e667385ad533a0ff1660ec920498", 15456),
}
freeze = {}
for k, (p, h, n) in ESP.items():
    hh, nn = sha(p)
    freeze[k] = {"sha256": hh, "bytes": nn, "ok": hh == h and nn == n}
freeze_ok = all(v["ok"] for v in freeze.values())
fz = json.load(open(ESP["FREEZE_R2"][0], encoding="utf-8"))
congelado = fz["congelado_em_utc"]

# recibo de 12/10 contra o disco
recibo_p = os.path.join(REENS, "RECIBO_REENSAIO_R2.json")
rec = json.load(open(recibo_p, encoding="utf-8"))
man = rec["arquivos_de_2_REENSAIO"]
div = []
for rel, info in man.items():
    p = os.path.join(REENS, rel.replace("/", os.sep))
    if not os.path.exists(p):
        div.append({"arquivo": rel, "problema": "ausente"})
        continue
    hh, nn = sha(p)
    if hh != info["sha256"] or nn != info["bytes"]:
        div.append({"arquivo": rel, "problema": "hash/bytes divergem"})
disco = []
for root, dirs, files in os.walk(REENS):
    for f in files:
        disco.append(os.path.relpath(os.path.join(root, f), REENS).replace(os.sep, "/"))
orfaos = [d for d in disco if d not in man and d != "RECIBO_REENSAIO_R2.json" and not d.startswith("CONTINUACAO_13out/")]
tool = [d for d in disco if any(s in d.lower() for s in ("toolchain", ".lake", "cache", "__pycache__"))]
res_p = os.path.join(REENS, "RESULTADO_REENSAIO_R2.json")
res = json.load(open(res_p, encoding="utf-8"))
ensaio_inicio = res["inicio_utc"]
posterior = datetime.fromisoformat(ensaio_inicio) > datetime.fromisoformat(congelado)

# (b) recomputo independente
raw = open(UM, "rb").read()
um_sha = hashlib.sha256(raw).hexdigest()
lines = raw.split(b"\n")
l95 = lines[94].decode("utf-8", "replace")
l5557 = lines[5556].decode("utf-8", "replace")
lit5557 = re.search(r"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l5557).group(1)
lit95 = re.search(r"SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", l95).group(1)
alpha = float(lit5557)
beta = alpha * 1.0 * math.sqrt(math.e)
eps = 2.0 ** -52
th = math.asin(math.sqrt(beta))
c, s = math.cos(th), math.sin(th)
a, b = c * c, s * s
T = np.array([[a, b], [b, a]])
lam = 1.0 - 2.0 * beta
R = np.full((2, 2), 0.5)
I = np.eye(2)
dT = Fraction(a) + Fraction(b) - 1
tau_T = lambda k: k * (abs(float(dT)) / 2 + eps) + 2 * eps
mx = 0; kmx = 0; rmx = 0; krmx = 0; fora = 0; first = None; k13 = None
for k in range(1, 10001):
    d = float(np.max(np.abs(np.linalg.matrix_power(T, k) - (R + lam ** k * (I - R)))))
    t = tau_T(k)
    if d > mx:
        mx, kmx = d, k
    if d / t > rmx:
        rmx, krmx = d / t, k
    if d > t:
        fora += 1
        if first is None:
            first = k
    if k13 is None and d > 1e-13:
        k13 = k
t9f = {"representacao": "E2: T = |Smat(theta_M)|^2, theta_M = arcsin(sqrt(beta)); numpy.linalg.matrix_power; ref R + lam^k (I - R)",
       "T_hex": [[T[0, 0].hex(), T[0, 1].hex()], [T[1, 0].hex(), T[1, 1].hex()]],
       "delta_T_exato_fraction": str(dT), "delta_T": float(dT), "delta_T_em_2^-53": float(dT * 2 ** 53),
       "max_k<=1e4": mx, "k_do_max": kmx, "tau_T(1e4)": tau_T(10000), "max_razao": rmx, "k_da_max_razao": krmx,
       "n_k_fora_de_tau": fora, "primeiro_k_fora": first, "PASSA_sob_tau_T": fora == 0,
       "R1_criterio_1e-13": {"primeiro_k_acima": k13, "FALHA_R1_reproduzida": mx > 1e-13}}
mp.mp.dps = 200
al = mp.mpf(lit5557)
be = al * mp.sqrt(mp.e)
thm = mp.asin(mp.sqrt(be))
cm, sm = mp.cos(thm), mp.sin(thm)
Tm = mp.matrix([[cm * cm, sm * sm], [sm * sm, cm * cm]])
lamm = 1 - 2 * be
Rm = mp.matrix([[mp.mpf("0.5")] * 2] * 2)
Im = mp.eye(2)
Pk = mp.eye(2)
mxe = mp.mpf(0); kme = 0
for k in range(1, 10001):
    Pk = Pk * Tm
    ref = Rm + (lamm ** k) * (Im - Rm)
    d = max(abs(Pk[i, j] - ref[i, j]) for i in range(2) for j in range(2))
    if d > mxe:
        mxe, kme = d, k
t9e = {"dps": 200, "metodo": "multiplicacao repetida; beta do literal como string exata; ref R + lam^k (I - R)",
       "max_desvio": mp.nstr(mxe, 8), "k_do_max": kme, "PASSA_1e-150_absoluta": bool(mxe < mp.mpf("1e-150"))}
c1, s1 = math.cosh(1.0), math.sinh(1.0)
dB = float(abs((mp.mpf(c1) - mp.mpf(s1)) - mp.exp(-1)) / mp.exp(-1))
mB = (math.exp(2.0) + 1.0) / 2.0          # a formula da normativa: (e^{2s} + 1)/2 com s = 1, via math.exp(2*s)
mB_variante_e2 = (math.e ** 2 + 1) / 2    # variante math.e**2: difere 1 ulp (4.194528049465324 vs ...325); registrada, nao usada
tau_B = lambda k: k * (dB + mB * eps) + 3 * eps
x, y = 1.0, -1.0
mxr = 0; kr = 0; foraB = 0
for k in range(1, 11):
    x, y = c1 * x + s1 * y, s1 * x + c1 * y
    nrm = math.hypot(x, y)
    ref = math.sqrt(2.0) * math.exp(-k)
    rel = abs(nrm - ref) / ref
    if rel > mxr:
        mxr, kr = rel, k
    if rel > tau_B(k):
        foraB += 1
B = np.array([[c1, s1], [s1, c1]])
firstk = None; rel10 = None
for k in range(1, 11):
    w = np.linalg.matrix_power(B, k) @ np.array([1.0, -1.0])
    rel = abs(float(np.linalg.norm(w)) - math.sqrt(2) * math.exp(-k)) / (math.sqrt(2) * math.exp(-k))
    if rel > tau_B(k) and firstk is None:
        firstk = k
    if k == 10:
        rel10 = rel
off = {"representacao": "E4: orbita v <- B(1) v iterada em escalar IEEE do Python (c1 x + s1 y, s1 x + c1 y); norma hypot",
       "c1_hex": c1.hex(), "s1_hex": s1.hex(), "delta_B_rel": dB, "m_B": mB, "m_B_variante_math.e**2_(1_ulp,_nao_usada)": mB_variante_e2,
       "max_rel_k<=10": mxr, "k_do_max": kr, "tau_B(10)": tau_B(10), "n_k_fora": foraB, "PASSA_sob_tau_B": foraB == 0,
       "det_B1_menos_1": c1 * c1 - s1 * s1 - 1,
       "C-UNIF-a_matrix_power": {"primeiro_k_fora_de_tau_B": firstk, "rel_k=10": rel10, "FALHA_como_registrado": firstk is not None}}
fm = mp.cosh(1) - mp.sinh(1)
mxo = mp.mpf(0); kmo = 0
for k in range(1, 101):
    rel = abs(fm ** k - mp.exp(-k)) / mp.exp(-k)
    if rel > mxo:
        mxo, kmo = rel, k
ofe = {"dps": 200, "metodo": "(cosh 1 - sinh 1)^k contra e^-k, relativo, k = 1..100", "max_rel": mp.nstr(mxo, 8), "k_do_max": kmo,
       "PASSA_1e-150_relativa": bool(mxo < mp.mpf("1e-150"))}

# comparacao com o runner (RESULTADO_REENSAIO_R2.json)
rT = res["T9.o'(c)"]
rO = res["O-f'"]
por_k = rO["float64_E4"]["por_k"]           # o runner guarda k = 1..100; O2 so exige k <= 10 (k = 11..100 e informativo)
tol_frozen = json.load(open(os.path.join(R2, "0_ADENDO", "saidas", "TOLERANCIA_UNIFORME_R2.json"), encoding="utf-8"))
pB_frozen = tol_frozen["O-f'"]["parametros"]
pT_frozen = tol_frozen["T9.o'(c)"]["parametros"]
cmp_ = {
    "parametros_congelados_iguais": {"delta_T": float(dT) == pT_frozen["delta_T"], "delta_B_rel": dB == pB_frozen["delta_B_rel"], "m_B": mB == pB_frozen["m"],
                                     "tau_B_rel(10)": tau_B(10) == tol_frozen["O-f'"]["predicao"]["tau_B_rel(10)"],
                                     "tau_T(1e4)": tau_T(10000) == tol_frozen["T9.o'(c)"]["predicao"]["tau_T(1e4)"]},
    "beta_runtime_igual": beta == res["beta"].get("beta", res["beta"].get("beta_runtime")),
    "T9_float_max_igual_bit_a_bit": mx == rT["float64_E2"]["max_k<=1e4"],
    "T9_float_tau_T_1e4_igual": tau_T(10000) == rT["float64_E2"]["tau_T(1e4)"],
    "T9_float_max_razao_igual": rmx == rT["float64_E2"]["max_razao_medido/tau"],
    "T9_delta_T_fraction_igual": str(dT) == rT["float64_E2"]["delta_T_exato_fraction"],
    "T9_exato_ambos_<=1e-150": t9e["PASSA_1e-150_absoluta"],
    "Of_float_max_rel_k<=10_igual_bit_a_bit": mxr == max(por_k["k=%d" % k]["rel"] for k in range(1, 11)) == rO["float64_E4"]["max_rel_k<=10"],
    "Of_por_k_rel_k<=10_todos_iguais_bit_a_bit": None,  # preenchido abaixo
    "Of_tau_B_10_igual": tau_B(10) == por_k["k=10"]["tau_B_rel"],
    "C_UNIF_a_primeiro_k_fora_igual_3": firstk == 3,
    "nota": "o recomputo e codigo proprio; igualdade bit a bit nas medidas float e o esperado na mesma maquina; os maximos exatos a 200 digitos diferem na mantissa ~1e-198 pela ordem das operacoes e ficam ambos ~48 ordens abaixo de 1e-150",
    "errata_da_tentativa_001_desta_continuacao": "a primeira rodada deste script (preservada em tentativa_001_comparacao_defeituosa/) marcou dois sinalizadores falsos por defeito da COMPARACAO, nao do runner: (1) tomou o maximo de por_k sobre k = 1..100 (O2 so exige k <= 10); (2) avaliou m_B = (math.e**2 + 1)/2 = 4.194528049465324, 1 ulp abaixo da normativa (math.exp(2*s), 4.194528049465325), o que moveu tau_B(10) em 2e-30; o veredito nao se altera em nenhum dos dois casos",
}
# E4 por k, k <= 10, bit a bit
x, y = 1.0, -1.0
iguais = []
for k in range(1, 11):
    x, y = c1 * x + s1 * y, s1 * x + c1 * y
    rel = abs(math.hypot(x, y) - math.sqrt(2.0) * math.exp(-k)) / (math.sqrt(2.0) * math.exp(-k))
    iguais.append(rel == por_k["k=%d" % k]["rel"])
cmp_["Of_por_k_rel_k<=10_todos_iguais_bit_a_bit"] = all(iguais)
runner_vals = {"T9_float_max": rT["float64_E2"]["max_k<=1e4"], "T9_tau_T_1e4": rT["float64_E2"]["tau_T(1e4)"],
               "T9_max_razao": rT["float64_E2"]["max_razao_medido/tau"],
               "Of_float_max_rel_k<=10": rO["float64_E4"]["max_rel_k<=10"], "Of_tau_B_rel_10": rO["float64_E4"]["tau_B_rel(10)"],
               "Of_exato_max_rel": rO["exato_mpmath_200"].get("max_rel", rO["exato_mpmath_200"]),
               "T9_exato_max_desvio": rT["exato_mpmath_200"]["max_desvio_k<=10000"],
               "vereditos": res["quadro_ao_lado"]}
recheck = {"documento": "RECHECK INDEPENDENTE (continuacao 13/10) de T9.o'(c) e O-f' nos dois caminhos; codigo proprio, sem importar o runner",
           "estatuto": "[REAL - medido aqui, modelo sintetico]; beta [DERIVED: lido nos bytes do um.py (l.5557 == l.95) e calculado em runtime]; tolerancias [INPUT da gerencia - ADENDO R2 congelado]; PASSA = validade na face testada, nao creditacao; nada move o gate",
           "um_py": {"sha256": um_sha, "bytes": len(raw), "executado": False, "l95": l95.strip(), "l5557": l5557.strip(),
                     "literal_l5557": lit5557, "literal_l95": lit95, "iguais": float(lit5557) == float(lit95)},
           "beta": {"valor": beta, "hex": beta.hex(), "expressao": "alpha * ONE * sqrt(e) em runtime"},
           "T9.o'(c)_float64_E2": t9f, "T9.o'(c)_exato": t9e, "O-f'_float64_E4": off, "O-f'_exato": ofe,
           "comparacao_com_o_runner_R2": cmp_, "valores_do_runner": runner_vals,
           "errata_do_proprio_recheck": "num primeiro rascunho (scratchpad, nao gravado aqui) este reensaiador somou a + b em float e obteve delta_T = eps = 2^-52; o ADENDO define delta_T como a diferenca EXATA (Fraction) da matriz guardada, 17/2^57 = 1,0625 * 2^-53; corrigido aqui; o erro era de leitura deste reensaiador, nao do runner",
           "ambiente": {"python": sys.version, "numpy": np.__version__, "mpmath": mp.__version__}}
recheck_p = wjson("RECHECK_INDEPENDENTE_13out.json", recheck)

# (c) impressao digital DEPOIS (so leitura do kernel) e recibo
fp_script = os.path.join(REENS, "scripts", "fingerprint_kernel.py")
fp_depois_p = os.path.join(HERE, "FINGERPRINT_CONTINUACAO_DEPOIS.json")
subprocess.run([sys.executable, "-I", "-X", "utf8", fp_script, fp_depois_p], check=True, capture_output=True)
fa = json.load(open(os.path.join(HERE, "FINGERPRINT_CONTINUACAO_ANTES.json"), encoding="utf-8"))
fd = json.load(open(fp_depois_p, encoding="utf-8"))
META = "b1b47447ac30f7c74ad33b200bd2a3025987650a13593038ddc7465de6fab21f"
SRC = "911cb40b9de1a8bb3bdd0789d5af3f718fa98ee9f0b1f5fcd6ffa4abb616bd3d"
fp_ok = fa["meta_sha256"] == fd["meta_sha256"] == META and fa["src_sha256"] == fd["src_sha256"] == SRC

recibo = {
    "documento": "RECIBO da CONTINUACAO (13/10/2026) do reensaio R2 da face otica F1.TEMPO - reensaiador otico, subagente do workflow posto-e-tempo da gerencia c1",
    "inicio_utc": T0, "fim_utc": datetime.now(timezone.utc).isoformat(),
    "o_que_e": "continuacao administrativa: o ensaio com veredito (tentativa_002, 12/10 20:25 local) e o seu recibo (20:28) ja estavam gravados; esta continuacao NAO reensaia, NAO sobrescreve e NAO cria nova tentativa; confere, recomputa de forma independente e deixa o rastro ao lado",
    "freeze_e_adendo_conferidos_hoje": freeze, "freeze_todos_ok": freeze_ok, "FREEZE_R2_congelado_em_utc": congelado,
    "ensaio_com_veredito": {"pasta": "tentativas/tentativa_002_ensaio (copiado para a raiz de 2_REENSAIO)", "inicio_utc": ensaio_inicio,
                            "posterior_ao_FREEZE_R2 (V2)": posterior,
                            "RESULTADO_REENSAIO_R2.json": dict(zip(("sha256", "bytes"), sha(res_p))),
                            "reensaio_r2.log": dict(zip(("sha256", "bytes"), sha(os.path.join(REENS, "reensaio_r2.log")))),
                            "RECIBO_REENSAIO_R2.json (12/10)": dict(zip(("sha256", "bytes"), sha(recibo_p))),
                            "valido_no_resultado": res["valido"], "motivos_de_INVALIDO": res["motivos_de_INVALIDO"]},
    "recibo_de_12_10_contra_o_disco": {"arquivos_no_manifesto": len(man), "divergentes_ou_ausentes": div,
                                       "orfaos_fora_do_manifesto (excluida esta pasta)": orfaos, "toolchain_lake_cache_na_pasta": tool},
    "vereditos_R2_lidos_do_resultado": res["quadro_ao_lado"],
    "leitura_pela_tabela_pre_fixada_do_ADENDO (parte_b.o_que_cada_resultado_significa)": {
        "T9.o'(c)": "exato PASSA e float PASSA => T9.o'(c) = PASSA; a FALHA R1 fica registrada ao lado com o diagnostico confirmado pelo numero (piso de representacao k|delta|/2 + arredondamento <= k*eps)",
        "O-f'": "exato PASSA e float E4 PASSA e C-UNIF-a FALHA como registrado (k = 3) => O-f' = PASSA; a tolerancia nao virou cheque em branco",
        "a_leitura_FALHA_R1_=_piso_de_representacao_confirma_se_pelo_exato": True,
        "porque": "o caminho exato a 200 digitos devolve a identidade T^k = R + lam^k (I - R) a ~1e-198 em todo k <= 1e4 (o kernel a prova; o numero so a confere); o mesmo float E2 da R1 (mesma matriz, mesmo max 6.518119377574294e-13 em k = 1e4, mesmo primeiro k acima de 1e-13 = 1529) fica dentro de k(|delta_T|/2 + eps) + 2eps com razao maxima 0,4169 (em k = 6); logo o 6,5e-13 da R1 e representacao (soma de coluna 1 + 17/2^57) e arredondamento, nao contraexemplo",
        "nao_e": "nao e creditacao; nao ha veredito global; nada move o gate; beta na natureza a 5 sigma nao e tocado; T2 segue CITADA; o veredito T9' (afirmacao) pela regra A1 depende ainda da pedra corrigida e reauditada (outro ator)"},
    "recheck_independente": {"arquivo": "RECHECK_INDEPENDENTE_13out.json", **dict(zip(("sha256", "bytes"), sha(recheck_p))), "comparacao_com_o_runner": cmp_},
    "impressao_digital_tgl_kernel": {"antes": {"meta": fa["meta_sha256"], "src": fa["src_sha256"], "taken_at": fa["taken_at"]},
                                     "depois": {"meta": fd["meta_sha256"], "src": fd["src_sha256"], "taken_at": fd["taken_at"]},
                                     "iguais_e_iguais_a_R1_e_ao_FREEZE_R2": fp_ok},
    "lean": "nenhum (reensaio otico; nenhum toolchain, .lake ou cache copiado; nada a apagar)",
    "um_py": {"sha256": um_sha, "executado": False, "beta_estatuto": "[DERIVED: lido nos bytes (l.5557 == l.95) e calculado em runtime; nunca literal; nao e medida]"},
    "observado_sem_atribuir_autoria": "5_R2/1_PEDRA existe (pasta irma, outro ator: pedra corrigida E5 em curso); nao tocada; 2_OPTICO/rodada_2 e 3_KERNEL/rodada_2 seguem como tentativas preservadas (V2)",
    "acom": "sem referencia propria; nenhum init e nenhuma transition (atos da gerencia); nenhuma projecao nova nesta continuacao",
    "nada_escrito_fora": "escrito SO em 5_R2/2_REENSAIO/CONTINUACAO_13out (esta pasta). Nada no quadro, no mapa, na memoria, no tunel, no Nos, no kernel do Nos, na Bancada, no site ou no git. O um.py nao foi executado. Nenhum Lean rodado. Nenhum dado observado; nenhum provedor remoto; nenhuma chamada paga. Rascunhos de recomputo no scratchpad da sessao (fora do acervo), reproduzidos aqui pelo script continuacao_13out.py",
    "script": {"arquivo": "continuacao_13out.py", **dict(zip(("sha256", "bytes"), sha(os.path.abspath(__file__))))},
}
p = wjson("RECIBO_CONTINUACAO_13out.json", recibo)
print(json.dumps({"freeze_ok": freeze_ok, "posterior": posterior, "divergentes": div, "orfaos": orfaos, "tool": tool, "cmp": cmp_, "fp_ok": fp_ok,
                  "t9f": {"max": mx, "tau": tau_T(10000), "razao": rmx, "k": krmx, "fora": fora}, "t9e": t9e,
                  "off": {"max_rel": mxr, "k": kr, "tau": tau_B(10), "fora": foraB, "cunifa": firstk},
                  "ofe": ofe, "recibo": p, "recibo_sha": sha(p)}, ensure_ascii=False, indent=1))
