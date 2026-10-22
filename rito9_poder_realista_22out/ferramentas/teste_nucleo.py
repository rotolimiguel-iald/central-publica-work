"""Testes do nucleo numerico contra solucoes ANALITICAS (nenhum perfil pre-registrado e usado aqui).

Uso:  python teste_nucleo.py <caminho_um.py>

Cada teste lanca AssertionError se falhar (fail-closed). A funcao executar() devolve um dict com os numeros
medidos, para entrar no registro da rodada.
"""
from __future__ import annotations

import itertools
import math
import os
import sys

import numpy as np
from scipy.signal import lfilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nucleo_poder as N  # noqa: E402


def t_gauss_shift():
    """H0=N(0,1), H1=N(d,1): Lambda_n e gaussiana; n_req analitico = ceil(25/d^2)."""
    out = {}
    for d, esperado in ((1.0, 25), (0.5, 100), (2.0, 7)):
        h = 0.01
        edges = np.arange(-14.0, 14.0 + d + h, h)
        P0 = N.massa_gauss_celulas(edges, 0.0, 1.0)
        P1 = N.massa_gauss_celulas(edges, d, 1.0)
        P0, P1, lam, lam_c = N.llr_celulas(P0, P1, cap=60.0)
        delta = 0.01
        p0, p1, lo = N.pmf_rede(P0, P1, lam_c, delta)
        n_req, rows, diag = N.varrer_n(p0, p1, lo, delta, n_max=5000)
        assert n_req is not None and abs(n_req - esperado) <= 1, (d, n_req, esperado)
        # limiar analitico no n_req: c = -n d^2/2 + 5 d sqrt(n)
        r = [x for x in rows if x["n"] == n_req][0]
        c_an = -n_req * d * d / 2 + 5 * d * math.sqrt(n_req)
        assert abs(r["c_n"] - c_an) < 0.05, (d, r["c_n"], c_an)
        out[f"gauss_d{d}"] = dict(n_req=n_req, esperado=esperado, c_n=r["c_n"], c_analitico=c_an, poder=r["poder"])
    return out


def t_iir_vs_pente():
    rng = np.random.default_rng(1)
    P0 = rng.random(60)
    P0 /= P0.sum()
    beta = 0.0120313
    P1 = lfilter([beta], [1.0, -(1.0 - beta)], P0)
    K = 6000
    w = beta * (1 - beta) ** np.arange(K)
    brute = np.convolve(P0, w)[: P0.size]
    assert np.allclose(P1, brute, rtol=1e-11, atol=1e-16)
    return dict(max_rel_err=float(np.max(np.abs(P1 - brute) / np.maximum(brute, 1e-300))))


def t_enumeracao():
    """soma_n contra enumeracao exata de uma pmf discreta pequena."""
    delta, lo = 0.1, -1.0
    pmf = np.zeros(8)
    pmf[0], pmf[3], pmf[7] = 0.5, 0.3, 0.2
    for n in (1, 2, 4):
        S = N.soma_n(pmf, lo, delta, n)
        # enumeracao
        dist = {}
        for combo in itertools.product([0, 3, 7], repeat=n):
            p = 1.0
            for q in combo:
                p *= {0: 0.5, 3: 0.3, 7: 0.2}[q]
            val = n * lo + sum(combo) * delta
            dist[round(val, 9)] = dist.get(round(val, 9), 0.0) + p
        for val, p in dist.items():
            assert abs(S.cauda(val) - sum(pp for vv, pp in dist.items() if vv >= val - 1e-9)) < 1e-12, (n, val)
        assert abs(S.pmf.sum() - 1.0) < 1e-12
    return dict(ok=True)


def t_exata_vs_janela():
    rng = np.random.default_rng(7)
    q = np.arange(600)
    pmf = np.exp(-0.5 * ((q - 250) / 40.0) ** 2) + 0.02 * np.exp(-q / 90.0)
    pmf /= pmf.sum()
    lo, delta = -3.0, 0.01
    res = {}
    for n in (50, 300):
        A = N.soma_n(pmf, lo, delta, n)
        B = N.soma_n(pmf, lo, delta, n, forcar_janela=True)
        assert A.exata and not B.exata
        cA = A.quantil_superior(N.P5)
        cB = B.quantil_superior(N.P5)
        assert abs(cA - cB) < 0.02, (n, cA, cB)
        assert abs(A.cauda(cA) - B.cauda(cA)) < 1e-9 + 1e-3 * A.cauda(cA)
        assert B.fora < 1e-12, B.fora
        res[f"n{n}"] = dict(c_exata=cA, c_janela=cB, fora=B.fora)
    return res


