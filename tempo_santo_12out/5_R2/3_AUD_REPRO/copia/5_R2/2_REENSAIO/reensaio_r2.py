# -*- coding: utf-8 -*-
r"""
reensaio_r2.py -- F1.TEMPO (trilha TEMPO; gerencia c1; programa IALD / TGL): REENSAIO R2 da face otica,
SO de O-f e T9.o(c), sob o ADENDO UNIFORME congelado (5_R2/0_ADENDO/FREEZE_R2.json).
Papel: reensaiador otico da R2 (subagente do workflow posto-e-tempo da gerencia c1).

O que faz (e so isto):
  (i)  caminho EXATO: mpmath mp.dps = 200 (conferencia cruzada com `decimal` prec = 200: C-UNIF-d); beta do LITERAL
       da l.5557 do um.py (string exata) vezes sqrt(e); T^k por MULTIPLICACAO REPETIDA; tolerancia 1e-150 (absoluta em
       T9.o'(c), relativa em O-f'); controle C-UNIF-c (dps = 20 TEM de falhar).
  (ii) caminho FLOAT64: a mesma representacao E2 da R1 (T = |Smat(theta_M)|^2 guardada) com numpy.linalg.matrix_power
       e a orbita escalar IEEE E4 do boost, sob tau(k) = S_k*[k*(w*|delta| + m*eps) + c*eps] com os parametros da
       implementacao de referencia NORMATIVA (scripts/tolerancia_uniforme_r2.py, importada, nunca redigitada);
       controles C-UNIF-a (matrix_power do boost TEM de falhar tau_B) e C-UNIF-b (ALT e EST passam a mesma tau_T).
  V4:  se a reproducao da R1 pelo runner da R1 copiado (2_OPTICO/RESULTADO_OPTICO.json desta pasta) existir, compara
       criterio a criterio com a R1 (fora dos dois testes tudo tem de reproduzir) e emite O3 (T9.o') e O4 (T4.o').
Regras: nada se escreve fora de 5_R2/2_REENSAIO; o um.py NAO e executado (bytes lidos pelo leitor do runner da R1);
nenhum dado observado; nenhum provedor remoto; nenhum Lean; beta NUNCA literal (lido e calculado em runtime; estatuto
[DERIVED: lido e calculado]); tentativas preservadas (tentativas/tentativa_NNN_<modo>/); a R1 fica intacta.
Uso:  python -B -E -P -X utf8 reensaio_r2.py            (ensaio: grava tentativa nova e copia o resultado para a raiz)
      python -B -E -P -X utf8 reensaio_r2.py --infra    (so conferencias, beta, parametros; nenhum teste)
"""
import hashlib
import json
import math
import os
import platform
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction

import numpy as np
import mpmath
from mpmath import mp, mpf

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != "2_REENSAIO":
    sys.stderr.write("RECUSA: o reensaio so roda dentro de 5_R2/2_REENSAIO\n")
    sys.exit(2)
W = os.path.dirname(os.path.dirname(HERE))                      # ...\tempo_santo_12out
ADENDO = os.path.join(W, "5_R2", "0_ADENDO")
R1_OPT = os.path.join(W, "2_OPTICO")
R1_RES = os.path.join(R1_OPT, "RESULTADO_OPTICO.json")
R1_DIAG = os.path.join(R1_OPT, "diagnostico", "DIAGNOSTICO_T9c.json")
R1_ACH = os.path.join(R1_OPT, "ACHADOS_FORA_DO_PREREGISTRO.json")
TOL_FROZEN = os.path.join(ADENDO, "saidas", "TOLERANCIA_UNIFORME_R2.json")
BETA_FROZEN = os.path.join(ADENDO, "saidas", "BETA_RUNTIME_R2.json")
FREEZE_R2 = os.path.join(ADENDO, "FREEZE_R2.json")
FREEZE_R1 = os.path.join(W, "1_PREREGISTRO", "FREEZE.json")
V4_RES = os.path.join(HERE, "2_OPTICO", "RESULTADO_OPTICO.json")

# esperado (copiado do enunciado da tarefa / FREEZE_R2; a conferencia e contra os bytes)
EXP_FREEZE_R2 = ("0737f608505afdb5122e9c9154a2d99e18d6fe12a84ead9ab890b825e8065de5", 4982)
EXP_FREEZE_R1 = ("6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b", 5986)
EXP_KERNEL = {"meta": "b1b47447ac30f7c74ad33b200bd2a3025987650a13593038ddc7465de6fab21f",
              "src": "911cb40b9de1a8bb3bdd0789d5af3f718fa98ee9f0b1f5fcd6ffa4abb616bd3d"}
SAMPLE_T = [1, 10, 100, 1000, 1529, 2000, 4096, 5000, 8192, 10000]
SAMPLE_D = [1, 10, 100, 1000, 10000]

sys.path.insert(0, os.path.join(HERE, "scripts"))
import tolerancia_uniforme_r2 as TU          # noqa: E402  a implementacao de referencia NORMATIVA (copia byte a byte)
sys.path.insert(0, os.path.join(HERE, "2_OPTICO"))
import run_optico as RO                      # noqa: E402  o runner da R1 (copia byte a byte; so funcoes)


# ----------------------------------------------------------------------------- utilidades
class Log:
    def __init__(self):
        self.fh = None

    def open(self, path):
        self.fh = open(path, "a", encoding="utf-8", newline="\n")

    def __call__(self, msg):
        line = time.strftime("%Y-%m-%d %H:%M:%S") + "  " + msg
        print(line, flush=True)
        if self.fh:
            self.fh.write(line + "\n")
            self.fh.flush()

    def close(self):
        if self.fh:
            self.fh.close()
            self.fh = None


LOG = Log()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as fh:
        while True:
            c = fh.read(1 << 22)
            if not c:
                break
            h.update(c)
            n += len(c)
    return h.hexdigest(), n


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (int, np.integer)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        f = float(o)
        return f if math.isfinite(f) else ("inf" if f > 0 else ("-inf" if f < 0 else "nan"))
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, mpmath.mpf):
        return mpmath.nstr(o, 25)
    if isinstance(o, (Decimal, Fraction)):
        return str(o)
    return o


