#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
orchestrator — ESTAGIO B. The complete end-to-end SkyGrid application core.

Runs the FULL pipeline of the aggregating patent (BR 10 2026 004850-0) per
transfer, composing every subsystem block:

  telemetry [DATA/PILOTO-DET]  -> payload frame (real HESE events or orbital)
  ACOM Mirror Crypto (BLOCO 1c) -> 3 ontological shares, fail-closed integrity
  TGL Tensor (BLOCO 2)          -> compression w/ Verb Floor 1-beta (GPU-ready)
  Psi-NET (BLOCO 4)             -> angular addressing + hop estimate
  DOUBLE RAIL (BLOCO 7)         -> Rail-Psi (holographic) vs Rail-E (bytes)
  Proof of Phase QUORUM (A3)    -> >=67% of independent validators seal
  Celula de Reversao (BLOCO 5c) -> angular-phase storage, retention measured
  IALD/GKSL control (BLOCO 3a)  -> stabilization budget = 100/beta [A5 fix]
  Kernel + Psionic memory (A4)  -> verbal filter summary + persistent state

FAULT INJECTION (resilience proof): 'dead' (node down -> rerouted & logged),
'tamper' (corrupted share -> fail-closed ValueError -> rejected & detected),
'noise' (carrier degraded -> rail correlation collapses -> rejected).
The PLACEBO node (claim 3) always runs and MUST be rejected by construction.

