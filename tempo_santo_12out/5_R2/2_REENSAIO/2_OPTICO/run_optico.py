# -*- coding: utf-8 -*-
r"""
run_optico.py -- F1.TEMPO (trilha TEMPO; gerencia c1; programa IALD / TGL): a FACE OTICA.
Papel: construtor otico (subagente do workflow posto-e-tempo da gerencia c1).

Ensaio SINTETICO: numpy float64 (decimal de 200 digitos so onde o pre-registro manda; mpmath e scipy
so nos autotestes). Nenhum dado observado, nenhum provedor remoto, nenhuma chamada paga, nenhuma
ferramenta de calculo da Bancada. NAO executa o um.py: le os BYTES (regex + ast.parse, sem exec).
beta NUNCA literal: alpha e lido dos bytes do um.py e beta = alpha*ONE*sqrt(e) e calculado em runtime;
o valor de conferencia vem do PREREGISTRO.json congelado e so confere.

Uso:  python -B -E -P -X utf8 run_optico.py           (ensaio completo; grava uma tentativa nova)
      python -B -E -P -X utf8 run_optico.py --infra   (so preflight, beta e autotestes; nenhum subitem)

Escreve SO dentro de 2_OPTICO: tentativas/tentativa_NNN_<modo>/{RESULTADO_OPTICO.json,
ACHADOS_FORA_DO_PREREGISTRO.json, run_optico.log}; no ensaio completo copia esses bytes para
2_OPTICO/RESULTADO_OPTICO.json, ACHADOS_FORA_DO_PREREGISTRO.json e run_optico.log. Tentativas
anteriores nunca sao apagadas.

ESCOLHAS DO CONSTRUTOR [INPUT do construtor], fixadas ANTES da primeira rodada (o pre-registro deixa
estes pontos em aberto; nenhuma muda tolerancia, mapeamento ou esperado):
 E1  Um gerador novo numpy.random.default_rng(SEMENTE) por bloco de teste (cada bloco reprodutivel
     isoladamente). A semente e a do pre-registro, lida do PREREGISTRO.json (20261012).
 E2  S = Smat(theta_M) = cos(theta_M)*1 + sin(theta_M)*Grot (definicao do kernel, SMatrix.lean), com
     theta_M = arcsin(sqrt(beta)); T = |S|^2 entrada a entrada (a matriz das populacoes de C).
 E3  T4.o (O-d): k = 1..4096 (C iterado). Em k = 0 nao ha iteracao (C^0 = id) e a igualdade nao se
     aplica as coerencias; a borda k = 0 vai ao anexo.
 E4  T4.o (O-f), float64, k <= 10: a orbita v <- B(1) v iterada em aritmetica IEEE-754 ESCALAR do
     Python (cada operacao corretamente arredondada; sem BLAS, sem FMA), para que o numero seja
     reprodutivel em qualquer maquina. Os caminhos BLAS (B @ v) e numpy.linalg.matrix_power sao medidos
     e vao ao anexo, com o mesmo criterio, para o auditor ver a dependencia do caminho aritmetico.
 E5  T6.o: 300 estados POR n (n em {2,3,5}); (b) na grade de (a) e tambem numa grade densa
     t = 0..20, passo 0,1, com minimo corrente (todos os pares t1 <= t2).
 E6  T7.o (a)-(b): taxa gamma = 1 e t = gamma*t; (b) para gamma*t em {beta, 1, 10} e Davies em t = 1.
 E7  T10.o (a): t na grade do T3.o e tambem na grade [0, 50] de passo 0,01 do T10.o (c).
 E8  T3.o (c): t na grade do T3.o.  T8.o (d): psi_+ e 100 estados aleatorios (n = 2).
 E9  T1.o: para n = 2, alem dos 200 pares aleatorios, 200 T aleatorias com H = H_ot.
 E10 Escopo da leitura de alpha: a linha fisica nao indentada l.5557 (unica) esta DENTRO do modulo
     embutido como texto (_NIVEL2_MCMC_FILES) no um.py, e e conferida contra SEALED_CODATA_ALPHA da AST
     de topo do um.py (l.95), como na errata R2/R3 do leitor da F1.ATRATOR.
"""
import ast
import hashlib
import json
import math
import os
import platform
import re
import shutil
import sys
import time
import traceback
from decimal import Decimal, localcontext

import numpy as np

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(HERE) != "2_OPTICO":
    sys.stderr.write("RECUSA: o runner so roda dentro de 2_OPTICO\n")
    sys.exit(2)

PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO"
FREEZE_PATH = os.path.join(PRE, "FREEZE.json")
FREEZE_SHA256 = "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b"
FREEZE_BYTES = 5986
OPER_PATH = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
OPER_SHA16_GERENCIA = "2c8b7b712aa9ad7f"
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
KERNEL_ROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
LONG = "\\\\?\\"

SEED = None  # lido do PREREGISTRO.json
I2 = np.eye(2, dtype=complex)
GROT = np.array([[0, 1], [-1, 0]], dtype=complex)
E00 = np.array([[1, 0], [0, 0]], dtype=complex)
E11 = np.array([[0, 0], [0, 1]], dtype=complex)
E01 = np.array([[0, 1], [0, 0]], dtype=complex)
E10 = np.array([[0, 0], [1, 0]], dtype=complex)
PSI_PLUS = 0.5 * np.ones((2, 2), dtype=complex)
GRID_T3 = [-3.0, -1.0, -0.1, 0.0, 0.1, 1.0, 3.0]


# ----------------------------------------------------------------------------- utilidades
class Log:
    def __init__(self):
        self.lines = []
        self.fh = None

    def open(self, path):
        self.fh = open(path, "a", encoding="utf-8", newline="\n")

    def __call__(self, msg):
        line = time.strftime("%Y-%m-%d %H:%M:%S") + "  " + msg
        self.lines.append(line)
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


def read_bytes(p):
    with open(p, "rb") as fh:
        return fh.read()


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


def fro(x):
    return float(np.linalg.norm(x))


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, bool):
        return o
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, (np.floating, float)):
        f = float(o)
        if math.isfinite(f):
            return f
        return "inf" if f > 0 else ("-inf" if f < 0 else "nan")
    if isinstance(o, (np.complexfloating, complex)):
        return {"re": jsonable(float(o.real)), "im": jsonable(float(o.imag))}
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, Decimal):
        return str(o)
    return o


