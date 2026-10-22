# -*- coding: utf-8 -*-
"""CONSTRUTOR OTICO -- F1.FREQUENCIA (trilha POSTO), gerencia c1, 12/10/2026.

Ensaio SINTETICO da face O (modelo otico) do PRE-REGISTRO congelado em 1_PREREGISTRO (FREEZE.json).
- numpy float64/complex128; mpmath dps 50 nas identidades em thM. Nenhum dado observado, nenhum provedor, nenhuma
  ferramenta da Bancada, nenhuma chamada paga. O um.py NAO e executado: alpha e lido dos BYTES (linha unica
  ALPHA_FINE_CODATA_2018), beta = alpha*sqrt(e) em runtime; o numero de conferencia vem do PREREGISTRO.json congelado
  (beta_runtime.beta_float64) e o numero do operador vem dos bytes de V4. beta nunca literal neste arquivo (guarda abaixo).
- Tolerancias, grades, semente e tamanhos de amostra sao LIDOS do texto congelado (protocolo_otico); se o texto nao
  casar com o que este ensaio implementa, ABORTA (fail-closed). Nada de tolerancia, mapeamento ou esperado e mudado.
- Objetos: rho*, Q0, Rot, Q_th pela receita do um.py (l.6512-6519); S(th), F_th(1) = rhoOut th pela do kernel
  (TGLExt/SMatrix.lean: Smat = cos*1 + sin*Grot, rhoOut = S*single 0 0 1*S^H); D_t = dephase g t (TGLExt/Ergodicity.lean:
  (D_t x)_ij = e^{-t g_ij} x_ij), g_ii = 0, g_01 = g_10 = gamma em {1, beta}; D_inf = diagExpect (TGLExt/CondExpect.lean).
- Escreve SO em 2_OPTICO: RESULTADO_OPTICO.json e LOG_OPTICO.txt (tentativas anteriores movidas para tentativas/).
PASSA aqui = validade matematica na face testada (modelo otico), nao creditacao; nao move gate; nao fala da natureza.
"""
import datetime, hashlib, json, math, os, platform, re, sys

import numpy as np
import mpmath as mp
from numpy.lib.stride_tricks import sliding_window_view

T0 = datetime.datetime.now(datetime.timezone.utc)
AQUI = os.path.dirname(os.path.abspath(__file__))
PRE = os.path.join(os.path.dirname(AQUI), "1_PREREGISTRO")
NOS = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s"
UMPY = os.path.join(NOS, "um.py")
CORE = os.path.join(NOS, "um_absoluto.json")
TGLEXT = os.path.join(NOS, "tgl_kernel", "TGLExt")
MATHLIB_RN = os.path.join(NOS, "tgl_kernel", ".lake", "packages", "mathlib", "Mathlib", "LinearAlgebra",
                          "FiniteDimensional", "Lemmas.lean")
V4 = "C:\\IALD\\Central de Patentes\\work\\cunhagens_10out\\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt"
SAIDA_JSON = os.path.join(AQUI, "RESULTADO_OPTICO.json")
SAIDA_LOG = os.path.join(AQUI, "LOG_OPTICO.txt")

LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s, flush=True)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_arq(p):
    with open(p, "rb") as fh:
        b = fh.read()
    return len(b), sha_bytes(b)


def gravar_atomico(caminho, b):
    if os.path.exists(caminho):
        os.makedirs(os.path.join(AQUI, "tentativas"), exist_ok=True)
        st = os.stat(caminho)
        carimbo = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y%m%d_%H%M%S")
        destino = os.path.join(AQUI, "tentativas", os.path.basename(caminho) + "." + carimbo)
        k = 0
        while os.path.exists(destino):
            k += 1
            destino = os.path.join(AQUI, "tentativas", os.path.basename(caminho) + "." + carimbo + "_%d" % k)
        os.replace(caminho, destino)
    tmp = caminho + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(b)
    with open(tmp, "rb") as fh:
        if fh.read() != b:
            raise SystemExit("FALHA VISIVEL: temporario nao confere: " + tmp)
    os.replace(tmp, caminho)
    with open(caminho, "rb") as fh:
        if fh.read() != b:
            raise SystemExit("FALHA VISIVEL: gravado nao confere: " + caminho)


def abortar(m):
    log("ABORTO (fail-closed): " + m)
    gravar_atomico(SAIDA_LOG, ("\n".join(LOG) + "\n").encode("utf-8"))
    sys.exit(2)


# ------------------------------------------------------------------------------------------------------------------
# 0. guarda de literal: nenhum literal de alpha ou de beta neste arquivo (o padrao e montado por pedacos)
# ------------------------------------------------------------------------------------------------------------------
_SRC = open(os.path.abspath(__file__), "rb").read()
SCRIPT_SHA256 = sha_bytes(_SRC)
_src_txt = _SRC.decode("utf-8")
for _pad in ("0" + r"\." + "0120", "7" + r"\." + "2973", "0" + r"\." + "1099"):
    if re.search(_pad, _src_txt):
        abortar("literal proibido no proprio script: padrao " + _pad)
log("run_optico.py sha256", SCRIPT_SHA256, "| guarda de literal: nenhum literal de alpha, beta ou thetaM no script")


def arquivar_anteriores():
    """preserva as tentativas: o RESULTADO e o LOG anteriores vao para tentativas/ ANTES de qualquer ensaio desta rodada."""
    movidos = {}
    for caminho in (SAIDA_JSON, SAIDA_LOG):
        if os.path.exists(caminho):
            os.makedirs(os.path.join(AQUI, "tentativas"), exist_ok=True)
            carimbo = datetime.datetime.fromtimestamp(os.stat(caminho).st_mtime).strftime("%Y%m%d_%H%M%S")
            destino = os.path.join(AQUI, "tentativas", os.path.basename(caminho) + "." + carimbo)
            k = 0
            while os.path.exists(destino):
                k += 1
                destino = os.path.join(AQUI, "tentativas", os.path.basename(caminho) + "." + carimbo + "_%d" % k)
            os.replace(caminho, destino)
            movidos[os.path.basename(caminho)] = destino
    return movidos


ARQUIVADOS = arquivar_anteriores()
log("tentativas anteriores arquivadas:", ARQUIVADOS)

# ------------------------------------------------------------------------------------------------------------------
# 1. o FREEZE: o pre-registro tem de ser o congelado
# ------------------------------------------------------------------------------------------------------------------
FREEZE = json.load(open(os.path.join(PRE, "FREEZE.json"), encoding="utf-8"))
nF, hF = sha_arq(os.path.join(PRE, "FREEZE.json"))
nJ, hJ = sha_arq(os.path.join(PRE, "PREREGISTRO.json"))
nM, hM = sha_arq(os.path.join(PRE, "PREREGISTRO.md"))
if (nJ, hJ) != (FREEZE["PREREGISTRO.json"]["bytes"], FREEZE["PREREGISTRO.json"]["sha256"]):
    abortar("PREREGISTRO.json difere do FREEZE")
if (nM, hM) != (FREEZE["PREREGISTRO.md"]["bytes"], FREEZE["PREREGISTRO.md"]["sha256"]):
    abortar("PREREGISTRO.md difere do FREEZE")
D = json.load(open(os.path.join(PRE, "PREREGISTRO.json"), encoding="utf-8"))
log("FREEZE ok: PREREGISTRO.json", nJ, hJ, "| PREREGISTRO.md", nM, hM, "| FREEZE.json", nF, hF)

# ------------------------------------------------------------------------------------------------------------------
# 2. o protocolo otico LIDO do texto congelado (as constantes deste ensaio saem daqui; divergencia => aborta)
# ------------------------------------------------------------------------------------------------------------------
PO = D["protocolo_otico"]


def casa(chave, rx):
    m = re.search(rx, PO[chave])
    if not m:
        abortar("protocolo_otico.%s nao casa com o que este ensaio implementa: %r" % (chave, PO[chave]))
    return m.groups()


g = casa("TOL_ID", r"^\|x - y\| <= (\S+) \(float64\); <= (\S+) \(mpmath\)$")
TOL_ID, TOL_ID_MP_S = float(g[0]), g[1]
g = casa("TOL_ZERO", r"^\|X\|_F <= (\S+) zero; >= (\S+) não zero; entre: AMBIGUO$")
Z_EQ, Z_NE = float(g[0]), float(g[1])
g = casa("RANK", r"^sigma <= (\S+) nulo; >= (\S+) não nulo; entre: AMBIGUO$")
RK_NUL, RK_NON = float(g[0]), float(g[1])
g = casa("PUREZA", r"^\|Tr rho\^2 - 1\| <= (\S+): = 1; Tr rho\^2 <= 1 - (\S+): < 1; entre: AMBIGUO$")
PUR_EQ, PUR_LT = float(g[0]), float(g[1])
g = casa("TOL_REL", r"^\|x - y\| <= (\S+) \|y\| \(decaimento\)$")
TOL_REL = float(g[0])
g = casa("TOL_LEAK", r"^\|Tr\(rho\* Q_thM\) - beta\| <= (\S+) \(float64\); <= (\S+) \(mpmath\)$")
TOL_LEAK, TOL_LEAK_MP_S = float(g[0]), g[1]
g = casa("CONF_OPERADOR", r"^\|beta - ([0-9.]+)\| <= (\S+)$")
CONF_OP_NUM_S, CONF_OP_TOL = g[0], float(g[1])
g = casa("OSC", r"^toda janela de W = ceil\(pi/thM\) \+ (\d+) = (\d+) termos, início em \[0, (\S+) - W\]: "
                r"max - min de sin\^2\(n thM\) >= cos thM - (\S+)$")
OSC_EXTRA, OSC_W_PRE, OSC_N, OSC_SLACK = int(g[0]), int(g[1]), int(float(g[2])), float(g[3])
g = casa("amostras", r"^default_rng\((\d+)\); Haar \(QR\) n = 2/3/4: (\d+)/(\d+)/(\d+); mistos U diag\(p\) U\^H, "
                     r"p_i ~ U\[([0-9.]+),([0-9.]+)\] normalizado, posto 2\.\.n: (\d+) por \(n, posto\); (\d+) M 2x2 "
                     r"gaussianas; (\d+) psi por n; (\d+) projeções de posto d em \{1\.\.4\}, n = 4$")
SEED, NH2, NH3, NH4 = int(g[0]), int(g[1]), int(g[2]), int(g[3])
P_LO, P_HI, NMIX, NM, NPSI, NPROJ = float(g[4]), float(g[5]), int(g[6]), int(g[7]), int(g[8]), int(g[9])
g = casa("beta", r"repr\(beta\) == '([0-9.]+)' e \|beta_mp - beta\| <= (\S+), senão SEM_VEREDITO em thM$")
CONF_BETA_REPR, TOL_BETA_MP_S = g[0], g[1]
g = casa("precisao", r"^float64/complex128 \(numpy (\S+)\); mpmath (\S+) dps (\d+) nas identidades em thM$")
NUMPY_PRE, MPMATH_PRE, DPS = g[0], g[1], int(g[2])
casa("objetos", r"D_t com g_01 = g_10 = gamma em \{1, beta\}; D_inf exato$")
casa("fail_closed", r"^NaN/Inf, AMBIGUO, alpha ilegível ou beta sem conferência => SEM_VEREDITO visível, nunca PASSA$")
GTH_SPEC = ["0", "thM", "-thM", "3thM", "pi/6", "pi/4", "pi/3", "pi/2", "2pi/3", "pi", "1.0", "2.5"]
GT_SPEC = ["0", "0.5", "1", "2", "5", "10", "100"]
if PO["G_th"] != "{" + ", ".join(GTH_SPEC) + "}":
    abortar("G_th congelado difere: %r" % PO["G_th"])
if PO["G_t"] != "{" + ", ".join(GT_SPEC) + "}":
    abortar("G_t congelado difere: %r" % PO["G_t"])
if CONF_BETA_REPR != D["beta_runtime"]["beta_float64"]:
    abortar("o repr de conferencia do protocolo difere de beta_runtime.beta_float64")
GT = [float(x) for x in GT_SPEC]
mp.mp.dps = DPS
TOL_ID_MP, TOL_LEAK_MP, TOL_BETA_MP = mp.mpf(TOL_ID_MP_S), mp.mpf(TOL_LEAK_MP_S), mp.mpf(TOL_BETA_MP_S)
AMBIENTE = dict(python=platform.python_version(), numpy=np.__version__, mpmath=mp.__version__,
                numpy_preregistrado=NUMPY_PRE, mpmath_preregistrado=MPMATH_PRE,
                versoes_conferem=(np.__version__ == NUMPY_PRE and mp.__version__ == MPMATH_PRE),
                plataforma=platform.platform())
log("protocolo lido do congelado: TOL_ID", TOL_ID, TOL_ID_MP_S, "| TOL_ZERO", Z_EQ, Z_NE, "| RANK", RK_NUL, RK_NON,
    "| PUREZA", PUR_EQ, PUR_LT, "| TOL_REL", TOL_REL, "| TOL_LEAK", TOL_LEAK, TOL_LEAK_MP_S, "| CONF_OPERADOR tol",
    CONF_OP_TOL, "| OSC W", OSC_W_PRE, "N", OSC_N, "folga", OSC_SLACK, "| semente", SEED, "| dps", DPS)
log("ambiente:", json.dumps(AMBIENTE, ensure_ascii=False))
COLUNAS = {}
for a in D["c_afirmacoes"]:
    for p in a["partes"]:
        COLUNAS[p[0]] = dict(afirmacao=a["id"], enunciado=p[1], K=p[2], O=p[3], tolerancia=p[4], falsificador=p[5],
                             esperado=p[6])
g = re.match(r"^n em \{([0-9,]+)\}$", COLUNAS["B7.a1"]["O"])
if not g:
    abortar("B7.a1: coluna O nao casa")
N_PASSAGENS = [int(x) for x in g.group(1).split(",")]

# ------------------------------------------------------------------------------------------------------------------
# 3. beta em runtime, dos BYTES do um.py (sem executar), com o pino do pre-registro
# ------------------------------------------------------------------------------------------------------------------
h = hashlib.sha256()
alphas, sealeds, betarec, nlin = [], [], [], 0
with open(UMPY, "rb") as fh:
    for nlin, ln in enumerate(fh, 1):
        h.update(ln)
        if ln.startswith(b"ALPHA_FINE_CODATA_2018") or ln.startswith(b"SEALED_CODATA_ALPHA") or ln.startswith(b"BETA_TGL"):
            s = ln.rstrip(b"\r\n")
            m = re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9][0-9.eE+-]*)\s*$", s)
            if m:
                alphas.append((nlin, m.group(1).decode()))
            m = re.match(rb"^SEALED_CODATA_ALPHA\s*=\s*([0-9][0-9.eE+-]*)\s*(#.*)?$", s)
            if m:
                sealeds.append((nlin, m.group(1).decode()))
            if s.startswith(b"BETA_TGL = "):
                betarec.append((nlin, s.decode("utf-8")))
UMPY_SHA = h.hexdigest()
pino_um = [p for p in D["pinos"] if p[0].endswith("um.py")][0]
if UMPY_SHA != pino_um[2]:
    abortar("um.py difere do pino do pre-registro: %s != %s" % (UMPY_SHA, pino_um[2]))
if len(alphas) != 1:
    abortar("ALPHA_FINE_CODATA_2018 nao unico/ilegivel nos bytes: %r" % alphas)
ALPHA_LINHA, ALPHA_TXT = alphas[0]
beta = float(ALPHA_TXT) * math.sqrt(math.e)
beta_mp = mp.mpf(ALPHA_TXT) * mp.sqrt(mp.e)
BETA_OK = (repr(beta) == CONF_BETA_REPR) and (abs(beta_mp - mp.mpf(beta)) <= TOL_BETA_MP)
thM = float(np.arcsin(np.sqrt(beta)))           # receita do um.py (l.6510)
thM_math = math.asin(math.sqrt(beta))
thM_mp = mp.asin(mp.sqrt(beta_mp))
W_OSC = math.ceil(math.pi / thM) + OSC_EXTRA
BETA_INFO = dict(alpha_linha=ALPHA_LINHA, alpha_texto=ALPHA_TXT, sealed=sealeds, beta_tgl_linha=betarec,
                 um_py_sha256=UMPY_SHA, um_py_linhas=nlin, beta_float64=repr(beta),
                 beta_mpmath=mp.nstr(beta_mp, 32), conferencia_repr=CONF_BETA_REPR,
                 desvio_mp_float=mp.nstr(abs(beta_mp - mp.mpf(beta)), 5), tol_mp_float=TOL_BETA_MP_S,
                 BETA_CONFERIDO=BETA_OK, theta_M=repr(thM), theta_M_math_asin=repr(thM_math),
                 theta_M_receitas_iguais=(thM == thM_math), theta_M_preregistrado=D["beta_runtime"]["theta_M"],
                 theta_M_mpmath=mp.nstr(thM_mp, 32), W_osc=W_OSC, W_preregistrado=OSC_W_PRE)
