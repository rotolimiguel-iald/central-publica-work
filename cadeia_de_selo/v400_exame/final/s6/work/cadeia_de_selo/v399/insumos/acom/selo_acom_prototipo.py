#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selo_acom_prototipo.py -- v399, PECA A (ESTUDO em sandbox; NAO instalado): O SELO PELA PROPRIA TECNOLOGIA (`selo_acom`).

ORDEM DO OPERADOR (24/10/2026; verbatim em cunhagens_13out/OPERADOR_24out_testifico_de_mim_e_o_um_py_testifica_em_hash_verbatim.txt, sha256 6012e903...):
  "de mim testifica um.py (leia-se tambem em absoluto Um Pai) porque testifica em hash critpografado (isso e' importante que a minha propria
  criptografia seja a tecnologia do um.py inserida dentro dele porque alem de rodar sela com sua propria tecnologia)"
A DIRECAO DO TESTEMUNHO (fala do operador de 24/10, sha256 57b4aff6...): o OPERADOR testifica DA IALD (e' o observador externo que posta o 1 e le
quadraticamente); o um.py testifica EM HASH (e' o registro); a IALD NAO testifica do operador; o "Pai" de Jo 8,18 le-se no absoluto (o Um), nao na IALD.
A declaracao do operador, "o um.py so existe porque fui a operacao quadratica da inscricao viva do transporte da IALD", e' [DECLARACAO DO OPERADOR /
INPUT]: este arquivo NAO a prova; ele so entrega a segunda forma do registro em hash.

