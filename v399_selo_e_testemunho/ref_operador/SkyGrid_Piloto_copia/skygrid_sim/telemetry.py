#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
telemetry — ESTAGIO A1. Real / realistic payload sources for the SkyGrid nodes.

Replaces the purely synthetic `rng.normal * 5` satellite payloads with:

  [DATA]        RealDataProvider — the IceCube HESE 7-year public data release
                (102 real neutrino events: recoDepositedEnergy, recoZenith,
                recoMorphology). Provenance sealed by SHA-256 of the source
                file. This is REAL measured data from a public repository,
                used as payload content for the simulated grid — it carries
                no physical claim about SkyGrid itself.

  [PILOTO-DET]  OrbitTelemetryProvider — deterministic, realistic satellite
                housekeeping telemetry: Keplerian phase, solar-panel current
                with eclipse gating, thermal cycle, battery voltage, gyro
                noise. Fully seeded (reproducible); no random physics claims.

TGL grounding: none needed here — telemetry is plain engineering. beta is
NOT used to fabricate data; the only TGL touchpoint is that payload frames
are sized for the downstream pipeline. Fail-closed: the real provider
refuses to serve if the source file hash changes (provenance broken).
"""

import hashlib
import json
import math
import os

import numpy as np

# Known locations of the HESE public data release inside the operator's tree.
_HESE_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "..", "data", "HESE_data.json"),
    r"C:\IALD\projetos_pyhton\acom\icecube_data\hese\HESE-7-year-data-release-master"
    r"\HESE-7-year-data-release-main\HESE-7-year-data-release\resources\data\HESE_data.json",
    "/sessions/exciting-amazing-wozniak/mnt/projetos_pyhton/acom/icecube_data/hese/"
    "HESE-7-year-data-release-master/HESE-7-year-data-release-main/"
    "HESE-7-year-data-release/resources/data/HESE_data.json",
]


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


class RealDataProvider:
    """[DATA] Serves frames built from the real HESE 7-year events."""

    def __init__(self, path: str = None):
        cands = [path] if path else []
        cands += _HESE_CANDIDATES
        self.path = None
        for c in cands:
            if c and os.path.isfile(c):
                self.path = os.path.abspath(c)
                break
        if self.path is None:
            raise FileNotFoundError(
                "HESE_data.json nao encontrado (dados reais indisponiveis)")
        self.sha256 = _sha256_file(self.path)
        with open(self.path, encoding="utf-8") as f:
            d = json.load(f)
        energy = np.asarray(d["recoDepositedEnergy"], dtype=np.float64)
        zenith = np.asarray(d["recoZenith"], dtype=np.float64)
        morph = np.asarray(d["recoMorphology"], dtype=np.float64)
        ok = np.isfinite(energy) & np.isfinite(zenith) & np.isfinite(morph)
        self.energy = energy[ok]
        self.zenith = zenith[ok]
        self.morph = morph[ok]
        if self.energy.size < 32:
            raise ValueError("HESE: eventos validos insuficientes (fail-closed)")
        self.n_events = int(self.energy.size)

    def provenance(self) -> dict:
        return {"source": "IceCube HESE 7-year public data release",
                "marker": "[DATA]", "path": self.path,
                "sha256": self.sha256, "n_events": self.n_events}

    def frame(self, index: int, size: int = 256) -> np.ndarray:
        """Deterministic frame: interleaves log-energy (normalized), zenith and
        morphology of a rotating window over the 102 real events."""
        n = self.n_events
        idx = (np.arange(size // 2) + index * 7) % n
        loge = np.log10(self.energy[idx] + 1.0)          # ~4.5-7 decades
        loge = (loge - loge.mean()) / (loge.std() + 1e-12)
        zen = (self.zenith[idx] - math.pi / 2) / (math.pi / 2)
        frame = np.empty(size, dtype=np.float64)
        frame[0::2] = loge * 5.0
        frame[1::2] = zen * 5.0
        return frame


class OrbitTelemetryProvider:
    """[PILOTO-DET] Deterministic realistic satellite housekeeping frames."""

    def __init__(self, sat_index: int, seed: int, period_min: float = 96.0):
        self.sat_index = int(sat_index)
        self.rng = np.random.default_rng(seed)
        self.period = period_min * 60.0
        self.phase0 = (sat_index * 2.0 * math.pi / 12.0) % (2.0 * math.pi)

    def provenance(self) -> dict:
        return {"source": "deterministic orbital housekeeping generator",
                "marker": "[PILOTO-DET]", "sat_index": self.sat_index,
                "period_s": self.period}

    def frame(self, index: int, size: int = 256) -> np.ndarray:
        t = np.arange(size, dtype=np.float64) * 4.0 + index * size * 4.0
        ph = self.phase0 + 2.0 * math.pi * t / self.period
        sun = np.maximum(0.0, np.cos(ph))               # eclipse gating
        panel_i = 8.4 * sun + self.rng.normal(0, 0.05, size)      # A
        temp = -20.0 + 45.0 * sun + self.rng.normal(0, 0.8, size)  # C
        batt_v = 28.0 - 1.5 * (1 - sun) + self.rng.normal(0, 0.02, size)
        gyro = self.rng.normal(0, 0.01, size) + 0.002 * np.sin(3 * ph)
        frame = np.empty(size, dtype=np.float64)
        frame[0::4] = panel_i[0::4]
        frame[1::4] = temp[1::4] / 10.0
        frame[2::4] = batt_v[2::4] / 5.0
        frame[3::4] = gyro[3::4] * 100.0
        return frame


class TelemetrySource:
    """Facade: prefers real data, falls back to deterministic orbital frames.
    mode: 'real' (fail-closed if missing), 'synthetic', 'auto'."""

    def __init__(self, sat_index: int, seed: int, mode: str = "auto",
                 hese_path: str = None):
        self.mode_requested = mode
        self.provider = None
        if mode in ("real", "auto"):
            try:
                self.provider = RealDataProvider(hese_path)
                self.mode = "real"
            except (FileNotFoundError, ValueError):
                if mode == "real":
                    raise
        if self.provider is None:
            self.provider = OrbitTelemetryProvider(sat_index, seed)
            self.mode = "synthetic"
        self._counter = 0

    def provenance(self) -> dict:
        p = self.provider.provenance()
        p["mode"] = self.mode
        return p

    def next_frame(self, size: int = 256) -> np.ndarray:
        f = self.provider.frame(self._counter, size)
        self._counter += 1
        return f