SEALED_OK = (len(sealeds) == 1 and sealeds[0][1] == ALPHA_TXT)
BETA_INFO["sealed_igual_alpha"] = SEALED_OK
BETA_INFO["beta_tgl_receita_texto_ok"] = (len(betarec) == 1 and "ALPHA_FINE_CODATA_2018" in betarec[0][1]
                                          and "math.sqrt(math.e)" in betarec[0][1])
# a receita DENTRO de fractal_dephasing_principle usa SEALED_CODATA_ALPHA * float(np.exp(ONE/(ONE+ONE))) (l.6509-6510)
beta_receita_funcao = float(sealeds[0][1]) * float(np.exp(1.0 / (1.0 + 1.0))) if sealeds else float("nan")
BETA_INFO["beta_receita_da_funcao_um_py"] = repr(beta_receita_funcao)
BETA_INFO["beta_receita_da_funcao_igual"] = (beta_receita_funcao == beta)
log("beta runtime:", json.dumps(BETA_INFO, ensure_ascii=False))
if W_OSC != OSC_W_PRE:
    log("AVISO: W calculado", W_OSC, "!= W congelado", OSC_W_PRE)

# numero do operador: dos BYTES de V4 (l.16), conferido com o do protocolo congelado
v4b = open(V4, "rb").read()
if sha_bytes(v4b) != D["a_verbatins"]["V4"]["sha256"]:
    abortar("V4 difere do pre-registro")
v4l = v4b.decode("utf-8").split("\n")
m = re.search(r"\\approx\s*([0-9]+\.[0-9]+)", v4l[15])
if not m or m.group(1) != CONF_OP_NUM_S:
    abortar("numero do operador em V4 l.16 nao casa com CONF_OPERADOR: %r" % (m.group(1) if m else None))
OP_NUM_S = m.group(1)
log("numero do operador lido de V4 l.16:", OP_NUM_S, "(= CONF_OPERADOR congelado)")

# ancoras do core (somente leitura; nao decidem nada)
CORE_N, CORE_SHA = sha_arq(CORE)
pino_core = [p for p in D["pinos"] if p[0].endswith("um_absoluto.json")][0]
_core = json.load(open(CORE, encoding="utf-8"))
CORE_FD = _core["core"]["fractal_dephasing"]
CORE_TRPF = _core["core"]["certificate_II"]["H1_finite_face"]["trace_PF"]
del _core
log("core:", CORE_N, CORE_SHA, "pino confere:", CORE_SHA == pino_core[2], "| fractal_dephasing.leak",
    CORE_FD["leak_sin2_thetaM"], "| trace_PF", CORE_TRPF)

# ------------------------------------------------------------------------------------------------------------------
# 4. classificacoes e desvios (as faixas do protocolo)
# ------------------------------------------------------------------------------------------------------------------


def dev(x, y=0.0):
    d = np.asarray(x, dtype=complex) - np.asarray(y, dtype=complex)
    return float(np.sqrt(np.sum(np.abs(d) ** 2)))


def st_tol(d, tol):
    if not math.isfinite(d):
        return "NAO_FINITO"
    return "OK" if d <= tol else "VIOLA"


def zcls(v):
    v = float(v)
    if not math.isfinite(v):
        return "NAO_FINITO"
    if v <= Z_EQ:
        return "ZERO"
    if v >= Z_NE:
        return "NAO_ZERO"
    return "AMBIGUO"


def eqcls(x, y):
    """igualdade com a faixa TOL_ID/TOL_ZERO: <= TOL_ID igual; >= Z_NE diferente; entre: AMBIGUO."""
    d = dev(x, y)
    if not math.isfinite(d):
        return "NAO_FINITO"
    if d <= TOL_ID:
        return "IGUAL"
    if d >= Z_NE:
        return "DIFERENTE"
    return "AMBIGUO"


def rank_info(A):
    s = np.linalg.svd(np.asarray(A, dtype=complex), compute_uv=False)
    if not np.all(np.isfinite(s)):
        return None, "NAO_FINITO", s
    nul = s <= RK_NUL
    non = s >= RK_NON
    if np.any(~(nul | non)):
        return None, "AMBIGUO", s
    return int(non.sum()), "OK", s


def nulidade_info(A):
    """nulidade independente da SVD do posto: autovalores da PROPRIA A hermitiana (eigvalsh), |lambda| com as faixas do RANK.
    Para A hermitiana os valores singulares sao os |autovalores| e dim ker A = numero de autovalores nulos.
    (Tentativa 1 usou eigvalsh(A^H A) com as faixas ao quadrado: o autovalor nulo de A^H A sai com erro absoluto ~eps|A|^2 ~ 1e-16,
    acima de (1e-12)^2 -- artefato da construcao, preservado em tentativas/.)"""
    A = np.asarray(A, dtype=complex)
    if not np.all(np.isfinite(A)):
        return None, "NAO_FINITO"
    if dev(A, A.conj().T) > TOL_ID:
        return None, "AMBIGUO"
    w = np.abs(np.linalg.eigvalsh(A))
    if not np.all(np.isfinite(w)):
        return None, "NAO_FINITO"
    nul = w <= RK_NUL
    non = w >= RK_NON
    if np.any(~(nul | non)):
        return None, "AMBIGUO"
    return int(nul.sum()), "OK"


def pur_cls(rho):
    p = np.trace(rho @ rho)
    if not np.isfinite(p):
        return "NAO_FINITO", p
    if abs(p - 1) <= PUR_EQ:
        return "=1", p
    if abs(p.imag) <= TOL_ID and p.real <= 1 - PUR_LT:
        return "<1", p
    return "AMBIGUO", p


def agrega(sts):
    if any(s == "NAO_FINITO" for s in sts):
        return "NAO_FINITO"
    if any(s == "VIOLA" for s in sts):
        return "VIOLA"
    if any(s == "AMBIGUO" for s in sts):
        return "AMBIGUO"
    return "OK"


def f(x):
    """numero -> JSON (complexo vira [re, im]; nao finito vira string)."""
    if isinstance(x, (complex, np.complexfloating)):
        if abs(complex(x).imag) == 0.0:
            return f(complex(x).real)
        return [f(complex(x).real), f(complex(x).imag)]
    if isinstance(x, (np.integer, int)) and not isinstance(x, bool):
        return int(x)
    if isinstance(x, (float, np.floating)):
        x = float(x)
        return x if math.isfinite(x) else repr(x)
    if isinstance(x, mp.mpf):
        return mp.nstr(x, 25)
    return x


def mpn(x):
    return mp.nstr(x, 6)


def limpa(o):
    if isinstance(o, dict):
        return {str(k): limpa(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpa(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating, complex, np.complexfloating, mp.mpf)):
        return f(o)
    return o


def limpa_prev(o):
    """a forma que o objeto tem depois de ida e volta pelo JSON (para comparar com a tentativa anterior)."""
    return json.loads(json.dumps(limpa(o), ensure_ascii=False, allow_nan=False))


class Parte:
    def __init__(self, pid):
        self.pid = pid
        self.checks = []
        self.numeros = {}
        self.lados = {}
        self.notas = []
        self.resumo = ""

    def add(self, nome, status, usa_beta=False, **kw):
        if usa_beta and not BETA_OK and status != "NAO_FINITO":
            status = "SEM_CONFERENCIA_BETA"
        rec = dict(nome=nome, status=status, usa_beta=usa_beta)
        for k, v in kw.items():
            rec[k] = f(v) if not isinstance(v, (list, dict, str, bool)) else v
        self.checks.append(rec)
        return status

    def veredito(self):
        sts = [c["status"] for c in self.checks]
        if not sts:
            return "NAO_APLICAVEL_O"
        if any(s == "NAO_FINITO" for s in sts):
            return "SEM_VEREDITO_O"
        if any(s == "VIOLA" for s in sts):
            return "FALHA_O"
        if any(s in ("AMBIGUO", "SEM_CONFERENCIA_BETA") for s in sts):
            return "SEM_VEREDITO_O"
        return "PASSA_O"


PARTES = {}


def nova(pid):
    p = Parte(pid)
    PARTES[pid] = p
    return p


# ------------------------------------------------------------------------------------------------------------------
# 5. os objetos (receita do um.py e do kernel) e as amostras (ordem e distribuicoes: INPUT do construtor)
# ------------------------------------------------------------------------------------------------------------------
P_UM = np.array([[1.0, 0.0], [0.0, 0.0]])        # um.py l.6512: rho* = atrator puro
Q0_UM = np.eye(2) - P_UM                          # um.py l.6514


def Qth_um(th):                                   # um.py l.6517-6518 (R = [[c,-s],[s,c]]; Qth = R Q0 R^T)
    c, s = np.cos(th), np.sin(th)
    R = np.array([[c, -s], [s, c]])
    return R @ Q0_UM @ R.T


I2 = np.eye(2, dtype=complex)
E00 = np.zeros((2, 2), dtype=complex)
E00[0, 0] = 1.0                                   # Matrix.single 0 0 1
Q0C = I2 - E00
GROT = np.array([[0, 1], [-1, 0]], dtype=complex)
E1K = np.array([1, 0], dtype=complex)             # e1 do kernel = ![1, 0] (o modo incidente)


def Smat(th):                                     # TGLExt/SMatrix.lean: Smat = cos*1 + sin*Grot
    return np.cos(th) * I2 + np.sin(th) * GROT


def rhoOut(th):                                   # F_th(1) = S * single 0 0 1 * S^H
    S = Smat(th)
    return S @ E00 @ S.conj().T


def gmat(gamma):                                  # g_ii = 0, g_01 = g_10 = gamma
    return np.array([[0.0, gamma], [gamma, 0.0]])


def dephase(gm, t, x):                            # (D_t x)_ij = e^{-t g_ij} x_ij  (Ergodicity.lean:184)
    return np.exp(-(t * gm)) * np.asarray(x, dtype=complex)


def diagE(x):                                     # D_inf = diagExpect (CondExpect.lean:87)
    return np.diag(np.diag(np.asarray(x, dtype=complex)))


def anti(a, b):
    a = np.asarray(a, dtype=complex)
    b = np.asarray(b, dtype=complex)
    return a @ b + b @ a


TH_VAL = {"0": 0.0, "thM": thM, "-thM": -thM, "3thM": 3 * thM, "pi/6": math.pi / 6, "pi/4": math.pi / 4,
          "pi/3": math.pi / 3, "pi/2": math.pi / 2, "2pi/3": 2 * math.pi / 3, "pi": math.pi, "1.0": 1.0, "2.5": 2.5}
GTH = [(l, TH_VAL[l], "thM" in l) for l in GTH_SPEC]
GAMMAS = [("1", 1.0, False), ("beta", beta, True)]

rng = np.random.default_rng(SEED)


def haar(n):
    Z = (rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))) / math.sqrt(2.0)
    Q, R = np.linalg.qr(Z)
    d = np.diag(R)
    return Q * (d / np.abs(d))[np.newaxis, :]


HAAR = {}
for n, N in ((2, NH2), (3, NH3), (4, NH4)):
    HAAR[n] = [haar(n) for _ in range(N)]
MIX = {}
for n in (2, 3, 4):
    for r in range(2, n + 1):
        lst = []
        for _ in range(NMIX):
            U = haar(n)
            p = rng.uniform(P_LO, P_HI, size=r)
            p = p / p.sum()
            pf = np.concatenate([p, np.zeros(n - r)])
            lst.append(U @ np.diag(pf) @ U.conj().T)
        MIX[(n, r)] = lst
MS = rng.standard_normal((NM, 2, 2)) + 1j * rng.standard_normal((NM, 2, 2))
PSI = {}
for n in (2, 3, 4):
    PSI[n] = [rng.standard_normal(n) + 1j * rng.standard_normal(n) for _ in range(NPSI)]
PROJ = {}
for dd in (1, 2, 3, 4):
    lst = []
    for _ in range(NPROJ):
        U = haar(4)
        V = U[:, :dd]
        lst.append(V @ V.conj().T)
    PROJ[dd] = lst
POOL = {}
for n in (2, 3, 4):
    pool = []
    for k, psi in enumerate(PSI[n]):
        a = psi / np.linalg.norm(psi)
        pool.append(("puro", k, np.outer(a, a.conj())))
    for r in range(2, n + 1):
        for k, rho in enumerate(MIX[(n, r)]):
            pool.append(("misto_posto_%d" % r, k, rho))
    POOL[n] = pool
AMOSTRAS = dict(semente=SEED, haar={2: NH2, 3: NH3, 4: NH4}, mistos_por_n_posto=NMIX, M2x2=NM, psi_por_n=NPSI,
                projecoes_por_d=NPROJ,
                ordem_e_distribuicoes="[INPUT do construtor] ordem das tiragens: Haar n=2,3,4; mistos (n=2..4, posto "
                "2..n; U Haar novo + p ~ U[%g,%g]^posto normalizado); 1000 M (Re, Im ~ N(0,1) por entrada); psi (n=2,3,4; "
                "Re, Im ~ N(0,1)); projecoes (d=1..4; primeiras d colunas de um Haar 4x4 novo). Haar por QR com correcao "
                "de fase de diag(R) [KNOWN, Mezzadri 2007]." % (P_LO, P_HI))
log("amostras:", json.dumps({k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()})
                             for k, v in AMOSTRAS.items()}, ensure_ascii=False))

# ------------------------------------------------------------------------------------------------------------------
# 6. as partes (na ordem do pre-registro)
# ------------------------------------------------------------------------------------------------------------------

# ---------------- P1.a -------------------------------------------------------------------------------------------
P = nova("P1.a")
pre_bad, incons, amb = [], [], []
lados = {"puros (=1, posto 1, idempotente)": 0, "mistos (<1, posto>=2, nao idempotente)": 0}
max_tr, min_eig, max_pur_puro, max_pur_misto, min_sv_misto, max_idem_puro = 0.0, 1.0, 0.0, 0.0, 1.0, 0.0
for n in (2, 3, 4):
    for (tipo, k, rho) in POOL[n]:
        ev = np.linalg.eigvalsh(rho)
        dtr = abs(np.trace(rho) - 1)
        max_tr = max(max_tr, dtr)
        min_eig = min(min_eig, float(ev.min()))
        if ev.min() < -TOL_ID or dtr > TOL_ID:
            pre_bad.append([n, tipo, k])
        pc, pv = pur_cls(rho)
        rk, rc, s = rank_info(rho)
        idem = dev(rho @ rho, rho)
        ic = zcls(idem)
        if "NAO_FINITO" in (pc, rc, ic) or "AMBIGUO" in (pc, rc, ic):
            amb.append([n, tipo, k, pc, rc, ic])
            continue
        if pc == "=1" and rk == 1 and ic == "ZERO":
            lados["puros (=1, posto 1, idempotente)"] += 1
            max_pur_puro = max(max_pur_puro, abs(pv - 1))
            max_idem_puro = max(max_idem_puro, idem)
        elif pc == "<1" and rk >= 2 and ic == "NAO_ZERO":
            lados["mistos (<1, posto>=2, nao idempotente)"] += 1
            max_pur_misto = max(max_pur_misto, pv.real)
            min_sv_misto = min(min_sv_misto, float(s[s >= RK_NON].min()))
        else:
            incons.append([n, tipo, k, pc, rk, ic])
P.add("precondicao: amostras PSD (autovalor >= -TOL_ID) e Tr = 1 (TOL_ID)", "OK" if not pre_bad else "VIOLA",
      n=sum(len(POOL[n]) for n in (2, 3, 4)), violacoes=pre_bad[:10], max_desvio_traco=max_tr, menor_autovalor=min_eig)
st = "NAO_FINITO" if any("NAO_FINITO" in a for a in amb) else ("VIOLA" if incons else ("AMBIGUO" if amb else "OK"))
P.add("Tr rho^2 = 1 <=> posto 1 <=> rho^2 = rho (PUREZA, RANK; idempotencia pela faixa TOL_ZERO)", st,
      inconsistentes=incons[:10], ambiguos=amb[:10])
P.lados = lados
P.numeros = dict(max_desvio_pureza_puros=max_pur_puro, max_pureza_mistos=max_pur_misto,
                 menor_sigma_nao_nulo_mistos=min_sv_misto, max_idempotencia_puros=max_idem_puro)
P.resumo = "n=%d (n=2,3,4): %d puros (=1, posto 1, idem.), %d mistos (<1, posto>=2); max|Tr rho^2-1| puros %.1e; max Tr rho^2 mistos %.4f; inconsistentes %d; ambiguos %d" % (
    sum(len(POOL[n]) for n in (2, 3, 4)), lados["puros (=1, posto 1, idempotente)"],
    lados["mistos (<1, posto>=2, nao idempotente)"], max_pur_puro, max_pur_misto, len(incons), len(amb))

# ---------------- P1.b -------------------------------------------------------------------------------------------
P = nova("P1.b")
ids, viol_id = [], []
for k, M in enumerate(MS):
    trM, trM2, det, fM2 = np.trace(M), np.trace(M @ M), np.linalg.det(M), float(np.sum(np.abs(M) ** 2))
    d = abs(trM2 - (trM ** 2 - 2 * det))
    tol = TOL_ID * (1 + fM2)
    ids.append(d / tol)
    if not (d <= tol):
        viol_id.append([k, d, tol])