def write_json_atomic(path, obj):
    if os.path.commonpath([os.path.abspath(path), HERE]) != HERE:
        raise RuntimeError("escrita fora de 5_R2/2_REENSAIO recusada: " + path)
    data = (json.dumps(jsonable(obj), ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    if os.path.getsize(tmp) != len(data):
        raise RuntimeError("tamanho do temporario nao confere: " + tmp)
    os.replace(tmp, path)
    return sha256_bytes(data), len(data)


def write_text_atomic(path, text):
    if os.path.commonpath([os.path.abspath(path), HERE]) != HERE:
        raise RuntimeError("escrita fora de 5_R2/2_REENSAIO recusada: " + path)
    data = text.encode("utf-8")
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)
    return sha256_bytes(data), len(data)


def copy_bytes_atomic(src, dst):
    if os.path.commonpath([os.path.abspath(dst), HERE]) != HERE:
        raise RuntimeError("escrita fora de 5_R2/2_REENSAIO recusada: " + dst)
    data = open(src, "rb").read()
    tmp = dst + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    if os.path.getsize(tmp) != len(data):
        raise RuntimeError("tamanho do temporario nao confere: " + tmp)
    os.replace(tmp, dst)
    return sha256_bytes(data), len(data)


def new_attempt_dir(mode):
    base = os.path.join(HERE, "tentativas")
    os.makedirs(base, exist_ok=True)
    nums = [int(m.group(1)) for d in os.listdir(base) for m in [re.match(r"^tentativa_(\d{3})_", d)] if m]
    n = 1 + max(nums or [0])
    path = os.path.join(base, "tentativa_%03d_%s" % (n, mode))
    os.makedirs(path)  # nunca reaproveita uma pasta existente
    return path, n


def fmt(x):
    if isinstance(x, float):
        return "%.6e" % x
    if isinstance(x, mpmath.mpf):
        return mpmath.nstr(x, 6)
    return str(x)


class Checks:
    def __init__(self):
        self.items = []

    def chk(self, item, got, exp):
        ok = (got == exp)
        self.items.append({"item": item, "esperado": exp, "lido": got, "ok": bool(ok)})
        if not ok:
            LOG("   DIVERGENCIA: %s | lido=%r | esperado=%r" % (item, got, exp))
        return ok

    @property
    def ok(self):
        return all(c["ok"] for c in self.items)

    @property
    def falhas(self):
        return [c for c in self.items if not c["ok"]]


# ----------------------------------------------------------------------------- conferencias (V1, V2, V3)
def conferir_freezes(res):
    c = Checks()
    s, n = sha_file(FREEZE_R2)
    c.chk("FREEZE_R2.json sha256", s, EXP_FREEZE_R2[0])
    c.chk("FREEZE_R2.json bytes", n, EXP_FREEZE_R2[1])
    fz = json.load(open(FREEZE_R2, encoding="utf-8"))
    frozen = datetime.fromisoformat(fz["congelado_em_utc"])
    now = datetime.fromisoformat(res["inicio_utc"])
    c.chk("inicio do ensaio (UTC) POSTERIOR a congelado_em_utc (V2)", now > frozen, True)
    res["segundos_depois_do_FREEZE_R2"] = (now - frozen).total_seconds()
    for key in ("adendo_json", "adendo_md"):
        s, n = sha_file(fz[key]["arquivo"])
        c.chk("FREEZE_R2.%s sha256" % key, s, fz[key]["sha256"])
        c.chk("FREEZE_R2.%s bytes" % key, n, fz[key]["bytes"])
    for a in fz["anexos"]:
        s, n = sha_file(os.path.join(ADENDO, a["caminho"].replace("/", os.sep)))
        c.chk("anexo %s sha256" % a["caminho"], s, a["sha256"])
        c.chk("anexo %s bytes" % a["caminho"], n, a["bytes"])
    norm = fz["implementacao_de_referencia_normativa"]
    s, n = sha_file(os.path.join(HERE, "scripts", "tolerancia_uniforme_r2.py"))
    c.chk("implementacao normativa importada == congelada (sha256)", s, norm["sha256"])
    s, n = sha_file(os.path.join(HERE, "2_OPTICO", "run_optico.py"))
    c.chk("runner da R1 copiado == R1 (sha256)", s, sha_file(os.path.join(R1_OPT, "run_optico.py"))[0])
    s, n = sha_file(FREEZE_R1)
    c.chk("FREEZE R1 sha256", s, EXP_FREEZE_R1[0])
    c.chk("FREEZE R1 bytes", n, EXP_FREEZE_R1[1])
    c.chk("FREEZE_R2.freeze_R1.sha256 == FREEZE R1", fz["freeze_R1"]["sha256"], EXP_FREEZE_R1[0])
    res["freeze"] = {"FREEZE_R2": {"arquivo": FREEZE_R2, "sha256": EXP_FREEZE_R2[0], "bytes": EXP_FREEZE_R2[1],
                                   "congelado_em_utc": fz["congelado_em_utc"]},
                     "FREEZE_R1": {"arquivo": FREEZE_R1, "sha256": EXP_FREEZE_R1[0], "bytes": EXP_FREEZE_R1[1]},
                     "itens": c.items, "n": len(c.items), "falhas": c.falhas, "todos_ok": c.ok}
    return c.ok, fz


# ----------------------------------------------------------------------------- beta: float (um.py) e exato (literal)
def beta_runtime(prereg):
    b = RO.read_beta(prereg)                      # bytes do um.py; sem executar; mesma expressao do um.py
    b["estatuto"] = "[DERIVED — lido nos bytes do um.py (l.5557 embutida == l.95 topo) e calculado em runtime: alpha*ONE*sqrt(e); nao e medida]"
    lit = b["alpha_literal"]
    with mp.workdps(200):
        beta_mp = mpf(lit) * mp.sqrt(mp.e)
        b["beta_200_mpmath_do_literal"] = mpmath.nstr(beta_mp, 200)
    with localcontext() as ctx:
        ctx.prec = 200
        beta_D = Decimal(lit) * Decimal(1).exp().sqrt()
        b["beta_200_decimal_do_literal"] = str(beta_D)
    frozen = json.load(open(BETA_FROZEN, encoding="utf-8"))
    b["conferencia_com_BETA_RUNTIME_R2_congelado"] = {
        "literal_igual": lit == frozen["ALPHA_FINE_CODATA_2018"]["literal"],
        "beta_float_igual": b["beta_runtime"] == frozen["beta_runtime_float64"],
        "beta_float_hex": float(b["beta_runtime"]).hex(), "beta_float_hex_congelado": frozen["beta_runtime_float64_hex"],
        "beta_200_decimal_igual_ao_congelado": str(beta_D) == frozen["beta_200_digitos_do_literal"],
        "um_py_sha256_igual": b["um_py_sha256"] == frozen["um_py_sha256"],
    }
    with mp.workdps(200):
        b["mpmath_vs_decimal_200_abs"] = mpmath.nstr(abs(mpf(str(beta_D)) - beta_mp), 5)
    return b, lit


# ----------------------------------------------------------------------------- T9.o'(c)
def t9_float(T, R, lam, p, label, log_rows=False):
    """criterio (c)-entradas como na R1 (matrix_power; ref = R + lam^k (I-R) em float), sob tau_T(k) da regra uniforme."""
    I = np.eye(2)
    rows = []
    maxd, kmax, maxratio, kratio, first_fail = 0.0, 0, 0.0, 0, None
    k0_exact = None
    sample = {}
    nfail = 0
    for k in range(0, 10001):
        Tk = np.linalg.matrix_power(T, k)
        ref = R + lam ** k * (I - R)
        d = float(np.max(np.abs(Tk - ref)))
        if k == 0:
            k0_exact = (d == 0.0)
            ok = k0_exact
            tau = 0.0
            ratio = 0.0
        else:
            tau = TU.tau(k, p["delta_T"], p["w"], p["m"], p["c"])
            ok = d <= tau
            ratio = d / tau
        if not ok:
            nfail += 1
            if first_fail is None:
                first_fail = k
        if d > maxd:
            maxd, kmax = d, k
        if ratio > maxratio:
            maxratio, kratio = ratio, k
        if k in SAMPLE_T:
            sample["k=%d" % k] = {"medido": d, "tau_T": tau, "razao": ratio, "ok": ok}
        if log_rows:
            rows.append((k, d, tau, ratio, ok))
    out = {"representacao": label, "matriz": T.tolist(), "matriz_hex": [[float(x).hex() for x in r] for r in T.tolist()],
           "lambda_float": lam, "delta_T": p["delta_T"], "delta_T_exato_fraction": p["delta_T_exato_fraction"],
           "w": p["w"], "m": p["m"], "c": p["c"], "k0_igualdade_exata": k0_exact,
           "max_k<=1e4": maxd, "k_do_max": kmax, "tau_T(1e4)": TU.tau(10000, p["delta_T"], p["w"], p["m"], p["c"]),
           "max_razao_medido/tau": maxratio, "k_da_max_razao": kratio, "n_k_fora_de_tau": nfail,
           "primeiro_k_fora_de_tau": first_fail, "amostra": sample,
           "PASSA_todo_k": bool(k0_exact and nfail == 0)}
    return out, rows


def t9_exact_mp(lit, dps, kmax=10000):
    """caminho exato: T^k por multiplicacao repetida a `dps` digitos; ref = R + lam^k (I-R) (lam^k por mp.power)."""
    with mp.workdps(dps):
        beta = mpf(lit) * mp.sqrt(mp.e)
        a, b = 1 - beta, beta
        lam = 1 - 2 * beta
        half = mpf(1) / 2
        tol = mpf("1e-150")
        p00, p01, p10, p11 = mpf(1), mpf(0), mpf(0), mpf(1)
        maxd, kmax_d, first_fail, nfail = mpf(0), 0, None, 0
        sample = {}
        keep = {}
        for k in range(0, kmax + 1):
            if k > 0:
                p00, p01, p10, p11 = p00 * a + p01 * b, p00 * b + p01 * a, p10 * a + p11 * b, p10 * b + p11 * a
            lk = mp.power(lam, k)
            r00 = half + lk * half      # (R + lam^k (I-R))_00 = 1/2 + lam^k/2
            r01 = half - lk * half      # (R + lam^k (I-R))_01 = 1/2 - lam^k/2
            d = max(abs(p00 - r00), abs(p01 - r01), abs(p10 - r01), abs(p11 - r00))
            ok = d <= tol
            if not ok:
                nfail += 1
                if first_fail is None:
                    first_fail = k
            if d > maxd:
                maxd, kmax_d = d, k
            if k in SAMPLE_D:
                sample["k=%d" % k] = {"desvio_max_abs": mpmath.nstr(d, 8), "ok_1e-150": ok,
                                      "T^k_00": mpmath.nstr(p00, 40), "T^k_01": mpmath.nstr(p01, 40),
                                      "lambda^k": mpmath.nstr(lk, 40)}
                keep[k] = (p00, p01, p10, p11, lk, d)
        out = {"dps": dps, "beta_literal": lit, "beta": mpmath.nstr(beta, 40), "lambda": mpmath.nstr(lam, 40),
               "tolerancia": "1e-150 absoluta, por k", "max_desvio_k<=%d" % kmax: mpmath.nstr(maxd, 8),
               "k_do_max": kmax_d, "n_k_fora": nfail, "primeiro_k_fora": first_fail, "amostra": sample,
               "PASSA_todo_k": nfail == 0}
    return out, keep


def t9_exact_decimal(lit, prec=200, kmax=10000):
    with localcontext() as ctx:
        ctx.prec = prec
        beta = Decimal(lit) * Decimal(1).exp().sqrt()
        a, b = 1 - beta, beta
        lam = 1 - 2 * beta
        half = Decimal("0.5")
        tol = Decimal("1e-150")
        p00, p01, p10, p11 = Decimal(1), Decimal(0), Decimal(0), Decimal(1)
        maxd, kmax_d, nfail, first_fail = Decimal(0), 0, 0, None
        keep = {}
        for k in range(0, kmax + 1):
            if k > 0:
                p00, p01, p10, p11 = p00 * a + p01 * b, p00 * b + p01 * a, p10 * a + p11 * b, p10 * b + p11 * a
            lk = lam ** k
            r00 = half + lk * half
            r01 = half - lk * half
            d = max(abs(p00 - r00), abs(p01 - r01), abs(p10 - r01), abs(p11 - r00))
            if d > tol:
                nfail += 1
                if first_fail is None:
                    first_fail = k
            if d > maxd:
                maxd, kmax_d = d, k
            if k in SAMPLE_D:
                keep[k] = (p00, p01, p10, p11, lk, d)
        return {"prec": prec, "beta": str(beta)[:45], "max_desvio": "%.6E" % maxd, "k_do_max": kmax_d, "n_k_fora": nfail,
                "primeiro_k_fora": first_fail, "PASSA_todo_k": nfail == 0}, keep


def cross_check_t9(keep_mp, keep_D):
    """C-UNIF-d: mpmath(200) x decimal(200) nas mesmas quantidades, k in SAMPLE_D, concordancia <= 1e-150 (absoluta)."""
    out = {}
    worst = mpf(0)
    with mp.workdps(200):
        tol = mpf("1e-150")
        for k in SAMPLE_D:
            m = keep_mp[k]
            d = keep_D[k]
            diffs = [abs(mpf(str(d[i])) - m[i]) for i in range(5)]
            dd = abs(mpf(str(d[5])) - m[5])
            mx = max(diffs)
            worst = max(worst, mx)
            out["k=%d" % k] = {"max_dif_entradas_e_lambda^k": mpmath.nstr(mx, 6), "dif_dos_desvios": mpmath.nstr(dd, 6),
                               "concordam_1e-150": mx <= tol}
        return {"por_k": out, "max_dif": mpmath.nstr(worst, 6), "concordam_1e-150_todos": worst <= tol}


# ----------------------------------------------------------------------------- O-f'
def of_float_E4(pB, kmax=100):
    c1, s1 = math.cosh(1.0), math.sinh(1.0)
    x, y = 1.0, -1.0
    rows = {}
    worst10, worst100, first_fail, nfail10 = 0.0, 0.0, None, 0
    sym = True
    for k in range(1, kmax + 1):
        x, y = c1 * x + s1 * y, s1 * x + c1 * y
        sym = sym and (x == -y)
        nrm = math.hypot(x, y)
        ref = math.sqrt(2.0) * math.exp(-k)
        rel = abs(nrm - ref) / ref
        tau = TU.tau(k, pB["delta_B_rel"], pB["w"], pB["m"], pB["c"])
        ok = rel <= tau
        rows["k=%d" % k] = {"norma": nrm, "sqrt2_e^-k": ref, "rel": rel, "tau_B_rel": tau, "razao": rel / tau, "ok": ok,
                            "obrigatorio": k <= 10}
        if k <= 10:
            worst10 = max(worst10, rel)
            if not ok:
                nfail10 += 1
                if first_fail is None:
                    first_fail = k
        worst100 = max(worst100, rel)
    return {"c1": c1, "s1": s1, "c1_hex": c1.hex(), "s1_hex": s1.hex(), "por_k": rows,
            "max_rel_k<=10": worst10, "tau_B_rel(10)": TU.tau(10, pB["delta_B_rel"], pB["w"], pB["m"], pB["c"]),
            "max_rel_k<=100_informativo": worst100, "orbita_fica_na_reta_nula_exatamente_k<=100": sym,
            "n_k<=10_fora_de_tau": nfail10, "primeiro_k_fora": first_fail,
            "PASSA_k<=10": nfail10 == 0,
            "informativo_k11..100_todos_dentro_de_tau": all(rows["k=%d" % k]["ok"] for k in range(11, kmax + 1))}


def of_exact_mp(dps=200, kmax=100):
    with mp.workdps(dps):
        e1 = mp.e
        ch = (e1 + 1 / e1) / 2
        sh = (e1 - 1 / e1) / 2
        tol = mpf("1e-150")
        x, y = mpf(1), mpf(-1)
        worst, kw, nfail, first_fail = mpf(0), 0, 0, None
        sample = {}
        keep = {}
        for k in range(1, kmax + 1):
            x, y = ch * x + sh * y, sh * x + ch * y
            nr = mp.sqrt(x * x + y * y)
            ref = mp.sqrt(2) * mp.exp(-k)
            rel = abs(nr - ref) / ref
            if rel > tol:
                nfail += 1
                if first_fail is None:
                    first_fail = k
            if rel > worst:
                worst, kw = rel, k
            if k in (1, 10, 50, 100):
                sample["k=%d" % k] = {"norma": mpmath.nstr(nr, 40), "sqrt2_e^-k": mpmath.nstr(ref, 40), "rel": mpmath.nstr(rel, 8)}
            if k in (10, 100):
                keep[k] = (nr, rel)
        out = {"dps": dps, "cosh1_de_exp": mpmath.nstr(ch, 40), "sinh1_de_exp": mpmath.nstr(sh, 40),
               "cosh1_exp_vs_mp_cosh_abs": mpmath.nstr(abs(ch - mp.cosh(1)), 5),
               "det_B_menos_1": mpmath.nstr(ch * ch - sh * sh - 1, 5),
               "tolerancia": "1e-150 relativa, por k = 1..%d" % kmax, "max_rel": mpmath.nstr(worst, 8), "k_do_max": kw,
               "n_k_fora": nfail, "primeiro_k_fora": first_fail, "amostra": sample, "PASSA_todo_k": nfail == 0}
    return out, keep


def of_exact_decimal(prec=200, kmax=100):
    """o mesmo caminho decimal da R1 (run_optico.py, T4.o O-f): reproduz as strings da R1 em k = 10 e 100."""
    with localcontext() as ctx:
        ctx.prec = prec
        e1 = Decimal(1).exp()
        ch = (e1 + 1 / e1) / 2
        sh = (e1 - 1 / e1) / 2
        xd, yd = Decimal(1), Decimal(-1)
        keep = {}
        for k in range(1, kmax + 1):
            xd, yd = ch * xd + sh * yd, sh * xd + ch * yd
            nr = (xd * xd + yd * yd).sqrt()
            if k in (10, 100):
                ref = Decimal(2).sqrt() * Decimal(-k).exp()
                keep[k] = (nr, abs(nr - ref) / ref)
        return keep


def cross_check_of(keep_mp, keep_D, r1_dec):
    out = {}
    worst = mpf(0)
    with mp.workdps(200):
        tol = mpf("1e-150")
        for k in (10, 100):
            nm, rm = keep_mp[k]
            nd, rd = keep_D[k]
            rel = abs(mpf(str(nd)) - nm) / nm
            worst = max(worst, rel)
            out["k=%d" % k] = {"dif_rel_norma_mpmath_vs_decimal": mpmath.nstr(rel, 6), "concordam_1e-150": rel <= tol,
                               "rel_decimal": "%.6E" % rd, "rel_mpmath": mpmath.nstr(rm, 6),
                               "norma_decimal_igual_a_string_da_R1": str(nd) == r1_dec["k=%d" % k]["norma"],
                               "rel_decimal_igual_a_string_da_R1": str(rd) == r1_dec["k=%d" % k]["rel"]}
        return {"por_k": out, "max_dif_rel": mpmath.nstr(worst, 6), "concordam_1e-150_todos": worst <= tol}


def cunif_a(pB):
    """C-UNIF-a: o caminho numpy.linalg.matrix_power(B,k) @ (1,-1) TEM de FALHAR tau_B em algum k <= 10; BLAS informativo."""
    B = RO.boost_f64(1.0)
    v = np.array([1.0, -1.0])
    rows = {}
    first_mp = first_blas = None
    for k in range(1, 13):
        v = B @ v
        ref = math.sqrt(2.0) * math.exp(-k)
        r_blas = abs(float(np.linalg.norm(v)) - ref) / ref
        w = np.linalg.matrix_power(B, k) @ np.array([1.0, -1.0])
        r_mp = abs(float(np.linalg.norm(w)) - ref) / ref
        tau = TU.tau(k, pB["delta_B_rel"], pB["w"], pB["m"], pB["c"])
        rows["k=%d" % k] = {"rel_matrix_power": r_mp, "rel_BLAS_B@v": r_blas, "tau_B_rel": tau,
                            "matrix_power_dentro_de_tau": r_mp <= tau, "BLAS_dentro_de_tau": r_blas <= tau,
                            "matrix_power_fica_na_reta_nula": bool(w[0] == -w[1]), "BLAS_fica_na_reta_nula": bool(v[0] == -v[1])}
        if first_mp is None and r_mp > tau:
            first_mp = k
        if first_blas is None and r_blas > tau:
            first_blas = k
    falha_ate_10 = first_mp is not None and first_mp <= 10
    return {"por_k": rows, "primeiro_k_matrix_power_fora_de_tau": first_mp, "primeiro_k_BLAS_fora_de_tau_k<=12": first_blas,
            "matrix_power_FALHA_em_algum_k<=10": falha_ate_10,
            "comportou_se_como_registrado": falha_ate_10,
            "leitura": "instabilidade numerica da sela (cancelamento cosh - sinh cresce como eps*e^{2k}); se passasse, tau_B seria cheque em branco e O-f' INVALIDO"}


# ----------------------------------------------------------------------------- V4: a reproducao da R1 pelo runner copiado
def comparar_v4(r1, v4):
    out = {"existe": True, "arquivo": V4_RES, "runner_sha256_v4": v4["runner"]["sha256"], "runner_sha256_r1": r1["runner"]["sha256"],
           "runner_igual": v4["runner"]["sha256"] == r1["runner"]["sha256"], "semente_v4": v4.get("semente"), "semente_r1": r1.get("semente"),
           "valido_v4": v4.get("valido"), "valido_r1": r1.get("valido"), "preflight_falhas_v4": len(v4["preflight"]["falhas"]),
           "subitens": {}, "controles": {}, "por_afirmacao": {}}
    n_crit = n_ok_igual = n_med_igual = n_med_dif = 0
    dif_ok = []
    for sid, d1 in r1["subitens_oticos"].items():
        d4 = v4["subitens_oticos"].get(sid)
        if d4 is None:
            out["subitens"][sid] = {"ausente_na_v4": True}
            dif_ok.append((sid, "ausente"))
            continue
        c1, c4 = d1["criterios"], d4["criterios"]
        same_names = [c["nome"] for c in c1] == [c["nome"] for c in c4]
        eq_ok = eq_med = 0
        for a, b in zip(c1, c4):
            n_crit += 1
            if a["ok"] == b["ok"]:
                eq_ok += 1
            else:
                dif_ok.append((sid, a["nome"]))
            if a["medida"] == b["medida"]:
                eq_med += 1
            else:
                n_med_dif += 1
        n_ok_igual += eq_ok
        n_med_igual += eq_med
        out["subitens"][sid] = {"resultado_r1": d1.get("resultado"), "resultado_v4": d4.get("resultado"),
                                "mesmo_resultado": d1.get("resultado") == d4.get("resultado"), "mesmos_nomes_de_criterio": same_names,
                                "n_criterios": len(c1), "vereditos_por_criterio_iguais": eq_ok, "medidas_bit_a_bit_iguais": eq_med}
    for cid, d1 in r1["controles_oticos"].items():
        d4 = v4["controles_oticos"].get(cid, {})
        out["controles"][cid] = {"r1": d1.get("comportou_se_como_registrado"), "v4": d4.get("comportou_se_como_registrado"),
                                 "igual": d1.get("comportou_se_como_registrado") == d4.get("comportou_se_como_registrado")}
    for tid, d1 in r1["por_afirmacao_face_otica"].items():
        d4 = v4["por_afirmacao_face_otica"].get(tid, {})
        out["por_afirmacao"][tid] = {"r1": d1["resultado_da_face_otica"], "v4": d4.get("resultado_da_face_otica"),
                                     "igual": d1["resultado_da_face_otica"] == d4.get("resultado_da_face_otica")}
    out["n_criterios"] = n_crit
    out["n_vereditos_por_criterio_iguais"] = n_ok_igual
    out["n_medidas_bit_a_bit_iguais"] = n_med_igual
    out["n_medidas_diferentes"] = n_med_dif
    out["criterios_com_veredito_diferente"] = dif_ok
    out["controles_todos_iguais"] = all(v["igual"] for v in out["controles"].values())
    out["por_afirmacao_todos_iguais"] = all(v["igual"] for v in out["por_afirmacao"].values())
    out["reproduz_a_R1_em_todo_criterio"] = (n_ok_igual == n_crit and not dif_ok and out["controles_todos_iguais"]
                                             and out["por_afirmacao_todos_iguais"] and v4.get("valido") is True)
    out["kernel_v4"] = v4.get("impressao_digital_kernel", {}).get("iguais")
    out["T9.o_c_entradas_v4"] = next((c for c in v4["subitens_oticos"]["T9.o"]["criterios"] if c["nome"].startswith("(c) max_{k<=10^4}")), None)
    out["Of_E4_v4"] = next((c for c in v4["subitens_oticos"]["T4.o"]["criterios"] if "IEEE escalar (E4)" in c["nome"]), None)
    return out


# ----------------------------------------------------------------------------- main
def main():
    mode = "infra" if "--infra" in sys.argv else "ensaio"
    att_dir, att_n = new_attempt_dir(mode)
    LOG.open(os.path.join(att_dir, "reensaio_r2.log"))
    inicio_utc = datetime.now(timezone.utc).isoformat()
    LOG("F1.TEMPO — REENSAIO R2 da face otica (O-f' e T9.o'(c) sob o ADENDO UNIFORME) — tentativa %03d (%s) — %s" % (att_n, mode, att_dir))
    rb = open(os.path.abspath(__file__), "rb").read()
    res = {"documento": "RESULTADO_REENSAIO_R2 — F1.TEMPO, face otica: O-f' e T9.o'(c) sob o ADENDO UNIFORME (R2)",
           "unidade": "F1.TEMPO", "trilha": "TEMPO", "gerencia": "c1",
           "papel": "reensaiador otico da R2 (subagente do workflow posto-e-tempo da gerencia c1)",
           "estatuto_do_documento": ("[REAL — medido aqui, modelo sintetico] por criterio; beta [DERIVED: lido nos bytes do um.py e "
                                     "calculado em runtime]; regra e tolerancias [INPUT da gerencia — ADENDO R2 congelado]; "
                                     "PASSA = validade matematica na face testada, nao creditacao; sem veredito global; o gate nao se "
                                     "move; beta na natureza a 5 sigma nao e tocado; nenhum dado observado; nenhum Lean rodado; "
                                     "o um.py nao foi executado."),
           "tentativa": att_n, "modo": mode, "inicio_utc": inicio_utc, "inicio_local": time.strftime("%Y-%m-%d %H:%M:%S"),
           "ambiente": {"python": sys.version, "numpy": np.__version__, "mpmath": mpmath.__version__, "plataforma": platform.platform(),
                        "flags": {"dont_write_bytecode": sys.flags.dont_write_bytecode, "ignore_environment": sys.flags.ignore_environment,
                                  "safe_path": sys.flags.safe_path, "isolated": sys.flags.isolated}},
           "runner_r2": {"arquivo": os.path.abspath(__file__), "sha256": sha256_bytes(rb), "bytes": len(rb)},
           "implementacao_normativa_importada": {"arquivo": os.path.abspath(TU.__file__), "sha256": sha_file(TU.__file__)[0]},
           "runner_r1_copiado_importado": {"arquivo": os.path.abspath(RO.__file__), "sha256": sha_file(RO.__file__)[0]},
           "fontes_so_leitura": {"RESULTADO_OPTICO_R1": dict(zip(("sha256", "bytes"), sha_file(R1_RES))),
                                 "DIAGNOSTICO_T9c_R1": dict(zip(("sha256", "bytes"), sha_file(R1_DIAG))),
                                 "ACHADOS_R1": dict(zip(("sha256", "bytes"), sha_file(R1_ACH))),
                                 "TOLERANCIA_UNIFORME_R2_congelada": dict(zip(("sha256", "bytes"), sha_file(TOL_FROZEN))),
                                 "BETA_RUNTIME_R2_congelado": dict(zip(("sha256", "bytes"), sha_file(BETA_FROZEN)))}}
    invalid = []
    LOG("0. conferencia dos FREEZE (R1 e R2), da copia do runner e da implementacao normativa")
    ok_fz, fz = conferir_freezes(res)
    LOG("   %d itens, %d falhas; inicio %.1f s depois do FREEZE_R2" % (res["freeze"]["n"], len(res["freeze"]["falhas"]), res["segundos_depois_do_FREEZE_R2"]))
    if not ok_fz:
        invalid.append("FREEZE divergente ou ensaio anterior ao FREEZE_R2 (V1/V2)")
    LOG("0b. preflight da R1 (runner copiado): FREEZE R1, pre-registro, texto do operador")
    checks, prereg, fz1 = RO.preflight()
    res["preflight_R1"] = {"n": len(checks), "falhas": [c for c in checks if not c["ok"]], "todos_ok": all(c["ok"] for c in checks)}
    LOG("   preflight R1: %d itens, %d falhas" % (len(checks), len(res["preflight_R1"]["falhas"])))
    if not res["preflight_R1"]["todos_ok"]:
        invalid.append("preflight R1 divergente")
    m = re.search(r"default_rng\((\d+)\)", prereg["modelo_otico"]["sementes"])
    res["semente"] = int(m.group(1))
    LOG("1. impressao digital do tgl_kernel (inicio)")
    fp0 = RO.kernel_fingerprint()
    LOG("   meta %s src %s (%d arquivos)" % (fp0["meta_sha256"][:16], fp0["src_sha256"][:16], fp0["files"]))
    LOG("2. beta em runtime (bytes do um.py; sem executar) — float64 e 200 digitos do literal")
    binfo, lit = beta_runtime(prereg)
    res["beta"] = binfo
    LOG("   alpha literal %s (l.%s; SEALED l.%s igual=%s) -> beta = %r ; dif conferencia %r ; confere=%s ; mp x decimal = %s" % (
        lit, binfo.get("linha_alpha"), binfo.get("SEALED_CODATA_ALPHA_linha"), binfo.get("alpha_igual_SEALED"),
        binfo.get("beta_runtime"), binfo.get("dif_abs_conferencia"), binfo.get("confere"), binfo["mpmath_vs_decimal_200_abs"]))
    if not binfo.get("confere") or not all(binfo["conferencia_com_BETA_RUNTIME_R2_congelado"].values()):
        invalid.append("beta lido nao confere (conferencia do pre-registro ou BETA_RUNTIME_R2 congelado)")
    if invalid:
        res["valido"] = False
        res["motivos_de_INVALIDO"] = invalid
        res["impressao_digital_kernel"] = {"inicio": fp0}
        write_json_atomic(os.path.join(att_dir, "RESULTADO_REENSAIO_R2.json"), res)
        LOG("INVALIDO antes do ensaio: %s" % invalid)
        LOG.close()
        return 2

    LOG("3. modelo (E2) e parametros da regra uniforme (implementacao normativa importada)")
    M = RO.build_model(binfo["beta_runtime"])
    r1 = json.load(open(R1_RES, encoding="utf-8"))
    diag = json.load(open(R1_DIAG, encoding="utf-8"))
    ach = json.load(open(R1_ACH, encoding="utf-8"))
    tol = json.load(open(TOL_FROZEN, encoding="utf-8"))
    c = Checks()
    T = M["T"]
    c.chk("T runtime == modelo.T guardado na R1 (bit a bit)", T.tolist(), r1["modelo"]["T"])
    c.chk("T simetrica exata", bool(T[0, 0] == T[1, 1] and T[0, 1] == T[1, 0]), True)
    c.chk("T[0][0] hex == congelado", float(T[0, 0]).hex(), tol["T9.o'(c)"]["parametros"]["a_hex"])
    c.chk("T[0][1] hex == congelado", float(T[0, 1]).hex(), tol["T9.o'(c)"]["parametros"]["b_hex"])
    c.chk("lambda runtime == R1", M["lam"], r1["modelo"]["lambda"])
    c.chk("R == J/2", M["R"].tolist(), [[0.5, 0.5], [0.5, 0.5]])
    c.chk("beta runtime == modelo.beta R1", M["beta"], r1["modelo"]["beta"])
    pT = TU.params_T(T.tolist())
    pB = TU.params_B(1.0)
    fT = tol["T9.o'(c)"]["parametros"]
    fB = tol["O-f'"]["parametros"]
    for k in ("delta_T", "delta_T_exato_fraction", "delta_T_em_unidades_de_2^-53", "w", "m", "c", "a_hex", "b_hex", "simetrica_exata"):
        c.chk("param T9: %s == congelado" % k, pT[k], fT[k])
    for k in ("cosh_hex", "sinh_hex", "cosh", "sinh", "mu_B_exato_fraction", "delta_B_rel", "det_B_float_menos_1", "w", "m", "c"):
        c.chk("param O-f: %s == congelado" % k, pB[k], fB[k])
    for row in tol["T9.o'(c)"]["tabela"]:
        c.chk("tau_T(%d) == tabela congelada" % row["k"], TU.tau(row["k"], pT["delta_T"], pT["w"], pT["m"], pT["c"]), row["tau_T(k)"])
    for row in tol["O-f'"]["tabela"]:
        c.chk("tau_B(%d) == tabela congelada" % row["k"], TU.tau(row["k"], pB["delta_B_rel"], pB["w"], pB["m"], pB["c"]), row["tau_B_rel(k)"])
    c.chk("c1 = math.cosh(1.0) bit a bit == congelado", math.cosh(1.0).hex(), fB["cosh_hex"])
    c.chk("s1 = math.sinh(1.0) bit a bit == congelado", math.sinh(1.0).hex(), fB["sinh_hex"])
    c.chk("eps da regra == 2^-52", TU.EPS, 2.0 ** -52)
    res["modelo_e_parametros"] = {"itens": c.items, "n": len(c.items), "falhas": c.falhas, "todos_ok": c.ok,
                                  "T": T.tolist(), "T_hex": [[float(x).hex() for x in r] for r in T.tolist()],
                                  "lambda": M["lam"], "theta_M": M["theta_M"], "parametros_T9": pT, "parametros_Of": pB,
                                  "formula": tol["regra"]}
    LOG("   %d itens, %d falhas (delta_T = %r = %s * 2^-53; delta_B_rel = %r; m_B = %r)" % (
        len(c.items), len(c.falhas), pT["delta_T"], pT["delta_T_em_unidades_de_2^-53"], pB["delta_B_rel"], pB["m"]))
    if not c.ok:
        invalid.append("modelo/parametros divergem do congelado (ambiente ou representacao mudou): INVALIDO, novo ADENDO")
    if mode == "infra" or invalid:
        fp1 = RO.kernel_fingerprint()
        res["impressao_digital_kernel"] = {"inicio": fp0, "fim": fp1, "iguais": fp0["meta_sha256"] == fp1["meta_sha256"] and fp0["src_sha256"] == fp1["src_sha256"]}
        res["valido"] = not invalid
        res["motivos_de_INVALIDO"] = invalid
        res["nota"] = "verificacao de infraestrutura (conferencias, beta, modelo, parametros); nenhum teste do ADENDO foi medido" if mode == "infra" else "INVALIDO"
        res["fim_utc"] = datetime.now(timezone.utc).isoformat()
        sha, nb = write_json_atomic(os.path.join(att_dir, "RESULTADO_REENSAIO_R2.json"), res)
        LOG("%s: valido=%s ; resultado sha256 %s (%d B)" % (mode, res["valido"], sha, nb))
        LOG.close()
        return 0 if res["valido"] else 2

    # ------------------------------------------------------------------ T9.o'(c)
    LOG("4. T9.o'(c) — caminho FLOAT64 (E2: T = |S|^2 guardada; matrix_power; ref R + lam^k (I-R)) sob tau_T(k)")
    t0 = time.time()
    fE2, rowsE2 = t9_float(T, M["R"], M["lam"], pT, "E2: T = |Smat(theta_M)|^2 (a representacao do veredito, fixada na R1)", log_rows=True)
    fE2["segundos"] = round(time.time() - t0, 2)
    # bit a bit contra a R1 (diagnostico, mesma maquina): esperado igual
    e2d = diag["E2_|S|^2 (escolha fixada antes da rodada)"]
    fE2["R1_ao_lado"] = {"max_k<=1e4_R1": e2d["max_k<=10^4_float"], "k_do_max_R1": e2d["k_do_max"], "tolerancia_R1": "1e-13 absoluta",
                         "veredito_R1_T9.o(c)_entradas": "FALHA (6.518119377574294e-13 > 1e-13; acima de 1e-13 desde k = 1529)",
                         "max_R2_bit_a_bit_igual_ao_R1": fE2["max_k<=1e4"] == e2d["max_k<=10^4_float"],
                         "amostra_bit_a_bit_igual_ao_R1": {k: (fE2["amostra"][k]["medido"] == e2d["por_k"][k]["float_matrix_power_vs_ref"])
                                                           for k in fE2["amostra"] if k in e2d["por_k"]},
                         "primeiro_k_acima_de_1e-13_R2": next((r[0] for r in rowsE2 if r[1] > 1e-13), None),
                         "primeiro_k_acima_de_1e-13_R1": e2d["primeiro_k_com_desvio_>1e-13"]}
    # decomposicao informativa: potencia EXATA da matriz float (forma fechada da matriz real [[a,b],[b,a]]) vs ref float
    with mp.workdps(60):
        am, bm, lm = mpf(float(T[0, 0])), mpf(float(T[0, 1])), mpf(M["lam"])
        dec = {}
        for k in SAMPLE_T:
            p, q = (am + bm) ** k, (am - bm) ** k
            ex00, ex01 = (p + q) / 2, (p - q) / 2
            r00, r01 = (1 + lm ** k) / 2, (1 - lm ** k) / 2
            d_rep = float(max(abs(ex00 - r00), abs(ex01 - r01)))
            dec["k=%d" % k] = {"representacao_(potencia_exata_do_T_float_vs_ref)": d_rep, "k*|delta_T|/2": k * abs(pT["delta_T"]) / 2,
                               "medido_float": fE2["amostra"]["k=%d" % k]["medido"],
                               "arredondamento_residual_(medido - representacao)": fE2["amostra"]["k=%d" % k]["medido"] - d_rep,
                               "k*eps": k * TU.EPS}
    fE2["decomposicao_informativa"] = dec
    LOG("   max = %.6e em k = %d ; tau_T(1e4) = %.6e ; max razao = %.4f em k = %d ; fora de tau: %d ; k0 exato = %s ; igual a R1 bit a bit = %s" % (
        fE2["max_k<=1e4"], fE2["k_do_max"], fE2["tau_T(1e4)"], fE2["max_razao_medido/tau"], fE2["k_da_max_razao"], fE2["n_k_fora_de_tau"],
        fE2["k0_igualdade_exata"], fE2["R1_ao_lado"]["max_R2_bit_a_bit_igual_ao_R1"]))
    LOG("4b. C-UNIF-b — ALT e EST sob a MESMA tau_T (delta de cada matriz)")
    beta = M["beta"]
    T_alt = np.array([[1 - beta, beta], [beta, 1 - beta]])
    b2 = float(T[0, 1])
    bq = round(b2 * 2 ** 53) / 2 ** 53
    T_est = np.array([[1 - bq, bq], [bq, 1 - bq]])
    cb = {}
    for name, Tm, lam_m, key in (("ALT", T_alt, M["lam"], "ALT_[[fl(1-b), b],[b, fl(1-b)]] (outra forma escrita no modelo)"),
                                 ("EST", T_est, 1 - 2 * bq, "EST_exatamente_estocastica (controle; b' diadico 2^-53)")):
        p = TU.params_T(Tm.tolist())
        o, _ = t9_float(Tm, M["R"], lam_m, p, name)
        o["matriz_igual_ao_diagnostico_R1"] = Tm.tolist() == diag[key]["T"]
        o["max_k<=1e4_R1"] = diag[key]["max_k<=10^4_float"]
        o["max_bit_a_bit_igual_ao_R1"] = o["max_k<=1e4"] == diag[key]["max_k<=10^4_float"]
        cb[name] = o
        LOG("   %s: delta = %r ; max = %.6e ; tau_T(1e4) = %.6e ; fora de tau: %d ; PASSA = %s" % (name, p["delta_T"], o["max_k<=1e4"], o["tau_T(1e4)"], o["n_k_fora_de_tau"], o["PASSA_todo_k"]))
    cb["comportou_se_como_registrado"] = cb["ALT"]["PASSA_todo_k"] and cb["EST"]["PASSA_todo_k"]
    cb["EST_soma_exata_igual_1"] = (Fraction(1 - bq) + Fraction(bq) == 1)
    LOG("5. T9.o'(c) — caminho EXATO (mpmath dps = 200; multiplicacao repetida; tolerancia 1e-150 absoluta)")
    t0 = time.time()
    xE, keep_mp = t9_exact_mp(lit, 200)
    xE["segundos"] = round(time.time() - t0, 2)
    LOG("   max desvio = %s em k = %d ; fora de 1e-150: %d ; PASSA = %s (%.1f s)" % (xE["max_desvio_k<=10000"], xE["k_do_max"], xE["n_k_fora"], xE["PASSA_todo_k"], xE["segundos"]))
    LOG("5b. C-UNIF-c — o mesmo teste exato a dps = 20 TEM de FALHAR a 1e-150")
    xC, _ = t9_exact_mp(lit, 20)
    xC["comportou_se_como_registrado"] = not xC["PASSA_todo_k"]
    LOG("   dps 20: max desvio = %s ; primeiro k fora = %s ; FALHA como registrado = %s" % (xC["max_desvio_k<=10000"], xC["primeiro_k_fora"], xC["comportou_se_como_registrado"]))
    LOG("5c. C-UNIF-d — conferencia cruzada decimal prec = 200 (k in %s)" % SAMPLE_D)
    t0 = time.time()
    xD, keep_D = t9_exact_decimal(lit, 200)
    xD["segundos"] = round(time.time() - t0, 2)
    ccT = cross_check_t9(keep_mp, keep_D)
    LOG("   decimal: max desvio = %s ; fora: %d ; mpmath x decimal max dif = %s ; concordam = %s" % (xD["max_desvio"], xD["n_k_fora"], ccT["max_dif"], ccT["concordam_1e-150_todos"]))

    # ------------------------------------------------------------------ O-f'
    LOG("6. O-f' — caminho FLOAT64 (E4: orbita escalar IEEE) sob tau_B(k) relativa; det e cosh^2 - sinh^2")
    B1 = RO.boost_f64(1.0)
    dB = float(np.linalg.det(B1))
    c1, s1 = math.cosh(1.0), math.sinh(1.0)
    oF = of_float_E4(pB)
    oF["det_B1_float64_LU"] = dB
    oF["|det B(1) - 1| <= 1e-12"] = {"medida": abs(dB - 1), "ok": abs(dB - 1) <= 1e-12}
    oF["|cosh^2 - sinh^2 - 1| <= 1e-12"] = {"medida": abs(c1 * c1 - s1 * s1 - 1), "ok": abs(c1 * c1 - s1 * s1 - 1) <= 1e-12}
    oF["c1_s1_iguais_aos_guardados"] = (c1.hex() == fB["cosh_hex"] and s1.hex() == fB["sinh_hex"])
    r1of = r1["subitens_oticos"]["T4.o"]["medidas"]["Of"]
    oF["R1_ao_lado"] = {"max_rel_k<=10_R1": max(r1of["float64_IEEE_escalar"]["k=%d" % k]["rel"] for k in range(1, 11)),
                        "tolerancia_R1": "1e-9 relativa", "veredito_R1_O-f_E4": "PASSA (5.9130281346959e-16 <= 1e-9)",
                        "bit_a_bit_igual_ao_R1_k<=10": all(oF["por_k"]["k=%d" % k]["rel"] == r1of["float64_IEEE_escalar"]["k=%d" % k]["rel"] for k in range(1, 11)),
                        "det_B1_igual_R1": dB == r1of["det_B1_float64_LU"]}
    LOG("   max rel k<=10 = %.6e ; tau_B(10) = %.6e ; fora: %d ; PASSA k<=10 = %s ; k11..100 dentro = %s ; reta nula exata = %s ; igual R1 = %s" % (
        oF["max_rel_k<=10"], oF["tau_B_rel(10)"], oF["n_k<=10_fora_de_tau"], oF["PASSA_k<=10"], oF["informativo_k11..100_todos_dentro_de_tau"],
        oF["orbita_fica_na_reta_nula_exatamente_k<=100"], oF["R1_ao_lado"]["bit_a_bit_igual_ao_R1_k<=10"]))
    LOG("6b. C-UNIF-a — matrix_power(B,k) @ (1,-1) TEM de FALHAR tau_B em algum k <= 10")
    cA = cunif_a(pB)
    pa = ach["itens"]["O-f_caminhos_aritmeticos_float64"]["por_k"]
    cA["bit_a_bit_igual_ao_anexo_R1"] = all(cA["por_k"]["k=%d" % k]["rel_matrix_power"] == pa["k=%d" % k]["rel_matrix_power"] and
                                            cA["por_k"]["k=%d" % k]["rel_BLAS_B@v"] == pa["k=%d" % k]["rel_BLAS_B@v"] for k in range(1, 13))
    LOG("   primeiro k fora (matrix_power) = %s ; BLAS primeiro k fora (k<=12) = %s ; como registrado = %s ; igual anexo R1 = %s" % (
        cA["primeiro_k_matrix_power_fora_de_tau"], cA["primeiro_k_BLAS_fora_de_tau_k<=12"], cA["comportou_se_como_registrado"], cA["bit_a_bit_igual_ao_anexo_R1"]))
    LOG("7. O-f' — caminho EXATO (mpmath dps = 200; k = 1..100; 1e-150 relativa) e conferencia cruzada decimal (k = 10, 100)")
    oX, keep_of_mp = of_exact_mp(200)
    keep_of_D = of_exact_decimal(200)
    ccB = cross_check_of(keep_of_mp, keep_of_D, r1of["decimal_200"])
    oX["R1_ao_lado"] = {"decimal_200_R1": {k: {"rel": r1of["decimal_200"][k]["rel"][:12] + "..."} for k in ("k=10", "k=100")},
                        "tolerancia_R1": "1e-50 relativa (k = 10, 100)", "veredito_R1": "PASSA (2.0e-198; 2.0e-197)"}
    LOG("   max rel = %s em k = %d ; fora: %d ; PASSA = %s ; mpmath x decimal concordam = %s ; strings da R1 reproduzidas = %s" % (
        oX["max_rel"], oX["k_do_max"], oX["n_k_fora"], oX["PASSA_todo_k"], ccB["concordam_1e-150_todos"],
        all(v["norma_decimal_igual_a_string_da_R1"] and v["rel_decimal_igual_a_string_da_R1"] for v in ccB["por_k"].values())))

    # ------------------------------------------------------------------ vereditos (regra de decisao R2, face otica O1/O2)
    LOG("8. vereditos pela regra de decisao da R2 (O1, O2)")
    t9_invalid = []
    if not xC["comportou_se_como_registrado"]:
        t9_invalid.append("C-UNIF-c: o caminho exato a dps = 20 PASSOU a 1e-150 (tolerancia vazia): caminho exato INVALIDO")
    if not ccT["concordam_1e-150_todos"]:
        t9_invalid.append("C-UNIF-d: mpmath(200) e decimal(200) discordam alem de 1e-150: INVALIDO")
    if t9_invalid:
        t9c = "INVÁLIDO"
    elif xE["PASSA_todo_k"] and fE2["PASSA_todo_k"] and cb["comportou_se_como_registrado"]:
        t9c = "PASSA"
    else:
        t9c = "FALHA"
    if xE["PASSA_todo_k"] and fE2["PASSA_todo_k"]:
        leit_t9 = ("exato PASSA e float PASSA: T9.o'(c) = PASSA; a FALHA da R1 fica registrada AO LADO; a leitura «FALHA R1 = piso de "
                   "representacao» e sustentada pelo numero: a identidade e exata a 200 digitos (desvio %s) e o desvio float %.3e esta "
                   "dentro de k|delta|/2 + k*eps + 2eps = %.3e (razao %.3f)" % (xE["max_desvio_k<=10000"], fE2["max_k<=1e4"], fE2["tau_T(1e4)"], fE2["max_razao_medido/tau"]))
    elif xE["PASSA_todo_k"] and not fE2["PASSA_todo_k"]:
        leit_t9 = "exato PASSA e float FALHA: T9.o'(c) = FALHA; o diagnostico M1 (piso de representacao) fica FALSIFICADO como explicacao suficiente; causa a investigar; sem terceira rodada sem novo ADENDO"
    elif not xE["PASSA_todo_k"]:
        leit_t9 = "exato FALHA: T9.o'(c) = FALHA e INCONSISTENCIA DO RUNNER (o kernel prova a identidade); nunca se corrige tolerancia"
    else:
        leit_t9 = "ver controles"
    if t9c == "FALHA" and not cb["comportou_se_como_registrado"] and xE["PASSA_todo_k"] and fE2["PASSA_todo_k"]:
        leit_t9 = "exato PASSA e float PASSA, mas C-UNIF-b nao se comportou como registrado (ALT ou EST fora de tau_T): FALHA pela regra O1; registra-se; nao e licenca para trocar de representacao"
    of_invalid = []
    if not oF["c1_s1_iguais_aos_guardados"]:
        of_invalid.append("c1/s1 diferem dos guardados (ambiente mudou): O-f' INVALIDO")
    if not cA["comportou_se_como_registrado"]:
        of_invalid.append("C-UNIF-a: o caminho matrix_power PASSOU tau_B em todo k <= 10 (cheque em branco): O-f' INVALIDO")
    if not ccB["concordam_1e-150_todos"]:
        of_invalid.append("C-UNIF-d (O-f): mpmath(200) e decimal(200) discordam alem de 1e-150: INVALIDO")
    if of_invalid:
        of = "INVÁLIDO"
    elif oX["PASSA_todo_k"] and oF["PASSA_k<=10"] and oF["|det B(1) - 1| <= 1e-12"]["ok"] and oF["|cosh^2 - sinh^2 - 1| <= 1e-12"]["ok"]:
        of = "PASSA"
    else:
        of = "FALHA"
    leit_of = ("exato PASSA (k = 1..100, max rel %s) e float E4 PASSA (max rel %.3e <= tau_B(10) = %.3e), com o caminho mal condicionado "
               "falhando tau_B desde k = %s como registrado: O-f' = PASSA; a dependencia do caminho aritmetico (R1) fica dita e controlada" % (
                   oX["max_rel"], oF["max_rel_k<=10"], oF["tau_B_rel(10)"], cA["primeiro_k_matrix_power_fora_de_tau"])) if of == "PASSA" else "ver criterios"

    res["T9.o'(c)"] = {"regra": "O1: PASSA <=> exato PASSA (todo k <= 1e4 a 1e-150) e float E2 PASSA (k = 0 exato; todo k <= 1e4 sob tau_T) e C-UNIF-b, c, d como registrado; outra combinacao = FALHA lida pela (b); C-UNIF-c passar ou C-UNIF-d discordar = INVALIDO",
                       "float64_E2": fE2, "C-UNIF-b": cb, "exato_mpmath_200": xE, "C-UNIF-c_dps20": xC, "exato_decimal_200": xD, "C-UNIF-d": ccT,
                       "motivos_de_INVALIDO": t9_invalid, "resultado": t9c, "leitura": leit_t9,
                       "predicao_registrada": tol["T9.o'(c)"]["predicao"]["predicao_T9.o'(c)_float_E2"],
                       "predicao_cumprida": (tol["T9.o'(c)"]["predicao"]["predicao_T9.o'(c)_float_E2"] == ("PASSA" if fE2["PASSA_todo_k"] else "FALHA"))}
    res["O-f'"] = {"regra": "O2: PASSA <=> exato PASSA (k = 1..100, 1e-150 relativa) e float E4 PASSA (k = 1..10 sob tau_B) e |det B(1) - 1| <= 1e-12 e |cosh^2 - sinh^2 - 1| <= 1e-12 e C-UNIF-a FALHA como registrado e c1, s1 iguais aos guardados; C-UNIF-a passar ou c1/s1 diferirem = INVALIDO",
                   "float64_E4": oF, "C-UNIF-a": cA, "exato_mpmath_200": oX, "C-UNIF-d": ccB,
                   "motivos_de_INVALIDO": of_invalid, "resultado": of, "leitura": leit_of,
                   "predicao_registrada": tol["O-f'"]["predicao"]["predicao_O-f'_float_E4_k<=10"],
                   "predicao_cumprida": (tol["O-f'"]["predicao"]["predicao_O-f'_float_E4_k<=10"] == ("PASSA" if oF["PASSA_k<=10"] else "FALHA"))}
    LOG("   T9.o'(c) = %s | O-f' = %s" % (t9c, of))

    # ------------------------------------------------------------------ V4 (reproducao da R1 pelo runner copiado) e O3/O4
    LOG("9. V4 — reproducao da R1 pelo runner da R1 copiado (fora dos dois testes tudo tem de reproduzir); O3 (T9.o') e O4 (T4.o')")
    if os.path.exists(V4_RES):
        v4 = json.load(open(V4_RES, encoding="utf-8"))
        cmpv4 = comparar_v4(r1, v4)
        LOG("   V4: %d criterios; vereditos iguais %d; medidas bit a bit iguais %d (diferentes %d); controles iguais %s; por afirmacao iguais %s; valido %s; reproduz = %s" % (
            cmpv4["n_criterios"], cmpv4["n_vereditos_por_criterio_iguais"], cmpv4["n_medidas_bit_a_bit_iguais"], cmpv4["n_medidas_diferentes"],
            cmpv4["controles_todos_iguais"], cmpv4["por_afirmacao_todos_iguais"], cmpv4["valido_v4"], cmpv4["reproduz_a_R1_em_todo_criterio"]))
        if not cmpv4["reproduz_a_R1_em_todo_criterio"]:
            invalid.append("V4: a reproducao da R1 pelo runner copiado mudou algum veredito fora dos dois testes do ADENDO (defeito do runner/ambiente): INVALIDO")
        t9o_rest_ok = all(c["ok"] for c in v4["subitens_oticos"]["T9.o"]["criterios"] if not c["nome"].startswith("(c) max_{k<=10^4}"))
        t4o_rest_ok = all(c["ok"] for c in v4["subitens_oticos"]["T4.o"]["criterios"])
        o3 = "PASSA" if (t9c == "PASSA" and t9o_rest_ok and cmpv4["reproduz_a_R1_em_todo_criterio"]) else ("INVÁLIDO" if t9c == "INVÁLIDO" or not cmpv4["reproduz_a_R1_em_todo_criterio"] else "FALHA")
        o4 = "PASSA" if (of == "PASSA" and t4o_rest_ok and cmpv4["reproduz_a_R1_em_todo_criterio"]) else ("INVÁLIDO" if of == "INVÁLIDO" or not cmpv4["reproduz_a_R1_em_todo_criterio"] else "FALHA")
        res["V4_reproducao_R1"] = cmpv4
        res["T9.o'"] = {"regra": "O3: T9.o' = PASSA <=> T9.o'(c) PASSA e (a), (b) e os demais criterios de (c) reproduzem a R1",
                        "T9.o'(c)": t9c, "demais_criterios_T9.o_reproduzem_R1_(V4)": t9o_rest_ok, "resultado": o3,
                        "R1_ao_lado": "T9.o = FALHA (so pelo criterio (c)-entradas, 6.518e-13 > 1e-13; 22 de 23 criterios ok)"}
        res["T4.o'"] = {"regra": "O4: T4.o' = PASSA <=> O-f' PASSA e O-a..O-e reproduzem a R1",
                        "O-f'": of, "O-a..O-f_R1_reproduzem_(V4)": t4o_rest_ok, "resultado": o4, "R1_ao_lado": "T4.o = PASSA"}
        LOG("   T9.o' = %s | T4.o' = %s" % (o3, o4))
    else:
        res["V4_reproducao_R1"] = {"existe": False, "nota": "2_OPTICO/RESULTADO_OPTICO.json desta pasta ausente: O3/O4 pendentes da reproducao V4"}
        res["T9.o'"] = {"resultado": "PENDENTE (V4 nao rodada)", "T9.o'(c)": t9c}
        res["T4.o'"] = {"resultado": "PENDENTE (V4 nao rodada)", "O-f'": of}
        LOG("   V4 ausente: O3/O4 pendentes")

    LOG("10. impressao digital do tgl_kernel (fim)")
    fp1 = RO.kernel_fingerprint()
    same = (fp0["meta_sha256"] == fp1["meta_sha256"] and fp0["src_sha256"] == fp1["src_sha256"])
    same_r1 = (fp0["meta_sha256"] == EXP_KERNEL["meta"] and fp0["src_sha256"] == EXP_KERNEL["src"])
    res["impressao_digital_kernel"] = {"inicio": fp0, "fim": fp1, "iguais": same, "igual_a_R1_e_ao_FREEZE_R2": same_r1}
    LOG("   meta %s src %s iguais=%s igual_R1=%s" % (fp1["meta_sha256"][:16], fp1["src_sha256"][:16], same, same_r1))
    if not same:
        invalid.append("impressao digital do tgl_kernel alterada durante o ensaio")
    res["valido"] = not invalid
    res["motivos_de_INVALIDO"] = invalid
    if invalid:
        for key in ("T9.o'(c)", "O-f'", "T9.o'", "T4.o'"):
            if key in res and isinstance(res[key], dict):
                res[key]["resultado_sob_INVALIDO"] = "INVÁLIDO (ensaio invalido: ver motivos_de_INVALIDO)"
    res["quadro_ao_lado"] = {
        "nota": "linhas NOVAS ao lado das da R1; nenhuma linha da R1 e sobrescrita; sem veredito global; PASSA = validade na face testada, nao creditacao; nada move o gate",
        "T9.o(c)-entradas": {"R1 (1e-13 absoluta, float64 E2)": "FALHA: 6.518119377574294e-13 > 1e-13 (k = 1e4; acima desde k = 1529)",
                             "R2 float64 E2 (tau_T(k) = k(|delta_T|/2 + eps) + 2eps)": "%s: max %.6e vs tau_T(1e4) %.6e (razao %.4f; fora de tau em %d k)" % (
                                 "PASSA" if fE2["PASSA_todo_k"] else "FALHA", fE2["max_k<=1e4"], fE2["tau_T(1e4)"], fE2["max_razao_medido/tau"], fE2["n_k_fora_de_tau"]),
                             "R2 exato mpmath 200 (1e-150 absoluta, k <= 1e4)": "%s: max desvio %s" % ("PASSA" if xE["PASSA_todo_k"] else "FALHA", xE["max_desvio_k<=10000"]),
                             "R2 decimal 200 (conferencia cruzada)": "%s: max desvio %s; mpmath x decimal concordam = %s" % ("PASSA" if xD["PASSA_todo_k"] else "FALHA", xD["max_desvio"], ccT["concordam_1e-150_todos"]),
                             "R2 T9.o'(c) (regra O1)": t9c},
        "O-f": {"R1 (1e-9 relativa, float64 E4, k <= 10; decimal 200 a 1e-50 em k = 10, 100)": "PASSA: 5.9130281346959e-16; 2.0e-198 / 2.0e-197",
                "R2 float64 E4 (tau_B(k) = k(|delta_B| + 4.1945 eps) + 3eps, relativa)": "%s: max rel %.6e vs tau_B(10) %.6e" % ("PASSA" if oF["PASSA_k<=10"] else "FALHA", oF["max_rel_k<=10"], oF["tau_B_rel(10)"]),
                "R2 exato mpmath 200 (1e-150 relativa, k = 1..100)": "%s: max rel %s" % ("PASSA" if oX["PASSA_todo_k"] else "FALHA", oX["max_rel"]),
                "R2 C-UNIF-a (matrix_power tem de falhar)": "como registrado = %s (primeiro k fora = %s)" % (cA["comportou_se_como_registrado"], cA["primeiro_k_matrix_power_fora_de_tau"]),
                "R2 O-f' (regra O2)": of},
        "T9.o'": res["T9.o'"]["resultado"], "T4.o'": res["T4.o'"]["resultado"],
    }
    res["fim_utc"] = datetime.now(timezone.utc).isoformat()
    res["segundos"] = round(time.time() - T_START, 1)
    # tabela por k (todo k <= 1e4) do caminho float E2, preservada em texto
    lines = ["# T9.o'(c) float64 E2 por k: k\tmedido\ttau_T\trazao\tok  (tentativa %03d; tau_T(k) = k(|delta_T|/2 + eps) + 2eps; k = 0 exige igualdade exata)" % att_n]
    for k, d, tau, ratio, ok in rowsE2:
        lines.append("%d\t%.17g\t%.17g\t%.6f\t%s" % (k, d, tau, ratio, int(ok)))
    sha_t, nb_t = write_text_atomic(os.path.join(att_dir, "T9c_float_E2_por_k.tsv"), "\n".join(lines) + "\n")
    res["tabela_por_k"] = {"arquivo": "T9c_float_E2_por_k.tsv", "sha256": sha_t, "bytes": nb_t, "linhas": len(rowsE2)}
    sha_r, nb_r = write_json_atomic(os.path.join(att_dir, "RESULTADO_REENSAIO_R2.json"), res)
    LOG("11. resumo: T9.o'(c) = %s ; O-f' = %s ; T9.o' = %s ; T4.o' = %s ; valido = %s ; resultado sha256 %s (%d B)" % (
        t9c, of, res["T9.o'"]["resultado"], res["T4.o'"]["resultado"], res["valido"], sha_r, nb_r))
    LOG.close()
    for name in ("RESULTADO_REENSAIO_R2.json", "reensaio_r2.log", "T9c_float_E2_por_k.tsv"):
        copy_bytes_atomic(os.path.join(att_dir, name), os.path.join(HERE, name))
    return 0 if res["valido"] else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        LOG("ERRO DO RUNNER:\n" + traceback.format_exc())
        LOG.close()
        sys.exit(3)
