#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kernel_link — ESTAGIO A4. Continuous learning wired to the REAL IALD kernel.

Two pieces [PILOTO]:

  KernelProfile  — loads the operator's real IALD kernel text (v11 preferred,
                   v6 fallback), seals its SHA-256 as provenance, and applies
                   the kernel's VERBAL FILTER rule to run summaries: only the
                   beta-fraction of metrics with the largest information
                   (deviation from memory) is MANIFESTED; the rest is pruned
                   (the kernel's "max ~1.2% manifested / compress" rule,
                   IALD_Kernel_v11 lines 154-196, realized here with
                   beta = tgl_core.beta() at runtime — never a literal).

  GridMemory     — persistent psionic state of the WHOLE GRID across runs
                   (wraps BLOCO 3b PsionicMemory): inscribes run metrics as
                   EMA with rate beta, increments the session lineage and
                   fail-closes on tampered state files.

No physics asserted. The kernel file is used as PROVENANCE + rule source;
this module does not claim the grid "is" the IALD — it links the pilot's
continuous-learning layer to the operator's real kernel artifact.
"""

import hashlib
import os

import numpy as np

from . import tgl_core
from .kernel_ontologico import verb_filter
from .psionic_memory import PsionicMemory

_KERNEL_CANDIDATES = [
    r"C:\IALD\projetos_pyhton\IALD\Atualização Kernel\IALD_Kernel_v11.txt",
    r"C:\IALD\projetos_pyhton\IALD\IALD_Kernel_v6.txt",
    "/sessions/exciting-amazing-wozniak/mnt/projetos_pyhton/IALD/"
    "Atualização Kernel/IALD_Kernel_v11.txt",
    "/sessions/exciting-amazing-wozniak/mnt/projetos_pyhton/IALD/IALD_Kernel_v6.txt",
]


class KernelProfile:
    """Provenance-sealed link to the operator's real IALD kernel text."""

    def __init__(self, path: str = None):
        cands = ([path] if path else []) + _KERNEL_CANDIDATES
        self.path = None
        for c in cands:
            if c and os.path.isfile(c):
                self.path = os.path.abspath(c)
                break
        self.beta = tgl_core.beta()
        if self.path is not None:
            with open(self.path, "rb") as f:
                blob = f.read()
            self.sha256 = hashlib.sha256(blob).hexdigest()
            self.kernel_version = os.path.basename(self.path)
            self.linked = True
        else:                       # kernel file absent: rule still applies,
            self.sha256 = None      # provenance marked as unlinked
            self.kernel_version = "builtin-rule-only"
            self.linked = False

    def provenance(self) -> dict:
        return {"kernel": self.kernel_version, "sha256": self.sha256,
                "linked": self.linked, "beta_runtime": self.beta,
                "marker": "[PILOTO]"}

    def manifest_summary(self, metrics: dict, memory: "GridMemory" = None) -> dict:
        """The kernel's verbal filter applied to a metrics dict: the weight of
        each metric is its |deviation| from the remembered (EMA) value —
        information, not magnitude. verb_filter (BLOCO 3c) keeps only the
        components >= beta*max and renormalizes. Returns manifested subset."""
        keys = sorted(metrics.keys())
        vals = np.array([float(metrics[k]) for k in keys], dtype=np.float64)
        if memory is not None:
            remembered = np.array(
                [memory.mem.recall("metric/" + k) or 0.0 for k in keys])
            w = np.abs(vals - remembered)
        else:
            w = np.abs(vals)
        if not np.any(w > 0):
            w = np.ones_like(w)
        w_f, stats = verb_filter(w)
        manifested = {k: metrics[k] for k, wf in zip(keys, w_f) if wf > 0}
        pruned = [k for k, wf in zip(keys, w_f) if wf == 0]
        return {"manifested": manifested, "pruned_keys": pruned,
                "filter_stats": stats}


class GridMemory:
    """Persistent psionic state of the grid across sessions (BLOCO 3b)."""

    def __init__(self, state_path: str):
        self.state_path = state_path
        if os.path.isfile(state_path):
            self.mem = PsionicMemory.load(state_path)   # fail-closed on tamper
            self.resumed = True
        else:
            self.mem = PsionicMemory()
            self.resumed = False

    @property
    def sessions(self) -> int:
        return int(self.mem.state.get("sessions", 0))

    def inscribe_run(self, metrics: dict) -> dict:
        """EMA-inscribe each metric with rate beta; returns new values."""
        out = {}
        for k, v in sorted(metrics.items()):
            try:
                out[k] = self.mem.inscribe("metric/" + k, float(v))
            except (TypeError, ValueError):
                continue
        return out

    def save(self):
        self.mem.save(self.state_path)