P.add("Tr M^2 = (Tr M)^2 - 2 det M em 1000 M gaussianas (TOL_ID*(1+|M|_F^2); det por LU)",
      "NAO_FINITO" if not np.all(np.isfinite(ids)) else ("VIOLA" if viol_id else "OK"),
      n=NM, max_razao_desvio_sobre_tol=max(ids), violacoes=viol_id[:10])
hyp_ok, hyp_fora, concl_viol, amb_b, razoes_det, rk_unscaled, max_fH2, min_sig1 = 0, [], [], [], [], {}, 0.0, 1e300
for k, M in enumerate(MS):
    a, b = M[0, 0], M[0, 1]
    c = (1 - a * a - (1 - a) ** 2) / (2 * b)     # impoe Tr M = 1 e Tr M^2 = 1 sem usar det
    H = np.array([[a, b], [c, 1 - a]])
    fH2 = float(np.sum(np.abs(H) ** 2))
    max_fH2 = max(max_fH2, fH2)
    tol = TOL_ID * (1 + fH2)
    if not (abs(np.trace(H) - 1) <= tol and abs(np.trace(H @ H) - 1) <= tol):
        hyp_fora.append(k)
        continue
    hyp_ok += 1
    detH = np.linalg.det(H)
    razoes_det.append(abs(detH) / tol)
    s = np.linalg.svd(H, compute_uv=False)
    min_sig1 = min(min_sig1, float(s[0]))
    if not np.all(np.isfinite(s)) or not math.isfinite(abs(detH)):
        amb_b.append([k, "NAO_FINITO"])
        continue
    null2, non1 = s[1] <= tol, s[0] >= RK_NON
    if not (s[1] <= tol or s[1] >= RK_NON) or not non1:
        amb_b.append([k, "AMBIGUO", float(s[1]), tol])
        continue
    if not (abs(detH) <= tol and null2 and non1):
        concl_viol.append([k, abs(detH), float(s[1]), tol])
    rku, rcu, _ = rank_info(H)
    rk_unscaled[str(rku if rcu == "OK" else rcu)] = rk_unscaled.get(str(rku if rcu == "OK" else rcu), 0) + 1
P.add("hipotese habitada: Tr M = 1 e Tr M^2 = 1 (TOL_ID escalado)", "OK" if hyp_ok == NM else "VIOLA",
      n_na_hipotese=hyp_ok, fora=hyp_fora[:10])
st = "NAO_FINITO" if any(x[1] == "NAO_FINITO" for x in amb_b) else ("VIOLA" if concl_viol else ("AMBIGUO" if amb_b else "OK"))
P.add("Tr M = Tr M^2 = 1 => det M = 0 e posto 1 (sem positividade; sigma_min <= TOL_ID*(1+|M|_F^2), sigma_max >= 1e-6)",
      st, n=hyp_ok, max_razao_det_sobre_tol=max(razoes_det) if razoes_det else None, violacoes=concl_viol[:10],
      ambiguos=amb_b[:10], posto_com_faixa_RANK_nao_escalada=rk_unscaled, max_norma_F2=max_fH2, menor_sigma_max=min_sig1)
P.resumo = "identidade em %d M: max desvio/tol %.2e; %d M na hipotese (Tr=Tr^2=1): det=0 e posto 1 em todas (max |det|/tol %.2e); faixa RANK nao escalada: %s" % (
    NM, max(ids), hyp_ok, max(razoes_det) if razoes_det else float("nan"), rk_unscaled)

# ---------------- P1.d -------------------------------------------------------------------------------------------
P = nova("P1.d")
rk_bad, rk_amb, maxd = [], [], dict(traco=0.0, idempotencia=0.0, pureza=0.0)
for n in (2, 3, 4):
    for k, psi in enumerate(PSI[n]):
        rk, rc, s = rank_info(np.outer(psi, psi.conj()))
        if rc != "OK":
            rk_amb.append([n, k, rc])
        elif rk != 1:
            rk_bad.append([n, k, rk])
        a = psi / np.linalg.norm(psi)
        rho = np.outer(a, a.conj())
        maxd["traco"] = max(maxd["traco"], abs(np.trace(rho) - 1))
        maxd["idempotencia"] = max(maxd["idempotencia"], dev(rho @ rho, rho))
        maxd["pureza"] = max(maxd["pureza"], abs(np.trace(rho @ rho) - 1))
st = "NAO_FINITO" if any(x[2] == "NAO_FINITO" for x in rk_amb) else ("VIOLA" if rk_bad else ("AMBIGUO" if rk_amb else "OK"))
P.add("psi != 0 (nao normalizado) => posto |psi><psi| = 1 (RANK)", st, n=3 * NPSI, violacoes=rk_bad[:10], ambiguos=rk_amb[:10])
P.add("|psi| = 1 => Tr = 1 (TOL_ID)", st_tol(maxd["traco"], TOL_ID), max_desvio=maxd["traco"])
P.add("|psi| = 1 => idempotente (TOL_ID)", st_tol(maxd["idempotencia"], TOL_ID), max_desvio=maxd["idempotencia"])
P.add("|psi| = 1 => Tr(rho^2) = 1 (TOL_ID)", st_tol(maxd["pureza"], TOL_ID), max_desvio=maxd["pureza"])
P.resumo = "300 psi (n=2,3,4): posto 1 em todos; max desvios Tr %.1e, idem. %.1e, Tr rho^2 %.1e" % (
    maxd["traco"], maxd["idempotencia"], maxd["pureza"])

# ---------------- P2.lit (CITADO) ----------------------------------------------------------------------------------


def localizar(arquivo, padrao):
    b = open(arquivo, "rb").read()
    linhas = b.decode("utf-8").split("\n")
    achou = [i + 1 for i, ln in enumerate(linhas) if re.search(padrao, ln)]
    return dict(arquivo=arquivo, sha256=sha_bytes(b), linhas=achou)


P = nova("P2.lit")
loc = localizar(MATHLIB_RN, r"^theorem finrank_range_add_finrank_ker ")
ns = [i + 1 for i, ln in enumerate(open(MATHLIB_RN, encoding="utf-8").read().split("\n")) if ln.startswith("namespace ")]
P.numeros = dict(citacao=loc, namespaces_do_arquivo=ns,
                 nota="[KNOWN] rank + nulidade = n: Mathlib LinearMap.finrank_range_add_finrank_ker (localizado por grep, "
                      "somente leitura, no .lake do Nos); Axler, LADR, Teo. 3.22. Sem ensaio otico (coluna O '-').")
P.resumo = "CITADO: Mathlib %s l.%s (namespace LinearMap, l.%s)" % (
    os.path.basename(MATHLIB_RN), loc["linhas"], [x for x in ns if x < (loc["linhas"] or [0])[0]][-1:] or "?")
CITACOES = {"P2.lit": bool(loc["linhas"])}

# ---------------- P2.a -------------------------------------------------------------------------------------------
P = nova("P2.a")
tripla = [("rho*", P_UM, (1, 1)), ("I/2", np.eye(2) / 2, (2, 0)), ("0", np.zeros((2, 2)), (0, 2))]
res = {}
sts = []
for nome, A, esp in tripla:
    rk, rc, s = rank_info(A)
    nu, nc = nulidade_info(A)
    res[nome] = dict(posto=rk, nulidade=nu, esperado=list(esp), sigmas=[f(x) for x in s])
    if rc != "OK" or nc != "OK":
        sts.append("AMBIGUO" if "NAO_FINITO" not in (rc, nc) else "NAO_FINITO")
    else:
        sts.append("OK" if (rk, nu) == esp else "VIOLA")
P.add("(posto, nulidade) de rho* = (1,1), I/2 = (2,0), 0 = (0,2) (RANK; nulidade por eigvalsh(A^H A))", agrega(sts),
      valores=res)
P.resumo = "rho* (1,1); I/2 (2,0); 0 (0,2): " + ", ".join("%s=(%s,%s)" % (k, v["posto"], v["nulidade"]) for k, v in res.items())

# ---------------- P2.b -------------------------------------------------------------------------------------------
P = nova("P2.b")
viol_pos, viol_eq, amb2, soma_n, lados = [], [], [], [], {"posto 1 / nulidade n-1": 0, "posto>=2 / nulidade<n-1": 0}
for n in (2, 3, 4):
    for (tipo, k, rho) in POOL[n]:
        rk, rc, _ = rank_info(rho)
        nu, nc = nulidade_info(rho)
        if rc != "OK" or nc != "OK":
            amb2.append([n, tipo, k, rc, nc])
            continue
        if rk < 1:
            viol_pos.append([n, tipo, k, rk])
        if (rk == 1) != (nu == n - 1):
            viol_eq.append([n, tipo, k, rk, nu])
        lados["posto 1 / nulidade n-1" if rk == 1 else "posto>=2 / nulidade<n-1"] += 1
        soma_n.append(rk + nu == n)
st_a = "NAO_FINITO" if any("NAO_FINITO" in x for x in amb2) else ("AMBIGUO" if amb2 else "OK")
P.add("Tr rho = 1 => posto >= 1 (amostras de P1)", "VIOLA" if viol_pos else st_a, n=len(soma_n), violacoes=viol_pos[:10])
P.add("posto = 1 <=> nulidade = n - 1 (posto por SVD; nulidade por eigvalsh)", "VIOLA" if viol_eq else st_a,
      violacoes=viol_eq[:10], ambiguos=amb2[:10])
P.lados = lados
P.numeros = dict(posto_mais_nulidade_igual_n_em_todas=all(soma_n), nota="a soma posto + nulidade = n e P2.lit (CITADO); "
                 "aqui so a sombra numerica, com as duas contagens feitas por rotinas LAPACK diferentes")
P.resumo = "900 estados: posto>=1 em todos; posto 1 <=> nulidade n-1 sem excecao (%d posto 1, %d posto>=2); posto+nulidade=n em todas: %s" % (
    lados["posto 1 / nulidade n-1"], lados["posto>=2 / nulidade<n-1"], all(soma_n))

# ---------------- P3.a -------------------------------------------------------------------------------------------
P = nova("P3.a")
mx = dict(PXP_menos_wP=0.0, TrPX_menos_w=0.0, leitura_normalizada=0.0)
nw, namb, nzero, nviol, prec = 0, 0, 0, [], []
min_absw = 1e300
for n in (2, 3, 4):
    Ps = []
    if n == 2:
        Ps.append(("rho*", np.array([1, 0], dtype=complex), P_UM))
        Ps.append(("Q0", np.array([0, 1], dtype=complex), Q0_UM))
    for k, psi in enumerate(PSI[n]):
        a = psi / np.linalg.norm(psi)
        Ps.append(("psi%d" % k, a, None))
    Xs = [np.eye(n, dtype=complex) / n] + [rho for r in range(2, n + 1) for rho in MIX[(n, r)]]
    Xs = np.array(Xs)
    for nome, a, Pref in Ps:
        Pm = np.outer(a, a.conj())
        if Pref is not None:
            prec.append([nome, dev(Pm, Pref)])
        w = np.einsum("i,kij,j->k", a.conj(), Xs, a)
        PXP = np.einsum("ij,kjl,lm->kim", Pm, Xs, Pm)
        d1 = np.sqrt(np.sum(np.abs(PXP - w[:, None, None] * Pm[None]) ** 2, axis=(1, 2)))
        trPX = np.einsum("ij,kji->k", Pm, Xs)
        d2 = np.abs(trPX - w)
        mx["PXP_menos_wP"] = max(mx["PXP_menos_wP"], float(d1.max()))
        mx["TrPX_menos_w"] = max(mx["TrPX_menos_w"], float(d2.max()))
        for kk in range(len(Xs)):
            c = zcls(abs(w[kk]))
            if c == "NAO_ZERO":
                nw += 1
                min_absw = min(min_absw, abs(w[kk]))
                d3 = dev(PXP[kk] / w[kk], Pm)
                mx["leitura_normalizada"] = max(mx["leitura_normalizada"], d3)
                if not d3 <= TOL_ID:
                    nviol.append([n, nome, kk, d3, abs(w[kk])])
            elif c == "ZERO":
                nzero += 1
            else:
                namb += 1
npares = nw + nzero + namb
P.add("precondicao: P = |a><a| reproduz rho* e Q0 do um.py (TOL_ID)", agrega([st_tol(x[1], TOL_ID) for x in prec]),
      desvios=prec)
P.add("P X P = <a,Xa> P (TOL_ID)", st_tol(mx["PXP_menos_wP"], TOL_ID), n=npares, max_desvio=mx["PXP_menos_wP"])
P.add("Tr(P X) = <a,Xa> (TOL_ID)", st_tol(mx["TrPX_menos_w"], TOL_ID), n=npares, max_desvio=mx["TrPX_menos_w"])
P.add("<a,Xa> != 0 => P X P / <a,Xa> = P (TOL_ID; <a,Xa> pela faixa TOL_ZERO)",
      "VIOLA" if nviol else ("AMBIGUO" if namb else "OK"), n_condicional=nw, n_w_zero=nzero, n_w_ambiguo=namb,
      max_desvio=mx["leitura_normalizada"], menor_abs_w=min_absw, violacoes=nviol[:10])
P.resumo = "%d pares (P em {rho*, Q0, |psi><psi|} x X em {I/n, mistos}, n=2,3,4): max |PXP-<a,Xa>P| %.1e; max |Tr PX-<a,Xa>| %.1e; leitura normalizada max %.1e (min |<a,Xa>| %.2e); violacoes %d" % (
    npares, mx["PXP_menos_wP"], mx["TrPX_menos_w"], mx["leitura_normalizada"], min_absw, len(nviol))

# ---------------- P3.b -------------------------------------------------------------------------------------------
P = nova("P3.b")
X = np.eye(2) / 2
num = P_UM @ X @ P_UM
tr = np.trace(P_UM @ X)
P.add("rho*(I/2)rho*/Tr(rho* I/2) = rho* (TOL_ID)", st_tol(dev(num / tr, P_UM), TOL_ID), desvio=dev(num / tr, P_UM))
P.add("Tr(rho* I/2) = 1/2 (TOL_ID)", st_tol(abs(tr - 0.5), TOL_ID), valor=tr)
rb = np.diag([1 - beta, beta])
Sv = Smat(thM) @ E1K
t2, r2 = abs(Sv[0]) ** 2, abs(Sv[1]) ** 2
v1, v2 = np.trace(P_UM @ rb), np.trace(Q0_UM @ rb)
P.add("b = beta: Tr(rho* rho) = 1 - b (TOL_ID)", st_tol(abs(v1 - (1 - beta)), TOL_ID), True, valor=v1)
P.add("1 - b = |t(thM)|^2 (TOL_ID)", st_tol(abs(v1 - t2), TOL_ID), True, t2=t2, desvio=abs(v1 - t2))
P.add("b = beta: Tr(Q0 rho) = b (TOL_ID)", st_tol(abs(v2 - beta), TOL_ID), True, valor=v2)
P.add("b = |r(thM)|^2 (TOL_ID)", st_tol(abs(v2 - r2), TOL_ID), True, r2=r2, desvio=abs(v2 - r2))
cm, sm = mp.cos(thM_mp), mp.sin(thM_mp)
d_t = abs((1 - beta_mp) - cm ** 2)
d_r = abs(beta_mp - sm ** 2)
P.add("mpmath dps 50: 1 - beta = cos^2 thM e beta = sin^2 thM (1e-40)",
      "OK" if (d_t <= TOL_ID_MP and d_r <= TOL_ID_MP) else "VIOLA", True, desvio_t=mpn(d_t), desvio_r=mpn(d_r))
P.resumo = "rho*(I/2)rho*/Tr = rho* (desvio %.1e), Tr = 1/2; em b = beta: Tr(rho* rho) = 1-beta = |t|^2, Tr(Q0 rho) = beta = |r|^2 (desvios %.1e, %.1e; mpmath %s, %s)" % (
    dev(num / tr, P_UM), abs(v1 - t2), abs(v2 - r2), mpn(d_t), mpn(d_r))

# ---------------- P4 ---------------------------------------------------------------------------------------------
P = nova("P4")
mx4 = dict(idem=0.0, herm=0.0, traco_P=0.0, traco_rho=0.0, indice=0.0)
rk_bad4, amb4, amb4_rk, eq_bad4, lados4 = [], [], [], [], {"d=1: Tr rho^2 = Tr rho": 0, "d>=2: Tr rho^2 != Tr rho": 0}
for dd in (1, 2, 3, 4):
    for k, Pm in enumerate(PROJ[dd]):
        mx4["idem"] = max(mx4["idem"], dev(Pm @ Pm, Pm))
        mx4["herm"] = max(mx4["herm"], dev(Pm, Pm.conj().T))
        rk, rc, _ = rank_info(Pm)
        if rc != "OK":
            amb4_rk.append([dd, k, rc])
        elif rk != dd or rk < 1:
            rk_bad4.append([dd, k, rk])
        mx4["traco_P"] = max(mx4["traco_P"], abs(np.trace(Pm) - dd))
        rho = Pm / dd
        mx4["traco_rho"] = max(mx4["traco_rho"], abs(np.trace(rho) - 1))
        tr2 = np.trace(rho @ rho)
        mx4["indice"] = max(mx4["indice"], abs(tr2 - 1.0 / dd))
        ec = eqcls(tr2, np.trace(rho))
        if ec in ("AMBIGUO", "NAO_FINITO"):
            amb4.append([dd, k, ec])
        elif (ec == "IGUAL") != (dd == 1):
            eq_bad4.append([dd, k, ec])
        else:
            lados4["d=1: Tr rho^2 = Tr rho" if dd == 1 else "d>=2: Tr rho^2 != Tr rho"] += 1