def t_invariantes_celulas(um_path: str):
    info = N.ler_alpha_um(um_path)
    beta = N.beta_de_alpha(info["alpha"])
    g = N.perfil_burst(4, 14.0, 2.0, "damped", 1.0, 0.6)
    perfil = N.perfil_dict("TESTE", g, f_tail=0.8, tau_ms=100.0)
    edges, P0, P1, tau0 = N.celulas(perfil, 20.0, beta)
    assert abs(P0.sum() - 1.0) < 1e-12, P0.sum()
    assert abs(P1.sum() - 1.0) < 1e-9, P1.sum()
    assert np.all(P1 >= beta * P0 * (1 - 1e-12))
    P0f, P1f, lam, lam_c = N.llr_celulas(P0, P1, cap=40.0)
    assert lam.min() >= math.log(beta) - 1e-9
    # media do atraso: E[t1]-E[t0] = tau0 (1-beta)/beta
    mid = 0.5 * (edges[:-1] + edges[1:])
    dm = float((P1 * mid).sum() - (P0 * mid).sum())
    esp = tau0 * (1 - beta) / beta
    assert abs(dm - esp) / esp < 2e-3, (dm, esp)
    return dict(beta=beta, tau0_ms=tau0, atraso_medio_ms=dm, esperado_ms=esp, soma_P0=float(P0.sum()), soma_P1=float(P1.sum()))


def t_mc_is_vs_exato():
    """IS-MC reproduz o limiar analitico da gaussiana (d=1, n=25): c = 12.5 e poder 0.5."""
    d, n = 1.0, 25
    h = 0.01
    edges = np.arange(-14.0, 14.0 + d + h, h)
    P0 = N.massa_gauss_celulas(edges, 0.0, 1.0)
    P1 = N.massa_gauss_celulas(edges, d, 1.0)
    P0, P1, lam, lam_c = N.llr_celulas(P0, P1, cap=60.0)
    delta = 0.01
    p0, p1, lo = N.pmf_rede(P0, P1, lam_c, delta)
    ev = N.avaliar_n(p0, p1, lo, delta, n)
    seed = np.random.SeedSequence([20261022, 0, n])
    mc = N.verificar_mc(P1, lam, lam_c, n, ev["c_n"], 400_000, seed)
    assert abs(mc["c_hat"] - ev["c_n"]) < 0.3, (mc["c_hat"], ev["c_n"])
    assert abs(mc["poder_mc"] - ev["poder"]) < max(0.01, 4 * mc["se_poder"]), (mc["poder_mc"], ev["poder"])
    assert abs(mc["cauda_nula_em_c_lat"] / N.P5 - 1.0) < 0.5, mc["cauda_nula_em_c_lat"]
    return dict(c_lat=ev["c_n"], c_hat=mc["c_hat"], poder_lat=ev["poder"], poder_mc=mc["poder_mc"],
                cauda_nula_mc_sobre_p5=mc["cauda_nula_em_c_lat"] / N.P5)


def t_offset_convolucao(um_path: str):
    """Offset gaussiano do ponto-zero: pico N(0,1) com offset sigma=2 deve virar N(0,sqrt(5)); H1 segue exato."""
    info = N.ler_alpha_um(um_path)
    beta = N.beta_de_alpha(info["alpha"])
    perfil = N.perfil_dict("TESTE", [(1.0, 0.0, 1.0)], 0.0, None, "t", sigma_offset_ms=2.0)
    edges, P0, P1, tau0 = N.celulas(perfil, 20.0, beta)
    ref = N.massa_gauss_celulas(edges, 0.0, math.sqrt(5.0))
    err = float(np.max(np.abs(P0 - ref)))
    # erro esperado O((tau0/sigma)^2/12) ~ 4e-5 do pico (convolucao discreta de massas por celula)
    assert err < 1e-4 * float(ref.max()) + 1e-9, err
    assert abs(P0.sum() - 1.0) < 1e-9 and abs(P1.sum() - 1.0) < 1e-9
    # caudas preservadas (convolucao direta): massa em +12 sigma_total nao pode ser zerada por ruido
    return dict(erro_max_abs=err, pico_ref=float(ref.max()))


def executar(um_path: str) -> dict:
    res = {}
    for nome, fn, args in (
        ("gauss_shift", t_gauss_shift, ()),
        ("iir_vs_pente", t_iir_vs_pente, ()),
        ("enumeracao", t_enumeracao, ()),
        ("exata_vs_janela", t_exata_vs_janela, ()),
        ("invariantes_celulas", t_invariantes_celulas, (um_path,)),
        ("offset_convolucao", t_offset_convolucao, (um_path,)),
        ("mc_is_vs_exato", t_mc_is_vs_exato, ()),
    ):
        res[nome] = fn(*args)
        res[nome]["passou"] = True
        print(f"[teste_nucleo] {nome}: PASSOU", flush=True)
    return res


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    import json
    print(json.dumps(executar(sys.argv[1]), indent=2, default=float))
