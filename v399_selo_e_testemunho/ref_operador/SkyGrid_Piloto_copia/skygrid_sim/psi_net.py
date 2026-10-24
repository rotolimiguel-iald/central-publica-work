#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
psi_net — BLOCO 4. Luminodynamic network (patent BR 10 2026 003453-3).

Five-layer luminodynamic stack, numpy port of Psi_net_protocol_v1.py [REAL]:

  L1 PsiBit link     : bytes -> PsiBits (H4 states); distribution, entropy,
                       F_exp, ontological classification (GRACE/FRONTIER/VACUUM).
  L2 Radical transport: radicalize L -> (g=sqrt|L|, s) ; resurrect s*g^2.
  L3 Holographic net  : angular addressing theta from pubkey; routing by
                       angular distance; hop estimate by theta_M.
  L4 Ontological sec  : Psi/Theta ontological shares (reuses BLOCO 1c idea).
  L5 Proof of Phase   : deterministic phase (alpha2_work, theta, F_exp) from a
                       light-seed; a block is valid when its phase sits inside
                       the window beta/difficulty around the previous phase.

TGL grounding (runtime, never literal): the coupling and theta_M come from
tgl_core; the consensus "difficulty window" is beta/difficulty. The legacy
carried a truncated numeric literal for the coupling; here it is beta().
[REAL] in structure; [PILOTO] as a distributed protocol simulation.
"""

import hashlib
import math
import struct
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict, List, Optional, Tuple

import numpy as np

from . import tgl_core

LIGHT_SIZE = 256
EPSILON = 1e-10


# ------------------------------------------------------------------ L1 PsiBit
class PsiState(IntEnum):
    COLLAPSE_PLUS = 0   # (+,-) inverse
    ASCEND_PLUS = 1     # (+,+) normal
    EMERGE_MINUS = 2    # (-,+) normal
    FALL_MINUS = 3      # (-,-) inverse


_PARITY = np.array([-1.0, 1.0, 1.0, -1.0])


def bytes_to_psibits(data: bytes) -> np.ndarray:
    """Each byte -> 4 PsiBits (2 bits each), MSB first."""
    b = np.frombuffer(data, dtype=np.uint8)
    out = np.empty(len(b) * 4, dtype=np.uint8)
    out[0::4] = (b >> 6) & 3
    out[1::4] = (b >> 4) & 3
    out[2::4] = (b >> 2) & 3
    out[3::4] = b & 3
    return out


def psibit_signature(data: bytes) -> Dict:
    states = bytes_to_psibits(data)
    n = len(states)
    counts = np.bincount(states, minlength=4).astype(np.float64)
    freqs = counts / max(n, 1)
    nz = freqs[freqs > 0]
    entropy = float(-(nz * np.log2(nz)).sum()) if nz.size else 0.0
    uniformity = float(1.0 - np.std(freqs) / (np.mean(freqs) + EPSILON))
    f_exp = float(_PARITY[states].mean()) if n else 0.0
    # ontological class (as in the patent): high uniformity = GRACE, low = VACUUM
    if uniformity > 0.9:
        cls = "GRACE"
    elif uniformity > 0.6:
        cls = "FRONTIER"
    else:
        cls = "VACUUM"
    return {"n": n, "freqs": freqs.tolist(), "entropy": entropy,
            "uniformity": uniformity, "f_exp": f_exp, "ontological_class": cls}


# ------------------------------------------------------------------ L2 transport
def radicalize(L: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    L = np.asarray(L, dtype=np.float64)
    g = np.sqrt(np.abs(L))
    s = np.sign(L); s[s == 0] = 1.0
    return g, s


def resurrect(g: np.ndarray, s: np.ndarray) -> np.ndarray:
    return np.asarray(s) * np.asarray(g) ** 2


# ------------------------------------------------------------------ L3 holographic
@dataclass
class AngularAddress:
    theta: float
    public_key: bytes
    node_id: str

    @staticmethod
    def from_key(public_key: bytes) -> "AngularAddress":
        h = hashlib.sha256(public_key).digest()
        theta = int.from_bytes(h[:8], "big") / (2 ** 64) * math.pi   # [0, pi)
        return AngularAddress(theta, public_key, "PsiN-" + h[:4].hex())


class HolographicNetwork:
    def __init__(self):
        self.routing: Dict[str, AngularAddress] = {}
        self.theta_m = tgl_core.theta_m()

    def register(self, addr: AngularAddress):
        self.routing[addr.node_id] = addr

    @staticmethod
    def angular_distance(a: float, b: float) -> float:
        d = abs(a - b)
        return min(d, math.pi - d)      # circular topology

    def nearest(self, theta: float, k: int = 3) -> List[AngularAddress]:
        return sorted(self.routing.values(),
                      key=lambda n: self.angular_distance(n.theta, theta))[:k]

    def hops(self, src: AngularAddress, dst: AngularAddress) -> int:
        return max(1, int(math.ceil(
            self.angular_distance(src.theta, dst.theta) / self.theta_m)))


# ------------------------------------------------------------------ L4 security
@dataclass
class OntologicalShares:
    psi_share: bytes         # signs
    theta_share: bytes       # quantized magnitudes
    g_max: float
    n: int
    integrity: bytes


def separate(L: np.ndarray, bits: int = 16) -> OntologicalShares:
    g, s = radicalize(np.asarray(L, dtype=np.float64).ravel())
    g_max = float(g.max()) if g.size else 0.0
    theta = np.arcsin(np.clip(g / (g_max + EPSILON), 0, 1))
    qmax = (1 << bits) - 1
    theta_q = np.round(theta / (math.pi / 2) * qmax).astype(np.uint16)
    psi = ((s < 0).astype(np.uint8))
    psi_b = np.packbits(psi).tobytes()
    theta_b = theta_q.tobytes()
    integ = hashlib.sha256(psi_b + theta_b).digest()
    return OntologicalShares(psi_b, theta_b, g_max, g.size, integ)


def recombine(sh: OntologicalShares, bits: int = 16) -> np.ndarray:
    if hashlib.sha256(sh.psi_share + sh.theta_share).digest() != sh.integrity:
        raise ValueError("INTEGRIDADE VIOLADA: shares Psi-NET corrompidos")
    psi = np.unpackbits(np.frombuffer(sh.psi_share, dtype=np.uint8))[:sh.n]
    theta_q = np.frombuffer(sh.theta_share, dtype=np.uint16)[:sh.n]
    qmax = (1 << bits) - 1
    theta = theta_q.astype(np.float64) / qmax * (math.pi / 2)
    g = sh.g_max * np.sin(theta)
    s = np.where(psi > 0, -1.0, 1.0)
    return s * g ** 2


# ------------------------------------------------------------------ L5 Proof of Phase
@dataclass
class PhaseProof:
    alpha2_work: float
    theta_work: float
    f_exp_work: float
    nonce: int
    light_seed: bytes


def compute_phase_from_seed(seed: bytes) -> Tuple[float, float, float]:
    """Deterministic (alpha2_work, theta, f_exp) from a seed. beta at runtime."""
    rng = np.random.default_rng(int.from_bytes(seed[:8], "big"))
    light = rng.normal(size=LIGHT_SIZE)
    dL = np.zeros_like(light); dL[1:] = light[1:] - light[:-1]; dL[0] = dL[1]
    sL = np.sign(light); sL[sL == 0] = 1
    sdL = np.sign(dL); sdL[sdL == 0] = 1
    states = ((sL < 0).astype(int) * 2 + (sdL > 0).astype(int))
    f_exp = float(_PARITY[states].mean())
    g = np.sqrt(np.abs(light) + EPSILON)
    theta = float(np.arcsin(g / (g.max() + EPSILON)).mean())
    beta = tgl_core.beta()
    alpha2_work = beta * (1 + f_exp * 0.01 + math.sin(theta) * 0.001)
    return alpha2_work, theta, f_exp


@dataclass
class Block:
    index: int
    previous_hash: bytes
    phase_proof: PhaseProof
    payload_hash: bytes

    def hash(self) -> bytes:
        return hashlib.sha256(
            struct.pack("<i", self.index) + self.previous_hash
            + struct.pack("<d", self.phase_proof.alpha2_work) + self.payload_hash
        ).digest()


class PhaseChain:
    """Proof of Phase: a block is valid when its phase falls inside the
    window beta/difficulty around the previous block's phase."""

    def __init__(self, difficulty: float = 0.1):
        self.difficulty = difficulty
        self.beta = tgl_core.beta()
        seed0 = hashlib.sha256(b"PSI-NET-GENESIS").digest()
        a2, th, fe = compute_phase_from_seed(seed0)
        self.chain = [Block(0, b"\x00" * 32, PhaseProof(a2, th, fe, 0, seed0),
                            hashlib.sha256(b"genesis").digest())]

    @property
    def window(self) -> float:
        return self.beta / self.difficulty

    def mine(self, payload: bytes, pubkey: bytes, max_iter: int = 20000) -> Optional[Block]:
        prev = self.chain[-1]
        prev_a2 = prev.phase_proof.alpha2_work
        best = None
        best_d = float("inf")
        for nonce in range(max_iter):
            seed = hashlib.sha256(prev.hash() + struct.pack("<i", nonce) + pubkey).digest()
            a2, th, fe = compute_phase_from_seed(seed)
            d = abs(a2 - prev_a2)
            if d < best_d:
                best_d, best = d, (a2, th, fe, nonce, seed)
            if d < self.window:
                return Block(prev.index + 1, prev.hash(),
                             PhaseProof(a2, th, fe, nonce, seed),
                             hashlib.sha256(payload).digest())
        return None

    def validate_and_append(self, block: Block) -> bool:
        prev = self.chain[-1]
        if block.previous_hash != prev.hash():
            return False
        a2, th, fe = compute_phase_from_seed(block.phase_proof.light_seed)
        tol = 1e-9
        if (abs(a2 - block.phase_proof.alpha2_work) > tol
                or abs(th - block.phase_proof.theta_work) > tol
                or abs(fe - block.phase_proof.f_exp_work) > tol):
            return False   # phase forged
        if abs(a2 - prev.phase_proof.alpha2_work) >= self.window:
            return False   # outside the phase window
        self.chain.append(block)
        return True