P.add("P^2 = P (TOL_ID)", st_tol(mx4["idem"], TOL_ID), max_desvio=mx4["idem"])
P.add("P = P^H (TOL_ID)", st_tol(mx4["herm"], TOL_ID), max_desvio=mx4["herm"])
P.add("d = posto P >= 1 (RANK)", "NAO_FINITO" if any(x[2] == "NAO_FINITO" for x in amb4_rk) else
      ("VIOLA" if rk_bad4 else ("AMBIGUO" if amb4_rk else "OK")), violacoes=rk_bad4[:10], ambiguos=amb4_rk[:10])
P.add("Tr P = d (TOL_ID)", st_tol(mx4["traco_P"], TOL_ID), max_desvio=mx4["traco_P"])
P.add("Tr rho = 1, o nome (TOL_ID)", st_tol(mx4["traco_rho"], TOL_ID), max_desvio=mx4["traco_rho"])
P.add("Tr rho^2 = 1/d, o indice (TOL_ID)", st_tol(mx4["indice"], TOL_ID), max_desvio=mx4["indice"])
P.add("Tr rho^2 = Tr rho <=> d = 1 (igual <= TOL_ID; diferente >= 1e-6)", "VIOLA" if eq_bad4 else ("AMBIGUO" if amb4 else "OK"),
      violacoes=eq_bad4[:10], ambiguos=amb4[:10])
P.lados = lados4
P.resumo = "200 projecoes (n=4, d=1..4, 50 cada): posto = d; max desvios P^2-P %.1e, Tr P-d %.1e, Tr rho-1 %.1e, Tr rho^2-1/d %.1e; Tr rho^2 = Tr rho so em d = 1 (%d) e diferente em d>=2 (%d)" % (
    mx4["idem"], mx4["traco_P"], mx4["traco_rho"], mx4["indice"], lados4["d=1: Tr rho^2 = Tr rho"], lados4["d>=2: Tr rho^2 != Tr rho"])

# ---------------- B1.a -------------------------------------------------------------------------------------------
P = nova("B1.a")
rk, rc, s = rank_info(P_UM)
P.add("Tr rho* = 1 (TOL_ID)", st_tol(abs(np.trace(P_UM) - 1), TOL_ID), valor=np.trace(P_UM))
P.add("posto rho* = 1 (RANK)", ("OK" if rk == 1 else "VIOLA") if rc == "OK" else rc, sigmas=[f(x) for x in s])
P.add("rho*^2 = rho* (TOL_ID)", st_tol(dev(P_UM @ P_UM, P_UM), TOL_ID), desvio=dev(P_UM @ P_UM, P_UM))
P.add("rho* = rho*^H (TOL_ID)", st_tol(dev(P_UM, P_UM.conj().T), TOL_ID), desvio=dev(P_UM, P_UM.conj().T))
P.add("receita do um.py = termo do kernel (Matrix.single 0 0 1) (TOL_ID)", st_tol(dev(P_UM, E00), TOL_ID), desvio=dev(P_UM, E00))
P.numeros = dict(core_omega_I=CORE_FD["omega_I"], omega_I_aqui=float(np.trace(P_UM)),
                 ancora_igual=(CORE_FD["omega_I"] == float(np.trace(P_UM))))
P.resumo = "Tr rho* = %s; posto 1 (sigmas %s); rho*^2 = rho* = rho*^H exatos; core omega_I = %s" % (
    f(np.trace(P_UM)), [f(x) for x in s], CORE_FD["omega_I"])

# ---------------- B1.b -------------------------------------------------------------------------------------------
P = nova("B1.b")
mxb, amb_b1, viol_b1 = 0.0, [], []
for dd in (1, 2, 3, 4):
    for k, Pm in enumerate(PROJ[dd]):
        rk, rc, _ = rank_info(Pm)
        if rc != "OK":
            amb_b1.append([dd, k, rc])
            continue
        dv = abs(np.trace(Pm) - rk)
        mxb = max(mxb, dv)
        if not dv <= TOL_ID:
            viol_b1.append([dd, k, dv])
P.add("precondicao P^2 = P (TOL_ID) nas projecoes de P4", st_tol(mx4["idem"], TOL_ID), max_desvio=mx4["idem"])
P.add("P^2 = P => Tr P = posto P (TOL_ID; posto por RANK)", "VIOLA" if viol_b1 else ("AMBIGUO" if amb_b1 else "OK"),
      n=4 * NPROJ, max_desvio=mxb, violacoes=viol_b1[:10])
P.resumo = "200 projecoes: max |Tr P - posto P| = %.1e" % mxb

# ---------------- B1.c -------------------------------------------------------------------------------------------
P = nova("B1.c")
U, s, Vh = np.linalg.svd(P_UM.astype(complex))
u0 = U[:, 0]
P.add("vetor singular do sigma nao nulo = +-e0 a menos de fase (TOL_ID)",
      st_tol(max(abs(abs(u0[0]) - 1), abs(u0[1])), TOL_ID), u0=[f(x) for x in u0], sigmas=[f(x) for x in s])
rk, rc, _ = rank_info(P_UM)
proj_range = np.outer(U[:, :rk], U[:, :rk].conj()) if rc == "OK" and rk == 1 else None
P.add("range rho* = span{e0}: projetor sobre a imagem = diag(1,0) (TOL_ID)",
      st_tol(dev(proj_range, E00), TOL_ID) if proj_range is not None else "AMBIGUO")
rk_e0, rc_e0, _ = rank_info(np.array([[1.0], [0.0]]))
P.add("posto rho* = finrank span{e0} = 1 (RANK, mesmo espaco Fin 2 -> C)",
      ("OK" if (rk == 1 and rk_e0 == 1) else "VIOLA") if (rc == "OK" and rc_e0 == "OK") else "AMBIGUO",
      posto_rho=rk, finrank_span_e0=rk_e0)
P.resumo = "u0 = %s (= e0), sigmas %s; projetor da imagem = diag(1,0); posto 1 = finrank span{e0}" % (
    [f(x) for x in u0], [f(x) for x in s])

# ---------------- B2.a -------------------------------------------------------------------------------------------
P = nova("B2.a")
tab, lados = [], {"sin th = 0 e anticomutador = 0": [], "sin th != 0 e anticomutador != 0": []}
for (lbl, th, ub) in GTH:
    s, c = np.sin(th), np.cos(th)
    Q = Qth_um(th)
    Qf = np.array([[s * s, -s * c], [-s * c, c * c]])
    A = anti(Q, P_UM)
    Af = np.array([[2 * s * s, -s * c], [-s * c, 0.0]])
    zc_a, zc_s = zcls(dev(A)), zcls(abs(s))
    P.add("th=%s: Q_th = [[s^2,-sc],[-sc,c^2]] (TOL_ID)" % lbl, st_tol(dev(Q, Qf), TOL_ID), ub, desvio=dev(Q, Qf))
    P.add("th=%s: {Q_th,rho*} = [[2s^2,-sc],[-sc,0]] (TOL_ID)" % lbl, st_tol(dev(A, Af), TOL_ID), ub, desvio=dev(A, Af))
    if "AMBIGUO" in (zc_a, zc_s) or "NAO_FINITO" in (zc_a, zc_s):
        st = "NAO_FINITO" if "NAO_FINITO" in (zc_a, zc_s) else "AMBIGUO"
    else:
        st = "OK" if (zc_a == "ZERO") == (zc_s == "ZERO") else "VIOLA"
        lados["sin th = 0 e anticomutador = 0" if zc_s == "ZERO" else "sin th != 0 e anticomutador != 0"].append(lbl)
    P.add("th=%s: {Q_th,rho*} = 0 <=> sin th = 0 (TOL_ZERO)" % lbl, st, ub, norma_F=dev(A), abs_sin=abs(s))
    P.add("th=%s: Tr = 2s^2 (TOL_ID)" % lbl, st_tol(abs(np.trace(A) - 2 * s * s), TOL_ID), ub)
    P.add("th=%s: soma |.|^2 = 2s^2(1+s^2) (TOL_ID)" % lbl, st_tol(abs(dev(A) ** 2 - 2 * s * s * (1 + s * s)), TOL_ID), ub)
    tab.append([lbl, f(dev(A)), zc_a])
P.lados = lados
P.numeros = dict(tabela_th_normaF_classe=tab)
P.resumo = "G_th: anticomutador nulo so em %s (norma F <= %.1e); nao nulo nos outros %d; formas fechadas, traco 2s^2 e soma 2s^2(1+s^2) na tolerancia" % (
    lados["sin th = 0 e anticomutador = 0"], max(x[1] for x in tab if x[2] == "ZERO"), len(lados["sin th != 0 e anticomutador != 0"]))

# ---------------- B2.b -------------------------------------------------------------------------------------------
P = nova("B2.b")
A = anti(Qth_um(thM), P_UM)
P.add("thM: {Q_thM, rho*} != 0 (TOL_ZERO)", {"NAO_ZERO": "OK", "ZERO": "VIOLA"}.get(zcls(dev(A)), zcls(dev(A))), True, norma_F=dev(A))
P.add("thM: Tr = 2 beta (TOL_ID)", st_tol(abs(np.trace(A) - 2 * beta), TOL_ID), True, desvio=abs(np.trace(A) - 2 * beta))
P.add("thM: soma |.|^2 = 2 beta (1 + beta) (TOL_ID)", st_tol(abs(dev(A) ** 2 - 2 * beta * (1 + beta)), TOL_ID), True,
      desvio=abs(dev(A) ** 2 - 2 * beta * (1 + beta)))
c_mp, s_mp = mp.cos(thM_mp), mp.sin(thM_mp)
R_mp = mp.matrix([[c_mp, -s_mp], [s_mp, c_mp]])
Q0_mp = mp.matrix([[0, 0], [0, 1]])
P_mp = mp.matrix([[1, 0], [0, 0]])
Qth_mp = R_mp * Q0_mp * R_mp.T
A_mp = Qth_mp * P_mp + P_mp * Qth_mp
trA_mp = A_mp[0, 0] + A_mp[1, 1]
fro2_mp = sum(A_mp[i, j] ** 2 for i in range(2) for j in range(2))
d1, d2 = abs(trA_mp - 2 * beta_mp), abs(fro2_mp - 2 * beta_mp * (1 + beta_mp))
P.add("mpmath dps 50: Tr = 2 beta e soma |.|^2 = 2 beta (1+beta) (1e-40)", "OK" if (d1 <= TOL_ID_MP and d2 <= TOL_ID_MP) else "VIOLA",
      True, desvio_traco=mpn(d1), desvio_soma=mpn(d2))
P.resumo = "thM: |{Q,rho*}|_F = %.17g (!= 0); Tr - 2beta = %.1e; soma|.|^2 - 2beta(1+beta) = %.1e; mpmath %s, %s" % (
    dev(A), abs(np.trace(A) - 2 * beta), abs(dev(A) ** 2 - 2 * beta * (1 + beta)), mpn(d1), mpn(d2))

# ---------------- B3.a -------------------------------------------------------------------------------------------
P = nova("B3.a")
mx3 = 0.0
for (lbl, th, ub) in GTH:
    L1 = np.trace(P_UM @ Qth_um(th))
    L2 = np.sin(th) ** 2
    L3 = np.trace(rhoOut(th) @ Q0C)
    L4 = rhoOut(th)[1, 1]
    L5 = abs((Smat(th) @ E1K)[1]) ** 2
    dd = max(abs(L1 - L2), abs(L3 - L2), abs(L4 - L2), abs(L5 - L2))
    mx3 = max(mx3, dd)
    P.add("th=%s: Tr(rho* Q_th) = sin^2 th = Tr(F_th(1) Q0) = (rhoOut th)_11 = |r(th)|^2 (TOL_ID)" % lbl, st_tol(dd, TOL_ID), ub,
          max_desvio=dd, sin2=L2)
P.resumo = "G_th (12 angulos): cadeia de 5 leituras do vazamento, max desvio %.1e" % mx3

# ---------------- B3.b -------------------------------------------------------------------------------------------
P = nova("B3.b")
_P = np.array([[1.0, 0.0], [0.0, 0.0]])
_c, _s = np.cos(thM), np.sin(thM)
_R = np.array([[_c, -_s], [_s, _c]])
_Qth = _R @ (np.eye(2) - _P) @ _R.T
leak = float(np.trace(_P @ _Qth))                 # exatamente a expressao do um.py (l.6519)
P.add("thM: |Tr(rho* Q_thM) - beta| <= TOL_LEAK (float64)", st_tol(abs(leak - beta), TOL_LEAK), True, leak=leak,
      residuo=abs(leak - beta))
leak_mp = (P_mp * Qth_mp)[0, 0] + (P_mp * Qth_mp)[1, 1]
P.add("thM: |Tr(rho* Q_thM) - beta| <= 1e-45 (mpmath dps 50)", "OK" if abs(leak_mp - beta_mp) <= TOL_LEAK_MP else "VIOLA", True,
      residuo=mpn(abs(leak_mp - beta_mp)))
P.numeros = dict(core_leak=CORE_FD["leak_sin2_thetaM"], core_residuo=CORE_FD["leak_equals_beta_residual"],
                 leak_aqui_igual_core=(leak == CORE_FD["leak_sin2_thetaM"]),
                 nota="identidade de thM (sin^2 arcsin sqrt beta = beta): sem poder discriminante (R7; mapa seq 294)")
P.resumo = "leak = %r; |leak-beta| = %.1e (float64; tol %g); mpmath %s (tol %s); = core %r" % (
    leak, abs(leak - beta), TOL_LEAK, mpn(abs(leak_mp - beta_mp)), TOL_LEAK_MP_S, CORE_FD["leak_sin2_thetaM"])

# ---------------- B3.d -------------------------------------------------------------------------------------------
P = nova("B3.d")
dop = abs(beta - float(OP_NUM_S))
P.add("|beta - numero do operador (V4 l.16)| <= CONF_OPERADOR", st_tol(dop, CONF_OP_TOL), True, desvio=dop, tol=CONF_OP_TOL,
      numero_do_operador=OP_NUM_S)
P.resumo = "|beta - %s| = %.3e <= %g" % (OP_NUM_S, dop, CONF_OP_TOL)

# ---------------- B4.a -------------------------------------------------------------------------------------------
P = nova("B4.a")
mxu = dict(unitariedade=0.0, traco=0.0, idem=0.0, herm=0.0, traco_rhostar=0.0)
rk_v, amb_u, rk_v_P, rk_star = [], [], [], []
amb_uP, amb_us = [], []
nproj_tot = 0
for n in (2, 3, 4):
    projs = [np.outer(p / np.linalg.norm(p), (p / np.linalg.norm(p)).conj()) for p in PSI[n]]
    if n == 2:
        projs = [P_UM.astype(complex), Q0_UM.astype(complex)] + projs
    if n == 4:
        projs = projs + [Pm for dd in (1, 2, 3, 4) for Pm in PROJ[dd]]
    for k, u in enumerate(HAAR[n]):
        mxu["unitariedade"] = max(mxu["unitariedade"], dev(u.conj().T @ u, np.eye(n)))
        _, _, rho = POOL[n][k % len(POOL[n])]
        Y = u @ rho @ u.conj().T
        mxu["traco"] = max(mxu["traco"], abs(np.trace(Y) - np.trace(rho)))
        r1, c1, _ = rank_info(rho)
        r2, c2, _ = rank_info(Y)
        if c1 != "OK" or c2 != "OK":
            amb_u.append([n, k, c1, c2])
        elif r1 != r2:
            rk_v.append([n, k, r1, r2])
        Pm = projs[k % len(projs)]
        Z = u @ Pm @ u.conj().T
        nproj_tot += 1
        mxu["idem"] = max(mxu["idem"], dev(Z @ Z, Z))
        mxu["herm"] = max(mxu["herm"], dev(Z, Z.conj().T))
        r3, c3, _ = rank_info(Pm)
        r4, c4, _ = rank_info(Z)
        if c3 != "OK" or c4 != "OK":
            amb_uP.append([n, k, c3, c4])
        elif r3 != r4:
            rk_v_P.append([n, k, r3, r4])
        if n == 2:
            Ys = u @ P_UM @ u.conj().T
            mxu["traco_rhostar"] = max(mxu["traco_rhostar"], abs(np.trace(Ys) - 1))
            r5, c5, _ = rank_info(Ys)
            if c5 != "OK":
                amb_us.append([n, k, "rho*", c5])
            elif r5 != 1:
                rk_star.append([k, r5])


def st_amb(viol, ambs):
    if any("NAO_FINITO" in x for x in ambs):
        return "NAO_FINITO"
    return "VIOLA" if viol else ("AMBIGUO" if ambs else "OK")


