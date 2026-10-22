"""Nucleo numerico do ESTUDO DE PODER REALISTA do Rito 9 (22/10/2026).

Estatuto: SYNTHETIC_DIAGNOSTIC_ONLY. Nenhum dado observacional; nenhuma afirmacao sobre a natureza.

Modelo (fixado em PREREGISTRO.json antes de qualquer rodada)
------------------------------------------------------------
H0 : perfil de chegada de UM neutrino detectado, f0(t) (oraculo: totalmente conhecido).
H1 : f1 = f0 (*) K_beta(ell),  K_beta = espera geometrica do EXCESSO:
        atraso = (N-1) * ell / c ,  N ~ Geom(beta) em {1,2,...},  P(N=n) = beta (1-beta)^(n-1).
beta = SEALED_CODATA_ALPHA * sqrt(e), com SEALED_CODATA_ALPHA LIDO por script do um.py (nunca literal).

Discretizacao exata
-------------------
Celulas de largura tau0 = ell/c. Como o atraso e multiplo inteiro de tau0, a massa de H1 na celula i
e EXATAMENTE  P1_i = sum_k beta (1-beta)^k P0_{i-k}  (filtro IIR de 1a ordem), sem interpolacao.
Estatistica: LLR de forma completa  Lambda_n = sum_i ln(P1_{c(i)} / P0_{c(i)})  (celulas = resolucao ideal tau0).

Limiar e poder
--------------
c_n = menor valor v tal que P0(Lambda_n >= v) <= p5sigma  (cauda gaussiana unilateral de 5 sigma).
poder(n) = P1(Lambda_n >= c_n);  n_req = menor n com poder >= 0.5  (mediana do LLR sob H1 >= limiar).
A distribuicao de Lambda_n e obtida por convolucao n-vezes EXATA na rede de lambda (FFT), e verificada por
simulacao com amostragem por importancia (identidade exata P0(A) = E1[exp(-Lambda); A]).
"""
from __future__ import annotations

import hashlib
import math
import re

import numpy as np
from scipy.signal import lfilter
from scipy.special import erf, erfc

C_M_S = 299792458.0
P5 = 0.5 * math.erfc(5.0 / math.sqrt(2.0))          # 1 - Phi(5), unilateral
FWHM_TO_SIGMA = 1.0 / (2.0 * math.sqrt(2.0 * math.log(2.0)))


# ----------------------------------------------------------------------------------------------
# beta: lido do um.py (so leitura); nunca literal
# ----------------------------------------------------------------------------------------------
def ler_alpha_um(caminho: str) -> dict:
    """Le SEALED_CODATA_ALPHA do um.py (bytes, so leitura; nao importa nem executa o arquivo)."""
    with open(caminho, "rb") as f:
        b = f.read()
    m = re.search(rb"^SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+\-]+)", b, re.M)
    if m is None:
        raise RuntimeError("SEALED_CODATA_ALPHA nao encontrado no um.py (falha visivel)")
    return dict(
        alpha=float(m.group(1)),
        linha=b[: m.start()].count(b"\n") + 1,
        texto=m.group(0).decode("ascii"),
        sha256=hashlib.sha256(b).hexdigest(),
        bytes=len(b),
    )


def beta_de_alpha(alpha: float) -> float:
    return alpha * math.sqrt(math.e)


# ----------------------------------------------------------------------------------------------
# Perfis H0 (famílias fixadas no pré-registro)
# ----------------------------------------------------------------------------------------------
def _pesos(K: int, amp: str, r_damped: float) -> list:
    if amp == "flat":
        w = [1.0] * K
    elif amp == "damped":
        w = [r_damped ** j for j in range(K)]
    else:
        raise ValueError(f"amp invalido: {amp}")
    s = sum(w)
    return [x / s for x in w]


def perfil_burst(K: int, S_ms: float, gamma_ms: float, amp: str, mu1_ms: float, r_damped: float) -> list:
    """K picos gaussianos igualmente espacados de mu1 ate S (FWHM = gamma). Retorna [(w, mu, sigma)]."""
    sig = gamma_ms * FWHM_TO_SIGMA
    w = _pesos(K, amp, r_damped)
    mus = [mu1_ms + j * (S_ms - mu1_ms) / (K - 1) for j in range(K)]
    return [(w[j], mus[j], sig) for j in range(K)]