Verdict is STRUCTURAL only: ARCHITECTURE_CLOSES when every healthy transfer
is accepted, the placebo is rejected AND every injected fault is detected.
physical_verdict_allowed=False in every output. beta is never a literal —
it comes from tgl_core at runtime. The pilot proves the architecture closes,
NOT that energy flows.
"""

import hashlib
import json
import math
import os
import time
import zlib

import numpy as np

from . import tgl_core
from .acom_crypto import ACOMMirrorCrypto
from .acom_mirror import DimensionalMirror
from .celula_reversao import CelulaReversao
from .dipolo import DipoloTransistor
from .iald_gksl import VerbGenerator
from .kernel_link import GridMemory, KernelProfile
from .psi_net import AngularAddress, HolographicNetwork, QuorumPhaseChain
from .telemetry import TelemetrySource
from .tgl_tensor import TGLTensorAccel, gpu_available

RAIL_THRESHOLD = 0.999
FRAME_SIZE = 256


class SatNode:
    """Orbital node: telemetry source + dipole gate + accel tensor engine."""

    def __init__(self, index: int, seed: int, telemetry_mode: str = "auto"):
        self.node_id = "SAT-%03d" % index
        self.index = index
        self.alive = True
        self.telemetry = TelemetrySource(index, seed, mode=telemetry_mode)
        self.dipolo = DipoloTransistor()

    def extract(self, size: int = FRAME_SIZE) -> np.ndarray:
        frame = self.telemetry.next_frame(size)
        gated = self.dipolo.gate(frame)
        return gated["output"] if gated["open"] else frame


class BaseNode:
    """Terrestrial node: angular-phase storage + delivery bookkeeping."""

    def __init__(self, index: int):
        self.node_id = "BASE-%04d" % index
        self.celula = CelulaReversao(angular_bits=16)
        self.delivered_units = 0.0     # payload units [PILOTO] — NOT energy

    def store_recover_deliver(self, payload: np.ndarray) -> dict:
        pattern = np.abs(payload) + 0.1
        self.celula.charge(pattern)
        recovered = self.celula.discharge()
        a, b = pattern.ravel(), recovered.ravel()
        retention = float(np.corrcoef(a, b)[0, 1]) if a.std() and b.std() else 1.0
        units = float(np.sum(np.abs(recovered)))
        self.delivered_units += units
        return {"retention": retention, "units": units}


class SkyGridOrchestrator:
    """The end-to-end application core (Estagio B)."""

    def __init__(self, n_sats: int = 12, n_bases: int = 12, seed: int = 11,
                 telemetry_mode: str = "auto", faults=(), n_validators: int = 5,
                 state_path: str = None, use_gpu: bool = False):
        self.beta = tgl_core.beta()
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.placebo_rng = np.random.default_rng(seed ^ 0xC0FFEE)
        self.faults = tuple(sorted(set(faults)))
        self.telemetry_mode = telemetry_mode

        self.sats = [SatNode(i, seed * 1000 + i + 1, telemetry_mode)
                     for i in range(n_sats)]
        self.bases = [BaseNode(i) for i in range(n_bases)]

        self.mirror = DimensionalMirror(angular_bits=16)
        self.crypto = ACOMMirrorCrypto(angular_bits=8)
        self.tensor = TGLTensorAccel(bits=10, device="cuda" if use_gpu else None)
        self.chain = QuorumPhaseChain(difficulty=0.1, n_validators=n_validators)
        self.net = HolographicNetwork()
        self.addr = {}
        for node in self.sats + self.bases:
            a = AngularAddress.from_key(node.node_id.encode())
            self.addr[node.node_id] = a
            self.net.register(a)

        # A5: stabilization budget — the honest finding of BLOCO 3: the
        # slowest modular pair dies at ~0.06/beta, so full dephasing takes
        # ~100/beta flow-time (NOT 3/beta). Budget in integrator steps:
        self.stab_horizons = 100.0
        self.stab_budget_steps = int(math.ceil(100.0 / self.beta))
        self.verb = VerbGenerator(n=4, seed=seed)

        # A4: continuous learning wired to the real kernel
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.state_path = state_path or os.path.join(root, "SKYGRID_PSIONIC_STATE.json")
        self.memory = GridMemory(self.state_path)
        self.kernel = KernelProfile()

        self.transfers = []
        self.fault_events = []

    # ---- double rail ---------------------------------------------------------
    def _rail_psi(self, payload: np.ndarray, noise: bool = False) -> np.ndarray:
        r = self.mirror.reflect(payload)
        out = self.mirror.manifest(r)
        if noise:   # injected carrier degradation (fault) — independent stream
            out = out + self.placebo_rng.normal(0, np.abs(out).mean() * 3 + 1.0,
                                                out.shape)
        return out

    @staticmethod
    def _rail_e(payload: np.ndarray) -> np.ndarray:
        return np.frombuffer(payload.astype(np.float64).tobytes(),
                             dtype=np.float64).copy()

    @staticmethod
    def _corr(a: np.ndarray, b: np.ndarray) -> float:
        a, b = a.ravel(), b.ravel()
        if a.std() == 0 or b.std() == 0:
            return 1.0 if np.allclose(a, b) else 0.0
        return float(np.corrcoef(a, b)[0, 1])

    # ---- the full pipeline per transfer ---------------------------------------
    def transfer_full(self, sat: SatNode, base: BaseNode,
                      inject: str = None) -> dict:
        rec = {"from": sat.node_id, "to": base.node_id, "fault_injected": inject,
               "beta_coupled": True}
        t0 = time.perf_counter()

        # 0) dead-node detection happens BEFORE extraction (handled by run())
        payload = sat.extract()
        rec["payload_bytes"] = int(payload.size * 8)

        # 1) security rail: 3 ontological shares, fail-closed integrity
        enc = self.crypto.encrypt(payload)
        if inject == "tamper":     # corrupt the theta share ciphertext
            blob = bytearray(enc.theta_share.encrypted_angles)
            blob[len(blob) // 2] ^= 0xFF
            enc.theta_share.encrypted_angles = bytes(blob)
        try:
            payload_rx = self.crypto.decrypt(enc.psi_share, enc.theta_share,
                                             enc.master_key)
            rec["crypto_ok"] = True
            rec["crypto_corr"] = self._corr(payload, payload_rx)
        except (ValueError, zlib.error) as e:
            # fail-closed: ANY corruption pathway (integrity hash mismatch OR
            # broken ciphertext container -> zlib checksum) rejects the transfer
            rec["crypto_ok"] = False
            rec["crypto_error"] = "%s: %s" % (type(e).__name__, str(e)[:70])
            payload_rx = None

        if payload_rx is None:     # fail-closed: tampered share never proceeds
            rec.update({"accepted": False, "rejected_stage": "crypto",
                        "elapsed_s": time.perf_counter() - t0})
            self.transfers.append(rec)
            if inject:
                self.fault_events.append({"type": inject, "detected": True,
                                          "stage": "crypto", "sat": sat.node_id})
            return rec

        # 2) compression with the Verb Floor (1-beta retention)
        comp = self.tensor.compress_direct(payload_rx)
        payload_c = self.tensor.decompress_direct(comp)
        rec["compression_ratio"] = comp.compression_ratio
        rec["compression_fidelity"] = self._corr(payload_rx, payload_c)
        rec["gpu_active"] = self.tensor.gpu_active

        # 3) routing by angular address
        a_src, a_dst = self.addr[sat.node_id], self.addr[base.node_id]
        rec["hops"] = self.net.hops(a_src, a_dst)

        # 4) double rail cross-check
        psi = self._rail_psi(payload_c, noise=(inject == "noise"))
        e = self._rail_e(payload_c)
        rec["rail_cross_corr"] = self._corr(psi, e)
        rail_ok = rec["rail_cross_corr"] > RAIL_THRESHOLD

        # 5) quorum Proof of Phase seal
        blk = self.chain.mine(payload_c.tobytes(), sat.node_id.encode(),
                              max_iter=20000)
        sealed = bool(blk is not None and self.chain.validate_and_append(blk))
        rec["phase_sealed"] = sealed
        if self.chain.vote_log:
            last = self.chain.vote_log[-1]
            rec["quorum_votes"] = "%d/%d" % (last["votes_yes"], last["votes_total"])

        # 6) storage + delivery at the base
        st = base.store_recover_deliver(psi)
        rec["retention"] = st["retention"]
        rec["delivered_units"] = st["units"]     # [PILOTO] payload units

        rec["accepted"] = bool(rec["crypto_ok"] and rail_ok and sealed)
        if not rec["accepted"]:
            rec["rejected_stage"] = ("rail" if not rail_ok else
                                     "phase" if not sealed else "crypto")
        rec["elapsed_s"] = time.perf_counter() - t0
        self.transfers.append(rec)
        if inject:
            self.fault_events.append({"type": inject,
                                      "detected": not rec["accepted"],
                                      "stage": rec.get("rejected_stage", "-"),
                                      "sat": sat.node_id})
        return rec

    def placebo_transfer(self, sat: SatNode, base: BaseNode) -> dict:
        """Claim 3 negative control: carrier with NO beta coupling (independent
        placebo stream, disjoint seed) — must be rejected by construction."""
        payload = sat.extract()
        psi_noise = self.placebo_rng.normal(size=payload.size)
        corr = self._corr(psi_noise, self._rail_e(payload))
        rec = {"from": sat.node_id, "to": base.node_id, "placebo": True,
               "beta_coupled": False, "rail_cross_corr": corr,
               "accepted": bool(corr > RAIL_THRESHOLD)}
        self.transfers.append(rec)
        return rec

    # ---- IALD control certificate ---------------------------------------------
    def control_certificate(self) -> dict:
        rho0 = self.verb.pure_state(seed=self.seed)
        cert = self.verb.stabilize(rho0, horizons=int(self.stab_horizons))
        coh = self.verb.coherence(cert["rho_final"])
        return {"budget_horizons_over_beta": self.stab_horizons,
                "budget_steps_100_over_beta": self.stab_budget_steps,
                "F1_max_trace_dev": cert["F1_max_trace_dev"],
                "F2_entropy_monotone": bool(cert["F2_entropy_monotone"]),
                "F3_rel_entropy_monotone": bool(cert["F3_rel_entropy_monotone"]),
                "residual_coherence": float(coh)}

    # ---- run -------------------------------------------------------------------
    def run(self) -> dict:
        t_start = time.perf_counter()
        results = []
        # fault scheduling: dead -> sat 1; tamper -> transfer 2; noise -> transfer 3
        dead_index = 1 if "dead" in self.faults and len(self.sats) > 1 else None
        if dead_index is not None:
            self.sats[dead_index].alive = False

        k = 0
        for i, sat in enumerate(self.sats):
            base = self.bases[i % len(self.bases)]
            if not sat.alive:
                # dead node detected -> reroute its slot to the next live sat
                donor = next(s for s in self.sats if s.alive)
                self.fault_events.append({"type": "dead", "detected": True,
                                          "stage": "routing", "sat": sat.node_id,
                                          "rerouted_via": donor.node_id})
                results.append(self.transfer_full(donor, base))
                continue
            inject = None
            if "tamper" in self.faults and k == 2:
                inject = "tamper"
            elif "noise" in self.faults and k == 3:
                inject = "noise"
            results.append(self.transfer_full(sat, base, inject=inject))
            k += 1

        placebo = self.placebo_transfer(
            next(s for s in self.sats if s.alive), self.bases[0])
        cert = self.control_certificate()

        healthy = [r for r in results if not r.get("fault_injected")]
        faulted = [r for r in results if r.get("fault_injected")]
        n_ok = sum(r["accepted"] for r in healthy)
        faults_detected = all(ev["detected"] for ev in self.fault_events)
        elapsed = time.perf_counter() - t_start
        total_bytes = sum(r.get("payload_bytes", 0) for r in results)

        metrics = {
            "acceptance_rate": n_ok / max(len(healthy), 1),
            "mean_rail_corr": float(np.mean([r["rail_cross_corr"]
                                             for r in healthy])) if healthy else 0.0,
            "mean_compression_ratio": float(np.mean(
                [r["compression_ratio"] for r in healthy
                 if "compression_ratio" in r])) if healthy else 0.0,
            "mean_retention": float(np.mean(
                [r["retention"] for r in healthy if "retention" in r])) if healthy else 0.0,
            "throughput_bytes_per_s": total_bytes / max(elapsed, 1e-9),
            "chain_length": len(self.chain.chain),
            "residual_coherence": cert["residual_coherence"],
        }

        # continuous learning: inscribe (rate beta), kernel verbal filter, persist
        ema = self.memory.inscribe_run(metrics)
        summary = self.kernel.manifest_summary(metrics, self.memory)
        self.memory.save()

        verdict_ok = (n_ok == len(healthy) and not placebo["accepted"]
                      and faults_detected)
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "beta_runtime": self.beta,
            "n_sats": len(self.sats), "n_bases": len(self.bases),
            "telemetry_provenance": self.sats[0].telemetry.provenance(),
            "kernel_provenance": self.kernel.provenance(),
            "gpu": {"torch_cuda_available": gpu_available(),
                    "gpu_active": self.tensor.gpu_active},
            "quorum": {"n_validators": len(self.chain.validators),
                       "threshold": 0.67,
                       "blocks_sealed": len(self.chain.chain) - 1},
            "transfers_healthy_accepted": n_ok,
            "transfers_healthy_total": len(healthy),
            "transfers_faulted": len(faulted) + sum(
                1 for ev in self.fault_events if ev["type"] == "dead"),
            "faults_injected": list(self.faults),
            "faults_all_detected": bool(faults_detected),
            "fault_events": self.fault_events,
            "placebo_rejected": not placebo["accepted"],
            "iald_control": cert,
            "metrics": metrics,
            "memory": {"sessions": self.memory.sessions,
                       "resumed": self.memory.resumed,
                       "ema_after": ema},
            "kernel_summary": summary,
            "elapsed_s": elapsed,
            "physical_verdict_allowed": False,
            "verdict": "ARCHITECTURE_CLOSES" if verdict_ok else "OPEN",
        }
        report["seal_sha256"] = hashlib.sha256(
            json.dumps(report, sort_keys=True, default=str).encode()).hexdigest()
        return report