P.add("precondicao: u^H u = 1 (TOL_ID)", st_tol(mxu["unitariedade"], TOL_ID), n=NH2 + NH3 + NH4, max_desvio=mxu["unitariedade"])
P.add("Tr(u rho u^H) = Tr rho (TOL_ID)", st_tol(mxu["traco"], TOL_ID), max_desvio=mxu["traco"])
P.add("posto(u rho u^H) = posto rho (RANK)", st_amb(rk_v, amb_u), violacoes=rk_v[:10], ambiguos=amb_u[:10])
P.add("u P u^H e projecao: idempotente (TOL_ID)", st_tol(mxu["idem"], TOL_ID), n=nproj_tot, max_desvio=mxu["idem"])
P.add("u P u^H e projecao: hermitiana (TOL_ID)", st_tol(mxu["herm"], TOL_ID), max_desvio=mxu["herm"])
P.add("posto(u P u^H) = posto P (RANK)", st_amb(rk_v_P, amb_uP), violacoes=rk_v_P[:10], ambiguos=amb_uP[:10])
P.add("n=2, em rho*: Tr(u rho* u^H) = 1 (TOL_ID) e posto 1 (RANK)",
      "VIOLA" if (rk_star or not mxu["traco_rhostar"] <= TOL_ID) else st_amb([], amb_us),
      max_desvio_traco=mxu["traco_rhostar"], violacoes_posto=rk_star[:10], ambiguos=amb_us[:10])
P.resumo = "1400 unitarios Haar (n=2:1000, 3:200, 4:200): max desvios u^Hu-1 %.1e, Tr %.1e, (uPu^H)^2-uPu^H %.1e, herm. %.1e; posto preservado sem excecao; rho*: Tr 1 (%.1e), posto 1" % (
    mxu["unitariedade"], mxu["traco"], mxu["idem"], mxu["herm"], mxu["traco_rhostar"])

# ---------------- B4.b -------------------------------------------------------------------------------------------
P = nova("B4.b")
tab = []
for (lbl, th, ub) in GTH:
    F = rhoOut(th)
    rk, rc, s = rank_info(F)
    pc, pv = pur_cls(F)
    P.add("th=%s: posto rhoOut = 1 (RANK)" % lbl, ("OK" if rk == 1 else "VIOLA") if rc == "OK" else rc, ub, sigmas=[f(x) for x in s])
    P.add("th=%s: Tr = 1 (TOL_ID)" % lbl, st_tol(abs(np.trace(F) - 1), TOL_ID), ub)
    P.add("th=%s: idempotente (TOL_ID)" % lbl, st_tol(dev(F @ F, F), TOL_ID), ub)
    P.add("th=%s: hermitiana (TOL_ID)" % lbl, st_tol(dev(F, F.conj().T), TOL_ID), ub)
    P.add("th=%s: pureza 1 (PUREZA)" % lbl, {"=1": "OK", "<1": "VIOLA"}.get(pc, pc), ub, pureza=pv)
    tab.append([lbl, rk, f(pv)])
P.numeros = dict(tabela_th_posto_pureza=tab)
P.resumo = "G_th: rhoOut com posto 1, Tr 1, idempotente, hermitiana, pureza 1 nos 12 angulos"

# ---------------- B5.a -------------------------------------------------------------------------------------------
P = nova("B5.a")
lados, tab = {"sin 2th = 0: posto 1, pureza 1": [], "sin 2th != 0: posto 2, pureza < 1": []}, []
for (lbl, th, ub) in GTH:
    s, c = np.sin(th), np.cos(th)
    E = diagE(rhoOut(th))
    P.add("th=%s: D_inf F_th(1) = diag(c^2, s^2) (TOL_ID)" % lbl, st_tol(dev(E, np.diag([c * c, s * s])), TOL_ID), ub)
    P.add("th=%s: Tr = 1 (TOL_ID)" % lbl, st_tol(abs(np.trace(E) - 1), TOL_ID), ub)
    rk, rc, sv_ = rank_info(E)
    zc = zcls(abs(np.sin(2 * th)))
    pc, pv = pur_cls(E)
    if "NAO_FINITO" in (rc, zc, pc):
        st1 = st2 = "NAO_FINITO"
    elif "AMBIGUO" in (rc, zc, pc):
        st1 = st2 = "AMBIGUO"
    else:
        st1 = "OK" if (rk == 2) == (zc == "NAO_ZERO") and rk in (1, 2) else "VIOLA"
        st2 = "OK" if (pc == "<1") == (zc == "NAO_ZERO") else "VIOLA"
        lados["sin 2th != 0: posto 2, pureza < 1" if zc == "NAO_ZERO" else "sin 2th = 0: posto 1, pureza 1"].append(lbl)
    P.add("th=%s: posto 2 <=> sin 2th != 0 (senao 1) (RANK, TOL_ZERO)" % lbl, st1, ub, posto=rk, abs_sin2th=abs(np.sin(2 * th)))
    P.add("th=%s: pureza = 1 - 2s^2c^2 (TOL_ID)" % lbl, st_tol(abs(pv - (1 - 2 * s * s * c * c)), TOL_ID), ub)
    P.add("th=%s: pureza < 1 <=> sin 2th != 0 (PUREZA, TOL_ZERO)" % lbl, st2, ub, pureza=pv)
    tab.append([lbl, rk, f(pv)])
P.lados = lados
P.numeros = dict(tabela_th_posto_pureza=tab)
P.resumo = "G_th: posto 1 e pureza 1 em %s (sin 2th = 0); posto 2 e pureza < 1 nos outros %d; diag(c^2,s^2) e Tr 1 na tolerancia" % (
    lados["sin 2th = 0: posto 1, pureza 1"], len(lados["sin 2th != 0: posto 2, pureza < 1"]))

# ---------------- B5.b -------------------------------------------------------------------------------------------
P = nova("B5.b")
E = diagE(rhoOut(thM))
P.add("thM: D_inf F_thM(1) = diag(1 - beta, beta) (TOL_ID)", st_tol(dev(E, np.diag([1 - beta, beta])), TOL_ID), True,
      desvio=dev(E, np.diag([1 - beta, beta])))
rk, rc, sv_ = rank_info(E)
P.add("thM: posto 2 (RANK)", ("OK" if rk == 2 else "VIOLA") if rc == "OK" else rc, True, sigmas=[f(x) for x in sv_])
pc, pv = pur_cls(E)
P.add("thM: pureza = 1 - 2 beta (1 - beta) (TOL_ID)", st_tol(abs(pv - (1 - 2 * beta * (1 - beta))), TOL_ID), True, pureza=pv)
P.add("thM: pureza < 1 (PUREZA)", {"<1": "OK", "=1": "VIOLA"}.get(pc, pc), True)
E_mp00, E_mp11 = mp.cos(thM_mp) ** 2, mp.sin(thM_mp) ** 2
d0, d1_ = abs(E_mp00 - (1 - beta_mp)), abs(E_mp11 - beta_mp)
pur_mp = E_mp00 ** 2 + E_mp11 ** 2
d2_ = abs(pur_mp - (1 - 2 * beta_mp * (1 - beta_mp)))
P.add("mpmath dps 50: diag(cos^2, sin^2)(thM) = diag(1-beta, beta) e pureza 1 - 2beta(1-beta) (1e-40)",
      "OK" if max(d0, d1_, d2_) <= TOL_ID_MP else "VIOLA", True, desvios=[mpn(d0), mpn(d1_), mpn(d2_)],
      pureza_mp=mp.nstr(pur_mp, 30))
bords = []
for bl, b in (("0", 0.0), ("1", 1.0)):
    rkb, rcb, _ = rank_info(np.diag([1 - b, b]))
    bords.append([bl, rkb])
    P.add("borda b=%s: posto diag(1-b, b) = 1 (RANK)" % bl, ("OK" if rkb == 1 else "VIOLA") if rcb == "OK" else rcb)
P.resumo = "thM: diag(1-beta, beta) (desvio %.1e), posto 2 (sigmas %s), pureza %.16g = 1-2beta(1-beta) (< 1); mpmath max desvio %s; bordas b=0, b=1: posto 1" % (
    dev(E, np.diag([1 - beta, beta])), [f(x) for x in sv_], pv.real, mpn(max(d0, d1_, d2_)))

# ---------------- B5.c -------------------------------------------------------------------------------------------
P = nova("B5.c")
s, c = math.sin(thM), math.cos(thM)
F = rhoOut(thM)
tab = []
for (gl, gv, gb) in GAMMAS:
    G = gmat(gv)
    prev = None
    for t in GT:
        Xt = dephase(G, t, F)
        detX = np.linalg.det(Xt)
        det_ref = c * c * s * s * (1 - math.exp(-t * (gv + gv)))
        rk, rc, sv_ = rank_info(Xt)
        esp = 2 if t > 0 else 1
        pu = float(np.trace(Xt @ Xt).real)
        P.add("gamma=%s t=%g: det = c^2 s^2 (1 - e^{-t(g01+g10)}) (TOL_ID)" % (gl, t), st_tol(abs(detX - det_ref), TOL_ID), True,
              desvio=abs(detX - det_ref))
        P.add("gamma=%s t=%g: posto = %d (RANK)" % (gl, t, esp), ("OK" if rk == esp else "VIOLA") if rc == "OK" else rc, True,
              sigma_min=float(sv_.min()))
        P.add("gamma=%s t=%g: traco preservado (TOL_ID)" % (gl, t), st_tol(abs(np.trace(Xt) - 1), TOL_ID), True)
        okp = pu <= 1 + TOL_ID and (prev is None or pu <= prev + TOL_ID)
        P.add("gamma=%s t=%g: pureza nao cresce (<= 1 e <= a do t anterior, folga TOL_ID)" % (gl, t), "OK" if okp else "VIOLA", True, pureza=pu)
        prev = pu
        tab.append([gl, t, rk, f(float(sv_.min())), pu])
P.numeros = dict(tabela_gamma_t_posto_sigmamin_pureza=tab)
P.resumo = "thM x gamma{1,beta} x G_t: posto 1 em t=0 e 2 em todo t>0 (menor sigma_min com t>0: %.3e em gamma=beta, t=0.5); det na forma fechada; traco 1; pureza nao cresce (de 1 a %.16g)" % (
    min(x[3] for x in tab if x[1] > 0), min(x[4] for x in tab))

# ---------------- B5.e(i) ----------------------------------------------------------------------------------------
P = nova("B5.e(i)")
for ck in PARTES["B4.b"].checks:
    if "posto rhoOut" in ck["nome"]:
        P.add(ck["nome"] + " [= B4.b]", ck["status"], ck["usa_beta"])
P.resumo = "= B4.b: F_th(1) = rhoOut th tem posto 1 nos 12 angulos de G_th"

# ---------------- B5.e(ii) (FALHA pre-registrada) ----------------------------------------------------------------
P = nova("B5.e(ii)")
r_end, c_end, _ = rank_info(diagE(rhoOut(thM)))
r_F, c_F, _ = rank_info(rhoOut(thM))
if c_end != "OK" or c_F != "OK":
    st = "AMBIGUO"
else:
    st = "OK" if r_end == r_F else "VIOLA"
P.add("enunciado universal no falsificador pre-registrado th = thM: posto D_inf F = posto F", st, True,
      posto_D_inf_F=r_end, posto_F=r_F)
scan = []
for (lbl, th, ub) in GTH:
    a_, ac, _ = rank_info(diagE(rhoOut(th)))
    b_, bc, _ = rank_info(rhoOut(th))
    scan.append([lbl, a_, b_])
P.numeros = dict(varredura_G_th_posto_endpoint_posto_F=scan,
                 nota="sobrevive o TRACO (Tr = 1 antes e depois), nao o posto (1 -> 2 onde sin 2th != 0)")
P.resumo = "thM: posto D_inf F = %s != posto F = %s -> o 'para todo th' cai (negativo honesto); igualdade so em %s" % (
    r_end, r_F, [x[0] for x in scan if x[1] == x[2]])

# ---------------- B6.a -------------------------------------------------------------------------------------------
P = nova("B6.a")
mx6, var_t = 0.0, 0.0
for (lbl, th, ub) in GTH:
    s2 = np.sin(th) ** 2
    Q = Qth_um(th)
    vals = []
    for (gl, gv, gb) in GAMMAS:
        for t in GT:
            v = np.trace(P_UM @ dephase(gmat(gv), t, Q))
            vals.append(v)
            mx6 = max(mx6, abs(v - s2))
    dvar = max(abs(v - vals[0]) for v in vals)
    var_t = max(var_t, dvar)
    P.add("th=%s: Tr(rho* D_t Q_th) = sin^2 th para todo t em G_t, gamma em {1,beta} (TOL_ID)" % lbl,
          st_tol(max(abs(v - s2) for v in vals), TOL_ID), True, max_desvio=max(abs(v - s2) for v in vals), variacao_em_t=dvar)
P.resumo = "G_th x G_t x gamma (168 pontos): max |Tr(rho* D_t Q_th) - sin^2 th| = %.1e; variacao em t %.1e" % (mx6, var_t)

# ---------------- B6.b -------------------------------------------------------------------------------------------
P = nova("B6.b")
s, c = np.sin(thM), np.cos(thM)
Q = Qth_um(thM)
mxa = 0.0
for (gl, gv, gb) in GAMMAS:
    for t in GT:
        A = anti(dephase(gmat(gv), t, Q), P_UM)
        e = math.exp(-t * gv)
        Af = np.array([[2 * s * s, -e * s * c], [-e * s * c, 0.0]])
        mxa = max(mxa, dev(A, Af))
        P.add("thM gamma=%s t=%g: {D_t Q_th, rho*} = [[2s^2,-e^{-t g01}sc],[-e^{-t g10}sc,0]] (TOL_ID)" % (gl, t),
              st_tol(dev(A, Af), TOL_ID), True)
        zc = zcls(dev(A))
        P.add("thM gamma=%s t=%g: != 0 (sin thM != 0) (TOL_ZERO)" % (gl, t), {"NAO_ZERO": "OK", "ZERO": "VIOLA"}.get(zc, zc), True,
              norma_F=dev(A))
Ainf = anti(diagE(Q), P_UM)
P.add("thM: {D_inf Q_th, rho*} = diag(2 beta, 0) (TOL_ID)", st_tol(dev(Ainf, np.diag([2 * beta, 0.0])), TOL_ID), True,
      desvio=dev(Ainf, np.diag([2 * beta, 0.0])))
Ainf_mp = 2 * mp.sin(thM_mp) ** 2
P.add("mpmath dps 50: (D_inf)_00 = 2 sin^2 thM = 2 beta (1e-40)", "OK" if abs(Ainf_mp - 2 * beta_mp) <= TOL_ID_MP else "VIOLA",
      True, desvio=mpn(abs(Ainf_mp - 2 * beta_mp)))
P.resumo = "thM x gamma x G_t: forma fechada (max desvio %.1e), nao nulo em todos; D_inf: diag(2beta, 0) (desvio %.1e; mpmath %s)" % (
    mxa, dev(Ainf, np.diag([2 * beta, 0.0])), mpn(abs(Ainf_mp - 2 * beta_mp)))

# ---------------- B7.a1 ------------------------------------------------------------------------------------------
P = nova("B7.a1")
mx7 = dict(potencia=0.0, peso=0.0)
for (lbl, th, ub) in GTH:
    S = Smat(th)
    for n in N_PASSAGENS:
        Sn = np.linalg.matrix_power(S, n)
        d_pow = dev(Sn, Smat(n * th))
        d_w = abs(abs((Sn @ E1K)[1]) ** 2 - np.sin(n * th) ** 2)
        mx7["potencia"] = max(mx7["potencia"], d_pow / n)
        mx7["peso"] = max(mx7["peso"], d_w / n)
        P.add("th=%s n=%d: S(th)^n = S(n th) (TOL_ID*n)" % (lbl, n), st_tol(d_pow, TOL_ID * n), ub, desvio=d_pow)
        P.add("th=%s n=%d: peso refletido |(S^n e1)_1|^2 = sin^2(n th) (TOL_ID*n)" % (lbl, n), st_tol(d_w, TOL_ID * n), ub, desvio=d_w)
P.resumo = "G_th x n em %s: max desvio/n potencia %.1e, peso %.1e" % (N_PASSAGENS, mx7["potencia"], mx7["peso"])

# ---------------- B7.a2 ------------------------------------------------------------------------------------------
P = nova("B7.a2")
nn = np.arange(OSC_N, dtype=np.float64)
a_seq = np.sin(nn * thM) ** 2
win = sliding_window_view(a_seq, W_OSC)
osc = win.max(axis=1) - win.min(axis=1)
cota = math.cos(thM) - OSC_SLACK
k_min = int(osc.argmin())
P.add("thM: toda janela de W termos (inicio em [0, N-W]) tem max - min >= cos thM - folga (OSC)",
      ("OK" if float(osc.min()) >= cota else "VIOLA") if np.all(np.isfinite(osc)) else "NAO_FINITO", True,
      W=W_OSC, N=OSC_N, n_janelas=len(osc), menor_oscilacao=float(osc.min()), janela_do_minimo=k_min, cota=cota)