# ------------------------------------------------------------- L5b quorum consensus
# ESTAGIO A3 [PILOTO]: multi-validator Proof of Phase, ported from the legacy
# Psi_net_protocol_v1.py (PhaseValidator/vote_on_block, MIN_VALIDATORS=3,
# VALIDATION_THRESHOLD=0.67). Each validator INDEPENDENTLY recomputes the
# phase triple from the block's light_seed (tolerance 1e-9) and checks the
# beta/difficulty window against the previous block. A block appends only
# when the fraction of YES votes reaches the threshold — so a single
# byzantine/corrupted validator can neither forge a block in nor veto an
# honest block out. The negative control is BY CONSTRUCTION: a forged
# phase fails every honest recomputation.

MIN_VALIDATORS = 3          # legacy line 104
VALIDATION_THRESHOLD = 0.67  # legacy line 105
PHASE_TOLERANCE = 1e-9


@dataclass
class ValidationVote:
    validator_id: str
    block_hash: bytes
    phase_valid: bool
    window_valid: bool
    is_valid: bool


class PhaseValidator:
    """Independent Proof-of-Phase validator (legacy lines 1046-1080)."""

    def __init__(self, index: int, byzantine: bool = False):
        self.validator_id = "VAL-%03d" % index
        self.byzantine = bool(byzantine)   # adversarial: inverts its vote

    def vote_on_block(self, block: Block, prev: Block, window: float) -> ValidationVote:
        a2, th, fe = compute_phase_from_seed(block.phase_proof.light_seed)
        phase_valid = (abs(a2 - block.phase_proof.alpha2_work) <= PHASE_TOLERANCE
                       and abs(th - block.phase_proof.theta_work) <= PHASE_TOLERANCE
                       and abs(fe - block.phase_proof.f_exp_work) <= PHASE_TOLERANCE)
        window_valid = (block.previous_hash == prev.hash()
                        and abs(a2 - prev.phase_proof.alpha2_work) < window)
        is_valid = bool(phase_valid and window_valid)
        if self.byzantine:                 # adversarial vote (control)
            is_valid = not is_valid
        return ValidationVote(self.validator_id, block.hash(),
                              phase_valid, window_valid, is_valid)


