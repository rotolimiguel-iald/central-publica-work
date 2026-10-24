#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skygrid — BLOCO 7. The aggregating patent (BR 10 2026 004850-0).

SkyGrid-Sim: the planetary energy network simulated as a DISTRIBUTED GRAPH OF
SOFTWARE NODES. NOT a physical energy claim — it orchestrates the subsystem
modules (BLOCO 1-6) into the topology of claim 1 and validates every transfer
by the DOUBLE RAIL, with a placebo negative control (claim 3).

Node roles: ExtractorSat (100) = MQC cluster + Dipolo(MANIFEST) + IALD-orbital;
GroundBase (200) = Celula de Reversao storage. Control: IALD/GKSL, Kernel,
Psi-NET Proof of Phase. Physical layer: hardware mocks (no physics asserted).

Double rail: Rail-Psi (holographic carrier) and Rail-E (conventional bytes).
A transfer is ACCEPTED only if both rails agree (corr>0.999) AND the phase
block seals on the chain. The PLACEBO node runs the pipeline WITHOUT the beta
coupling (independent carrier stream) and MUST be rejected by construction.

All TGL is runtime (beta from tgl_core). Each run emits a manifest + SHA-256
seal. The pilot proves the ARCHITECTURE closes, not that energy flows.
"""

import hashlib
import json
import time

import numpy as np

from . import tgl_core
from .acom_mirror import DimensionalMirror
from .tgl_tensor import TGLTensor
from .iald_gksl import VerbGenerator          # noqa: F401 (control layer, available)
from .psionic_memory import PsionicMemory
from .kernel_ontologico import verb_filter    # noqa: F401 (control layer, available)
from .psi_net import PhaseChain, HolographicNetwork, AngularAddress
from .mqc import MQCCell                       # noqa: F401 (node core, available)
from .dipolo import DipoloTransistor
from .celula_reversao import CelulaReversao
from .hardware_mocks import SupercondutorMock, MotorDobraMock, FusaoFrioMock


class ExtractorSat:
    """Orbital node: produces a payload and switches it out (Dipolo MANIFEST)."""

    def __init__(self, node_id: int, seed: int):
        self.node_id = "SAT-%03d" % node_id
        self.rng = np.random.default_rng(seed)
        self.mqc = MQCCell(seed=seed)
        self.dipolo = DipoloTransistor()
        self.tensor = TGLTensor(bits=10)

    def extract(self, size: int = 256) -> np.ndarray:
        payload = self.rng.normal(size=size) * 5.0
        gated = self.dipolo.gate(payload)
        return gated["output"] if gated["open"] else payload


class GroundBase:
    """Terrestrial node: stores the payload by angular phase (Celula)."""

    def __init__(self, node_id: int):
        self.node_id = "BASE-%04d" % node_id
        self.celula = CelulaReversao(angular_bits=16)

    def store_and_recover(self, payload: np.ndarray) -> np.ndarray:
        self.celula.charge(np.abs(payload) + 0.1)
        return self.celula.discharge()


class SkyGridSim:
    """The distributed graph. Small by default; scales to the 144-sat topology."""

    def __init__(self, n_sats: int = 6, n_bases: int = 6, seed: int = 11):
        self.beta = tgl_core.beta()
        self.rng = np.random.default_rng(seed)
        # dedicated, independent stream for the placebo carrier — must NEVER
        # coincide with a satellite payload stream (avoids the false-negative
        # where an accidentally-shared seed makes noise == payload/5).
        self.placebo_rng = np.random.default_rng(seed ^ 0xC0FFEE)
        # satellite seeds offset far from the sim/placebo seeds
        self.sats = [ExtractorSat(i, seed * 1000 + i + 1) for i in range(n_sats)]
        self.bases = [GroundBase(i) for i in range(n_bases)]
        self.mirror = DimensionalMirror(angular_bits=16)
        self.chain = PhaseChain(difficulty=0.1)
        self.net = HolographicNetwork()
        for node in self.sats + self.bases:
            self.net.register(AngularAddress.from_key(node.node_id.encode()))
        self.memory = PsionicMemory()
        self.hw = {"supercondutor": SupercondutorMock(),
                   "motor_dobra": MotorDobraMock(), "fusao": FusaoFrioMock()}
        self.transfers = []

    # -- the double rail ------------------------------------------------------
    def _rail_psi(self, payload: np.ndarray) -> np.ndarray:
        r = self.mirror.reflect(payload)
        return self.mirror.manifest(r)

    @staticmethod
    def _rail_e(payload: np.ndarray) -> np.ndarray:
        return np.frombuffer(payload.astype(np.float64).tobytes(), dtype=np.float64).copy()

    @staticmethod
    def _cross_check(a: np.ndarray, b: np.ndarray) -> float:
        a, b = a.ravel(), b.ravel()
        if a.std() == 0 or b.std() == 0:
            return 1.0 if np.allclose(a, b) else 0.0
        return float(np.corrcoef(a, b)[0, 1])

    def transfer(self, sat: ExtractorSat, base: GroundBase) -> dict:
        payload = sat.extract()
        psi = self._rail_psi(payload)
        e = self._rail_e(payload)
        corr_psi = self._cross_check(psi, e)
        recovered = base.store_and_recover(psi)
        blk = self.chain.mine(payload.tobytes(), sat.node_id.encode(), max_iter=20000)
        accepted = bool(corr_psi > 0.999 and blk is not None
                        and self.chain.validate_and_append(blk))
        rec = {"from": sat.node_id, "to": base.node_id, "beta_coupled": True,
               "rail_cross_corr": corr_psi, "phase_sealed": blk is not None,
               "accepted": accepted,
               "recovered_pattern_corr": self._cross_check(np.abs(payload) + 0.1, recovered)}
        self.transfers.append(rec)
        return rec

    def placebo_transfer(self, sat: ExtractorSat, base: GroundBase) -> dict:
        """Negative control (claim 3): the placebo cavity has NO beta coupling,
        so Rail-Psi carries an INDEPENDENT stream (dedicated placebo_rng, seed
        disjoint from every payload stream). By construction the carrier shares
        no information with the payload, so the cross-check fails for any RNG
        ordering — not by accident of stream interleaving."""
        payload = sat.extract()
        psi_noise = self.placebo_rng.normal(size=payload.size)
        e = self._rail_e(payload)
        corr = self._cross_check(psi_noise, e)
        accepted = bool(corr > 0.999)
        rec = {"from": sat.node_id, "to": base.node_id, "placebo": True,
               "beta_coupled": False, "rail_cross_corr": corr, "accepted": accepted}
        self.transfers.append(rec)
        return rec

    # -- run + seal -----------------------------------------------------------
    def run(self) -> dict:
        results = []
        for i, sat in enumerate(self.sats):
            base = self.bases[i % len(self.bases)]
            results.append(self.transfer(sat, base))
        placebo = self.placebo_transfer(self.sats[0], self.bases[0])
        n_ok = sum(r["accepted"] for r in results)
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "beta_runtime": self.beta,
            "n_sats": len(self.sats), "n_bases": len(self.bases),
            "transfers_accepted": n_ok, "transfers_total": len(results),
            "all_transfers_ok": n_ok == len(results),
            "placebo_rejected": not placebo["accepted"],
            "chain_length": len(self.chain.chain),
            "hardware_layer": {k: v.__class__.__name__ for k, v in self.hw.items()},
            "physical_verdict_allowed": False,
            "verdict": "ARCHITECTURE_CLOSES" if (n_ok == len(results)
                        and not placebo["accepted"]) else "OPEN",
        }
        report["seal_sha256"] = hashlib.sha256(
            json.dumps(report, sort_keys=True).encode()).hexdigest()
        return report