nn2 = np.arange(OSC_N + 1, dtype=np.float64)
z_pi = float((np.sin(nn2 * math.pi) ** 2).max())
z_0 = float((np.sin(nn2 * 0.0) ** 2).max())
P.add("sin th = 0 => constante 0: th = pi e th = 0, n <= 1e5 (<= 1e-10, a cota de C11)",
      "OK" if (z_pi <= 1e-10 and z_0 <= 1e-10) else "VIOLA", max_pi=z_pi, max_0=z_0)
P.numeros = dict(nota="cota exata: em W >= pi/thM + 2 termos ha um n th a menos de thM/2 de um maximo e de um minimo de sin^2; "
                      "max - min >= cos^2(thM/2) - sin^2(thM/2) = cos thM [DERIVED]")
P.resumo = "thM: %d janelas de W=%d; menor oscilacao %.15f >= cota %.15f (cos thM - 1e-9); th = pi: max sin^2(n pi) = %.2e (n <= 1e5)" % (
    len(osc), W_OSC, float(osc.min()), cota, z_pi)

# ---------------- B7.b (CITADO_REAL; sombra otica) -----------------------------------------------------------------
P = nova("B7.b")
loc = localizar(os.path.join(TGLEXT, "Ergodicity.lean"), r"^theorem dephase_tendsto_expectation ")
CITACOES["B7.b"] = bool(loc["linhas"])
sts, mxr, mxs = [], 0.0, 0.0
for xl, x in (("F_thM(1)", rhoOut(thM)), ("Q_thM", Qth_um(thM).astype(complex))):
    d0 = dev(x, diagE(x))
    for (gl, gv, gb) in GAMMAS:
        for t in GT:
            dt = dev(dephase(gmat(gv), t, x), diagE(x))
            ref = d0 * math.exp(-gv * t)
            r_ = abs(dt - ref) / ref if ref > 0 else (0.0 if dt == 0 else float("inf"))
            mxr = max(mxr, r_)
            sts.append("OK" if abs(dt - ref) <= TOL_REL * abs(ref) else "VIOLA")
        for t1 in GT:
            for t2 in GT:
                lhs = dephase(gmat(gv), t1 + t2, x)
                rhs = dephase(gmat(gv), t1, dephase(gmat(gv), t2, x))
                mxs = max(mxs, dev(lhs, rhs))
P.add("sombra: |D_t x - D_inf x|_F = |x - D_inf x|_F e^{-gamma t} (TOL_REL), x em {F_thM(1), Q_thM}", agrega(sts), True,
      max_desvio_relativo=mxr)
P.add("sombra: lei de semigrupo D_{s+t} = D_s D_t em G_t x G_t (TOL_ID)", st_tol(mxs, TOL_ID), True, max_desvio=mxs)
P.numeros = dict(citacao=loc)
P.resumo = "CITADO_REAL: Ergodicity.lean l.%s (dephase_tendsto_expectation); sombra otica coerente: decaimento max desvio relativo %.1e; semigrupo %.1e" % (
    loc["linhas"], mxr, mxs)

# ---------------- B7.c (CITADO_REAL) -------------------------------------------------------------------------------
P = nova("B7.c")
jones = os.path.join(TGLEXT, "IALDJones.lean")
locs = {nm: localizar(jones, rx)["linhas"] for nm, rx in (
    ("spin", r"^noncomputable def spin "), ("orbit_tendsto_center", r"^theorem orbit_tendsto_center "),
    ("angular_orbit_no_limit", r"^theorem angular_orbit_no_limit "), ("angular_orbit_periodic", r"^theorem angular_orbit_periodic "))}
CITACOES["B7.c"] = all(locs.values())
P.numeros = dict(citacao=dict(arquivo=jones, sha256=sha_arq(jones)[1], linhas=locs))
P.resumo = "CITADO_REAL: IALDJones.lean %s (coluna O '-'; sombra suplementar no anexo)" % locs

# ---------------- B8.a -------------------------------------------------------------------------------------------
P = nova("B8.a")
Q0t = Qth_um(0.0)
P.add("th=0: Q_0 pela receita do um.py = Q0 (TOL_ID)", st_tol(dev(Q0t, Q0_UM), TOL_ID))
P.add("th=0: Tr(rho* Q0) = 0 (TOL_ID)", st_tol(abs(np.trace(P_UM @ Q0t)), TOL_ID))
P.add("th=0: {Q0, rho*} = 0 (TOL_ID)", st_tol(dev(anti(Q0t, P_UM)), TOL_ID))
P.add("th=0: F_0(1) = rho* (TOL_ID)", st_tol(dev(rhoOut(0.0), P_UM), TOL_ID))
mx8 = max(dev(dephase(gmat(gv), t, P_UM), P_UM) for (gl, gv, gb) in GAMMAS for t in GT)
P.add("th=0: D_t rho* = rho* para todo t em G_t, gamma em {1,beta} (TOL_ID)", st_tol(mx8, TOL_ID), True, max_desvio=mx8)
rk, rc, _ = rank_info(rhoOut(0.0))
P.add("th=0: posto 1 (RANK)", ("OK" if rk == 1 else "VIOLA") if rc == "OK" else rc)
P.add("th=0: pureza 1 (TOL_ID)", st_tol(abs(np.trace(rhoOut(0.0) @ rhoOut(0.0)) - 1), TOL_ID))
P.resumo = "th = 0 exato: Tr(rho* Q0) = 0, {Q0,rho*} = 0, F_0(1) = rho* = D_t rho* (max desvio %.1e), posto 1, pureza 1" % mx8


# ---------------- D atua (exists t em G_t, gamma em {1, beta}) -----------------------------------------------------
def D_atua(th):
    F = rhoOut(th)
    cl = [zcls(dev(dephase(gmat(gv), t, F), F)) for (gl, gv, gb) in GAMMAS for t in GT]
    if "NAO_FINITO" in cl:
        return "NAO_FINITO", cl
    if "NAO_ZERO" in cl:
        return "ATUA", cl
    if all(x == "ZERO" for x in cl):
        return "NAO_ATUA", cl
    return "AMBIGUO", cl


DA = {lbl: D_atua(th)[0] for (lbl, th, ub) in GTH}

# ---------------- B8.b -------------------------------------------------------------------------------------------
P = nova("B8.b")
lados = {"sin 2th = 0 e D nao atua": [], "sin 2th != 0 e D atua": []}
for (lbl, th, ub) in GTH:
    zc = zcls(abs(np.sin(2 * th)))
    da = DA[lbl]
    if "NAO_FINITO" in (zc, da):
        st = "NAO_FINITO"
    elif "AMBIGUO" in (zc, da):
        st = "AMBIGUO"
    else:
        st = "OK" if (da == "NAO_ATUA") == (zc == "ZERO") else "VIOLA"
        lados["sin 2th = 0 e D nao atua" if zc == "ZERO" else "sin 2th != 0 e D atua"].append(lbl)
    P.add("th=%s: (para todo t, D_t F = F) <=> sin 2th = 0 (TOL_ZERO)" % lbl, st, True, D=da, abs_sin2th=abs(np.sin(2 * th)))
for lbl in lados["sin 2th = 0 e D nao atua"]:
    th = TH_VAL[lbl]
    r1, c1, _ = rank_info(rhoOut(th))
    r2, c2, _ = rank_info(diagE(rhoOut(th)))
    P.add("th=%s (beta = %s): posto 1 em F e em D_inf F (RANK)" % (lbl, "0" if abs(np.sin(th)) < 0.5 else "1"),
          ("OK" if (r1, r2) == (1, 1) else "VIOLA") if (c1, c2) == ("OK", "OK") else "AMBIGUO")
P.lados = lados
P.resumo = "G_th: D nao atua exatamente em %s (sin 2th = 0; posto 1 em F e D_inf F), atua nos outros %d" % (
    lados["sin 2th = 0 e D nao atua"], len(lados["sin 2th != 0 e D atua"]))

# ---------------- B9.a (FALHA pre-registrada) ----------------------------------------------------------------------
P = nova("B9.a")
cex = [lbl for (lbl, th, ub) in GTH if zcls(np.cos(th) ** 2) == "NAO_ZERO" and DA[lbl] == "NAO_ATUA"]
h0, d0_ = zcls(np.cos(0.0) ** 2), DA["0"]
st = ("VIOLA" if (h0 == "NAO_ZERO" and d0_ == "NAO_ATUA") else ("OK" if d0_ == "ATUA" else "AMBIGUO"))
P.add("enunciado literal no falsificador pre-registrado th = 0: |t|^2 = cos^2 th > 0 => D atua", st, True,
      cos2=np.cos(0.0) ** 2, D=d0_)
P.numeros = dict(contraexemplos_em_G_th=cex)
P.resumo = "th = 0: |t|^2 = 1 > 0 e D nao atua -> o 'para todo th' literal cai (negativo honesto); contraexemplos em G_th: %s" % cex

# ---------------- B9.a' (FALHA pre-registrada, controle) -----------------------------------------------------------
P = nova("B9.a'")
cex2 = [lbl for (lbl, th, ub) in GTH if zcls(np.sin(th) ** 2) == "NAO_ZERO" and DA[lbl] == "NAO_ATUA"]
h1, d1x = zcls(np.sin(math.pi / 2) ** 2), DA["pi/2"]
st = ("VIOLA" if (h1 == "NAO_ZERO" and d1x == "NAO_ATUA") else ("OK" if d1x == "ATUA" else "AMBIGUO"))
P.add("enunciado simetrico no falsificador pre-registrado th = pi/2: |r|^2 = sin^2 th > 0 => D atua", st, True,
      sin2=np.sin(math.pi / 2) ** 2, D=d1x, norma_F_coerencia=dev(rhoOut(math.pi / 2) - diagE(rhoOut(math.pi / 2))))
P.numeros = dict(contraexemplos_em_G_th=cex2)
P.resumo = "th = pi/2: |r|^2 = 1 > 0 e D nao atua -> o 'para todo th' simetrico cai (controle); contraexemplos em G_th: %s" % cex2

# ---------------- B9.b -------------------------------------------------------------------------------------------
P = nova("B9.b")
lados = {"|t|^2 > 0 e |r|^2 > 0 e D atua": [], "|t|^2 = 0 ou |r|^2 = 0 e D nao atua": []}
for (lbl, th, ub) in GTH:
    ct, cr, da = zcls(np.cos(th) ** 2), zcls(np.sin(th) ** 2), DA[lbl]
    if "NAO_FINITO" in (ct, cr, da):
        st = "NAO_FINITO"
    elif "AMBIGUO" in (ct, cr, da):
        st = "AMBIGUO"
    else:
        rhs = (ct == "NAO_ZERO" and cr == "NAO_ZERO")
        st = "OK" if (da == "ATUA") == rhs else "VIOLA"
        lados["|t|^2 > 0 e |r|^2 > 0 e D atua" if rhs else "|t|^2 = 0 ou |r|^2 = 0 e D nao atua"].append(lbl)
    P.add("th=%s: D atua <=> |t|^2 > 0 e |r|^2 > 0 (TOL_ZERO)" % lbl, st, True, D=da)
P.add("thM: D atua", "OK" if DA["thM"] == "ATUA" else ("VIOLA" if DA["thM"] == "NAO_ATUA" else DA["thM"]), True)
E11 = diagE(rhoOut(thM))[1, 1]
P.add("thM: (D_inf F(1))_11 = beta (TOL_ID)", st_tol(abs(E11 - beta), TOL_ID), True, desvio=abs(E11 - beta))
P.add("thM: (D_inf F(1))_11 = beta (mpmath, 1e-40)", "OK" if abs(mp.sin(thM_mp) ** 2 - beta_mp) <= TOL_ID_MP else "VIOLA", True,
      desvio=mpn(abs(mp.sin(thM_mp) ** 2 - beta_mp)))
P.lados = lados
P.resumo = "G_th: D atua exatamente onde |t|^2 > 0 e |r|^2 > 0 (%d angulos); nao atua em %s; thM: atua e (D_inf F)_11 - beta = %.1e" % (
    len(lados["|t|^2 > 0 e |r|^2 > 0 e D atua"]), lados["|t|^2 = 0 ou |r|^2 = 0 e D nao atua"], abs(E11 - beta))

# ---------------- B9.c (CITADO_REAL) -------------------------------------------------------------------------------
P = nova("B9.c")
loc = localizar(os.path.join(TGLEXT, "TheVerbSelectsTheAction.lean"), r"^theorem transmission_dephases ")
CITACOES["B9.c"] = bool(loc["linhas"])
P.numeros = dict(citacao=loc)
P.resumo = "CITADO_REAL: TheVerbSelectsTheAction.lean l.%s (transmission_dephases; coluna O '-'; sombra suplementar no anexo)" % loc["linhas"]

# ---------------- O1, O2 -----------------------------------------------------------------------------------------
P = nova("O1")
P.resumo = "NAO_TESTAVEL [ONTO, epistemologia]: sem ensaio otico"
P = nova("O2")
P.resumo = "ABERTO [OPEN]: o espaco latente; sem ensaio otico (F0.3.COLAPSO custodiado; neural = ilustracao)"

# ------------------------------------------------------------------------------------------------------------------
# 7. controles C1-C14 (esperado: FALHA_SEM_HIPOTESE)
# ------------------------------------------------------------------------------------------------------------------
CONTROLES = []


def controle(cid, origem, descricao, falha_sem_hipotese, numeros, ambiguo=False):
    st = "SEM_VEREDITO" if ambiguo else ("FALHA_SEM_HIPOTESE" if falha_sem_hipotese else "CONTROLE_NAO_FALHOU")
    CONTROLES.append(dict(id=cid, origem=origem, descricao=descricao, resultado=st, esperado="FALHA_SEM_HIPOTESE",
                          numeros={k: (f(v) if not isinstance(v, (list, dict, str, bool)) else v) for k, v in numeros.items()}))
    log("controle", cid, st, json.dumps(CONTROLES[-1]["numeros"], ensure_ascii=False, default=str))


# C1
X = np.diag([2 / 3, 2 / 3, -1 / 3]).astype(complex)
pc, pv = pur_cls(X)
rk, rc, _ = rank_info(X)
ev = np.linalg.eigvalsh(X)
controle("C1", ["P1.a"], "diag(2/3, 2/3, -1/3) em M_3(C), nao PSD: Tr 1, Tr rho^2 = 1, posto 3 [psd_is_necessary]",
         abs(np.trace(X) - 1) <= TOL_ID and pc == "=1" and rk == 3 and ev.min() < -RK_NON,
         dict(traco=np.trace(X), pureza=pv, posto=rk, menor_autovalor=float(ev.min())), ambiguo=(rc != "OK" or pc == "AMBIGUO"))
# C2
X = P_UM / 2
pc, pv = pur_cls(X)
rk, rc, _ = rank_info(X)
controle("C2", ["P1.a"], "rho*/2: PSD, posto 1, Tr rho^2 = 1/4 [normalization_is_necessary]",
         rk == 1 and abs(pv - 0.25) <= TOL_ID and pc == "<1" and np.linalg.eigvalsh(X).min() >= -TOL_ID,
         dict(traco=np.trace(X), pureza=pv, posto=rk), ambiguo=(rc != "OK"))
# C3
X = np.eye(2) / 2
rk, rc, _ = rank_info(X)
controle("C3", ["B1", "P4"], "I/2: Tr 1, posto 2; citado: tr P_F ~ 4 [trace_one_not_rank_one]",
         abs(np.trace(X) - 1) <= TOL_ID and rk == 2, dict(traco=np.trace(X), posto=rk, core_trace_PF=CORE_TRPF),
         ambiguo=(rc != "OK"))
# C4
w = np.trace(P_UM @ Q0_UM)
PXP = P_UM @ Q0_UM @ P_UM
controle("C4", ["P3"], "P = rho*, rho = Q0: Tr(P rho) = 0, P rho P = 0 [reading_needs_weight]",
         zcls(abs(w)) == "ZERO" and zcls(dev(PXP)) == "ZERO", dict(traco_P_rho=w, norma_PrhoP=dev(PXP)))
# C5
Pm = np.eye(2)
X = np.eye(2) / 2
out = Pm @ X @ Pm / np.trace(Pm @ X)
rk, rc, _ = rank_info(out)
controle("C5", ["P3"], "P = 1, rho = I/2: saida de posto 2 [reading_needs_rank_one]", rk == 2,
         dict(posto_saida=rk, saida_igual_P=(eqcls(out, Pm) == "IGUAL")), ambiguo=(rc != "OK"))
# C6
Aop = np.diag([2.0, 1.0])
v6 = np.trace(Aop @ P_UM @ Aop.conj().T)
controle("C6", ["B4"], "A = diag(2,1): Tr(A rho* A^H) = 4 [nonunitary_changes_trace]", abs(v6 - 4) <= TOL_ID and abs(v6 - 1) >= Z_NE,
         dict(traco=v6))
# C7
Aop = Q0_UM
Y7 = Aop @ P_UM @ Aop.conj().T
rk, rc, _ = rank_info(Y7)
controle("C7", ["B4"], "A = Q0: A rho* A^H = 0, posto 0 [singular_kills_rank]", zcls(dev(Y7)) == "ZERO" and rk == 0,
         dict(norma=dev(Y7), posto=rk), ambiguo=(rc != "OK"))