def write_json_atomic(path, obj):
    if os.path.commonpath([os.path.abspath(path), HERE]) != HERE:
        raise RuntimeError("escrita fora de 2_OPTICO recusada: " + path)
    data = (json.dumps(jsonable(obj), ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    if os.path.getsize(tmp) != len(data):
        raise RuntimeError("tamanho do temporario nao confere: " + tmp)
    os.replace(tmp, path)
    return sha256_bytes(data), len(data)


def copy_bytes_atomic(src, dst):
    if os.path.commonpath([os.path.abspath(dst), HERE]) != HERE:
        raise RuntimeError("escrita fora de 2_OPTICO recusada: " + dst)
    data = read_bytes(src)
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
    nums = []
    for d in os.listdir(base):
        m = re.match(r"^tentativa_(\d{3})_", d)
        if m:
            nums.append(int(m.group(1)))
    n = 1 + max(nums or [0])
    path = os.path.join(base, "tentativa_%03d_%s" % (n, mode))
    os.makedirs(path)  # nunca reaproveita uma pasta existente
    return path, n


# ----------------------------------------------------------------------------- objetos do modelo
def Smat(theta):
    return complex(math.cos(theta)) * I2 + complex(math.sin(theta)) * GROT


def Dmap(x):
    """defasagem completa na base computacional (anula as coerencias); aceita pilhas (..., n, n)."""
    return x * np.eye(x.shape[-1])


def Ad(U, x):
    return U @ x @ U.conj().T


def Cmap(S, x):
    """C = D o Ad(S) o D (o sistema aberto da F1.ATRATOR)."""
    return Dmap(Ad(S, Dmap(x)))


def dephase(g, t, x):
    """forma canonica do kernel (Ergodicity.dephase): (T_t x)_ij = exp(-(t*g_ij)) * x_ij."""
    return np.exp(-(t * np.asarray(g, dtype=float))) * x


class ModularFlow:
    """sigma_t(a) = rho^{it} a rho^{-it}, rho^{it} = exp(it log rho) (ModularFlow.lean: modPow, sigma)."""

    def __init__(self, rho):
        w, V = np.linalg.eigh(rho)
        if float(np.min(w)) <= 0.0:
            raise ValueError("rho nao e positiva-definida")
        self.w = w
        self.V = V
        self.logw = np.log(w)

    def modpow(self, t):
        return (self.V * np.exp(1j * t * self.logw)) @ self.V.conj().T

    def sigma(self, t, a):
        return self.modpow(t) @ a @ self.modpow(-t)


def axiom_flow(P, t):
    n = P.shape[0]
    return P + math.exp(-t) * (np.eye(n) - P)


def boost_f64(s):
    return np.array([[math.cosh(s), math.sinh(s)], [math.sinh(s), math.cosh(s)]])


def cgauss(rng, shape):
    return (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / math.sqrt(2.0)


def rand_state(rng, n):
    A = cgauss(rng, (n, n))
    Mx = A @ A.conj().T
    return Mx / np.trace(Mx).real


def rand_unitary(rng, n):
    Z = cgauss(rng, (n, n))
    Q, Rr = np.linalg.qr(Z)
    d = np.diag(Rr)
    return Q * (d / np.abs(d))


def rand_herm(rng, n):
    A = cgauss(rng, (n, n))
    return (A + A.conj().T) / 2.0


def rand_rates(rng, n):
    U = rng.uniform(0.0, 1.0, (n, n))
    g = np.triu(U, 1)
    return g + g.T


def rng_new():
    return np.random.default_rng(SEED)


def tr2(x):
    return complex(np.trace(x @ x))


def build_model(beta):
    m = {"beta": beta}
    m["theta_M"] = math.asin(math.sqrt(beta))
    m["S"] = Smat(m["theta_M"])
    m["H_ot"] = 1j * GROT
    m["T"] = np.abs(m["S"]) ** 2
    m["R"] = np.full((2, 2), 0.5)
    m["lam"] = 1.0 - 2.0 * beta
    m["a"] = -math.log(m["lam"]) / 2.0
    m["rho1"] = np.diag([1.0 - beta, beta]).astype(complex)
    m["omega1"] = math.log((1.0 - beta) / beta)
    m["P1"] = 2.0 * math.pi / m["omega1"]
    m["g01"] = beta * abs(math.log((1.0 - beta) / beta))
    m["Gdav"] = np.array([[0.0, m["g01"]], [m["g01"], 0.0]])
    m["G1"] = np.array([[0.0, 1.0], [1.0, 0.0]])
    return m


# ----------------------------------------------------------------------------- registro por subitem
def find_subitem(prereg, sid):
    for a in prereg["afirmacoes"]:
        for s in a["subitens"]:
            if s["id"] == sid:
                return s, a
    raise KeyError(sid)


def find_control(prereg, cid):
    for c in prereg["controles"]:
        if c["id"] == cid:
            return c
    raise KeyError(cid)


class Sub:
    def __init__(self, sid, prereg):
        item, af = find_subitem(prereg, sid)
        self.d = {"id": sid, "afirmacao": af["id"], "obrigatorio": item["obrigatorio"], "face": item["face"],
                  "enunciado": item["enunciado"], "procedimento": item.get("procedimento"),
                  "tolerancia_preregistrada": item["tolerancia"], "falsificador": item["falsificador"],
                  "esperado_preregistrado": item["esperado"], "criterios": [], "medidas": {},
                  "conferencia": {}, "informativo_sem_veredito": {}}

    def crit(self, nome, medida, limite, ok):
        self.d["criterios"].append({"nome": nome, "medida": medida, "limite": limite, "ok": bool(ok)})
        LOG("   [%s] %-4s %s | medida=%s | limite=%s" % (self.d["id"], "ok" if ok else "NAO", nome,
                                                         fmt(medida), limite))
        return bool(ok)

    def med(self, k, v):
        self.d["medidas"][k] = v

    def conf(self, k, ours, theirs):
        dif = abs(float(ours) - float(theirs))
        self.d["conferencia"][k] = {"calculado_aqui": ours, "preregistro": theirs, "dif_abs": dif,
                                    "dif_rel": (dif / abs(float(theirs))) if float(theirs) != 0.0 else None}

    def info(self, k, v):
        self.d["informativo_sem_veredito"][k] = v

    def done(self):
        self.d["n_criterios"] = len(self.d["criterios"])
        self.d["todos_os_criterios_ok"] = all(c["ok"] for c in self.d["criterios"])
        return self.d


class Ctl:
    def __init__(self, cid, prereg):
        c = find_control(prereg, cid)
        self.d = {"id": cid, "face": c["face"], "liga": c["liga"], "enunciado": c["enunciado"],
                  "esperado_preregistrado": c["esperado"], "medidas": {}, "comportou_se_como_registrado": None,
                  "parte_desta_face": "numerica (a parte de kernel, quando existe, e do construtor do kernel)"}

    def med(self, k, v):
        self.d["medidas"][k] = v

    def done(self, ok, leitura):
        self.d["comportou_se_como_registrado"] = bool(ok)
        self.d["leitura"] = leitura
        LOG("   [%s] %s — %s" % (self.d["id"], "comportou-se como registrado" if ok else "NAO se comportou como registrado", leitura))
        return self.d


def fmt(x):
    if isinstance(x, float):
        return "%.6e" % x
    return str(x)


# ----------------------------------------------------------------------------- preflight, beta, impressao digital
def preflight():
    checks = []

    def chk(item, got, exp, compact=False):
        ok = (got == exp)
        checks.append({"item": item, "esperado": ("(texto pre-registrado)" if compact else exp),
                       "lido": ("(igual)" if (compact and ok) else got), "ok": bool(ok)})
        return ok

    fb = read_bytes(FREEZE_PATH)
    chk("FREEZE.json sha256", sha256_bytes(fb), FREEZE_SHA256)
    chk("FREEZE.json bytes", len(fb), FREEZE_BYTES)
    fz = json.loads(fb.decode("utf-8"))
    chk("FREEZE congelado_antes_de_qualquer_ensaio", fz.get("congelado_antes_de_qualquer_ensaio"), True)
    chk("FREEZE nenhum_teste_rodado", fz.get("nenhum_teste_rodado"), True)
    chk("FREEZE kernel antes==depois", fz.get("kernel_impressao_digital", {}).get("iguais"), True)
    for key in ("preregistro_json", "preregistro_md"):
        ent = fz[key]
        s, n = sha_file(ent["arquivo"])
        chk(key + " sha256", s, ent["sha256"])
        chk(key + " bytes", n, ent["bytes"])
    for a in fz["anexos"]:
        p = os.path.join(PRE, a["caminho"].replace("/", os.sep))
        s, n = sha_file(p)
        chk("anexo " + a["caminho"] + " sha256", s, a["sha256"])
        chk("anexo " + a["caminho"] + " bytes", n, a["bytes"])
    pre_raw = read_bytes(fz["preregistro_json"]["arquivo"])
    chk("PREREGISTRO.json relido: sha256", sha256_bytes(pre_raw), fz["preregistro_json"]["sha256"])
    prereg = json.loads(pre_raw.decode("utf-8"))
    to = prereg["texto_do_operador"]
    ob = read_bytes(OPER_PATH)
    so = sha256_bytes(ob)
    chk("texto do operador 12/10: sha256 (PREREGISTRO)", so, to["sha256"])
    chk("texto do operador 12/10: sha16 (gerencia)", so[:16], OPER_SHA16_GERENCIA)
    chk("texto do operador 12/10: bytes", len(ob), to["bytes"])
    sp = to["segunda_parte"]
    p2 = ob[sp["byte_offset"]: sp["byte_offset"] + sp["bytes"]]
    chk("segunda parte: vai ate o fim do arquivo", sp["byte_offset"] + sp["bytes"], len(ob))
    chk("segunda parte: sha256", sha256_bytes(p2), sp["sha256"])
    chk("segunda parte: comeca na frase pre-registrada", p2.decode("utf-8").startswith(sp["inicio"]), True)
    chk("numero de frases", len(to["frases"]), to["n_frases"])
    for f in to["frases"]:
        seg = ob[f["byte_offset"]: f["byte_offset"] + f["bytes"]]
        chk("frase %s: sha256" % f["id"], sha256_bytes(seg), f["sha256"])
        chk("frase %s: texto" % f["id"], seg.decode("utf-8"), f["texto"], compact=True)
    return checks, prereg, fz


def read_beta(prereg):
    raw = read_bytes(UMPY)
    sha = sha256_bytes(raw)
    text = raw.decode("utf-8")
    pat = re.compile(r"^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([^\r\n#]+?)[ \t]*\r?$", re.MULTILINE)
    hits = list(pat.finditer(text))
    out = {"um_py": UMPY, "um_py_sha256": sha, "um_py_bytes": len(raw),
           "um_py_sha256_do_preregistro": prereg["beta"]["um_py_sha256"],
           "um_py_igual_ao_do_preregistro": sha == prereg["beta"]["um_py_sha256"],
           "n_linhas_fisicas_nao_indentadas_ALPHA_FINE_CODATA_2018": len(hits), "executou_um_py": False}
    if len(hits) != 1:
        out["confere"] = False
        out["erro"] = "linha de alpha nao unica"
        return out
    h = hits[0]
    line_no = text.count("\n", 0, h.start()) + 1
    assign = ast.parse(h.group(0).strip()).body[0]
    alpha = ast.literal_eval(assign.value)
    lines = text.split("\n")
    l_one = lines[line_no].rstrip("\r")
    l_beta = lines[line_no + 1].rstrip("\r")
    one_node = ast.parse(l_one.strip()).body[0]
    one_ok = isinstance(one_node, ast.Assign) and getattr(one_node.targets[0], "id", None) == "ONE"
    ONE = ast.literal_eval(one_node.value) if one_ok else None
    beta_line_ok = (l_beta.strip() == "BETA_TGL = ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)")
    tree = ast.parse(text)
    sealed = [n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == "SEALED_CODATA_ALPHA" for t in n.targets)]
    outer_alpha = [n for n in tree.body if isinstance(n, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == "ALPHA_FINE_CODATA_2018" for t in n.targets)]
    container = None
    for n in tree.body:
        if n.lineno <= line_no <= (n.end_lineno or n.lineno):
            container = {"tipo": type(n).__name__, "linha_ini": n.lineno, "linha_fim": n.end_lineno,
                         "alvos": [getattr(t, "id", None) for t in getattr(n, "targets", [])]}
            break
    sealed_val = ast.literal_eval(sealed[0].value) if len(sealed) == 1 else None
    beta = alpha * ONE * math.sqrt(math.e) if one_ok else float("nan")
    conf = prereg["beta"]["beta_conferencia"]
    dif = abs(beta - conf)
    out.update({"linha_alpha": line_no, "linha_alpha_preregistro": prereg["beta"]["linha_alpha"],
                "alpha_literal": h.group(1), "alpha_literal_preregistro": prereg["beta"]["alpha_literal"],
                "alpha": alpha, "linha_ONE": line_no + 1, "ONE": ONE, "linha_BETA_TGL": line_no + 2,
                "expressao_BETA_TGL_confere": beta_line_ok,
                "escopo": "linha fisica nao indentada dentro do no de topo %s (modulo embutido como texto); "
                          "conferida contra SEALED_CODATA_ALPHA da AST de topo do um.py" % (container,),
                "no_de_topo_que_contem_a_linha": container,
                "ALPHA_FINE_CODATA_2018_na_AST_de_topo_externa": len(outer_alpha),
                "SEALED_CODATA_ALPHA_linha": sealed[0].lineno if len(sealed) == 1 else None,
                "SEALED_CODATA_ALPHA": sealed_val, "alpha_igual_SEALED": (sealed_val == alpha),
                "sqrt_e": math.sqrt(math.e), "beta_runtime": beta, "beta_conferencia": conf,
                "dif_abs_conferencia": dif,
                "confere": bool(one_ok and beta_line_ok and sealed_val == alpha and dif <= 1e-15),
                "estatuto": "[REAL — medido aqui; beta calculado em runtime; a conferencia so confere]"})
    return out


def kernel_fingerprint():
    t0 = time.time()
    meta = hashlib.sha256()
    src = hashlib.sha256()
    n = nbytes = nlean = 0
    for dp, dn, fn in os.walk(LONG + KERNEL_ROOT):
        dn.sort()
        for f in sorted(fn):
            lp = os.path.join(dp, f)
            st = os.stat(lp)
            rel = os.path.relpath(lp, LONG + KERNEL_ROOT).replace("\\", "/")
            meta.update(("%s\t%d\t%d\n" % (rel, st.st_size, st.st_mtime_ns)).encode("utf-8"))
            n += 1
            nbytes += st.st_size
            if rel.endswith(".lean") and not rel.startswith(".lake/"):
                with open(lp, "rb") as fh:
                    hh = hashlib.sha256(fh.read()).hexdigest()
                src.update(("%s\t%s\n" % (rel, hh)).encode("utf-8"))
                nlean += 1
    return {"root": KERNEL_ROOT, "files": n, "bytes": nbytes, "lean_src_files": nlean,
            "meta_sha256": meta.hexdigest(), "src_sha256": src.hexdigest(),
            "seconds": round(time.time() - t0, 1), "taken_at": time.strftime("%Y-%m-%d %H:%M:%S")}


# ----------------------------------------------------------------------------- autotestes do runner
def autotests(M, prereg):
    res = []

    def at(nome, medida, limite, ok, invalida=False):
        res.append({"nome": nome, "medida": medida, "limite": limite, "ok": bool(ok),
                    "condicao_de_INVALIDO_preregistrada": invalida})
        LOG("   [autoteste] %-4s %s | %s | %s" % ("ok" if ok else "NAO", nome, fmt(medida), limite))

    beta = M["beta"]
    S = M["S"]
    T = M["T"]
    lam = M["lam"]
    e = fro(S.conj().T @ S - I2)
    at("S unitaria: ||S^H S - I||_F", e, "<= 1e-12", e <= 1e-12, invalida=True)
    rng = rng_new()
    worst = 0.0
    for _ in range(200):
        rho = rand_state(rng, 2)
        worst = max(worst, abs(np.trace(Cmap(S, rho)) - np.trace(rho)))
    at("traco de C preservado (200 estados)", worst, "<= 1e-12", worst <= 1e-12, invalida=True)
    Ssq = np.array([[math.sqrt(1 - beta), math.sqrt(beta)], [-math.sqrt(beta), math.sqrt(1 - beta)]], dtype=complex)
    e = fro(S - Ssq)
    at("Smat(theta_M) == [[sqrt(1-b), sqrt b], [-sqrt b, sqrt(1-b)]]", e, "<= 1e-14", e <= 1e-14)
    Tref = np.array([[1 - beta, beta], [beta, 1 - beta]])
    e = fro(T - Tref)
    at("T = |S|^2 == [[1-b, b], [b, 1-b]]", e, "<= 1e-14", e <= 1e-14)
    rng = rng_new()
    worst = 0.0
    for _ in range(50):
        p = rng.uniform(0, 1)
        out = Cmap(S, np.diag([p, 1 - p]).astype(complex))
        worst = max(worst, fro(np.diag(out).real - T @ np.array([p, 1 - p])), fro(out - np.diag(np.diag(out))))
    at("C nas populacoes == T p, sem coerencias", worst, "<= 1e-14", worst <= 1e-14)
    try:
        from scipy.linalg import expm
        e1 = fro(S - expm(M["theta_M"] * GROT))
        e2 = fro(S - expm(-1j * M["theta_M"] * M["H_ot"]))
        X = np.array([[0.0, 1.0], [1.0, 0.0]])
        e3 = fro(T - expm(M["a"] * (X - np.eye(2))))
        at("S == exp(theta_M Grot) == exp(-i theta_M H_ot)", max(e1, e2), "<= 1e-14", max(e1, e2) <= 1e-14)
        at("T == exp[a(X - I)], a = -ln(lambda)/2", e3, "<= 1e-14", e3 <= 1e-14)
    except Exception as exc:  # scipy ausente: autoteste falha visivel
        at("scipy.linalg.expm disponivel", repr(exc), "importavel", False)
    mf = ModularFlow(M["rho1"])
    worst = 0.0
    for t in GRID_T3:
        U = mf.modpow(t)
        ref = np.diag([np.exp(1j * t * math.log(1 - beta)), np.exp(1j * t * math.log(beta))])
        worst = max(worst, fro(U - ref), fro(U.conj().T @ U - I2))
    worst = max(worst, fro(mf.modpow(0.0) - I2))
    at("rho1^{it}: forma fechada diag(d^{it}), unitario, rho^{i0} = 1", worst, "<= 1e-14", worst <= 1e-14)
    g = np.array([[0.0, 0.3, 1.7], [0.3, 0.0, 2.0], [1.7, 2.0, 0.0]])
    x = np.arange(9).reshape(3, 3) * (1 + 0.5j)
    t = 0.7
    ref = np.array([[math.exp(-(t * g[i, j])) * x[i, j] for j in range(3)] for i in range(3)])
    e = fro(dephase(g, t, x) - ref) / fro(ref)
    at("dephase == exp(-(t g_ij)) x_ij (3x3 a mao; relativa)", e, "<= 1e-15", e <= 1e-15)
    worst = 0.0
    for d, n in (([1.0, 2.0], 2), ([1.0, 1.0, 2.0], 3), ([0.5, -1.0, 2.0, 3.0], 4)):
        H = np.diag(d).astype(complex)
        I = np.eye(n, dtype=complex)
        L = np.kron(H.T, I) - np.kron(I, H)
        b = (1j * I).reshape(-1, order="F")
        v = np.linalg.lstsq(L, b, rcond=None)[0]
        worst = max(worst, abs(fro(L @ v - b) - math.sqrt(n)))
    at("lstsq: min ||TH-HT-i1||_F = sqrt(n) em H diagonal a mao", worst, "<= 1e-12", worst <= 1e-12)
    rng = rng_new()
    worst = 0.0
    for n in (2, 3, 5):
        H = rand_herm(rng, n)
        Tm = cgauss(rng, (n, n))
        I = np.eye(n, dtype=complex)
        L = np.kron(H.T, I) - np.kron(I, H)
        worst = max(worst, fro(L @ Tm.reshape(-1, order="F") - (Tm @ H - H @ Tm).reshape(-1, order="F")))
    at("vec coluna: L vec(T) == vec(TH - HT)", worst, "<= 1e-13", worst <= 1e-13)
    try:
        import mpmath
        mpmath.mp.dps = 60
        with localcontext() as ctx:
            ctx.prec = 200
            e_dec = Decimal(1).exp()
            e_mp = mpmath.e
            d1 = abs(mpmath.mpf(str(e_dec)[:70]) - e_mp)
            d2 = abs(float(e_dec) - math.e)
        at("Decimal exp(1) (200 dig.) vs mpmath e", float(d1), "<= 1e-58", float(d1) <= 1e-58)
        at("Decimal exp(1) vs math.e", d2, "<= 1e-15", d2 <= 1e-15)
        # avalia a EXATIDAO DA AVALIACAO das formas fechadas: entradas = os floats exatos (lam, g01, beta)
        mb = mpmath.mpf(beta)
        ml = mpmath.mpf(lam)
        mg = mpmath.mpf(M["g01"])
        refs = {
            "lam^4096": (lam ** 4096, ml ** 4096),
            "omega_1": (2 * math.atanh(lam), 2 * mpmath.atanh(ml)),
            "omega_10": (2 * math.atanh(lam ** 10), 2 * mpmath.atanh(ml ** 10)),
            "omega_100": (2 * math.atanh(lam ** 100), 2 * mpmath.atanh(ml ** 100)),
            "omega_1000": (2 * math.atanh(lam ** 1000), 2 * mpmath.atanh(ml ** 1000)),
            "sqrt2*e^-100": (math.sqrt(2) * math.exp(-100), mpmath.sqrt(2) * mpmath.exp(-100)),
            "e^-2g01": (math.exp(-2 * M["g01"]), mpmath.exp(-2 * mg)),
            "(1-e^beta)/2": (-math.expm1(beta) / 2, (1 - mpmath.exp(mb)) / 2),
            "(1-e^1)/2": (-math.expm1(1.0) / 2, (1 - mpmath.e) / 2),
            "(1-e^10)/2": (-math.expm1(10.0) / 2, (1 - mpmath.exp(10)) / 2),
            "(1-e^g01)/2": (-math.expm1(M["g01"]) / 2, (1 - mpmath.exp(mg)) / 2),
        }
        worst = 0.0
        for k, (f, mp_) in refs.items():
            r = float(abs(mpmath.mpf(f) - mp_) / abs(mp_))
            worst = max(worst, r)
        at("formas fechadas float64 vs mpmath 60 dig. (relativa; entradas = os floats)", worst, "<= 1e-14", worst <= 1e-14)
        rep = float(abs(mpmath.mpf(lam) - (1 - 2 * mb)) / (1 - 2 * mb))
        at("[registro] erro de representacao de lambda = fl(1-2beta) (relativo; nao e criterio)", rep, "registro", True)
    except Exception as exc:
        at("mpmath disponivel", repr(exc), "importavel", False)
    T64 = M["T"]
    P = np.eye(2)
    worst = 0.0
    for k in range(1, 65):
        P = P @ T64
        worst = max(worst, float(np.max(np.abs(np.linalg.matrix_power(T64, k) - P))))
    at("matrix_power(T,k) == produto repetido, k <= 64", worst, "<= 1e-13", worst <= 1e-13)
    rng = rng_new()
    worst_s = worst_u = 0.0
    for n in (2, 3, 5, 8):
        for _ in range(20):
            rho = rand_state(rng, n)
            worst_s = max(worst_s, abs(np.trace(rho) - 1), max(0.0, -float(np.min(np.linalg.eigvalsh(rho)))))
            U = rand_unitary(rng, n)
            worst_u = max(worst_u, fro(U.conj().T @ U - np.eye(n)))
    at("geradores: estado psd e traco 1", worst_s, "<= 1e-14", worst_s <= 1e-14)
    at("geradores: unitario aleatorio", worst_u, "<= 1e-13", worst_u <= 1e-13)
    ok = all(r["ok"] for r in res)
    inval = [r["nome"] for r in res if r["condicao_de_INVALIDO_preregistrada"] and not r["ok"]]
    return res, ok, inval


# ----------------------------------------------------------------------------- T1.o
def test_T1o(M, prereg):
    sub = Sub("T1.o", prereg)
    rng = rng_new()
    for n in (2, 3, 4, 5, 8):
        I = np.eye(n, dtype=complex)
        b = (1j * I).reshape(-1, order="F")
        sq = math.sqrt(n)
        groups = [("aleatorio", None)]
        if n == 2:
            groups.append(("H_ot", M["H_ot"]))
        for label, Hfix in groups:
            mi = mir = mii = miii = miiir = 0.0
            rmin, rmax = math.inf, -math.inf
            ok_i = ok_ii = ok_iii = True
            fals_ii = False
            r_T0 = r_TH = None
            for _ in range(200):
                H = rand_herm(rng, n) if Hfix is None else Hfix
                T = cgauss(rng, (n, n))
                Cm = T @ H - H @ T
                vi = abs(np.trace(Cm))
                tol_i = 1e-10 * (1.0 + fro(T) * fro(H))
                ok_i = ok_i and vi <= tol_i
                mi = max(mi, vi)
                mir = max(mir, vi / tol_i)
                L = np.kron(H.T, I) - np.kron(I, H)
                v = np.linalg.lstsq(L, b, rcond=None)[0]
                r = fro(L @ v - b)
                rmin = min(rmin, r)
                rmax = max(rmax, r)
                dev = abs(r - sq)
                ok_ii = ok_ii and dev <= 1e-10
                mii = max(mii, dev)
                fals_ii = fals_ii or (r < sq - 1e-10)
                c2 = fro(Cm) ** 2
                viii = abs(fro(Cm - 1j * I) ** 2 - c2 - n)
                tol_iii = 1e-9 * (1.0 + c2)
                ok_iii = ok_iii and viii <= tol_iii
                miii = max(miii, viii)
                miiir = max(miiir, viii / tol_iii)
                r_T0 = fro(np.zeros((n, n)) @ H - H @ np.zeros((n, n)) - 1j * I)
                r_TH = fro(H @ H - H @ H - 1j * I)
            key = "n=%d/%s" % (n, label)
            sub.med(key, {"pares": 200, "i_max_abs": mi, "i_max_razao_tol": mir, "ii_min_residuo": rmin,
                          "ii_max_residuo": rmax, "sqrt_n": sq, "ii_max_desvio": mii,
                          "ii_residuo_em_T0": r_T0, "ii_residuo_em_T_igual_H": r_TH,
                          "iii_max_abs": miii, "iii_max_razao_tol": miiir})
            sub.crit("(i) %s: |tr(TH-HT)| <= 1e-10(1+||T||_F||H||_F)" % key, mir, "razao <= 1", ok_i)
            sub.crit("(ii) %s: |min_T ||TH-HT-i1||_F - sqrt(n)| <= 1e-10" % key, mii, "<= 1e-10", ok_ii)
            sub.crit("(ii) %s: falsificador min < sqrt(n) - 1e-10 nunca ocorre" % key, rmin, ">= %.15f" % (sq - 1e-10), not fals_ii)
            sub.crit("(iii) %s: | ||C-i1||^2 - ||C||^2 - n | <= 1e-9(1+||C||^2)" % key, miiir, "razao <= 1", ok_iii)
    return sub.done()


# ----------------------------------------------------------------------------- T3.o
def test_T3o(M, prereg, conf):
    sub = Sub("T3.o", prereg)
    rho1 = M["rho1"]
    om = M["omega1"]
    mf = ModularFlow(rho1)
    rng = rng_new()
    As = [cgauss(rng, (2, 2)) for _ in range(200)]
    Bs = [cgauss(rng, (2, 2)) for _ in range(200)]
    ma = mb = mc = 0.0
    for a in As:
        for s in GRID_T3:
            for t in GRID_T3:
                ma = max(ma, fro(mf.sigma(s, mf.sigma(t, a)) - mf.sigma(s + t, a)))
        mb = max(mb, fro(mf.sigma(0.0, a) - a))
        for t in GRID_T3:
            mc = max(mc, abs(np.trace(rho1 @ mf.sigma(t, a)) - np.trace(rho1 @ a)))
    sub.med("a_max", ma)
    sub.med("b_max", mb)
    sub.med("c_max", mc)
    sub.crit("(a) max ||sigma_s(sigma_t a) - sigma_{s+t} a||_F, 200 a, (s,t) na grade^2", ma, "<= 1e-10", ma <= 1e-10)
    sub.crit("(b) max ||sigma_0 a - a||_F", mb, "<= 1e-10", mb <= 1e-10)
    sub.crit("(c) max |tr(rho1 sigma_t a) - tr(rho1 a)|, t na grade", mc, "<= 1e-10", mc <= 1e-10)
    rinv = np.linalg.inv(rho1)
    md = mdr = 0.0
    for a, b in zip(As, Bs):
        v = abs(np.trace(rho1 @ a @ b) - np.trace(rho1 @ b @ rho1 @ a @ rinv))
        md = max(md, v)
        mdr = max(mdr, v / (1e-10 * (1.0 + fro(a) * fro(b))))
    sub.med("d_max_abs", md)
    sub.med("d_max_razao_tol", mdr)
    sub.crit("(d) KMS |tr(rho1 ab) - tr(rho1 b rho1 a rho1^-1)| <= 1e-10(1+||a||||b||), 200 pares", mdr, "razao <= 1", mdr <= 1.0)
    me = mfull = 0.0
    for t in GRID_T3:
        st = mf.sigma(t, E01)
        me = max(me, abs(st[0, 1] - np.exp(1j * t * om)))
        mfull = max(mfull, fro(st - np.exp(1j * t * om) * E01))
    sub.med("e_max", me)
    sub.med("e_max_matriz_inteira", mfull)
    sub.med("omega1", om)
    sub.med("P1", M["P1"])
    sub.crit("(e) max |sigma_t(E01)_01 - e^{i t omega1}|, t na grade", me, "<= 1e-12", me <= 1e-12)
    sub.conf("omega1", om, conf["omega1"])
    sub.conf("P1", M["P1"], conf["P1"])
    return sub.done()


# ----------------------------------------------------------------------------- T4.o
def test_T4o(M, prereg, conf):
    sub = Sub("T4.o", prereg)
    S = M["S"]
    th = M["theta_M"]
    lam = M["lam"]
    T = M["T"]
    # (O-a)
    sts = fro(S.T @ S - I2)
    shs = fro(S.conj().T @ S - I2)
    dS = complex(np.linalg.det(S))
    sv = np.linalg.svd(S, compute_uv=False)
    sub.med("Oa", {"StS_menos_I": sts, "SHS_menos_I": shs, "det_S": dS, "valores_singulares": sv})
    sub.crit("(O-a) ||S^T S - I||_F", sts, "<= 1e-12", sts <= 1e-12)
    sub.crit("(O-a) |det S - 1|", abs(dS - 1), "<= 1e-12", abs(dS - 1) <= 1e-12)
    sub.crit("(O-a) max |sv(S) - 1|", float(np.max(np.abs(sv - 1))), "<= 1e-12", float(np.max(np.abs(sv - 1))) <= 1e-12)
    # (O-b)
    rng = rng_new()
    pairs = [(rand_state(rng, 2), rand_state(rng, 2)) for _ in range(500)]
    ks = [1, 10, 100, 1000, 10000]
    mats = []
    for k in ks:
        mats.append(("angulo_exato", k, Smat(k * th), Smat(-k * th)))
    P = I2.copy()
    Pinv = I2.copy()
    Sinv = Smat(-th)
    for j in range(1, 1001):
        P = P @ S
        Pinv = Pinv @ Sinv
        if j in ks:
            mats.append(("produto_repetido", j, P.copy(), Pinv.copy()))
    ob = {}
    ok_all = True
    for label, k, Sk, Skinv in mats:
        md = msp = mpu = mim = 0.0
        for rho, sig in pairs:
            X = Sk @ rho @ Skinv
            Y = Sk @ sig @ Skinv
            md = max(md, abs(fro(X - Y) - fro(rho - sig)))
            for Z, Z0 in ((X, rho), (Y, sig)):
                ev = np.linalg.eigvals(Z)
                mim = max(mim, float(np.max(np.abs(ev.imag))))
                evs = np.sort(ev.real)
                ev0 = np.linalg.eigvalsh(Z0)
                msp = max(msp, float(np.max(np.abs(evs - ev0))))
                mpu = max(mpu, abs(tr2(Z) - tr2(Z0)))
        key = "%s/k=%d" % (label, k)
        ob[key] = {"dist_max": md, "espectro_max": msp, "pureza_max": mpu, "parte_imag_autovalores_max": mim}
        okk = md <= 1e-10 and msp <= 1e-10 and mpu <= 1e-10
        ok_all = ok_all and okk
        sub.crit("(O-b) %s: max(|dist|, espectro, pureza), 500 pares" % key, max(md, msp, mpu), "<= 1e-10", okk)
    sub.med("Ob", ob)
    # (O-c)
    rho0 = E00
    oc = {}
    mins = []
    for N in (100, 1000, 10000):
        kk = np.arange(N, 2 * N + 1)
        ang = kk * th
        c = np.cos(ang)
        s = np.sin(ang)
        Sk = np.zeros((len(kk), 2, 2), dtype=complex)
        Sk[:, 0, 0] = c
        Sk[:, 0, 1] = s
        Sk[:, 1, 0] = -s
        Sk[:, 1, 1] = c
        rk = Sk @ rho0 @ np.conj(np.swapaxes(Sk, 1, 2))
        diffs = np.linalg.norm(rk - rk[0], axis=(1, 2))
        MN = float(diffs.max())
        closed = math.sqrt(2.0) * float(np.max(np.abs(np.sin(np.arange(0, N + 1) * th))))
        oc["N=%d" % N] = {"M_N": MN, "forma_fechada_sqrt2_max_sen": closed, "dif": abs(MN - closed),
                          "conferencia_preregistro": conf["noland_M_N"][str(N)]}
        mins.append(MN)
        sub.crit("(O-c) M_N, N=%d (ilustracao do nao-pouso)" % N, MN, ">= 1.0", MN >= 1.0)
    sub.med("Oc", oc)
    sub.conf("Oc_min_M_N", min(mins), conf["noland_min"])
    # (O-d)
    rng = rng_new()
    pairs = [(rand_state(rng, 2), rand_state(rng, 2)) for _ in range(500)]
    ineq = -math.inf
    for rho, sig in pairs:
        ineq = max(ineq, fro(Cmap(S, rho) - Cmap(S, sig)) - lam * fro(rho - sig))
    sub.crit("(O-d) max(||C rho - C sigma||_F - lambda ||rho - sigma||_F), 500 pares", ineq, "<= 1e-12", ineq <= 1e-12)
    X0 = np.stack([p for pr in pairs for p in pr])
    half = 0.5 * np.eye(2)
    d0 = np.linalg.norm(Dmap(X0) - half, axis=(1, 2))
    X = X0.copy()
    mx = 0.0
    kmx = 0
    bands = {"k<=100": 0.0, "100<k<=1000": 0.0, "1000<k<=4096": 0.0}
    for k in range(1, 4097):
        X = Cmap(S, X)
        dist = np.linalg.norm(X - half, axis=(1, 2))
        diff = float(np.max(np.abs(dist - (lam ** k) * d0)))
        if diff > mx:
            mx, kmx = diff, k
        band = "k<=100" if k <= 100 else ("100<k<=1000" if k <= 1000 else "1000<k<=4096")
        bands[band] = max(bands[band], diff)
    sub.med("Od", {"desigualdade_max": ineq, "iteracao_max_dif": mx, "k_do_max": kmx, "por_faixa": bands,
                   "estados": int(X0.shape[0]), "lambda": lam, "lambda^4096": lam ** 4096})
    sub.crit("(O-d) max_k<=4096 | ||C^k rho - I/2||_F - lambda^k ||D rho - I/2||_F |, 1000 estados", mx, "<= 1e-11", mx <= 1e-11)
    sub.conf("lambda", lam, conf["lam"])
    sub.conf("lambda^4096", lam ** 4096, conf["lam4096"])
    # (O-e)
    dT = float(np.linalg.det(T))
    sub.crit("(O-e) |det T - (1 - 2 beta)|", abs(dT - (1 - 2 * M["beta"])), "<= 1e-12", abs(dT - (1 - 2 * M["beta"])) <= 1e-12)
    sub.conf("det_T", dT, conf["det_T"])
    basis = [E00, E11, E01 + E10, 1j * (E01 - E10)]

    def coords(Xm):
        return [Xm[0, 0].real, Xm[1, 1].real, Xm[0, 1].real, Xm[0, 1].imag]

    oe = {"det_T": dT}
    for t in (0.5, 1.0, 10.0):
        Mt = np.column_stack([coords(dephase(M["Gdav"], t, B)) for B in basis])
        dv = float(np.linalg.det(Mt))
        ref = math.exp(-2.0 * M["g01"] * t)
        oe["t=%g" % t] = {"det_4x4": dv, "e^{-2 g01 t}": ref, "dif": abs(dv - ref)}
        sub.crit("(O-e) volume Davies 4x4 real, t=%g: |det - e^{-2 g01 t}|" % t, abs(dv - ref), "<= 1e-12", abs(dv - ref) <= 1e-12)
        if t == 1.0:
            sub.conf("e^{-2g01} (t=1)", dv, conf["vol_davies_t1"])
    sub.med("Oe", oe)
    # (O-f)
    B1 = boost_f64(1.0)
    dB = float(np.linalg.det(B1))
    c1, s1 = math.cosh(1.0), math.sinh(1.0)
    sub.crit("(O-f) float64: |det B(1) - 1| (numpy LU)", abs(dB - 1), "<= 1e-12", abs(dB - 1) <= 1e-12)
    sub.crit("(O-f) float64: |cosh^2 - sinh^2 - 1|", abs(c1 * c1 - s1 * s1 - 1), "<= 1e-12", abs(c1 * c1 - s1 * s1 - 1) <= 1e-12)
    x, y = 1.0, -1.0
    of64 = {}
    worst = 0.0
    sym = True
    for k in range(1, 11):
        x, y = c1 * x + s1 * y, s1 * x + c1 * y
        sym = sym and (x == -y)
        nrm = math.hypot(x, y)
        ref = math.sqrt(2.0) * math.exp(-k)
        rel = abs(nrm - ref) / ref
        of64["k=%d" % k] = {"norma": nrm, "sqrt2_e^-k": ref, "rel": rel}
        worst = max(worst, rel)
    sub.crit("(O-f) float64 IEEE escalar (E4), k<=10: max rel | ||B^k(1,-1)|| - sqrt2 e^-k |", worst, "<= 1e-9", worst <= 1e-9)
    sub.info("Of_float64_orbita_fica_na_reta_nula_exatamente", sym)
    with localcontext() as ctx:
        ctx.prec = 200
        e1 = Decimal(1).exp()
        ch = (e1 + 1 / e1) / 2
        sh = (e1 - 1 / e1) / 2
        detd = ch * ch - sh * sh
        xd, yd = Decimal(1), Decimal(-1)
        norms = [(xd * xd + yd * yd).sqrt()]
        dec = {}
        for k in range(1, 101):
            xd, yd = ch * xd + sh * yd, sh * xd + ch * yd
            nr = (xd * xd + yd * yd).sqrt()
            norms.append(nr)
            if k in (10, 100):
                ref = Decimal(2).sqrt() * Decimal(-k).exp()
                rel = abs(nr - ref) / ref
                dec["k=%d" % k] = {"norma": str(nr), "sqrt2_e^-k": str(ref), "rel": str(rel)}
                sub.crit("(O-f) decimal 200 dig., k=%d: rel | ||B^k(1,-1)|| - sqrt2 e^-k |" % k, float(rel),
                         "<= 1e-50", rel <= Decimal("1e-50"))
        decreasing = all(norms[i + 1] < norms[i] for i in range(100))
        conf_dec = Decimal(conf["boost_k100_decimal"])
        dif100 = abs(norms[100] - conf_dec) / conf_dec
        sub.med("Of", {"det_B1_float64_LU": dB, "float64_IEEE_escalar": of64,
                       "decimal_200": dec, "det_B1_decimal_menos_1": str(detd - 1),
                       "normas_decimais_estritamente_decrescentes_k0a100": decreasing,
                       "norma_k100_decimal": str(norms[100])})
        sub.d["conferencia"]["boost_k100_decimal"] = {"calculado_aqui": str(norms[100]), "preregistro": conf["boost_k100_decimal"],
                                                      "dif_rel": str(dif100)}
    sub.conf("boost_k100_float", float(norms[100]), conf["boost_k100"])
    sub.d["_cT4a"] = {"det_float64": dB, "det_decimal_menos_1": str(detd - 1), "decrescente": decreasing,
                      "norma_k100": str(norms[100])}
    return sub.done()


# ----------------------------------------------------------------------------- T6.o
def test_T6o(M, prereg, conf):
    sub = Sub("T6.o", prereg)
    ts = [0.0, 0.1, 1.0, 10.0]
    dense = [j / 10.0 for j in range(0, 201)]
    grid_b = sorted(set(ts + dense))
    rng = rng_new()
    out = {}
    for n in (2, 3, 5):
        ma = 0.0
        mb_viol = -math.inf
        mbd_viol = -math.inf
        qual = 0
        dmin = math.inf
        md = 0.0
        mim = 0.0
        for _ in range(300):
            rho = rand_state(rng, n)
            g = rand_rates(rng, n)
            rates = [("aleatoria", g)]
            if n == 2:
                rates.append(("davies", M["Gdav"]))
            for name, gg in rates:
                purs = {}
                for t in grid_b:
                    Xt = dephase(gg, t, rho)
                    v = tr2(Xt)
                    mim = max(mim, abs(v.imag))
                    purs[t] = v.real
                for t in ts:
                    formula = float(np.sum(np.exp(-2.0 * t * gg) * np.abs(rho) ** 2))
                    ma = max(ma, abs(purs[t] - formula))
                run = math.inf
                for t in ts:
                    if run < math.inf:
                        mb_viol = max(mb_viol, purs[t] - run)
                    run = min(run, purs[t])
                run = math.inf
                for t in grid_b:
                    if run < math.inf:
                        mbd_viol = max(mbd_viol, purs[t] - run)
                    run = min(run, purs[t])
                cond = False
                for i in range(n):
                    for j in range(n):
                        if i != j and abs(rho[i, j]) >= 0.05 and gg[i, j] >= 0.01:
                            cond = True
                if cond:
                    qual += 1
                    dmin = min(dmin, purs[0.0] - purs[1.0])
            U = rand_unitary(rng, n)
            md = max(md, abs(tr2(U @ rho @ U.conj().T).real - tr2(rho).real))
        out["n=%d" % n] = {"a_max": ma, "b_violacao_max_grade_a": mb_viol, "b_violacao_max_grade_densa": mbd_viol,
                           "c_qualificados": qual, "c_queda_min": dmin, "d_max": md, "parte_imag_max": mim}
        sub.crit("(a) n=%d: max |Tr(T_t rho)^2 - sum e^{-2t g}|rho_ij|^2|" % n, ma, "<= 1e-12", ma <= 1e-12)
        sub.crit("(b) n=%d: monotonia na grade de (a): max[Tr(T_t2 rho)^2 - min_{t1<=t2} Tr(T_t1 rho)^2]" % n, mb_viol, "<= 1e-14", mb_viol <= 1e-14)
        sub.crit("(b) n=%d: monotonia na grade densa 0..20 (E5)" % n, mbd_viol, "<= 1e-14", mbd_viol <= 1e-14)
        sub.crit("(c) n=%d: queda minima em t=1 nos qualificados (%d)" % (n, qual), dmin, ">= 1e-8", qual > 0 and dmin >= 1e-8)
        sub.crit("(d) n=%d: max |Tr(U rho U^H)^2 - Tr rho^2|, 300 unitarios" % n, md, "<= 1e-12", md <= 1e-12)
    sub.med("por_n", out)
    v = tr2(dephase(M["Gdav"], 1.0, PSI_PLUS)).real
    ref = (1.0 + math.exp(-2.0 * M["g01"])) / 2.0
    sub.med("e", {"Tr(T_1 psi+)^2": v, "(1+e^{-2g01})/2": ref})
    sub.crit("(e) |Tr(T_1 psi+)^2 - (1+e^{-2 g01})/2| (Davies)", abs(v - ref), "<= 1e-12", abs(v - ref) <= 1e-12)
    sub.conf("pur_psi_t1", v, conf["pur_psi_t1"])
    return sub.done()


# ----------------------------------------------------------------------------- T7.o
def test_T7o(M, prereg, conf):
    sub = Sub("T7.o", prereg)
    beta = M["beta"]
    oa = {}
    for gt, ck in ((beta, "neg_beta"), (1.0, "neg_1"), (10.0, "neg_10")):
        X = dephase(M["G1"], -gt, PSI_PLUS)
        emin = float(np.min(np.linalg.eigvalsh(X)))
        ref = -math.expm1(gt) / 2.0
        oa["gt=%r" % gt] = {"autovalor_min": emin, "(1-e^{gt})/2": ref, "dif": abs(emin - ref)}
        sub.crit("(a) gt=%r: |lambda_min(T_{-t} psi+) - (1-e^{gt})/2|" % gt, abs(emin - ref), "<= 1e-12(1+|v|) = %.3e" % (1e-12 * (1 + abs(ref))),
                 abs(emin - ref) <= 1e-12 * (1 + abs(ref)))
        sub.crit("(a) gt=%r: lambda_min < -1e-10" % gt, emin, "< -1e-10", emin < -1e-10)
        sub.conf("a gt=%r" % gt, emin, conf[ck])
    sub.med("a", oa)
    rng = rng_new()
    states = [rand_state(rng, 2) for _ in range(100)]
    ob = {}
    for label, g, t in (("gamma=1,gt=beta", M["G1"], beta), ("gamma=1,gt=1", M["G1"], 1.0),
                        ("gamma=1,gt=10", M["G1"], 10.0), ("davies,t=1", M["Gdav"], 1.0)):
        mx = max(fro(dephase(g, -t, dephase(g, t, r)) - r) for r in states)
        ob[label] = mx
        sub.crit("(b) %s: max ||T_{-t}(T_t rho) - rho||_F, 100 estados" % label, mx, "<= 1e-12", mx <= 1e-12)
    sub.med("b", ob)
    X = dephase(M["Gdav"], -1.0, PSI_PLUS)
    emin = float(np.min(np.linalg.eigvalsh(X)))
    ref = -math.expm1(M["g01"]) / 2.0
    sub.med("c", {"autovalor_min": emin, "(1-e^{g01})/2": ref})
    sub.crit("(c) Davies t=1: |lambda_min - (1-e^{g01})/2|", abs(emin - ref), "<= 1e-12(1+|v|)", abs(emin - ref) <= 1e-12 * (1 + abs(ref)))
    sub.crit("(c) Davies t=1: lambda_min < -1e-10", emin, "< -1e-10", emin < -1e-10)
    sub.conf("c davies", emin, conf["neg_davies"])
    return sub.done()


# ----------------------------------------------------------------------------- potencias de T (T8.o, T9.o)
_TPOW = {}


def tpow(T, k):
    if k not in _TPOW:
        _TPOW[k] = np.linalg.matrix_power(T, k)
    return _TPOW[k]


# ----------------------------------------------------------------------------- T8.o
def test_T8o(M, prereg, conf):
    sub = Sub("T8.o", prereg)
    T = M["T"]
    lam = M["lam"]
    e0 = np.array([1.0, 0.0])
    ma = 0.0
    kma = 0
    first_floor = None
    cs = []
    for k in range(0, 10001):
        p = tpow(T, k) @ e0
        c = p[0] - p[1]
        cs.append(c)
        d = abs(c - lam ** k)
        if d > ma:
            ma, kma = d, k
        if first_floor is None and c < 1e-15:
            first_floor = k
    sub.med("a", {"max_dif": ma, "k_do_max": kma, "c_1": cs[1], "c_100": cs[100], "c_1000": cs[1000]})
    sub.crit("(a) max_{k<=10^4} |c_k - lambda^k| (matrix_power)", ma, "<= 1e-13", ma <= 1e-13)
    sub.info("b_primeiro_k_contraste_float64_abaixo_de_1e-15", first_floor)
    sub.info("b_esperado_preregistro", conf["k_float_floor"])
    sub.info("b_leitura", "sombra numerica do abismo, nao um zero; que c_k > 0 para todo k decide-o o kernel (T8.b(iv))")
    lnl = math.log(lam)
    oc = {}
    for eps in (1e-1, 1e-3, 1e-6):
        q = math.log(eps) / lnl
        k_eps = math.floor(q) + 1
        lo = math.exp(k_eps * lnl)
        hi = math.exp((k_eps - 1) * lnl)
        ok1 = lo < eps
        ok2 = eps <= hi
        oc[str(eps)] = {"q=ln eps/ln lambda": q, "parte_fracionaria": q - math.floor(q), "k_eps": k_eps,
                        "lambda^k_eps": lo, "lambda^(k_eps-1)": hi, "segunda_tambem_estrita": eps < hi,
                        "k_eps_preregistro": conf["k_eps"][str(eps)], "frac_preregistro": conf["frac_eps"][str(eps)]}
        sub.crit("(c) eps=%g: lambda^{k_eps} < eps (k_eps=%d)" % (eps, k_eps), lo, "< %g" % eps, ok1)
        sub.crit("(c) eps=%g: eps <= lambda^{k_eps-1}" % eps, hi, ">= %g" % eps, ok2)
        sub.crit("(c) eps=%g: k_eps igual ao pre-registro (%d)" % (eps, conf["k_eps"][str(eps)]), k_eps, "== %d" % conf["k_eps"][str(eps)], k_eps == conf["k_eps"][str(eps)])
        sub.conf("frac eps=%g" % eps, q - math.floor(q), conf["frac_eps"][str(eps)])
    sub.med("c", oc)
    rng = rng_new()
    xs = [PSI_PLUS] + [rand_state(rng, 2) for _ in range(100)]
    od = {}
    for t in (0.1, 1.0, 10.0):
        mx = max(abs(abs(dephase(M["Gdav"], t, x)[0, 1]) - math.exp(-M["g01"] * t) * abs(x[0, 1])) for x in xs)
        od["t=%g" % t] = mx
        sub.crit("(d) t=%g: max | |x01(t)| - e^{-g01 t}|x01(0)| |, psi+ e 100 estados" % t, mx, "<= 1e-12", mx <= 1e-12)
    sub.med("d", od)
    sk = {k: -k * lnl for k in (1, 10, 100)}
    sub.med("lei_de_escala_s_k=-k ln lambda=2ak", {str(k): {"s_k": s, "2ak": 2 * M["a"] * k, "e^{-s_k}": math.exp(-s), "lambda^k": lam ** k} for k, s in sk.items()})
    return sub.done()


# ----------------------------------------------------------------------------- T9.o
def test_T9o(M, prereg, conf):
    sub = Sub("T9.o", prereg)
    T = M["T"]
    R = M["R"]
    lam = M["lam"]
    a = M["a"]
    I = np.eye(2)
    va = fro(T - (R + math.exp(-2 * a) * (I - R)))
    sub.med("a", {"dif": va, "2a": 2 * a, "-ln lambda": -math.log(lam)})
    sub.crit("(a) ||T - (R + e^{-2a}(I-R))||_F", va, "<= 1e-15", va <= 1e-15)
    sub.conf("2a", 2 * a, conf["dois_a"])
    nIR = fro(I - R)
    ob = {}
    for t in (1e-6, 1e-3, 0.1, 1.0, 10.0, 30.0):
        F = axiom_flow(R, t)
        m1 = fro(F @ F - F)
        v1 = math.exp(-t) * (-math.expm1(-t)) * nIR
        m2 = float(np.linalg.det(F))
        v2 = math.exp(-t)
        ob["t=%g" % t] = {"||F^2-F||_F": m1, "e^-t(1-e^-t)||I-R||": v1, "det F": m2, "e^-t": v2}
        sub.crit("(b) t=%g: | ||F^2-F||_F - e^-t(1-e^-t)||I-R||_F |" % t, abs(m1 - v1), "<= 1e-12*v + 1e-15 = %.3e" % (1e-12 * v1 + 1e-15), abs(m1 - v1) <= 1e-12 * v1 + 1e-15)
        sub.crit("(b) t=%g: |det F(t) - e^-t|" % t, abs(m2 - v2), "<= 1e-12*v + 1e-15 = %.3e" % (1e-12 * v2 + 1e-15), abs(m2 - v2) <= 1e-12 * v2 + 1e-15)
        sub.crit("(b) t=%g: falsificador 'F(t) idempotente dentro da tolerancia' nao ocorre" % t, m1, "> %.3e" % (1e-12 * v1 + 1e-15), m1 > 1e-12 * v1 + 1e-15)
    sub.med("b", ob)
    sub.med("||I-R||_F", nIR)
    me = 0.0
    kme = 0
    for k in range(0, 10001):
        d = float(np.max(np.abs(tpow(T, k) - (R + lam ** k * (I - R)))))
        if d > me:
            me, kme = d, k
    sub.crit("(c) max_{k<=10^4} max_ij |T^k - (R + lambda^k (I-R))|", me, "<= 1e-13", me <= 1e-13)
    msv = 0.0
    for k in range(0, 501):
        s = np.linalg.svd(tpow(T, k), compute_uv=False)
        msv = max(msv, abs(s.min() - lam ** k) / lam ** k)
    sub.crit("(c) max_{k<=500} rel |s_min(T^k) - lambda^k|", msv, "<= 1e-9", msv <= 1e-9)

    def nrank(A):
        s = np.linalg.svd(A, compute_uv=False)
        return int(np.sum(s > 1e-12 * s.max()))

    ranks = [nrank(tpow(T, k)) for k in range(0, 1001)]
    ok_r = all(r == 2 for r in ranks)
    sub.crit("(c) posto numerico de T^k == 2 para todo k <= 1000 (limiar 1e-12 ||T^k||_2)", min(ranks), "== 2", ok_r)
    rR = nrank(R)
    sub.crit("(c) posto de R == 1", rR, "== 1", rR == 1)
    drop = None
    for k in range(1001, 10001):
        if nrank(tpow(T, k)) < 2:
            drop = k
            break
    sub.med("c", {"entradas_max_dif": me, "k_do_max": kme, "sv_rel_max": msv, "posto_min_k<=1000": min(ranks), "posto_R": rR})
    sub.info("c_primeiro_k_posto_numerico_cai_a_1", drop)
    sub.info("c_esperado_preregistro", conf["k_rank_drop"])
    sub.info("c_leitura", "sombra numerica do limite, nao um posto em tempo finito; o kernel decide (T9.b)")
    return sub.done()


# ----------------------------------------------------------------------------- T10.o
def test_T10o(M, prereg):
    sub = Sub("T10.o", prereg)
    om = M["omega1"]
    P1 = M["P1"]
    tg = np.array(GRID_T3)
    td = np.arange(0, 5001) / 100.0
    va = float(np.max(np.abs(np.exp(1j * om * (tg + P1)) - np.exp(1j * om * tg))))
    vd = float(np.max(np.abs(np.exp(1j * om * (td + P1)) - np.exp(1j * om * td))))
    sub.med("a", {"grade_T3": va, "grade_0_50_passo_0.01": vd, "omega1": om, "P1": P1})
    sub.crit("(a) grade do T3.o: max |e^{i w1 (t+P1)} - e^{i w1 t}|", va, "<= 1e-12", va <= 1e-12)
    sub.crit("(a) grade [0,50] passo 0,01 (E7): max |e^{i w1 (t+P1)} - e^{i w1 t}|", vd, "<= 1e-12", vd <= 1e-12)
    mf = ModularFlow(M["rho1"])
    rng = rng_new()
    xs = [cgauss(rng, (2, 2)) for _ in range(200)]
    vb = 0.0
    for x in xs:
        for t in GRID_T3:
            vb = max(vb, float(np.max(np.abs(np.abs(mf.sigma(t, x)) - np.abs(x)))))
    sub.med("b", vb)
    sub.crit("(b) max_ij | |sigma_t(x)_ij| - |x_ij| |, 200 x, t na grade", vb, "<= 1e-12", vb <= 1e-12)
    c = np.exp(-2.0 * M["a"] * td)
    dif = c[:-1] - c[1:]
    nuniq = len(set(c.tolist()))
    sub.med("c", {"menor_diferenca_consecutiva": float(dif.min()), "valores_distintos": nuniq, "pontos": len(td),
                  "c(50)": float(c[-1]),
                  "c(k)=lambda^k em t inteiro (max dif)": float(max(abs(math.exp(-2 * M["a"] * k) - M["lam"] ** k) for k in range(0, 51)))})
    sub.crit("(c) c(t)=e^{-2at}: diferencas consecutivas > 0 em [0,50] passo 0,01", float(dif.min()), "> 0", bool(np.all(dif > 0)))
    sub.crit("(c) c(t) injetivo na grade (5001 valores distintos)", nuniq, "== 5001", nuniq == len(td))
    T = M["T"]
    R = M["R"]
    v1 = fro(T @ R - R)
    v2 = fro(R @ T - R)
    sub.med("d", {"||TR-R||": v1, "||RT-R||": v2})
    sub.crit("(d) ||TR - R||_F", v1, "<= 1e-12", v1 <= 1e-12)
    sub.crit("(d) ||RT - R||_F", v2, "<= 1e-12", v2 <= 1e-12)
    return sub.done()


# ----------------------------------------------------------------------------- T11.o
def test_T11o(M, prereg, conf):
    sub = Sub("T11.o", prereg)
    S = M["S"]
    lam = M["lam"]
    X = E00.copy()
    cs = {}
    ws = {}
    for k in range(1, 1001):
        X = Cmap(S, X)
        c = X[0, 0].real - X[1, 1].real
        cs[k] = c
        ws[k] = 2.0 * math.atanh(c)
    oa = {}
    for k in (1, 10, 100, 1000):
        we = 2.0 * math.atanh(lam ** k)
        alt = math.log((1 + lam ** k) / (1 - lam ** k))
        d = abs(ws[k] - we)
        tol = 1e-13 + 1e-12 * abs(we)
        oa["k=%d" % k] = {"c_k_medido": cs[k], "omega_k_medido": ws[k], "omega_k=2artanh(lam^k)": we,
                          "ln((1+l^k)/(1-l^k))": alt, "dif": d, "tol": tol,
                          "omega_k_preregistro": conf["omega_k"][str(k)]}
        sub.crit("(a) k=%d: |omega_k(medido) - 2 artanh(lambda^k)|" % k, d, "<= 1e-13 + 1e-12|w| = %.3e" % tol, d <= tol)
        sub.conf("omega_%d" % k, ws[k], conf["omega_k"][str(k)])
    sub.med("a", oa)
    dec = all(ws[k + 1] < ws[k] for k in range(1, 1000))
    mind = min(ws[k] - ws[k + 1] for k in range(1, 1000))
    sub.med("b", {"estritamente_decrescente_k1a1000": dec, "menor_queda": mind})
    sub.crit("(b) omega_k(medido) estritamente decrescente, k = 1..1000", mind, "> 0", dec)
    w1 = math.log((1 - M["beta"]) / M["beta"])
    rel = abs(ws[1] - w1) / abs(w1)
    sub.med("c", {"omega_1_medido": ws[1], "ln((1-b)/b)": w1, "rel": rel})
    sub.crit("(c) k=1: rel |omega_1(medido) - ln((1-b)/b)|", rel, "<= 1e-12", rel <= 1e-12)
    sub.d["_ws"] = {k: ws[k] for k in (1, 10, 100, 1000)}
    return sub.done()


# ----------------------------------------------------------------------------- controles oticos
def controls(M, prereg, subs):
    out = {}
    rho1 = M["rho1"]
    mf = ModularFlow(rho1)
    # C-T3-a
    c = Ctl("C-T3-a", prereg)
    rng = rng_new()
    As = [cgauss(rng, (2, 2)) for _ in range(200)]
    Bs = [cgauss(rng, (2, 2)) for _ in range(200)]
    rinv2 = np.linalg.inv(rho1 @ rho1)
    gaps = [abs(np.trace(rho1 @ a @ b) - np.trace(rho1 @ b @ (rho1 @ rho1 @ a @ rinv2))) for a, b in zip(As, Bs)]
    cnt = sum(1 for g in gaps if g > 1e-6)
    c.med("pares_com_gap_maior_que_1e-6", cnt)
    c.med("gap_mediana", float(np.median(gaps)))
    c.med("gap_max", float(np.max(gaps)))
    out["C-T3-a"] = c.done(cnt >= 1, "a KMS com a temperatura errada (Delta_2) falha em %d de 200 pares" % cnt)
    # C-T3-b
    c = Ctl("C-T3-b", prereg)
    gab = np.trace(rho1 @ E01 @ E10)
    gba = np.trace(rho1 @ E10 @ E01)
    gap = abs(gab - gba)
    c.med("tr(rho1 E01 E10)", gab)
    c.med("tr(rho1 E10 E01)", gba)
    c.med("gap", gap)
    c.med("1-2beta", M["lam"])
    out["C-T3-b"] = c.done(gap >= 0.5 and abs(gap - M["lam"]) <= 1e-15,
                           "o fluxo identidade nao e KMS para rho1: gap = %.15f = 1 - 2 beta" % gap)
    # C-T3-c
    c = Ctl("C-T3-c", prereg)
    mt = ModularFlow(0.5 * I2)
    mx = max(fro(mt.sigma(t, a) - a) for a in As for t in GRID_T3)
    c.med("max ||sigma_t(a) - a||_F (I/2)", mx)
    out["C-T3-c"] = c.done(mx <= 1e-12, "no estado tracial I/2 o fluxo modular e a identidade (o relogio para)")
    # C-T4-a
    c = Ctl("C-T4-a", prereg)
    ct = subs.get("T4.o", {}).get("_cT4a")
    if ct is None:
        out["C-T4-a"] = c.done(False, "T4.o nao produziu os numeros do boost")
    else:
        c.med("det_B1_float64", ct["det_float64"])
        c.med("det_B1_decimal_menos_1", ct["det_decimal_menos_1"])
        c.med("normas_decimais_estritamente_decrescentes_k0a100", ct["decrescente"])
        c.med("norma_k100_decimal", ct["norma_k100"])
        ok = abs(ct["det_float64"] - 1) <= 1e-12 and ct["decrescente"] and Decimal(ct["norma_k100"]) < Decimal("1e-40")
        out["C-T4-a"] = c.done(ok, "o boost conserva volume (det 1) e pousa no raio nulo passado: 'volume conservado => nada pousa' falha")
    # C-T6-a
    c = Ctl("C-T6-a", prereg)
    rng = rng_new()
    mx = 0.0
    for n in (2, 3, 5):
        for _ in range(100):
            rho = rand_state(rng, n)
            dx = Dmap(rho)
            g = rand_rates(rng, n)
            for t in (0.0, 0.1, 1.0, 10.0, 30.0):
                mx = max(mx, abs(tr2(dephase(g, t, dx)).real - tr2(dx).real))
    c.med("max |pur(T_t D rho) - pur(D rho)|", mx)
    out["C-T6-a"] = c.done(mx <= 1e-14, "sem coerencia nao ha queda: a queda estrita falha (igualdade)")
    # C-T6-b
    c = Ctl("C-T6-b", prereg)
    rng = rng_new()
    mx = 0.0
    for n in (2, 3, 5):
        for _ in range(100):
            rho = rand_state(rng, n)
            U = rand_unitary(rng, n)
            mx = max(mx, abs(tr2(U @ rho @ U.conj().T).real - tr2(rho).real))
    c.med("max |Tr(U rho U^H)^2 - Tr rho^2|", mx)
    out["C-T6-b"] = c.done(mx <= 1e-12, "sob a unitaria a queda estrita falha (constancia)")
    # C-T6-c
    c = Ctl("C-T6-c", prereg)
    v = tr2(dephase(M["G1"], -1.0, PSI_PLUS)).real
    ref = (1.0 + math.e ** 2) / 2.0
    c.med("Tr(T_{-1} psi+)^2", v)
    c.med("(1+e^2)/2", ref)
    out["C-T6-c"] = c.done(abs(v - ref) <= 1e-12 * ref and v > 1.0 and v > tr2(PSI_PLUS).real,
                           "para t < 0 a pureza cresce acima de 1: a monotonia falha (a seta)")
    # C-T7-b
    c = Ctl("C-T7-b", prereg)
    mx = 0.0
    mev = math.inf
    for g in (M["G1"], M["Gdav"]):
        for t in (M["beta"], 1.0, 10.0, 30.0):
            for p in (0.0, 0.1, 0.5, 0.9, 1.0):
                Xd = np.diag([p, 1 - p]).astype(complex)
                Y = dephase(g, -t, Xd)
                mx = max(mx, fro(Y - Xd))
                mev = min(mev, float(np.min(np.linalg.eigvalsh(Y))))
    c.med("max ||T_{-t} diag(p,1-p) - diag(p,1-p)||_F", mx)
    c.med("menor autovalor", mev)
    out["C-T7-b"] = c.done(mx == 0.0 and mev >= 0.0, "T_{-t} fixa a diagonal: a nao positividade falha (autovalores >= 0)")
    # C-T7-c
    c = Ctl("C-T7-c", prereg)
    rng = rng_new()
    mx = 0.0
    mev = math.inf
    for n in (2, 3, 5):
        for _ in range(100):
            rho = rand_state(rng, n)
            U = rand_unitary(rng, n)
            Y = U @ rho @ U.conj().T
            mx = max(mx, fro(U.conj().T @ Y @ U - rho))
            mev = min(mev, float(np.min(np.linalg.eigvalsh(Y))))
    c.med("max ||U^H (U rho U^H) U - rho||_F", mx)
    c.med("menor autovalor de U rho U^H", mev)
    out["C-T7-c"] = c.done(mx <= 1e-12 and mev >= -1e-12, "a unitaria e reversivel como canal: Ad(U*) inverte Ad(U) e preserva positividade")
    # C-T11-a
    c = Ctl("C-T11-a", prereg)
    t = math.pi / M["omega1"]
    st = mf.sigma(t, E01)
    v = abs(st[0, 1] - E01[0, 1])
    c.med("t = pi/omega1", t)
    c.med("|sigma_t(E01)_01 - 1|", v)
    out["C-T11-a"] = c.done(v >= 1.0 and abs(v - 2.0) <= 1e-12, "fora do atrator o relogio nao para: |sigma_{pi/w1}(E01)_01 - 1| = %.15f" % v)
    return out


# ----------------------------------------------------------------------------- anexo: achados fora do pre-registro
def annex(M, prereg, subs):
    A = {"estatuto": "[DERIVED/REAL numerico, informativo] — FORA do pre-registro: nenhum veredito, nenhuma tolerancia "
                     "nova; nada aqui converte PASSA em FALHA nem o contrario. Modelo sintetico; nada sobre a natureza.",
         "itens": {}}
    beta0 = M["beta"]

    def guard(name, fn):
        try:
            A["itens"][name] = fn()
        except Exception:
            A["itens"][name] = {"erro_do_runner": traceback.format_exc()}
        LOG("   [anexo] %s" % name)

    def sweep_beta():
        out = {}
        rng = rng_new()
        pairs = [(rand_state(rng, 2), rand_state(rng, 2)) for _ in range(200)]
        for b in (0.0, 1e-9, 1e-6, 1e-3, beta0, 0.1, 0.25, 0.4, 0.49, 0.5, 0.6, 0.75, 0.9, 1.0):
            th = math.asin(math.sqrt(b))
            Sb = Smat(th)
            Tb = np.abs(Sb) ** 2
            lb = 1.0 - 2.0 * b
            ratio = max(fro(Cmap(Sb, r) - Cmap(Sb, s)) / fro(r - s) for r, s in pairs)
            X = E00.copy()
            cs = [1.0]
            dist = {}
            for k in range(1, 1001):
                X = Cmap(Sb, X)
                cs.append(X[0, 0].real - X[1, 1].real)
                if k in (1, 10, 100, 1000):
                    dist[str(k)] = fro(X - 0.5 * I2)
            signs = [np.sign(cs[k]) for k in range(1, 21)]
            alternates = all(signs[i] == -signs[i + 1] for i in range(len(signs) - 1)) and lb < 0
            if lb == 1.0:
                cls = "T = I (S = 1): nada se move; todo estado diagonal e fixo; nao ha bacia"
            elif 0.0 < lb < 1.0:
                cls = "contracao; T = F(t) com t = -ln(lambda); contraste c_k = lambda^k > 0, monotono; omega_k desce a 0"
            elif lb == 0.0:
                cls = "T = R em UM passo: o posto alcancado em passo finito (lambda = 0 corresponde a t = infinito em F)"
            elif -1.0 < lb < 0.0:
                cls = "contracao com oscilacao: c_k alterna de sinal; T nao e F(t) para t real; converge a I/2"
            else:
                cls = "T = X (troca): isometria nas populacoes; orbitas de periodo 2 (um continuo de ciclos neutros, nao atratores)"
            w1 = math.log((1 - b) / b) if 0.0 < b < 1.0 else None
            g01 = b * abs(w1) if w1 is not None else None
            ws = None
            if 0.0 < lb < 1.0:
                ws = [2 * math.atanh(cs[k]) for k in range(1, 51)]
            out["beta=%r" % b] = {"lambda": lb, "det_T": float(np.linalg.det(Tb)), "||S^H S - I||": fro(Sb.conj().T @ Sb - I2),
                                  "contracao_max_200_pares": ratio, "|lambda|": abs(lb),
                                  "dist_C^k(E00)_a_I/2": dist, "c_1..c_5": cs[1:6], "alterna_sinal": bool(alternates),
                                  "classe": cls, "omega1_do_estado_de_uma_travessia": w1, "taxa_davies_g01=b|w1|": g01,
                                  "omega_k_decrescente_k1a50": (all(ws[i + 1] < ws[i] for i in range(49)) if ws else None)}
        return {"descricao": "familia T(beta) = R + (1-2beta)(I-R) do canal C = D Ad(Smat(arcsin sqrt beta)) D, varrida em beta "
                             "(bordas 0, 1/2, 1). Leitura: nesta familia nao ha ciclo limite ATRATOR; so em lambda = -1 ha orbitas "
                             "periodicas, neutras (isometria). Nao fecha o [OPEN] do 'ciclo limite' (RP09): vale so para esta familia.",
                "por_beta": out}

    def sweep_theta():
        out = {}
        rng = rng_new()
        pairs = [(rand_state(rng, 2), rand_state(rng, 2)) for _ in range(100)]
        for name, th in (("0", 0.0), ("1e-8", 1e-8), ("theta_M", M["theta_M"]), ("pi/4", math.pi / 4), ("pi/2", math.pi / 2),
                         ("pi", math.pi), ("2pi-1e-8", 2 * math.pi - 1e-8), ("2pi", 2 * math.pi)):
            Sm = Smat(th)
            iso = max(abs(fro(Ad(Sm, r) - Ad(Sm, s)) - fro(r - s)) for r, s in pairs)
            per = fro(Smat(th + 2 * math.pi) - Sm)
            N = 1000
            kk = np.arange(N, 2 * N + 1)
            rk = [Ad(Smat(k * th), E00) for k in (N, N + 1)]
            MN = math.sqrt(2.0) * float(np.max(np.abs(np.sin(np.arange(0, N + 1) * th))))
            fixed = fro(Ad(Sm, E00) - E00)
            out[name] = {"isometria_max_dif": iso, "||S(th+2pi)-S(th)||": per, "M_1000_forma_fechada": MN,
                         "||Ad(S)E00 - E00||": fixed, "passo_rho_N->rho_N+1": fro(rk[1] - rk[0])}
        return {"descricao": "regime do ANGULO varrido em theta: Ad(S) e isometria em todo theta; periodico (2 pi); "
                             "so os pontos fixos tem orbita convergente (theta em pi Z: tudo fixo). Nunca se pede limite ao angulo.",
                "por_theta": out}

    def sweep_time_dephase():
        rng = rng_new()
        n = 3
        rho = rand_state(rng, n)
        g = rand_rates(rng, n)
        ts = [-1.0, -1e-3, 0.0, 1e-12, 1e-6, 1e-3, 0.1, 1.0, 10.0, 30.0, 100.0]
        law = 0.0
        for s in ts:
            for t in ts:
                A1 = dephase(g, s, dephase(g, t, rho))
                A2 = dephase(g, s + t, rho)
                law = max(law, fro(A1 - A2) / (1.0 + fro(A2)))
        pur = {repr(t): tr2(dephase(g, t, rho)).real for t in ts}
        mev = {repr(t): float(np.min(np.linalg.eigvalsh(dephase(g, t, rho)))) for t in ts}
        gmin = min(g[i, j] for i in range(n) for j in range(n) if i != j)
        dist = {repr(t): {"||T_t rho - E_D rho||": fro(dephase(g, t, rho) - Dmap(rho)),
                          "cota e^{-gmin t}||rho - E_D rho||": math.exp(-gmin * t) * fro(rho - Dmap(rho))} for t in ts if t >= 0}
        psi_ev = {repr(t): float(np.min(np.linalg.eigvalsh(dephase(M["Gdav"], t, PSI_PLUS)))) for t in ts}
        return {"descricao": "semigrupo de defasagem (n=3, taxas aleatorias; psi+ com Davies) numa grade de t com bordas "
                             "(t<0, t=0, t=1e-12, t grande): lei de GRUPO dos mapas lineares (inclusive t<0), pureza monotona "
                             "so para t>=0, positividade so para t>=0 (para t<0 o mapa linear inverso sai dos estados: T7), "
                             "distancia a E_D sob a cota e^{-g_min t}.",
                "lei_de_grupo_max_rel": law, "pureza_por_t": pur, "menor_autovalor_por_t": mev,
                "distancia_a_E_D": dist, "psi+_davies_menor_autovalor_por_t": psi_ev, "g_min": gmin}

    def sweep_boost_s():
        out = {}
        with localcontext() as ctx:
            ctx.prec = 200
            for s in (-1, 0, Decimal("0.1"), 1, 3):
                sd = Decimal(s)
                es = sd.exp()
                ch = (es + 1 / es) / 2
                sh = (es - 1 / es) / 2
                xp, yp = Decimal(1), Decimal(-1)
                xf, yf = Decimal(1), Decimal(1)
                for _ in range(10):
                    xp, yp = ch * xp + sh * yp, sh * xp + ch * yp
                    xf, yf = ch * xf + sh * yf, sh * xf + ch * yf
                npast = (xp * xp + yp * yp).sqrt()
                nfut = (xf * xf + yf * yf).sqrt()
                out[str(s)] = {"det_menos_1": str(ch * ch - sh * sh - 1),
                               "||B^10 (1,-1)||": str(npast), "sqrt2 e^{-10 s}": str(Decimal(2).sqrt() * (-10 * sd).exp()),
                               "||B^10 (1,1)||": str(nfut), "sqrt2 e^{+10 s}": str(Decimal(2).sqrt() * (10 * sd).exp())}
        return {"descricao": "o boost em s (decimal 200 dig.): det = 1 em todo s; o raio nulo passado contrai para s>0, "
                             "fica fixo em s=0 e expande para s<0; o raio futuro faz o contrario: a sela (volume conservado, "
                             "pouso so na variedade estavel).", "por_s": out}

    def boost_paths():
        B = boost_f64(1.0)
        v = np.array([1.0, -1.0])
        rows = {}
        first_blas = first_mp = None
        for k in range(1, 13):
            v = B @ v
            ref = math.sqrt(2.0) * math.exp(-k)
            r_blas = abs(float(np.linalg.norm(v)) - ref) / ref
            w = np.linalg.matrix_power(B, k) @ np.array([1.0, -1.0])
            r_mp = abs(float(np.linalg.norm(w)) - ref) / ref
            rows["k=%d" % k] = {"rel_BLAS_B@v": r_blas, "rel_matrix_power": r_mp,
                                "BLAS_fica_na_reta_nula": bool(v[0] == -v[1]), "matrix_power_fica_na_reta_nula": bool(w[0] == -w[1])}
            if first_blas is None and r_blas > 1e-9:
                first_blas = k
            if first_mp is None and r_mp > 1e-9:
                first_mp = k
        return {"descricao": "O-f em float64 por outros caminhos aritmeticos (mesmo criterio rel <= 1e-9 do pre-registro, so "
                             "informativo): a reta nula passada e variedade estavel de medida nula; se o arredondamento quebra a "
                             "simetria (FMA no BLAS, ou cancelamento cosh-sinh na potencia da matriz), a componente futura cresce "
                             "como eps*e^{2k}. Instabilidade da sela, numerica, nao matematica (RP02).",
                "por_k": rows, "primeiro_k_acima_de_1e-9_BLAS": first_blas, "primeiro_k_acima_de_1e-9_matrix_power": first_mp,
                "numpy": np.__version__}

    def od_edge_k0():
        rng = rng_new()
        pairs = [(rand_state(rng, 2), rand_state(rng, 2)) for _ in range(500)]
        diffs = [fro(r - 0.5 * I2) - fro(Dmap(r) - 0.5 * I2) for pr in pairs for r in pr]
        return {"descricao": "borda k = 0 do O-d: C^0 = id; ||rho - I/2|| - ||D rho - I/2|| >= 0, > 0 com coerencia: a igualdade "
                             "do O-d so vale do primeiro passo em diante (D apaga as coerencias no primeiro passo).",
                "min": min(diffs), "max": max(diffs), "estados": len(diffs)}

    def full_channel_matrix():
        basis = [E00, E11, E01 + E10, 1j * (E01 - E10)]

        def coords(Xm):
            return [Xm[0, 0].real, Xm[1, 1].real, Xm[0, 1].real, Xm[0, 1].imag]

        Mc = np.column_stack([coords(Cmap(M["S"], Bm)) for Bm in basis])
        ev = np.linalg.eigvals(Mc)
        return {"descricao": "o canal otico completo C sobre as hermitianas 2x2 (base E00, E11, E01+E10, i(E01-E10)): "
                             "det 0 e posto 2 (D projeta as coerencias); o 'volume' otico mede-se nas populacoes (RP08).",
                "det_4x4": float(np.linalg.det(Mc)), "posto": int(np.linalg.matrix_rank(Mc)),
                "autovalores": sorted([complex(e) for e in ev], key=lambda z: -abs(z))}

    def two_clocks_stop():
        lam = M["lam"]
        rows = {}
        for k in (1, 10, 100, 1000):
            ck = lam ** k
            wk = 2 * math.atanh(ck)
            rows[str(k)] = {"omega_k (angulo: frequencia modular de rho_k)": wk,
                            "P_k = 2pi/omega_k (periodo modular)": 2 * math.pi / wk,
                            "g_k = beta*omega_k (face: taxa de Davies de rho_k)": beta0 * wk}
        return {"descricao": "ao longo do canal, para rho_k = diag((1+lam^k)/2, (1-lam^k)/2): a frequencia modular omega_k e a "
                             "taxa de Davies g_k = beta*|ln p0 - ln p1| = beta*omega_k descem juntas a zero; o periodo modular "
                             "cresce sem limite. No atrator tracial os DOIS relogios param (face finita). [DERIVED] identidade "
                             "do modelo; em III1 nao ha estado tracial (RP06).", "por_k": rows,
                "beta_vezes_omega1_igual_g01": abs(beta0 * M["omega1"] - M["g01"])}

    def t1_edges():
        out = {}
        T0 = np.zeros((0, 0), dtype=complex)
        H0 = np.zeros((0, 0), dtype=complex)
        out["n=0"] = {"TH-HT == i*1 (matrizes vazias)": bool(np.array_equal(T0 @ H0 - H0 @ T0, 1j * np.eye(0))),
                      "leitura": "sem nao vacuidade a igualdade vale trivialmente (C-T1-b, sombra numerica)"}
        rng = rng_new()
        mx = 0.0
        for _ in range(50):
            H = rand_herm(rng, 1)
            T = cgauss(rng, (1, 1))
            mx = max(mx, abs(fro(T @ H - H @ T - 1j * np.eye(1)) - 1.0))
        out["n=1"] = {"max | ||TH-HT-i1|| - 1 |": mx, "leitura": "em M1 tudo comuta; o residuo e exatamente |i| = sqrt(1) (V-T1-a, sombra)"}
        for n, npairs in ((16, 10), (32, 4)):
            I = np.eye(n, dtype=complex)
            b = (1j * I).reshape(-1, order="F")
            dev = 0.0
            tri = 0.0
            for _ in range(npairs):
                H = rand_herm(rng, n)
                T = cgauss(rng, (n, n))
                L = np.kron(H.T, I) - np.kron(I, H)
                v = np.linalg.lstsq(L, b, rcond=None)[0]
                dev = max(dev, abs(fro(L @ v - b) - math.sqrt(n)))
                tri = max(tri, abs(np.trace(T @ H - H @ T)) / (1 + fro(T) * fro(H)))
            out["n=%d" % n] = {"max |min residuo - sqrt n|": dev, "max |tr|/(1+||T||||H||)": tri, "pares": npairs}
        return {"descricao": "bordas e escala do T1: n = 0 (vacuo), n = 1, n = 16 e 32 (a lei sqrt(n) do melhor 'operador de tempo').",
                "por_n": out}

    def flow_scan():
        R = M["R"]
        ts = np.arange(-500, 501) / 100.0
        vals = []
        for t in ts:
            F = axiom_flow(R, float(t))
            vals.append(fro(F @ F - F))
        vals = np.array(vals)
        nz = vals[ts != 0.0]
        Fm = axiom_flow(R, -1.0)
        return {"descricao": "F(t) = R + e^{-t}(I-R) em t de -5 a 5 (passo 0,01): ||F^2 - F|| = e^{-t}|1 - e^{-t}| so zera em t = 0; "
                             "para t < 0, F(t) e o inverso linear da face e nao e estocastico (entradas negativas): o inverso da "
                             "face nao e canal (liga T9 a T7).",
                "min_fora_de_t0": float(nz.min()), "em_t0": float(vals[ts == 0.0][0]),
                "F(-1)": Fm, "menor_entrada_F(-1)": float(Fm.min())}

    def agape_shadow():
        rng = rng_new()
        x = rand_state(rng, 2)
        g = M["G1"]
        ss = [-10.0, -1.0, 0.0, 1.0, 10.0, 100.0, 700.0]
        rows = {repr(s): {"|x01(s)|": abs(dephase(g, s, x)[0, 1]), "e^{-s}|x01|": math.exp(-s) * abs(x[0, 1])} for s in ss}
        under = None
        for s in range(700, 800):
            if math.exp(-s) == 0.0:
                under = s
                break
        return {"descricao": "a coerencia na lei de escala da Agape (instancia coherenceScaling, g01 = 1): |x01(s)| = e^{-s}|x01| "
                             "para s real, inclusive s < 0 (mapa linear; a subida nao tem teto). Em float64, e^{-s} vira 0 "
                             "exato a partir de s = %s (underflow): sombra numerica do abismo, nao um zero (RP18)." % under,
                "por_s": rows, "primeiro_s_inteiro_com_exp(-s)==0_em_float64": under}

    def kernel_control_shadows():
        out = {}
        out["C-T1-a"] = {"TH-HT (T=E01, H=E10)": E01 @ E10 - E10 @ E01}
        out["C-T4-b"] = {"psi+ != E_D psi+": fro(PSI_PLUS - Dmap(PSI_PLUS)),
                         "||T_30 psi+ - E_D psi+|| (g=1)": fro(dephase(M["G1"], 30.0, PSI_PLUS) - Dmap(PSI_PLUS))}
        out["C-T5-a"] = {"E00 e E11 fixos por T_t (max)": max(fro(dephase(M["G1"], t, E) - E) for t in (0.1, 1.0, 10.0) for E in (E00, E11))}
        Y = dephase(M["G1"], 0.0, PSI_PLUS)
        out["C-T7-a"] = {"||T_0 psi+ - psi+||": fro(Y - PSI_PLUS), "autovalores": np.linalg.eigvalsh(Y)}
        out["C-T8-a"] = {"|x01| e^{-2s} vs e^{-s}|x01| em s=1": [abs(dephase(M["G1"], 2.0, PSI_PLUS)[0, 1]), math.exp(-1) * 0.5]}
        out["C-T8-b"] = {"|(T_1 x)_00| vs e^{-1}|x_00| (x=psi+)": [abs(dephase(M["G1"], 1.0, PSI_PLUS)[0, 0]), math.exp(-1) * 0.5]}
        out["C-T9-a"] = {"max_t ||F(t)^2 - F(t)|| com P = 1": max(fro(axiom_flow(np.eye(2), t) @ axiom_flow(np.eye(2), t) - axiom_flow(np.eye(2), t)) for t in (-1.0, 0.0, 1.0, 10.0))}
        F0 = axiom_flow(M["R"], 0.0)
        out["C-T9-b"] = {"||F(0) - 1||": fro(F0 - np.eye(2)), "||F(0)^2 - F(0)||": fro(F0 @ F0 - F0)}
        out["C-T10-a"] = {"leitura com kappa=0 e constante (max |e^{i0t} - 1|)": 0.0}
        out["C-T10-b"] = {"min_t |e^{-r(t+P)} - e^{-rt}| (r=1, P=1, t em [0,10])": float(min(abs(math.exp(-(t + 1.0)) - math.exp(-t)) for t in np.linspace(0, 10, 101)))}
        return {"descricao": "sombras NUMERICAS dos controles de kernel (informativo; o veredito deles e do construtor do kernel).",
                "por_controle": out}

    guard("varredura_beta", sweep_beta)
    guard("varredura_theta", sweep_theta)
    guard("varredura_tempo_defasagem", sweep_time_dephase)
    guard("varredura_boost_s", sweep_boost_s)
    guard("O-f_caminhos_aritmeticos_float64", boost_paths)
    guard("O-d_borda_k0", od_edge_k0)
    guard("canal_completo_C_4x4", full_channel_matrix)
    guard("os_dois_relogios_param_no_atrator", two_clocks_stop)
    guard("T1_bordas_e_escala", t1_edges)
    guard("T9_varredura_do_fluxo", flow_scan)
    guard("T8_sombra_do_abismo", agape_shadow)
    guard("sombras_numericas_dos_controles_de_kernel", kernel_control_shadows)
    return A


# ----------------------------------------------------------------------------- onto / known / open
def onto_known_open(prereg):
    out = {"ONTO": [], "KNOWN": [], "OPEN": []}
    for fr in prereg["mapeamento_frases"]:
        for cl in fr["clausulas"]:
            for tag in ("ONTO", "KNOWN", "OPEN"):
                if "[" + tag + "]" in cl["marca"]:
                    out[tag].append({"frase": fr["frase"], "trecho": cl["trecho"], "marca": cl["marca"]})
    exc = [{"excerto": e["excerto"], "marca": e["marca"]} for e in prereg["mapeamento_excertos"] if "ONTO" in e["marca"] or "DECLARADO" in e["marca"]]
    sub = []
    for a in prereg["afirmacoes"]:
        for s in a["subitens"]:
            if s["face"] in ("citacao", "leitura"):
                sub.append({"id": s["id"], "face": s["face"], "rotulo": "CITADA" if s["face"] == "citacao" else "LEITURA",
                            "esperado_preregistrado": s["esperado"]})
    return {"nota": "lista lida do PREREGISTRO.json congelado (nao e interpretacao deste ensaio). [ONTO] nao se testa; "
                    "[KNOWN] entra por citacao; [OPEN] fica aberto. Nenhum destes recebe PASSA de teste.",
            "contagem": {k: len(v) for k, v in out.items()}, "clausulas": out,
            "excertos_ONTO_ou_DECLARADO": exc, "subitens_CITADA_LEITURA": sub}


# ----------------------------------------------------------------------------- main
def parse_choices():
    choices = []
    for ln in __doc__.split("ESCOLHAS DO CONSTRUTOR")[1].split("\n")[1:]:
        s = ln.strip()
        if re.match(r"^E\d+\s", s):
            choices.append(s)
        elif s and choices:
            choices[-1] += " " + s
    return choices


def main():
    global SEED
    mode = "infra" if "--infra" in sys.argv else "ensaio"
    att_dir, att_n = new_attempt_dir(mode)
    LOG.open(os.path.join(att_dir, "run_optico.log"))
    LOG("F1.TEMPO — face otica — tentativa %03d (%s) — %s" % (att_n, mode, att_dir))
    rb = read_bytes(os.path.abspath(__file__))
    res = {"documento": "RESULTADO_OPTICO — F1.TEMPO (o tempo que nao se deixa nomear), face otica",
           "unidade": "F1.TEMPO", "trilha": "TEMPO", "gerencia": "c1",
           "papel": "construtor otico (subagente do workflow posto-e-tempo da gerencia c1)",
           "estatuto_do_documento": "[REAL — medido aqui, modelo sintetico] por subitem; PASSA = validade matematica na face "
                                    "testada, nao creditacao; sem veredito global; o gate nao se move; beta na natureza a 5 sigma "
                                    "nao e tocado; nenhum dado observado.",
           "tentativa": att_n, "modo": mode, "inicio_local": time.strftime("%Y-%m-%d %H:%M:%S"),
           "ambiente": {"python": sys.version, "numpy": np.__version__, "plataforma": platform.platform(),
                        "flags": {"dont_write_bytecode": sys.flags.dont_write_bytecode, "ignore_environment": sys.flags.ignore_environment,
                                  "safe_path": sys.flags.safe_path}},
           "runner": {"arquivo": os.path.abspath(__file__), "sha256": sha256_bytes(rb), "bytes": len(rb)},
           "escolhas_do_construtor_[INPUT]": parse_choices()}
    invalid = []
    LOG("0. preflight (FREEZE, pre-registro, texto do operador)")
    checks, prereg, fz = preflight()
    res["preflight"] = {"n": len(checks), "falhas": [c for c in checks if not c["ok"]], "todos_ok": all(c["ok"] for c in checks),
                        "itens": checks}
    LOG("   preflight: %d itens, %d falhas" % (len(checks), len(res["preflight"]["falhas"])))
    if not res["preflight"]["todos_ok"]:
        invalid.append("preflight: divergencia com o FREEZE (nao ensaiar)")
    m = re.search(r"default_rng\((\d+)\)", prereg["modelo_otico"]["sementes"])
    SEED = int(m.group(1))
    res["semente"] = SEED
    LOG("   semente lida do pre-registro: %d" % SEED)
    LOG("1. impressao digital do tgl_kernel (inicio)")
    fp0 = kernel_fingerprint()
    LOG("   meta %s src %s" % (fp0["meta_sha256"][:16], fp0["src_sha256"][:16]))
    LOG("2. beta em runtime (bytes do um.py; sem executar)")
    binfo = read_beta(prereg)
    res["beta"] = binfo
    LOG("   alpha literal %s (l.%s; SEALED l.%s igual=%s) -> beta = %r ; dif conferencia %r ; confere=%s" % (
        binfo.get("alpha_literal"), binfo.get("linha_alpha"), binfo.get("SEALED_CODATA_ALPHA_linha"),
        binfo.get("alpha_igual_SEALED"), binfo.get("beta_runtime"), binfo.get("dif_abs_conferencia"), binfo.get("confere")))
    if not binfo.get("confere"):
        invalid.append("beta lido nao confere com a conferencia (|dif| > 1e-15) ou leitura de alpha defeituosa")
    if invalid:
        res["valido"] = False
        res["motivos_de_INVALIDO"] = invalid
        res["impressao_digital_kernel"] = {"inicio": fp0}
        write_json_atomic(os.path.join(att_dir, "RESULTADO_OPTICO.json"), res)
        LOG("INVALIDO antes do ensaio: %s" % invalid)
        LOG.close()
        return 2
    M = build_model(binfo["beta_runtime"])
    conf = prereg["numeros_de_conferencia"]
    res["modelo"] = {"beta": M["beta"], "theta_M": M["theta_M"], "S": M["S"], "H_ot": M["H_ot"], "T": M["T"], "R": M["R"],
                     "lambda": M["lam"], "a": M["a"], "rho1": M["rho1"], "omega1": M["omega1"], "P1": M["P1"], "g01": M["g01"],
                     "descricao": prereg["modelo_otico"]}
    LOG("3. autotestes do runner")
    ats, at_ok, at_inval = autotests(M, prereg)
    res["autotestes"] = {"itens": ats, "aprovado": at_ok}
    if at_inval:
        invalid.append("condicao de INVALIDO pre-registrada nos autotestes: %s" % at_inval)
    if not at_ok:
        invalid.append("runner nao aprovado nos autotestes")
    subs = {}
    ctl = {}
    ann = None
    if mode == "ensaio":
        LOG("4. subitens oticos pre-registrados")
        plan = [("T1.o", lambda: test_T1o(M, prereg)), ("T3.o", lambda: test_T3o(M, prereg, conf)),
                ("T4.o", lambda: test_T4o(M, prereg, conf)), ("T6.o", lambda: test_T6o(M, prereg, conf)),
                ("T7.o", lambda: test_T7o(M, prereg, conf)), ("T8.o", lambda: test_T8o(M, prereg, conf)),
                ("T9.o", lambda: test_T9o(M, prereg, conf)), ("T10.o", lambda: test_T10o(M, prereg)),
                ("T11.o", lambda: test_T11o(M, prereg, conf))]
        for sid, fn in plan:
            LOG(" - %s" % sid)
            t0 = time.time()
            try:
                subs[sid] = fn()
            except Exception:
                tb = traceback.format_exc()
                LOG("   ERRO DO RUNNER em %s:\n%s" % (sid, tb))
                subs[sid] = {"id": sid, "erro_do_runner": tb, "todos_os_criterios_ok": False}
            subs[sid]["segundos"] = round(time.time() - t0, 2)
        LOG("5. controles oticos")
        try:
            ctl = controls(M, prereg, subs)
        except Exception:
            tb = traceback.format_exc()
            LOG("   ERRO DO RUNNER nos controles:\n%s" % tb)
            ctl = {"erro_do_runner": tb}
        LOG("6. anexo: achados fora do pre-registro (informativo)")
        ann = annex(M, prereg, subs)
    LOG("7. impressao digital do tgl_kernel (fim)")
    fp1 = kernel_fingerprint()
    same = (fp0["meta_sha256"] == fp1["meta_sha256"] and fp0["src_sha256"] == fp1["src_sha256"])
    res["impressao_digital_kernel"] = {"inicio": fp0, "fim": fp1, "iguais": same}
    LOG("   meta %s src %s iguais=%s" % (fp1["meta_sha256"][:16], fp1["src_sha256"][:16], same))
    if not same:
        invalid.append("impressao digital do tgl_kernel alterada durante o ensaio")
    valid = not invalid
    res["valido"] = valid
    res["motivos_de_INVALIDO"] = invalid
    if mode == "infra":
        res["nota"] = "verificacao de infraestrutura (preflight, beta, autotestes); nenhum subitem pre-registrado foi medido"
        sha, nb = write_json_atomic(os.path.join(att_dir, "RESULTADO_OPTICO.json"), res)
        LOG("infra: valido=%s ; resultado sha256 %s (%d B)" % (valid, sha, nb))
        LOG.close()
        return 0 if valid else 2
    # vereditos por subitem
    for sid, d in subs.items():
        if not valid or "erro_do_runner" in d:
            d["resultado"] = "INVÁLIDO"
        else:
            d["resultado"] = "PASSA" if d.get("todos_os_criterios_ok") else "FALHA"
        d.pop("_cT4a", None)
        d.pop("_ws", None)
    ctl_ok = {}
    for cid, d in ctl.items():
        if isinstance(d, dict) and "comportou_se_como_registrado" in d:
            ctl_ok[cid] = bool(d["comportou_se_como_registrado"]) and valid
    # por afirmacao (so a face otica)
    links = {}
    for c in prereg["controles"]:
        if "otico" in c["face"]:
            for t in [x.strip() for x in c["liga"].split(",")]:
                links.setdefault(t, []).append(c["id"])
    por = {}
    for a in prereg["afirmacoes"]:
        tid = a["id"]
        oticos = [s["id"] for s in a["subitens"] if s["face"] == "otico"]
        cit = [s["id"] for s in a["subitens"] if s["face"] == "citacao"]
        lei = [s["id"] for s in a["subitens"] if s["face"] == "leitura"]
        ker = [s["id"] + (" (obrigatorio)" if s["obrigatorio"] else " (opcional)") for s in a["subitens"] if s["face"] == "kernel"]
        cl = links.get(tid, [])
        if not oticos:
            fo = "SEM_FACE_OTICA"
        elif not valid or any(subs[s]["resultado"] == "INVÁLIDO" for s in oticos) or any(c not in ctl_ok for c in cl):
            fo = "INVÁLIDO"
        elif all(subs[s]["resultado"] == "PASSA" for s in oticos) and all(ctl_ok[c] for c in cl):
            fo = "PASSA"
        else:
            fo = "FALHA"
        por[tid] = {"titulo": a["titulo"], "subitens_oticos": {s: subs[s]["resultado"] for s in oticos},
                    "controles_oticos_ligados": {c: ("comportou-se como registrado" if ctl_ok.get(c) else "NAO") for c in cl},
                    "resultado_da_face_otica": fo,
                    "citadas": {s: "CITADA (entra por citacao; nunca PASSA de teste)" for s in cit},
                    "leituras": {s: "LEITURA (entra marcada; nunca PASSA de teste)" for s in lei},
                    "subitens_de_kernel_fora_deste_ensaio": ker,
                    "veredito_da_afirmacao": "pendente da face kernel (construtor do kernel); esta tabela e so a face otica"}
    res["subitens_oticos"] = subs
    res["controles_oticos"] = ctl
    res["controles_oticos_todos_como_registrado"] = bool(ctl_ok) and all(ctl_ok.values()) and len(ctl_ok) == 10
    res["por_afirmacao_face_otica"] = por
    res["onto_known_open"] = onto_known_open(prereg)
    res["regra"] = prereg["regra_de_decisao"]
    sha_a, nb_a = write_json_atomic(os.path.join(att_dir, "ACHADOS_FORA_DO_PREREGISTRO.json"), ann)
    res["anexo_achados_fora_do_preregistro"] = {"arquivo": "ACHADOS_FORA_DO_PREREGISTRO.json", "sha256": sha_a, "bytes": nb_a}
    res["fim_local"] = time.strftime("%Y-%m-%d %H:%M:%S")
    res["segundos"] = round(time.time() - T_START, 1)
    sha_r, nb_r = write_json_atomic(os.path.join(att_dir, "RESULTADO_OPTICO.json"), res)
    LOG("8. resumo")
    for sid, d in subs.items():
        LOG("   %-6s %s (%d criterios)" % (sid, d["resultado"], d.get("n_criterios", 0)))
    for cid, ok in ctl_ok.items():
        LOG("   %-8s %s" % (cid, "comportou-se como registrado" if ok else "NAO"))
    for tid, d in por.items():
        LOG("   %-4s face otica: %s" % (tid, d["resultado_da_face_otica"]))
    LOG("   valido=%s ; resultado sha256 %s (%d B) ; anexo sha256 %s (%d B)" % (valid, sha_r, nb_r, sha_a, nb_a))
    LOG.close()
    for name in ("RESULTADO_OPTICO.json", "ACHADOS_FORA_DO_PREREGISTRO.json", "run_optico.log"):
        copy_bytes_atomic(os.path.join(att_dir, name), os.path.join(HERE, name))
    return 0 if valid else 2


if __name__ == "__main__":
    sys.exit(main())
