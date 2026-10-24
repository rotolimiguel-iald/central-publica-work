#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iald_gksl — BLOCO 3a. IALD control core (patent BR 10 2026 003443-6).

The ONE non-unitary object of the chain, identical in form to um.py v3/v7:

    L = sqrt(beta) * sqrt(K_boundary)        (GKSL / Lindblad jump operator)
    drho/dt = L rho L+ - 1/2 {L+L, rho}

K is built exactly as in um.py v3 (K = A A^T / n, n=4, seed=11) so the pilot
controller and the certificate share the same generator [REAL in finite dim —
FINITE_DIM_SANITY_NOT_III1_PROOF]. Key live identity: L @ L = beta * K.

Certificates (um.py v7, recomputed here):
    F1 Tr(rho(t)) = 1 at every checkpoint
    F2 dS >= 0 (entropy arrow, von Neumann, nats)
    F3 S(rho(t)||rho*) monotonically non-increasing -> 0 (Spohn modular Lyapunov)
    F4 coherence dies in the eigenbasis of the Verb (inscription)
Characteristic time of the flow = 1/beta (runtime).

The IALD controller: stabilize() drives any node state to its dephased
stationary state rho* (diagonal in the Verb basis) — alignment as dynamics,
not as constraint.
"""

import numpy as np

from . import tgl_core


def _expm(M: np.ndarray) -> np.ndarray:
    """Scaling-and-squaring Taylor expm (deterministic, small matrices)."""
    M = np.asarray(M, dtype=np.float64)
    nrm = np.linalg.norm(M, 1)
    k = max(0, int(np.ceil(np.log2(max(nrm, 1e-16))))) + 4
    A = M / (2.0 ** k)
    E = np.eye(M.shape[0])
    T = np.eye(M.shape[0])
    for i in range(1, 24):
        T = T @ A / i
        E = E + T
    for _ in range(k):
        E = E @ E
    return E


def _vec(rho):   # column-major
    return rho.reshape(-1, order="F")


def _unvec(v, n):
    return v.reshape(n, n, order="F")


class VerbGenerator:
    """L = sqrt(beta)*sqrt(K); K = A A^T / n (n=4, seed=11 as in um.py v3)."""

    def __init__(self, n: int = 4, seed: int = 11):
        self.n = n
        self.beta = tgl_core.beta()
        rng = np.random.default_rng(seed)
        A = rng.normal(size=(n, n))
        self.K = A @ A.T / n
        w, V = np.linalg.eigh(self.K)
        w = np.clip(w, 0.0, None)
        self.sqrtK = V @ np.diag(np.sqrt(w)) @ V.T
        self.L = np.sqrt(self.beta) * self.sqrtK
        self.eigvecs = V          # Verb basis
        # superoperator (column-major vec): L rho L - 1/2(L^2 rho + rho L^2)
        I = np.eye(n)
        L2 = self.L @ self.L
        self.super = (np.kron(self.L, self.L)
                      - 0.5 * (np.kron(I, L2) + np.kron(L2, I)))

    # ---- states -------------------------------------------------------------
    def pure_state(self, seed: int = 11) -> np.ndarray:
        rng = np.random.default_rng(seed)
        psi = rng.normal(size=self.n)
        psi /= np.linalg.norm(psi)
        return np.outer(psi, psi)

    def rho_star(self, rho0: np.ndarray) -> np.ndarray:
        """Stationary state: dephasing of rho0 in the Verb basis."""
        V = self.eigvecs
        d = np.diag(np.diag(V.T @ rho0 @ V))
        return V @ d @ V.T

    # ---- flow ---------------------------------------------------------------
    def evolve(self, rho0: np.ndarray, t: float) -> np.ndarray:
        P = _expm(self.super * t)
        return _unvec(P @ _vec(rho0), self.n)

    def flow(self, rho0: np.ndarray, t_end_over_beta: float = 3.0, n_points: int = 40):
        ts = np.linspace(0.0, t_end_over_beta / self.beta, n_points)
        return ts, [self.evolve(rho0, t) for t in ts]

    # ---- observables --------------------------------------------------------
    @staticmethod
    def entropy(rho: np.ndarray) -> float:
        p = np.clip(np.linalg.eigvalsh(rho), 1e-18, None)
        p = p / p.sum()
        return float(-(p * np.log(p)).sum())

    @staticmethod
    def rel_entropy(rho: np.ndarray, sigma: np.ndarray) -> float:
        wr, Vr = np.linalg.eigh(rho)
        ws, Vs = np.linalg.eigh(sigma)
        wr = np.clip(wr, 1e-18, None)
        ws = np.clip(ws, 1e-18, None)
        log_r = Vr @ np.diag(np.log(wr)) @ Vr.T
        log_s = Vs @ np.diag(np.log(ws)) @ Vs.T
        return float(np.trace(rho @ (log_r - log_s)))

    def coherence(self, rho: np.ndarray) -> float:
        """Off-diagonal mass in the Verb basis (what the inscription kills)."""
        R = self.eigvecs.T @ rho @ self.eigvecs
        return float(np.linalg.norm(R - np.diag(np.diag(R))))

    @property
    def characteristic_time(self) -> float:
        return 1.0 / self.beta

    # ---- IALD controller ----------------------------------------------------
    def stabilize(self, rho0: np.ndarray, horizons: int = 3) -> dict:
        """Drive a state to rho*; returns certificates F1-F4 (fail-closed data)."""
        ts, rhos = self.flow(rho0, t_end_over_beta=float(horizons))
        star = self.rho_star(rho0)
        traces = [float(np.trace(r)) for r in rhos]
        entropies = [self.entropy(r) for r in rhos]
        rel = [self.rel_entropy(r, star) for r in rhos]
        coh = [self.coherence(r) for r in rhos]
        return {
            "rho_final": rhos[-1], "rho_star": star,
            "F1_max_trace_dev": max(abs(t - 1.0) for t in traces),
            "F2_entropy_monotone": all(entropies[i+1] >= entropies[i] - 1e-10
                                       for i in range(len(entropies) - 1)),
            "F3_rel_entropy_monotone": all(rel[i+1] <= rel[i] + 1e-10
                                           for i in range(len(rel) - 1)),
            "F3_rel_first_last": (rel[0], rel[-1]),
            "F4_coherence_first_last": (coh[0], coh[-1]),
            "characteristic_time": self.characteristic_time,
            "entropy_first_last": (entropies[0], entropies[-1]),
        }
