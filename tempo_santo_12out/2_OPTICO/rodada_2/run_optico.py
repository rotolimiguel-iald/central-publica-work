#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_optico.py -- F1.TEMPO (trilha TEMPO, gerencia c1, programa IALD), FACE OTICA, RODADA 2.

Reensaio AO LADO da rodada 1 (2_OPTICO\\RESULTADO_OPTICO.json), contra o MESMO FREEZE
(1_PREREGISTRO\\FREEZE.json), SEM ADENDO: mesmos procedimentos, mesmas tolerancias, mesmo
mapeamento, mesmos esperados. A rodada 2 nao substitui a rodada 1; as duas se preservam.
Codigo escrito de novo nesta rodada (nao copiado da rodada 1).

Modelo SINTETICO: nenhum dado observado, nenhum provedor remoto, nenhuma chamada paga, nenhuma
ferramenta de calculo da Bancada. beta NUNCA literal: o literal de ALPHA_FINE_CODATA_2018 e lido
nos BYTES do um.py (sem executa-lo) e beta = ALPHA * ONE * sqrt(e) e calculado aqui, na mesma
ordem do um.py. Todo numero de conferencia e lido do PREREGISTRO.json e so confere.

PASSA = validade matematica na face testada (modelo sintetico), nao creditacao. Nao ha veredito
global. Nada aqui move o gate. beta na natureza a 5 sigma nao e tocado.

Uso:  python -I -X utf8 run_optico.py --modo autoteste     (so preflight + autotestes)
      python -I -X utf8 run_optico.py --modo ensaio        (o ensaio pre-registrado)
