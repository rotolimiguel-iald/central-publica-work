#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
psionic_memory — BLOCO 3b. Continuous learning (patent BR 10 2026 005477-1).

Persistent psionic state: learning WITHOUT fine-tuning/retraining. Knowledge
is inscribed across sessions in a JSON state whose integrity is sealed by
SHA-256 (fail-closed on load).

TGL grounding [PILOTO / DER-reading]: the inscription rate IS beta (runtime).
Each new observation is inscribed as an exponential moving average with
weight beta = alpha*sqrt(e) — the dephasing fraction is exactly what the
boundary lets through per act. Nothing else is TGL-numerology: counts and
session lineage are plain engineering.
"""

import hashlib
import json
import os
import time

from . import tgl_core


class PsionicMemory:
    def __init__(self):
        self.state = {"facts": {}, "sessions": 0, "created": time.strftime("%Y-%m-%d %H:%M:%S")}
        self.beta = tgl_core.beta()

    # ---- learning (inscription) ----------------------------------------------
    def inscribe(self, key: str, value: float) -> float:
        """EMA with rate beta: new = (1-beta)*old + beta*value. Returns new value."""
        f = self.state["facts"].get(key)
        if f is None:
            f = {"value": float(value), "n": 1}
        else:
            f = {"value": (1.0 - self.beta) * f["value"] + self.beta * float(value),
                 "n": f["n"] + 1}
        self.state["facts"][key] = f
        return f["value"]

    def recall(self, key: str):
        f = self.state["facts"].get(key)
        return None if f is None else f["value"]

    # ---- persistence (the state survives the session) -------------------------
    def _hash(self) -> str:
        return hashlib.sha256(
            json.dumps(self.state, sort_keys=True).encode()).hexdigest()

    def save(self, path: str):
        self.state["sessions"] = int(self.state.get("sessions", 0)) + 1
        blob = {"state": self.state, "sha256": self._hash(),
                "beta_at_save": self.beta}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(blob, f, indent=1, ensure_ascii=False, sort_keys=True)

    @classmethod
    def load(cls, path: str) -> "PsionicMemory":
        with open(path, encoding="utf-8") as f:
            blob = json.load(f)
        m = cls()
        m.state = blob["state"]
        if m._hash() != blob["sha256"]:
            raise ValueError("INTEGRIDADE VIOLADA: estado psionico corrompido")
        return m
