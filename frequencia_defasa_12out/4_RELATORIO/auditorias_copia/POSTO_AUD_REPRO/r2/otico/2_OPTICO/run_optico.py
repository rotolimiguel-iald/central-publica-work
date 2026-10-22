# -*- coding: utf-8 -*-
"""
run_optico.py -- ENSAIO OTICO SINTETICO da unidade F1.FREQUENCIA (trilha POSTO), gerencia c1.
Rodada 2 do construtor otico (12/10/2026). A rodada 1 (12/10, 13:31-13:56 local) esta preservada byte a byte
em rodada1_20261012_1356/ (PRESERVACAO_RODADA1.json); esta rodada reconstroi o ensaio do zero, sem ler o
codigo da rodada 1.

O que faz (escrita SO dentro de 2_OPTICO):
  0. confere o FREEZE do pre-registro (sha256 dos bytes de PREREGISTRO.json e PREREGISTRO.md); se divergir, PARA
     e grava so a divergencia;
  1. confere os pinos (um.py, verbatins V1-V4, core, modulos do kernel, mapa, inventario) por sha256 dos bytes;
  2. le ALPHA_FINE_CODATA_2018 nos BYTES do um.py (sem executa-lo) e calcula beta = alpha*sqrt(e) em runtime;
     confere com o valor congelado no pre-registro (lido do JSON congelado; nenhum valor de beta escrito aqui);
  3. constroi os objetos pre-registrados -- rho*, Q0, R, Q_th pela receita do um.py (l.6512-6519); S(th) e
     F_th(1) = rhoOut th pela receita do kernel (SMatrix.lean); o semigrupo dephase g t (Ergodicity.lean, G3:
     amortecimento entrada a entrada e^{-t g_ij}, g_ii = 0, g_ij > 0) e D_inf = diagExpect (CondExpect.lean) --
     e testa CADA parte com a tolerancia fixada; roda os controles C1-C14 (tem de falhar sem a hipotese); varre
     G_th x G_t x gamma e, como anexo FORA do pre-registro, grades densas, taxas assimetricas e bordas;
  4. grava RESULTADO_OPTICO.json, CONFERENCIA_FREEZE.json e LOG_OPTICO.txt (temporario -> conferir -> substituir;
     versao anterior desta rodada vai para tentativas/).

Estatuto: PASSA_O = validade matematica na face OTICA testada (numerica: float64/complex128; mpmath dps 50 nas
identidades em theta_M), nao creditacao; nao move gate; nao fala da natureza. Nada aqui executa o um.py, o Lean,
a Bancada ou provedor; nenhum dado observado.
"""
import hashlib
import json
import math
import os
import platform
import re
import sys
import time
from datetime import datetime, timezone

import mpmath as mp
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

# ------------------------------------------------------------------------------------------------ caminhos
AQUI = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(AQUI)
PRE_DIR = os.path.join(WORK, "1_PREREGISTRO")
PRE_JSON = os.path.join(PRE_DIR, "PREREGISTRO.json")
PRE_MD = os.path.join(PRE_DIR, "PREREGISTRO.md")
FREEZE = os.path.join(PRE_DIR, "FREEZE.json")
NOS = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s"
UMPY = os.path.join(NOS, "um.py")
CORE = os.path.join(NOS, "um_absoluto.json")
KERNEL = os.path.join(NOS, "tgl_kernel")
KERNEL_LONGO = "\\\\?\\" + KERNEL
V12 = r"C:\IALD\Central de Patentes\work\cunhagens_12out"
V10 = r"C:\IALD\Central de Patentes\work\cunhagens_10out"
VERBATINS = {
    "V1": os.path.join(V12, "OPERADOR_10out_posto_rank_texto_verbatim.txt"),
    "V2": os.path.join(V12, "OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"),
    "V3": os.path.join(V10, "OPERADOR_10out_posto_rank_verbatim.txt"),
    "V4": os.path.join(V10, "OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"),
}
SAIDA_JSON = os.path.join(AQUI, "RESULTADO_OPTICO.json")
SAIDA_LOG = os.path.join(AQUI, "LOG_OPTICO.txt")
CONF_FREEZE = os.path.join(AQUI, "CONFERENCIA_FREEZE.json")
TENTATIVAS = os.path.join(AQUI, "tentativas")

# ------------------------------------------------------------------- tolerancias (as do protocolo congelado)
# Cada valor abaixo e conferido contra o texto congelado de PREREGISTRO.json['protocolo_otico'] em runtime.
TOL_ID = 1e-12                      # |x - y| <= 1e-12 (float64)
TOL_ID_MP = mp.mpf("1e-40")         # <= 1e-40 (mpmath)
ZERO_MAX, NAOZERO_MIN = 1e-12, 1e-6  # TOL_ZERO: |X|_F <= 1e-12 zero; >= 1e-6 nao zero; entre: AMBIGUO
RANK_NULO, RANK_NAONULO = 1e-12, 1e-6  # RANK: sigma <= 1e-12 nulo; >= 1e-6 nao nulo; entre: AMBIGUO
PUREZA_UM, PUREZA_MENOR = 1e-12, 1e-6  # PUREZA: |Tr rho^2 - 1| <= 1e-12: = 1; Tr rho^2 <= 1 - 1e-6: < 1
TOL_REL = 1e-10                     # |x - y| <= 1e-10 |y| (decaimento)
TOL_LEAK = 1e-15                    # |Tr(rho* Q_thM) - beta| <= 1e-15 (float64)
TOL_LEAK_MP = mp.mpf("1e-45")       # <= 1e-45 (mpmath)
CONF_OPERADOR = 5e-7                # |beta - numero do operador| <= 5e-7
OSC_FOLGA = 1e-9                    # max - min >= cos thM - 1e-9
OSC_N = 100000                      # janelas com inicio em [0, 1e5 - W]
C11_TOL = 1e-10                     # C11: sin^2(n pi) <= 1e-10 em float64 ate 1e5
C10_DELTA = 1e-3                    # C10: variacao >= 1e-3
CONF_BETA_MP = 1e-17                # |beta_mp - beta| <= 1e-17
SEMENTE = 20261012                  # default_rng(20261012)
MP_DPS = 50                         # mpmath dps 50

CONFERE_TEXTO = [  # (nome, valor como escrito no protocolo, chave do protocolo)
    ("TOL_ID float64", "1e-12", "TOL_ID"), ("TOL_ID mpmath", "1e-40", "TOL_ID"),
    ("TOL_ZERO zero", "1e-12", "TOL_ZERO"), ("TOL_ZERO nao zero", "1e-6", "TOL_ZERO"),
    ("RANK nulo", "1e-12", "RANK"), ("RANK nao nulo", "1e-6", "RANK"),
    ("PUREZA = 1", "1e-12", "PUREZA"), ("PUREZA < 1", "1 - 1e-6", "PUREZA"),
    ("TOL_REL", "1e-10", "TOL_REL"), ("TOL_LEAK float64", "1e-15", "TOL_LEAK"), ("TOL_LEAK mpmath", "1e-45", "TOL_LEAK"),
    ("CONF_OPERADOR", "5e-7", "CONF_OPERADOR"), ("OSC folga", "1e-9", "OSC"), ("OSC N", "1e5", "OSC"),
    ("semente", "default_rng(20261012)", "amostras"), ("mpmath", "dps 50", "precisao"), ("beta conf mp", "1e-17", "beta"),
]


# ============================================================================================ utilidades
def agora_local():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def agora_utc():
    return datetime.now(timezone.utc).isoformat()


def sha256_arquivo(p, limite=None):
    h = hashlib.sha256()
    lidos = 0
    with open(p, "rb") as fh:
        while True:
            n = 1 << 20
            if limite is not None:
                n = min(n, limite - lidos)
                if n <= 0:
                    break
            b = fh.read(n)
            if not b:
                break
            h.update(b)
            lidos += len(b)
    return h.hexdigest()


def preserva(p):
    """Se p existe, move-o para tentativas/ com carimbo (nunca apaga)."""
    if os.path.exists(p):
        os.makedirs(TENTATIVAS, exist_ok=True)
        carimbo = time.strftime("%Y%m%d_%H%M%S")
        destino = os.path.join(TENTATIVAS, os.path.basename(p) + "." + carimbo)
        k = 1
        while os.path.exists(destino):
            destino = os.path.join(TENTATIVAS, os.path.basename(p) + "." + carimbo + "_%d" % k)
            k += 1
        os.replace(p, destino)
        return destino
    return None


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        xf = float(x)
        if math.isnan(xf) or math.isinf(xf):
            return repr(xf)
        return xf
    if isinstance(x, (complex, np.complexfloating)):
        return [jsonable(float(x.real)), jsonable(float(x.imag))]
    if isinstance(x, mp.mpf):
        return mp.nstr(x, 30)
    if isinstance(x, mp.mpc):
        return [mp.nstr(x.real, 30), mp.nstr(x.imag, 30)]
    if isinstance(x, np.ndarray):
        return jsonable(x.tolist())
    return x


def escrever_json(p, obj):
    txt = json.dumps(jsonable(obj), ensure_ascii=False, indent=1)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(txt)
    if os.path.getsize(tmp) <= 0:
        raise RuntimeError("FALHA VISIVEL: JSON vazio " + p)
    preserva(p)
    os.replace(tmp, p)
    return dict(caminho=p, bytes=os.path.getsize(p), sha256=sha256_arquivo(p))


class Log:
    def __init__(self, p):
        self.p = p
        self.tmp = p + ".tmp"
        self.fh = open(self.tmp, "w", encoding="utf-8")

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.fh.write(s + "\n")
        self.fh.flush()

    def fechar(self):
        self.fh.close()
        if os.path.getsize(self.tmp) <= 0:
            raise RuntimeError("FALHA VISIVEL: log vazio")
        preserva(self.p)
        os.replace(self.tmp, self.p)


def impressao_digital_kernel():
    """Mesmo metodo de 0_LEVANTAMENTO / 1_PREREGISTRO (somente leitura)."""
    meta, lean = [], []
    nfiles = total = 0
    for dp, dns, fns in os.walk(KERNEL_LONGO):
        dns.sort()
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            st = os.stat(p)
            rel = os.path.relpath(p, KERNEL_LONGO).replace("\\", "/")
            meta.append(f"{rel}\t{st.st_size}\t{st.st_mtime_ns}")
            nfiles += 1
            total += st.st_size
            if rel.endswith(".lean") and not rel.startswith(".lake/"):
                with open(p, "rb") as fh:
                    lean.append(f"{rel}\t{hashlib.sha256(fh.read()).hexdigest()}")
    meta.sort()
    lean.sort()
    return dict(quando_local=agora_local(), n_arquivos=nfiles, bytes_total=total,
                sha256_metadados=hashlib.sha256("\n".join(meta).encode("utf-8")).hexdigest(),
                n_lean_fora_lake=len(lean),
                sha256_conteudo_lean=hashlib.sha256("\n".join(lean).encode("utf-8")).hexdigest())


# =================================================================================== classificadores (fail-closed)
def finito(*xs):
    for x in xs:
        a = np.asarray(x)
        if not np.all(np.isfinite(a)):
            return False
    return True


def cls_zero(v):
    v = float(v)
    if not math.isfinite(v):
        return "NAN"
    if v <= ZERO_MAX:
        return "ZERO"
    if v >= NAOZERO_MIN:
        return "NAO_ZERO"
    return "AMBIGUO"


def cls_pureza(p):
    p = float(p)
    if not math.isfinite(p):
        return "NAN"
    if abs(p - 1.0) <= PUREZA_UM:
        return "=1"
    if p <= 1.0 - PUREZA_MENOR:
        return "<1"
    return "AMBIGUO"


def posto(A):
    """RANK pre-registrado: sigma <= 1e-12 nulo; >= 1e-6 nao nulo; entre: AMBIGUO (posto None)."""
    A = np.asarray(A)
    if not finito(A):
        return dict(posto=None, nulidade=None, ambiguos=-1, sigmas=[])
    s = np.linalg.svd(A, compute_uv=False)
    nn = int(np.sum(s >= RANK_NAONULO))
    nu = int(np.sum(s <= RANK_NULO))
    amb = len(s) - nn - nu
    return dict(posto=(nn if amb == 0 else None), nulidade=(nu if amb == 0 else None), ambiguos=amb,
                sigmas=[float(x) for x in s])


def maxabs(X):
    return float(np.max(np.abs(np.asarray(X)))) if np.asarray(X).size else 0.0


def mx(*vals):
    """max que PROPAGA NaN (fail-closed): o max() do Python descarta NaN conforme a ordem; aqui NaN vira NaN."""
    return float(np.max(np.array([abs(v) if isinstance(v, (complex, np.complexfloating)) else v for v in vals], dtype=float)))