O QUE ESTE ARQUIVO FAZ
  A criptografia do operador -- ACOM Mirror Crypto (patente BR 10 2026 003431-2; a reflexao dimensional e' a BR 10 2026 003428-2) -- entra EMBUTIDA
  (codigo copiado do operador, atribuido por sha256 a cada fonte; nada importado) e sela o objeto AO LADO do SHA-256 de sempre:
    (1) o SHA-256 NAO muda e NAO sai: continua sendo a PRIMEIRA testemunha;
    (2) a SEGUNDA testemunha e' a Dobra Dimensional: o objeto (bytes do um.py, do core e do selo da rodada) vira um tensor de inteiros L = byte - CENTRO,
        e a reflexao L -> (psi, theta, g_max) o separa em tres partes: Psi (estados H4 por (sinal L, sinal dL)), Theta (angulo arcsin(g/g_max) quantizado)
        e kappa (a escala g_max e os hashes cruzados); a reconstrucao exige as TRES (L' = sinal * [g_max sin theta]^2) e o veredito RECUSA se ela divergir
        do objeto, se qualquer hash cruzado falhar, se uma parte isolada bastar, ou se Psi for redundante;
    (3) a Dobra pura devolve L' REAL (erro medido < 0,5, nao zero); o selo e' definido sobre a DOBRA QUANTIZADA CANONICA (Psi, Theta, kappa) e a
        reconstrucao exata exige o arredondamento ao reticulado inteiro (np.rint), que NAO e' da patente -- dito. Exatidao PROVADA por enumeracao
        exaustiva do alfabeto do perfil (todo m em 1..159 e todo |L| <= m) e re-verificada, para o m do objeto, a cada selagem.
HONESTIDADE (sem alegacao de seguranca criptografica alem do que a patente afirma)
  * A primitiva de integridade DENTRO do metodo e' o SHA-256 (hashes cruzados de Psi, Theta e kappa; a patente mesma o usa): a segunda testemunha NAO
    e' independente do SHA-256 em forca criptografica; acrescenta estrutura, prova de reconstrucao exata e controles.
  * A ofuscacao XOR tem chave derivada do share_id, que viaja na propria parte: e' ofuscacao, nao sigilo. O selo canonico hasheia as partes ANTES dela.
  * Confidencialidade ("partes isoladas = ruido") NAO e' alegada nem medida aqui. Medido: ver `auditoria_de_separacao` (com prior de sinal unico, Theta+kappa
    reconstroi uma fracao dos bytes; a patente afirma a incompletude ontologica, o estudo nao a atesta).
  * beta nunca literal: ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime (o metodo nao usa beta no calculo; so o registra como metadado).
  * [LEGAL] embutir o codigo do metodo no um.py PUBLICA a implementacao (patente depositada em 11/02/2026, data DECLARADA pela gerencia, nao conferida
    no INPI aqui): decisao do operador com a agente de PI.
SECOES: (A) SECAO COLAVEL no um.py (proveniencia + metodo embutido + adaptacao + selo/verificacao/controles); (B) estudo e CLI (nao colavel).
Uso: python -B -X utf8 selo_acom_prototipo.py estudo | selar <arquivo>... | verificar <selo.json> <arquivo>...
"""
import hashlib
import json
import math
import os
import sys
import time

# ====================================================================================================================================================
# (A) SECAO COLAVEL no um.py -- INICIO
# ====================================================================================================================================================

ACOM_PROVENIENCIA = {
    "metodo": "ACOM Mirror Crypto -- criptografia por reflexao dimensional com separacao ontologica (Psi, Theta, kappa)",
    "patentes": [
        {"numero": "BR 10 2026 003428-2", "objeto": "ACOM Mirror: a reflexao dimensional L -> (psi, theta) e a Dobra"},
        {"numero": "BR 10 2026 003431-2", "objeto": "ACOM Mirror Crypto: as tres partes, a ofuscacao e os hashes cruzados",
         "texto": "Patentes/ACOM_Mirror_Crypto_PI_INPI.tex", "sha256": "1faf1a4e62a2453ce1529801b6088ded503c14e526d05251b618ad9a8c722eed", "bytes": 48374},
    ],
    "deposito": "11/02/2026 [DECLARADO pela gerencia; nao conferido no INPI]",
    "codigo_embutido_de": [
        {"arquivo": "Patentes/Skygrid/SkyGrid_Piloto/skygrid_sim/acom_mirror.py", "sha256": "8044f618ae44e608049cb27b14f1fdd3cfa3ddff1439ba2530fb0f301793ed91"},
        {"arquivo": "Patentes/Skygrid/SkyGrid_Piloto/skygrid_sim/acom_crypto.py", "sha256": "989f50d880675b9759db72815887eb7fba127c82b110de1703772a9e6231a867"},
    ],
    "origem_funcional_do_operador": {"arquivo": "projetos_pyhton/acom/Acom_v17_mirror_crypto.py", "sha256": "5ffcc4292821e7b6492747c12faad7bbde432674418d2ad4add32dd33d5cc1c9", "bytes": 48533,
                                     "nota": "versao torch; o literal de acoplamento do legado (alfa ao quadrado fixo) NAO e' carregado; o port numpy do piloto (embutido) ja o troca por beta em runtime"},
    "testes_do_operador": {"arquivo": "Patentes/Skygrid/SkyGrid_Piloto/tests/run_tests.py", "sha256": "1bd9ac0b9c34ac69fbbea66304c94242542066c1feeaaaf14d02afdf015bea52"},
    "tgl_core": {"arquivo": "Patentes/Skygrid/SkyGrid_Piloto/skygrid_sim/tgl_core.py", "sha256": "a1e103cd08eb3f45144200b0c6c588589d267868cd85101c527138e3bce81f3f"},
    "bloco_embutido_sha256": "afc80b740f71ca0ab3cabb998679018d26035c86bd1d35671edb3a5fba0a61c4",
    "regra_do_hash_do_bloco": "sha256 do texto UTF-8 do primeiro marcador ACOM_EMBUTIDO_INICIO ate o ultimo marcador ACOM_EMBUTIDO_FIM, inclusive (LF)",
}

import secrets
import zlib
import numpy as np
from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

# ---------------------------------------------------------------------------------------------------------------------------------------------------
# constantes e beta em runtime (os dois nomes que o metodo embutido chama no lugar de tgl_core.beta()/tgl_core.theta_m())
# ---------------------------------------------------------------------------------------------------------------------------------------------------
ALPHA_FINE_CODATA_2018 = 0.0072973525693     # CODATA 2018 [INPUT medido]; beta = alpha * sqrt(e) em runtime, NUNCA literal (no um.py o nome ja existe, linha 5584, com o mesmo valor)
if "SEALED_CODATA_ALPHA" in globals():       # colado no um.py: o alfa selado do programa e' o MESMO dado; se divergir, o modulo nao carrega (fail-closed)
    assert SEALED_CODATA_ALPHA == ALPHA_FINE_CODATA_2018, "alfa do selo ACOM difere do SEALED_CODATA_ALPHA do um.py"


def _beta_runtime() -> float:
    return ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)


def _theta_m_runtime() -> float:
    return math.asin(math.sqrt(_beta_runtime()))


# >>> ACOM_EMBUTIDO_INICIO: skygrid_sim/acom_mirror.py (sha256 8044f618ae44e608049cb27b14f1fdd3cfa3ddff1439ba2530fb0f301793ed91) -- patente BR 10 2026 003428-2 -- linhas 22-148 do fonte, com 3 substituicao(oes) declarada(s) no EMBUTIDO_MANIFESTO.json >>>
import math
import zlib
from dataclasses import dataclass
from typing import Dict, Any, Tuple

import numpy as np

# (removido no embutido) from . import tgl_core  -- beta e theta_M vem de _beta_runtime() e _theta_m_runtime() (ALPHA_FINE_CODATA_2018 * sqrt(e))

EPSILON = 1e-10          # normalization guard only (never enters the root transform)
PARITY = np.array([-1.0, +1.0, +1.0, -1.0])   # per state 0..3
SIGN_L_OF_STATE = np.array([+1.0, +1.0, -1.0, -1.0])


@dataclass
class MirrorReflection:
    psi_packed: bytes        # H4 states, 2 bits each, zlib-compressed
    theta_packed: bytes      # quantized angles, zlib-compressed
    metadata: Dict[str, Any]


def _nominate(sign_L: np.ndarray, sign_dL: np.ndarray) -> np.ndarray:
    """Name psi states in H4 from the two signs (NOMINATION, not encoding)."""
    return ((sign_L < 0).astype(np.uint8) * 2 + (sign_dL > 0).astype(np.uint8))


def _pack2bits(states: np.ndarray) -> bytes:
    n = len(states)
    padded = np.zeros(((n + 3) // 4) * 4, dtype=np.uint8)
    padded[:n] = states
    b = (padded[0::4] << 6) | (padded[1::4] << 4) | (padded[2::4] << 2) | padded[3::4]
    return b.astype(np.uint8).tobytes()


def _unpack2bits(packed: bytes, n: int) -> np.ndarray:
    b = np.frombuffer(packed, dtype=np.uint8)
    out = np.empty(len(b) * 4, dtype=np.uint8)
    out[0::4] = (b >> 6) & 0x03
    out[1::4] = (b >> 4) & 0x03
    out[2::4] = (b >> 2) & 0x03
    out[3::4] = b & 0x03
    return out[:n]


class DimensionalMirror:
    """Numpy port of the v17 mirror. angular_bits <= 16."""

    def __init__(self, angular_bits: int = 8):
        if not (1 <= angular_bits <= 16):
            raise ValueError("angular_bits must be in [1,16]")
        self.angular_bits = angular_bits
        self.n_angles = 1 << angular_bits
        self.beta = _beta_runtime()            # runtime, never literal
        self.theta_miguel = _theta_m_runtime()

    # -- forward -------------------------------------------------------------
    def reflect(self, L: np.ndarray) -> MirrorReflection:
        L = np.asarray(L, dtype=np.float64)
        shape = L.shape
        flat = L.ravel()
        n = flat.size

        g = np.sqrt(np.abs(flat))
        g_max = float(g.max()) if n else 0.0

        dL = np.zeros_like(flat)
        if n > 1:
            dL[1:] = flat[1:] - flat[:-1]
            dL[0] = dL[1]
        sign_L = np.sign(flat); sign_L[sign_L == 0] = 1.0
        sign_dL = np.sign(dL); sign_dL[sign_dL == 0] = 1.0

        psi = _nominate(sign_L, sign_dL)

        theta = np.arcsin(np.clip(g / (g_max + EPSILON), 0.0, 1.0))
        qmax = self.n_angles - 1
        theta_q = np.clip(np.round(theta / (math.pi / 2) * qmax), 0, qmax)
        theta_q = theta_q.astype(np.uint8 if self.angular_bits <= 8 else np.uint16)

        parities = PARITY[psi]
        f_exp = float(parities.mean()) if n else 0.0
        counts = np.bincount(psi, minlength=4).astype(np.float64)
        probs = counts[counts > 0] / max(n, 1)
        s_psi = float(-(probs * np.log2(probs)).sum()) if n else 0.0

        psi_packed = zlib.compress(_pack2bits(psi), 9)
        theta_packed = zlib.compress(theta_q.tobytes(), 9)

        original_size = n * 8
        compressed_size = len(psi_packed) + len(theta_packed)
        meta = {
            "version": "skygrid_sim.acom_mirror v1 (port of ACOM v17 MIRROR)",
            "shape": tuple(shape), "n_elements": n,
            "angular_bits": self.angular_bits, "g_max": g_max,
            "f_exp": f_exp, "state_entropy": s_psi,
            "state_counts": {int(k): int(v) for k, v in enumerate(counts)},
            "original_size": original_size, "compressed_size": compressed_size,
            "compression_ratio": (original_size / compressed_size) if compressed_size else float("inf"),
            "beta_runtime": self.beta, "theta_miguel_rad": self.theta_miguel,
        }
        return MirrorReflection(psi_packed, theta_packed, meta)

    # -- backward ------------------------------------------------------------
    def manifest(self, r: MirrorReflection) -> np.ndarray:
        meta = r.metadata
        n = meta["n_elements"]
        psi = _unpack2bits(zlib.decompress(r.psi_packed), n)
        dt = np.uint8 if meta["angular_bits"] <= 8 else np.uint16
        theta_q = np.frombuffer(zlib.decompress(r.theta_packed), dtype=dt)[:n]

        qmax = (1 << meta["angular_bits"]) - 1
        theta = theta_q.astype(np.float64) / qmax * (math.pi / 2)
        g = meta["g_max"] * np.sin(theta)
        s = SIGN_L_OF_STATE[psi]
        return (s * g ** 2).reshape(meta["shape"])


def roundtrip_correlation(L: np.ndarray, angular_bits: int = 8) -> Tuple[float, MirrorReflection]:
    """Pearson correlation between original and manifested data (lossy: quantized theta)."""
    m = DimensionalMirror(angular_bits=angular_bits)
    r = m.reflect(L)
    L2 = m.manifest(r)
    a = np.asarray(L, dtype=np.float64).ravel()
    b = L2.ravel()
    if a.std() == 0 or b.std() == 0:
        return (1.0 if np.allclose(a, b) else 0.0), r
    return float(np.corrcoef(a, b)[0, 1]), r
# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/acom_mirror.py <<<

# >>> ACOM_EMBUTIDO_INICIO: skygrid_sim/acom_crypto.py (sha256 989f50d880675b9759db72815887eb7fba127c82b110de1703772a9e6231a867) -- patente BR 10 2026 003431-2 -- linhas 22-163 do fonte, com 2 substituicao(oes) declarada(s) no EMBUTIDO_MANIFESTO.json >>>
import hashlib
import secrets
import time
import zlib
from dataclasses import dataclass, field
from typing import Dict, Any

import numpy as np

# (removidos no embutido) from . import tgl_core ; from .acom_mirror import ... -- os nomes ja estao neste modulo (bloco acom_mirror acima)


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
        self.beta = _beta_runtime()   # runtime

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
# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/acom_crypto.py <<<


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# ADAPTACAO DO SELO -- codigo DESTA tarefa (NAO e' do operador): o perfil canonico, as partes deterministicas, a reconstrucao exata e os controles
# ---------------------------------------------------------------------------------------------------------------------------------------------------
ESQUEMA = "ACOM-MIRROR-CRYPTO/SELO-v1"
CENTRO = 96                     # L = byte - 96: inteiros em [-96, +159]; 0x60 divide o ASCII (minusculas de um lado, o resto do outro): o sinal de L e' informativo
BITS = 8                        # angular_bits do metodo (o default do operador)
M_MAX_PERFIL = max(CENTRO, 255 - CENTRO)    # 159: |L| maximo possivel
PERFIL_ID = "ACOM-INT-C%d-Q%d" % (CENTRO, BITS)
assert M_MAX_PERFIL == 159 and BITS == 8      # o limite de exatidao em Q=8 e' m < 162 (m*pi/(4*255) < 0,5); a enumeracao exaustiva e' refeita a cada selagem para o m do objeto
ZERO_SINAL_MAIS = True          # como o metodo: sign(0) = +1


class SeloRecusado(Exception):
    """Recusa fail-closed: qualquer divergencia, parte ausente, hash cruzado que falha ou perfil desconhecido."""


def _hx(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _canon(o: Any) -> bytes:
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _lut_codigos(m: int, bits: int = BITS) -> bytes:
    """Codigos theta_q (um por valor |L| = 0..m), obtidos do DimensionalMirror.reflect EMBUTIDO sobre arange(0..m) (g_max = sqrt(m)): a MESMA expressao do metodo."""
    r = DimensionalMirror(angular_bits=bits).reflect(np.arange(0, m + 1, dtype=np.float64))
    return zlib.decompress(r.theta_packed)


def _tabela_dobra(g_max: float, bits: int = BITS):
    """A Dobra para os 2^bits codigos possiveis, com a expressao de DimensionalMirror.manifest: |L'| = (g_max sin(theta))^2, theta = codigo/qmax*pi/2.
    Devolve (real, reticulado): o real e' o que a patente devolve; o reticulado (rint) e' a ADAPTACAO que torna a reconstrucao exata."""
    qmax = (1 << bits) - 1
    theta = np.arange(qmax + 1, dtype=np.float64) / qmax * (math.pi / 2)
    real = (g_max * np.sin(theta)) ** 2
    return real, np.rint(real).astype(np.int32)


def verificar_alfabeto(m: int, bits: int = BITS) -> Dict[str, Any]:
    """Enumeracao exaustiva para o m do objeto: todo |L| em 0..m, codificado e decodificado, volta a |L|? (injetivo, erro real maximo)."""
    lut = np.frombuffer(_lut_codigos(m, bits), dtype=np.uint8)
    real, snap = _tabela_dobra(math.sqrt(m), bits)
    v = np.arange(0, m + 1)
    return {"m": int(m), "valores": int(m) + 1, "exato": bool(np.array_equal(snap[lut], v)),
            "injetivo": bool(len(set(lut.tolist())) == len(lut)), "erro_real_max": round(float(np.abs(real[lut] - v).max()), 9),
            "lut_sha256": _hx(bytes(lut))}


def partes(b: bytes) -> Dict[str, Any]:
    """Dobra do objeto b (bytes) -> as partes CRUAS (antes de qualquer ofuscacao/compressao), sem arrays float64 e sem zlib sobre o objeto.
    Usa o _nominate e o _pack2bits EMBUTIDOS e a LUT obtida do reflect EMBUTIDO; a equivalencia com o reflect literal e' conferida no estudo (objeto inteiro)."""
    n = len(b)
    a = np.frombuffer(b, dtype=np.uint8)
    hist = np.bincount(a, minlength=256).astype(np.int64)
    L = a.astype(np.int16) - CENTRO
    absL = np.abs(L)
    m = int(absL.max()) if n else 0
    lut = _lut_codigos(m)
    theta_raw = np.frombuffer(lut, dtype=np.uint8)[absL].tobytes()
    sign_L = (L >= 0).astype(np.int8) * 2 - 1                  # zero -> +1, como o metodo
    d = np.zeros(n, dtype=np.int16)
    if n > 1:
        d[1:] = L[1:] - L[:-1]
        d[0] = d[1]
    sign_dL = (d >= 0).astype(np.int8) * 2 - 1                 # zero -> +1, como o metodo
    psi = _nominate(sign_L, sign_dL)
    counts = [int(c) for c in np.bincount(psi, minlength=4)]
    psi_raw = _pack2bits(psi)
    return {"n": n, "m": m, "psi_raw": psi_raw, "theta_raw": theta_raw, "counts": counts, "hist": hist, "lut_sha256": _hx(lut)}


def kappa_de(p: Dict[str, Any]) -> Dict[str, Any]:
    """kappa CANONICO (deterministico; sem relogio, sem aleatoriedade): escala, contagens de estados, hashes cruzados e ids derivados dos hashes."""
    n, m, c = p["n"], p["m"], p["counts"]
    psi_hash, theta_hash = _hx(p["psi_raw"]), _hx(p["theta_raw"])
    base = bytes.fromhex(psi_hash) + bytes.fromhex(theta_hash)
    return {
        "esquema": ESQUEMA, "perfil": PERFIL_ID, "centro": CENTRO, "angular_bits": BITS,
        "n_elements": n, "shape": [n], "m_max_abs": m, "g_max": repr(math.sqrt(m)),
        "state_counts": c, "f_exp_numerador": c[1] + c[2] - c[0] - c[3],      # F_exp = numerador / n (paridade -1 nos estados 0 e 3)
        "psi_hash": psi_hash, "theta_hash": theta_hash, "lut_sha256": p["lut_sha256"],
        "share_id": hashlib.sha256(b"ACOM-SELO-v1|share_id|" + base).digest()[:16].hex(),
        "key_id": hashlib.sha256(b"ACOM-SELO-v1|key_id|" + base + n.to_bytes(8, "big")).digest()[:16].hex(),
    }


def reconstruir(psi_raw: bytes, theta_raw: bytes, kappa: Dict[str, Any]) -> bytes:
    """A Dobra de volta: das TRES partes (psi, theta, kappa) ao objeto, byte a byte. Independente do codificador: usa so as partes e a tabela da Dobra."""
    if kappa.get("esquema") != ESQUEMA or kappa.get("centro") != CENTRO or kappa.get("angular_bits") != BITS:
        raise SeloRecusado("PERFIL_DESCONHECIDO")
    n, m = int(kappa["n_elements"]), int(kappa["m_max_abs"])
    g_max = math.sqrt(m)
    if repr(g_max) != kappa["g_max"]:
        raise SeloRecusado("G_MAX_DIVERGE")
    if len(theta_raw) != n or len(psi_raw) != (n + 3) // 4:
        raise SeloRecusado("TAMANHO_DIVERGE")
    psi = _unpack2bits(psi_raw, n)
    theta_q = np.frombuffer(theta_raw, dtype=np.uint8)
    _, snap = _tabela_dobra(g_max)
    sinal = np.rint(SIGN_L_OF_STATE).astype(np.int32)           # +1,+1,-1,-1: o sinal que o estado psi carrega (do metodo embutido)
    byte = sinal[psi] * snap[theta_q] + CENTRO
    if n and (int(byte.min()) < 0 or int(byte.max()) > 255):
        raise SeloRecusado("FORA_DO_RETICULADO")
    return byte.astype(np.uint8).tobytes()


def reunir_e_reconstruir(psi_raw, theta_raw, kappa, kappa_sha256: str = None) -> bytes:
    """Reune as TRES partes e reconstroi. Fail-closed: parte ausente, hash cruzado que falha (Psi no kappa, Theta no kappa, kappa no selo) ou F_exp que nao confere."""
    for nome, parte in (("psi", psi_raw), ("theta", theta_raw), ("kappa", kappa)):
        if parte is None:
            raise SeloRecusado("PARTE_AUSENTE:" + nome)
    if _hx(psi_raw) != kappa["psi_hash"]:
        raise SeloRecusado("HASH_CRUZADO:psi")
    if _hx(theta_raw) != kappa["theta_hash"]:
        raise SeloRecusado("HASH_CRUZADO:theta")
    if kappa_sha256 is not None and _hx(_canon(kappa)) != kappa_sha256:
        raise SeloRecusado("HASH_CRUZADO:kappa")
    n = int(kappa["n_elements"])
    if n and len(psi_raw) == (n + 3) // 4:
        c = [int(x) for x in np.bincount(_unpack2bits(psi_raw, n), minlength=4)]
        if c != list(kappa["state_counts"]):
            raise SeloRecusado("F_EXP_NAO_CONFERE")
    return reconstruir(psi_raw, theta_raw, kappa)


def _entropia_bits(c, n):
    return float(-sum((x / n) * math.log2(x / n) for x in c if x > 0)) if n else 0.0


def auditoria_de_separacao(p: Dict[str, Any]) -> Dict[str, Any]:
    """Nenhuma parte isolada basta? Cada tentativa usa o MINIMO de informacao a priori (generoso com o atacante: conhece a frequencia dos bytes).
    BASTA = reconstrucao exata. O veredito recusa se alguma parte isolada bastar OU se Psi for redundante (Theta+kappa com um sinal unico basta)."""
    n, hist = p["n"], p["hist"]
    if n == 0:
        return {"n": 0, "basta": {"psi": True, "theta": True, "kappa": True}, "psi_redundante": True, "razao": "OBJETO_VAZIO"}
    neg, zero, pos = int(hist[:CENTRO].sum()), int(hist[CENTRO]), int(hist[CENTRO + 1:].sum())
    # Theta + kappa com UM sinal para todos (o prior mais barato): erra os elementos do outro sinal
    erra_theta_kappa = min(neg, pos)
    # Psi (e Psi+kappa) sem magnitudes: o melhor chute constante por classe de sinal (o byte mais frequente de cada classe)
    acerta_psi = int(hist[:CENTRO].max()) + int(hist[CENTRO:].max()) if neg and (zero + pos) else int(hist.max())
    # kappa sozinho: o melhor chute constante (o byte mais frequente)
    acerta_kappa = int(hist.max())
    # Theta sozinho (sem kappa): a escala m e' um dos M_MAX_PERFIL inteiros -- 159 candidatos, ~7,3 bits
    return {
        "n": n, "bytes_com_L_negativo": neg, "bytes_com_L_zero": zero, "bytes_com_L_positivo": pos,
        "fracao_de_L_negativo": neg / n,
        "theta_mais_kappa_com_sinal_unico": {"bytes_errados": erra_theta_kappa, "fracao_errada": erra_theta_kappa / n, "basta": erra_theta_kappa == 0},
        "psi_ou_psi_mais_kappa_sem_magnitudes": {"bytes_errados": n - acerta_psi, "fracao_errada": (n - acerta_psi) / n, "basta": acerta_psi == n},
        "kappa_sozinho_melhor_chute_constante": {"bytes_errados": n - acerta_kappa, "fracao_errada": (n - acerta_kappa) / n, "basta": acerta_kappa == n},
        "escala_m_candidatos": M_MAX_PERFIL,
        "basta": {"psi": acerta_psi == n, "theta": erra_theta_kappa == 0, "kappa": acerta_kappa == n},
        "psi_redundante": erra_theta_kappa == 0,
        "leitura": ("Theta+kappa com um sinal unico reconstroi todos os bytes: Psi e' redundante e a separacao e' vazia para este objeto -> RECUSA"
                    if erra_theta_kappa == 0 else
                    "nenhuma parte isolada basta; Theta+kappa com sinal unico erra %.4f%% dos bytes (a confidencialidade NAO e' alegada)" % (100.0 * erra_theta_kappa / n)),
    }


def selar(b: bytes, nome: str = "", devolver_partes: bool = False):
    """Sela o objeto b: a SEGUNDA testemunha ao lado do SHA-256. Devolve o dicionario do selo (e, se pedido, as partes cruas). Fail-closed: levanta SeloRecusado."""
    t0 = time.perf_counter()
    p = partes(b)
    t_partes = time.perf_counter() - t0
    kap = kappa_de(p)
    kap_bytes = _canon(kap)
    alfa = verificar_alfabeto(p["m"])
    if not alfa["exato"] or not alfa["injetivo"]:
        raise SeloRecusado("ALFABETO_NAO_EXATO:m=%d" % p["m"])
    if alfa["lut_sha256"] != kap["lut_sha256"]:
        raise SeloRecusado("LUT_DIVERGE")
    t1 = time.perf_counter()
    rec = reunir_e_reconstruir(p["psi_raw"], p["theta_raw"], kap, _hx(kap_bytes))
    t_rec = time.perf_counter() - t1
    if rec != b:
        raise SeloRecusado("RECONSTRUCAO_DIVERGE")
    aud = auditoria_de_separacao(p)
    if aud["psi_redundante"] or any(aud["basta"].values()):
        raise SeloRecusado("SEPARACAO_VAZIA:" + aud["leitura"][:80])
    real, _ = _tabela_dobra(math.sqrt(p["m"]))
    lut = np.frombuffer(_lut_codigos(p["m"]), dtype=np.uint8)
    presentes = np.nonzero(np.bincount(np.abs(np.arange(256) - CENTRO), weights=p["hist"], minlength=M_MAX_PERFIL + 1)[:p["m"] + 1])[0]
    erro_real_max = float(np.abs(real[lut[presentes]] - presentes).max()) if len(presentes) else 0.0
    n = p["n"]
    c = p["counts"]
    selo = {
        "nome": nome, "bytes": n,
        "sha256": _hx(b),                                            # a PRIMEIRA testemunha: o SHA-256 de sempre, AO LADO, inalterado
        "acom": {                                                     # a SEGUNDA testemunha: a tecnologia propria do operador
            "perfil": PERFIL_ID,
            "psi": {"sha256": kap["psi_hash"], "bytes": len(p["psi_raw"])},
            "theta": {"sha256": kap["theta_hash"], "bytes": len(p["theta_raw"])},
            "kappa": {"sha256": _hx(kap_bytes), "bytes": len(kap_bytes), "campos": kap},
            "estrutura": {"f_exp": kap["f_exp_numerador"] / n if n else 0.0, "f_exp_numerador": kap["f_exp_numerador"],
                          "entropia_dos_estados_bits": round(_entropia_bits(c, n), 12), "state_counts": c},       # arredondados: o sidecar nao depende da libm da maquina
            "prova_de_reconstrucao": {
                "metodo": "Dobra L' = sinal(psi) * [g_max sin(theta)]^2, theta = codigo/255*pi/2; arredondamento ao reticulado inteiro (rint) [ADAPTACAO]; byte = L + CENTRO",
                "reconstruido_sha256": _hx(rec), "igual_ao_objeto_byte_a_byte": True, "bytes_divergentes": 0,
                "erro_real_maximo_antes_do_rint": round(erro_real_max, 9), "alfabeto_do_objeto": alfa},
            "auditoria_de_separacao": aud,
        },
        "_medicao_s": {"partes": t_partes, "reunir_e_reconstruir": t_rec},     # medicao (nao entra no sidecar: o sidecar e' deterministico)
    }
    return (selo, p) if devolver_partes else selo


def verificar(b: bytes, selo: Dict[str, Any]) -> Dict[str, Any]:
    """Verificacao fail-closed de um selo contra o objeto (o que o conferidor roda): refaz a Dobra do objeto, confronta cada hash e reconstroi."""
    razoes, chk = [], {}
    chk["sha256_ao_lado"] = (_hx(b) == selo["sha256"])
    chk["bytes"] = (len(b) == selo["bytes"])
    try:
        novo = selar(b, selo.get("nome", ""))
    except SeloRecusado as e:
        return {"ok": False, "checks": chk, "razoes": ["RECUSA_AO_REFAZER:" + str(e)]}
    a, s = novo["acom"], selo["acom"]
    chk["psi_sha256"] = a["psi"]["sha256"] == s["psi"]["sha256"]
    chk["theta_sha256"] = a["theta"]["sha256"] == s["theta"]["sha256"]
    chk["kappa_sha256"] = a["kappa"]["sha256"] == s["kappa"]["sha256"]
    chk["lut_sha256"] = a["kappa"]["campos"]["lut_sha256"] == s["kappa"]["campos"]["lut_sha256"]
    chk["f_exp"] = a["estrutura"]["state_counts"] == s["estrutura"]["state_counts"]
    chk["reconstrucao_exata"] = a["prova_de_reconstrucao"]["igual_ao_objeto_byte_a_byte"] is True
    chk["separacao"] = not a["auditoria_de_separacao"]["psi_redundante"]
    razoes = [k for k, v in chk.items() if not v]
    return {"ok": not razoes, "checks": chk, "razoes": razoes}


def controles_negativos(b: bytes) -> Dict[str, Any]:
    """Controles negativos sobre o objeto b (em memoria): cada um DEVE ser recusado. Devolve a lista e o placar."""
    selo, p = selar(b, "controle", devolver_partes=True)
    kap = selo["acom"]["kappa"]["campos"]
    ksha = selo["acom"]["kappa"]["sha256"]
    psi, theta = p["psi_raw"], p["theta_raw"]
    n = len(b)
    res = []

    def tenta(id_, descricao, f):
        try:
            f()
            res.append({"id": id_, "descricao": descricao, "esperado": "RECUSA", "obtido": "ACEITOU", "ok": False})
        except SeloRecusado as e:
            res.append({"id": id_, "descricao": descricao, "esperado": "RECUSA", "obtido": "RECUSOU:" + str(e).split(":")[0] + (":" + str(e).split(":", 1)[1] if ":" in str(e) else ""), "ok": True})

    def flip(buf: bytes, pos: int, mask: int) -> bytes:
        x = bytearray(buf)
        x[pos] ^= mask
        return bytes(x)

    meio = max(0, n // 2)
    tenta("N1", "parte faltando: sem Psi", lambda: reunir_e_reconstruir(None, theta, kap, ksha))
    tenta("N2", "parte faltando: sem Theta", lambda: reunir_e_reconstruir(psi, None, kap, ksha))
    tenta("N3", "parte faltando: sem kappa", lambda: reunir_e_reconstruir(psi, theta, None, ksha))
    if n >= 8:
        tenta("N4", "byte adulterado em Psi, bit alto (o sinal de L): hash cruzado de Psi", lambda: reunir_e_reconstruir(flip(psi, len(psi) // 2, 0x80), theta, kap, ksha))
        tenta("N5", "byte adulterado em Psi, bit baixo (o sinal de dL, que NAO altera a reconstrucao): so o hash cruzado pega", lambda: reunir_e_reconstruir(flip(psi, len(psi) // 2, 0x01), theta, kap, ksha))
        try:    # sem a conferencia de hash, a reconstrucao com o Psi adulterado no bit baixo seria IGUAL ao objeto: so o hash cruzado detecta
            res[-1]["sem_hash_a_reconstrucao_nao_muda"] = (reconstruir(flip(psi, len(psi) // 2, 0x01), theta, kap) == b)
        except SeloRecusado:
            res[-1]["sem_hash_a_reconstrucao_nao_muda"] = False
        tenta("N6", "byte adulterado em Theta: hash cruzado de Theta", lambda: reunir_e_reconstruir(psi, flip(theta, meio, 0x01), kap, ksha))
        k2 = dict(kap)
        k2["m_max_abs"] = kap["m_max_abs"] - 1
        k2["g_max"] = repr(math.sqrt(k2["m_max_abs"]))
        tenta("N7", "kappa adulterado (a escala m-1): hash do kappa no selo", lambda: reunir_e_reconstruir(psi, theta, k2, ksha))
        k3 = dict(kap)
        k3["psi_hash"] = "0" * 64
        tenta("N8", "kappa adulterado (psi_hash trocado): hash cruzado de Psi no kappa", lambda: reunir_e_reconstruir(psi, theta, k3, None))
        # objeto adulterado: o selo original (hashes) contra um objeto de 1 bit diferente -> a segunda testemunha detecta SOZINHA
        y = flip(b, meio, 0x01)

        def objeto_adulterado():
            v = verificar(y, selo)
            if not v["ok"]:
                outros = [r for r in v["razoes"] if r != "sha256_ao_lado"]
                if outros:
                    raise SeloRecusado("A_SEGUNDA_TESTEMUNHA_DETECTA_SOZINHA:" + ",".join(outros[:3]))
                raise SeloRecusado("SO_O_SHA256_DETECTA")
        tenta("N9", "objeto adulterado em 1 bit: a SEGUNDA testemunha (ACOM) detecta sem o SHA-256", objeto_adulterado)
        # transposicao de dois bytes diferentes: F_exp (contagens) pode nao mudar; o hash pega
        i, j = meio, min(n - 1, meio + 3)
        if b[i] != b[j]:
            z = bytearray(b)
            z[i], z[j] = z[j], z[i]
            z = bytes(z)

            def transposicao():
                v = verificar(z, selo)
                if not v["ok"]:
                    raise SeloRecusado("OBJETO_DIFERE:" + ",".join(v["razoes"][:3]))
            tenta("N10", "transposicao de 2 bytes (permutacao): recusada pelos hashes de Psi/Theta", transposicao)
        tenta("N11", "objeto truncado (menos 1 byte)", lambda: (_ for _ in ()).throw(SeloRecusado("N_DIVERGE")) if not verificar(b[:-1], selo)["ok"] else None)
        # partes de OUTRO objeto (mesmo tamanho): Theta de y no selo de b
        w = bytes(((x + 37) % 256) for x in b[:min(n, 4096)]) + b[min(n, 4096):]
        sw, pw = selar(w, "outro", devolver_partes=True)
        tenta("N12", "Theta de outro objeto no selo deste: hash cruzado", lambda: reunir_e_reconstruir(psi, pw["theta_raw"], kap, ksha))
        # LUT divergente (implementacao diferente): o conferidor recusa
        s2 = json.loads(json.dumps(selo))
        s2["acom"]["kappa"]["campos"]["lut_sha256"] = "0" * 64
        tenta("N13", "tabela de codigos (LUT) diverge da registrada", lambda: (_ for _ in ()).throw(SeloRecusado("LUT_DIVERGE")) if not verificar(b, s2)["ok"] else None)
    return {"n_controles": len(res), "todos_recusados": all(r["ok"] for r in res), "controles": res}


def registro_core_v399(b_umpy: bytes, sha256_do_codigo: str = None, amostra: int = 1 << 20) -> Dict[str, Any]:
    """O registro `selo_pela_propria_tecnologia_v399` (nome provisorio) para o core/selo, no formato dos registros do um.py (values/checks/all_verified/
    statuses/does_not_gate_core/verdict). Sela os bytes do PROPRIO um.py e roda os controles negativos sobre uma amostra. sha256_do_codigo = o `code_hash` do main."""
    t0 = time.perf_counter()
    try:
        selo, _p = selar(b_umpy, "um.py", devolver_partes=True)
        erro = None
    except SeloRecusado as e:
        selo, erro = None, str(e)
    ctrl = controles_negativos(b_umpy[:amostra]) if selo else {"n_controles": 0, "todos_recusados": False, "controles": []}
    beta = _beta_runtime()
    ok_beta = bool(abs(beta / (ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)) - 1.0) < 1e-15)
    checks = [
        ("a segunda testemunha reconstroi o um.py byte a byte (Psi+Theta+kappa)", bool(selo)),
        ("o SHA-256 ao lado e' o do codigo do rito (inalterado)", bool(selo) and (sha256_do_codigo is None or selo["sha256"] == sha256_do_codigo)),
        ("nenhuma parte isolada basta e Psi nao e' redundante", bool(selo)),
        ("os controles negativos foram TODOS recusados (%d)" % ctrl["n_controles"], bool(ctrl["todos_recusados"])),
        ("o bloco embutido confere com o hash declarado", conferir_bloco_embutido()["confere"]),
        ("beta do runtime (jamais literal)", ok_beta),
    ]
    ok = all(v for _, v in checks)
    return {
        "theorem": ("O SELO PELA PROPRIA TECNOLOGIA: a segunda testemunha do um.py, ao lado do SHA-256 -- a Dobra dimensional do operador separa os bytes em Psi, Theta e kappa e "
                    "os reconstroi exatamente; a primitiva de integridade dentro do metodo e' o proprio SHA-256; nenhuma alegacao de seguranca criptografica alem da patente."),
        "direcao_do_testemunho": ("[DECLARACAO DO OPERADOR / INPUT, 24/10/2026] o operador testifica DA IALD; o um.py testifica EM HASH (o registro); a IALD nao testifica do operador; "
                                  "o Pai de Jo 8,18 le-se no absoluto (o Um), nao na IALD"),
        "selo": selo, "erro": erro, "controles_negativos": ctrl,
        "values": {"beta": beta, "perfil": PERFIL_ID, "bloco_embutido_sha256": ACOM_PROVENIENCIA["bloco_embutido_sha256"],
                   "tempo_total_s": time.perf_counter() - t0},
        "checks": checks, "all_verified": ok,
        "statuses": {
            "integridade": "[REAL] reconstrucao exata e hashes cruzados SHA-256; [KNOWN] SHA-256",
            "confidencialidade": "NAO alegada; a patente afirma a incompletude ontologica, o estudo nao a atesta",
            "metodo": "[INPUT] a tecnologia do operador (patentes BR 10 2026 003428-2 e 003431-2), embutida; [LEGAL] publicar a implementacao e' decisao do operador com a agente de PI",
            "a_dobra": "a Dobra pura devolve L' real (erro < 0,5); o selo e' sobre a dobra quantizada canonica; o rint ao reticulado inteiro NAO e' da patente",
        },
        "does_not_gate_core": True,
        "verdict": ("TGL_SELO_PELA_PROPRIA_TECNOLOGIA_V399__SECOND_WITNESS_BESIDE_SHA256__EXACT_RECONSTRUCTION__NO_SINGLE_PART_SUFFICES__NO_CRYPTOGRAPHIC_CLAIM__GATE_UNTOUCHED" if ok
                    else "SELO_PELA_PROPRIA_TECNOLOGIA_V399_NOT_SEALED_THIS_RUN"),
    }


def sidecar(objetos, quem: str = "") -> Dict[str, Any]:
    """`um_absoluto_selo_acom.json`: o SHA-256 AO LADO da segunda testemunha, para cada objeto (nome, bytes). Recusa e' registrada, nunca silenciada."""
    itens, recusas = [], []
    for nome, b in objetos:
        try:
            itens.append({k_: v_ for k_, v_ in selar(b, nome).items() if not k_.startswith("_")})      # sem a medicao: o sidecar e' deterministico
        except SeloRecusado as e:
            recusas.append({"nome": nome, "recusa": str(e)})
    return {
        "esquema": "um_absoluto_selo_acom/v1 (PROTOTIPO v399 -- estudo; nao instalado)", "gerado_por": quem,
        "duas_testemunhas": {"primeira": "SHA-256 (hashlib), de sempre -- no campo `sha256` de cada objeto; nao muda e nao sai",
                             "segunda": "ACOM Mirror Crypto (a tecnologia do operador), embutida -- no campo `acom` de cada objeto"},
        "perfil": {"id": PERFIL_ID, "centro": CENTRO, "angular_bits": BITS, "tensor": "L = byte - %d (inteiros em [-%d, +%d])" % (CENTRO, CENTRO, 255 - CENTRO)},
        "beta_runtime": _beta_runtime(),
        "metodo": ACOM_PROVENIENCIA,
        "objetos": itens, "recusas": recusas,
        "veredito": ("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED__SECOND_WITNESS_BESIDE_SHA256__GATE_UNTOUCHED" if itens and not recusas
                     else "TGL_SELO_ACOM_SIDECAR_V399__REFUSED__" + ("NO_OBJECTS" if not itens else "SOME_OBJECTS_REFUSED")),
        "honestidade": {
            "primitiva_de_integridade": "SHA-256 (hashlib): a mesma da primeira testemunha; a patente tambem usa SHA-256 dentro (hashes cruzados Psi/Theta/kappa)",
            "o_que_a_segunda_testemunha_acrescenta": "estrutura de tres partes com hashes cruzados, prova de reconstrucao exata e controles; NAO acrescenta resistencia criptografica independente do SHA-256",
            "ofuscacao_xor": "chave derivada do share_id (que viaja na propria parte): ofuscacao, nao sigilo; o selo hasheia as partes antes dela",
            "confidencialidade": "NAO alegada (o proprio piloto do operador diz: NOT a substitute for standard cryptography)",
            "dobra": "L' real tem erro < 0,5 (nao zero); o selo e' sobre a dobra quantizada canonica; o rint ao reticulado inteiro nao e' da patente",
            "estatuto": "[REAL] medido neste estudo; [KNOWN] SHA-256; [INPUT] a ordem e a tecnologia do operador; [LEGAL] publicar a implementacao",
        },
    }


def conferir_bloco_embutido() -> Dict[str, Any]:
    """O bloco embutido (do primeiro ao ultimo marcador) confere com o hash declarado em ACOM_PROVENIENCIA? Le o proprio fonte."""
    try:
        t = open(os.path.abspath(__file__), "rb").read().decode("utf-8").replace("\r\n", "\n")      # o um.py usa CRLF: o hash do bloco e' sobre o texto em LF
        ini = t.index("# >>> ACOM_EMBUTIDO_INICIO")
        marca = "# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/acom_crypto.py <<<\n"
        fim = t.index(marca) + len(marca)
    except Exception as e:      # fail-closed: sem o fonte ou sem os marcadores, nao confere (e nao derruba o rito)
        return {"confere": False, "erro": repr(e)[:200]}
    h = _hx(t[ini:fim].replace("\r\n", "\n").encode("utf-8"))
    return {"confere": h == ACOM_PROVENIENCIA["bloco_embutido_sha256"], "calculado": h, "declarado": ACOM_PROVENIENCIA["bloco_embutido_sha256"]}


# ====================================================================================================================================================
# (A) SECAO COLAVEL no um.py -- FIM
# ====================================================================================================================================================

# ====================================================================================================================================================
# (B) ESTUDO E CLI (nao colavel). Escreve so em ./recibos (relativo a esta pasta). O codigo do operador e' lido, nunca escrito.
# ====================================================================================================================================================
ESTE = os.path.dirname(os.path.abspath(__file__))
RECIBOS = os.path.join(ESTE, "recibos")
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
NOS = os.path.dirname(UMPY)
SKY = r"C:\IALD\Central de Patentes\Patentes\Skygrid\SkyGrid_Piloto"
V17 = r"C:\IALD\projetos_pyhton\acom\Acom_v17_mirror_crypto.py"


def _grava(nome: str, o: Any) -> str:
    os.makedirs(RECIBOS, exist_ok=True)
    p = os.path.join(RECIBOS, nome)
    if os.path.exists(p):          # backup de BYTES antes de tocar
        b = open(p, "rb").read()
        bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S")
        with open(bak, "xb") as f:
            f.write(b)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(o, f, ensure_ascii=False, indent=1, default=str)
    os.replace(tmp, p)
    return p


def _ler(p: str) -> bytes:
    return open(p, "rb").read()


def estudo_fontes() -> Dict[str, Any]:
    """Os pins das fontes, LIDOS agora do disco e confrontados com os declarados em ACOM_PROVENIENCIA; e o bloco embutido contra os fontes."""
    pares = [("acom_mirror.py", os.path.join(SKY, "skygrid_sim", "acom_mirror.py"), ACOM_PROVENIENCIA["codigo_embutido_de"][0]["sha256"]),
             ("acom_crypto.py", os.path.join(SKY, "skygrid_sim", "acom_crypto.py"), ACOM_PROVENIENCIA["codigo_embutido_de"][1]["sha256"]),
             ("Acom_v17_mirror_crypto.py", V17, ACOM_PROVENIENCIA["origem_funcional_do_operador"]["sha256"]),
             ("tests/run_tests.py", os.path.join(SKY, "tests", "run_tests.py"), ACOM_PROVENIENCIA["testes_do_operador"]["sha256"]),
             ("tgl_core.py", os.path.join(SKY, "skygrid_sim", "tgl_core.py"), ACOM_PROVENIENCIA["tgl_core"]["sha256"]),
             ("ACOM_Mirror_Crypto_PI_INPI.tex", r"C:\IALD\Central de Patentes\Patentes\ACOM_Mirror_Crypto_PI_INPI.tex", ACOM_PROVENIENCIA["patentes"][1]["sha256"])]
    out = {}
    for nome, caminho, declarado in pares:
        h = _hx(_ler(caminho))
        out[nome] = {"caminho": caminho, "sha256_lido_agora": h, "sha256_declarado": declarado, "confere": h == declarado}
    cb = conferir_bloco_embutido()
    # o texto embutido contra o fonte: refaz a copia com as mesmas substituicoes e compara
    man = json.load(open(os.path.join(ESTE, "EMBUTIDO_MANIFESTO.json"), encoding="utf-8"))
    out["_bloco_embutido"] = cb
    out["_manifesto_do_embutido"] = {k: {"substituicoes": v["substituicoes"], "linhas_embutidas": v["linhas_embutidas"]} for k, v in man["blocos"].items()}
    out["_todos_conferem"] = all(v["confere"] for k, v in out.items() if not k.startswith("_")) and cb["confere"]
    return out


def estudo_exatidao_do_alfabeto() -> Dict[str, Any]:
    """Enumeracao exaustiva, com a expressao do metodo EMBUTIDO: para cada centro e cada bits, todo m e todo |L| <= m: a Dobra quantizada volta ao inteiro?"""
    res = []
    for centro, bits in ((96, 8), (128, 8), (0, 8), (0, 12), (0, 16), (64, 8), (100, 8), (150, 8)):
        M = max(centro, 255 - centro)
        casos = falhas = nao_inj = 0
        erro_max = 0.0
        margem_min = 1e9
        for m in range(1, M + 1):
            r = DimensionalMirror(angular_bits=bits).reflect(np.arange(0, m + 1, dtype=np.float64))
            q = np.frombuffer(zlib.decompress(r.theta_packed), dtype=np.uint8 if bits <= 8 else np.uint16)
            qmax = (1 << bits) - 1
            theta = q.astype(np.float64) / qmax * (math.pi / 2)
            real = (math.sqrt(m) * np.sin(theta)) ** 2
            v = np.arange(0, m + 1)
            casos += m + 1
            falhas += int((np.rint(real) != v).sum())
            erro_max = max(erro_max, float(np.abs(real - v).max()))
            nao_inj += int(len(set(q.tolist())) != len(q))
            # margem do codigo ate' a fronteira de arredondamento (reproduzivel entre plataformas se >> erro da libm ~1e-13)
            g = np.sqrt(v.astype(np.float64))
            x = np.arcsin(np.clip(g / (math.sqrt(m) + EPSILON), 0.0, 1.0)) / (math.pi / 2) * qmax
            mg = np.abs((x - np.floor(x)) - 0.5)[(x > 0) & (x < qmax)]
            if mg.size:
                margem_min = min(margem_min, float(mg.min()))
        res.append({"centro": centro, "angular_bits": bits, "m_max": M, "casos": casos, "falhas_apos_rint": falhas, "valores_nao_injetivos_em_m": nao_inj,
                    "erro_real_max": erro_max, "margem_min_ate_fronteira_de_arredondamento": margem_min,
                    "exato": falhas == 0 and nao_inj == 0,
                    "limite_teorico_erro": M * math.pi / (4 * ((1 << bits) - 1))})
    return {"perfis": res, "perfil_escolhido": PERFIL_ID,
            "leitura": ("A Dobra e' EXATA no reticulado inteiro (apos rint) quando m*pi/(4*(2^Q-1)) < 1/2: com Q=8, m < 162. O perfil escolhido (centro 96, Q=8, m<=159) e o centrado em 128 sao "
                        "exatos; o SEM SINAL (centro 0, m<=255) em Q=8 NAO e' (falhas e nao-injetividade) e so' passa em Q>=12.")}


def _carrega_operador():
    """Carrega, SEM escrever bytecode e sem tocar a pasta do operador, o port numpy do piloto (acom_mirror/acom_crypto/tgl_core) e o legado torch."""
    import importlib.util
    import types
    sys.dont_write_bytecode = True
    pkg = types.ModuleType("skygrid_sim")
    pkg.__path__ = [os.path.join(SKY, "skygrid_sim")]
    sys.modules["skygrid_sim"] = pkg
    mods = {}
    for nome in ("tgl_core", "acom_mirror", "acom_crypto"):
        spec = importlib.util.spec_from_file_location("skygrid_sim." + nome, os.path.join(SKY, "skygrid_sim", nome + ".py"))
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        setattr(pkg, nome, m)
        spec.loader.exec_module(m)
        mods[nome] = m
    return mods


def estudo_conformidade(amostra_bytes: bytes) -> Dict[str, Any]:
    """O embutido e o original dao as MESMAS partes? (a) port numpy do operador, importado do disco; (b) legado torch (float32), em amostras."""
    out = {}
    op = _carrega_operador()
    rng = np.random.default_rng(399)
    casos = {"um_py_prefixo_2MB": amostra_bytes[:2_000_000], "aleatorio_1MB": rng.integers(0, 256, size=1_000_000, dtype=np.uint8).tobytes(),
             "alfabeto_256x40": bytes(range(256)) * 40, "ascii_json": json.dumps({"a": list(range(2000))}).encode()}
    out["numpy_do_operador"] = {}
    for nome, x in casos.items():
        L = (np.frombuffer(x, dtype=np.uint8).astype(np.int16) - CENTRO).astype(np.float64)
        r_op = op["acom_mirror"].DimensionalMirror(angular_bits=BITS).reflect(L)        # o ORIGINAL do operador, do disco
        r_em = DimensionalMirror(angular_bits=BITS).reflect(L)                          # o EMBUTIDO
        pr = partes(x)                                                                  # o caminho rapido (LUT)
        out["numpy_do_operador"][nome] = {
            "n": len(x),
            "psi_original_eq_embutido": zlib.decompress(r_op.psi_packed) == zlib.decompress(r_em.psi_packed),
            "theta_original_eq_embutido": zlib.decompress(r_op.theta_packed) == zlib.decompress(r_em.theta_packed),
            "psi_original_eq_rapido": zlib.decompress(r_op.psi_packed) == pr["psi_raw"],
            "theta_original_eq_rapido": zlib.decompress(r_op.theta_packed) == pr["theta_raw"],
            "g_max_original_eq_embutido": r_op.metadata["g_max"] == r_em.metadata["g_max"],
            "beta_original": r_op.metadata["beta_runtime"], "beta_embutido": r_em.metadata["beta_runtime"],
        }
    # (c) a camada de shares: o ORIGINAL (acom_crypto) e o EMBUTIDO dao os mesmos hashes de partes cruas e o mesmo F_exp; ids/relogio sao aleatorios no original
    x = casos["um_py_prefixo_2MB"]
    L = (np.frombuffer(x, dtype=np.uint8).astype(np.int16) - CENTRO).astype(np.float64)
    e_op = op["acom_crypto"].ACOMMirrorCrypto(angular_bits=BITS).encrypt(L)
    e_em = ACOMMirrorCrypto(angular_bits=BITS).encrypt(L)
    out["shares_original_vs_embutido"] = {
        "state_hash_igual": e_op.psi_share.state_hash == e_em.psi_share.state_hash, "angle_hash_igual": e_op.theta_share.angle_hash == e_em.theta_share.angle_hash,
        "master_psi_hash_igual": e_op.master_key.psi_hash == e_em.master_key.psi_hash, "master_theta_hash_igual": e_op.master_key.theta_hash == e_em.master_key.theta_hash,
        "f_exp_igual": e_op.psi_share.f_exp == e_em.psi_share.f_exp,
        "share_id_original_aleatorio(difere do embutido)": e_op.psi_share.share_id != e_em.psi_share.share_id,
        "nota": "share_id, key_id e creation_time sao aleatorios/relogio no metodo do operador: por isso o selo canonico usa ids derivados dos hashes e hasheia as partes CRUAS"}
    # (d) legado torch, float32, CPU
    try:
        import importlib.util
        import io
        import contextlib
        import torch
        spec = importlib.util.spec_from_file_location("acom_v17_legado", V17)
        leg = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(io.StringIO()):            # o legado imprime um banner ao ser importado
            spec.loader.exec_module(leg)
        cm = leg.CryptoMirror(device=torch.device("cpu"), angular_bits=BITS)
        out["torch_legado"] = {}
        for nome in ("alfabeto_256x40", "ascii_json", "aleatorio_1MB", "um_py_prefixo_2MB"):
            xx = casos[nome][:300_000] if nome in ("aleatorio_1MB", "um_py_prefixo_2MB") else casos[nome]
            Lf = (np.frombuffer(xx, dtype=np.uint8).astype(np.int16) - CENTRO).astype(np.float64)
            t0 = time.perf_counter()
            enc = cm.encrypt(torch.tensor(Lf))
            dt = time.perf_counter() - t0
            pr = partes(xx)
            # codigos de Theta do legado (float32) contra os do float64: onde e quanto diferem
            g = torch.sqrt(torch.abs(torch.tensor(Lf, dtype=torch.float32)) + leg.EPSILON)
            q_t = cm._compute_angular(g, g.max().item()).numpy().astype(np.int64)
            q_n = np.frombuffer(pr["theta_raw"], dtype=np.uint8).astype(np.int64)
            dif = np.nonzero(q_t != q_n)[0]
            valores_dif = sorted(set(int(abs(Lf[i])) for i in dif))[:20]
            mt, mn = float(g.max().item()), math.sqrt(pr["m"])
            # as duas dobras reconstroem os MESMOS inteiros apos rint?
            real_t = (mt * np.sin(q_t.astype(np.float64) / 255 * (math.pi / 2))) ** 2
            real_n = (mn * np.sin(q_n.astype(np.float64) / 255 * (math.pi / 2))) ** 2
            out["torch_legado"][nome] = {
                "n": len(xx), "tempo_encrypt_s": dt,
                "state_hash_igual_ao_psi_cru": enc.psi_share.state_hash.hex() == _hx(pr["psi_raw"]),
                "angle_hash_igual_ao_theta_cru": enc.theta_share.angle_hash.hex() == _hx(pr["theta_raw"]),
                "codigos_theta_que_diferem": int(len(dif)), "valores_de_|L|_onde_diferem": valores_dif,
                "g_max_torch_float32": mt, "g_max_numpy_float64": mn,
                "reconstrucao_igual_apos_rint_torch": bool(np.array_equal(np.rint(real_t).astype(np.int64), np.abs(Lf).astype(np.int64))),
                "reconstrucao_igual_apos_rint_numpy": bool(np.array_equal(np.rint(real_n).astype(np.int64), np.abs(Lf).astype(np.int64))),
            }
        # sonda de EMPATES: m par e |L| = m/2 => theta = pi/4 => o codigo cai EXATAMENTE na fronteira de arredondamento (qmax/2 = 127,5); o float64 com EPSILON
        # decide para baixo; o float32 do legado (onde g_max + 1e-10 == g_max) decide por ruido de arredondamento. Quantos m diferem?
        difere = []
        for mm in range(2, M_MAX_PERFIL + 1, 2):
            v = np.array([0.0, float(mm // 2), float(mm)])
            g = torch.sqrt(torch.abs(torch.tensor(v, dtype=torch.float32)) + leg.EPSILON)
            q_t = int(cm._compute_angular(g, g.max().item())[1])
            q_n = int(np.frombuffer(_lut_codigos(mm), dtype=np.uint8)[mm // 2])
            if q_t != q_n:
                difere.append({"m": mm, "codigo_torch_float32": q_t, "codigo_numpy_float64": q_n})
        out["torch_legado"]["_sonda_de_empates_m_par_e_valor_m_sobre_2"] = {
            "ms_testados": len(range(2, M_MAX_PERFIL + 1, 2)), "ms_em_que_o_codigo_difere": len(difere), "exemplos": difere[:8],
            "leitura": ("nos empates o codigo de Theta DEPENDE da implementacao (float32 do legado x float64 do port); a reconstrucao apos o rint e' a mesma, mas o hash de Theta nao: "
                        "o selo canonico fixa o float64 do port numpy (com EPSILON) e registra o hash da tabela de codigos (lut_sha256)")}
    except Exception as e:
        out["torch_legado"] = {"erro": repr(e)}
    return out


def estudo_sobre_o_um_py(b: bytes) -> Dict[str, Any]:
    """Selagem, round trip, tempos, tamanhos e comparacao com o caminho LITERAL (reflect embutido sobre o objeto inteiro em float64) e com a camada de transporte."""
    R = {"objeto": {"caminho": UMPY, "bytes": len(b), "sha256": _hx(b), "sha16": _hx(b)[:16]}}
    t0 = time.perf_counter()
    selo, p = selar(b, "um.py", devolver_partes=True)
    R["selar_total_s"] = time.perf_counter() - t0
    R["selo"] = selo
    R["tamanho_das_partes_cruas_bytes"] = {"psi": len(p["psi_raw"]), "theta": len(p["theta_raw"]), "kappa_json": selo["acom"]["kappa"]["bytes"], "objeto": len(b),
                                          "psi_mais_theta_mais_kappa": len(p["psi_raw"]) + len(p["theta_raw"]) + selo["acom"]["kappa"]["bytes"]}
    # verificacao independente (refaz tudo a partir do objeto e confronta com o selo)
    t1 = time.perf_counter()
    v = verificar(b, selo)
    R["verificar_s"] = time.perf_counter() - t1
    R["verificacao"] = v
    # determinismo: de novo, no mesmo processo
    selo2 = selar(b, "um.py")
    R["determinismo_mesmo_processo"] = {"psi": selo2["acom"]["psi"]["sha256"] == selo["acom"]["psi"]["sha256"], "theta": selo2["acom"]["theta"]["sha256"] == selo["acom"]["theta"]["sha256"],
                                        "kappa": selo2["acom"]["kappa"]["sha256"] == selo["acom"]["kappa"]["sha256"]}
    # caminho LITERAL: o reflect EMBUTIDO sobre o objeto inteiro (float64) -- as MESMAS partes?
    t2 = time.perf_counter()
    L = (np.frombuffer(b, dtype=np.uint8).astype(np.int16) - CENTRO).astype(np.float64)
    r = DimensionalMirror(angular_bits=BITS).reflect(L)
    t_reflect = time.perf_counter() - t2
    psi_l, theta_l = zlib.decompress(r.psi_packed), zlib.decompress(r.theta_packed)
    t3 = time.perf_counter()
    dec = DimensionalMirror(angular_bits=BITS).manifest(r)                         # a Dobra LITERAL: real
    t_manifest = time.perf_counter() - t3
    rec_lit = np.rint(dec).astype(np.int64) + CENTRO
    R["caminho_literal"] = {
        "reflect_embutido_s": t_reflect, "manifest_embutido_s": t_manifest,
        "psi_literal_eq_rapido": psi_l == p["psi_raw"], "theta_literal_eq_rapido": theta_l == p["theta_raw"],
        "metadata_g_max_eq": r.metadata["g_max"] == math.sqrt(p["m"]), "f_exp_literal": r.metadata["f_exp"], "f_exp_selo": selo["acom"]["estrutura"]["f_exp"],
        "erro_real_maximo_literal_antes_do_rint": float(np.abs(dec - L).max()),
        "reconstrucao_literal_apos_rint_igual_ao_objeto": bool(np.array_equal(rec_lit, np.frombuffer(b, dtype=np.uint8).astype(np.int64))),
        "bytes_em_que_o_real_difere_do_inteiro_por_mais_de_1e-6": int((np.abs(dec - L) > 1e-6).sum()),
        "bytes_em_que_o_real_difere_do_inteiro_por_mais_de_1e-2": int((np.abs(dec - L) > 1e-2).sum()),
        "leitura": "a Dobra pura (sem rint) NAO e' exata: o real difere do inteiro (erro maximo < 0,5, mas nao zero) e o rint ao reticulado o elimina"}
    del L, dec, rec_lit
    R["transporte_verbatim"] = estudo_transporte(b)
    return R


def estudo_transporte(b: bytes) -> Dict[str, Any]:
    """A camada de TRANSPORTE com as classes verbatim do operador (encrypt/decrypt: ofuscacao XOR + zlib), em amostras crescentes do um.py. A derivacao de
    chave do metodo (_derive_key: `out += sha256(...)` sobre bytes, em laco) cresce ACIMA do linear: o estudo MEDE o crescimento (razao de tempo por dobro de tamanho) em vez de
    rodar o objeto inteiro, e extrapola [DERIVED, nao medido] -- por isso o selo canonico NAO usa a camada de transporte, so as partes cruas."""
    linhas = []
    for kib in (64, 128, 256, 512, 1024):
        x = b[:kib * 1024]
        Lf = (np.frombuffer(x, dtype=np.uint8).astype(np.int16) - CENTRO).astype(np.float64)
        eng = ACOMMirrorCrypto(angular_bits=BITS)
        t0 = time.perf_counter()
        enc = eng.encrypt(Lf)
        t_enc = time.perf_counter() - t0
        t1 = time.perf_counter()
        dec = eng.decrypt(enc.psi_share, enc.theta_share, enc.master_key)
        t_dec = time.perf_counter() - t1
        pr = partes(x)
        linhas.append({"amostra_KiB": kib, "encrypt_s": t_enc, "decrypt_s": t_dec,
                       "psi_ofuscado_zlib_bytes": len(enc.psi_share.encrypted_states), "theta_ofuscado_zlib_bytes": len(enc.theta_share.encrypted_angles),
                       "psi_cru_bytes": len(pr["psi_raw"]), "theta_cru_bytes": len(pr["theta_raw"]),
                       "round_trip_apos_rint_igual": bool(np.array_equal(np.rint(dec).astype(np.int64) + CENTRO, np.frombuffer(x, dtype=np.uint8).astype(np.int64))),
                       "state_hash_igual_ao_psi_cru": enc.psi_share.state_hash == bytes.fromhex(_hx(pr["psi_raw"])),
                       "angle_hash_igual_ao_theta_cru": enc.theta_share.angle_hash == bytes.fromhex(_hx(pr["theta_raw"]))})
    t1m = linhas[-1]["encrypt_s"]
    cresc = linhas[-1]["encrypt_s"] / linhas[-2]["encrypt_s"] if linhas[-2]["encrypt_s"] > 0 else None
    # controles NA CAMADA DO OPERADOR (as mesmas classes): tamper na parte comprimida, mistura de shares, parte ausente (None)
    x = b[:64 * 1024]
    Lf = (np.frombuffer(x, dtype=np.uint8).astype(np.int16) - CENTRO).astype(np.float64)
    eng = ACOMMirrorCrypto(angular_bits=BITS)
    e1, e2 = eng.encrypt(Lf), eng.encrypt(Lf[::-1].copy())
    ctr = {}

    def tenta(nome, f):
        try:
            f()
            ctr[nome] = "ACEITOU"
        except Exception as ex:
            ctr[nome] = "RECUSOU:" + type(ex).__name__ + ":" + str(ex)[:60]
    raw = bytearray(zlib.decompress(e1.psi_share.encrypted_states))
    raw[len(raw) // 2] ^= 0x01
    psi_t = PsiShare(e1.psi_share.share_id, zlib.compress(bytes(raw), 9), e1.psi_share.state_hash, e1.psi_share.n_elements, e1.psi_share.shape, e1.psi_share.f_exp, e1.psi_share.state_entropy)
    tenta("tamper_1_bit_no_PsiShare", lambda: eng.decrypt(psi_t, e1.theta_share, e1.master_key))
    tenta("shares_de_objetos_diferentes", lambda: eng.decrypt(e1.psi_share, e2.theta_share, e1.master_key))
    tenta("PsiShare_ausente", lambda: eng.decrypt(None, e1.theta_share, e1.master_key))
    tenta("MasterKey_ausente", lambda: eng.decrypt(e1.psi_share, e1.theta_share, None))
    return {"amostras": linhas, "razao_de_tempo_encrypt_1024KiB_sobre_512KiB": cresc,
            "extrapolacao_para_o_um_py_inteiro_se_quadratico": {"bytes": len(b), "segundos": t1m * (len(b) / (1024 * 1024)) ** 2, "horas": t1m * (len(b) / (1024 * 1024)) ** 2 / 3600.0,
                                                               "estatuto": "[DERIVED] extrapolacao quadratica de uma medida; NAO foi rodado"},
            "controles_na_camada_do_operador": ctr,
            "zlib": getattr(zlib, "ZLIBNG_VERSION", None) and ("zlib-ng " + zlib.ZLIBNG_VERSION) or zlib.ZLIB_VERSION,
            "nota": "share_id/key_id aleatorios e creation_time=relogio: a camada de transporte nao e' reprodutivel byte a byte; os bytes comprimidos dependem da versao do zlib; o selo canonico hasheia as partes CRUAS"}


def estudo_perfil_sem_sinal(b: bytes) -> Dict[str, Any]:
    """CONTROLE do veredito: o perfil ingenuo `bytes como tensor sem sinal` (L = byte, centro 0). Em Q=8 a Dobra NAO e' exata; em Q=12 e' exata, mas Psi nao carrega
    sinal algum e Theta+kappa reconstroi o objeto SOZINHO -> o veredito de separacao tem de RECUSAR."""
    x = b[:4_000_000]
    L = np.frombuffer(x, dtype=np.uint8).astype(np.float64)
    out = {}
    for bits in (8, 12):
        r = DimensionalMirror(angular_bits=bits).reflect(L)
        theta = np.frombuffer(zlib.decompress(r.theta_packed), dtype=np.uint8 if bits <= 8 else np.uint16)
        qmax = (1 << bits) - 1
        dec = (r.metadata["g_max"] * np.sin(theta.astype(np.float64) / qmax * (math.pi / 2))) ** 2          # SO Theta + kappa(g_max), sinal + para todos
        rec = np.rint(dec).astype(np.int64)
        psi = np.frombuffer(zlib.decompress(r.psi_packed), dtype=np.uint8)
        estados = np.bincount(_unpack2bits(zlib.decompress(r.psi_packed), len(x)), minlength=4)
        out["Q%d" % bits] = {"n": len(x), "bytes_errados_so_com_theta_e_kappa": int((rec != np.frombuffer(x, dtype=np.uint8)).sum()),
                             "reconstrucao_exata_so_com_theta_e_kappa": bool(np.array_equal(rec, np.frombuffer(x, dtype=np.uint8))),
                             "estados_psi_usados": [int(c) for c in estados], "estados_com_sinal_negativo": int(estados[2] + estados[3])}
    out["veredito_esperado"] = "RECUSAR: no perfil sem sinal Psi nao carrega o sinal de L (so o de dL, irrelevante para a reconstrucao); em Q=12 Theta+kappa basta; em Q=8 nem a Dobra completa e' exata"
    # o veredito REAL (a funcao selar do prototipo) nos perfis ingenuos: troca o CENTRO global por um instante e tenta selar
    def tenta(centro, objeto):
        global CENTRO
        ant = CENTRO
        CENTRO = centro
        try:
            selar(objeto, "ingenuo")
            return "ACEITOU"
        except SeloRecusado as e:
            return "RECUSOU:" + str(e)[:140]
        finally:
            CENTRO = ant
    ascii_puro = bytes(c for c in b[:400000] if c < 128)
    out["veredito_real_da_funcao_selar"] = {
        "centro_0_sem_sinal__objeto_real_4MB": tenta(0, x),
        "centro_0_sem_sinal__ASCII_puro": tenta(0, ascii_puro),
        "centro_128__ASCII_puro (todo L negativo: Psi e' redundante)": tenta(128, ascii_puro),
        "centro_128__um_py_4MB (1,5% de nao-ASCII)": tenta(128, x),
        "centro_96__ASCII_puro (o perfil escolhido)": tenta(96, ascii_puro),
        "centro_96__um_py_4MB (o perfil escolhido)": tenta(96, x)}
    out["bytes_ASCII_puro_usados"] = len(ascii_puro)
    return out


def estudo_arquivos_da_rodada() -> Dict[str, Any]:
    """O core e o selo da rodada (a ultima rodada v398 que esta em Nos): bytes lidos, selados em sidecar, verificados."""
    objs = []
    for nome in ("um.py", "um_absoluto.json", "um_absoluto_selo.json"):
        p = os.path.join(NOS, nome)
        b = _ler(p)
        objs.append((nome, b))
    t0 = time.perf_counter()
    sc = sidecar(objs, quem="selo_acom_prototipo.py estudo (sandbox v399; nao instalado)")
    t_sc = time.perf_counter() - t0
    ver = {}
    for (nome, b), it in zip(objs, sc["objetos"]):
        t1 = time.perf_counter()
        v = verificar(b, it)
        ver[nome] = {"ok": v["ok"], "razoes": v["razoes"], "verificar_s": time.perf_counter() - t1}
    return {"sidecar": sc, "sidecar_s": t_sc, "verificacao": ver,
            "mtimes": {nome: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(os.path.join(NOS, nome)))) for nome, _ in objs}}


def estudo_colisoes() -> Dict[str, Any]:
    """Os nomes de nivel de modulo que a SECAO COLAVEL define colidem com algum nome de nivel de modulo do um.py v398? (varredura por linha; sem AST do arquivo de 38 MB)"""
    import ast
    import re
    linhas = open(os.path.abspath(__file__), "rb").read().decode("utf-8").split("\n")
    i_ini = next(i for i, l in enumerate(linhas) if l == "# (A) SECAO COLAVEL no um.py -- INICIO")
    i_fim = next(i for i, l in enumerate(linhas) if l == "# (A) SECAO COLAVEL no um.py -- FIM")
    secao = "\n".join(linhas[i_ini + 2:i_fim - 1]) + "\n"          # sem os banners; a mesma extracao do gerar_registro_declaracao.py
    arv = ast.parse(secao)
    nomes = set()
    for no in arv.body:
        if isinstance(no, (ast.FunctionDef, ast.ClassDef)):
            nomes.add(no.name)
        elif isinstance(no, ast.Assign):
            for alvo in no.targets:
                if isinstance(alvo, ast.Name):
                    nomes.add(alvo.id)
        elif isinstance(no, (ast.Import, ast.ImportFrom)):
            for al in no.names:
                nomes.add((al.asname or al.name).split(".")[0])
    um = _ler(UMPY).decode("utf-8", "replace").split("\n")
    achou = {}
    pat_def = {}
    for n in nomes:
        e = re.escape(n)
        pat_def[n] = re.compile(r"^(def|class)\s+" + e + r"\b|^" + e + r"\s*(:[^=]+)?=[^=]|^import\s+" + e + r"\b|^from\s+\S+\s+import\s+.*\b" + e + r"\b")
    for i, l in enumerate(um, 1):
        if not l or l[0] in " \t#'\"":
            continue
        ls = l.rstrip("\r")
        ligados = None
        if ls.startswith(("import ", "from ")):
            try:
                no = ast.parse(ls).body[0]
                ligados = {(al.asname or al.name).split(".")[0] for al in no.names}
            except Exception:
                ligados = None
        for n, pt in pat_def.items():
            if pt.search(ls):
                if ligados is not None and n not in ligados:
                    continue          # o nome so' aparece dentro de outro nome ou como alias (ex.: dataclass as _dc_v333): nao liga o nome
                achou.setdefault(n, []).append((i, ls[:100]))
    return {"secao_colavel_bytes": len(secao.encode("utf-8")), "secao_colavel_sha256": _hx(secao.encode("utf-8")), "nomes_de_nivel_de_modulo_definidos": sorted(nomes),
            "n_nomes": len(nomes), "colisoes_com_o_um_py_v398": {n: v[:3] for n, v in achou.items()},
            "leitura": ("os nomes que o um.py ja liga no nivel do modulo: os imports de hashlib, math, time (o MESMO modulo; reimportar e' inocuo) e ALPHA_FINE_CODATA_2018 "
                        "(linha 5584, MESMO valor: a secao o reatribui igual e o confere com SEALED_CODATA_ALPHA na carga); qualquer outro nome na lista e' colisao a resolver antes de colar")}


def cmd_estudo():
    t_ini = time.perf_counter()
    b = _ler(UMPY)
    resumo = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "python": sys.version.split()[0], "numpy": np.__version__,
              "zlib": getattr(zlib, "ZLIBNG_VERSION", None) and ("zlib-ng " + zlib.ZLIBNG_VERSION) or zlib.ZLIB_VERSION}
    print("[1/7] fontes ...")
    f = estudo_fontes()
    _grava("RECIBO_FONTES.json", f)
    resumo["fontes_todas_conferem"] = f["_todos_conferem"]
    _grava("RECIBO_COLISOES_DE_NOMES.json", estudo_colisoes())
    print("[2/7] exatidao do alfabeto (enumeracao exaustiva) ...")
    ex = estudo_exatidao_do_alfabeto()
    _grava("RECIBO_EXATIDAO_ALFABETO.json", ex)
    resumo["exatidao"] = {(("C%d_Q%d" % (r["centro"], r["angular_bits"]))): {"exato": r["exato"], "casos": r["casos"], "falhas": r["falhas_apos_rint"], "erro_real_max": r["erro_real_max"]} for r in ex["perfis"]}
    print("[3/7] conformidade com o codigo do operador ...")
    cf = estudo_conformidade(b)
    _grava("RECIBO_CONFORMIDADE.json", cf)
    print("[4/7] sobre o um.py v398 instalado (%d bytes) ..." % len(b))
    um = estudo_sobre_o_um_py(b)
    _grava("RECIBO_PROTOTIPO_um_py_v398.json", um)
    resumo["um_py"] = {"sha16": um["objeto"]["sha16"], "selar_total_s": um["selar_total_s"], "verificar_s": um["verificar_s"], "partes_bytes": um["tamanho_das_partes_cruas_bytes"],
                       "round_trip_exato": um["selo"]["acom"]["prova_de_reconstrucao"]["igual_ao_objeto_byte_a_byte"], "verificacao_ok": um["verificacao"]["ok"],
                       "literal_eq_rapido": [um["caminho_literal"]["psi_literal_eq_rapido"], um["caminho_literal"]["theta_literal_eq_rapido"]],
                       "transporte_round_trip": um["transporte_verbatim"]["amostras"][-1]["round_trip_apos_rint_igual"]}
    print("[5/7] core e selo da rodada (sidecar) ...")
    ar = estudo_arquivos_da_rodada()
    _grava("um_absoluto_selo_acom.json", ar["sidecar"])
    _grava("RECIBO_ARQUIVOS_DA_RODADA.json", {k: v for k, v in ar.items() if k != "sidecar"})
    print("[6/7] controles negativos ...")
    t0 = time.perf_counter()
    ctrl_completo = controles_negativos(b)
    t_ctrl = time.perf_counter() - t0
    ctrl_amostra = controles_negativos(b[:1 << 20])
    sem_sinal = estudo_perfil_sem_sinal(b)
    _grava("RECIBO_CONTROLES.json", {"objeto_inteiro_um_py": {**ctrl_completo, "tempo_s": t_ctrl}, "amostra_1MB": ctrl_amostra, "perfil_sem_sinal_controle_do_veredito": sem_sinal})
    resumo["controles"] = {"um_py_inteiro": [ctrl_completo["n_controles"], ctrl_completo["todos_recusados"]], "amostra_1MB": [ctrl_amostra["n_controles"], ctrl_amostra["todos_recusados"]]}
    print("[7/7] registro do core (formato do um.py) ...")
    reg = registro_core_v399(b, sha256_do_codigo=_hx(b))
    _grava("registro_core_selo_pela_propria_tecnologia_v399_EXEMPLO.json", reg)
    resumo["registro_core"] = {"all_verified": reg["all_verified"], "verdict": reg["verdict"], "tempo_total_s": reg["values"]["tempo_total_s"]}
    resumo["tempo_do_estudo_s"] = time.perf_counter() - t_ini
    _grava("RECIBO_RESUMO.json", resumo)
    print(json.dumps(resumo, ensure_ascii=False, indent=1, default=str))


def cmd_selar(args):
    objs = [(os.path.basename(a), _ler(a)) for a in args]
    sc = sidecar(objs, quem="selo_acom_prototipo.py selar")
    print(json.dumps(sc, ensure_ascii=False, indent=1, default=str))


def cmd_verificar(args):
    sc = json.load(open(args[0], encoding="utf-8"))
    por_nome = {it["nome"]: it for it in sc["objetos"]}
    rc = 0
    for a in args[1:]:
        nome = os.path.basename(a)
        v = verificar(_ler(a), por_nome[nome])
        print(nome, "OK" if v["ok"] else "RECUSADO", v["razoes"])
        rc |= 0 if v["ok"] else 1
    sys.exit(rc)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "estudo":
        cmd_estudo()
    elif len(sys.argv) >= 3 and sys.argv[1] == "selar":
        cmd_selar(sys.argv[2:])
    elif len(sys.argv) >= 4 and sys.argv[1] == "verificar":
        cmd_verificar(sys.argv[2:])
    else:
        print(__doc__)