def perfil_dict(familia: str, gauss: list, f_tail: float = 0.0, tau_ms: float | None = None, nome: str = "",
                sigma_offset_ms: float = 0.0) -> dict:
    """sigma_offset_ms > 0: H0 vira a media sobre a populacao de eventos com ponto-zero deslocado por N(0,sigma^2),
    um deslocamento independente por neutrino (valido quando cada neutrino vem de uma fusao diferente)."""
    return dict(familia=familia, gauss=gauss, f_tail=float(f_tail), tau_ms=tau_ms, nome=nome,
                sigma_offset_ms=float(sigma_offset_ms))


# ----------------------------------------------------------------------------------------------
# Massas por célula (exatas) e H1 por filtro IIR
# ----------------------------------------------------------------------------------------------
def massa_gauss_celulas(edges: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    """Massa gaussiana exata por celula [edges[i], edges[i+1]], sem cancelamento nas caudas."""
    s = sigma * math.sqrt(2.0)
    lo = (edges[:-1] - mu) / s
    hi = (edges[1:] - mu) / s
    out = np.empty_like(lo)
    right = lo >= 0.0
    left = hi <= 0.0
    mid = ~(right | left)
    out[right] = 0.5 * (erfc(lo[right]) - erfc(hi[right]))
    out[left] = 0.5 * (erfc(-hi[left]) - erfc(-lo[left]))
    out[mid] = 0.5 * (erf(hi[mid]) - erf(lo[mid]))
    return out


def celulas(perfil: dict, ell_km: float, beta: float, massa_residual_log: float = 41.4):
    """Constroi (edges, P0, P1) para o perfil e o comprimento ell. tau0 = ell/c (ms)."""
    tau0 = ell_km * 1e3 / C_M_S * 1e3
    gauss = perfil["gauss"]
    f = perfil["f_tail"]
    tau = perfil["tau_ms"]
    mus = [g[1] for g in gauss]
    sigs = [g[2] for g in gauss]
    atraso_medio = tau0 * (1.0 - beta) / beta
    s_off = float(perfil.get("sigma_offset_ms", 0.0))
    t_lo = min(m - 12.0 * s for m, s in zip(mus, sigs)) - 12.0 * s_off
    t_hi = max(m + 12.0 * s for m, s in zip(mus, sigs)) + 12.0 * s_off + massa_residual_log * atraso_medio
    if f > 0.0:
        t_hi = max(t_hi, 34.5 * tau + 12.0 * s_off)
    i_lo = int(math.floor(t_lo / tau0))
    i_hi = int(math.ceil(t_hi / tau0))
    edges = tau0 * np.arange(i_lo, i_hi + 1, dtype=np.float64)
    B = np.zeros(edges.size - 1)
    for w, mu, s in gauss:
        B += w * massa_gauss_celulas(edges, mu, s)
    if f > 0.0:
        T = np.zeros_like(B)
        a = edges[:-1]
        pos = a >= 0.0
        T[pos] = np.exp(-a[pos] / tau) * (-np.expm1(-tau0 / tau))
        P0 = (1.0 - f) * B + f * T
    else:
        P0 = B
    if s_off > 0.0:
        K = int(math.ceil(12.0 * s_off / tau0))
        kedges = tau0 * (np.arange(-K, K + 2, dtype=np.float64) - 0.5)
        ker = massa_gauss_celulas(kedges, 0.0, s_off)
        ker /= ker.sum()
        P0 = np.convolve(P0, ker, mode="same")      # direta (sem FFT): preserva as caudas
    P1 = lfilter([beta], [1.0, -(1.0 - beta)], P0)
    return edges, P0, P1, tau0


def llr_celulas(P0: np.ndarray, P1: np.ndarray, cap: float):
    """Retorna (P0, P1, lam_true, lam_cap) so nas celulas com P1>0. lam_true=+inf onde P0==0."""
    m = P1 > 0.0
    P0 = P0[m]
    P1 = P1[m]
    pos = P0 > 0.0
    lam = np.full(P0.shape, np.inf)
    lam[pos] = np.log(P1[pos]) - np.log(P0[pos])
    return P0, P1, lam, np.minimum(lam, cap)


# ----------------------------------------------------------------------------------------------
# Rede de lambda e soma n-vezes por FFT
# ----------------------------------------------------------------------------------------------
def pmf_rede(P0: np.ndarray, P1: np.ndarray, lam_c: np.ndarray, delta: float):
    """pmf de lambda (clipado) sob H0 e H1 numa rede comum, com 'linear binning' (preserva a media)."""
    lo = math.floor((float(lam_c.min()) - 1e-12) / delta) * delta
    x = (lam_c - lo) / delta
    q0 = np.floor(x).astype(np.int64)
    fr = x - q0
    Qn = int(q0.max()) + 2

    def _pmf(w):
        a = np.bincount(q0, weights=w * (1.0 - fr), minlength=Qn)
        b = np.bincount(q0 + 1, weights=w * fr, minlength=Qn)
        p = (a + b)[:Qn]
        return p / p.sum()

    return _pmf(P0), _pmf(P1), lo


class SomaN:
    """Distribuicao da soma de n variaveis iid na rede (ordenada por valor crescente)."""

    __slots__ = ("pmf", "base", "L", "delta", "exata", "fora")

    def __init__(self, pmf, base, L, delta, exata, fora):
        self.pmf, self.base, self.L, self.delta, self.exata, self.fora = pmf, base, L, delta, exata, fora

    def valor(self, i):
        return self.base + (i - self.L // 2) * self.delta

    def indice_de(self, c):
        return int(math.ceil((c - self.base) / self.delta - 1e-9)) + self.L // 2

    def cauda(self, c):
        i = self.indice_de(c)
        if i <= 0:
            return float(self.pmf.sum())
        if i >= self.L:
            return 0.0
        return float(self.pmf[i:].sum())

    def quantil_superior(self, p):
        """menor valor v tal que P(S >= v) <= p."""
        ct = np.cumsum(self.pmf[::-1])[::-1]
        ok = ct <= p
        if not ok.any():
            raise RuntimeError("cauda nunca <= p (janela insuficiente)")
        i = int(np.argmax(ok))
        return self.valor(i)

    def mediana(self):
        cs = np.cumsum(self.pmf)
        i = int(np.searchsorted(cs, 0.5 * cs[-1]))
        return self.valor(i)


def soma_n(pmf: np.ndarray, lo: float, delta: float, n: int, L_exato_max: int = 1 << 22,
           L_max: int = 1 << 24, janela_sd: float = 14.0, forcar_janela: bool = False) -> SomaN:
    Qn = pmf.size
    j = np.arange(Qn)
    mean = float((j * pmf).sum())
    var = float((((j - mean) ** 2) * pmf).sum())
    nu = int(round(mean))
    full = n * max(nu, Qn - 1 - nu)
    exata = (2 * full + 2 <= L_exato_max) and not forcar_janela
    if exata:
        half = full + 2
    else:
        sd_n = math.sqrt(n * var)
        off = n * (mean - nu)
        half = int(math.ceil(janela_sd * sd_n + abs(off))) + 8
    L = 1 << int(math.ceil(math.log2(2 * half + 2)))
    if L > L_max:
        raise RuntimeError(f"L={L} excede L_max={L_max} (n={n})")
    if (not exata) and Qn > L:
        raise RuntimeError(f"pmf unitaria (Qn={Qn}) mais larga que a janela L={L} (n={n}): dobra proibida")
    arr = np.zeros(L)
    np.add.at(arr, (j - nu) % L, pmf)
    res = np.fft.irfft(np.fft.rfft(arr) ** n, n=L)
    res[res < 0.0] = 0.0
    res = np.fft.fftshift(res)
    base = n * (lo + nu * delta)
    k = max(1, L // 20)
    # 'fora' so mede vazamento por dobra ciclica (modo janela); no modo exato nao ha dobra, logo 0.
    fora = 0.0 if exata else float(res[:k].sum() + res[-k:].sum())
    return SomaN(res, base, L, delta, exata, fora)


def avaliar_n(p0, p1, lo, delta, n, p5=P5, **kw):
    A0 = soma_n(p0, lo, delta, n, **kw)
    A1 = soma_n(p1, lo, delta, n, **kw)
    c = A0.quantil_superior(p5)
    return dict(n=n, c_n=c, poder=A1.cauda(c), mediana_h1=A1.mediana(), cauda_h0_em_c=A0.cauda(c),
                exata=bool(A0.exata and A1.exata), fora=max(A0.fora, A1.fora), L=A0.L)


def varrer_n(p0, p1, lo, delta, n_max=1_000_000, alvo=0.5, p5=P5, **kw):
    """Acha n_req = menor n com poder >= alvo. Retorna (n_req|None, linhas_da_varredura, diagnosticos)."""
    cache = {}

    def ev(n):
        if n not in cache:
            cache[n] = avaliar_n(p0, p1, lo, delta, n, p5=p5, **kw)
        return cache[n]

    cand = list(range(1, 17))
    n = 16
    while n < n_max:
        n = max(n + 1, int(math.ceil(n * 1.12)))
        cand.append(min(n, n_max))
    cand = sorted(set(cand))
    n_lo, n_hi = 0, None
    for n in cand:
        if ev(n)["poder"] >= alvo:
            n_hi = n
            break
        n_lo = n
    if n_hi is None:
        rows = [cache[k] for k in sorted(cache)]
        return None, rows, dict(motivo="n_req > n_max", n_max=n_max)
    lo_b, hi_b = n_lo, n_hi            # lo_b falha (ou 0); hi_b passa
    while hi_b - lo_b > 1:
        mid = (lo_b + hi_b) // 2
        if ev(mid)["poder"] >= alvo:
            hi_b = mid
        else:
            lo_b = mid
    n_req = hi_b
    mono_ok = True
    for extra in (n_req + 1, n_req + 2):
        if extra <= n_max and ev(extra)["poder"] < alvo:
            mono_ok = False
    rows = [cache[k] for k in sorted(cache)]
    return n_req, rows, dict(monotono_ok=mono_ok)


# ----------------------------------------------------------------------------------------------
# Verificacao por simulacao com amostragem por importancia (identidade exata)
# ----------------------------------------------------------------------------------------------
def verificar_mc(P1: np.ndarray, lam_true: np.ndarray, lam_c: np.ndarray, n: int, c_lat: float,
                 M: int, seed_seq, p5: float = P5, chunk_pares: int = 4_000_000):
    """Simula M somas de n neutrinos de H1 (celulas ~ P1).

    P0(S >= c) = E1[ exp(-Lambda_verdadeiro) 1{S >= c} ]  (exata). Devolve:
      c_hat (quantil 5sigma da nula estimado), cauda nula em c_lat, poder MC em c_lat, erros-padrao.
    """
    rng = np.random.default_rng(seed_seq)
    cdf = np.cumsum(P1)
    cdf /= cdf[-1]
    chunk = max(1, chunk_pares // max(1, n))
    S_list, W_list = [], []
    cont_poder = 0
    smin = c_lat - 6.0
    feitos = 0
    while feitos < M:
        m = min(chunk, M - feitos)
        u = rng.random((m, n))
        idx = np.searchsorted(cdf, u)
        np.minimum(idx, cdf.size - 1, out=idx)
        S = lam_c[idx].sum(axis=1)
        cont_poder += int((S >= c_lat - 1e-9).sum())
        sel = S >= smin
        if sel.any():
            with np.errstate(over="ignore", invalid="ignore"):
                Lt = lam_true[idx[sel]].sum(axis=1)
                w = np.exp(-Lt)
            S_list.append(S[sel])
            W_list.append(w)
        feitos += m
    S_all = np.concatenate(S_list) if S_list else np.zeros(0)
    W_all = np.concatenate(W_list) if W_list else np.zeros(0)
    o = np.argsort(-S_all)
    Ss, Ws = S_all[o], W_all[o] / M
    cw = np.cumsum(Ws)
    if cw.size and cw[-1] > p5:
        pos = int(np.argmax(cw > p5))
        c_hat = float(Ss[pos])
    else:
        c_hat = float("nan")
    sel_c = S_all >= c_lat - 1e-9
    tail = float(W_all[sel_c].sum() / M)
    se_tail = float(np.sqrt(max(0.0, (np.sum(W_all[sel_c] ** 2) / M - tail ** 2) / M)))
    pw = cont_poder / M
    se_pw = math.sqrt(max(pw * (1 - pw), 1e-12) / M)
    return dict(n=n, M=M, c_hat=c_hat, c_lat=c_lat, cauda_nula_em_c_lat=tail, se_cauda=se_tail,
                poder_mc=pw, se_poder=se_pw)