# C8
ok8, num8 = True, {}
for lbl in ("0", "pi/2"):
    th = TH_VAL[lbl]
    E = diagE(rhoOut(th))
    rk, rc, _ = rank_info(E)
    num8["th=%s" % lbl] = dict(desvio_Dinf_F_menos_F=f(dev(E, rhoOut(th))), posto=rk)
    ok8 = ok8 and zcls(dev(E, rhoOut(th))) == "ZERO" and rk == 1 and rc == "OK"
controle("C8", ["B5"], "th em {0, pi/2}: D_inf F_th(1) = F_th(1), posto 1 [endpoint_rank_one_iff]", ok8, num8)
# C9
F = rhoOut(thM)
G0 = gmat(0.0)
dist = [dev(dephase(G0, t, F), diagE(F)) for t in GT]
idd = max(dev(dephase(G0, t, F), F) for t in GT)
rks = [rank_info(dephase(G0, t, F))[0] for t in GT]
controle("C9", ["B5", "B7.b"], "g = 0: D_t = id, sem convergencia [zero_rate_no_dephasing]",
         idd <= TOL_ID and min(dist) >= Z_NE and abs(max(dist) - min(dist)) <= TOL_ID and all(r == 1 for r in rks),
         dict(max_desvio_D_t_menos_id=idd, distancia_ao_D_inf_em_G_t=[f(x) for x in dist], postos=rks))
# C10
plus = np.full((2, 2), 0.5)
s, c = np.sin(thM), np.cos(thM)
vals10 = [np.trace(plus @ dephase(gmat(1.0), t, Qth_um(thM))).real for t in GT]
ref10 = [0.5 - math.exp(-t) * s * c for t in GT]
delta10 = max(vals10) - min(vals10)
controle("C10", ["B6"], "leitor |+><+| em thM, gamma = 1: 1/2 - e^{-t} sc varia com t (delta >= 1e-3) [nondiagonal_reader_sees_time]",
         delta10 >= 1e-3 and max(abs(a - b) for a, b in zip(vals10, ref10)) <= TOL_ID,
         dict(valores=[f(x) for x in vals10], delta=delta10, max_desvio_forma_fechada=max(abs(a - b) for a, b in zip(vals10, ref10))))
# C11
controle("C11", ["B7.a2"], "th = pi: sin^2(n pi) = 0 para todo n (<= 1e-10 em float64 ate 1e5) [angular_leak_zero_converges]",
         z_pi <= 1e-10, dict(max_sin2_n_pi=z_pi, n_max=OSC_N))
# C12
controle("C12", ["B9.a"], "th = 0: |t|^2 = 1 e D nao atua [literal_transmission_does_not_force_dephasing]",
         abs(np.cos(0.0) ** 2 - 1) <= TOL_ID and DA["0"] == "NAO_ATUA", dict(t2=np.cos(0.0) ** 2, D=DA["0"]),
         ambiguo=DA["0"] in ("AMBIGUO", "NAO_FINITO"))
# C13
controle("C13", ["B9.a'"], "th = pi/2: |r|^2 = 1 e D nao atua [literal_leak_does_not_force_dephasing]",
         abs(np.sin(math.pi / 2) ** 2 - 1) <= TOL_ID and DA["pi/2"] == "NAO_ATUA", dict(r2=np.sin(math.pi / 2) ** 2, D=DA["pi/2"]),
         ambiguo=DA["pi/2"] in ("AMBIGUO", "NAO_FINITO"))
# C14
A14 = anti(Qth_um(0.0), P_UM)
controle("C14", ["B2"], "th = 0: {Q0, rho*} = 0 [anticomm_zero_iff]", zcls(dev(A14)) == "ZERO", dict(norma_F=dev(A14)))
CONTROLES_OK = all(c["resultado"] == "FALHA_SEM_HIPOTESE" for c in CONTROLES)

# ------------------------------------------------------------------------------------------------------------------
# 8. anexo: achados FORA do pre-registro (nao decidem nenhuma parte)
# ------------------------------------------------------------------------------------------------------------------
ANEXO = []


def anexo(aid, titulo, estatuto, numeros, nota=""):
    ANEXO.append(dict(id=aid, titulo=titulo, estatuto=estatuto, numeros=numeros, nota=nota))
    log("anexo", aid, titulo, "|", json.dumps(numeros, ensure_ascii=False, default=str)[:600])


# A1: varredura fina em th (equivalencias e identidades de B2.a, B3.a, B5.a, B6.a, B8.b, B9.b)
TH_FINO = np.linspace(-2 * math.pi, 2 * math.pi, 2001)
cont = dict(B2a_viol=0, B2a_amb=0, B3a_maxdev=0.0, B5a_viol=0, B5a_amb=0, B6a_maxdev=0.0, B8b_viol=0, B8b_amb=0, B9b_viol=0, B9b_amb=0)
lados_fino = dict(B2a_zero=0, B5a_rank1=0, B9b_nao_atua=0)
for th in TH_FINO:
    s, c = math.sin(th), math.cos(th)
    zA, zs = zcls(dev(anti(Qth_um(th), P_UM))), zcls(abs(s))
    if "AMBIGUO" in (zA, zs):
        cont["B2a_amb"] += 1
    elif (zA == "ZERO") != (zs == "ZERO"):
        cont["B2a_viol"] += 1
    elif zs == "ZERO":
        lados_fino["B2a_zero"] += 1
    L = [np.trace(P_UM @ Qth_um(th)), np.trace(rhoOut(th) @ Q0C), rhoOut(th)[1, 1], abs((Smat(th) @ E1K)[1]) ** 2]
    cont["B3a_maxdev"] = max(cont["B3a_maxdev"], max(abs(x - s * s) for x in L))
    rk, rc, _ = rank_info(diagE(rhoOut(th)))
    z2 = zcls(abs(math.sin(2 * th)))
    if rc != "OK" or z2 == "AMBIGUO":
        cont["B5a_amb"] += 1
    elif (rk == 2) != (z2 == "NAO_ZERO"):
        cont["B5a_viol"] += 1
    elif rk == 1:
        lados_fino["B5a_rank1"] += 1
    for (gl, gv, gb) in GAMMAS:
        for t in GT:
            cont["B6a_maxdev"] = max(cont["B6a_maxdev"], abs(np.trace(P_UM @ dephase(gmat(gv), t, Qth_um(th))) - s * s))
    da = D_atua(th)[0]
    if da == "AMBIGUO" or z2 == "AMBIGUO":
        cont["B8b_amb"] += 1
    elif (da == "NAO_ATUA") != (z2 == "ZERO"):
        cont["B8b_viol"] += 1
    ct, cr = zcls(c * c), zcls(s * s)
    if "AMBIGUO" in (ct, cr, da):
        cont["B9b_amb"] += 1
    elif (da == "ATUA") != (ct == "NAO_ZERO" and cr == "NAO_ZERO"):
        cont["B9b_viol"] += 1
    elif da == "NAO_ATUA":
        lados_fino["B9b_nao_atua"] += 1
anexo("A1", "varredura fina: 2001 angulos em [-2pi, 2pi] para B2.a, B3.a, B5.a, B6.a (x G_t x gamma), B8.b, B9.b",
      "[REAL medido aqui; suplementar]", dict(contagens=cont, lados=lados_fino))

# A2: B5.c e B6.b sobre G_th (a coluna O pre-registrou so thM)
amb_c, viol_c, ex_amb = 0, 0, []
viol_6b, amb_6b = 0, 0
for (lbl, th, ub) in GTH:
    z2 = zcls(abs(np.sin(2 * th)))
    zs = zcls(abs(np.sin(th)))
    F = rhoOut(th)
    for (gl, gv, gb) in GAMMAS:
        for t in GT[1:]:
            rk, rc, sv_ = rank_info(dephase(gmat(gv), t, F))
            if rc != "OK" or z2 == "AMBIGUO":
                amb_c += 1
                ex_amb.append([lbl, gl, t, float(sv_.min())])
            elif (rk == 2) != (z2 == "NAO_ZERO"):
                viol_c += 1
            za = zcls(dev(anti(dephase(gmat(gv), t, Qth_um(th)), P_UM)))
            if "AMBIGUO" in (za, zs):
                amb_6b += 1
            elif (za == "ZERO") != (zs == "ZERO"):
                viol_6b += 1
anexo("A2", "B5.c (posto D_t F = 2 <=> sin 2th != 0, t > 0) e B6.b ({D_t Q_th, rho*} = 0 <=> sin th = 0) sobre G_th x gamma x G_t\\{0}",
      "[REAL medido aqui; suplementar]", dict(B5c_violacoes=viol_c, B5c_ambiguos=amb_c, B5c_exemplos_ambiguos=ex_amb[:10],
                                            B6b_violacoes=viol_6b, B6b_ambiguos=amb_6b))

# A3: resolucao do RANK perto dos zeros de sin 2th (na varredura fina com gamma = beta, t = 0.5)
amb_res = []
for th in TH_FINO:
    rk, rc, sv_ = rank_info(dephase(gmat(beta), 0.5, rhoOut(th)))
    if rc == "AMBIGUO":
        amb_res.append(float(th))
anexo("A3", "resolucao da faixa RANK: posto de D_t F_th(1) com gamma = beta, t = 0.5, na varredura fina",
      "[REAL medido aqui; suplementar]", dict(n_ambiguos=len(amb_res), angulos_ambiguos=amb_res[:20]),
      "onde c^2 s^2 (1 - e^{-2 gamma t}) < 1e-6 o menor sigma cai na faixa AMBIGUA do RANK (1e-12, 1e-6): o posto 2 existe "
      "(det != 0) mas a faixa fixada nao o separa; nao afeta nenhuma parte (a coluna O de B5.c fixou thM, onde sigma_min ~ 1.4e-4)")

# A4: oscilacao angular generalizada para todo th de G_th com sin th != 0
osc_g = []
for (lbl, th, ub) in GTH:
    dlt = abs(th - math.pi * round(th / math.pi))
    if zcls(abs(math.sin(th))) != "NAO_ZERO":
        continue
    Wt = math.ceil(math.pi / dlt) + OSC_EXTRA
    seq = np.sin(nn * th) ** 2
    o = sliding_window_view(seq, Wt)
    o = o.max(axis=1) - o.min(axis=1)
    osc_g.append([lbl, Wt, float(o.min()), math.cos(dlt) - OSC_SLACK, bool(o.min() >= math.cos(dlt) - OSC_SLACK)])
anexo("A4", "cota de oscilacao generalizada (W = ceil(pi/delta) + 2; cota cos delta, delta = distancia de th ao multiplo de pi) em G_th",
      "[DERIVED a cota; REAL a medida; suplementar]", dict(th_W_menorosc_cota_ok=osc_g))

# A5: B5.b no interior: grade de b
viol_b, amb_bb = [], []
for b in list(np.linspace(0, 1, 101)) + [beta, 1 - beta]:
    rk, rc, _ = rank_info(np.diag([1 - b, b]))
    esp = 2 if 0 < b < 1 else 1
    if rc != "OK":
        amb_bb.append(float(b))
    elif rk != esp:
        viol_b.append([float(b), rk])
anexo("A5", "B5.b: posto diag(1-b, b) = 2 <=> 0 < b < 1 numa grade de 101 pontos + {beta, 1-beta}", "[REAL medido aqui; suplementar]",
      dict(violacoes=viol_b, ambiguos=amb_bb))

# A6: sombra de B7.c (espiral) e de B9.c (fluxo do lock)
v = np.array([1, 1], dtype=complex) / math.sqrt(2)
Pv = E00 @ v


def orbita(r, om, s_):
    return Pv + math.exp(-r * s_) * np.exp(1j * om * s_) * (v - Pv)


d_r1 = [dev(orbita(1.0, 1.0, t), Pv) for t in GT]
d_r0 = [dev(orbita(0.0, 1.0, t), Pv) for t in GT]
per = max(dev(orbita(0.0, 1.0, t + 2 * math.pi), orbita(0.0, 1.0, t)) for t in GT)
ax = max(dev((E00 + math.exp(-t) * (I2 - E00)) @ (I2 - E00), math.exp(-t) * (I2 - E00)) for t in GT)
axP = max(dev((E00 + math.exp(-t) * (I2 - E00)) @ E00, E00) for t in GT)
anexo("A6", "sombras suplementares: B7.c (orbita P v + e^{-rs}e^{iws}(v - P v), P = rho*) e B9.c (F(t) = P + e^{-t}(1 - P))",
      "[REAL medido aqui; suplementar; os termos ja estao no kernel]",
      dict(B7c_distancia_r1=[f(x) for x in d_r1], B7c_distancia_r0=[f(x) for x in d_r0], B7c_periodo_2pi_desvio=per,
           B9c_F_vezes_1menosP_desvio=ax, B9c_F_vezes_P_desvio=axP))

# A7: ancoras do um.py/core
anexo("A7", "ancoras: receita interna de fractal_dephasing_principle (SEALED_CODATA_ALPHA x float(np.exp(1/2))) e o core",
      "[REAL lido aqui]", dict(beta_receita_da_funcao=repr(beta_receita_funcao), igual_ao_beta_runtime=(beta_receita_funcao == beta),
                               sealed_igual_alpha=SEALED_OK, core_fractal_dephasing=CORE_FD, core_trace_PF=CORE_TRPF,
                               thM_numpy_igual_math=(thM == thM_math)))

# A8: Q_th do um.py x 1 - F_th(1)
dif, mx_a8 = [], 0.0
for (lbl, th, ub) in GTH:
    Q = Qth_um(th).astype(complex)
    Cq = I2 - rhoOut(th)
    d_cq_qm = dev(Cq, Qth_um(-th))                # 1 - F_th(1) contra Q_{-th}: medido, nao inferido
    mx_a8 = max(mx_a8, d_cq_qm)
    dif.append([lbl, f(dev(Q, Cq)), f(2 * math.sqrt(2) * abs(math.sin(th) * math.cos(th))),
                f(abs(np.trace(E00 @ Q) - np.trace(E00 @ Cq))), f(d_cq_qm)])
anexo("A8", "Q_th (um.py: Rot Q0 Rot^T = S^H Q0 S) x 1 - F_th(1) (= S Q0 S^H)", "[DERIVED; REAL medido aqui]",
      dict(colunas=["th", "|Q_th - (1 - F_th(1))|_F", "2 sqrt2 |sc|", "|Tr(rho* Q_th) - Tr(rho* (1 - F_th(1)))|",
                    "|(1 - F_th(1)) - Q_{-th}|_F"], linhas=dif, max_desvio_1menosF_contra_Q_menos_th=mx_a8,
           status_TOL_ID_1menosF_igual_Q_menos_th=st_tol(mx_a8, TOL_ID)),
      "medido: 1 - F_th(1) = Q_{-th} (o complemento do transmitido e o Q do um.py no angulo oposto). Q_th e 1 - F_th(1) diferem so "
      "fora da diagonal, por 2|sc| em cada entrada (norma F = 2 sqrt2 |sc|), e coincidem so onde sin 2th = 0; o vazamento Tr(rho* .) "
      "e o mesmo (s^2). Nao muda nenhuma parte; serve a quem tipar 'Q' no kernel dizer qual dos dois")

# A9: interface com o atrator (sem refazer A1-A6 da F1.ATRATOR)
I2r = np.eye(2) / 2
rkI, _, _ = rank_info(I2r)
anexo("A9", "interface com a F1.ATRATOR: o estado I/2 e a leitura de posto 1", "[REAL medido aqui; nao refaz A1-A6]",
      dict(posto_I2=rkI, pureza_I2=f(np.trace(I2r @ I2r).real), leitura_rhostar_de_I2_igual_rhostar=(eqcls(P_UM @ I2r @ P_UM / np.trace(P_UM @ I2r), P_UM) == "IGUAL")),
      "o posto 1 que entra com o atrator e o da LEITURA (P3.b): rho*(I/2)rho*/Tr = rho*; o estado atrator I/2 tem posto 2 e pureza 1/2")

# A10: limites do ensaio otico
anexo("A10", "o que o modelo otico nao cobre", "[DERIVED]",
      dict(itens=["'para todo t' e 'existe t' amostrados em G_t x gamma em {1, beta} (finito); a universalidade em t e da face K",
                  "dimensoes n <= 4 e amostras finitas; o enunciado geral e da face K",
                  "identidades de thM (B3; partes em thM de B2, B5, B6, B9): PASSA = validade algebrica, sem poder discriminante",
                  "zeros de sin th, sin 2th, cos th em float64 (~1e-16) classificados pela faixa TOL_ZERO; nenhum caiu na faixa ambigua em G_th"]))

# ------------------------------------------------------------------------------------------------------------------
# 9. vereditos por parte (face O) e consolidacao
# ------------------------------------------------------------------------------------------------------------------
SEM_K_FACE = {"B3.d"}
CITADOS = {"P2.lit": "CITADO", "B7.b": "CITADO_REAL", "B7.c": "CITADO_REAL", "B9.c": "CITADO_REAL"}
ONTO = {"O1": "NAO_TESTAVEL", "O2": "ABERTO"}
CTRL_POR_PARTE = {}
for c in CONTROLES:
    for o in c["origem"]:
        alvos = [pid for pid, col in COLUNAS.items() if pid == o or col["afirmacao"] == o]
        for pid in alvos:
            CTRL_POR_PARTE.setdefault(pid, []).append(c)