def tem_nan(x):
    if isinstance(x, dict):
        return any(tem_nan(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return any(tem_nan(v) for v in x)
    if isinstance(x, np.ndarray):
        return bool(np.any(np.isnan(x))) if np.issubdtype(x.dtype, np.number) else False
    if isinstance(x, (float, np.floating)):
        return math.isnan(float(x))
    if isinstance(x, (complex, np.complexfloating)):
        return math.isnan(x.real) or math.isnan(x.imag)
    return False


def frob(X):
    return float(np.linalg.norm(np.asarray(X)))


def mp_maxabs(X, Y=None):
    m = mp.mpf(0)
    for i in range(X.rows):
        for j in range(X.cols):
            d = X[i, j] - (Y[i, j] if Y is not None else 0)
            m = max(m, abs(d))
    return m


# ===================================================================================== objetos pre-registrados
E00 = np.array([[1, 0], [0, 0]], dtype=complex)        # Matrix.single 0 0 1 (o termo de rhoOut)
GROT = np.array([[0, 1], [-1, 0]], dtype=complex)      # Grot = !![0, 1; -1, 0] (SMatrix.lean:40)
I2 = np.eye(2, dtype=complex)


def S(th):
    """Kernel: Smat th = (cos th) . 1 + (sin th) . Grot = [[c, s], [-s, c]] (SMatrix.lean:45)."""
    return complex(np.cos(th)) * I2 + complex(np.sin(th)) * GROT


def rho_out(th):
    """Kernel: rhoOut th = Smat th * single 0 0 1 * (Smat th)^H (SMatrix.lean:263) = F_th(1)."""
    s = S(th)
    return s @ E00 @ s.conj().T


def umpy_objetos(th):
    """Receita do um.py (fractal_dephasing_principle, l.6512-6519), com th no lugar de theta_M."""
    P = np.array([[1.0, 0.0], [0.0, 0.0]])
    omega_I = float(np.trace(P))
    Q0 = np.eye(2) - P
    anti0 = Q0 @ P + P @ Q0
    c, s = np.cos(th), np.sin(th)
    R = np.array([[c, -s], [s, c]])
    Qth = R @ Q0 @ R.T
    leak = float(np.trace(P @ Qth))
    return dict(P=P, omega_I=omega_I, Q0=Q0, anti0=anti0, R=R, Qth=Qth, leak=leak, c=float(c), s=float(s))


def dephase(g, t, x):
    """Kernel (Ergodicity.lean:184, G3): (T_t x)_ij = exp(-(t * g_ij)) * x_ij -- Schur puro."""
    return np.exp(-(t * np.asarray(g, dtype=float))) * x


def diag_expect(x):
    """Kernel (CondExpect.lean:87): diagExpect x = diagonal x.diag = D_inf (limite exato do semigrupo)."""
    return np.diag(np.diag(x))


def g_sim(gamma):
    return np.array([[0.0, gamma], [gamma, 0.0]])


def g_assim(g01, g10):
    return np.array([[0.0, g01], [g10, 0.0]])


def anticomm(A, B):
    return A @ B + B @ A


def det2(M):
    return M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]


# =========================================================================================== a parte (registro)
class Parte:
    def __init__(self, pid, meta, afirm):
        self.id = pid
        self.meta = meta          # linha do pre-registro: id, enunciado, K, O, tolerancia, falsificador, esperado
        self.afirm = afirm        # afirmacao: id, titulo, estatuto
        self.checks = []
        self.extra = {}

    def check(self, nome, ok, **numeros):
        if ok is not None:
            ok = bool(ok)
        if tem_nan(numeros):          # fail-closed: NaN em qualquer numero do check -> SEM_VEREDITO, nunca PASSA
            ok = None
            nome = nome + " [NaN -> SEM_VEREDITO]"
        self.checks.append(dict(nome=nome, ok=ok, numeros=jsonable(numeros)))
        return ok

    def face_O(self):
        if not self.checks:
            return "NAO_APLICAVEL_O"
        if any(c["ok"] is None for c in self.checks):
            return "SEM_VEREDITO_O"
        if all(c["ok"] for c in self.checks):
            return "PASSA_O"
        return "FALHA_O"


class Controle:
    def __init__(self, cid, texto):
        self.id = cid
        self.texto = texto
        self.obs = {}
        self.falha_sem_hipotese = None
        self.nota = ""

    def fechar(self, falhou, nota, **obs):
        self.falha_sem_hipotese = (None if falhou is None else bool(falhou))
        self.nota = nota
        self.obs = jsonable(obs)


# ============================================================================================== o ensaio
class Ensaio:
    def __init__(self, log, pre):
        self.log = log
        self.pre = pre
        self.partes = {}
        self.controles = {}
        self.anexo = []          # achados fora do pre-registro
        self.varredura = {}
        self.decisoes = []       # escolhas do construtor [INPUT do construtor], fixadas antes de rodar
        self.alertas = []
        afirmacoes = {a["id"]: a for a in pre["c_afirmacoes"]}
        self.ordem_partes = []
        for a in pre["c_afirmacoes"]:
            for linha in a["partes"]:
                meta = dict(zip(["id", "enunciado", "K", "O", "tolerancia", "falsificador", "esperado"], linha))
                self.partes[meta["id"]] = Parte(meta["id"], meta, dict(id=a["id"], titulo=a["titulo"],
                                                                       estatuto=a["estatuto"],
                                                                       controles=a.get("controles", []),
                                                                       nao_afirma=a.get("nao_afirma", "")))
                self.ordem_partes.append(meta["id"])
        self.afirmacoes = afirmacoes
        for txt in pre["d_controles"]["lista"]:
            cid = txt.split(" ", 1)[0]
            self.controles[cid] = Controle(cid, txt)

    def P(self, pid):
        return self.partes[pid]

    def C(self, cid):
        return self.controles[cid]


# ---------------------------------------------------------------------------------------------- beta
def ler_beta(pre, log):
    raw = open(UMPY, "rb").read()
    txt = raw.decode("utf-8")
    out = dict(um_py=dict(caminho=UMPY, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()), ok=False)

    def linha_de(pos):
        return txt.count("\n", 0, pos) + 1

    ms = list(re.finditer(r"^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)[ \t]*\r?$", txt, re.M))
    out["alpha_ocorrencias_no_inicio_de_linha"] = [dict(linha=linha_de(m.start()), texto=m.group(1)) for m in ms]
    linha_esperada = pre["ancoras_um_py"]["ALPHA_FINE_CODATA_2018"]
    if len(ms) != 1:
        out["falha"] = "ALPHA_FINE_CODATA_2018 nao e linha unica no inicio de linha"
        return out
    alpha_texto = ms[0].group(1)
    alpha_linha = linha_de(ms[0].start())
    out.update(alpha_texto=alpha_texto, alpha_linha=alpha_linha, alpha_linha_pre_registrada=linha_esperada,
               alpha_linha_confere=(alpha_linha == linha_esperada),
               alpha_texto_confere_pre=(alpha_texto == pre["beta_runtime"]["alpha_texto"]))
    ms2 = list(re.finditer(r"^SEALED_CODATA_ALPHA = ([0-9.eE+-]+)", txt, re.M))
    out["SEALED_CODATA_ALPHA"] = [dict(linha=linha_de(m.start()), texto=m.group(1)) for m in ms2]
    sealed_texto = ms2[0].group(1) if len(ms2) == 1 else None
    out["SEALED_igual_ao_alpha"] = (sealed_texto == alpha_texto)
    mb = list(re.finditer(r"^BETA_TGL = ALPHA_FINE_CODATA_2018 \* ONE \* math\.sqrt\(math\.e\)", txt, re.M))
    out["receita_BETA_TGL_linhas"] = [linha_de(m.start()) for m in mb]
    alpha = float(alpha_texto)
    beta = alpha * math.sqrt(math.e)                      # beta nunca literal: alpha (bytes do um.py) * sqrt(e)
    conf_repr = pre["beta_runtime"]["beta_float64"]       # valor de conferencia, LIDO do pre-registro congelado
    out["beta_repr"] = repr(beta)
    out["beta_repr_confere"] = (repr(beta) == conf_repr)
    # a receita da propria fractal_dephasing_principle: SEALED_CODATA_ALPHA * float(np.exp(ONE/(ONE+ONE)))
    ONE = 1.0
    beta_fd = (float(sealed_texto) if sealed_texto else float("nan")) * float(np.exp(ONE / (ONE + ONE)))
    out["beta_receita_fractal_dephasing_igual_bit_a_bit"] = (beta_fd == beta)
    out["exp_meio_igual_sqrt_e_float"] = (float(np.exp(0.5)) == math.sqrt(math.e))
    mp.mp.dps = MP_DPS
    alpha_mp = mp.mpf(alpha_texto)
    beta_mp = alpha_mp * mp.sqrt(mp.e)
    dif = abs(beta_mp - mp.mpf(beta))
    out["beta_mp_30"] = mp.nstr(beta_mp, 30)
    out["beta_mp_confere_pre_30dig"] = (mp.nstr(beta_mp, 30) == pre["beta_runtime"]["beta_mpmath_30dig"])
    out["abs_beta_mp_menos_beta"] = mp.nstr(dif, 10)
    out["beta_mp_dentro_1e-17"] = bool(dif <= mp.mpf(CONF_BETA_MP))
    thM = float(np.arcsin(np.sqrt(beta)))                 # theta_M = arcsin(sqrt(beta)) (receita do um.py l.6511)
    out["thetaM_repr"] = repr(thM)
    out["thetaM_repr_confere"] = (repr(thM) == pre["beta_runtime"]["theta_M"])
    thM_mp = mp.asin(mp.sqrt(beta_mp))
    # numero do operador (V4 l.16), lido dos BYTES do verbatim
    v4 = open(VERBATINS["V4"], "rb").read().decode("utf-8")
    mo = re.search(r"\\beta_\{TGL\} \\approx ([0-9]+\.[0-9]+)", v4)
    num_op_texto = mo.group(1) if mo else None
    out["numero_do_operador_V4_texto"] = num_op_texto
    out["numero_do_operador_V4_linha"] = (v4.count("\n", 0, mo.start()) + 1) if mo else None
    out["ok"] = bool(out["alpha_linha_confere"] and out["alpha_texto_confere_pre"] and out["beta_repr_confere"]
                     and out["beta_mp_dentro_1e-17"] and out["thetaM_repr_confere"] and num_op_texto is not None)
    return out, alpha_texto, beta, thM, beta_mp, thM_mp, num_op_texto


# ================================================================================================ main
def main():
    t0 = time.time()
    # fail-closed: operacao numpy que gere NaN/Inf (0/0, divisao por zero, overflow) PARA o ensaio visivelmente;
    # underflow (e^{-t g} abaixo do menor float) e legitimo e vira 0.
    np.seterr(divide="raise", invalid="raise", over="raise", under="ignore")
    os.makedirs(TENTATIVAS, exist_ok=True)
    log = Log(SAIDA_LOG)
    log("=" * 100)
    log("RUN_OPTICO F1.FREQUENCIA (trilha POSTO) -- rodada 2 do construtor otico -- inicio", agora_local(), "| UTC", agora_utc())
    log("ambiente: python", sys.version.split()[0], "| numpy", np.__version__, "| mpmath", mp.__version__, "|", platform.platform())

    # ------------------------------------------------------------------------------------------ 0. FREEZE
    fz = json.load(open(FREEZE, encoding="utf-8"))
    conf = dict(documento="CONFERENCIA_FREEZE -- rodada 2 do construtor otico (F1.FREQUENCIA, trilha POSTO)",
                quando_local=agora_local(), quando_utc=agora_utc(),
                FREEZE_json=dict(caminho=FREEZE, bytes=os.path.getsize(FREEZE), sha256=sha256_arquivo(FREEZE)),
                congelado_utc=fz.get("congelado_utc"), itens={})
    ok_fz = True
    for nome, p in (("PREREGISTRO.json", PRE_JSON), ("PREREGISTRO.md", PRE_MD)):
        b, h = os.path.getsize(p), sha256_arquivo(p)
        e = fz[nome]
        bate = (b == e["bytes"] and h == e["sha256"])
        conf["itens"][nome] = dict(bytes=b, sha256=h, congelado=e, bate=bate)
        ok_fz = ok_fz and bate
    demais = {}
    for rel, (b0, h0) in fz.get("demais_arquivos_da_pasta", {}).items():
        p = os.path.join(PRE_DIR, rel.replace("/", os.sep))
        demais[rel] = (dict(bate=(os.path.getsize(p) == b0 and sha256_arquivo(p) == h0)) if os.path.exists(p)
                       else dict(bate=False, ausente=True))
    conf["demais_arquivos_da_pasta"] = demais
    conf["demais_todos_batem"] = all(v["bate"] for v in demais.values())
    conhecidos = set(fz.get("demais_arquivos_da_pasta", {}).keys()) | {"PREREGISTRO.json", "PREREGISTRO.md", "FREEZE.json"}
    novos = []
    for dp, dns, fns in os.walk(PRE_DIR):
        for fn in fns:
            rel = os.path.relpath(os.path.join(dp, fn), PRE_DIR).replace("\\", "/")
            if rel not in conhecidos:
                novos.append(rel)
    conf["arquivos_novos_na_pasta_do_preregistro"] = sorted(novos)
    t_freeze = datetime.fromisoformat(fz["congelado_utc"])
    conf["freeze_anterior_a_este_ensaio"] = (t_freeze < datetime.now(timezone.utc))
    conf["veredito"] = "FREEZE_CONFERE" if ok_fz else "FREEZE_DIVERGENTE"
    escrever_json(CONF_FREEZE, conf)
    log("[0] FREEZE:", conf["veredito"], "| PREREGISTRO.json", conf["itens"]["PREREGISTRO.json"]["sha256"][:16],
        "| PREREGISTRO.md", conf["itens"]["PREREGISTRO.md"]["sha256"][:16], "| demais batem:", conf["demais_todos_batem"],
        "| novos:", conf["arquivos_novos_na_pasta_do_preregistro"])
    if not ok_fz:
        escrever_json(SAIDA_JSON, dict(documento="RESULTADO_OPTICO -- PARADO", veredito="PARADO_FREEZE_DIVERGENTE",
                                       divergencia=conf))
        log("PARADO: o FREEZE nao confere; nenhum teste rodado.")
        log.fechar()
        return 3
    pre = json.load(open(PRE_JSON, encoding="utf-8"))
    proto = pre["protocolo_otico"]

    # conferencia das tolerancias contra o texto congelado
    tol_conf = []
    for nome, val, chave in CONFERE_TEXTO:
        tol_conf.append(dict(nome=nome, valor=val, chave=chave, presente_no_texto_congelado=(val in proto[chave])))
    tol_ok = all(x["presente_no_texto_congelado"] for x in tol_conf)
    log("[0] tolerancias conferidas contra o texto congelado:", tol_ok)

    # ------------------------------------------------------------------------- impressao digital do kernel (inicio)
    imp_ini = impressao_digital_kernel()
    imp_pre = pre["impressao_digital_kernel_antes"]
    imp_ini["igual_ao_freeze"] = (imp_ini["sha256_metadados"] == imp_pre[0] and imp_ini["sha256_conteudo_lean"] == imp_pre[1])
    log("[0] impressao digital do tgl_kernel (inicio):", imp_ini["sha256_metadados"][:16], imp_ini["sha256_conteudo_lean"][:16],
        "| n =", imp_ini["n_arquivos"], "| igual ao FREEZE:", imp_ini["igual_ao_freeze"])

    # ------------------------------------------------------------------------------------------------ 1. pinos
    pinos = []
    for caminho, b0, h0 in pre["pinos"]:
        d = dict(caminho=caminho, bytes_congelado=b0, sha_congelado=h0)
        if not os.path.exists(caminho):
            d.update(existe=False, bate=False)
        else:
            b = os.path.getsize(caminho)
            h = sha256_arquivo(caminho)
            d.update(existe=True, bytes=b, sha256=h, bate=(b == b0 and h.startswith(h0)))
            if not d["bate"] and b > b0:
                hp = sha256_arquivo(caminho, limite=b0)
                d["prefixo_congelado_intacto"] = hp.startswith(h0)
                d["leitura"] = ("cresceu so por acrescimo (livro so-acrescimo)" if d["prefixo_congelado_intacto"]
                                else "MUDOU (prefixo nao confere)")
        pinos.append(d)
    pinos_kernel = []
    for item in pre["pinos_kernel_sha16"]:
        rel, h0 = item.rsplit(" ", 1)
        p = os.path.join(KERNEL, rel.replace("/", os.sep))
        h = sha256_arquivo(p) if os.path.exists(p) else None
        pinos_kernel.append(dict(arquivo=rel, sha16_congelado=h0, sha16=(h[:16] if h else None), bate=bool(h and h.startswith(h0))))
    verb = {}
    for k, p in VERBATINS.items():
        raw = open(p, "rb").read()
        e = pre["a_verbatins"][k]
        verb[k] = dict(arquivo=p, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), bytes_pre=e["bytes"],
                       sha256_pre=e["sha256"], bate=(len(raw) == e["bytes"] and hashlib.sha256(raw).hexdigest() == e["sha256"]),
                       crlf=raw.count(b"\r"))
    raw2 = open(VERBATINS["V2"], "rb").read()
    trilha = b"".join(raw2.splitlines(keepends=True)[:32])   # «l.1-33»: os bytes ate o fim da l.32 (a l.33 e vazia)
    e2 = pre["a_verbatins"]["V2"]["trilha"]
    verb["V2_trilha"] = dict(recorte="splitlines(keepends)[:32] (a l.33 e vazia)", bytes=len(trilha),
                             sha256=hashlib.sha256(trilha).hexdigest(), bytes_pre=e2["bytes"], sha256_pre=e2["sha256"],
                             bate=(len(trilha) == e2["bytes"] and hashlib.sha256(trilha).hexdigest() == e2["sha256"]))
    um_ok = any(d["bate"] for d in pinos if d["caminho"].endswith("um.py"))
    verb_ok = all(v["bate"] for v in verb.values())
    log("[1] pinos: um.py bate:", um_ok, "| verbatins batem:", verb_ok, "| kernel (sha16) batem:",
        all(x["bate"] for x in pinos_kernel), "| demais:", [(os.path.basename(d["caminho"]), d["bate"], d.get("leitura", "")) for d in pinos if not d["bate"]])

    # ------------------------------------------------------------------------------------------------ 2. beta
    braw = ler_beta(pre, log)
    if not isinstance(braw, tuple):
        beta_info = braw
        beta_ok = False
        alpha_texto = beta = thM = beta_mp = thM_mp = num_op_texto = None
    else:
        beta_info, alpha_texto, beta, thM, beta_mp, thM_mp, num_op_texto = braw
        beta_ok = beta_info["ok"]
    beta_conferido = bool(beta_ok and um_ok and verb_ok and tol_ok)
    log("[2] beta de runtime: alpha", beta_info.get("alpha_texto"), "(l.%s)" % beta_info.get("alpha_linha"),
        "| repr(beta) confere:", beta_info.get("beta_repr_confere"), "| |beta_mp - beta| =", beta_info.get("abs_beta_mp_menos_beta"),
        "| thetaM confere:", beta_info.get("thetaM_repr_confere"), "| numero do operador (V4 l.%s):" % beta_info.get("numero_do_operador_V4_linha"),
        num_op_texto, "| BETA CONFERIDO:", beta_conferido)
    if not beta_conferido:
        log("FAIL-CLOSED: alpha ilegivel ou beta sem conferencia -> SEM_VEREDITO_O visivel em todas as partes; nenhum teste rodado")
        escrever_json(SAIDA_JSON, dict(documento="RESULTADO_OPTICO -- SEM_VEREDITO_O (fail-closed)",
                                       veredito="SEM_VEREDITO_O__BETA_SEM_CONFERENCIA", beta_runtime=beta_info, freeze=conf,
                                       tolerancias_conferidas=dict(ok=tol_ok, itens=tol_conf),
                                       pinos=dict(pinos=pinos, kernel=pinos_kernel, verbatins=verb)))
        log.fechar()
        return 4

    # ------------------------------------------------------------------------------------- o ensaio, parte a parte
    E = Ensaio(log, pre)
    E.decisoes += [
        "[INPUT do construtor] ordem de sorteio fixada antes de rodar, num unico default_rng(20261012): (1) Haar QR n=2/3/4: "
        "1000/200/200; (2) mistos por (n, posto) n=2..4, posto 2..n, 100 cada (cada um com seu Haar e seu p); (3) 1000 M 2x2 "
        "gaussianas complexas (Re, Im ~ N(0,1)); (4) 100 psi por n em {2,3,4} (gaussianas complexas); (5) projecoes n=4, "
        "posto d em {1..4}, 50 POR d (V = primeiras d colunas de um Haar); (6) so depois, as amostras dos anexos.",
        "[INPUT do construtor] Haar por QR com correcao de fase: Z = (N + iN)/sqrt(2); Q, R = qr(Z); U = Q diag(r_ii/|r_ii|).",
        "[INPUT do construtor] estados puros de P1.a: rho = u e0 e0^H u^H para cada Haar (1400); mistos: os 600 de (2).",
        "[INPUT do construtor] a perna 'rho^2 = rho' de P1.a usa o TOL_ZERO pre-registrado em |rho^2 - rho|_F (a coluna de "
        "tolerancia de P1.a cita PUREZA e RANK; o criterio de 'matriz nula' do protocolo e o TOL_ZERO).",
        "[INPUT do construtor] P1.b, implicacao: de cada M gaussiana, M' = [[a, b], [c, 1-a]] com c = (1 - a^2 - (1-a)^2)/(2b) "
        "(so traco: Tr M' = 1 e Tr M'^2 = 1, sem usar det); mais rho* e F_th(1) para th em G_th.",
        "[INPUT do construtor] P3.a: PRODUTO COMPLETO por n -- todo P em {rho*, Q0 (n = 2)} U {|psi_j><psi_j|, j = 0..99} contra "
        "todo rho em {I/n} U mistos(n) (60502 pares). As tentativas 1-3 desta rodada pareavam por indice (805 pares) e passaram; "
        "a tentativa 4 adota o produto completo, que e a leitura mais fiel e mais exigente do 'P em {...}, rho em {...}'.",
        "[INPUT do construtor] TOL_ID em matrizes = maximo entrada a entrada |x_ij - y_ij| (a rodada 1 usou a norma de "
        "Frobenius). [DERIVED] como |X|_F <= n max|x_ij| e n <= 4, a leitura de Frobenius muda um residuo no maximo por 4; os "
        "maximos medidos (log) ficam ordens abaixo de 1e-12, salvo B7.a1, cujo residuo e comparado com 1e-12 n.",
        "[INPUT do construtor] B4.a: cada Haar u de n=2 age em rho*, Q0, um misto e um puro (indice mod 100); n=3 em E00, "
        "um misto, um puro; n=4 em E00, um misto, um puro e uma projecao de P4 (indice ciclico).",
        "[INPUT do construtor] 'D atua' (objetos): existe t em G_t \\ {0} com |D_t F - F|_F >= 1e-6, para cada gamma em "
        "{1, beta}; 'nao atua': <= 1e-12 para todo t; entre: AMBIGUO (fail-closed).",
        "[INPUT do construtor] B5.b: grade de b = {0, 1e-5, 1e-3, beta, 0.1, 0.25, 0.5, 0.75, 0.9, 1-beta, 1-1e-3, 1-1e-5, 1} "
        "(b em (0, 1e-6) fica abaixo da resolucao do criterio RANK: a face K decide ali).",
        "[INPUT do construtor] TOL_ID n (B7.a1) = 1e-12 * n.",
        "[INPUT do construtor] OSC (B7.a2): n = 0..99999, janelas de W termos com inicio k = 0..1e5 - W (sliding window).",
    ]

    # ------------------------------------------------------------------------------------------- grades e amostras
    PI = math.pi
    G_TH = []
    if beta_conferido:
        G_TH = [("0", 0.0), ("thM", thM), ("-thM", -thM), ("3thM", 3 * thM), ("pi/6", PI / 6), ("pi/4", PI / 4),
                ("pi/3", PI / 3), ("pi/2", PI / 2), ("2pi/3", 2 * PI / 3), ("pi", PI), ("1.0", 1.0), ("2.5", 2.5)]
    G_T = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0]
    G_T_POS = [t for t in G_T if t > 0]
    GAMMAS = [("1", 1.0), ("beta", beta)] if beta_conferido else [("1", 1.0)]
    log("[3] G_th =", [l for l, _ in G_TH], "| G_t =", G_T, "| gamma em", [l for l, _ in GAMMAS])

    rng = np.random.default_rng(SEMENTE)

    def haar(n):
        Z = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) / math.sqrt(2.0)
        Q, R = np.linalg.qr(Z)
        d = np.diag(R)
        return Q * (d / np.abs(d))

    HAAR = {2: [haar(2) for _ in range(1000)], 3: [haar(3) for _ in range(200)], 4: [haar(4) for _ in range(200)]}
    MISTOS = {}
    for n in (2, 3, 4):
        for r in range(2, n + 1):
            lst = []
            for _ in range(100):
                U = haar(n)
                p = rng.uniform(0.05, 1.0, size=r)
                p = p / p.sum()
                Dg = np.zeros((n, n), dtype=complex)
                Dg[np.arange(r), np.arange(r)] = p
                lst.append(U @ Dg @ U.conj().T)
            MISTOS[(n, r)] = lst
    MS = [rng.standard_normal((2, 2)) + 1j * rng.standard_normal((2, 2)) for _ in range(1000)]
    PSIS = {}
    for n in (2, 3, 4):
        PSIS[n] = [rng.standard_normal(n) + 1j * rng.standard_normal(n) for _ in range(100)]
    PROJ = {}
    for d in (1, 2, 3, 4):
        lst = []
        for _ in range(50):
            U = haar(4)
            V = U[:, :d]
            lst.append(V @ V.conj().T)
        PROJ[d] = lst
    PSIH = {n: [v / np.linalg.norm(v) for v in PSIS[n]] for n in (2, 3, 4)}
    log("[3] amostras: Haar", {n: len(v) for n, v in HAAR.items()}, "| mistos", {"%d,%d" % k: len(v) for k, v in MISTOS.items()},
        "| M", len(MS), "| psi", {n: len(v) for n, v in PSIS.items()}, "| projecoes", {d: len(v) for d, v in PROJ.items()})

    def estado_info(rho):
        n = rho.shape[0]
        ev = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
        tr = complex(np.trace(rho))
        pur = float(np.real(np.trace(rho @ rho)))
        idem = frob(rho @ rho - rho)
        pk = posto(rho)
        return dict(n=n, herm=maxabs(rho - rho.conj().T), min_ev=float(ev.min()), tr_desvio=abs(tr - 1.0), pureza=pur,
                    cls_pur=cls_pureza(pur), idem=idem, cls_idem=cls_zero(idem), posto=pk["posto"], nulidade=pk["nulidade"],
                    ambiguos=pk["ambiguos"], sigmas=pk["sigmas"], finito=finito(rho))

    # ============================================================================================== P1
    log("-" * 100)
    log("[P1] estado puro <=> posto 1  [KNOWN Nielsen & Chuang Ex. 2.71; o PASSA_O e da sombra numerica]")
    p = E.P("P1.a")
    estados = []
    for n in (2, 3, 4):
        for k, U in enumerate(HAAR[n]):
            psi = U[:, 0]
            estados.append((np.outer(psi, psi.conj()), "puro", n, "haar%d[%d]e0" % (n, k)))
    for (n, r), lst in MISTOS.items():
        for k, rho in enumerate(lst):
            estados.append((rho, "misto", n, "misto%d_%d[%d]" % (n, r, k)))
    infos = [estado_info(st[0]) for st in estados]
    hip_herm = max(i["herm"] for i in infos)
    hip_psd = min(i["min_ev"] for i in infos)
    hip_tr = max(i["tr_desvio"] for i in infos)
    p.check("hipoteses habitadas em todas as amostras: rho hermitiana, PSD (autovalor >= -1e-12), Tr rho = 1 (TOL_ID)",
            hip_herm <= TOL_ID and hip_psd >= -TOL_ID and hip_tr <= TOL_ID and all(i["finito"] for i in infos),
            max_desvio_hermitiano=hip_herm, min_autovalor=hip_psd, max_desvio_traco=hip_tr, n=len(infos))
    amb = [st[3] for st, i in zip(estados, infos) if i["cls_pur"] not in ("=1", "<1") or i["posto"] is None
           or i["cls_idem"] not in ("ZERO", "NAO_ZERO")]
    p.check("nenhuma classificacao AMBIGUO/NaN (PUREZA, RANK, TOL_ZERO em rho^2 - rho)", None if amb else True,
            n_ambiguos=len(amb), exemplos=amb[:10])
    viol, lados = [], dict(puro_tudo_verdadeiro=0, misto_tudo_falso=0, outros=0)
    for st, i in zip(estados, infos):
        a, b, c = (i["cls_pur"] == "=1"), (i["posto"] == 1), (i["cls_idem"] == "ZERO")
        if not (a == b == c):
            viol.append(st[3])
        if st[1] == "puro" and a and b and c:
            lados["puro_tudo_verdadeiro"] += 1
        elif st[1] == "misto" and not a and not b and not c:
            lados["misto_tudo_falso"] += 1
        else:
            lados["outros"] += 1
    pur_puros = [abs(i["pureza"] - 1) for st, i in zip(estados, infos) if st[1] == "puro"]
    pur_mistos = [i["pureza"] for st, i in zip(estados, infos) if st[1] == "misto"]
    s2_puros = [i["sigmas"][1] for st, i in zip(estados, infos) if st[1] == "puro"]
    smin_mistos = [i["sigmas"][i["posto"] - 1] for st, i in zip(estados, infos) if st[1] == "misto" and i["posto"]]
    p.check("Tr rho^2 = 1 <=> posto 1 <=> rho^2 = rho: as tres classificacoes concordam em toda amostra", not viol,
            n_violacoes=len(viol), exemplos=viol[:10])
    p.check("os dois lados realizados: puros com as tres verdadeiras; mistos com as tres falsas",
            lados["puro_tudo_verdadeiro"] == 1400 and lados["misto_tudo_falso"] == 600 and lados["outros"] == 0, **lados)
    p.extra = dict(max_abs_pureza_menos_1_puros=max(pur_puros), max_pureza_mistos=max(pur_mistos),
                   max_sigma2_puros=max(s2_puros), min_menor_sigma_nao_nulo_mistos=min(smin_mistos))
    E.ESTADOS_P1 = list(zip(estados, infos))
    log("  P1.a:", p.face_O(), "| n =", len(infos), "| violacoes:", len(viol), "| max|pureza-1| puros = %.2e" % max(pur_puros),
        "| max pureza mistos = %.6f" % max(pur_mistos), "| max sigma2 puros = %.2e" % max(s2_puros),
        "| min sigma nao nulo mistos = %.4f" % min(smin_mistos))

    # C1, C2
    c = E.C("C1")
    R1 = np.diag([2 / 3, 2 / 3, -1 / 3]).astype(complex)
    i1 = estado_info(R1)
    c.fechar(abs(complex(np.trace(R1)) - 1) <= TOL_ID and i1["cls_pur"] == "=1" and i1["posto"] == 3 and i1["min_ev"] < 0,
             "sem PSD: Tr 1 e Tr rho^2 = 1 mas posto 3 -- 'pureza => posto 1' cai sem a positividade",
             traco=complex(np.trace(R1)), pureza=i1["pureza"], posto=i1["posto"], min_autovalor=i1["min_ev"])
    c = E.C("C2")
    R2 = E00 / 2
    i2 = estado_info(R2)
    c.fechar(i2["posto"] == 1 and abs(i2["pureza"] - 0.25) <= TOL_ID and i2["min_ev"] >= -TOL_ID and abs(complex(np.trace(R2)) - 0.5) <= TOL_ID,
             "sem Tr 1: PSD e posto 1 mas Tr rho^2 = 1/4 -- 'posto 1 => pureza 1' cai sem a normalizacao",
             traco=complex(np.trace(R2)), pureza=i2["pureza"], posto=i2["posto"])

    # P1.b
    p = E.P("P1.b")
    rid, razoes = [], []
    for M in MS:
        tr, tr2, de, nf2 = np.trace(M), np.trace(M @ M), det2(M), frob(M) ** 2
        r = abs(tr2 - (tr * tr - 2 * de))
        rid.append(r)
        razoes.append(r / (TOL_ID * (1 + nf2)))
    p.check("Tr M^2 = (Tr M)^2 - 2 det M nas 1000 M gaussianas complexas (TOL_ID (1 + |M|_F^2))",
            finito(rid) and max(razoes) <= 1.0, max_residuo=max(rid), max_residuo_sobre_tolerancia=max(razoes), n=len(MS))
    Ml = []
    for k, M in enumerate(MS):
        a, b = M[0, 0], M[0, 1]
        d = 1 - a
        cc = (1 - a * a - d * d) / (2 * b)
        Ml.append(("gauss[%d]" % k, np.array([[a, b], [cc, d]], dtype=complex)))
    Ml.append(("rho*", E00.copy()))
    for lab, th in G_TH:
        Ml.append(("F_%s(1)" % lab, rho_out(th)))
    hip_r, det_r, nao_herm, falhas, ambs = [], [], 0, [], []
    for lab, Mp in Ml:
        tol = TOL_ID * (1 + frob(Mp) ** 2)
        h1, h2 = abs(np.trace(Mp) - 1), abs(np.trace(Mp @ Mp) - 1)
        hip_r.append(max(h1, h2) / tol)
        dd = abs(det2(Mp))
        det_r.append(dd / tol)
        pk = posto(Mp)
        if pk["posto"] is None:
            ambs.append(lab)
        if not (max(h1, h2) <= tol and dd <= tol and pk["posto"] == 1):
            falhas.append(lab)
        if maxabs(Mp - Mp.conj().T) >= 1e-6:
            nao_herm += 1
    p.check("hipotese habitada: Tr M' = Tr M'^2 = 1 (TOL_ID (1 + |M'|_F^2)) nas %d matrizes" % len(Ml), max(hip_r) <= 1.0,
            max_desvio_sobre_tolerancia=max(hip_r))
    p.check("sem AMBIGUO no posto", None if ambs else True, ambiguos=ambs[:10])
    p.check("Tr M = Tr M^2 = 1 => det M = 0 e posto M = 1, sem positividade", not falhas, n=len(Ml), n_falhas=len(falhas),
            exemplos=falhas[:10], max_det_sobre_tolerancia=max(det_r), n_nao_hermitianas=nao_herm)
    log("  P1.b:", p.face_O(), "| identidade max = %.2e (razao %.2e)" % (max(rid), max(razoes)), "| implicacao em", len(Ml),
        "matrizes (nao hermitianas: %d), max|det|/tol = %.2e" % (nao_herm, max(det_r)))

    # P1.d
    p = E.P("P1.d")
    nz, r1, trd, idd, purd, amb = [], [], [], [], [], []
    for n in (2, 3, 4):
        for k, psi in enumerate(PSIS[n]):
            nz.append(cls_zero(np.linalg.norm(psi)) == "NAO_ZERO")
            pk = posto(np.outer(psi, psi.conj()))
            if pk["posto"] is None:
                amb.append("psi%d[%d]" % (n, k))
            r1.append(pk["posto"] == 1)
            ph = PSIH[n][k]
            rho = np.outer(ph, ph.conj())
            trd.append(abs(np.trace(rho) - 1))
            idd.append(maxabs(rho @ rho - rho))
            purd.append(abs(np.real(np.trace(rho @ rho)) - 1))
    p.check("psi != 0 em todas (TOL_ZERO)", all(nz), n=len(nz))
    p.check("sem AMBIGUO", None if amb else True, ambiguos=amb[:10])
    p.check("psi != 0 => posto |psi><psi| = 1 (RANK)", all(r1), n=len(r1))
    p.check("|psi| = 1 => Tr = 1, idempotente, Tr(rho^2) = 1 (TOL_ID)", max(trd) <= TOL_ID and max(idd) <= TOL_ID and max(purd) <= TOL_ID,
            max_desvio_traco=max(trd), max_desvio_idempotencia=max(idd), max_desvio_pureza=max(purd))
    log("  P1.d:", p.face_O(), "| n =", len(r1), "| max desvios: traco %.1e, idem %.1e, pureza %.1e" % (max(trd), max(idd), max(purd)))

    # ============================================================================================== P2
    log("-" * 100)
    log("[P2] posto-nulidade  [P2.lit KNOWN por citacao: Mathlib LinearMap.finrank_range_add_finrank_ker; Axler LADR Teo. 3.22]")
    p = E.P("P2.a")

    def posto_nulidade_verificado(A):
        U, s, Vh = np.linalg.svd(A)
        nn = s >= RANK_NAONULO
        nu = s <= RANK_NULO
        amb = int(np.sum(~(nn | nu)))
        nucleo = [Vh[i].conj() for i in range(len(s)) if nu[i]]
        imagem = [U[:, i] for i in range(len(s)) if nn[i]]
        res_nucleo = max([float(np.linalg.norm(A @ v)) for v in nucleo] or [0.0])
        return dict(posto=int(np.sum(nn)) if not amb else None, nulidade=int(np.sum(nu)) if not amb else None,
                    ambiguos=amb, max_residuo_A_v_nucleo=res_nucleo, base_imagem=[jsonable(v) for v in imagem])

    casos = [("rho*", E00, (1, 1)), ("I/2", I2 / 2, (2, 0)), ("0", np.zeros((2, 2), dtype=complex), (0, 2))]
    obs_p2 = []
    for lab, A, esp in casos:
        r = posto_nulidade_verificado(A)
        p.check("(posto, nulidade) de %s = %s, com o nucleo conferido (|A v| <= 1e-12)" % (lab, esp),
                None if r["ambiguos"] else ((r["posto"], r["nulidade"]) == esp and r["max_residuo_A_v_nucleo"] <= TOL_ID
                                            and r["posto"] + r["nulidade"] == 2),
                posto=r["posto"], nulidade=r["nulidade"], residuo_nucleo=r["max_residuo_A_v_nucleo"])
        obs_p2.append((lab, r["posto"], r["nulidade"]))
    log("  P2.a:", p.face_O(), "| (rotulo, posto, nulidade):", obs_p2)
    p = E.P("P2.b")
    viol1, viol2, n1 = [], [], 0
    for (st, i) in E.ESTADOS_P1:
        n = st[2]
        if i["posto"] is None or i["posto"] < 1:
            viol1.append(st[3])
        if (i["posto"] == 1) != (i["nulidade"] == n - 1):
            viol2.append(st[3])
        n1 += (i["posto"] == 1)
    p.check("Tr rho = 1 => posto rho >= 1 (amostras de P1)", not viol1, n=len(E.ESTADOS_P1), violacoes=viol1[:10])
    p.check("posto rho = 1 <=> nulidade = n - 1 (os dois lados: %d com posto 1, %d sem)" % (n1, len(E.ESTADOS_P1) - n1),
            (not viol2) and 0 < n1 < len(E.ESTADOS_P1), violacoes=viol2[:10])
    log("  P2.b:", p.face_O(), "| n =", len(E.ESTADOS_P1), "| posto 1:", n1)

    # ============================================================================================== P3
    log("-" * 100)
    log("[P3] a leitura (o colapso) como projecao de posto 1  [Luders KNOWN; forma geral nova]")
    p = E.P("P3.a")
    pares = []
    e0 = np.array([1, 0], dtype=complex)
    e1 = np.array([0, 1], dtype=complex)
    for n in (2, 3, 4):
        Xs = [("I/%d" % n, np.eye(n, dtype=complex) / n)]
        for r in range(2, n + 1):
            Xs += [("misto%d_%d[%d]" % (n, r, k), X) for k, X in enumerate(MISTOS[(n, r)])]
        As = [("psi%d[%d]" % (n, j), PSIH[n][j]) for j in range(100)]
        if n == 2:
            As = [("rho*", e0), ("Q0", e1)] + As
        for al, a in As:                      # produto completo P x rho (tentativa 4; ver TENTATIVAS_RODADA2.json)
            for xl, X in Xs:
                pares.append((al, a, xl, X))
    r_comp, r_tr, r_div, wmin, amb, ndiv = [], [], [], [], [], 0
    for al, a, xl, X in pares:
        Pm = np.outer(a, a.conj())
        w = complex(a.conj() @ X @ a)
        PXP = Pm @ X @ Pm
        r_comp.append(maxabs(PXP - w * Pm))
        r_tr.append(abs(np.trace(Pm @ X) - w))
        cz = cls_zero(abs(w))
        wmin.append(abs(w))
        if cz == "NAO_ZERO":
            r_div.append(maxabs(PXP / w - Pm))
            ndiv += 1
        elif cz != "ZERO":
            amb.append((al, xl))
    p.check("<a,a> = 1 (as projecoes sao de posto 1)", max(abs(np.linalg.norm(x[1]) - 1) for x in pares) <= TOL_ID)
    p.check("P X P = <a,Xa> P (TOL_ID) em %d pares" % len(pares), max(r_comp) <= TOL_ID, max_residuo=max(r_comp))
    p.check("Tr(P X) = <a,Xa> (TOL_ID)", max(r_tr) <= TOL_ID, max_residuo=max(r_tr))
    p.check("sem <a,Xa> AMBIGUO", None if amb else True, ambiguos=amb[:10])
    p.check("<a,Xa> != 0 => P X P / <a,Xa> = P (TOL_ID) em %d pares" % ndiv, ndiv > 0 and max(r_div) <= TOL_ID,
            max_residuo=max(r_div) if r_div else None, min_abs_w=min(wmin))
    log("  P3.a:", p.face_O(), "| pares", len(pares), "| max res: PXP %.1e, Tr %.1e, divisao %.1e | min|<a,Xa>| = %.3e"
        % (max(r_comp), max(r_tr), max(r_div), min(wmin)))
    c = E.C("C4")
    w = complex(e0.conj() @ (I2 - E00) @ e0)
    PXP = E00 @ (I2 - E00) @ E00
    c.fechar(cls_zero(abs(w)) == "ZERO" and cls_zero(frob(PXP)) == "ZERO" and frob(PXP - E00) >= NAOZERO_MIN,
             "sem peso: Tr(P rho) = 0 e P rho P = 0 -- a leitura nao devolve P (nada a normalizar)",
             peso=w, norma_PXP=frob(PXP), dist_PXP_a_P=frob(PXP - E00))
    c = E.C("C5")
    X = I2 / 2
    out = (I2 @ X @ I2) / np.trace(I2 @ X)
    pk = posto(out)
    c.fechar(pk["posto"] == 2, "P = 1 (posto 2): a saida P X P / Tr(P X) = I/2 tem posto 2 -- a leitura precisa de P de posto 1",
             posto_saida=pk["posto"], sigmas=pk["sigmas"])

    p = E.P("P3.b")
    if beta_conferido:
        X = I2 / 2
        lido = E00 @ X @ E00 / np.trace(E00 @ X)
        rb = np.diag([1 - beta, beta]).astype(complex)
        Sm = S(thM)
        t2 = abs((Sm @ e0)[0]) ** 2
        r2 = abs((Sm @ e0)[1]) ** 2
        Q0c = I2 - E00
        p.check("rho* (I/2) rho* / Tr(rho* I/2) = rho*, Tr(rho* I/2) = 1/2 (TOL_ID)",
                maxabs(lido - E00) <= TOL_ID and abs(np.trace(E00 @ X) - 0.5) <= TOL_ID,
                residuo=maxabs(lido - E00), traco=complex(np.trace(E00 @ X)))
        p.check("rho = diag(1-b, b), b = beta: Tr(rho* rho) = 1 - b = |t|^2 e Tr(Q0 rho) = b = |r|^2 (float64, TOL_ID)",
                abs(np.trace(E00 @ rb) - (1 - beta)) <= TOL_ID and abs(np.trace(E00 @ rb) - t2) <= TOL_ID
                and abs(np.trace(Q0c @ rb) - beta) <= TOL_ID and abs(np.trace(Q0c @ rb) - r2) <= TOL_ID,
                res_t=abs(np.trace(E00 @ rb) - t2), res_r=abs(np.trace(Q0c @ rb) - r2))
        c_mp, s_mp = mp.cos(thM_mp), mp.sin(thM_mp)
        rho_mp = mp.diag([1 - beta_mp, beta_mp])
        P_mp = mp.matrix([[1, 0], [0, 0]])
        Q0_mp = mp.eye(2) - P_mp
        tP = (P_mp * rho_mp)[0, 0] + (P_mp * rho_mp)[1, 1]
        tQ = (Q0_mp * rho_mp)[0, 0] + (Q0_mp * rho_mp)[1, 1]
        rt, rr = abs(tP - c_mp ** 2), abs(tQ - s_mp ** 2)
        p.check("idem em mpmath dps 50 (TOL_ID 1e-40)", rt <= TOL_ID_MP and rr <= TOL_ID_MP, res_t=rt, res_r=rr)
    else:
        p.check("beta sem conferencia: SEM_VEREDITO", None)
    log("  P3.b:", p.face_O())

    # ============================================================================================== P4
    log("-" * 100)
    log("[P4] o nome e o indice na densidade  [DERIVED]")
    p = E.P("P4")
    res = dict(idem=0.0, herm=0.0, tr=0.0, trrho=0.0, pur=0.0)
    viol, amb, distinto = [], [], []
    for d, lst in PROJ.items():
        for k, Pm in enumerate(lst):
            pk = posto(Pm)
            if pk["posto"] is None:
                amb.append("P%d[%d]" % (d, k))
                continue
            rho = Pm / d
            res["idem"] = max(res["idem"], maxabs(Pm @ Pm - Pm))
            res["herm"] = max(res["herm"], maxabs(Pm - Pm.conj().T))
            res["tr"] = max(res["tr"], abs(np.trace(Pm) - d))
            res["trrho"] = max(res["trrho"], abs(np.trace(rho) - 1))
            pr = float(np.real(np.trace(rho @ rho)))
            res["pur"] = max(res["pur"], abs(pr - 1.0 / d))
            igual = abs(pr - float(np.real(np.trace(rho)))) <= TOL_ID
            if pk["posto"] != d:
                viol.append("P%d[%d] posto %s" % (d, k, pk["posto"]))
            if igual != (d == 1):
                viol.append("P%d[%d] Tr rho^2 = Tr rho com d = %d" % (d, k, d))
            distinto.append((d, pr))
    p.check("sem AMBIGUO", None if amb else True, ambiguos=amb[:10])
    p.check("P^2 = P = P^H e posto P = d (n = 4, d em {1..4}, 50 por d)", res["idem"] <= TOL_ID and res["herm"] <= TOL_ID and
            not [v for v in viol if "posto" in v], max_idem=res["idem"], max_herm=res["herm"])
    p.check("Tr P = d; Tr rho = 1 (nome); Tr rho^2 = 1/d (indice) (TOL_ID)", res["tr"] <= TOL_ID and res["trrho"] <= TOL_ID and res["pur"] <= TOL_ID,
            max_tr=res["tr"], max_trrho=res["trrho"], max_pureza_menos_1_sobre_d=res["pur"])
    p.check("Tr rho^2 = Tr rho <=> d = 1 (os dois lados: d = 1 e d >= 2)", not [v for v in viol if "Tr" in v],
            violacoes=viol[:10])
    log("  P4:", p.face_O(), "| max res: idem %.1e herm %.1e TrP %.1e Trrho %.1e pureza %.1e" % (res["idem"], res["herm"], res["tr"], res["trrho"], res["pur"]))
    c = E.C("C3")
    pk = posto(I2 / 2)
    trPF = None
    try:
        core = json.load(open(CORE, encoding="utf-8"))
        trPF = core["core"]["certificate_II"]["H1_finite_face"]["trace_PF"]
        E.core_fd = core["core"].get("fractal_dephasing")
    except Exception as ex:  # citacao: falha visivel, nao muda o controle
        E.core_fd = None
        E.alertas.append("leitura do core falhou: %r" % (ex,))
    c.fechar(abs(np.trace(I2 / 2) - 1) <= TOL_ID and pk["posto"] == 2,
             "Tr 1 nao e posto 1: I/2 tem traco 1 e posto 2 (citado do core v391: tr P_F = %r, nao 1)" % (trPF,),
             traco=complex(np.trace(I2 / 2)), posto=pk["posto"], citado_trace_PF_core=trPF)

    # ============================================================================================== B1
    log("-" * 100)
    log("[B1] a unidade: Tr rho* = posto rho* = 1 (POSTO = RANK)  [REAL runtime; posicao <-> posto ONTO]")
    U0 = umpy_objetos(0.0)
    Pst = U0["P"]
    p = E.P("B1.a")
    pk = posto(Pst)
    p.check("Tr rho* = 1 (receita do um.py: omega_I = trace(P))", abs(U0["omega_I"] - 1.0) <= TOL_ID, omega_I=U0["omega_I"])
    p.check("posto rho* = 1 (RANK)", pk["posto"] == 1, sigmas=pk["sigmas"])
    p.check("rho*^2 = rho* = rho*^H (TOL_ID)", maxabs(Pst @ Pst - Pst) <= TOL_ID and maxabs(Pst - Pst.T) <= TOL_ID)
    if E.core_fd is not None:
        p.check("o core do um.py v391 diz o mesmo: fractal_dephasing.omega_I = 1.0 (citado, lido do um_absoluto.json)",
                E.core_fd.get("omega_I") == U0["omega_I"], core_omega_I=E.core_fd.get("omega_I"))
    log("  B1.a:", p.face_O())
    p = E.P("B1.b")
    rr = []
    for d, lst in PROJ.items():
        for Pm in lst:
            pk = posto(Pm)
            rr.append(abs(complex(np.trace(Pm)) - (pk["posto"] if pk["posto"] is not None else float("nan"))))
    for Pm in (E00, I2 - E00, I2, np.zeros((2, 2), dtype=complex)):
        pk = posto(Pm)
        rr.append(abs(complex(np.trace(Pm)) - pk["posto"]))
    p.check("P^2 = P => Tr P = posto P (as 200 projecoes de P4 + rho*, Q0, 1, 0)", finito(rr) and max(rr) <= TOL_ID, max_residuo=max(rr), n=len(rr))
    log("  B1.b:", p.face_O(), "| max |Tr P - posto P| = %.1e" % max(rr))
    p = E.P("B1.c")
    Uu, ss, Vh = np.linalg.svd(Pst)
    u0 = Uu[:, 0]
    p.check("vetor singular de sigma = 1 e +-e0: |<e0,u0>| = 1, |<e1,u0>| = 0 (TOL_ID)", abs(abs(u0[0]) - 1) <= TOL_ID and abs(u0[1]) <= TOL_ID,
            u0=u0, sigmas=ss)
    p.check("rho* e0 = e0 e rho* e1 = 0: imagem = span{e0}, nucleo = span{e1}", maxabs(Pst @ np.array([1.0, 0.0]) - np.array([1.0, 0.0])) <= TOL_ID
            and maxabs(Pst @ np.array([0.0, 1.0])) <= TOL_ID)
    p.check("posto rho* = dim span{e0} = 1", posto(Pst)["posto"] == 1 and posto(np.array([[1.0], [0.0]]))["posto"] == 1)
    log("  B1.c:", p.face_O())

    # ============================================================================================== B2
    log("-" * 100)
    log("[B2] o anticomutador {Q_th, rho*}  [REAL runtime so em th = 0; em thM so docstring DECLARADO]")
    p = E.P("B2.a")
    linhas_b2 = []
    for lab, th in G_TH:
        Uo = umpy_objetos(th)
        s_, c_ = Uo["s"], Uo["c"]
        Qf = np.array([[s_ * s_, -s_ * c_], [-s_ * c_, c_ * c_]])
        A = anticomm(Uo["Qth"], Uo["P"])
        Af = np.array([[2 * s_ * s_, -s_ * c_], [-s_ * c_, 0.0]])
        nA = frob(A)
        linha = dict(th=lab, res_Q=maxabs(Uo["Qth"] - Qf), res_anti=maxabs(A - Af), traco=float(np.trace(A)),
                     res_traco=abs(np.trace(A) - 2 * s_ * s_), soma_quad=float(np.sum(np.abs(A) ** 2)),
                     res_soma=abs(np.sum(np.abs(A) ** 2) - 2 * s_ * s_ * (1 + s_ * s_)), norma=nA, cls_anti=cls_zero(nA),
                     sin_th=s_, cls_sin=cls_zero(abs(s_)))
        linhas_b2.append(linha)
    p.check("Q_th (receita do um.py R Q0 R^T) = [[s^2,-sc],[-sc,c^2]] (TOL_ID) em G_th", max(l["res_Q"] for l in linhas_b2) <= TOL_ID,
            max_residuo=max(l["res_Q"] for l in linhas_b2))
    p.check("{Q_th, rho*} = [[2s^2,-sc],[-sc,0]]; Tr = 2s^2; soma |.|^2 = 2s^2(1+s^2) (TOL_ID)",
            max(max(l["res_anti"], l["res_traco"], l["res_soma"]) for l in linhas_b2) <= TOL_ID,
            max_residuo=max(max(l["res_anti"], l["res_traco"], l["res_soma"]) for l in linhas_b2))
    ambs = [l["th"] for l in linhas_b2 if "AMBIGUO" in (l["cls_anti"], l["cls_sin"]) or "NAN" in (l["cls_anti"], l["cls_sin"])]
    p.check("sem AMBIGUO", None if ambs else True, ambiguos=ambs)
    viol = [l["th"] for l in linhas_b2 if (l["cls_anti"] == "ZERO") != (l["cls_sin"] == "ZERO")]
    zeros = [l["th"] for l in linhas_b2 if l["cls_anti"] == "ZERO"]
    p.check("{Q_th, rho*} = 0 <=> sin th = 0 (os dois lados: zero so em %s)" % zeros, not viol and set(zeros) == {"0", "pi"},
            violacoes=viol, zeros=zeros)
    p.extra = dict(linhas=linhas_b2)
    log("  B2.a:", p.face_O(), "| zeros do anticomutador em", zeros)
    p = E.P("B2.b")
    if beta_conferido:
        Uo = umpy_objetos(thM)
        A = anticomm(Uo["Qth"], Uo["P"])
        nA = frob(A)
        p.check("{Q_thM, rho*} != 0 (TOL_ZERO: |.|_F >= 1e-6)", cls_zero(nA) == "NAO_ZERO", norma=nA)
        p.check("Tr = 2 beta e soma |.|^2 = 2 beta (1 + beta) (float64, TOL_ID)", abs(np.trace(A) - 2 * beta) <= TOL_ID
                and abs(np.sum(np.abs(A) ** 2) - 2 * beta * (1 + beta)) <= TOL_ID,
                res_traco=abs(np.trace(A) - 2 * beta), res_soma=abs(np.sum(np.abs(A) ** 2) - 2 * beta * (1 + beta)))
        c_mp, s_mp = mp.cos(thM_mp), mp.sin(thM_mp)
        P_mp = mp.matrix([[1, 0], [0, 0]])
        Q0_mp = mp.eye(2) - P_mp
        R_mp = mp.matrix([[c_mp, -s_mp], [s_mp, c_mp]])
        Qth_mp = R_mp * Q0_mp * R_mp.T
        A_mp = Qth_mp * P_mp + P_mp * Qth_mp
        tr_mp = A_mp[0, 0] + A_mp[1, 1]
        sq_mp = sum(abs(A_mp[i, j]) ** 2 for i in range(2) for j in range(2))
        p.check("idem em mpmath dps 50 (TOL_ID 1e-40)", abs(tr_mp - 2 * beta_mp) <= TOL_ID_MP and abs(sq_mp - 2 * beta_mp * (1 + beta_mp)) <= TOL_ID_MP,
                res_traco=abs(tr_mp - 2 * beta_mp), res_soma=abs(sq_mp - 2 * beta_mp * (1 + beta_mp)))
    else:
        p.check("beta sem conferencia: SEM_VEREDITO", None)
    log("  B2.b:", p.face_O())
    c = E.C("C14")
    A0 = anticomm(U0["Q0"], U0["P"])
    c.fechar(cls_zero(frob(A0)) == "ZERO", "em th = 0 o anticomutador se anula: o 'nao nulo' de B2 precisa de sin th != 0",
             norma=frob(A0), core_anticommutator_norm_at_thetaM_to_0=(E.core_fd or {}).get("anticommutator_norm_at_thetaM_to_0"))

    # ============================================================================================== B3
    log("-" * 100)
    log("[B3] o vazamento  [REAL runtime, identidade; sem poder discriminante]")
    p = E.P("B3.a")
    rows = []
    for lab, th in G_TH:
        Uo = umpy_objetos(th)
        F = rho_out(th)
        s2 = float(np.sin(th) ** 2)
        r = complex((S(th) @ e0)[1])
        rows.append(dict(th=lab, leak=Uo["leak"], sin2=s2, tr_FQ0=complex(np.trace(F @ (I2 - E00))), F11=complex(F[1, 1]), abs_r2=abs(r) ** 2,
                         res=max(abs(Uo["leak"] - s2), abs(np.trace(F @ (I2 - E00)) - s2), abs(F[1, 1] - s2), abs(abs(r) ** 2 - s2))))
    p.check("Tr(rho* Q_th) = sin^2 th = Tr(F_th(1) Q0) = (rhoOut th)_11 = |r(th)|^2 (TOL_ID) em G_th", max(x["res"] for x in rows) <= TOL_ID,
            max_residuo=max(x["res"] for x in rows))
    p.extra = dict(linhas=rows)
    log("  B3.a:", p.face_O(), "| max res %.1e" % max(x["res"] for x in rows))
    p = E.P("B3.b")
    if beta_conferido:
        Uo = umpy_objetos(thM)
        dl = abs(Uo["leak"] - beta)
        p.check("Tr(rho* Q_thM) = beta (receita do um.py, float64, TOL_LEAK 1e-15)", dl <= TOL_LEAK, leak=Uo["leak"], residuo=dl)
        c_mp, s_mp = mp.cos(thM_mp), mp.sin(thM_mp)
        P_mp = mp.matrix([[1, 0], [0, 0]])
        Q0_mp = mp.eye(2) - P_mp
        R_mp = mp.matrix([[c_mp, -s_mp], [s_mp, c_mp]])
        Qth_mp = R_mp * Q0_mp * R_mp.T
        PQ = P_mp * Qth_mp
        leak_mp = PQ[0, 0] + PQ[1, 1]
        p.check("idem em mpmath dps 50 (TOL_LEAK 1e-45)", abs(leak_mp - beta_mp) <= TOL_LEAK_MP, residuo=abs(leak_mp - beta_mp))
        if E.core_fd is not None:
            p.check("o mesmo numero do core v391 (fractal_dephasing.leak_sin2_thetaM), bit a bit (citado)",
                    E.core_fd.get("leak_sin2_thetaM") == Uo["leak"], core=E.core_fd.get("leak_sin2_thetaM"), aqui=Uo["leak"])
        log("  B3.b:", p.face_O(), "| leak float64 - beta = %.2e | mpmath = %s" % (dl, mp.nstr(abs(leak_mp - beta_mp), 5)))
    else:
        p.check("beta sem conferencia: SEM_VEREDITO", None)
    p = E.P("B3.d")
    if beta_conferido:
        num_op = float(num_op_texto)
        p.check("|beta - %s| <= 5e-7 (numero do operador, V4 l.16, lido dos bytes)" % num_op_texto, abs(beta - num_op) <= CONF_OPERADOR,
                diferenca=abs(beta - num_op))
        log("  B3.d:", p.face_O(), "| |beta - numero do operador| = %.3e" % abs(beta - num_op))
    else:
        p.check("beta sem conferencia: SEM_VEREDITO", None)

    # ============================================================================================== B4
    log("-" * 100)
    log("[B4] F preserva o Um  [REAL pedra 116; F e angulo: so le]")
    p = E.P("B4.a")
    res_u, res_tr, viol_rank, amb, res_proj, um_viol = 0.0, 0.0, [], [], 0.0, []

    def e00(n):
        M = np.zeros((n, n), dtype=complex)
        M[0, 0] = 1
        return M

    for n in (2, 3, 4):
        for k, u in enumerate(HAAR[n]):
            res_u = max(res_u, maxabs(u.conj().T @ u - np.eye(n)))
            alvos = [("E00", e00(n), True)]
            if n == 2:
                alvos.append(("Q0", I2 - E00, True))
                alvos.append(("misto", MISTOS[(2, 2)][k % 100], False))
            else:
                r = 2 + (k % (n - 1))
                alvos.append(("misto", MISTOS[(n, r)][k % 100], False))
            ph = PSIH[n][k % 100]
            alvos.append(("puro", np.outer(ph, ph.conj()), True))
            if n == 4:
                d = 1 + (k % 4)
                alvos.append(("proj", PROJ[d][k % 50], True))
            for lab, rho, eh_proj in alvos:
                Y = u @ rho @ u.conj().T
                res_tr = max(res_tr, abs(np.trace(Y) - np.trace(rho)))
                a, b = posto(Y), posto(rho)
                if a["posto"] is None or b["posto"] is None:
                    amb.append((n, k, lab))
                elif a["posto"] != b["posto"]:
                    viol_rank.append((n, k, lab))
                if eh_proj:
                    res_proj = max(res_proj, maxabs(Y @ Y - Y), maxabs(Y - Y.conj().T))
                if lab == "E00" and not (abs(np.trace(Y) - 1) <= TOL_ID and a["posto"] == 1):
                    um_viol.append((n, k))
    p.check("u^H u = 1 nas 1400 Haar (TOL_ID)", res_u <= TOL_ID, max_residuo=res_u)
    p.check("sem AMBIGUO", None if amb else True, ambiguos=amb[:10])
    p.check("Tr(u rho u^H) = Tr rho (TOL_ID)", res_tr <= TOL_ID, max_residuo=res_tr)
    p.check("posto(u rho u^H) = posto rho (RANK)", not viol_rank, violacoes=viol_rank[:10])
    p.check("u P u^H e projecao (idempotente e hermitiana, TOL_ID)", res_proj <= TOL_ID, max_residuo=res_proj)
    p.check("em rho* (E00): Tr = posto = 1", not um_viol, violacoes=um_viol[:10])
    log("  B4.a:", p.face_O(), "| max res: u^H u %.1e, traco %.1e, projecao %.1e" % (res_u, res_tr, res_proj))
    c = E.C("C6")
    A = np.diag([2.0, 1.0]).astype(complex)
    Y = A @ E00 @ A.conj().T
    c.fechar(abs(np.trace(Y) - 4) <= TOL_ID and maxabs(A.conj().T @ A - I2) >= NAOZERO_MIN,
             "A = diag(2,1) nao unitario: Tr(A rho* A^H) = 4 != 1 -- sem unitariedade o traco muda", traco=complex(np.trace(Y)))
    c = E.C("C7")
    A = I2 - E00
    Y = A @ E00 @ A.conj().T
    pk = posto(Y)
    c.fechar(pk["posto"] == 0 and cls_zero(frob(Y)) == "ZERO", "A = Q0 singular: A rho* A^H = 0, posto 0 -- sem unitariedade o posto cai",
             posto=pk["posto"], norma=frob(Y))
    p = E.P("B4.b")
    rows = []
    for lab, th in G_TH:
        F = rho_out(th)
        pk = posto(F)
        pur = float(np.real(np.trace(F @ F)))
        rows.append(dict(th=lab, posto=pk["posto"], traco=abs(np.trace(F) - 1), idem=maxabs(F @ F - F), herm=maxabs(F - F.conj().T),
                         pureza=pur, cls_pur=cls_pureza(pur)))
    p.check("rhoOut th: posto 1 (RANK) em G_th", all(r["posto"] == 1 for r in rows), postos=[r["posto"] for r in rows])
    p.check("Tr 1, idempotente, hermitiana (TOL_ID)", max(max(r["traco"], r["idem"], r["herm"]) for r in rows) <= TOL_ID,
            max_residuo=max(max(r["traco"], r["idem"], r["herm"]) for r in rows))
    p.check("pureza 1 (PUREZA)", all(r["cls_pur"] == "=1" for r in rows), purezas=[r["pureza"] for r in rows])
    log("  B4.b:", p.face_O())

    # ============================================================================================== B5
    log("-" * 100)
    log("[B5] Tudo = D(F(1)): o ponto final  [Tudo = CONJECTURE ontologica; o limite e de D, nunca de F]")
    p = E.P("B5.a")
    rows = []
    for lab, th in G_TH:
        F = rho_out(th)
        Dinf = diag_expect(F)
        c_, s_ = float(np.cos(th)), float(np.sin(th))
        pk = posto(Dinf)
        pur = float(np.real(np.trace(Dinf @ Dinf)))
        s2t = float(np.sin(2 * th))
        rows.append(dict(th=lab, res_diag=maxabs(Dinf - np.diag([c_ * c_, s_ * s_])), traco=abs(np.trace(Dinf) - 1), posto=pk["posto"],
                         pureza=pur, res_pureza=abs(pur - (1 - 2 * s_ * s_ * c_ * c_)), cls_pur=cls_pureza(pur),
                         sin2th=s2t, cls_sin2=cls_zero(abs(s2t)), sigmas=pk["sigmas"]))
    p.check("D_inf F_th(1) = diag(c^2, s^2); Tr 1; pureza = 1 - 2s^2c^2 (TOL_ID) em G_th",
            max(max(r["res_diag"], r["traco"], r["res_pureza"]) for r in rows) <= TOL_ID,
            max_residuo=max(max(r["res_diag"], r["traco"], r["res_pureza"]) for r in rows))
    ambs = [r["th"] for r in rows if r["posto"] is None or r["cls_pur"] in ("AMBIGUO", "NAN") or r["cls_sin2"] in ("AMBIGUO", "NAN")]
    p.check("sem AMBIGUO", None if ambs else True, ambiguos=ambs)
    v1 = [r["th"] for r in rows if (r["posto"] == 2) != (r["cls_sin2"] == "NAO_ZERO")]
    v2 = [r["th"] for r in rows if r["cls_sin2"] == "ZERO" and r["posto"] != 1]
    v3 = [r["th"] for r in rows if (r["cls_pur"] == "<1") != (r["cls_sin2"] == "NAO_ZERO")]
    lados = dict(posto2=[r["th"] for r in rows if r["posto"] == 2], posto1=[r["th"] for r in rows if r["posto"] == 1])
    p.check("posto 2 <=> sin 2th != 0 (senao 1); pureza < 1 <=> sin 2th != 0 (os dois lados realizados)",
            not v1 and not v2 and not v3 and lados["posto2"] and lados["posto1"], violacoes=v1 + v2 + v3, **lados)
    p.extra = dict(linhas=rows)
    log("  B5.a:", p.face_O(), "| posto 1 em", lados["posto1"])
    c = E.C("C8")
    oks, obs = [], {}
    for lab, th in (("0", 0.0), ("pi/2", PI / 2)):
        F = rho_out(th)
        dd = frob(diag_expect(F) - F)
        pk = posto(diag_expect(F))
        oks.append(cls_zero(dd) == "ZERO" and pk["posto"] == 1)
        obs[lab] = dict(dist=dd, posto=pk["posto"])
    c.fechar(all(oks), "nas bordas sin 2th = 0 (th = 0, pi/2) o ponto final e o proprio F(1), de posto 1: o posto 2 precisa de sin 2th != 0", **obs)

    p = E.P("B5.b")
    if beta_conferido:
        bgrid = [0.0, 1e-5, 1e-3, beta, 0.1, 0.25, 0.5, 0.75, 0.9, 1 - beta, 1 - 1e-3, 1 - 1e-5, 1.0]
        rows = []
        for b in bgrid:
            pk = posto(np.diag([1 - b, b]))
            rows.append(dict(b=b, posto=pk["posto"], esperado=(2 if 0 < b < 1 else 1)))
        ambs = [r["b"] for r in rows if r["posto"] is None]
        p.check("sem AMBIGUO na grade de b", None if ambs else True, ambiguos=ambs)
        p.check("posto diag(1-b, b) = 2 <=> 0 < b < 1; = 1 em b = 0 e b = 1", all(r["posto"] == r["esperado"] for r in rows),
                linhas=rows)
        F = rho_out(thM)
        Dinf = diag_expect(F)
        pk = posto(Dinf)
        pur = float(np.real(np.trace(Dinf @ Dinf)))
        p.check("D_inf F_thM(1) = diag(1-beta, beta) (float64, TOL_ID)", maxabs(Dinf - np.diag([1 - beta, beta])) <= TOL_ID,
                residuo=maxabs(Dinf - np.diag([1 - beta, beta])))
        p.check("posto 2 e pureza 1 - 2 beta (1 - beta) < 1 (PUREZA, TOL_ID)", pk["posto"] == 2 and cls_pureza(pur) == "<1"
                and abs(pur - (1 - 2 * beta * (1 - beta))) <= TOL_ID, posto=pk["posto"], pureza=pur, sigmas=pk["sigmas"])
        c_mp, s_mp = mp.cos(thM_mp), mp.sin(thM_mp)
        S_mp = mp.matrix([[c_mp, s_mp], [-s_mp, c_mp]])
        F_mp = S_mp * mp.matrix([[1, 0], [0, 0]]) * S_mp.T
        D_mp = mp.diag([F_mp[0, 0], F_mp[1, 1]])
        alvo = mp.diag([1 - beta_mp, beta_mp])
        pur_mp = D_mp[0, 0] ** 2 + D_mp[1, 1] ** 2
        p.check("idem em mpmath dps 50 (TOL_ID 1e-40)", mp_maxabs(D_mp, alvo) <= TOL_ID_MP and abs(pur_mp - (1 - 2 * beta_mp * (1 - beta_mp))) <= TOL_ID_MP,
                residuo=mp_maxabs(D_mp, alvo), res_pureza=abs(pur_mp - (1 - 2 * beta_mp * (1 - beta_mp))))
        log("  B5.b:", p.face_O(), "| pureza(thM) = %.16f | sigmas %s" % (pur, pk["sigmas"]))
    else:
        p.check("beta sem conferencia: SEM_VEREDITO", None)

    p = E.P("B5.c")
    rows, amb, viol, res_det, res_tr, mono = [], [], [], 0.0, 0.0, []
    for lab, th in G_TH:
        F = rho_out(th)
        c_, s_ = float(np.cos(th)), float(np.sin(th))
        cs2 = cls_zero(abs(float(np.sin(2 * th))))
        for gl, gm in GAMMAS:
            g = g_sim(gm)
            purs = []
            for t in G_T:
                X = dephase(g, t, F)
                dformula = c_ * c_ * s_ * s_ * (1 - math.exp(-t * (g[0, 1] + g[1, 0])))
                res_det = max(res_det, abs(det2(X) - dformula))
                res_tr = max(res_tr, abs(np.trace(X) - 1))
                pk = posto(X)
                purs.append(float(np.real(np.trace(X @ X))))
                if pk["posto"] is None or cs2 in ("AMBIGUO", "NAN"):
                    amb.append((lab, gl, t))
                    continue
                esperado = (1 if t == 0 else (2 if cs2 == "NAO_ZERO" else 1))
                if pk["posto"] != esperado:
                    viol.append((lab, gl, t, pk["posto"]))
                rows.append(dict(th=lab, gamma=gl, t=t, posto=pk["posto"], sigma_min=pk["sigmas"][-1]))
            if any(purs[k + 1] > purs[k] + TOL_ID for k in range(len(purs) - 1)):
                mono.append((lab, gl))
    p.check("det D_t F_th(1) = c^2 s^2 (1 - e^{-t(g01+g10)}) (TOL_ID) em G_th x G_t x gamma", res_det <= TOL_ID, max_residuo=res_det)
    p.check("traco preservado (TOL_ID)", res_tr <= TOL_ID, max_residuo=res_tr)
    p.check("sem AMBIGUO", None if amb else True, ambiguos=amb[:10])
    p.check("t > 0: posto 2 <=> sin 2th != 0; t = 0: posto 1", not viol, violacoes=viol[:10],
            menor_sigma_min_entre_postos_2=min([r["sigma_min"] for r in rows if r["posto"] == 2] or [None]))
    p.check("pureza nao cresce ao longo de G_t", not mono, violacoes=mono)
    log("  B5.c:", p.face_O(), "| max res det %.1e, traco %.1e | menor sigma_min (posto 2) = %.3e" % (res_det, res_tr,
        min([r["sigma_min"] for r in rows if r["posto"] == 2] or [float("nan")])))

    p = E.P("B5.e(i)")
    b4b = E.P("B4.b")
    p.check("= B4.b: F(1) tem posto 1 em G_th", all(r is True for r in [c_["ok"] for c_ in b4b.checks if c_["nome"].startswith("rhoOut th: posto 1")]),
            remete_a="B4.b")
    log("  B5.e(i):", p.face_O())
    p = E.P("B5.e(ii)")
    contra, amb, trsob = [], [], []
    for lab, th in G_TH:
        F = rho_out(th)
        a, b = posto(diag_expect(F)), posto(F)
        if a["posto"] is None or b["posto"] is None:
            amb.append(lab)
            continue
        trsob.append(abs(np.trace(diag_expect(F)) - np.trace(F)) <= TOL_ID)
        inst = (a["posto"] == b["posto"])
        p.check("instancia th = %s: posto D_inf F_th(1) = posto F_th(1)? (%s vs %s)" % (lab, a["posto"], b["posto"]), inst)
        if not inst:
            contra.append(lab)
    if amb:
        p.check("sem AMBIGUO", None, ambiguos=amb)
    p.extra = dict(contraexemplos=contra, contraexemplo_pre_registrado_thM_presente=("thM" in contra),
                   traco_sobrevive_em_todo_th=all(trsob))
    log("  B5.e(ii):", p.face_O(), "| contraexemplos (negativo honesto):", contra, "| o traco sobrevive em todo th:", all(trsob))

    # ============================================================================================== B6
    log("-" * 100)
    log("[B6] o vazamento sobrevive a defasagem  [termo novo; invariancia diagonal]")
    p = E.P("B6.a")
    res, spread = 0.0, 0.0
    for lab, th in G_TH:
        Uo = umpy_objetos(th)
        s2 = float(np.sin(th) ** 2)
        for gl, gm in GAMMAS:
            vals = [float(np.real(np.trace(Uo["P"] @ dephase(g_sim(gm), t, Uo["Qth"])))) for t in G_T]
            res = max(res, max(abs(v - s2) for v in vals))
            spread = max(spread, max(vals) - min(vals))
    p.check("Tr(rho* D_t Q_th) = sin^2 th para todo t (TOL_ID) em G_th x G_t x gamma", res <= TOL_ID, max_residuo=res)
    p.check("sem dependencia em t (max - min <= TOL_ID)", spread <= TOL_ID, max_variacao_em_t=spread)
    log("  B6.a:", p.face_O(), "| max res %.1e | max variacao em t %.1e" % (res, spread))
    p = E.P("B6.b")
    res, resinf, viol, amb = 0.0, 0.0, [], []
    for lab, th in G_TH:
        Uo = umpy_objetos(th)
        s_, c_ = Uo["s"], Uo["c"]
        csin = cls_zero(abs(s_))
        for gl, gm in GAMMAS:
            g = g_sim(gm)
            for t in G_T:
                X = dephase(g, t, Uo["Qth"])
                A = anticomm(X, Uo["P"])
                Af = np.array([[2 * s_ * s_, -math.exp(-t * g[0, 1]) * s_ * c_], [-math.exp(-t * g[1, 0]) * s_ * c_, 0.0]])
                res = max(res, maxabs(A - Af))
                ca = cls_zero(frob(A))
                if "AMBIGUO" in (ca, csin) or "NAN" in (ca, csin):
                    amb.append((lab, gl, t))
                elif (ca == "ZERO") != (csin == "ZERO"):
                    viol.append((lab, gl, t))
        Ainf = anticomm(diag_expect(Uo["Qth"]), Uo["P"])
        resinf = max(resinf, maxabs(Ainf - np.diag([2 * s_ * s_, 0.0])))
    p.check("{D_t Q_th, rho*} = [[2s^2, -e^{-t g01} sc], [-e^{-t g10} sc, 0]] (TOL_ID) em G_th x G_t x gamma", res <= TOL_ID, max_residuo=res)
    p.check("sem AMBIGUO", None if amb else True, ambiguos=amb[:10])
    p.check("= 0 <=> sin th = 0", not viol, violacoes=viol[:10])
    p.check("{D_inf Q_th, rho*} = diag(2s^2, 0) (TOL_ID)", resinf <= TOL_ID, max_residuo=resinf)
    if beta_conferido:
        Uo = umpy_objetos(thM)
        Ainf = anticomm(diag_expect(Uo["Qth"]), Uo["P"])
        p.check("em thM: diag(2 beta, 0) (float64, TOL_ID)", maxabs(Ainf - np.diag([2 * beta, 0.0])) <= TOL_ID, residuo=maxabs(Ainf - np.diag([2 * beta, 0.0])))
        c_mp, s_mp = mp.cos(thM_mp), mp.sin(thM_mp)
        P_mp = mp.matrix([[1, 0], [0, 0]])
        Q0_mp = mp.eye(2) - P_mp
        R_mp = mp.matrix([[c_mp, -s_mp], [s_mp, c_mp]])
        Qth_mp = R_mp * Q0_mp * R_mp.T
        Dq = mp.diag([Qth_mp[0, 0], Qth_mp[1, 1]])
        Ai = Dq * P_mp + P_mp * Dq
        p.check("idem em mpmath dps 50 (TOL_ID 1e-40)", mp_maxabs(Ai, mp.diag([2 * beta_mp, 0])) <= TOL_ID_MP, residuo=mp_maxabs(Ai, mp.diag([2 * beta_mp, 0])))
    else:
        p.check("beta sem conferencia: SEM_VEREDITO", None)
    log("  B6.b:", p.face_O(), "| max res %.1e, limite %.1e" % (res, resinf))
    c = E.C("C10")
    if beta_conferido:
        Uo = umpy_objetos(thM)
        mais = np.array([[0.5, 0.5], [0.5, 0.5]])
        vals = [float(np.real(np.trace(mais @ dephase(g_sim(1.0), t, Uo["Qth"])))) for t in G_T]
        form = [0.5 - math.exp(-t) * Uo["s"] * Uo["c"] for t in G_T]
        c.fechar((max(vals) - min(vals)) >= C10_DELTA and max(abs(a - b) for a, b in zip(vals, form)) <= TOL_ID,
                 "leitor nao diagonal |+><+|: 1/2 - e^{-t} sc varia com t -- a invariancia de B6.a precisa de leitor diagonal",
                 valores=vals, variacao=max(vals) - min(vals), residuo_formula=max(abs(a - b) for a, b in zip(vals, form)))
    else:
        c.fechar(None, "beta sem conferencia")

    # ============================================================================================== B7
    log("-" * 100)
    log("[B7] os dois regimes: o angulo (S unitario) so le, sem limite; o semigrupo (face) tem limite")
    p = E.P("B7.a1")
    NS = [1, 2, 3, 10, 100, 1000]
    rmax, rrel = 0.0, 0.0
    for lab, th in G_TH:
        for n in NS:
            Sn = np.linalg.matrix_power(S(th), n)
            r1 = maxabs(Sn - S(n * th))
            Fn = Sn @ E00 @ Sn.conj().T
            r2 = abs(Fn[1, 1] - np.sin(n * th) ** 2)
            rmax = max(rmax, r1, r2)
            rrel = max(rrel, max(r1, r2) / (TOL_ID * n))
    p.check("S(th)^n = S(n th) e peso refletido apos n passagens = sin^2(n th) (TOL_ID n) em G_th x n em %s" % NS, rrel <= 1.0,
            max_residuo=rmax, max_residuo_sobre_tolerancia=rrel)
    log("  B7.a1:", p.face_O(), "| max res %.1e (razao a tolerancia %.2e)" % (rmax, rrel))
    p = E.P("B7.a2")
    if beta_conferido:
        W = math.ceil(PI / thM) + 2
        Wpre = pre["beta_runtime"]["referencia_formula_fechada_DERIVED_nao_e_ensaio"]["W"]
        nn = np.arange(OSC_N, dtype=np.float64)
        v = np.sin(nn * thM) ** 2
        jan = sliding_window_view(v, W)
        amp = jan.max(axis=1) - jan.min(axis=1)
        cota = math.cos(thM) - OSC_FOLGA
        p.check("W = ceil(pi/thM) + 2 = %d (pre-registrado %d)" % (W, Wpre), W == Wpre)
        p.check("toda janela de W termos (inicio 0..1e5-W, %d janelas): max - min de sin^2(n thM) >= cos thM - 1e-9" % len(amp),
                bool(np.all(amp >= cota)) and len(amp) == OSC_N - W + 1, min_amplitude=float(amp.min()), cota=cota, n_janelas=len(amp))
        cauda = v[-1000:]
        p.check("a cauda (ultimos 1000 termos) nao converge: max - min >= cota", float(cauda.max() - cauda.min()) >= cota,
                amplitude_cauda=float(cauda.max() - cauda.min()))
        v0 = np.sin(nn * 0.0) ** 2
        p.check("sin th = 0 (th = 0) => constante 0 (exata)", float(np.max(np.abs(v0))) == 0.0)
        log("  B7.a2:", p.face_O(), "| W = %d | min amplitude %.6f >= cota %.6f | janelas %d" % (W, amp.min(), cota, len(amp)))
    else:
        p.check("beta sem conferencia: SEM_VEREDITO", None)
    c = E.C("C11")
    nn = np.arange(OSC_N + 1, dtype=np.float64)
    vpi = np.sin(nn * PI) ** 2
    c.fechar(float(vpi.max()) <= C11_TOL, "th = pi: sin^2(n pi) = 0 para todo n (<= 1e-10 ate 1e5) -- converge: o nao-limite precisa de sin th != 0",
             max_valor=float(vpi.max()))
    p = E.P("B7.b")
    res_rel, mono, amb = 0.0, [], []
    for lab, th in G_TH:
        F = rho_out(th)
        Dinf = diag_expect(F)
        for gl, gm in GAMMAS:
            g = g_sim(gm)
            dists = []
            for t in G_T:
                X = dephase(g, t, F)
                y = math.exp(-gm * t) * F[0, 1]
                if y == 0:
                    rr_ = 0.0 if X[0, 1] == 0 else float("inf")
                else:
                    rr_ = abs(X[0, 1] - y) / abs(y)
                res_rel = max(res_rel, rr_)
                dists.append(frob(X - Dinf))
            if any(dists[k + 1] > dists[k] + 1e-15 for k in range(len(dists) - 1)):
                mono.append((lab, gl))
    p.check("sombra do kernel (dephase_tendsto_expectation): (D_t x)_01 = e^{-gamma t} x_01 (TOL_REL) em G_th x G_t x gamma", res_rel <= TOL_REL,
            max_residuo_relativo=res_rel)
    p.check("|D_t x - D_inf x|_F nao cresce em t", not mono, violacoes=mono)
    log("  B7.b (sombra; veredito CITADO_REAL):", p.face_O(), "| max res relativo %.1e" % res_rel)
    c = E.C("C9")
    if beta_conferido:
        F = rho_out(thM)
        g0 = np.zeros((2, 2))
        dmax = max(frob(dephase(g0, t, F) - F) for t in G_T)
        dl = frob(F - diag_expect(F))
        c.fechar(dmax == 0.0 and cls_zero(dl) == "NAO_ZERO",
                 "g = 0: D_t = id para todo t e F_thM(1) != D_inf F_thM(1) -- sem taxa nao ha convergencia ao ponto final",
                 max_dist_Dt_id=dmax, dist_F_a_Dinf=dl)
    else:
        c.fechar(None, "beta sem conferencia")
    E.P("B7.c")  # CITADO_REAL, coluna O '-'

    # ============================================================================================== B8
    log("-" * 100)
    log("[B8] o ramo do nada (th = 0)  [algebra; 'nada sem referente' = ONTO]")
    p = E.P("B8.a")
    F0 = rho_out(0.0)
    p.check("th = 0: Tr(rho* Q0) = 0 (receita do um.py)", abs(U0["leak"]) <= TOL_ID, leak=U0["leak"])
    p.check("{Q0, rho*} = 0 (TOL_ZERO)", cls_zero(frob(U0["anti0"])) == "ZERO", norma=frob(U0["anti0"]))
    p.check("F_0(1) = rho* (TOL_ID)", maxabs(F0 - E00) <= TOL_ID, residuo=maxabs(F0 - E00))
    rmax = 0.0
    for gl, gm in GAMMAS:
        for t in G_T:
            rmax = max(rmax, maxabs(dephase(g_sim(gm), t, E00) - E00))
    p.check("D_t rho* = rho* para todo t em G_t e gamma (TOL_ID)", rmax <= TOL_ID, residuo=rmax)
    pk = posto(F0)
    p.check("posto 1 e pureza 1", pk["posto"] == 1 and cls_pureza(float(np.real(np.trace(F0 @ F0)))) == "=1")
    log("  B8.a:", p.face_O())

    def atua(th):
        F = rho_out(th)
        out = {}
        for gl, gm in GAMMAS:
            mx = max(frob(dephase(g_sim(gm), t, F) - F) for t in G_T_POS)
            out[gl] = (mx, cls_zero(mx))
        return out

    p = E.P("B8.b")
    rows, viol, amb = [], [], []
    for lab, th in G_TH:
        a = atua(th)
        cs2 = cls_zero(abs(float(np.sin(2 * th))))
        s2c, c2c = cls_zero(float(np.sin(th) ** 2)), cls_zero(float(np.cos(th) ** 2))
        classes = set(x[1] for x in a.values())
        if "AMBIGUO" in classes or "NAN" in classes or cs2 in ("AMBIGUO", "NAN"):
            amb.append(lab)
            continue
        if len(classes) != 1:
            viol.append((lab, "gammas discordam"))
            continue
        nao_atua = (classes == {"ZERO"})
        if nao_atua != (cs2 == "ZERO"):
            viol.append((lab, "<=>"))
        if cs2 == "ZERO" and not (posto(rho_out(th))["posto"] == 1 and ("ZERO" in (s2c, c2c))):
            viol.append((lab, "ramo sin 2th = 0 sem posto 1 ou sem peso refletido em {0, 1}"))
        rows.append(dict(th=lab, max_dist={k: v[0] for k, v in a.items()}, nao_atua=nao_atua, sin2th=cls_zero(abs(float(np.sin(2 * th)))),
                         peso_refletido_classe=s2c, peso_transmitido_classe=c2c))
    p.check("sem AMBIGUO", None if amb else True, ambiguos=amb)
    p.check("(para todo t, D_t F_th(1) = F_th(1)) <=> sin 2th = 0 (peso refletido 0 ou 1; posto 1 nos dois)", not viol and
            any(r["nao_atua"] for r in rows) and any(not r["nao_atua"] for r in rows), violacoes=viol,
            nao_atua_em=[r["th"] for r in rows if r["nao_atua"]])
    p.extra = dict(linhas=rows)
    log("  B8.b:", p.face_O(), "| D nao atua em", [r["th"] for r in rows if r["nao_atua"]])

    # ============================================================================================== B9
    log("-" * 100)
    log("[B9] a sonda honesta: 'o que transmite, por natureza, defasa'  [transmitir = INPUT da gerencia; duas leituras]")
    tabela = []
    for lab, th in G_TH:
        a = atua(th)
        classes = set(x[1] for x in a.values())
        tabela.append(dict(th=lab, t2=float(np.cos(th) ** 2), r2=float(np.sin(th) ** 2), cls_t2=cls_zero(float(np.cos(th) ** 2)),
                           cls_r2=cls_zero(float(np.sin(th) ** 2)), atua=(classes == {"NAO_ZERO"}), nao_atua=(classes == {"ZERO"}),
                           ambiguo=not (classes == {"NAO_ZERO"} or classes == {"ZERO"})))
    p = E.P("B9.a")
    contra = []
    for r in tabela:
        if r["ambiguo"] or r["cls_t2"] in ("AMBIGUO", "NAN"):
            p.check("instancia th = %s: AMBIGUO" % r["th"], None)
            continue
        inst = (r["cls_t2"] != "NAO_ZERO") or r["atua"]
        p.check("instancia th = %s: |t|^2 > 0 => D atua? (|t|^2 = %.3g, atua = %s)" % (r["th"], r["t2"], r["atua"]), inst)
        if not inst:
            contra.append(r["th"])
    p.extra = dict(contraexemplos=contra, contraexemplo_pre_registrado_th0_presente=("0" in contra))
    log("  B9.a (literal):", p.face_O(), "| contraexemplos:", contra)
    c = E.C("C12")
    r0 = [r for r in tabela if r["th"] == "0"]
    c.fechar(bool(r0) and abs(r0[0]["t2"] - 1) <= TOL_ID and r0[0]["nao_atua"],
             "th = 0: |t|^2 = 1 e D nao atua -- a transmissao literal nao forca a defasagem", **(r0[0] if r0 else {}))
    p = E.P("B9.a'")
    contra = []
    for r in tabela:
        if r["ambiguo"] or r["cls_r2"] in ("AMBIGUO", "NAN"):
            p.check("instancia th = %s: AMBIGUO" % r["th"], None)
            continue
        inst = (r["cls_r2"] != "NAO_ZERO") or r["atua"]
        p.check("instancia th = %s: |r|^2 > 0 => D atua? (|r|^2 = %.3g, atua = %s)" % (r["th"], r["r2"], r["atua"]), inst)
        if not inst:
            contra.append(r["th"])
    p.extra = dict(contraexemplos=contra, contraexemplo_pre_registrado_pi2_presente=("pi/2" in contra))
    log("  B9.a' (simetrico):", p.face_O(), "| contraexemplos:", contra)
    c = E.C("C13")
    r2_ = [r for r in tabela if r["th"] == "pi/2"]
    c.fechar(bool(r2_) and abs(r2_[0]["r2"] - 1) <= TOL_ID and r2_[0]["nao_atua"],
             "th = pi/2: |r|^2 = 1 e D nao atua -- o vazamento literal nao forca a defasagem", **(r2_[0] if r2_ else {}))
    p = E.P("B9.b")
    viol = []
    for r in tabela:
        if r["ambiguo"] or "AMBIGUO" in (r["cls_t2"], r["cls_r2"]):
            viol.append((r["th"], "AMBIGUO"))
            continue
        if r["atua"] != (r["cls_t2"] == "NAO_ZERO" and r["cls_r2"] == "NAO_ZERO"):
            viol.append((r["th"], "<=>"))
    amb = [v for v in viol if v[1] == "AMBIGUO"]
    p.check("sem AMBIGUO", None if amb else True, ambiguos=amb)
    p.check("D atua <=> |t|^2 > 0 e |r|^2 > 0 em G_th (os dois lados realizados)", not [v for v in viol if v[1] == "<=>"] and
            any(r["atua"] for r in tabela) and any(r["nao_atua"] for r in tabela), violacoes=viol,
            atua_em=[r["th"] for r in tabela if r["atua"]], nao_atua_em=[r["th"] for r in tabela if r["nao_atua"]])
    if beta_conferido:
        rM = [r for r in tabela if r["th"] == "thM"][0]
        F = rho_out(thM)
        p.check("em thM: D atua e (D_inf F(1))_11 = beta (float64, TOL_ID)", rM["atua"] and abs(diag_expect(F)[1, 1] - beta) <= TOL_ID,
                residuo=abs(diag_expect(F)[1, 1] - beta))
        c_mp, s_mp = mp.cos(thM_mp), mp.sin(thM_mp)
        S_mp = mp.matrix([[c_mp, s_mp], [-s_mp, c_mp]])
        F_mp = S_mp * mp.matrix([[1, 0], [0, 0]]) * S_mp.T
        p.check("idem em mpmath dps 50 (TOL_ID 1e-40)", abs(F_mp[1, 1] - beta_mp) <= TOL_ID_MP, residuo=abs(F_mp[1, 1] - beta_mp))
    else:
        p.check("beta sem conferencia: SEM_VEREDITO", None)
    p.extra = dict(tabela=tabela)
    log("  B9.b (inscricao):", p.face_O(), "| atua em", [r["th"] for r in tabela if r["atua"]])

    # ====================================================================================== anexos (fora do pre-registro)
    log("-" * 100)
    log("[ANEXO] varreduras e achados FORA do pre-registro (nao mudam veredito)")
    var = {}
    if beta_conferido:
        TH_D = np.unique(np.concatenate([np.linspace(-PI, PI, 2001), np.array([th for _, th in G_TH])]))
        v_b2 = v_b5 = v_b8 = v_b3 = amb_d = 0
        for th in TH_D:
            Uo = umpy_objetos(th)
            A = anticomm(Uo["Qth"], Uo["P"])
            ca, csn = cls_zero(frob(A)), cls_zero(abs(float(np.sin(th))))
            F = rho_out(th)
            Dinf = diag_expect(F)
            pk = posto(Dinf)
            cs2 = cls_zero(abs(float(np.sin(2 * th))))
            a = atua(th)
            classes = set(x[1] for x in a.values())
            if "AMBIGUO" in (ca, csn, cs2) or pk["posto"] is None or not (classes == {"ZERO"} or classes == {"NAO_ZERO"}):
                amb_d += 1
                continue
            v_b2 += (ca == "ZERO") != (csn == "ZERO")
            v_b5 += (pk["posto"] == 2) != (cs2 == "NAO_ZERO")
            v_b8 += (classes == {"ZERO"}) != (cs2 == "ZERO")
            s2 = float(np.sin(th) ** 2)
            v_b3 += max(abs(Uo["leak"] - s2), abs(F[1, 1] - s2)) > TOL_ID
        var["X1_theta_denso"] = dict(n_th=len(TH_D), ambiguos=amb_d, violacoes_B2a=v_b2, violacoes_B5a=v_b5, violacoes_B8b_B9b=v_b8,
                                     violacoes_B3a=v_b3, grade="linspace(-pi, pi, 2001) U G_th")
        log("  X1 theta denso (%d pontos): ambiguos %d | violacoes B2.a %d, B5.a %d, B8.b/B9.b %d, B3.a %d" % (len(TH_D), amb_d, v_b2, v_b5, v_b8, v_b3))
        TS_D = np.concatenate([[0.0], np.logspace(-6, 3, 91)])
        res_det = res_b6 = res_b7 = 0.0
        amb_t = []
        F = rho_out(thM)
        Uo = umpy_objetos(thM)
        for gl, gm in GAMMAS:
            g = g_sim(gm)
            for t in TS_D:
                X = dephase(g, t, F)
                res_det = max(res_det, abs(det2(X) - math.cos(thM) ** 2 * math.sin(thM) ** 2 * (1 - math.exp(-2 * gm * t))))
                pk = posto(X)
                if t > 0 and pk["posto"] != 2:
                    amb_t.append((gl, float(t), pk["posto"], pk["sigmas"][-1]))
                res_b6 = max(res_b6, abs(np.trace(Uo["P"] @ dephase(g, t, Uo["Qth"])) - beta))
                y = math.exp(-gm * t) * F[0, 1]
                if y == 0:   # e^{-gamma t} abaixo do menor float (t*gamma ~ 1e3): exige zero exato, sem 0/0
                    res_b7 = mx(res_b7, 0.0 if X[0, 1] == 0 else float("inf"))
                else:
                    res_b7 = mx(res_b7, abs(X[0, 1] - y) / abs(y))
        t_lim = {gl: max([x[1] for x in amb_t if x[0] == gl] or [0.0]) for gl, _ in GAMMAS}
        var["X2_t_denso_em_thM"] = dict(n_t=len(TS_D), max_res_det=res_det, max_res_B6a=res_b6, max_res_rel_B7b=res_b7,
                                        t_com_posto_nao_2=amb_t, maior_t_sem_posto_2_por_gamma=t_lim,
                                        leitura=("para t*gamma pequeno o posto 2 (exato para todo t > 0) cai na banda AMBIGUO do criterio RANK "
                                                 "(sigma_min ~ c^2 s^2 (1 - e^{-2 gamma t})): limite de resolucao da face numerica, nao falha; "
                                                 "a face K decide ali; a menor t de G_t (0.5) fica fora dessa banda"))
        log("  X2 t denso em thM: max res det %.1e, B6.a %.1e, B7.b rel %.1e | t>0 sem posto 2 (banda de resolucao): %d casos; maior t por gamma %s"
            % (res_det, res_b6, res_b7, len(amb_t), t_lim))
        assim = [(1.0, beta), (beta, 1.0), (2.0, 0.5), (0.3, 3.0)]
        res_a, res_ab = 0.0, 0.0
        for g01, g10 in assim:
            g = g_assim(g01, g10)
            for lab, th in G_TH:
                F = rho_out(th)
                Uo = umpy_objetos(th)
                c_, s_ = Uo["c"], Uo["s"]
                for t in G_T:
                    X = dephase(g, t, F)
                    res_a = max(res_a, abs(det2(X) - c_ * c_ * s_ * s_ * (1 - math.exp(-t * (g01 + g10)))))
                    A = anticomm(dephase(g, t, Uo["Qth"]), Uo["P"])
                    Af = np.array([[2 * s_ * s_, -math.exp(-t * g01) * s_ * c_], [-math.exp(-t * g10) * s_ * c_, 0.0]])
                    res_ab = max(res_ab, maxabs(A - Af))
        var["X3_taxas_assimetricas"] = dict(pares=assim, max_res_det_B5c=res_a, max_res_B6b=res_ab)
        log("  X3 taxas assimetricas %s: max res det %.1e, anticomutador %.1e" % ([(round(a, 4), round(b, 4)) for a, b in assim], res_a, res_ab))
        osc = []
        for lab, th in G_TH:
            h = abs(math.remainder(th, PI))
            if cls_zero(abs(math.sin(th))) != "NAO_ZERO":
                continue
            Wt = math.ceil(PI / h) + 2
            vv = np.sin(np.arange(OSC_N, dtype=np.float64) * th) ** 2
            am = sliding_window_view(vv, Wt)
            amp_ = am.max(axis=1) - am.min(axis=1)
            osc.append(dict(th=lab, h=h, W=Wt, cota=math.cos(h) - OSC_FOLGA, min_amplitude=float(amp_.min()),
                            ok=bool(np.all(amp_ >= math.cos(h) - OSC_FOLGA))))
        var["X5_OSC_generalizado_G_th"] = dict(regra="h = dist(th, pi Z); W = ceil(pi/h) + 2; cota cos h - 1e-9", linhas=osc,
                                               todos_ok=all(o["ok"] for o in osc))
        log("  X5 OSC generalizado em G_th (sin th != 0): todos ok =", all(o["ok"] for o in osc), "|",
            [(o["th"], o["W"], round(o["min_amplitude"], 4), round(o["cota"], 4)) for o in osc])
        conv = []
        for lab, th in G_TH:
            Uo = umpy_objetos(th)
            conv.append(dict(th=lab, res_Q_igual_1_menos_F_menos_th=maxabs(Uo["Qth"] - (I2 - rho_out(-th))),
                             dist_Q_a_1_menos_F_th=maxabs(Uo["Qth"] - (I2 - rho_out(th))), cls_sin2=cls_zero(abs(math.sin(2 * th)))))
        var["X6_convencao_Q_th"] = dict(linhas=conv, Q_th_igual_1_menos_F_menos_th=all(x["res_Q_igual_1_menos_F_menos_th"] <= TOL_ID for x in conv),
                                        Q_th_igual_1_menos_F_th_so_se_sin2th_zero=all((x["dist_Q_a_1_menos_F_th"] <= TOL_ID) == (x["cls_sin2"] == "ZERO") for x in conv))
        log("  X6 convencao: Q_th (um.py) = 1 - F_{-th}(1) (kernel) em G_th:", var["X6_convencao_Q_th"]["Q_th_igual_1_menos_F_menos_th"],
            "| Q_th = 1 - F_th(1) so onde sin 2th = 0:", var["X6_convencao_Q_th"]["Q_th_igual_1_menos_F_th_so_se_sin2th_zero"])
        sp = []
        for r_, w_ in ((0.5, 3.0), (beta, 1.0), (0.0, 3.0), (0.0, 1.0)):
            ss_ = np.linspace(0, 50, 5001)
            z = np.exp(-r_ * ss_) * np.exp(1j * w_ * ss_)
            sp.append(dict(r=r_, omega=w_, max_res_modulo=float(np.max(np.abs(np.abs(z) - np.exp(-r_ * ss_)))), modulo_final=float(abs(z[-1])),
                           periodico_2pi_sobre_omega=(float(abs(np.exp(1j * w_ * (2 * PI / w_)) - 1)) <= TOL_ID) if r_ == 0 else None))
        var["X9_sombra_B7c_spin"] = dict(linhas=sp, leitura="r > 0: |spin| = e^{-rs} -> 0 (o centro); r = 0: |spin| = 1, periodo 2pi/omega (so le)")
        log("  X9 sombra de B7.c (spin): ", [(round(x["r"], 4), x["omega"], "%.2e" % x["modulo_final"]) for x in sp])
    oblq = []
    for d in (1, 2, 3, 4):
        for _ in range(25):
            A = haar(4) @ np.diag([1.0, 2.0, 0.5, 1.5]) @ haar(4)
            Dd = np.diag([1.0] * d + [0.0] * (4 - d)).astype(complex)
            Pm = A @ Dd @ np.linalg.inv(A)
            pk = posto(Pm)
            oblq.append(dict(d=d, idem=maxabs(Pm @ Pm - Pm), herm=maxabs(Pm - Pm.conj().T), res_tr_posto=abs(np.trace(Pm) - (pk["posto"] or -1)),
                             posto=pk["posto"]))
    var["X4_idempotentes_obliquos"] = dict(n=len(oblq), max_idem=max(o["idem"] for o in oblq), min_nao_hermiticidade=min(o["herm"] for o in oblq if o["d"] < 4),
                                           max_res_tr_posto=max(o["res_tr_posto"] for o in oblq), postos_ok=all(o["posto"] == o["d"] for o in oblq),
                                           leitura="Tr P = posto P vale tambem para idempotentes NAO hermitianos (B1.b alem das projecoes)")
    log("  X4 idempotentes obliquos (n=4, 100): max |P^2-P| %.1e | min nao-hermiticidade %.2f | max |Tr P - posto P| %.1e | postos ok %s"
        % (var["X4_idempotentes_obliquos"]["max_idem"], var["X4_idempotentes_obliquos"]["min_nao_hermiticidade"],
           var["X4_idempotentes_obliquos"]["max_res_tr_posto"], var["X4_idempotentes_obliquos"]["postos_ok"]))
    E.varredura = var

    # consultas do cetico aferidor (gravadas antes por consultar_mapa.py e consultar_inventario_kernel.py): os numeros
    # citados no anexo sao LIDOS desses arquivos, nunca escritos de memoria
    KQ = {}
    try:
        kq = json.load(open(os.path.join(AQUI, "consultas_mapa", "k_inventario_kernel.json"), encoding="utf-8"))
        KQ = dict(n_lean=kq["kernel_n_arquivos_lean_varridos"],
                  k_S=kq["kernel_achados"]["lei_de_grupo_ou_potencia_da_matriz_S"]["n"],
                  k_S_lin=sorted(set("%s:%d" % (x["arquivo"], x["linha"]) for x in kq["kernel_achados"]["lei_de_grupo_ou_potencia_da_matriz_S"]["primeiros"]
                                     if "theorem" in x["texto"])),
                  k_pow=sum(1 for x in kq["kernel_achados"]["lei_de_grupo_ou_potencia_da_matriz_S"]["primeiros"]
                            if any(w in x["texto"] for w in ("Smat_pow", "Smat_npow", "Smat_nsmul", "Smat_add"))),
                  k_anti=kq["kernel_achados"]["anticomutador"]["n"], k_rank=kq["kernel_achados"]["Matrix_rank"]["n"],
                  i_S=kq["inventario"]["lei_de_grupo_ou_potencia_da_matriz_S"]["n"], i_anti=kq["inventario"]["anticomutador"]["n"],
                  i_rank=kq["inventario"]["Matrix_rank"]["n"])
        for cid in ("o03", "o05"):
            KQ[cid] = json.load(open(os.path.join(AQUI, "consultas_mapa", cid + ".json"), encoding="utf-8"))["n"]
    except Exception as ex:
        E.alertas.append("consulta do cetico aferidor ilegivel: %r (o anexo A1/A9/A10 fica sem numero)" % (ex,))
        KQ = {k: "ILEGIVEL" for k in ("n_lean", "k_S", "k_S_lin", "k_pow", "k_anti", "k_rank", "i_S", "i_anti", "i_rank", "o03", "o05")}
    anexo = [
        dict(id="A1", achado=("O kernel ja tem a LEI DE GRUPO da matriz-S: Smat_mul (a b) : Smat a * Smat b = Smat (a + b) "
             "(declaracao em %s; sha16 do SMatrix.lean conferido nos pinos). S(th)^n = S(n th) (B7.a1) sai dela por inducao. "
             "Consultas (cetico aferidor): kernel do Nos (%s .lean de TGLExt e TGL, fora de .lake) -- %s linhas com Smat_mul "
             "(declaracao, usos e Audit), %s com Smat_pow/Smat_npow/Smat_nsmul/Smat_add; inventario da bancada -- %s; mapa o03 -- %s "
             "(consultas_mapa/k_inventario_kernel.json e o03.json). O pre-registro diz 'S(th)^n: nenhum lema': certo para a "
             "potencia, mas a lei de grupo que a da por inducao ja esta no kernel.")
             % (KQ["k_S_lin"], KQ["n_lean"], KQ["k_S"], KQ["k_pow"], KQ["i_S"], KQ["o03"]), estatuto="[REAL kernel, citado; consulta]"),
        dict(id="A9", achado=("{Q_th, rho*}: as %s linhas do kernel com 'anticomm/anticommut/anticomut' sao dos homonimos -- "
             "current_anticommutes ({Z_d, L} = 0, ModularCurrent.lean), J_and_K_anticommute (TheTwoPairings.lean), "
             "J_anticommutes_with_K e the_light_anticommutes_with_the_gradient (TheVerbSelectsTheAction.lean) e as linhas de "
             "Audit; nenhuma e {Q_th, rho*}; inventario da bancada: %s; mapa o05: %s -- como o pre-registro (levantamento 2.12, "
             "c08 = 0). B2 e termo NOVO para a pedra; o 'nao nulo' em thM so existia na docstring do um.py.")
             % (KQ["k_anti"], KQ["i_anti"], KQ["o05"]), estatuto="[REAL consulta]"),
        dict(id="A10", achado=("Matrix.rank: %s linhas no kernel do Nos e %s no inventario (consultas_mapa/k_inventario_kernel.json), "
             "como o pre-registro; o que o kernel tem de pureza 1 sao INSTANCIAS (trace_square_rank_one_control, "
             "HermitianConeRigidity.lean:139; e a rigidez rank_one_* da forma quadratica), nao o <=> geral de P1 -- como o "
             "levantamento (2.3). P1, P2.a, P2.b e B1.b pedem Matrix.rank na pedra (Mathlib), termo novo.")
             % (KQ["k_rank"], KQ["i_rank"]), estatuto="[REAL consulta]"),
        dict(id="A2", achado="Convencao: o Q_th do um.py (R Q0 R^T, R = S(th)^H) e 1 - F_{-th}(1) do kernel, nao 1 - F_th(1) "
             "(diferem no sinal da coerencia salvo sin 2th = 0). O vazamento Tr(rho* Q_th) = sin^2 th e par em th e nao e afetado; "
             "quem ligar um.py e kernel numa pedra deve usar F_{-th} ou S^H (varredura X6).", estatuto="[REAL medido aqui]"),
        dict(id="A3", achado="Resolucao da face numerica: com gamma = beta e t pequeno, o posto 2 de D_t F_thM(1) (exato para todo "
             "t > 0) cai na banda AMBIGUO do criterio RANK (sigma_min ~ c^2 s^2 (1 - e^{-2 gamma t})); a menor t de G_t (0.5) "
             "esta fora da banda. E limite do instrumento numerico, nao falha da afirmacao (varredura X2).", estatuto="[REAL medido aqui]"),
        dict(id="A4", achado="Tr P = posto P vale tambem para idempotentes obliquos (nao hermitianos), n = 4, d em {1..4} "
             "(varredura X4): a pedra pode enunciar B1.b para IsIdempotentElem sem exigir P = P^H.", estatuto="[REAL medido aqui; KNOWN]"),
        dict(id="A5", achado="Taxas assimetricas g01 != g10 (varredura X3): det D_t F = c^2 s^2 (1 - e^{-t(g01+g10)}) e a forma "
             "fechada de B6.b com e^{-t g01}, e^{-t g10} separados conferem a TOL_ID -- o enunciado de B5.c/B6.b nao precisa de "
             "taxas simetricas.", estatuto="[REAL medido aqui]"),
        dict(id="A6", achado="O numero do core v391 (fractal_dephasing.leak_sin2_thetaM e omega_I) e reproduzido bit a bit pela "
             "receita do um.py reconstruida aqui sem executar o um.py; o campo 'anticommutator_norm_at_thetaM_to_0' do core e "
             "avaliacao exata em th = 0 (Q0), nao limite no angulo (regra dos dois regimes; nota do pre-registro em B2).",
             estatuto="[REAL runtime, citado]"),
        dict(id="A7", achado="beta pela receita da propria fractal_dephasing_principle (SEALED_CODATA_ALPHA * float(np.exp(1/2))) e "
             "pela de BETA_TGL (ALPHA_FINE_CODATA_2018 * sqrt(e)) coincide bit a bit; exp(1/2) == sqrt(e) em float64.",
             estatuto="[REAL medido aqui]"),
        dict(id="A8", achado="OSC generalizado (varredura X5): para todo th de G_th com sin th != 0, toda janela de W_th = ceil(pi/h)+2 "
             "termos (h = dist(th, pi Z)) tem max - min de sin^2(n th) >= cos h - 1e-9 -- o nao-limite angular nao e so do thM.",
             estatuto="[REAL medido aqui]"),
    ]
    E.anexo = anexo

    # =================================================================================== vereditos por parte
    log("=" * 100)
    log("VEREDITOS POR PARTE (face O; a parte final exige a face K quando ha duas faces -- regra (f))")
    por_parte = []
    nao_conformes = []
    for pid in E.ordem_partes:
        p = E.partes[pid]
        esp = p.meta["esperado"]
        if esp == "CITADO":
            fO, ver_parte, conf_ = "NAO_APLICAVEL_O", "CITADO", True
        elif esp == "CITADO_REAL":
            fO = p.face_O()
            ver_parte = "CITADO_REAL"
            conf_ = (fO in ("PASSA_O", "NAO_APLICAVEL_O"))
            if fO == "PASSA_O":
                fO = "SOMBRA_CONSISTENTE_O"
        elif esp == "NAO_TESTAVEL":
            fO, ver_parte, conf_ = "NAO_APLICAVEL_O", "NAO_TESTAVEL", True
        elif esp == "ABERTO":
            fO, ver_parte, conf_ = "NAO_APLICAVEL_O", "ABERTO", True
        else:
            fO = p.face_O()
            esperado_falha = esp.startswith("FALHA")
            if esperado_falha:
                chave = [k for k in p.extra if k.startswith("contraexemplo_pre_registrado")]
                presente = bool(chave and p.extra[chave[0]])
                conf_ = (fO == "FALHA_O" and presente)
            else:
                conf_ = (fO == "PASSA_O")
            so_O = (p.meta["K"].strip() == "-")
            if fO == "SEM_VEREDITO_O":
                ver_parte = "NAO_CONSTRUIDO (face O fail-closed)"
            elif so_O:
                ver_parte = ("PASSA" if fO == "PASSA_O" else "FALHA") + " (face unica O)"
            else:
                ver_parte = "AGUARDA_FACE_K (face O: %s)" % fO
        if not conf_:
            nao_conformes.append(pid)
        n_ok = sum(1 for c_ in p.checks if c_["ok"] is True)
        n_f = sum(1 for c_ in p.checks if c_["ok"] is False)
        n_sv = sum(1 for c_ in p.checks if c_["ok"] is None)
        por_parte.append(dict(id=pid, afirmacao=p.afirm["id"], titulo=p.afirm["titulo"], estatuto_da_afirmacao=p.afirm["estatuto"],
                              enunciado=p.meta["enunciado"], K_sugerida=p.meta["K"], O_pre_registrado=p.meta["O"],
                              tolerancia=p.meta["tolerancia"], falsificador=p.meta["falsificador"], esperado=esp,
                              face_O=fO, conforme_ao_esperado=conf_, veredito_parte=ver_parte,
                              checks_ok=n_ok, checks_falha=n_f, checks_sem_veredito=n_sv, checks=p.checks, extra=jsonable(p.extra)))
        log("  %-9s face O: %-22s esperado: %-55s conforme: %-5s parte: %s" % (pid, fO, esp[:55], conf_, ver_parte))

    ctrls = []
    for cid, c_ in E.controles.items():
        ctrls.append(dict(id=cid, texto=c_.texto, esperado="FALHA_SEM_HIPOTESE", falha_sem_hipotese=c_.falha_sem_hipotese,
                          comportou_como_esperado=(c_.falha_sem_hipotese is True), nota=c_.nota, observado=c_.obs))
        log("  %-4s FALHA_SEM_HIPOTESE: %-5s %s" % (cid, c_.falha_sem_hipotese, c_.nota))
    controles_ok = all(x["comportou_como_esperado"] for x in ctrls) and len(ctrls) == 14
    log("CONTROLES OK:", controles_ok, "| PARTES NAO CONFORMES AO ESPERADO:", nao_conformes)

    # ---------------------------------------------------- comparacao com a rodada 1 (so leitura do arquivo preservado)
    comp = dict(arquivo=None)
    r1p = os.path.join(AQUI, "rodada1_20261012_1356", "RESULTADO_OPTICO.json")
    if os.path.exists(r1p):
        try:
            r1 = json.load(open(r1p, encoding="utf-8"))
            v1 = {x["id"]: x.get("veredito_O") for x in r1.get("partes", [])}
            c1 = {x["id"]: x.get("resultado") for x in r1.get("controles", [])}
            equiv = {"SOMBRA_CONSISTENTE_O": "PASSA_O"}
            difs = [dict(id=x["id"], rodada1=v1.get(x["id"]), rodada2=x["face_O"]) for x in por_parte
                    if equiv.get(x["face_O"], x["face_O"]) != v1.get(x["id"])]
            difc = [dict(id=x["id"], rodada1=c1.get(x["id"]), rodada2=("FALHA_SEM_HIPOTESE" if x["comportou_como_esperado"] else "NAO_FALHOU"))
                    for x in ctrls if c1.get(x["id"]) != ("FALHA_SEM_HIPOTESE" if x["comportou_como_esperado"] else "NAO_FALHOU")]
            comp = dict(arquivo=r1p, sha256=sha256_arquivo(r1p), script_rodada1_sha256=(r1.get("script") or {}).get("sha256"),
                        partes_comparadas=len(por_parte), partes_com_face_O_diferente=difs, controles_diferentes=difc,
                        nota=("comparacao de VEREDITOS (face O), nao de numeros: as duas rodadas sorteiam com a mesma semente mas em "
                              "ordem e desenho proprios; o codigo da rodada 1 nao foi lido para construir esta rodada; "
                              "SOMBRA_CONSISTENTE_O (B7.b) equivale ao PASSA_O da rodada 1"))
        except Exception as ex:
            comp = dict(arquivo=r1p, erro=repr(ex))
    log("[comparacao] rodada 1 x rodada 2: partes com face O diferente:", comp.get("partes_com_face_O_diferente"),
        "| controles diferentes:", comp.get("controles_diferentes"))

    # ======================================================================================= estatutos ONTO / KNOWN
    mapa = pre["b_mapeamento"]["linhas"]
    onto = [dict(id=l[0], inicio=l[1], leitura=l[4], afirmacoes=l[5]) for l in mapa if l[3] == "[ONTO]"]
    inp = [dict(id=l[0], frase=l[1], leitura=l[4], afirmacoes=l[5]) for l in mapa if l[3].startswith("[INPUT")]
    estatutos = dict(
        ONTO_nao_se_testa=dict(
            resumo=("Ficam [ONTO] (leitura; nenhum PASSA de teste): 'Tudo = D_beta(F(1))' como identidade do Tudo (no um.py, "
                    "[CONJECTURE ontologica]); 'Nada = nome sem referente' e a impedancia; 'a transmissao e o verbo; a defasagem e a "
                    "materia'; 'a falha na transmissao cria espaco-tempo, gravidade e consciencia'; c^2 e c^3 como geometria e massa; "
                    "a frequencia como identidade em potencial infinito na borda; posicao <-> posto; 'o observador estabeleceu o "
                    "piso'; O1 (epistemologia: 'ou os vinculos fecham, ou nao fecham'). O que se testou aqui foi so a forma "
                    "matematica que o pre-registro deu a cada frase [INPUT da gerencia]."),
            frases=onto),
        INPUT_da_gerencia_mapeadas=inp,
        KNOWN_por_citacao=[
            "P1: Tr rho^2 = 1 <=> estado puro <=> posto 1 (Nielsen & Chuang, Quantum Computation and Quantum Information, Ex. 2.71) -- "
            "o PASSA_O e da sombra numerica; o conteudo segue [KNOWN]",
            "P2.lit: posto + nulidade = n (Mathlib LinearMap.finrank_range_add_finrank_ker; Axler, Linear Algebra Done Right, Teo. 3.22)",
            "P3: a regra de Luders (Luders 1951) -- P rho P / Tr(P rho) para P de posto 1",
            "B4: invariancia do traco e do posto por conjugacao unitaria (algebra linear elementar); no kernel, pedra 116 (FractalUnitarity)",
            "V4 l.2: fator do tipo III_1 (Connes 1973) -- citado no mapeamento, nao testado",
        ],
        CITADO_REAL_no_kernel=[
            "B7.b: dephase_tendsto_expectation (TGLExt/Ergodicity.lean, G3e) -- a sombra numerica aqui so confere a lei e^{-gamma t}",
            "B7.c: IALDJones.orbit_tendsto_center, angular_orbit_no_limit, angular_orbit_periodic (TGLExt/IALDJones.lean)",
            "B9.c: transmission_dephases (TGLExt/TheVerbSelectsTheAction.lean:529), re-exportacao de axiomFlow_gradient (v385)",
        ],
        OPEN=["O2: a leitura do espaco latente dos modelos (F0.3.COLAPSO: registro comportamental de 14/09; sem telemetria latente)"],
        REAL_runtime_reproduzido=["B1 (omega(I) = Tr rho* = 1) e B3.b (o vazamento = beta) reproduzem bit a bit os numeros do core v391"],
        regra_dos_dois_regimes=("F = Ad(S(th)) e angulo (unitario, periodico): B4, B7.a1, B7.a2 -- so le, sem limite (B7.a2 mostra que "
                                "sin^2(n th) nao converge); D_t e a face (semigrupo dissipativo): B5, B6, B7.b -- tem limite D_inf = "
                                "diagExpect. Nenhum limite foi pedido ao angulo; '{Q, rho*} = 0 so em thM -> 0' foi lido como avaliacao "
                                "em th = 0 (B8.a, C14)."),
    )

    # ======================================================================================= auto-auditoria do fonte
    fonte = open(os.path.abspath(__file__), "rb").read().decode("utf-8")
    proibidos_num = [r"0[.]0120", r"0[.]01203", r"7[.]297", r"0[.]1099", r"1[.]6487", r"0[.]9939", r"0[.]0240"]
    achados_num = {pat: len(re.findall(pat, fonte)) for pat in proibidos_num}
    # as palavras vigiadas sao montadas em runtime e reportadas por ROTULO neutro: nem o fonte nem o JSON as escrevem
    PALAVRAS = ["CONF" + "IRMED", "PRO" + "VED", "n\u00e3o " + "provou", "p\u00f3s-" + "di\u00e7\u00e3o"]
    ROTULOS = ["w1 (a palavra vedada pela regua n.4, ingles maiusculo)", "w2 (o participio ingles de 'provar', maiusculo)",
               "w3 (a negacao da prova, pt)", "w4 (o demerito da retrodicao, pt)"]
    achados_pal = {r_: fonte.count(w_) for r_, w_ in zip(ROTULOS, PALAVRAS)}
    auto = dict(beta_literal_no_fonte=achados_num, sem_beta_literal=all(v == 0 for v in achados_num.values()),
                palavras_proibidas_no_fonte=achados_pal, sem_palavras_proibidas=all(v == 0 for v in achados_pal.values()),
                fonte=dict(caminho=os.path.abspath(__file__), bytes=len(fonte.encode("utf-8")),
                           sha256=hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()))
    log("[auto-auditoria] sem beta literal no fonte:", auto["sem_beta_literal"], "| sem palavras proibidas:", auto["sem_palavras_proibidas"])

    # ------------------------------------------------------------------------- impressao digital do kernel (fim)
    imp_fim = impressao_digital_kernel()
    imp_fim["igual_ao_inicio"] = (imp_fim["sha256_metadados"] == imp_ini["sha256_metadados"] and
                                  imp_fim["sha256_conteudo_lean"] == imp_ini["sha256_conteudo_lean"])
    log("[fim] impressao digital do tgl_kernel:", imp_fim["sha256_metadados"][:16], imp_fim["sha256_conteudo_lean"][:16],
        "| igual ao inicio:", imp_fim["igual_ao_inicio"])

    resumo = dict(
        face_O={x["id"]: x["face_O"] for x in por_parte},
        partes_conformes_ao_esperado=sum(1 for x in por_parte if x["conforme_ao_esperado"]),
        partes_total=len(por_parte), nao_conformes=nao_conformes, controles_ok=controles_ok,
        falhas_pre_registradas_observadas={k: E.partes[k].extra.get("contraexemplos") for k in ("B5.e(ii)", "B9.a", "B9.a'")},
        beta_conferido=beta_conferido, freeze=conf["veredito"], kernel_intacto=imp_fim["igual_ao_inicio"] and imp_ini["igual_ao_freeze"],
        anexo_ids=[a["id"] for a in anexo])
    resultado = dict(
        documento="RESULTADO_OPTICO -- F1.FREQUENCIA (trilha POSTO), rodada 2 do construtor otico",
        gerencia="c1", autor="construtor otico (subagente do workflow posto-e-tempo), rodada 2",
        quando_local=agora_local(), quando_utc=agora_utc(), duracao_s=round(time.time() - t0, 2),
        escopo=("ensaio sintetico (numpy/mpmath); escrita so em 2_OPTICO; um.py lido por bytes, nao executado; nenhum Lean, Bancada, "
                "provedor, dado observado ou chamada paga; rodada 1 preservada em rodada1_20261012_1356/"),
        regra_de_leitura=("PASSA_O = validade matematica na face otica testada, nao creditacao; nao move gate; nao fala da natureza. "
                          "As identidades em thM (B3; partes em thM de B2, B5, B6) nao tem poder discriminante: PASSA = validade algebrica."),
        freeze=conf, tolerancias_conferidas=dict(ok=tol_ok, itens=tol_conf), pinos=dict(pinos=pinos, kernel=pinos_kernel, verbatins=verb),
        beta_runtime=beta_info, beta_conferido=beta_conferido,
        ambiente=dict(python=sys.version.split()[0], numpy=np.__version__, mpmath=mp.__version__, plataforma=platform.platform()),
        protocolo=dict(texto_congelado=proto, G_th=[l for l, _ in G_TH], G_t=G_T, gammas=[l for l, _ in GAMMAS], semente=SEMENTE),
        decisoes_do_construtor=E.decisoes,
        por_parte=por_parte, controles=ctrls, controles_ok=controles_ok,
        varredura=E.varredura, anexo_fora_do_preregistro=anexo, estatutos=estatutos,
        impressao_digital_kernel=dict(freeze=imp_pre, inicio=imp_ini, fim=imp_fim),
        comparacao_rodada1=comp,
        auto_auditoria_do_fonte=auto, alertas=E.alertas, resumo=resumo,
        arquivos=dict(script=os.path.abspath(__file__), log=SAIDA_LOG, conferencia_freeze=CONF_FREEZE,
                      preservacao_rodada1=os.path.join(AQUI, "PRESERVACAO_RODADA1.json")),
    )
    txt_res = json.dumps(jsonable(resultado), ensure_ascii=False)
    no_json = {r_: txt_res.count(w_) for r_, w_ in zip(ROTULOS, PALAVRAS)}
    resultado["auto_auditoria_do_fonte"]["palavras_vigiadas_no_RESULTADO"] = no_json
    resultado["auto_auditoria_do_fonte"]["RESULTADO_sem_palavras_vigiadas"] = all(v == 0 for v in no_json.values())
    log("[auto-auditoria] RESULTADO sem palavras vigiadas:", all(v == 0 for v in no_json.values()))
    info = escrever_json(SAIDA_JSON, resultado)
    log("RESULTADO_OPTICO.json:", info["bytes"], "bytes, sha256", info["sha256"])
    log("fim", agora_local(), "| %.1f s" % (time.time() - t0))
    log.fechar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
