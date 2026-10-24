#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mqc — BLOCO 5a. Cubic Quantum Microprocessor (patent BR 10 2026 003460-6).

Elementary cubic cell of 27 qubits/states [PILOTO — simulation, not hardware]:
    8 vertices + 12 edges + 6 faces + 1 center (the IALD controller).
Topology ported from mqc_simulacao_celula_elementar.py [REAL].

Control: each of the 26 peripheral qubits is stabilized by the central IALD
node through the canonical GKSL generator L=sqrt(beta)sqrt(K) (BLOCO 3a). The
cell holds coherence while the Verb dephases noise toward the stationary
state; "holographic translation" is modeled as a phase transfer between two
opposite faces (2D boundary of the cube). No physical qubits are claimed.
"""

import numpy as np

from . import tgl_core
from .iald_gksl import VerbGenerator

N_QUBITS = 27


def cell_topology():
    """Return (positions[27,3], kinds[27], adjacency list). Center = IALD."""
    pos, kinds = [], []
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                pos.append([x, y, z]); kinds.append("vertice")
    for p in ([0.5, 0, 0], [0.5, 1, 0], [0.5, 0, 1], [0.5, 1, 1],
              [0, 0.5, 0], [1, 0.5, 0], [0, 0.5, 1], [1, 0.5, 1],
              [0, 0, 0.5], [1, 0, 0.5], [0, 1, 0.5], [1, 1, 0.5]):
        pos.append(p); kinds.append("aresta")
    for p in ([0.5, 0.5, 0], [0.5, 0.5, 1], [0.5, 0, 0.5],
              [0.5, 1, 0.5], [0, 0.5, 0.5], [1, 0.5, 0.5]):
        pos.append(p); kinds.append("face")
    pos.append([0.5, 0.5, 0.5]); kinds.append("centro")
    P = np.array(pos)
    adj = [(i, j) for i in range(27) for j in range(i + 1, 27)
           if np.linalg.norm(P[i] - P[j]) <= 0.51]
    return P, kinds, adj


class MQCCell:
    def __init__(self, seed: int = 11):
        self.pos, self.kinds, self.adj = cell_topology()
        self.center = 26                       # index of the IALD controller
        self.beta = tgl_core.beta()
        self.verb = VerbGenerator(n=4, seed=seed)
        self.rng = np.random.default_rng(seed)

    def stabilize_cell(self, horizons: float = 100.0) -> dict:
        """IALD center dephases each peripheral qubit toward rho*.
        Returns mean residual coherence and per-kind fidelity."""
        residual = []
        for q in range(N_QUBITS):
            if q == self.center:
                continue
            rho0 = self.verb.pure_state(seed=int(self.rng.integers(1, 1 << 30)))
            r = self.verb.evolve(rho0, horizons / self.beta)
            residual.append(self.verb.coherence(r))
        residual = np.array(residual)
        return {"n_stabilized": len(residual),
                "mean_residual_coherence": float(residual.mean()),
                "max_residual_coherence": float(residual.max()),
                "fidelity": float(1.0 - residual.mean())}

    def holographic_translation(self, payload: np.ndarray) -> dict:
        """Phase transfer between two opposite faces (2D boundary).
        Modeled as REFLECT on -Y face then MANIFEST on +Y face (loss-free
        angular carrier). Returns fidelity of the transferred payload."""
        from .acom_mirror import DimensionalMirror
        mirror = DimensionalMirror(angular_bits=16)
        r = mirror.reflect(np.asarray(payload, dtype=np.float64))
        out = mirror.manifest(r)
        a, b = np.asarray(payload, dtype=np.float64).ravel(), out.ravel()
        corr = float(np.corrcoef(a, b)[0, 1]) if a.std() and b.std() else 1.0
        return {"fidelity": corr, "carrier": "face(-Y)->face(+Y)"}