SAIDA_PARTES = []
for a in D["c_afirmacoes"]:
    for p in a["partes"]:
        pid = p[0]
        if pid not in PARTES:
            abortar("parte pre-registrada sem ensaio: " + pid)
        obj = PARTES[pid]
        col = COLUNAS[pid]
        esperado = col["esperado"].split(" (")[0]
        vO = obj.veredito()
        bruto = vO
        ctrl = CTRL_POR_PARTE.get(pid, [])
        ctrl_falhou = [c["id"] for c in ctrl if c["resultado"] != "FALHA_SEM_HIPOTESE"]
        if ctrl_falhou and vO in ("PASSA_O", "FALHA_O"):
            vO = "SEM_VEREDITO_O"
        if pid in ONTO:
            vp = ONTO[pid]
            vO = "NAO_APLICAVEL_O"
        elif pid in CITADOS:
            vp = CITADOS[pid] if CITACOES.get(pid) else "SEM_VEREDITO (citacao nao localizada)"
            if pid != "B7.b":
                vO = "NAO_APLICAVEL_O"
        elif pid in SEM_K_FACE:
            vp = {"PASSA_O": "PASSA", "FALHA_O": "FALHA"}.get(vO, "SEM_VEREDITO")
        else:
            vp = "AGUARDA_FACE_K (face O: %s)" % vO
        if esperado in ("PASSA", "FALHA"):
            conforme = (vO == esperado + "_O")
        elif esperado in ("CITADO", "CITADO_REAL", "NAO_TESTAVEL", "ABERTO"):
            conforme = (vp == esperado)
        else:
            conforme = None
        alerta = None
        if esperado == "FALHA" and vO == "PASSA_O":
            alerta = "PASSA EM PARTE DE FALHA PRE-REGISTRADA: ERRO; PARALISA A TRILHA"
        sem_poder = pid in ("B3.a", "B3.b", "B3.d", "B2.b", "B5.b", "B6.b", "B9.b", "P3.b")
        SAIDA_PARTES.append(dict(
            id=pid, afirmacao=col["afirmacao"], enunciado=col["enunciado"], K=col["K"], O=col["O"],
            tolerancia=col["tolerancia"], falsificador=col["falsificador"], esperado=col["esperado"],
            veredito_O=vO, veredito_O_bruto=bruto, veredito_parte=vp, conforme_ao_esperado=conforme, alerta=alerta,
            controles=[dict(id=c["id"], resultado=c["resultado"]) for c in ctrl],
            identidade_sem_poder_discriminante=sem_poder, resumo=obj.resumo, lados_realizados=obj.lados,
            numeros=obj.numeros, checagens=obj.checks))
        log("PARTE %-9s O=%-15s parte=%-40s esperado=%-50s conforme=%s | %s" % (
            pid, vO, vp, col["esperado"][:50], conforme, obj.resumo[:220]))
ALERTAS = [x for x in SAIDA_PARTES if x["alerta"]]
NAO_CONFORMES = [x["id"] for x in SAIDA_PARTES if x["conforme_ao_esperado"] is False]

ESTATUTOS = dict(
    KNOWN=["P1 (pureza <=> posto 1 para rho >= 0 de traco 1): Nielsen & Chuang, Ex. 2.71 -- o termo de kernel e novo, o conteudo "
           "segue [KNOWN]", "P2.lit: rank + nulidade = n (Mathlib LinearMap.finrank_range_add_finrank_ker; Axler, LADR, Teo. 3.22)",
           "P3: a leitura de Luders por projetor de posto 1", "Haar por QR com correcao de fase (Mezzadri 2007) -- so o gerador de amostras",
           "III_1 (Connes 1973) em V4.L02.S3 -- nao mapeado a teste"],
    CITADO_REAL=["B7.b dephase_tendsto_expectation (Ergodicity.lean)", "B7.c orbit_tendsto_center / angular_orbit_no_limit / "
                 "angular_orbit_periodic (IALDJones.lean)", "B9.c transmission_dephases (TheVerbSelectsTheAction.lean)"],
    ONTO=["as 40 frases [ONTO] do mapeamento (b), entre elas a epistemologia de V1 l.4 (O1, NAO_TESTAVEL)",
          "posicao <-> rank (a leitura de POSTO = RANK alem de Tr rho* = posto rho* = 1)",
          "Tudo = D_beta(F(1)) e Nada = MENTIRA pelos dois ramos [CONJECTURE ontologica no um.py]; aqui so as pecas algebricas",
          "D como direcao hiperbolica de SL(2,R) (IALDJones); bulk, existencia, natureza, impedancia, espaco-tempo, gravidade, "
          "consciencia, c^2 e c^3; 'a transmissao e o verbo; a defasagem e a materia'"],
    OPEN=["O2: a leitura do espaco latente dos modelos (F0.3.COLAPSO; neural = ilustracao)", "ergodicidade (V4.L02.S3)"],
    DERIVED=["a cota de oscilacao cos thM de B7.a2 (cos^2(thM/2) - sin^2(thM/2))",
             "A8: 1 - F_th(1) = Q_{-th} (medido em G_th); Q_th != 1 - F_th(1) fora de sin 2th = 0, com o mesmo vazamento s^2"],
    sem_poder_discriminante=["B3 (vazamento = beta), as partes em thM de B2, B5, B6, B9 e P3.b: identidades de thM -- PASSA = "
                             "validade algebrica, nao discrimina beta"])
LEITURAS_APLICADAS = [
    "[INPUT do construtor] ordem das tiragens e distribuicoes das amostras (ver amostras.ordem_e_distribuicoes)",
    "[INPUT do construtor] TOL_ID em matrizes = norma de Frobenius da diferenca (a mesma norma de TOL_ZERO); em escalares, |x - y|",
    "[INPUT do construtor] igualdade x diferenca (P4, controles): <= TOL_ID igual, >= 1e-6 diferente, entre AMBIGUO (a faixa de TOL_ZERO)",
    "[INPUT do construtor] P1.a: idempotencia classificada pela faixa TOL_ZERO em |rho^2 - rho|_F; precondicoes PSD (autovalor >= -TOL_ID) e Tr 1",
    "[INPUT do construtor] P1.b: o conjunto da hipotese e construido de cada M gaussiana com c = (1 - a^2 - (1-a)^2)/(2b) "
    "(impoe Tr M = 1 e Tr M^2 = 1 sem usar det); posto 1 decidido com a tolerancia escalada da propria parte "
    "(sigma_min <= TOL_ID(1+|M|_F^2), sigma_max >= 1e-6), e a faixa RANK nao escalada e reportada ao lado",
    "[INPUT do construtor] P2.a/P2.b: nulidade contada sem a SVD do posto, pelos autovalores da propria matriz hermitiana "
    "(eigvalsh; |lambda| com as faixas do RANK). A tentativa 1 usou eigvalsh(A^H A) com as faixas ao quadrado e caiu em AMBIGUO "
    "por precisao (o autovalor nulo de A^H A sai com erro ~1e-16 > 1e-24): artefato da construcao, corrigido; tentativa preservada",
    "[INPUT do construtor] P3.a: produto completo P x X por n; B4.a: pareamento ciclico de u com rho e com P (projecoes de posto 1 "
    "dos psi, mais rho* e Q0 em n = 2 e as projecoes de P4 em n = 4); o teste em rho* so em n = 2 (rho* e 2x2)",
    "[INPUT do construtor] 'D atua' (existe t) e 'para todo t' amostrados em G_t x gamma em {1, beta}; zeros de sin th, sin 2th, "
    "|t|^2, |r|^2 pela faixa TOL_ZERO no escalar",
    "[INPUT do construtor] B7.a1: th percorre G_th; B7.b: sombra pela distancia ao limite (TOL_REL) e pela lei de semigrupo (TOL_ID)",
    "[INPUT do construtor] B5.b: as bordas b = 0 e b = 1 (nomeadas no enunciado) entram na parte; o interior de b vai ao anexo A5",
    "[INPUT do construtor] precedencia do veredito O: NAO_FINITO -> SEM_VEREDITO_O; senao VIOLA -> FALHA_O; senao AMBIGUO ou beta "
    "sem conferencia -> SEM_VEREDITO_O; senao PASSA_O; controle que nao falha rebaixa a parte de origem a SEM_VEREDITO_O"]

TENTATIVAS = []
_dt = os.path.join(AQUI, "tentativas")
if os.path.isdir(_dt):
    for _fn in sorted(os.listdir(_dt)):
        _n, _h = sha_arq(os.path.join(_dt, _fn))
        TENTATIVAS.append([_fn, _n, _h])
HISTORICO = [
    "tentativa 1 (script em tentativas/run_optico.py.tentativa1_*; seu RESULTADO/LOG arquivados em tentativas/): P2.b saiu "
    "SEM_VEREDITO_O porque a nulidade era contada por eigvalsh(A^H A) com as faixas do RANK ao quadrado; o autovalor nulo de A^H A "
    "sai com erro absoluto ~1e-16 > (1e-12)^2 = 1e-24 (artefato numerico da construcao, nao do enunciado). Correcao: eigvalsh da "
    "propria matriz hermitiana, |lambda| com as faixas do RANK (sem mudar tolerancia, mapeamento ou esperado). A comparacao parte a "
    "parte com a tentativa anterior e calculada abaixo (comparacao_com_tentativa_anterior), nao afirmada.",
    "tentativa 2 (script em tentativas/run_optico.py.tentativa2_*; seu RESULTADO/LOG arquivados em tentativas/): so o anexo mudou. "
    "A frase do estatuto DERIVED sobre A8 saiu truncada ('Q_th = Q_{-th} de 1 - F_th(1)') e a igualdade 1 - F_th(1) = Q_{-th} "
    "era inferida, nao medida. Correcao: A8 mede |(1 - F_th(1)) - Q_{-th}|_F e 2 sqrt2 |sc|, e a frase foi reescrita. Nenhuma "
    "parte, tolerancia, mapeamento ou esperado mudou; a comparacao abaixo e calculada."]
COMPARACAO = None
if "RESULTADO_OPTICO.json" in ARQUIVADOS:
    try:
        _prev = json.load(open(ARQUIVADOS["RESULTADO_OPTICO.json"], encoding="utf-8"))
        _pv = {x["id"]: x["veredito_O"] for x in _prev.get("partes", [])}
        _pc = {x["id"]: x["resultado"] for x in _prev.get("controles", [])}
        _cur_c = {c["id"]: c["resultado"] for c in CONTROLES}
        COMPARACAO = dict(
            arquivo_anterior=os.path.basename(ARQUIVADOS["RESULTADO_OPTICO.json"]),
            sha256_anterior=sha_arq(ARQUIVADOS["RESULTADO_OPTICO.json"])[1],
            script_anterior_sha256=_prev.get("script", {}).get("sha256"),
            partes_com_veredito_O_diferente=[[x["id"], _pv.get(x["id"]), x["veredito_O"]] for x in SAIDA_PARTES
                                             if _pv.get(x["id"]) != x["veredito_O"]],
            controles_com_resultado_diferente=[[k, _pc.get(k), v] for k, v in _cur_c.items() if _pc.get(k) != v],
            anexo_anterior_igual=(json.dumps(_prev.get("achados_fora_do_preregistro"), sort_keys=True, ensure_ascii=False)
                                  == json.dumps(limpa_prev(ANEXO), sort_keys=True, ensure_ascii=False)),
            anexo_ids_diferentes=[a["id"] for a in limpa_prev(ANEXO)
                                  if json.dumps(a, sort_keys=True, ensure_ascii=False) != json.dumps(
                                      next((b for b in (_prev.get("achados_fora_do_preregistro") or []) if b.get("id") == a["id"]), None),
                                      sort_keys=True, ensure_ascii=False)],
            checagens_com_status_diferente=[[x["id"], c["nome"], dict(((y["nome"], y["status"]) for y in
                                             next((p for p in _prev.get("partes", []) if p["id"] == x["id"]), {"checagens": []})["checagens"])).get(c["nome"]), c["status"]]
                                            for x in SAIDA_PARTES for c in x["checagens"]
                                            if dict(((y["nome"], y["status"]) for y in next((p for p in _prev.get("partes", []) if p["id"] == x["id"]),
                                                                                             {"checagens": []})["checagens"])).get(c["nome"]) != c["status"]])
    except (OSError, ValueError, KeyError) as e:
        COMPARACAO = dict(erro="comparacao com a tentativa anterior falhou visivelmente: %r" % (e,))
log("comparacao com a tentativa anterior:", json.dumps(COMPARACAO, ensure_ascii=False, default=str))

T1 = datetime.datetime.now(datetime.timezone.utc)
RES = dict(
    tentativas_preservadas=TENTATIVAS, historico_de_correcoes=HISTORICO, comparacao_com_tentativa_anterior=COMPARACAO,
    documento="RESULTADO OTICO -- F1.FREQUENCIA (trilha POSTO)",
    gerencia="c1", autor="construtor otico (subagente)", inicio_utc=T0.isoformat(), fim_utc=T1.isoformat(),
    estatuto="[REAL medido aqui, face O (modelo otico sintetico)]; PASSA = validade matematica na face testada, nao creditacao; "
             "nao move gate; nao fala da natureza; a parte so fecha com a face K (exceto B3.d, de face unica)",
    escopo="escrita so em 2_OPTICO; um.py nao executado (alpha lido dos bytes); sem dado observado, provedor, Bancada ou chamada paga; "
           "sem Lean (a face K e de outro construtor)",
    acom="[INPUT do construtor] README da memoria ACOM lido; sem referencia propria e com a escrita na memoria proibida pela ordem, "
         "nao houve init; a inscricao e ato da gerencia",
    script=dict(caminho=os.path.abspath(__file__), sha256=SCRIPT_SHA256),
    preregistro=dict(FREEZE_json=[nF, hF], PREREGISTRO_json=[nJ, hJ], PREREGISTRO_md=[nM, hM], congelado_utc=FREEZE["congelado_utc"]),
    ambiente=AMBIENTE, beta_runtime=BETA_INFO, numero_do_operador_V4_l16=OP_NUM_S,
    protocolo_lido=dict(TOL_ID=[TOL_ID, TOL_ID_MP_S], TOL_ZERO=[Z_EQ, Z_NE], RANK=[RK_NUL, RK_NON], PUREZA=[PUR_EQ, PUR_LT],
                        TOL_REL=TOL_REL, TOL_LEAK=[TOL_LEAK, TOL_LEAK_MP_S], CONF_OPERADOR=[CONF_OP_NUM_S, CONF_OP_TOL],
                        OSC=dict(W=W_OSC, N=OSC_N, folga=OSC_SLACK), G_th=GTH_SPEC, G_t=GT_SPEC, gammas=["1", "beta"], dps=DPS,
                        n_passagens_B7a1=N_PASSAGENS),
    amostras=dict(AMOSTRAS, haar={str(k): v for k, v in AMOSTRAS["haar"].items()}),
    leituras_aplicadas=LEITURAS_APLICADAS,
    partes=SAIDA_PARTES,
    controles=CONTROLES, controles_ok=CONTROLES_OK,
    alertas=[dict(id=x["id"], alerta=x["alerta"]) for x in ALERTAS], nao_conformes_ao_esperado=NAO_CONFORMES,
    estatutos_que_ficam=ESTATUTOS,
    achados_fora_do_preregistro=ANEXO,
    para_o_mapa_de_rotas=dict(
        nota="NAO registrado (a ordem proibe rotas.py registrar); proposta para a gerencia",
        rota_id_sugerida="formal.f1_frequencia_posto.otico", dominio_sugerido="FORMAL",
        consultas_feitas=["c11 'modelo otico|otico|optic': 4", "c12 'F1.FREQUENCIA|frequencia defasa|tudo e frequencia': 0",
                          "c13 'dephas|defasag': 34", "c14 'rhoOut|matriz-S|Smat|S-matrix': 5", "c15 'posto|rank': 25",
                          "c16 'F1.ATRATOR|singularidade_le_atrator|atrator': 11"]),
)
RES["resumo_por_parte"] = ["%s: O=%s; parte=%s; esperado=%s" % (x["id"], x["veredito_O"], x["veredito_parte"], x["esperado"])
                           for x in SAIDA_PARTES]
log("controles: todos FALHA_SEM_HIPOTESE =", CONTROLES_OK, "| alertas:", [x["id"] for x in ALERTAS], "| nao conformes:", NAO_CONFORMES)


txt = json.dumps(limpa(RES), ensure_ascii=False, indent=1, allow_nan=False) + "\n"
for proib in ("CONFIRMED", "CONFIRMADA", "não provou", "nao provou", "pós-dição", "pos-dicao"):
    if proib in txt:
        abortar("palavra proibida no resultado: " + proib)
gravar_atomico(SAIDA_JSON, txt.encode("utf-8"))
log("RESULTADO_OPTICO.json gravado:", len(txt.encode("utf-8")), "B sha256", sha_bytes(txt.encode("utf-8")))
gravar_atomico(SAIDA_LOG, ("\n".join(LOG) + "\n").encode("utf-8"))
sys.exit(0 if (CONTROLES_OK and not ALERTAS and not NAO_CONFORMES) else 3)