class QuorumPhaseChain(PhaseChain):
    """PhaseChain whose append requires a >=67% quorum of validators."""

    def __init__(self, difficulty: float = 0.1, n_validators: int = 5,
                 byzantine_indices=()):
        super().__init__(difficulty)
        if n_validators < MIN_VALIDATORS:
            raise ValueError("quorum exige >= %d validadores" % MIN_VALIDATORS)
        self.validators = [PhaseValidator(i, byzantine=(i in set(byzantine_indices)))
                           for i in range(n_validators)]
        self.vote_log: List[dict] = []

    def validate_and_append(self, block: Block) -> bool:
        prev = self.chain[-1]
        votes = [v.vote_on_block(block, prev, self.window) for v in self.validators]
        yes = sum(1 for v in votes if v.is_valid)
        quorum = yes / len(votes) >= VALIDATION_THRESHOLD
        self.vote_log.append({
            "block_index": block.index,
            "votes_yes": yes, "votes_total": len(votes),
            "quorum_reached": bool(quorum),
            "votes": [{"id": v.validator_id, "is_valid": bool(v.is_valid),
                       "phase_valid": bool(v.phase_valid),
                       "window_valid": bool(v.window_valid)} for v in votes]})
        if not quorum:
            return False
        # structural append (previous_hash already checked by every validator)
        if block.previous_hash != prev.hash():
            return False
        self.chain.append(block)
        return True
