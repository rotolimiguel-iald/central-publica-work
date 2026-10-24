# -*- coding: utf-8 -*-
"""amostrador.py -- o ensemble afim-invariante de Goodman & Weare (2010), o mesmo movimento «stretch» (a = 2) do emcee, em LOTE na GPU:
cada meia-rodada avalia todos os caminhantes de uma metade num único lote do motor. Semente explícita (reprodutível)."""
import math
import time

import numpy as np
import torch
from .regua import numero_finito, inteiro


def autocorr_integrada(x, c=5.0):
    """τ integrado (janela automática de Sokal, como no emcee), por parâmetro; x (passos, caminhantes)."""
    if not np.isfinite(x).all() or x.ndim != 2 or x.shape[0] < 2 or np.any(np.var(x, axis=0) == 0):
        raise ValueError("cadeia constante/curta/não finita: autocorrelação não estimável")
    n = x.shape[0]
    f = np.zeros(n)
    for k in range(x.shape[1]):
        y = x[:, k] - x[:, k].mean()
        m = 2 ** int(np.ceil(np.log2(2 * n)))
        F = np.fft.fft(y, n=m)
        ac = np.fft.ifft(F * np.conj(F))[:n].real
        if ac[0] > 0:
            f += ac / ac[0]
    f /= x.shape[1]
    taus = 2.0 * np.cumsum(f) - 1.0
    janela = np.arange(len(taus)) < c * taus
    w = int(np.argmin(janela)) if not janela.all() else len(taus) - 1
    return float(max(1.0, taus[w]))  # conservative ESS, never inflated above raw sample count


def amostrar(logp, p0, n_passos, semente=42, a=2.0, ao_passo=None):
    """logp: função (N,D) tensor -> (N,) tensor; p0 (W,D). Devolve cadeia (passos, W, D) numpy, logp, aceitação."""
    n_passos = inteiro(n_passos, "n_passos", 1, 20000)
    semente = inteiro(semente, "semente", 0, 2**32 - 1)
    a = numero_finito(a, "a")
    if a <= 1 or p0.ndim != 2 or p0.shape[0] < 2 * p0.shape[1] or p0.shape[0] % 2 or p0.dtype == torch.bool or not bool(torch.isfinite(p0).all()):
        raise ValueError("ensemble/stretch inválido")
    dev = p0.device
    g = torch.Generator(device=dev); g.manual_seed(int(semente))
    W, D = p0.shape
    meio = W // 2
    pos = p0.clone()
    lp = logp(pos)
    if lp.shape != (W,) or not bool(torch.isfinite(lp).all()):
        raise ValueError("caminhantes iniciais sem logp finito no suporte")
    cadeia = np.empty((n_passos, W, D))
    lps = np.empty((n_passos, W))
    aceitos = torch.zeros(W, device=dev)
    t0 = time.time()
    for s in range(n_passos):
        for S, C in ((slice(0, meio), slice(meio, W)), (slice(meio, W), slice(0, meio))):
            xs, xc = pos[S], pos[C]
            n = xs.shape[0]
            u = torch.rand(n, generator=g, device=dev, dtype=pos.dtype)
            z = ((a - 1.0) * u + 1.0) ** 2 / a
            j = torch.randint(0, xc.shape[0], (n,), generator=g, device=dev)
            prop = xc[j] + z[:, None] * (xs - xc[j])
            lpp = logp(prop)
            if lpp.shape != (n,) or bool((torch.isnan(lpp) | torch.isposinf(lpp)).any()):
                raise ValueError("logp de proposta inválido; -inf somente para fora do suporte")
            lnq = (D - 1) * torch.log(z) + lpp - lp[S]
            ok = torch.log(torch.rand(n, generator=g, device=dev, dtype=pos.dtype)) < lnq
            bloco = pos[S].clone(); bloco[ok] = prop[ok]; pos[S] = bloco
            lb = lp[S].clone(); lb[ok] = lpp[ok]; lp[S] = lb
            ac = aceitos[S].clone(); ac[ok] += 1; aceitos[S] = ac
        cadeia[s] = pos.cpu().numpy()
        lps[s] = lp.cpu().numpy()
        if ao_passo is not None:
            ao_passo(s + 1, n_passos, time.time() - t0)
    return cadeia, lps, (aceitos / n_passos).cpu().numpy(), time.time() - t0


def resumo(cadeia, queima, nomes):
    if cadeia.ndim != 3 or not np.isfinite(cadeia).all() or cadeia.shape[2] != len(nomes):
        raise ValueError("cadeia inválida")
    queima = inteiro(queima, "queima", 0, cadeia.shape[0] - 2)
    ch = cadeia[queima:]
    plano = ch.reshape(-1, ch.shape[2])
    out = {}
    for i, nm in enumerate(nomes):
        med = float(np.median(plano[:, i])); lo = float(np.percentile(plano[:, i], 16)); hi = float(np.percentile(plano[:, i], 84))
        out[nm] = dict(median=med, lo16=lo, hi84=hi, sigma_lower=med - lo, sigma_upper=hi - med, mean=float(plano[:, i].mean()),
                       std=float(plano[:, i].std()))
    taus = [autocorr_integrada(ch[:, :, i]) for i in range(ch.shape[2])]
    return out, taus, plano