Cada invocacao grava a sua propria pasta tentativas\\tentativa_NNN_<modo>; nada se apaga.
"""
import argparse
import datetime
import decimal
import hashlib
import io
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import tokenize
import traceback

import numpy as np

# ----------------------------------------------------------------------------------------------
# caminhos e valores esperados do FREEZE (copiados do enunciado da tarefa; conferidos contra BYTES)
# ----------------------------------------------------------------------------------------------
BASE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
PRE = os.path.join(BASE, "1_PREREGISTRO")
FREEZE = os.path.join(PRE, "FREEZE.json")
PREJSON = os.path.join(PRE, "PREREGISTRO.json")
PREMD = os.path.join(PRE, "PREREGISTRO.md")
OUT = os.path.join(BASE, "2_OPTICO", "rodada_2")
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
FP_ORIG = os.path.join(PRE, "scripts", "fingerprint_kernel.py")
FP_COPIA = os.path.join(OUT, "scripts", "fingerprint_kernel.py")

EXP_FREEZE_SHA = "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b"
EXP_FREEZE_BYTES = 5986
EXP_JSON_SHA = "64b1c38637befddf89ca06635c548a7d090072f1bc5b6492591cbd4eab163569"
EXP_JSON_BYTES = 208285
EXP_MD_SHA = "0261dc06a5fe513bef153b6df6f107042adf667b9cd97c14336380b9529799b8"
EXP_MD_BYTES = 103112

SEMENTE = None          # lida do PREREGISTRO.json (modelo_otico.sementes)
GRADE_T3 = [-3.0, -1.0, -0.1, 0.0, 0.1, 1.0, 3.0]   # grade pre-registrada do T3.o


# ----------------------------------------------------------------------------------------------
# utilitarios
# ----------------------------------------------------------------------------------------------
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
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


def agora_utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return jsonable(x.tolist())
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        f = float(x)
        if math.isnan(f) or math.isinf(f):
            return str(f)
        return f
    if isinstance(x, (np.complexfloating, complex)):
        return {"re": jsonable(float(x.real)), "im": jsonable(float(x.imag))}
    if isinstance(x, decimal.Decimal):
        return str(x)
    return x


def gravar_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fo:
        json.dump(jsonable(obj), fo, indent=1, ensure_ascii=False)
    os.replace(tmp, path)
    return sha256_file(path)


class Log:
    def __init__(self, path):
        self.path = path
        self.fh = open(path, "w", encoding="utf-8")

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.fh.write(s + "\n")
        self.fh.flush()

    def fechar(self):
        self.fh.close()


def crit(nome, medida, limite, ok, **kw):
    d = {"nome": nome, "medida": medida, "limite": limite, "ok": bool(ok)}
    d.update(kw)
    return d


def conf(calc, prereg_val):
    """conferencia (nunca motor): calculado aqui x numero do PREREGISTRO.json"""
    d = {"calculado_aqui": calc, "preregistro": prereg_val}
    try:
        da = abs(float(calc) - float(prereg_val))
        d["dif_abs"] = da
        d["dif_rel"] = da / abs(float(prereg_val)) if float(prereg_val) != 0 else None
    except Exception:
        d["dif_abs"] = None
    return d


# ----------------------------------------------------------------------------------------------
# algebra do modelo
# ----------------------------------------------------------------------------------------------
I2C = np.eye(2, dtype=complex)
IR = np.eye(2)
GROT = np.array([[0, 1], [-1, 0]], dtype=complex)     # Grot do kernel: !![0,1;-1,0]
E00 = np.array([[1, 0], [0, 0]], dtype=complex)
E11 = np.array([[0, 0], [0, 1]], dtype=complex)
E01 = np.array([[0, 1], [0, 0]], dtype=complex)
E10 = np.array([[0, 0], [1, 0]], dtype=complex)
PSI_PLUS = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)   # |+><+|


def smat(theta):
    """Smat(theta) = cos(theta)*1 + sin(theta)*Grot (definicao do kernel, SMatrix.lean)."""
    return math.cos(theta) * I2C + math.sin(theta) * GROT


def Dmap(X):
    """defasagem completa na base computacional (anula as coerencias); aceita lote (N,n,n)."""
    out = np.zeros_like(X)
    idx = np.arange(X.shape[-1])
    out[..., idx, idx] = X[..., idx, idx]
    return out


def Ad(U, X):
    return U @ X @ U.conj().T


def canal_C(S, X):
    """C = D o Ad(S) o D (o sistema aberto da F1.ATRATOR)."""
    return Dmap(Ad(S, Dmap(X)))


def dephase(g, t, X):
    """semigrupo de defasagem na forma canonica do kernel: (T_t x)_ij = exp(-t g_ij) x_ij."""
    return X * np.exp(-t * np.asarray(g, dtype=float))


def fluxo_modular(rho, t, X):
    """sigma_t(X) = rho^{it} X rho^{-it}; rho positiva-definida. Caminho diagonal exato quando rho e diagonal."""
    off = rho - np.diag(np.diag(rho))
    if not np.any(off):
        d = np.diag(rho).real
        u = np.exp(1j * t * np.log(d))
        return (u[:, None] * X) * np.conj(u)[None, :]
    w, V = np.linalg.eigh(rho)
    U = (V * np.exp(1j * t * np.log(w))) @ V.conj().T
    return U @ X @ U.conj().T


def fro(X):
    return float(np.linalg.norm(X))


def fro_lote(X):
    return np.linalg.norm(X, axis=(-2, -1))


def pureza(X):
    return float(np.trace(X @ X).real)


def pureza_lote(X):
    return np.einsum("nij,nji->n", X, X).real


def cgauss(rng, n):
    return rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))


def herm(rng, n):
    A = cgauss(rng, n)
    return (A + A.conj().T) / 2


def estado(rng, n):
    A = cgauss(rng, n)
    M = A @ A.conj().T
    return M / np.trace(M).real


def unitario(rng, n):
    Q, Rq = np.linalg.qr(cgauss(rng, n))
    d = np.diag(Rq)
    return Q * (d / np.abs(d))


def taxas_simetricas(rng, n):
    g = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            g[i, j] = g[j, i] = rng.uniform(0.0, 1.0)
    return g


def rng_bloco():
    return np.random.default_rng(SEMENTE)


def lstsq_min(H):
    """min_T ||TH - HT - i*1||_F com vec(T) livre (numpy.linalg.lstsq sobre T -> TH - HT); residuo medido."""
    n = H.shape[0]
    cols = []
    for k in range(n):
        for l in range(n):
            E = np.zeros((n, n), dtype=complex)
            E[k, l] = 1.0
            cols.append((E @ H - H @ E).reshape(-1))
    L = np.column_stack(cols)
    b = (1j * np.eye(n)).reshape(-1)
    x = np.linalg.lstsq(L, b, rcond=None)[0]
    return float(np.linalg.norm(L @ x - b))


def posto_numerico(A, fator=1e-12):
    sv = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(sv > fator * sv[0])), sv


# ----------------------------------------------------------------------------------------------
# 1. FREEZE
# ----------------------------------------------------------------------------------------------
def conferir_freeze():
    itens = []

    def chk(nome, lido, esperado):
        itens.append({"item": nome, "esperado": esperado, "lido": lido, "ok": lido == esperado})

    fb = open(FREEZE, "rb").read()
    chk("FREEZE.json sha256", sha256_bytes(fb), EXP_FREEZE_SHA)
    chk("FREEZE.json bytes", len(fb), EXP_FREEZE_BYTES)
    fz = json.loads(fb.decode("utf-8"))
    chk("FREEZE.preregistro_json.sha256 == enunciado", fz["preregistro_json"]["sha256"], EXP_JSON_SHA)
    chk("FREEZE.preregistro_md.sha256 == enunciado", fz["preregistro_md"]["sha256"], EXP_MD_SHA)
    pj = open(PREJSON, "rb").read()
    chk("PREREGISTRO.json sha256 (bytes)", sha256_bytes(pj), EXP_JSON_SHA)
    chk("PREREGISTRO.json bytes", len(pj), EXP_JSON_BYTES)
    pm = open(PREMD, "rb").read()
    chk("PREREGISTRO.md sha256 (bytes)", sha256_bytes(pm), EXP_MD_SHA)
    chk("PREREGISTRO.md bytes", len(pm), EXP_MD_BYTES)
    for a in fz["anexos"]:
        s, n = sha256_file(os.path.join(PRE, a["caminho"].replace("/", os.sep)))
        chk("anexo %s sha256" % a["caminho"], s, a["sha256"])
        chk("anexo %s bytes" % a["caminho"], n, a["bytes"])
    ok = all(i["ok"] for i in itens)
    return ok, itens, fz, pj


# ----------------------------------------------------------------------------------------------
# 2. beta em runtime (bytes do um.py; NAO executado)
# ----------------------------------------------------------------------------------------------
def ler_beta(prereg, log):
    raw = open(UMPY, "rb").read()
    sha = sha256_bytes(raw)

    def linha(pos):
        return raw.count(b"\n", 0, pos) + 1

    pat_a = re.compile(rb"(?m)^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([0-9][0-9eE.+\-]*)[ \t]*\r?$")
    ms = list(pat_a.finditer(raw))
    if len(ms) != 1:
        raise RuntimeError("esperava UMA atribuicao nao indentada de ALPHA_FINE_CODATA_2018; achei %d" % len(ms))
    m = ms[0]
    l_alpha = linha(m.start())
    alpha_lit = m.group(1).decode("ascii")
    pat_one = re.compile(rb"(?m)^ONE[ \t]*=[ \t]*([0-9][0-9eE.+\-]*)[ \t]*\r?$")
    m1 = [x for x in pat_one.finditer(raw) if x.start() > m.start()][0]
    l_one = linha(m1.start())
    one_lit = m1.group(1).decode("ascii")
    pat_b = re.compile(rb"(?m)^BETA_TGL[ \t]*=[ \t]*([^\r\n]*?)[ \t]*\r?$")
    mb = [x for x in pat_b.finditer(raw) if x.start() > m.start()][0]
    l_beta = linha(mb.start())
    expr = mb.group(1).decode("ascii")
    pat_s = re.compile(rb"(?m)^SEALED_CODATA_ALPHA[ \t]*=[ \t]*([0-9][0-9eE.+\-]*)")
    ms_ = list(pat_s.finditer(raw))
    sealed = [{"linha": linha(x.start()), "literal": x.group(1).decode("ascii")} for x in ms_]

    alpha = float(alpha_lit)
    ONE = float(one_lit)
    beta = alpha * ONE * math.sqrt(math.e)          # mesma ordem de BETA_TGL no um.py
    pb = prereg["beta"]
    beta_conf = prereg["numeros_de_conferencia"]["beta"]

    # escopo (informativo): a linha esta dentro de um literal de texto (modulo embutido) ou e codigo?
    escopo = {}
    try:
        pos = 0
        for _ in range(l_alpha + 40):
            pos = raw.index(b"\n", pos) + 1
        txt = raw[:pos].decode("utf-8")
        achado = None
        try:
            for tok in tokenize.generate_tokens(io.StringIO(txt).readline):
                if tok.start[0] <= l_alpha <= tok.end[0]:
                    if tok.type == tokenize.STRING:
                        achado = {"tipo": "STRING", "inicio": tok.start, "fim": tok.end}
                        break
                    if tok.type == tokenize.NAME and tok.string == "ALPHA_FINE_CODATA_2018" and tok.start[1] == 0:
                        achado = {"tipo": "CODIGO (NAME na coluna 0)", "inicio": tok.start}
                        break
                if tok.start[0] > l_alpha:
                    break
        except (tokenize.TokenError, SyntaxError) as e:
            achado = {"tipo": "literal multi-linha ainda aberto no fim do prefixo lido", "erro": repr(e)}
            try:
                ini = e.args[1][0]
                achado["linha_de_inicio_do_literal"] = ini
            except Exception:
                pass
        escopo = achado or {"tipo": "indeterminado"}
        ini = escopo.get("linha_de_inicio_do_literal") or (escopo.get("inicio") or [None])[0]
        if ini:
            pos = 0
            for _ in range(ini - 1):
                pos = raw.index(b"\n", pos) + 1
            fim = raw.index(b"\n", pos)
            escopo["texto_da_linha_de_inicio"] = raw[pos:fim].decode("utf-8", "replace")[:160]
            # o nome atribuido mais proximo acima (o dicionario que guarda o modulo embutido)
            prev = raw.rfind(b"\n_", 0, pos)
            if prev >= 0:
                fim2 = raw.index(b"\n", prev + 1)
                escopo["atribuicao_de_topo_mais_proxima_acima"] = {
                    "linha": linha(prev + 1), "texto": raw[prev + 1:fim2].decode("utf-8", "replace")[:160]}
    except Exception as e:
        escopo = {"erro": repr(e)}

    out = {
        "um_py": UMPY, "um_py_sha256": sha, "um_py_bytes": len(raw),
        "um_py_sha256_do_preregistro": pb["um_py_sha256"],
        "um_py_igual_ao_do_preregistro": sha == pb["um_py_sha256"],
        "executou_um_py": False,
        "atribuicoes_nao_indentadas_de_ALPHA_FINE_CODATA_2018": len(ms),
        "linha_alpha": l_alpha, "linha_alpha_preregistro": pb["linha_alpha"],
        "alpha_literal": alpha_lit, "alpha_literal_preregistro": pb["alpha_literal"],
        "linha_ONE": l_one, "ONE_literal": one_lit,
        "linha_BETA_TGL": l_beta, "expressao_BETA_TGL": expr,
        "expressao_BETA_TGL_preregistro": pb["expressao_beta_no_um_py"],
        "expressao_confere": expr == pb["expressao_beta_no_um_py"],
        "SEALED_CODATA_ALPHA": sealed,
        "alpha_igual_SEALED": all(float(s["literal"]) == alpha for s in sealed) and len(sealed) > 0,
        "escopo_da_linha_alpha_[informativo]": escopo,
        "alpha": alpha, "sqrt_e": math.sqrt(math.e),
        "beta_runtime": beta, "beta_conferencia_do_preregistro": beta_conf,
        "dif_abs_conferencia": abs(beta - beta_conf),
        "confere_1e-15": abs(beta - beta_conf) <= 1e-15,
        "estatuto": "[REAL — medido aqui: literal lido nos bytes; beta calculado em runtime; a conferencia so confere]",
    }
    log("beta: alpha l.%d = %s ; ONE l.%d = %s ; BETA_TGL l.%d = %s" % (l_alpha, alpha_lit, l_one, one_lit, l_beta, expr))
    log("beta_runtime = %r ; |dif conferencia| = %.3e ; um.py sha256 %s" % (beta, abs(beta - beta_conf), sha))
    return beta, out


# ----------------------------------------------------------------------------------------------
# 3. modelo
# ----------------------------------------------------------------------------------------------
def construir_modelo(beta):
    th = math.asin(math.sqrt(beta))
    S = smat(th)
    T = np.empty((2, 2))
    for j, Ej in enumerate((E00, E11)):
        Cj = canal_C(S, Ej)
        for i in range(2):
            T[i, j] = Cj[i, i].real
    R = np.full((2, 2), 0.5)
    lam = 1.0 - 2.0 * beta
    a = -math.log(lam) / 2.0
    rho1 = canal_C(S, E00)
    g01 = beta * abs(math.log((1.0 - beta) / beta))
    gD = np.array([[0.0, g01], [g01, 0.0]])
    w1 = math.log((1.0 - beta) / beta)
    P1 = 2.0 * math.pi / w1
    Hot = 1j * GROT
    return {"beta": beta, "theta_M": th, "S": S, "H_ot": Hot, "T": T, "R": R, "lam": lam, "a": a,
            "rho1": rho1, "g01": g01, "gD": gD, "omega1": w1, "P1": P1}


def F_lock(M, t):
    """fluxo do lock: F(t) = R + e^{-t}(I - R) (axiomFlow com P = R)."""
    return M["R"] + math.exp(-t) * (IR - M["R"])


# ----------------------------------------------------------------------------------------------
# 4. autotestes do runner (inclui mutacoes: o runner tem de saber reprovar)
# ----------------------------------------------------------------------------------------------
def autotestes(M, beta_info, log):
    it = []

    def add(nome, ok, medida, invalida=False):
        it.append({"autoteste": nome, "ok": bool(ok), "medida": medida, "INVALIDO_se_falhar": invalida})

    beta = M["beta"]
    add("beta lido == conferencia (|dif| <= 1e-15)", beta_info["confere_1e-15"], beta_info["dif_abs_conferencia"], True)
    S = M["S"]
    u = fro(S.conj().T @ S - I2C)
    add("S unitaria (||S^H S - I||_F <= 1e-12)", u <= 1e-12, u, True)
    rng = np.random.default_rng(SEMENTE + 1)   # gerador proprio dos autotestes (nao reusa o dos blocos)
    tr = max(abs(np.trace(canal_C(S, estado(rng, 2))) - 1.0) for _ in range(100))
    add("C preserva o traco (100 estados; <= 1e-12)", tr <= 1e-12, float(tr), True)
    d1 = float(np.max(np.abs(M["rho1"] - np.diag([1.0 - beta, beta]))))
    add("rho1 = C(|0><0|) = diag(1-beta, beta) (entradas <= 1e-15)", d1 <= 1e-15, d1)
    dT = float(np.max(np.abs(M["T"] - np.array([[1.0 - beta, beta], [beta, 1.0 - beta]]))))
    add("T = |S|^2 = [[1-b,b],[b,1-b]] (entradas <= 1e-15)", dT <= 1e-15, dT)
    # geradores aleatorios
    ok_e = True
    pior = 0.0
    for n in (2, 3, 5):
        for _ in range(50):
            r = estado(rng, n)
            pior = max(pior, fro(r - r.conj().T), abs(np.trace(r).real - 1.0), max(0.0, -np.linalg.eigvalsh(r)[0]))
    ok_e = pior <= 1e-14
    add("estado aleatorio: hermitiano, traco 1, PSD (<= 1e-14)", ok_e, pior)
    pu = max(fro(U.conj().T @ U - np.eye(n)) for n in (2, 3, 5) for U in [unitario(rng, n) for _ in range(50)])
    add("unitario aleatorio (QR + fase): ||U^H U - I|| <= 1e-13", pu <= 1e-13, pu)
    # dephase
    x = cgauss(rng, 3)
    g = taxas_simetricas(rng, 3)
    add("dephase com g = 0 e a identidade (exata)", np.array_equal(dephase(np.zeros((3, 3)), 1.7, x), x), 0.0)
    sg = fro(dephase(g, 0.3, dephase(g, 0.4, x)) - dephase(g, 0.7, x))
    add("dephase: T_s o T_t = T_{s+t} (<= 1e-14)", sg <= 1e-14, sg)
    # fluxo modular
    xa = cgauss(rng, 2)
    tri = max(fro(fluxo_modular(0.5 * I2C, t, xa) - xa) for t in GRADE_T3)
    add("fluxo modular de I/2 e a identidade (<= 1e-15)", tri <= 1e-15, tri)
    p = 0.3
    rp = np.diag([p, 1 - p]).astype(complex)
    fa = max(abs(fluxo_modular(rp, t, E01)[0, 1] - np.exp(1j * t * math.log(p / (1 - p)))) for t in GRADE_T3)
    add("fluxo modular de diag(0.3,0.7): sigma_t(E01)_01 = e^{it ln(p/(1-p))} (<= 1e-14)", fa <= 1e-14, fa)
    rnd = estado(rng, 3)                       # estado nao diagonal: exercita o caminho eigh
    fe1 = max(fro(fluxo_modular(rnd, t, rnd) - rnd) for t in GRADE_T3)
    xb = cgauss(rng, 3)
    fe2 = max(fro(fluxo_modular(rnd, s, fluxo_modular(rnd, t, xb)) - fluxo_modular(rnd, s + t, xb)) for s in GRADE_T3 for t in GRADE_T3)
    fe3 = max(abs(np.trace(rnd @ fluxo_modular(rnd, t, xb)) - np.trace(rnd @ xb)) for t in GRADE_T3)
    fe = max(fe1, fe2, float(fe3))
    add("fluxo modular (caminho eigh, estado 3x3 nao diagonal): sigma_t(rho)=rho, lei de grupo, invariancia (<= 1e-12)", fe <= 1e-12, fe)
    # lstsq
    Hd = np.diag([1.0, 2.0, 3.0]).astype(complex)
    mn = lstsq_min(Hd)
    add("lstsq: H = diag(1,2,3) da minimo sqrt(3) (<= 1e-12)", abs(mn - math.sqrt(3)) <= 1e-12, abs(mn - math.sqrt(3)))
    # alvo NO alcance de ad_H: residuo ~0 (o lstsq acha zero quando ha zero)
    n = 3
    cols = []
    for k in range(n):
        for l in range(n):
            E = np.zeros((n, n), dtype=complex)
            E[k, l] = 1.0
            cols.append((E @ Hd - Hd @ E).reshape(-1))
    L = np.column_stack(cols)
    tgt = np.zeros((3, 3), dtype=complex)
    tgt[0, 1] = 1.0
    b = (tgt @ Hd - Hd @ tgt).reshape(-1)
    xx = np.linalg.lstsq(L, b, rcond=None)[0]
    r0 = float(np.linalg.norm(L @ xx - b))
    add("lstsq: alvo no alcance de ad_H da residuo ~0 (<= 1e-13)", r0 <= 1e-13, r0)
    # decimal
    ctx = decimal.Context(prec=200)
    e200 = ctx.exp(decimal.Decimal(1))
    try:
        import mpmath
        mpmath.mp.dps = 210
        de = abs(mpmath.mpf(str(e200)) - mpmath.e)
        add("decimal 200 digitos: exp(1) confere com mpmath a 1e-195", de < mpmath.mpf("1e-195"), str(mpmath.nstr(de, 5)))
        mpmath.mp.dps = 15
    except ImportError:
        add("decimal 200 digitos (mpmath ausente: so precisao do contexto)", ctx.prec == 200, ctx.prec)
    # mutacoes: o runner reprova o que tem de reprovar
    Tm = M["T"].copy()
    Tm[0, 0] += 1e-9
    mut1 = fro(Tm - (M["R"] + math.exp(-2 * M["a"]) * (IR - M["R"])))
    add("MUTACAO: T perturbado em 1e-9 reprova o criterio T9.o(a) (<= 1e-15)", mut1 > 1e-15, mut1)
    wm = M["omega1"] * (1 + 1e-9)
    mut2 = abs(np.exp(1j * 3.0 * wm) - np.exp(1j * 3.0 * M["omega1"]))
    add("MUTACAO: omega errado em 1e-9 reprova o criterio T3.o(e) (<= 1e-12)", mut2 > 1e-12, float(mut2))
    r1, s1 = estado(rng, 2), estado(rng, 2)
    Sm = 0.999 * S
    mut3 = abs(fro(Ad(Sm, r1) - Ad(Sm, s1)) - fro(r1 - s1))
    add("MUTACAO: 0.999*S (nao isometria) reprova o criterio O-b (<= 1e-10)", mut3 > 1e-10, mut3)
    Tbad = np.array([[1.0, 0.0], [0.0, 1.0]]) * 1.0000001
    mut4 = float(np.max(np.abs(np.linalg.matrix_power(Tbad, 100) - IR)))
    add("MUTACAO: deriva de 1e-7 por passo reprova um criterio de entradas (<= 1e-13)", mut4 > 1e-13, mut4)
    # copia do script da impressao digital do kernel confere com o anexo do FREEZE
    it_ok = all(x["ok"] for x in it)
    invalid = [x["autoteste"] for x in it if not x["ok"] and x["INVALIDO_se_falhar"]]
    for x in it:
        log("  autoteste %-4s %s  (medida %s)" % ("ok" if x["ok"] else "FAIL", x["autoteste"], x["medida"]))
    return {"itens": it, "aprovado": it_ok, "motivos_de_INVALIDO": invalid}


# ----------------------------------------------------------------------------------------------
# 5. blocos oticos (um por subitem pre-registrado)
# ----------------------------------------------------------------------------------------------
def bloco_T1o(M, log):
    rng = rng_bloco()
    crits, med = [], {}
    for n in (2, 3, 4, 5, 8):
        I = np.eye(n, dtype=complex)
        r_i = r_iii = m_i = m_iii = 0.0
        mins = []
        for _ in range(200):
            T = cgauss(rng, n)
            H = herm(rng, n)
            Cm = T @ H - H @ T
            vi = abs(np.trace(Cm))
            ti = 1e-10 * (1 + fro(T) * fro(H))
            viii = abs(fro(Cm - 1j * I) ** 2 - fro(Cm) ** 2 - n)
            tiii = 1e-9 * (1 + fro(Cm) ** 2)
            m_i, r_i = max(m_i, vi), max(r_i, vi / ti)
            m_iii, r_iii = max(m_iii, viii), max(r_iii, viii / tiii)
            mins.append(lstsq_min(H))
        mins = np.array(mins)
        dev = float(np.max(np.abs(mins - math.sqrt(n))))
        med["n=%d" % n] = {"max_abs_tr_comutador": m_i, "max_razao_i_sobre_tol": r_i,
                           "min_do_minimo_lstsq": float(mins.min()), "max_do_minimo_lstsq": float(mins.max()),
                           "sqrt_n": math.sqrt(n), "max_abs_iii": m_iii, "max_razao_iii_sobre_tol": r_iii}
        crits.append(crit("(i) n=%d, 200 pares: max |tr(TH-HT)| / [1e-10(1+||T||F||H||F)]" % n, r_i, "<= 1", r_i <= 1,
                          maximo_absoluto=m_i))
        crits.append(crit("(ii) n=%d, 200 H: max |min_T ||TH-HT-i1||_F - sqrt(n)|" % n, dev, "<= 1e-10", dev <= 1e-10,
                          minimo_observado=float(mins.min()), falsificador_minimo_menor_que_sqrt_n_menos_1e10=bool(mins.min() < math.sqrt(n) - 1e-10)))
        crits.append(crit("(iii) n=%d, 200 pares: max | ||C-i1||^2 - ||C||^2 - n | / [1e-9(1+||C||^2)]" % n, r_iii, "<= 1",
                          r_iii <= 1, maximo_absoluto=m_iii))
    # n = 2 com H = H_ot
    H = M["H_ot"]
    I = np.eye(2, dtype=complex)
    r_i = r_iii = m_i = m_iii = 0.0
    for _ in range(200):
        T = cgauss(rng, 2)
        Cm = T @ H - H @ T
        vi = abs(np.trace(Cm))
        ti = 1e-10 * (1 + fro(T) * fro(H))
        viii = abs(fro(Cm - 1j * I) ** 2 - fro(Cm) ** 2 - 2)
        tiii = 1e-9 * (1 + fro(Cm) ** 2)
        m_i, r_i = max(m_i, vi), max(r_i, vi / ti)
        m_iii, r_iii = max(m_iii, viii), max(r_iii, viii / tiii)
    mh = lstsq_min(H)
    med["n=2, H=H_ot"] = {"max_abs_tr_comutador": m_i, "minimo_lstsq": mh, "max_abs_iii": m_iii}
    crits.append(crit("(i) n=2, H=H_ot, 200 T: max |tr|/tol", r_i, "<= 1", r_i <= 1, maximo_absoluto=m_i))
    crits.append(crit("(ii) n=2, H=H_ot: |min - sqrt(2)|", abs(mh - math.sqrt(2)), "<= 1e-10",
                      abs(mh - math.sqrt(2)) <= 1e-10, minimo=mh))
    crits.append(crit("(iii) n=2, H=H_ot, 200 T: max |...|/tol", r_iii, "<= 1", r_iii <= 1, maximo_absoluto=m_iii))
    return crits, med, {}, {}


def bloco_T3o(M, log, controles):
    rng = rng_bloco()
    rho = M["rho1"]
    A = np.array([cgauss(rng, 2) for _ in range(200)])
    crits, med, cf = [], {}, {}
    va = 0.0
    for s in GRADE_T3:
        for t in GRADE_T3:
            X = fluxo_modular(rho, s, fluxo_modular(rho, t, A))
            Y = fluxo_modular(rho, s + t, A)
            va = max(va, float(np.max(fro_lote(X - Y))))
    crits.append(crit("(a) max ||sigma_s(sigma_t(a)) - sigma_{s+t}(a)||_F, 200 a, (s,t) na grade 7x7", va, "<= 1e-10", va <= 1e-10))
    vb = float(np.max(fro_lote(fluxo_modular(rho, 0.0, A) - A)))
    crits.append(crit("(b) max ||sigma_0(a) - a||_F", vb, "<= 1e-10", vb <= 1e-10))
    vc = 0.0
    tra = np.einsum("ij,nji->n", rho, A)
    for t in GRADE_T3:
        trs = np.einsum("ij,nji->n", rho, fluxo_modular(rho, t, A))
        vc = max(vc, float(np.max(np.abs(trs - tra))))
    crits.append(crit("(c) max |tr(rho1 sigma_t(a)) - tr(rho1 a)|, t na grade", vc, "<= 1e-10", vc <= 1e-10))
    B = np.array([cgauss(rng, 2) for _ in range(200)])
    rinv = np.linalg.inv(rho)
    lhs = np.einsum("nii->n", rho @ A @ B)
    rhs = np.einsum("nii->n", rho @ B @ rho @ A @ rinv)
    tol = 1e-10 * (1 + fro_lote(A) * fro_lote(B))
    rd = float(np.max(np.abs(lhs - rhs) / tol))
    crits.append(crit("(d) KMS: max |tr(rho1 ab) - tr(rho1 b rho1 a rho1^-1)| / [1e-10(1+||a||F||b||F)], 200 pares", rd,
                      "<= 1", rd <= 1, maximo_absoluto=float(np.max(np.abs(lhs - rhs)))))
    w1 = M["omega1"]
    ve = max(abs(fluxo_modular(rho, t, E01)[0, 1] - np.exp(1j * t * w1)) for t in GRADE_T3)
    crits.append(crit("(e) max |sigma_t(E01)_01 - e^{i t omega1}|, t na grade", float(ve), "<= 1e-12", ve <= 1e-12))
    med = {"omega1": w1, "P1": M["P1"], "rho1_diag": np.diag(rho).real}
    nc = M["_prereg"]["numeros_de_conferencia"]
    cf = {"omega1": conf(w1, nc["omega1"]), "P1": conf(M["P1"], nc["P1"])}
    # controles C-T3-a, C-T3-b, C-T3-c
    rho2, rinv2 = rho @ rho, rinv @ rinv
    rhs2 = np.einsum("nii->n", rho @ B @ (rho2 @ A @ rinv2))
    gaps = np.abs(lhs - rhs2)
    nfal = int(np.sum(gaps > 1e-6))
    controles["C-T3-a"] = {"criterios": [crit("KMS com Delta_2 = rho1^2 a rho1^-2: no de pares (de 200) com gap > 1e-6", nfal,
                                              ">= 1", nfal >= 1, gap_min=float(gaps.min()), gap_mediana=float(np.median(gaps)),
                                              gap_max=float(gaps.max()))],
                           "comportou_se_como_registrado": nfal >= 1,
                           "leitura": "a KMS com a temperatura errada falha em %d de 200 pares" % nfal}
    g = abs(np.trace(rho @ E01 @ E10) - np.trace(rho @ E10 @ E01))
    controles["C-T3-b"] = {"criterios": [crit("fluxo identidade: |omega(E01 E10) - omega(E10 E01)| (gap)", float(g), ">= 0.5",
                                              g >= 0.5, conferencia_1_menos_2beta=conf(float(g), nc["lam"]))],
                           "comportou_se_como_registrado": g >= 0.5,
                           "leitura": "o fluxo identidade nao e KMS para rho1: gap = %.15f" % g}
    half = 0.5 * I2C
    vt = max(float(np.max(fro_lote(fluxo_modular(half, t, A) - A))) for t in GRADE_T3)
    controles["C-T3-c"] = {"criterios": [crit("estado tracial I/2: max ||sigma_t(a) - a||_F, 200 a, t na grade", vt, "<= 1e-12",
                                              vt <= 1e-12)],
                           "comportou_se_como_registrado": vt <= 1e-12,
                           "leitura": "no estado tracial I/2 o fluxo modular e a identidade (o relogio para)"}
    return crits, med, cf, {}


def bloco_T4o(M, log, controles):
    rng = rng_bloco()
    S, th, lam, beta = M["S"], M["theta_M"], M["lam"], M["beta"]
    nc = M["_prereg"]["numeros_de_conferencia"]
    crits, med, cf, inf = [], {}, {}, {}
    # (O-a)
    oa1 = fro(S.T @ S - I2C)
    oa2 = fro(S.conj().T @ S - I2C)
    dS = complex(np.linalg.det(S))
    sv = np.linalg.svd(S, compute_uv=False)
    crits.append(crit("(O-a) ||S^T S - I||_F", oa1, "<= 1e-12", oa1 <= 1e-12, adjunta=oa2))
    crits.append(crit("(O-a) |det S - 1|", abs(dS - 1), "<= 1e-12", abs(dS - 1) <= 1e-12, detS=dS))
    crits.append(crit("(O-a) max |valor singular de S - 1|", float(np.max(np.abs(sv - 1))), "<= 1e-12",
                      float(np.max(np.abs(sv - 1))) <= 1e-12, valores_singulares=sv))
    # pares de estados (usados em O-b e O-d)
    RHO, SIG = [], []
    for _ in range(500):
        RHO.append(estado(rng, 2))
        SIG.append(estado(rng, 2))
    RHO, SIG = np.array(RHO), np.array(SIG)
    d0 = fro_lote(RHO - SIG)
    ev0 = np.linalg.eigvalsh(RHO)
    pu0 = pureza_lote(RHO)
    prods = {}
    P = S.copy()
    for k in range(1, 1001):
        if k > 1:
            P = P @ S
        if k in (1, 10, 100, 1000):
            prods[k] = P.copy()
    ob = {}
    for k in (1, 10, 100, 1000, 10000):
        caminhos = {"angulo_exato": smat(k * th)}
        if k <= 1000:
            caminhos["produto_repetido"] = prods[k]
        for nome, U in caminhos.items():
            R1, S1 = Ad(U, RHO), Ad(U, SIG)
            di = float(np.max(np.abs(fro_lote(R1 - S1) - d0)))
            de = float(np.max(np.abs(np.linalg.eigvalsh(R1) - ev0)))
            dp = float(np.max(np.abs(pureza_lote(R1) - pu0)))
            ob["k=%d %s" % (k, nome)] = {"isometria": di, "espectro": de, "pureza": dp}
            crits.append(crit("(O-b) k=%d (%s): max | ||S^k(rho-sigma)S^-k||_F - ||rho-sigma||_F |, 500 pares" % (k, nome), di,
                              "<= 1e-10", di <= 1e-10))
            crits.append(crit("(O-b) k=%d (%s): max |espectro(S^k rho S^-k) - espectro(rho)|" % (k, nome), de, "<= 1e-10",
                              de <= 1e-10))
            crits.append(crit("(O-b) k=%d (%s): max |pureza(S^k rho S^-k) - pureza(rho)|" % (k, nome), dp, "<= 1e-10",
                              dp <= 1e-10))
    med["O-b"] = ob
    # (O-c) ilustracao do nao-pouso
    MN = {}
    for N in (100, 1000, 10000):
        ks = np.arange(N, 2 * N + 1)
        ang = ks * th
        U = np.zeros((N + 1, 2, 2), dtype=complex)
        U[:, 0, 0] = np.cos(ang)
        U[:, 0, 1] = np.sin(ang)
        U[:, 1, 0] = -np.sin(ang)
        U[:, 1, 1] = np.cos(ang)
        rk = U @ E00 @ np.conj(np.transpose(U, (0, 2, 1)))
        dif = fro_lote(rk - rk[0])
        MN[N] = float(np.max(dif))
        formula = math.sqrt(2) * float(np.max(np.abs(np.sin(np.arange(0, N + 1) * th))))
        crits.append(crit("(O-c) N=%d: M_N = max_{0<=j<=N} ||rho_{N+j} - rho_N||_F" % N, MN[N], ">= 1.0", MN[N] >= 1.0,
                          formula_sqrt2_max_sen=formula))
        cf["M_N N=%d" % N] = conf(MN[N], nc["noland_M_N"][str(N)])
    cf["M_N minimo"] = conf(min(MN.values()), nc["noland_min"])
    # (O-d) contracao do canal e pouso em I/2
    CR, CS = canal_C(S, RHO), canal_C(S, SIG)
    lhs = fro_lote(CR - CS)
    rhs = lam * d0 + 1e-12
    folga = float(np.max(lhs - rhs))
    crits.append(crit("(O-d) max [ ||C(rho)-C(sigma)||_F - (lambda ||rho-sigma||_F + 1e-12) ], 500 pares", folga, "<= 0",
                      folga <= 0, razao_max_contracao=float(np.max(lhs / d0))))
    X = np.concatenate([RHO, SIG])
    dref = fro_lote(Dmap(X) - 0.5 * I2C)
    Y = X.copy()
    pior, kpior, porK = 0.0, None, {}
    for k in range(1, 4097):
        Y = canal_C(S, Y)
        dk = float(np.max(np.abs(fro_lote(Y - 0.5 * I2C) - lam ** k * dref)))
        if dk > pior:
            pior, kpior = dk, k
        if k in (1, 10, 100, 1000, 2000, 4096):
            porK[k] = dk
    crits.append(crit("(O-d) max_{1<=k<=4096} max_rho | ||C^k(rho) - I/2||_F - lambda^k ||D(rho) - I/2||_F |, 1000 estados",
                      pior, "<= 1e-11", pior <= 1e-11, k_do_max=kpior, por_k=porK))
    cf["lambda"] = conf(lam, nc["lam"])
    cf["lambda^4096"] = conf(lam ** 4096, nc["lam4096"])
    # (O-e) volume
    dT = float(np.linalg.det(M["T"]))
    crits.append(crit("(O-e) |det T - (1 - 2 beta)|", abs(dT - (1 - 2 * beta)), "<= 1e-12", abs(dT - (1 - 2 * beta)) <= 1e-12,
                      detT=dT))
    cf["det T"] = conf(dT, nc["det_T"])
    base = [E00, E11, E01 + E10, 1j * (E01 - E10)]

    def coords(Xh):
        return [Xh[0, 0].real, Xh[1, 1].real, Xh[0, 1].real, Xh[0, 1].imag]

    vols = {}
    for t in (0.5, 1.0, 10.0):
        Mt = np.array([coords(dephase(M["gD"], t, Bk)) for Bk in base]).T
        d4 = float(np.linalg.det(Mt))
        ref = math.exp(-2 * M["g01"] * t)
        vols[t] = d4
        crits.append(crit("(O-e) Davies t=%g: |det_R4(T_t sobre hermitianas) - e^{-2 g01 t}|" % t, abs(d4 - ref), "<= 1e-12",
                          abs(d4 - ref) <= 1e-12, det4=d4, ref=ref))
    cf["vol Davies t=1"] = conf(vols[1.0], nc["vol_davies_t1"])
    # (O-f) boost
    c1, s1 = math.cosh(1.0), math.sinh(1.0)
    det_np = float(np.linalg.det(np.array([[c1, s1], [s1, c1]])))
    det_sc = c1 * c1 - s1 * s1
    crits.append(crit("(O-f) |det B(1) - 1| (numpy.linalg.det, float64)", abs(det_np - 1), "<= 1e-12", abs(det_np - 1) <= 1e-12))
    crits.append(crit("(O-f) |det B(1) - 1| (cosh^2 - sinh^2 escalar, float64)", abs(det_sc - 1), "<= 1e-12",
                      abs(det_sc - 1) <= 1e-12))
    v0, v1 = 1.0, -1.0
    rel_max, f64 = 0.0, {}
    for k in range(1, 11):
        v0, v1 = c1 * v0 + s1 * v1, s1 * v0 + c1 * v1
        nr = math.hypot(v0, v1)
        ref = math.sqrt(2.0) * math.exp(-k)
        rel = abs(nr - ref) / ref
        f64[k] = {"norma": nr, "ref": ref, "rel": rel, "componente_(1,1)": v0 + v1}
        rel_max = max(rel_max, rel)
    crits.append(crit("(O-f) float64 (aritmetica escalar IEEE), k=1..10: max rel | ||B(1)^k(1,-1)|| - sqrt2 e^-k |", rel_max,
                      "<= 1e-9", rel_max <= 1e-9))
    med["O-f float64"] = f64
    ctx = decimal.Context(prec=200)
    one = decimal.Decimal(1)
    e = ctx.exp(one)
    einv = ctx.divide(one, e)
    cD = ctx.divide(ctx.add(e, einv), decimal.Decimal(2))
    sD = ctx.divide(ctx.subtract(e, einv), decimal.Decimal(2))
    w0, w1_ = decimal.Decimal(1), decimal.Decimal(-1)
    dec, normas = {}, []
    for k in range(1, 101):
        w0, w1_ = ctx.add(ctx.multiply(cD, w0), ctx.multiply(sD, w1_)), ctx.add(ctx.multiply(sD, w0), ctx.multiply(cD, w1_))
        nr = ctx.sqrt(ctx.add(ctx.multiply(w0, w0), ctx.multiply(w1_, w1_)))
        normas.append(nr)
        if k in (10, 100):
            ref = ctx.multiply(ctx.sqrt(decimal.Decimal(2)), ctx.exp(decimal.Decimal(-k)))
            rel = ctx.divide(abs(ctx.subtract(nr, ref)), ref)
            dec[k] = {"norma": str(nr)[:70], "rel": str(rel)[:30], "rel_float": float(rel)}
            crits.append(crit("(O-f) decimal 200 digitos, k=%d: rel | ||B(1)^k(1,-1)|| - sqrt2 e^-k |" % k, float(rel), "<= 1e-50",
                              rel <= decimal.Decimal("1e-50")))
    med["O-f decimal"] = dec
    cf["boost k=100 (float da norma decimal)"] = conf(float(normas[99]), nc["boost_k100"])
    cf["boost k=100 decimal (60 digitos)"] = {"calculado_aqui": str(normas[99])[:60],
                                              "preregistro": nc["boost_k100_decimal"][:60],
                                              "iguais_nos_60_primeiros_caracteres": str(normas[99])[:60] == nc["boost_k100_decimal"][:60]}
    det_dec = ctx.subtract(ctx.multiply(cD, cD), ctx.multiply(sD, sD))
    # controle C-T4-a
    dets = {s: math.cosh(s) ** 2 - math.sinh(s) ** 2 for s in (0.5, 1.0, 2.0)}
    okdet = all(abs(v - 1) <= 1e-12 for v in dets.values())
    decresce = all(normas[i + 1] < normas[i] for i in range(len(normas) - 1))
    pousa = normas[-1] < decimal.Decimal("1e-40")
    controles["C-T4-a"] = {"criterios": [
        crit("det B(s) = 1 (float64, s em {0.5,1,2}): max |det - 1|", max(abs(v - 1) for v in dets.values()), "<= 1e-12", okdet),
        crit("det B(1) em decimal 200 digitos: |det - 1|", float(abs(det_dec - 1)), "<= 1e-190", abs(det_dec - 1) <= decimal.Decimal("1e-190")),
        crit("||B(1)^k(1,-1)|| estritamente decrescente em k=1..100 (decimal)", decresce, "True", decresce),
        crit("||B(1)^100(1,-1)|| (decimal) -> 0", float(normas[-1]), "< 1e-40", pousa)],
        "comportou_se_como_registrado": okdet and decresce and pousa,
        "leitura": "o boost conserva volume (det 1) e pousa no raio nulo passado: 'volume conservado => nada pousa' falha (parte numerica; a parte de kernel e do construtor do kernel)"}
    return crits, med, cf, inf


def bloco_T6o(M, log, controles):
    rng = rng_bloco()
    nc = M["_prereg"]["numeros_de_conferencia"]
    tgrid = [0.0, 0.1, 1.0, 10.0]
    dense = [round(0.1 * i, 10) for i in range(201)]
    crits, med, cf = [], {}, {}
    va = vb = vd = 0.0
    nqual, menor_queda = 0, math.inf
    cta = 0.0
    for n in (2, 3, 5):
        va_n = vb_n = vd_n = 0.0
        for _ in range(300):
            rho = estado(rng, n)
            g = taxas_simetricas(rng, n)
            U = unitario(rng, n)
            gs = [g] + ([M["gD"]] if n == 2 else [])
            for gg in gs:
                for t in tgrid:
                    lhs = pureza(dephase(gg, t, rho))
                    rhs = float(np.sum(np.exp(-2 * t * gg) * np.abs(rho) ** 2))
                    va_n = max(va_n, abs(lhs - rhs))
                for grade in (tgrid, dense):
                    P = [pureza(dephase(gg, t, rho)) for t in grade]
                    mn = math.inf
                    for p_ in P:
                        mn = min(mn, p_)
                        vb_n = max(vb_n, p_ - mn)       # P(t2) - min_{t1<=t2} P(t1)
                off = [(i, j) for i in range(n) for j in range(n) if i != j and abs(rho[i, j]) >= 0.05 and gg[i, j] >= 0.01]
                if off:
                    nqual += 1
                    q = pureza(rho) - pureza(dephase(gg, 1.0, rho))
                    menor_queda = min(menor_queda, q)
                dg = Dmap(rho)
                for t in tgrid:
                    cta = max(cta, abs(pureza(dephase(gg, t, dg)) - pureza(dg)))
            vd_n = max(vd_n, abs(pureza(Ad(U, rho)) - pureza(rho)))
        med["n=%d" % n] = {"a_max": va_n, "b_max_subida": vb_n, "d_max": vd_n}
        va, vb, vd = max(va, va_n), max(vb, vb_n), max(vd, vd_n)
    crits.append(crit("(a) max |Tr(T_t rho)^2 - sum e^{-2t g_ij}|rho_ij|^2|, n em {2,3,5} x 300, t em {0,0.1,1,10} (+Davies n=2)", va,
                      "<= 1e-12", va <= 1e-12))
    crits.append(crit("(b) monotonia: max_{t1<=t2} [Tr(T_t2 rho)^2 - Tr(T_t1 rho)^2] (grade de (a) e densa 0..20 passo 0.1)", vb,
                      "<= 1e-14", vb <= 1e-14))
    crits.append(crit("(c) estrita: menor queda Tr rho^2 - Tr(T_1 rho)^2 entre os casos qualificados (|rho_ij|>=0.05 e g_ij>=0.01)",
                      menor_queda, ">= 1e-8", nqual > 0 and menor_queda >= 1e-8, casos_qualificados=nqual))
    crits.append(crit("(d) 300 unitarios por n: max |Tr(U rho U^H)^2 - Tr rho^2|", vd, "<= 1e-12", vd <= 1e-12))
    pe = pureza(dephase(M["gD"], 1.0, PSI_PLUS))
    ref = (1 + math.exp(-2 * M["g01"])) / 2
    crits.append(crit("(e) psi_+, Davies, t=1: |Tr(T_1 psi_+)^2 - (1+e^{-2 g01})/2|", abs(pe - ref), "<= 1e-12",
                      abs(pe - ref) <= 1e-12, valor=pe))
    cf["pureza psi_+ t=1"] = conf(pe, nc["pur_psi_t1"])
    cf["g01"] = conf(M["g01"], nc["g01"])
    controles["C-T6-a"] = {"criterios": [crit("sem coerencia (x = D(rho)): max |pureza(T_t x) - pureza(x)|", cta, "<= 1e-14", cta <= 1e-14)],
                           "comportou_se_como_registrado": cta <= 1e-14,
                           "leitura": "sem coerencia nao ha queda: a queda estrita falha (igualdade)"}
    controles["C-T6-b"] = {"criterios": [crit("sob unitaria: max |Delta Tr rho^2| (900 pares estado/unitario)", vd, "<= 1e-12", vd <= 1e-12)],
                           "comportou_se_como_registrado": vd <= 1e-12,
                           "leitura": "sob a unitaria a queda estrita falha (constancia)"}
    g1 = np.array([[0.0, 1.0], [1.0, 0.0]])
    pm = pureza(dephase(g1, -1.0, PSI_PLUS))
    refm = (1 + math.e ** 2) / 2
    okc = pm > 1.0 and abs(pm - refm) <= 1e-12 * refm
    controles["C-T6-c"] = {"criterios": [crit("t = -1, g = (i!=j -> 1): Tr(T_-1 psi_+)^2", pm, "= (1+e^2)/2 > 1 = Tr psi_+^2", okc,
                                              ref=refm)],
                           "comportou_se_como_registrado": okc,
                           "leitura": "para t < 0 a pureza cresce acima de 1: a monotonia falha (a seta)"}
    return crits, med, cf, {}


def bloco_T7o(M, log, controles):
    rng = rng_bloco()
    nc = M["_prereg"]["numeros_de_conferencia"]
    beta = M["beta"]
    g1 = np.array([[0.0, 1.0], [1.0, 0.0]])          # gamma = 1
    crits, med, cf = [], {}, {}
    chaves = {beta: "neg_beta", 1.0: "neg_1", 10.0: "neg_10"}
    for gt in (beta, 1.0, 10.0):
        Xi = dephase(g1, -gt, PSI_PLUS)
        lm = float(np.linalg.eigvalsh(Xi)[0])
        val = (1 - math.exp(gt)) / 2
        ok = abs(lm - val) <= 1e-12 * (1 + abs(val)) and lm < -1e-10
        crits.append(crit("(a) gamma t=%r: menor autovalor de T_-t psi_+ contra (1-e^{gamma t})/2" % gt, abs(lm - val),
                          "<= 1e-12(1+|v|) e autovalor < -1e-10", ok, autovalor=lm, valor=val))
        cf["(a) gamma t=%r" % gt] = conf(lm, nc[chaves[gt]])
    RH = [estado(rng, 2) for _ in range(100)]
    vb = 0.0
    for gt in (beta, 1.0, 10.0):
        for r in RH:
            vb = max(vb, fro(dephase(g1, -gt, dephase(g1, gt, r)) - r))
    for r in RH:
        vb = max(vb, fro(dephase(M["gD"], -1.0, dephase(M["gD"], 1.0, r)) - r))
    crits.append(crit("(b) max ||T_-t(T_t rho) - rho||_F, 100 estados, gamma t em {beta,1,10} e Davies t=1", vb, "<= 1e-12", vb <= 1e-12))
    Xd = dephase(M["gD"], -1.0, PSI_PLUS)
    lm = float(np.linalg.eigvalsh(Xd)[0])
    val = (1 - math.exp(M["g01"])) / 2
    ok = abs(lm - val) <= 1e-12 * (1 + abs(val)) and lm < -1e-10
    crits.append(crit("(c) Davies g01, t=1: menor autovalor de T_-1 psi_+ contra (1-e^{g01})/2", abs(lm - val),
                      "<= 1e-12(1+|v|) e autovalor < -1e-10", ok, autovalor=lm, valor=val))
    cf["(c) Davies"] = conf(lm, nc["neg_davies"])
    # C-T7-b
    pior_res, pior_ev = 0.0, math.inf
    for p in (0.0, 0.25, 0.5, float(M["rho1"][0, 0].real), 1.0):
        dgm = np.diag([p, 1 - p]).astype(complex)
        for gg, t in [(g1, beta), (g1, 1.0), (g1, 10.0), (M["gD"], 1.0)]:
            Y = dephase(gg, -t, dgm)
            pior_res = max(pior_res, fro(Y - dgm))
            pior_ev = min(pior_ev, float(np.linalg.eigvalsh(Y)[0]))
    okb = pior_res == 0.0 and pior_ev >= -1e-12
    controles["C-T7-b"] = {"criterios": [crit("entrada diagonal: max ||T_-t(diag(p,1-p)) - diag(p,1-p)||_F", pior_res, "== 0", pior_res == 0.0),
                                         crit("entrada diagonal: menor autovalor de T_-t(diag(p,1-p))", pior_ev, ">= -1e-12", pior_ev >= -1e-12)],
                           "comportou_se_como_registrado": okb,
                           "leitura": "T_{-t} fixa a diagonal: a nao positividade falha (autovalores >= 0)"}
    # C-T7-c
    pr, pe_ = 0.0, math.inf
    for n in (2, 3, 5):
        for _ in range(300):
            U = unitario(rng, n)
            r = estado(rng, n)
            Y = Ad(U, r)
            pr = max(pr, fro(U.conj().T @ Y @ U - r))
            pe_ = min(pe_, float(np.linalg.eigvalsh(Y)[0]))
    okc = pr <= 1e-12 and pe_ >= -1e-12
    controles["C-T7-c"] = {"criterios": [crit("Ad(U^H) inverte Ad(U): max ||U^H (U rho U^H) U - rho||_F (900 pares)", pr, "<= 1e-12", pr <= 1e-12),
                                         crit("Ad(U) preserva positividade: menor autovalor de U rho U^H", pe_, ">= -1e-12", pe_ >= -1e-12)],
                           "comportou_se_como_registrado": okc,
                           "leitura": "a unitaria e reversivel como canal: Ad(U*) inverte Ad(U) e preserva positividade"}
    return crits, med, cf, {}


def bloco_T8o(M, log):
    rng = rng_bloco()
    nc = M["_prereg"]["numeros_de_conferencia"]
    T, lam = M["T"], M["lam"]
    crits, med, cf, inf = [], {}, {}, {}
    e0 = np.array([1.0, 0.0])
    pior, kpior, primeiro_piso = 0.0, None, None
    amostra = {}
    for k in range(0, 10001):
        Tk = np.linalg.matrix_power(T, k)
        p = Tk @ e0
        ck = p[0] - p[1]
        err = abs(ck - lam ** k)
        if err > pior:
            pior, kpior = err, k
        if primeiro_piso is None and ck < 1e-15:
            primeiro_piso = k
        if k in (0, 1, 10, 100, 1000, 1419, 5000, 10000):
            amostra[k] = {"c_k": ck, "lambda^k": lam ** k, "dif": err}
    crits.append(crit("(a) max_{0<=k<=10^4} |c_k - lambda^k| (T^k por numpy.linalg.matrix_power)", pior, "<= 1e-13 absoluta",
                      pior <= 1e-13, k_do_max=kpior))
    med["a"] = amostra
    inf["(b) primeiro k com c_k < 1e-15 em float64 [sem veredito]"] = primeiro_piso
    inf["(b) esperado no preregistro"] = nc["k_float_floor"]
    inf["(b) leitura"] = "sombra numerica do abismo, nao um zero; c_k > 0 para todo k e decidido pelo kernel (T8.b(iv), the_fall_never_lands)"
    lnl = math.log(lam)
    ce = {}
    for eps in (1e-1, 1e-3, 1e-6):
        r = math.log(eps) / lnl
        ke = math.floor(r) + 1
        lk = math.exp(ke * lnl)
        lk1 = math.exp((ke - 1) * lnl)
        ok = (lk < eps) and (eps <= lk1)
        ce[repr(eps)] = {"k_eps": ke, "lambda^k_eps": lk, "lambda^(k_eps-1)": lk1, "parte_fracionaria": r - math.floor(r)}
        crits.append(crit("(c) eps=%g: k_eps = floor(ln eps/ln lambda)+1 = %d satisfaz lambda^k_eps < eps <= lambda^(k_eps-1)" % (eps, ke),
                          [lk, eps, lk1], "desigualdades estritas como escritas", ok))
        cf["k_eps %g" % eps] = conf(ke, nc["k_eps"][repr(eps)] if repr(eps) in nc["k_eps"] else nc["k_eps"][str(eps)])
        key = repr(eps) if repr(eps) in nc["frac_eps"] else str(eps)
        cf["frac %g" % eps] = conf(r - math.floor(r), nc["frac_eps"][key])
    med["c"] = ce
    vd = 0.0
    xs = [PSI_PLUS] + [estado(rng, 2) for _ in range(100)]
    for t in (0.1, 1.0, 10.0):
        for x in xs:
            vd = max(vd, abs(abs(dephase(M["gD"], t, x)[0, 1]) - math.exp(-M["g01"] * t) * abs(x[0, 1])))
    crits.append(crit("(d) Davies: max | |x01(t)| - e^{-g01 t}|x01(0)| |, psi_+ e 100 estados, t em {0.1,1,10}", vd, "<= 1e-12",
                      vd <= 1e-12))
    return crits, med, cf, inf


def bloco_T9o(M, log):
    nc = M["_prereg"]["numeros_de_conferencia"]
    T, R, lam, a = M["T"], M["R"], M["lam"], M["a"]
    crits, med, cf, inf = [], {}, {}, {}
    da = fro(T - (R + math.exp(-2 * a) * (IR - R)))
    crits.append(crit("(a) ||T - (R + e^{-2a}(I-R))||_F", da, "<= 1e-15", da <= 1e-15))
    cf["2a"] = conf(2 * a, nc["dois_a"])
    cf["a"] = conf(a, nc["a"])
    nIR = fro(IR - R)
    med["||I-R||_F"] = nIR
    mb = {}
    for t in (1e-6, 1e-3, 0.1, 1.0, 10.0, 30.0):
        Ft = F_lock(M, t)
        m = fro(Ft @ Ft - Ft)
        v = math.exp(-t) * (1 - math.exp(-t)) * nIR
        tol = 1e-12 * v + 1e-15
        crits.append(crit("(b) t=%g: | ||F^2-F||_F - e^-t(1-e^-t)||I-R||_F |" % t, abs(m - v), "<= 1e-12 v + 1e-15 = %.4e" % tol,
                          abs(m - v) <= tol))
        dF = float(np.linalg.det(Ft))
        vd = math.exp(-t)
        told = 1e-12 * vd + 1e-15
        crits.append(crit("(b) t=%g: |det F(t) - e^-t|" % t, abs(dF - vd), "<= 1e-12 v + 1e-15 = %.4e" % told, abs(dF - vd) <= told))
        crits.append(crit("(b) t=%g: falsificador 'F(t) idempotente dentro da tolerancia' nao ocorre" % t, m, "> %.4e" % tol, m > tol))
        mb[t] = {"||F^2-F||_F": m, "valor": v, "det F": dF, "e^-t": vd}
    med["b"] = mb
    pior, kpior, primeiro_acima = 0.0, None, None
    amostra = {}
    svr, rank_min = 0.0, 2
    for k in range(1, 10001):
        Tk = np.linalg.matrix_power(T, k)
        ref = R + lam ** k * (IR - R)
        err = float(np.max(np.abs(Tk - ref)))
        if err > pior:
            pior, kpior = err, k
        if primeiro_acima is None and err > 1e-13:
            primeiro_acima = k
        if k in (1, 10, 100, 500, 1000, 1529, 2000, 5000, 10000):
            amostra[k] = err
        if k <= 1000:
            rk, sv = posto_numerico(Tk)
            rank_min = min(rank_min, rk)
            if k <= 500:
                svr = max(svr, abs(sv[-1] - lam ** k) / lam ** k)
    crits.append(crit("(c) max_{1<=k<=10^4} max_ij |T^k - (R + lambda^k (I-R))| (numpy.linalg.matrix_power)", pior,
                      "<= 1e-13 absoluta", pior <= 1e-13, k_do_max=kpior, primeiro_k_acima_de_1e_13=primeiro_acima, amostra=amostra))
    crits.append(crit("(c) max_{k<=500} rel |s_min(T^k) - lambda^k|", svr, "<= 1e-9", svr <= 1e-9))
    crits.append(crit("(c) posto numerico de T^k (limiar 1e-12 ||T^k||_2) == 2 para todo k <= 1000", rank_min, "== 2", rank_min == 2))
    rR, svR = posto_numerico(R)
    crits.append(crit("(c) posto de R == 1", rR, "== 1", rR == 1, valores_singulares_R=svR))
    primeiro_rank1 = None
    for k in range(1001, 3001):
        rk, _ = posto_numerico(np.linalg.matrix_power(T, k))
        if rk < 2:
            primeiro_rank1 = k
            break
    inf["(c) primeiro k em que o posto numerico cai a 1 [sem veredito]"] = primeiro_rank1
    inf["(c) esperado no preregistro"] = nc["k_rank_drop"]
    inf["(c) leitura"] = "sombra numerica do limite, nao um posto em tempo finito; o kernel decide (T9.b)"
    med["c"] = {"entradas_max_dif": pior, "k_do_max": kpior, "primeiro_k_acima_de_1e-13": primeiro_acima, "amostra": amostra,
                "sv_rel_max_k<=500": svr, "posto_min_k<=1000": rank_min, "posto_R": rR}
    return crits, med, cf, inf


def bloco_T10o(M, log):
    rng = rng_bloco()
    w1, P1, rho, T, R, a = M["omega1"], M["P1"], M["rho1"], M["T"], M["R"], M["a"]
    crits, med, cf, inf = [], {}, {}, {}
    densa = [round(0.01 * i, 10) for i in range(5001)]
    va = 0.0
    for t in GRADE_T3 + densa:
        va = max(va, abs(np.exp(1j * w1 * (t + P1)) - np.exp(1j * w1 * t)))
    crits.append(crit("(a) max |e^{i w1 (t+P1)} - e^{i w1 t}|, t na grade do T3.o e em [0,50] passo 0.01", float(va), "<= 1e-12",
                      va <= 1e-12))
    X = np.array([cgauss(rng, 2) for _ in range(200)])
    vb = 0.0
    for t in GRADE_T3:
        vb = max(vb, float(np.max(np.abs(np.abs(fluxo_modular(rho, t, X)) - np.abs(X)))))
    crits.append(crit("(b) max | |sigma_t(x)_ij| - |x_ij| |, 200 x, t na grade do T3.o", vb, "<= 1e-12", vb <= 1e-12))
    c = np.array([math.exp(-2 * a * t) for t in densa])
    dif = c[:-1] - c[1:]
    okc = bool(np.all(dif > 0)) and len(set(c.tolist())) == len(c)
    crits.append(crit("(c) c(t) = e^{-2at} em [0,50] passo 0.01: menor diferenca consecutiva (estrita) e injetividade", float(dif.min()),
                      "> 0 (float64) e valores distintos", okc, n_pontos=len(c), n_distintos=len(set(c.tolist()))))
    d1, d2 = fro(T @ R - R), fro(R @ T - R)
    crits.append(crit("(d) ||TR - R||_F", d1, "<= 1e-12", d1 <= 1e-12))
    crits.append(crit("(d) ||RT - R||_F", d2, "<= 1e-12", d2 <= 1e-12))
    return crits, med, cf, inf


def bloco_T11o(M, log, controles):
    nc = M["_prereg"]["numeros_de_conferencia"]
    S, lam, beta = M["S"], M["lam"], M["beta"]
    crits, med, cf, inf = [], {}, {}, {}
    X = E00.copy()
    om = {}
    dform = 0.0
    for k in range(1, 1001):
        X = canal_C(S, X)
        ck = float((X[0, 0] - X[1, 1]).real)
        om[k] = 2 * math.atanh(ck)
        dform = max(dform, float(np.max(np.abs(X - np.diag([(1 + lam ** k) / 2, (1 - lam ** k) / 2])))))
    for k in (1, 10, 100, 1000):
        ref = 2 * math.atanh(lam ** k)
        tol = 1e-13 + 1e-12 * abs(ref)
        crits.append(crit("(a) k=%d: |omega_k(medido no canal iterado) - 2 artanh(lambda^k)|" % k, abs(om[k] - ref), "<= %.4e" % tol,
                          abs(om[k] - ref) <= tol, omega_medido=om[k], omega_ref=ref))
        cf["omega_k k=%d" % k] = conf(om[k], nc["omega_k"][str(k)])
    dec = all(om[k] > om[k + 1] for k in range(1, 1000))
    crits.append(crit("(b) omega_k(medido) estritamente decrescente para 1<=k<=1000", dec, "True", dec,
                      menor_decremento=min(om[k] - om[k + 1] for k in range(1, 1000))))
    w1 = math.log((1 - beta) / beta)
    crits.append(crit("(c) k=1: rel |omega_1(medido) - ln((1-beta)/beta)|", abs(om[1] - w1) / w1, "<= 1e-12 relativa",
                      abs(om[1] - w1) / w1 <= 1e-12))
    inf["max_k<=1000 |C^k(|0><0|) - diag((1+lambda^k)/2,(1-lambda^k)/2)| [sem veredito; forma de rho_k]"] = dform
    rho = M["rho1"]
    x = fluxo_modular(rho, math.pi / M["omega1"], E01)
    v = abs(x[0, 1] - 1.0)
    controles["C-T11-a"] = {"criterios": [crit("|sigma_{pi/w1}(E01)_01 - 1| (rho1 nao tracial)", float(v), ">= 1 (esperado 2)", v >= 1)],
                            "comportou_se_como_registrado": v >= 1,
                            "leitura": "fora do atrator o relogio nao para: |sigma_{pi/w1}(E01)_01 - 1| = %.15f" % v}
    return crits, med, cf, inf


# ----------------------------------------------------------------------------------------------
# 6. anexo: achados fora do pre-registro (varreduras e diagnosticos; SEM veredito)
# ----------------------------------------------------------------------------------------------
def anexo(M, log):
    import mpmath
    beta, R = M["beta"], M["R"]
    out = {"documento": "ACHADOS FORA DO PRE-REGISTRO — F1.TEMPO, face otica, rodada 2",
           "estatuto": "[REAL — medido aqui, modelo sintetico, SEM veredito] salvo marca em contrario; nada aqui altera um veredito pre-registrado",
           "achados": {}}
    A = out["achados"]
    # V1: varredura do parametro p no lugar de beta (bordas incluidas)
    v1 = []
    for p in [0.0, 1e-12, 1e-6, 1e-3, beta, 0.05, 0.1, 0.25, 0.4, 0.49, 0.5, 0.6, 0.9, 1.0]:
        th = math.asin(math.sqrt(p))
        S = smat(th)
        T = np.array([[canal_C(S, Ej)[i, i].real for Ej in (E00, E11)] for i in range(2)])
        lp = 1 - 2 * p
        rk, sv = posto_numerico(T)
        reg = {"p": p, "lambda": lp, "det_T": float(np.linalg.det(T)),
               "||T-(R+lambda(I-R))||_F": fro(T - (R + lp * (IR - R))),
               "posto_numerico_T": rk, "||T^2-T||_F": fro(T @ T - T),
               "T_e_F(2a)_com_a_real": lp > 0, "fator_de_contracao_|lambda|": abs(lp)}
        if 0 < p < 1:
            reg["omega_1 = ln((1-p)/p)"] = math.log((1 - p) / p)
        v1.append(reg)
    A["V1_varredura_do_parametro"] = {
        "o_que": "a mesma construcao (S = Smat(asin sqrt p), C = D Ad(S) D, T = populacoes de C) com p no lugar de beta",
        "linhas": v1,
        "leitura": ("[DERIVED + REAL medido] Bordas: p = 0 da T = I (sem vazamento: nada se move, lambda = 1, nao ha contracao; o estado |0><0| e puro e "
                    "o fluxo modular nao se define). p = 1/2 da lambda = 0 e T = R: idempotente e de posto 1 ja em k = 1 — corresponde a 2a = +inf, "
                    "isto e, ao LIMITE do fluxo, nao a um tempo finito. p > 1/2 da lambda < 0: T nao e F(t) para t real algum (o contraste troca de "
                    "sinal a cada passo). A identificacao T = F(2a) do T9.o exige 0 < lambda <= 1, isto e, 0 <= p < 1/2; beta ~ 0.012 esta dentro.")}
    # V2: varredura de tempo do fluxo do lock (a sombra numerica)
    v2 = []
    for t in [0.0, 1e-15, 1e-12, 1e-9, 1e-6, 1e-3, 0.1, 1.0, 10.0, 27.0, 28.0, 30.0, 36.0, 37.0, 38.0, 40.0, 50.0, 100.0, 700.0, 745.0, 746.0]:
        Ft = F_lock(M, t)
        rk, sv = posto_numerico(Ft)
        v2.append({"t": t, "e^-t": math.exp(-t), "||F^2-F||_F": fro(Ft @ Ft - Ft), "det F": float(np.linalg.det(Ft)),
                   "posto_numerico_(limiar 1e-12)": rk, "F(t) == R bit a bit": bool(np.array_equal(Ft, R))})
    A["V2_varredura_do_tempo_do_fluxo"] = {
        "linhas": v2,
        "leitura": ("[REAL medido] Em t = 0, F = I e idempotente (posto pleno; o controle C-T9-b, do kernel). Para t > ~27,6 o posto 'numerico' "
                    "(limiar 1e-12) cai a 1 e, para t >= ~38, F(t) e R bit a bit em float64: a SOMBRA numerica do limite (RP18), nao um posto em "
                    "tempo finito. A grade pre-registrada do T9.o(b) para em t = 30, dentro do intervalo legivel.")}
    # V3: o inverso da defasagem perto da borda gamma t = 0
    v3 = []
    g1 = np.array([[0.0, 1.0], [1.0, 0.0]])
    for gt in [0.0, 1e-15, 1e-12, 1e-9, 1e-6, beta, 0.1, 1.0, 10.0, 50.0, 700.0]:
        Xi = dephase(g1, -gt, PSI_PLUS)
        lm = float(np.linalg.eigvalsh(Xi)[0])
        v3.append({"gamma_t": gt, "menor_autovalor_T_-t_psi_+": lm, "(1-e^{gamma t})/2": (1 - math.exp(gt)) / 2})
    A["V3_inverso_da_defasagem_perto_da_borda"] = {
        "linhas": v3,
        "leitura": ("[REAL medido] Em gamma t = 0 o menor autovalor e 0 (o inverso e a identidade: C-T7-a); para todo gamma t > 0 ele e negativo e "
                    "cresce em modulo como (e^{gamma t} - 1)/2. Abaixo de ~1e-10 a negatividade existe mas nao passa o limiar -1e-10 do criterio — por "
                    "isso a grade pre-registrada comeca em gamma t = beta.")}
    # V4: o relogio modular perto do estado tracial
    v4 = []
    for p in [0.5, 0.5 + 1e-12, 0.5 + 1e-9, 0.5 + 1e-6, 0.6, 1 - beta, 0.99, 1 - 1e-6, 1 - 1e-12]:
        rp = np.diag([p, 1 - p]).astype(complex)
        w = math.log(p / (1 - p))
        v4.append({"p": p, "omega = ln(p/(1-p))": w, "periodo 2pi/omega": (2 * math.pi / w) if w != 0 else "inf",
                   "|sigma_1(E01)_01 - 1|": float(abs(fluxo_modular(rp, 1.0, E01)[0, 1] - 1))})
    A["V4_relogio_modular_perto_do_tracial"] = {
        "linhas": v4,
        "leitura": ("[REAL medido] Quando o estado se aproxima do tracial (p -> 1/2) a frequencia modular vai a 0 e o periodo diverge; em p = 1/2 "
                    "o fluxo e a identidade (o relogio para: T11, C-T3-c). Na face finita, so no atrator tracial. Nao se estende a III_1 (RP06).")}
    # V5: a FALHA do T9.o(c) — sensibilidade a representacao float64 de T e conferencia exata
    lam = M["lam"]
    th = M["theta_M"]
    construcoes = {
        "Smat (cos/sin) -> |S|^2 [a do ensaio]": M["T"],
        "S na forma raiz [[sqrt(1-b), sqrt b],...] -> |S|^2": (lambda s, c: np.array([[c * c, s * s], [s * s, c * c]]))(math.sqrt(beta), math.sqrt(1 - beta)),
        "[[1-b, b],[b, 1-b]] direto": np.array([[1 - beta, beta], [beta, 1 - beta]]),
        "R + lambda(I-R) direto": R + lam * (IR - R),
    }
    mpmath.mp.dps = 60
    v5 = {}
    for nome, Tc in construcoes.items():
        pior, kp, prim = 0.0, None, None
        for k in range(1, 10001):
            err = float(np.max(np.abs(np.linalg.matrix_power(Tc, k) - (R + lam ** k * (IR - R)))))
            if err > pior:
                pior, kp = err, k
            if prim is None and err > 1e-13:
                prim = k
        soma = [mpmath.mpf(float(Tc[0, 0])) + mpmath.mpf(float(Tc[0, 1])) - 1, mpmath.mpf(float(Tc[1, 0])) + mpmath.mpf(float(Tc[1, 1])) - 1]
        delta = soma[0]
        # potencia EXATA (60 digitos) da matriz float64 representada, contra R + lambda_fl^k (I-R)
        Tm = mpmath.matrix([[mpmath.mpf(float(Tc[i, j])) for j in range(2)] for i in range(2)])
        Pk = Tm ** 10000
        lamk = mpmath.mpf(lam) ** 10000
        Rm = mpmath.matrix([[0.5, 0.5], [0.5, 0.5]])
        Im = mpmath.eye(2)
        refm = Rm + lamk * (Im - Rm)
        exato = max(abs(Pk[i, j] - refm[i, j]) for i in range(2) for j in range(2))
        v5[nome] = {"T": Tc, "soma_da_linha_menos_1_(exata, delta)": mpmath.nstr(delta, 6),
                    "previsao_k_delta/2_em_k=10^4": mpmath.nstr(10000 * delta / 2, 6),
                    "float64_matrix_power: max_k<=10^4 max_ij dif": pior, "k_do_max": kp, "primeiro_k_acima_de_1e-13": prim,
                    "potencia_EXATA_da_matriz_representada_em_k=10^4: max_ij dif": mpmath.nstr(exato, 6),
                    "passaria_1e-13": pior <= 1e-13}
    bm = mpmath.mpf(beta)
    Tex = mpmath.matrix([[1 - bm, bm], [bm, 1 - bm]])
    Pex = Tex ** 10000
    lex = (1 - 2 * bm) ** 10000
    Rm = mpmath.matrix([[0.5, 0.5], [0.5, 0.5]])
    refx = Rm + lex * (mpmath.eye(2) - Rm)
    exid = max(abs(Pex[i, j] - refx[i, j]) for i in range(2) for j in range(2))
    A["V5_T9o_c_sensibilidade_a_representacao"] = {
        "construcoes": v5,
        "identidade_exata_T^k = R + lambda^k(I-R) com beta exato (60 digitos), k = 10^4: max_ij dif": mpmath.nstr(exid, 6),
        "leitura": ("[REAL medido + DERIVED] A FALHA pre-registrada do T9.o(c) e a do float64, nao a da identidade: com aritmetica exata a "
                    "identidade vale (dif ~ 1e-60 ou menos); a potencia exata da matriz float64 REPRESENTADA ja se afasta de R + lambda^k(I-R) por "
                    "~k|delta|/2, porque a soma das linhas de T em float64 e 1 + delta (|delta| ~ 1e-16). As quatro construcoes equivalentes "
                    "em aritmetica exata dao deltas diferentes; a do ensaio (Smat, a definicao do kernel, a mesma da rodada 1) excede 1e-13. "
                    "Nenhuma construcao alternativa entra no veredito: mudar a construcao depois de conhecer o resultado seria escolher o caminho "
                    "pelo desfecho. A tolerancia 1e-13 do T9.o(c) esta abaixo da sombra numerica de 10^4 passos (achado A1 da rodada 1); mudar o "
                    "criterio exige ADENDO congelado antes de um reensaio (decisao da gerencia)."),
    }
    mpmath.mp.dps = 15
    # V6: dependencia do caminho aritmetico no boost (O-f)
    c1, s1 = math.cosh(1.0), math.sinh(1.0)
    B = np.array([[c1, s1], [s1, c1]])
    v6 = {"escalar_IEEE": {}, "numpy_B@v": {}, "matrix_power(B,k)@v0": {}}
    v0, v1_ = 1.0, -1.0
    vv = np.array([1.0, -1.0])
    for k in range(1, 41):
        v0, v1_ = c1 * v0 + s1 * v1_, s1 * v0 + c1 * v1_
        vv = B @ vv
        vm = np.linalg.matrix_power(B, k) @ np.array([1.0, -1.0])
        ref = math.sqrt(2.0) * math.exp(-k)
        if k in (1, 5, 10, 15, 20, 30, 40):
            v6["escalar_IEEE"][k] = abs(math.hypot(v0, v1_) - ref) / ref
            v6["numpy_B@v"][k] = abs(float(np.hypot(*vv)) - ref) / ref
            v6["matrix_power(B,k)@v0"][k] = abs(float(np.hypot(*vm)) - ref) / ref
    A["V6_boost_caminho_aritmetico"] = {
        "erro_relativo_por_k": v6,
        "leitura": ("[REAL medido] Na aritmetica escalar IEEE (a do ensaio, escolhida antes por reprodutibilidade) o iterado (x, -x) fica "
                    "exatamente antissimetrico (fl(a-b) = -fl(b-a)): a direcao nula futura nunca e povoada e o erro relativo cresce so "
                    "linearmente. Por matrix_power (quadrados) a direcao instavel e povoada pelo arredondamento e amplificada por ~e^{2k}: e a "
                    "instabilidade da sela (RP02), numerica, nao matematica. Por isso o pre-registro limitou o float64 a k <= 10 e usou decimal "
                    "de 200 digitos para k = 100.")}
    # V7: o achado A4 medido (posto de I/2 x posto de R)
    rI, svI = posto_numerico(0.5 * IR)
    rR, svR = posto_numerico(R)
    pops = [np.array([1.0, 0.0]), np.array([0.3, 0.7]), np.array([0.5, 0.5])]
    A["V7_posto_do_atrator_e_do_limite"] = {
        "posto_de_I/2": rI, "valores_singulares_I/2": svI, "posto_de_R=J/2": rR, "valores_singulares_R": svR,
        "R aplicado a vetores de populacao": {str(p.tolist()): (R @ p).tolist() for p in pops},
        "leitura": ("[REAL medido + DERIVED] O ESTADO-atrator I/2 tem posto 2 (invertivel); o posto 1 e o do MAPA-limite R = J/2 = lim T^k "
                    "(sobre vetores de populacao), cuja imagem e a reta gerada por (1/2, 1/2), isto e, o estado I/2. Chamar I/2 de 'o posto' "
                    "(S46.4 do pre-registro) e homonimo pela regua POSTO = RANK (achado A4); o que tem posto 1 e o mapa R, e o seu conjunto "
                    "imagem, de dimensao 1, e {I/2}.")}
    # V8: o achado A5(i) medido — o canal esquece as populacoes; a defasagem pura as guarda
    rng = np.random.default_rng(SEMENTE + 2)
    pares = [(estado(rng, 2), estado(rng, 2)) for _ in range(100)]
    S = M["S"]
    esquece = {}
    Yr = np.array([r for r, _ in pares])
    Ys = np.array([s for _, s in pares])
    for k in range(1, 1001):
        Yr, Ys = canal_C(S, Yr), canal_C(S, Ys)
        if k in (1, 100, 1000):
            esquece[k] = float(np.max(fro_lote(Yr - Ys)))
    guarda = {}
    for t in (1.0, 100.0, 1e4):
        guarda[t] = max(abs(fro(Dmap(dephase(M["gD"], t, r) - dephase(M["gD"], t, s))) - fro(Dmap(r - s))) for r, s in pares)
    A["V8_esquecer_e_lembrar"] = {
        "canal_C: max ||C^k(rho) - C^k(sigma)||_F (100 pares)": esquece,
        "defasagem_de_Davies: max | ||D(T_t rho - T_t sigma)|| - ||D(rho - sigma)|| | (100 pares)": guarda,
        "leitura": ("[REAL medido] O atrator otico I/2 ESQUECE as populacoes (a diferenca entre dois estados vai a 0 como lambda^k): e o "
                    "'repousar' do T11. A defasagem pura GUARDA as populacoes (a diagonal e invariante, para todo t): e o 'ser lembrada' do T5. "
                    "Sao duas dinamicas distintas; no canal C as duas coisas nao acontecem juntas (achado A5(i) da auditoria da rodada 1, aqui medido).")}
    # V9: regra dos dois regimes no ensaio (o que se pediu ao angulo)
    A["V9_dois_regimes_no_ensaio"] = {
        "leitura": ("[REAL — inspecao do proprio ensaio] Nenhum limite foi pedido ao angulo: no regime do ANGULO (Ad(S^k), fluxo modular, "
                    "fase e^{i w t}) mediram-se isometria, espectro, pureza, periodicidade e o NAO-pouso (O-c: M_N >= 1). Limites so na FACE: "
                    "C^k -> I/2 (O-d), T^k -> R (T9.o), c_k -> 0 (T8.o), omega_k -> 0 (T11.o), B(1)^k(1,-1) -> 0 (O-f). O fluxo modular finito "
                    "e unitario E periodico (periodo P1): o separador usado aqui e a direcao (compacta x hiperbolica), nao 'unitario' (achado A3).")}
    return out


# ----------------------------------------------------------------------------------------------
# 7. fio principal
# ----------------------------------------------------------------------------------------------
def nova_tentativa(modo):
    base = os.path.join(OUT, "tentativas")
    os.makedirs(base, exist_ok=True)
    nums = [int(m.group(1)) for d in os.listdir(base) for m in [re.match(r"tentativa_(\d{3})_", d)] if m]
    n = (max(nums) + 1) if nums else 1
    d = os.path.join(base, "tentativa_%03d_%s" % (n, modo))
    os.makedirs(d, exist_ok=False)
    return d, n


def impressao_digital(destino, log):
    cp = subprocess.run([sys.executable, "-I", FP_COPIA, destino], capture_output=True, timeout=900)
    if cp.returncode != 0:
        raise RuntimeError("impressao digital do kernel falhou: %r" % cp.stderr[-500:])
    d = json.load(open(destino, encoding="utf-8"))
    log("  kernel: %d arquivos, meta %s, src %s (%.1f s)" % (d["files"], d["meta_sha256"][:16], d["src_sha256"][:16], d["seconds"]))
    return d


def main():
    global SEMENTE
    ap = argparse.ArgumentParser()
    ap.add_argument("--modo", choices=["autoteste", "ensaio"], required=True)
    args = ap.parse_args()
    t0 = time.time()
    tdir, ntent = nova_tentativa(args.modo)
    log = Log(os.path.join(tdir, "run_optico.log"))
    runner_sha, runner_bytes = sha256_file(os.path.abspath(__file__))
    res = {
        "documento": "RESULTADO_OPTICO — F1.TEMPO (o tempo que nao se deixa nomear), face otica, RODADA 2",
        "unidade": "F1.TEMPO", "trilha": "TEMPO", "gerencia": "c1",
        "papel": "construtor otico, rodada 2 (subagente do workflow posto-e-tempo da gerencia c1)",
        "estatuto_do_documento": ("[REAL — medido aqui, modelo sintetico] por subitem; PASSA = validade matematica na face testada, nao "
                                  "creditacao; sem veredito global; o gate nao se move; beta na natureza a 5 sigma nao e tocado; nenhum dado observado."),
        "rodada": 2,
        "relacao_com_a_rodada_1": ("Reensaio AO LADO, contra o mesmo FREEZE e sem ADENDO; a rodada 1 (2_OPTICO\\RESULTADO_OPTICO.json) nao foi "
                                   "tocada e nao e substituida. Todas as tentativas se preservam."),
        "tentativa": ntent, "modo": args.modo, "pasta_da_tentativa": tdir,
        "inicio_utc": agora_utc(),
        "ambiente": {"python": sys.version, "numpy": np.__version__, "plataforma": platform.platform(), "flags": str(sys.flags)},
        "runner": {"arquivo": os.path.abspath(__file__), "sha256": runner_sha, "bytes": runner_bytes},
    }
    try:
        import mpmath
        res["ambiente"]["mpmath"] = mpmath.__version__
    except ImportError:
        res["ambiente"]["mpmath"] = None
    try:
        cfg = np.show_config(mode="dicts")
        res["ambiente"]["blas"] = cfg.get("Build Dependencies", {}).get("blas", {}).get("name")
    except Exception:
        res["ambiente"]["blas"] = None
    valido, motivos = True, []
    try:
        log("== F1.TEMPO face otica, rodada 2, tentativa %d (%s) ==" % (ntent, args.modo))
        log("runner sha256 %s (%d B)" % (runner_sha, runner_bytes))
        ok, itens, fz, pj = conferir_freeze()
        res["conferencia_freeze"] = {"n": len(itens), "falhas": [i for i in itens if not i["ok"]], "todos_ok": ok}
        log("FREEZE: %d itens, %d falhas" % (len(itens), sum(1 for i in itens if not i["ok"])))
        if not ok:
            res["valido"] = False
            res["motivos_de_INVALIDO"] = ["FREEZE diverge: nao se ensaia"]
            raise SystemExit(2)
        prereg = json.loads(pj.decode("utf-8"))
        msem = re.search(r"default_rng\((\d+)\)", prereg["modelo_otico"]["sementes"])
        SEMENTE = int(msem.group(1))
        res["semente"] = SEMENTE
        # copia de bytes do script da impressao digital (anexo conferido do FREEZE)
        fp_anexo = [a for a in fz["anexos"] if a["caminho"] == "scripts/fingerprint_kernel.py"][0]
        if not os.path.exists(FP_COPIA):
            os.makedirs(os.path.dirname(FP_COPIA), exist_ok=True)
            with open(FP_COPIA + ".tmp", "wb") as fo:
                fo.write(open(FP_ORIG, "rb").read())
            os.replace(FP_COPIA + ".tmp", FP_COPIA)
        fps, _ = sha256_file(FP_COPIA)
        res["script_impressao_digital"] = {"copia": FP_COPIA, "sha256": fps, "sha256_do_anexo_no_FREEZE": fp_anexo["sha256"],
                                           "confere": fps == fp_anexo["sha256"]}
        if fps != fp_anexo["sha256"]:
            valido = False
            motivos.append("copia do script da impressao digital nao confere com o anexo do FREEZE")
        beta, binfo = ler_beta(prereg, log)
        res["beta"] = binfo
        M = construir_modelo(beta)
        M["_prereg"] = prereg
        res["modelo"] = {k: v for k, v in M.items() if not k.startswith("_")}
        res["escolhas_do_construtor_[INPUT]"] = ESCOLHAS
        log("modelo: theta_M=%r lambda=%r a=%r omega1=%r g01=%r" % (M["theta_M"], M["lam"], M["a"], M["omega1"], M["g01"]))
        log("autotestes:")
        at = autotestes(M, binfo, log)
        res["autotestes"] = at
        if at["motivos_de_INVALIDO"]:
            valido = False
            motivos += at["motivos_de_INVALIDO"]
        if not at["aprovado"]:
            valido = False
            motivos.append("runner nao aprovado nos autotestes")
        if args.modo == "autoteste":
            res["valido"] = valido
            res["motivos_de_INVALIDO"] = motivos
            res["nota"] = "modo autoteste: nenhum subitem pre-registrado foi medido nesta tentativa"
            raise SystemExit(0 if valido else 2)
        log("impressao digital do kernel (inicio):")
        fpa = impressao_digital(os.path.join(tdir, "FINGERPRINT_OPTICO_R2_ANTES.json"), log)
        # ---- os blocos ----
        subs = {s["id"]: (a["id"], s) for a in prereg["afirmacoes"] for s in a["subitens"]}
        controles = {}
        blocos = [("T1.o", lambda: bloco_T1o(M, log)), ("T3.o", lambda: bloco_T3o(M, log, controles)),
                  ("T4.o", lambda: bloco_T4o(M, log, controles)), ("T6.o", lambda: bloco_T6o(M, log, controles)),
                  ("T7.o", lambda: bloco_T7o(M, log, controles)), ("T8.o", lambda: bloco_T8o(M, log)),
                  ("T9.o", lambda: bloco_T9o(M, log)), ("T10.o", lambda: bloco_T10o(M, log)),
                  ("T11.o", lambda: bloco_T11o(M, log, controles))]
        res_sub = {}
        for sid, fn in blocos:
            ts = time.time()
            crits, med, cf, inf = fn()
            afid, s = subs[sid]
            todos = all(c["ok"] for c in crits)
            res_sub[sid] = {"id": sid, "afirmacao": afid, "obrigatorio": s["obrigatorio"], "face": s["face"],
                            "enunciado": s["enunciado"], "procedimento": s["procedimento"],
                            "tolerancia_preregistrada": s["tolerancia"], "falsificador": s["falsificador"],
                            "esperado_preregistrado": s["esperado"], "criterios": crits, "medidas": med, "conferencia": cf,
                            "informativo_sem_veredito": inf, "n_criterios": len(crits), "todos_os_criterios_ok": todos,
                            "criterios_fora_da_tolerancia": [c["nome"] for c in crits if not c["ok"]],
                            "segundos": round(time.time() - ts, 2),
                            "resultado": "PASSA" if todos else "FALHA",
                            "estatuto": "[REAL — medido aqui, modelo sintetico]"}
            log("%-6s %-5s (%d criterios; %.1f s)%s" % (sid, res_sub[sid]["resultado"], len(crits), time.time() - ts,
                                                        "" if todos else "  fora: " + "; ".join(res_sub[sid]["criterios_fora_da_tolerancia"])))
        # controles: completar metadados do pre-registro
        cmeta = {c["id"]: c for c in prereg["controles"]}
        res_ctl = {}
        for cid in sorted(controles):
            c = dict(controles[cid])
            c.update({"id": cid, "face": cmeta[cid]["face"], "liga": cmeta[cid]["liga"], "enunciado": cmeta[cid]["enunciado"],
                      "esperado_preregistrado": cmeta[cid]["esperado"],
                      "parte_desta_face": "numerica (a parte de kernel, quando existe, e do construtor do kernel)"})
            res_ctl[cid] = c
            log("%-8s %s" % (cid, "comportou-se como registrado" if c["comportou_se_como_registrado"] else "NAO se comportou como registrado"))
        oticos_esperados = sorted(cid for cid, c in cmeta.items() if "otico" in c["face"])
        faltando = [c for c in oticos_esperados if c not in res_ctl]
        if faltando:
            valido = False
            motivos.append("controles oticos pre-registrados sem medida: %s" % faltando)
        log("impressao digital do kernel (fim):")
        fpd = impressao_digital(os.path.join(tdir, "FINGERPRINT_OPTICO_R2_DEPOIS.json"), log)
        iguais = fpa["meta_sha256"] == fpd["meta_sha256"] and fpa["src_sha256"] == fpd["src_sha256"]
        res["impressao_digital_kernel"] = {"inicio": {k: fpa[k] for k in ("files", "bytes", "lean_src_files", "meta_sha256", "src_sha256")},
                                           "fim": {k: fpd[k] for k in ("files", "bytes", "lean_src_files", "meta_sha256", "src_sha256")},
                                           "iguais": iguais,
                                           "igual_a_do_FREEZE": fpa["meta_sha256"] == fz["kernel_impressao_digital"]["depois"]["meta"]
                                           and fpa["src_sha256"] == fz["kernel_impressao_digital"]["depois"]["src"]}
        if not iguais:
            valido = False
            motivos.append("impressao digital do kernel alterada durante o ensaio")
        if not valido:
            for sid in res_sub:
                res_sub[sid]["resultado_medido"] = res_sub[sid]["resultado"]
                res_sub[sid]["resultado"] = "INVALIDO"
        res["valido"] = valido
        res["motivos_de_INVALIDO"] = motivos
        res["subitens_oticos"] = res_sub
        res["controles_oticos"] = res_ctl
        res["controles_oticos_todos_como_registrado"] = all(c["comportou_se_como_registrado"] for c in res_ctl.values())
        # por afirmacao (face otica)
        pa = {}
        for a in prereg["afirmacoes"]:
            oticos = {s["id"]: res_sub[s["id"]]["resultado"] for s in a["subitens"] if s["face"] == "otico"}
            ctl = {cid: ("comportou-se como registrado" if c["comportou_se_como_registrado"] else "NAO se comportou como registrado")
                   for cid, c in res_ctl.items() if a["id"] in [x.strip() for x in c["liga"].split(",")]}
            cit = {s["id"]: "CITADA (entra por citacao; nunca PASSA de teste)" for s in a["subitens"] if s["face"] == "citacao"}
            lei = {s["id"]: "LEITURA (entra marcada; nunca PASSA de teste)" for s in a["subitens"] if s["face"] == "leitura"}
            kern = ["%s (%s)" % (s["id"], "obrigatorio" if s["obrigatorio"] else "opcional") for s in a["subitens"] if s["face"] == "kernel"]
            if not valido:
                rf = "INVALIDO"
            elif not oticos:
                rf = "SEM_FACE_OTICA"
            elif all(v == "PASSA" for v in oticos.values()) and all(v.startswith("comportou") for v in ctl.values()):
                rf = "PASSA"
            else:
                rf = "FALHA"
            obrig_falha = [sid for sid, v in oticos.items() if v == "FALHA" and res_sub[sid]["obrigatorio"]]
            if obrig_falha:
                va = "FALHA (subitem obrigatorio %s em FALHA; pela regra congelada a face kernel nao reverte)" % ", ".join(obrig_falha)
            elif rf == "INVALIDO":
                va = "INVALIDO"
            else:
                va = "pendente da face kernel (construtor do kernel); esta tabela e so a face otica"
            pa[a["id"]] = {"titulo": a["titulo"], "subitens_oticos": oticos, "controles_oticos_ligados": ctl,
                           "resultado_da_face_otica": rf, "citadas": cit, "leituras": lei,
                           "subitens_de_kernel_fora_deste_ensaio": kern, "veredito_da_afirmacao": va}
        res["por_afirmacao_face_otica"] = pa
        # o que fica [ONTO], [KNOWN], [OPEN], [DECLARADO]
        cont = {}
        cl = {"ONTO": [], "KNOWN": [], "OPEN": [], "DECLARADO": []}
        for f in prereg["mapeamento_frases"]:
            for c in f["clausulas"]:
                for tag in re.findall(r"\[([^\]]+)\]", c["marca"]):
                    cont[tag] = cont.get(tag, 0) + 1
                for k in cl:
                    if k in c["marca"]:
                        cl[k].append({"frase": f["frase"], "trecho": c["trecho"], "marca": c["marca"], "objeto_ou_leitura": c["objeto_ou_leitura"]})
        exc = [{"excerto": e["excerto"], "marca": e["marca"]} for e in prereg["mapeamento_excertos"]
               if "ONTO" in e["marca"] or "DECLARADO" in e["marca"]]
        res["onto_known_open"] = {
            "nota": ("O ensaio otico nao testa leitura nem literatura: o que esta marcado [ONTO] entra como LEITURA, o [KNOWN] como CITADA, "
                     "o [OPEN] como ABERTA; nenhum recebe PASSA de teste. Contagem por etiqueta (uma clausula pode ter mais de uma)."),
            "contagem_de_etiquetas_nas_69_clausulas": cont,
            "clausulas": cl,
            "excertos_ONTO_ou_DECLARADO": exc,
            "subitens_CITADA_LEITURA": {s["id"]: ("CITADA" if s["face"] == "citacao" else "LEITURA")
                                        for a in prereg["afirmacoes"] for s in a["subitens"] if s["face"] in ("citacao", "leitura")},
            "ABERTA": "o 'ciclo limite' de S46.3 (RP09): nao tipado no canone; o dephasing finito puro nao tem espectro periferico fora de 1; nenhum teste aqui",
        }
        res["regra"] = prereg["regra_de_decisao"]
        # anexo
        log("anexo (achados fora do pre-registro):")
        an = anexo(M, log)
        an_path = os.path.join(tdir, "ACHADOS_FORA_DO_PREREGISTRO.json")
        s_an, b_an = gravar_json(an_path, an)
        res["anexo_achados_fora_do_preregistro"] = {"arquivo": an_path, "sha256": s_an, "bytes": b_an}
        log("  anexo gravado (%d B, sha256 %s)" % (b_an, s_an))
    except SystemExit as e:
        res.setdefault("valido", valido)
        res.setdefault("motivos_de_INVALIDO", motivos)
        log("encerrado (%s)" % e.code)
    except Exception:
        tb = traceback.format_exc()
        log("ERRO DE INFRA:\n" + tb)
        res["valido"] = False
        res["motivos_de_INVALIDO"] = motivos + ["erro de infraestrutura do runner (ver traceback)"]
        res["erro_de_infra"] = tb
    res["fim_utc"] = agora_utc()
    res["segundos"] = round(time.time() - t0, 1)
    nome = "RESULTADO_OPTICO.json" if args.modo == "ensaio" else "RESULTADO_AUTOTESTE.json"
    rp = os.path.join(tdir, nome)
    s_r, b_r = gravar_json(rp, res)
    log("resultado gravado: %s (%d B, sha256 %s); %.1f s" % (rp, b_r, s_r, res["segundos"]))
    log.fechar()
    return 0 if res.get("valido") else 2


ESCOLHAS = [
    "E1  Um gerador novo numpy.random.default_rng(SEMENTE) por bloco de teste; SEMENTE lida do PREREGISTRO.json (modelo_otico.sementes). Os autotestes e o anexo usam SEMENTE+1 e SEMENTE+2 (nao interferem nos blocos).",
    "E2  S = Smat(theta_M) = cos(theta_M)*1 + sin(theta_M)*Grot (a definicao do kernel, SMatrix.lean), theta_M = asin(sqrt(beta)); C = D o Ad(S) o D literalmente; T = matriz das populacoes de C, T_ij = (C(E_jj))_ii = |S_ij|^2; rho1 = C(|0><0|). Para S e T e a mesma construcao da rodada 1 (um reensaio nao troca o objeto); fixada ANTES de rodar. A sensibilidade do T9.o(c) a outras construcoes equivalentes vai ao anexo (V5), sem veredito.",
    "E3  T4.o (O-d): k = 1..4096 (C iterado) sobre os DOIS membros dos 500 pares (1000 estados); k = 0 fica fora (C^0 = id nao age nas coerencias). Os 500 pares sao os mesmos do (O-b).",
    "E4  T4.o (O-f), float64, k <= 10: iteracao v <- B(1) v em aritmetica escalar IEEE-754 do Python (cada operacao corretamente arredondada; sem BLAS, sem FMA), por reprodutibilidade; os caminhos BLAS e matrix_power vao ao anexo (V6). det B(1) e exigido pelos dois caminhos (numpy.linalg.det e cosh^2 - sinh^2).",
    "E5  T6.o: 300 estados POR n (n em {2,3,5}); taxas: entradas acima da diagonal uniformes em [0,1], espelhadas, diagonal zero, um sorteio por estado (ordem: estado, taxas, unitario); para n = 2 tambem a taxa de Davies nos mesmos estados; (b) na grade de (a) e numa grade densa t = 0..20 passo 0.1, todos os pares t1 <= t2.",
    "E6  T7.o (a)-(b): taxa gamma = 1 e t = gamma t; (b) para gamma t em {beta, 1, 10} e Davies em t = 1.",
    "E7  T10.o (a): t na grade do T3.o e na grade [0, 50] passo 0.01 do T10.o (c).",
    "E8  T3.o: as 200 matrizes a de (a)-(c) sao as mesmas de (d), pareadas com 200 b novas; (c) e (e) com t na grade do T3.o. T8.o (d): psi_+ e 100 estados aleatorios (n = 2).",
    "E9  T1.o: (ii) e medido por H (T livre) e o residuo e calculado explicitamente como ||Lx - b||; para n = 2, alem dos 200 pares, 200 T com H = H_ot. T complexa geral; H = (A + A^H)/2.",
    "E10 T9.o (c): ||T^k|| no limiar do posto numerico = norma de operador (maior valor singular); k = 1..10^4 para as entradas; o informativo do posto procura k em 1001..3000.",
    "E11 beta: literal da unica atribuicao nao indentada de ALPHA_FINE_CODATA_2018 (regex nos bytes), ONE da atribuicao seguinte, expressao BETA_TGL conferida como texto; beta = alpha * ONE * sqrt(e) nessa ordem; conferido com SEALED_CODATA_ALPHA (l.95) e com o PREREGISTRO.json.",
    "E12 Ad(U) rho = U rho U^H; S^{-k} := (S^k)^H. Em (O-b) S^k pelo angulo exato e Smat(k theta_M); por produto repetido, S multiplicado k vezes.",
    "E13 Rodada 2 gravada ao lado, em 2_OPTICO\\rodada_2; a rodada 1 nao e tocada. Cada invocacao do runner abre uma pasta de tentativa nova; nada se apaga.",
]


if __name__ == "__main__":
    sys.exit(main())
