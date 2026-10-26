#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
acom_crypto — BLOCO 1c. Ontological separation (patent BR 10 2026 003431-2).

Splits a dimensional reflection into three ontologically distinct shares:
    PsiShare   : the H4 states (signs / form)      — knows WHO, not HOW MUCH
    ThetaShare : the quantized angles (magnitudes) — knows HOW MUCH, not WHO
    MasterKey  : the scale (g_max) + integrity hashes + expected F_exp

All three are required to manifest. Integrity is verified by SHA-256 cross
hashes and by the expected expulsion force F_exp (structural signature).

[REAL] Ported from Acom_v17_mirror_crypto.py (torch) to pure numpy.
[PILOTO/HONESTY] The share obfuscation is XOR with a key derived from the
share_id (as in the legacy code). This is ONTOLOGICAL SEPARATION + integrity,
NOT a substitute for standard cryptography; for real deployments wrap shares
in standard AEAD. The security claim of the pilot is the separation itself.
Coupling constant: imported from tgl_core.beta() at runtime (never literal).
"""

import hashlib
import secrets
import time
import zlib
from dataclasses import dataclass, field
from typing import Dict, Any

import numpy as np

from . import tgl_core
from .acom_mirror import DimensionalMirror, MirrorReflection, _unpack2bits, PARITY


# --------------------------------------------------------------------------- shares
@dataclass
class PsiShare:
    share_id: bytes
    encrypted_states: bytes
    state_hash: bytes
    n_elements: int
    shape: tuple
    f_exp: float
    state_entropy: float


@dataclass
class ThetaShare:
    share_id: bytes
    encrypted_angles: bytes
    angle_hash: bytes
    n_elements: int
    angular_bits: int


@dataclass
class MasterKey:
    key_id: bytes
    g_max: float
    shape: tuple
    n_elements: int
    angular_bits: int
    expected_f_exp: float
    expected_entropy: float
    psi_hash: bytes
    theta_hash: bytes
    creation_time: float = field(default_factory=time.time)


@dataclass
class EncryptedReflection:
    psi_share: PsiShare
    theta_share: ThetaShare
    master_key: MasterKey


# --------------------------------------------------------------------------- helpers
def _derive_key(secret: bytes, context: str, length: int) -> bytes:
    out = b""
    counter = 0
    while len(out) < length:
        out += hashlib.sha256(secret + context.encode() + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def _xor(data: bytes, key: bytes) -> bytes:
    return (np.frombuffer(data, dtype=np.uint8) ^ np.frombuffer(key, dtype=np.uint8)).tobytes()


def _sha(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


# --------------------------------------------------------------------------- engine
class ACOMMirrorCrypto:
    def __init__(self, angular_bits: int = 8):
        self.mirror = DimensionalMirror(angular_bits=angular_bits)
        self.angular_bits = angular_bits
        self.beta = tgl_core.beta()   # runtime

    def encrypt(self, data: np.ndarray) -> EncryptedReflection:
        r: MirrorReflection = self.mirror.reflect(data)
        meta = r.metadata

        # raw (uncompressed, unobfuscated) payloads for hashing
        psi_raw = zlib.decompress(r.psi_packed)
        theta_raw = zlib.decompress(r.theta_packed)
        psi_hash, theta_hash = _sha(psi_raw), _sha(theta_raw)

        share_id = secrets.token_bytes(16)
        key_id = secrets.token_bytes(16)

        psi_obf = _xor(psi_raw, _derive_key(share_id, "psi_obfuscation", len(psi_raw)))
        theta_obf = _xor(theta_raw, _derive_key(share_id, "theta_obfuscation", len(theta_raw)))

        return EncryptedReflection(
            psi_share=PsiShare(share_id, zlib.compress(psi_obf, 9), psi_hash,
                               meta["n_elements"], meta["shape"],
                               meta["f_exp"], meta["state_entropy"]),
            theta_share=ThetaShare(share_id, zlib.compress(theta_obf, 9), theta_hash,
                                   meta["n_elements"], meta["angular_bits"]),
            master_key=MasterKey(key_id, meta["g_max"], meta["shape"],
                                 meta["n_elements"], meta["angular_bits"],
                                 meta["f_exp"], meta["state_entropy"],
                                 psi_hash, theta_hash),
        )

    def decrypt(self, psi: PsiShare, theta: ThetaShare, mk: MasterKey,
                verify_integrity: bool = True) -> np.ndarray:
        if psi.share_id != theta.share_id:
            raise ValueError("Shares incompatíveis: IDs diferentes")
        if not (psi.n_elements == theta.n_elements == mk.n_elements):
            raise ValueError("Shares/MasterKey incompatíveis: tamanhos diferentes")

        psi_raw = _xor(zlib.decompress(psi.encrypted_states),
                       _derive_key(psi.share_id, "psi_obfuscation",
                                   len(zlib.decompress(psi.encrypted_states))))
        theta_raw = _xor(zlib.decompress(theta.encrypted_angles),
                         _derive_key(theta.share_id, "theta_obfuscation",
                                     len(zlib.decompress(theta.encrypted_angles))))

        if verify_integrity:
            if _sha(psi_raw) != psi.state_hash or _sha(psi_raw) != mk.psi_hash:
                raise ValueError("INTEGRIDADE VIOLADA: PsiShare não corresponde")
            if _sha(theta_raw) != theta.angle_hash or _sha(theta_raw) != mk.theta_hash:
                raise ValueError("INTEGRIDADE VIOLADA: ThetaShare não corresponde")

        # rebuild a MirrorReflection and manifest through the fold
        meta: Dict[str, Any] = {
            "shape": tuple(mk.shape), "n_elements": mk.n_elements,
            "angular_bits": mk.angular_bits, "g_max": mk.g_max,
        }
        if verify_integrity:
            # F_exp recomputed from the psi states themselves (as in the legacy code)
            states = _unpack2bits(psi_raw, mk.n_elements)
            f_exp = float(PARITY[states].mean()) if mk.n_elements else 0.0
            if abs(f_exp - mk.expected_f_exp) > 0.001:
                raise ValueError("INTEGRIDADE VIOLADA: F_exp não confere "
                                 "(esperado %.4f, obtido %.4f)" % (mk.expected_f_exp, f_exp))

        r = MirrorReflection(zlib.compress(psi_raw, 9), zlib.compress(theta_raw, 9), meta)
        return self.mirror.manifest(r)
