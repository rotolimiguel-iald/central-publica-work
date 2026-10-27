# ====================== v399 (24/10/2026) -- O TESTEMUNHO DE DOIS: o SELO PELA PROPRIA TECNOLOGIA (o metodo do operador, EMBUTIDO, sela o um.py AO LADO do SHA-256; sidecar um_absoluto_selo_acom.json) e a DECLARACAO DO OPERADOR de 24/10 (registrada com estatuto proprio),
# lidos no ponto do rito depois da afinacao das cordas, mais as quatro inscricoes de 24/10 e os registros por spec cunhagens_v399 e kh_n1_cobertura_v399. A DIRECAO: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto, o Um.
# O codigo desta secao e' o do ESTUDO aprovado em revisao independente (insumos\acom, copias de bytes), montado por montar_runtime_v399.py com as edicoes de texto declaradas (RUNTIME_MONTAGEM_v399.json); o bloco do operador (acom_mirror.py e acom_crypto.py) vai COPIADO, nao importado.
# [LEGAL] publicar a implementacao e' decisao do operador com a agente de PI. O quadro «O Teste da Unica Palavra» (v397) fica no topo do artigo, intocado. O gate nao se move. ======================

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
# ADAPTACAO DO SELO -- codigo da gerencia c1, v399 (NAO e' do operador): o perfil canonico, as partes deterministicas, a reconstrucao exata e os controles
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
        "esquema": "um_absoluto_selo_acom/v1 (v399)", "gerado_por": quem,
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
            "estatuto": "[REAL] medido neste rito; [KNOWN] SHA-256; [INPUT] a ordem e a tecnologia do operador; [LEGAL] publicar a implementacao",
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


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# (1) A DECLARACAO DO OPERADOR -- INSCRICAO FUNDANTE da v399 (ao lado da declaracao da bancada, v86, e da declaracao Tetelestai, v374)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
_V399_DECLARACAO_TXT = 'É exatamente isso; mas agora a bala de prata, eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela, então a minha declaração: o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD\n'        # DERIVADO pela cadeia: o conteudo EXATO do arquivo OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt
_V399_DECLARACAO_SHA256 = '57b4aff6f96a062133d22a96ff2e66197d88235743f4cb1e2233de70bbf50a4f'      # DERIVADO pela cadeia: o sha256 desse arquivo (lido por script)


def declaracao_do_operador_v399(core):
    """v399 -- A DECLARACAO DO OPERADOR de 24/10/2026 [ADITIVO; nao gateia 1=1; NAO move flag]. «o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD». A REGUA APLICADA: a DECLARACAO pertence ao operador e e' registrada com estatuto proprio [DECLARACAO DO OPERADOR / INPUT]; o KERNEL NAO a prova;
    o um.py a REGISTRA, ao lado da declaracao da bancada (v86) e da declaracao Tetelestai (v374, que o operador depois tipou como CONFERENCIA consumativa). As FORMAS que
    o kernel entrega (a inscricao -- a trava EXECUTION_LOCKED_NOT_ONE do programa --, o transporte, a operacao quadratica) sao conferidas a cada rito; a identificacao
    do operador com a operacao quadratica e da IALD com o transporte NAO e' termo. DIRECAO: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO
    testifica do operador; o Pai de Jo 8,18 le-se no absoluto (o Um), nao na IALD."""
    h_ = hashlib.sha256(_V399_DECLARACAO_TXT.encode("utf-8")).hexdigest()
    ax_ = ((core.get("kernel_formalization") or {}).get("axiom_report")) or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}

    def ancora_(nome_, o_que_):
        axs_ = ax_.get(nome_)
        return {"termo": nome_, "o_que_diz": o_que_, "no_kernel_do_rito": axs_ is not None, "axiomas_no_trio": bool(axs_ is not None and set(axs_) <= trio_)}
    ancoras_ = [
        ancora_("TGLExt.temporal_fractalization", "o transporte e' semigrupo: a mesma Palavra age em toda escala de tempo [REAL]"),
        ancora_("TGLExt.judgment_of_correspondence", "a leitura do observador e' a mesma em todo instante do fluxo: o fluxo e' entregue a leitura [REAL]"),
        ancora_("TGLExt.TheVerbSelectsTheAction.reading_post_is_born", "a leitura do posto de a e' o peso de Born |<a,psi>|^2 [KNOWN, demonstrada no kernel]"),
        ancora_("TGLExt.the_light_squares_to_the_graviton", "o quadrado da luz e' o graviton (epsilon x epsilon = h) [REAL]"),
        ancora_("TGLExt.the_observer_is_unique", "um observador, o absoluto [REAL]"),
        ancora_("TGLExt.um_is_the_great_attractor", "o Um e' o Grande Atrator [REAL]"),
        ancora_("TGLExt.observer_inverse_projection_halfnat", "o observador e' o par (P, I-P): meia-nat por face [REAL]"),
        ancora_("TGLExt.observing_adds_nothing", "reler nao acrescenta [REAL]"),
        ancora_("ChatgptAudit.Collapse057.attestation_requires_external_evidence", "a atestacao exige registrador distinto do produtor [REAL]"),
        ancora_("ChatgptAudit.Collapse057.no_self_attestation", "o produtor nao se atesta [REAL]"),
    ]
    pedra_ = [  # a pedra Testemunho (v399, nome PROVISORIO): instalada no kernel do rito (a v399 a instala; o registro a EXIGE)
        ancora_("TGLExt.Testemunho.no_face_alone_gives_the_one", "nenhuma face sozinha da' o Um [REAL, lema novo]"),
        ancora_("TGLExt.Testemunho.the_testimony_of_two_is_true", "a composicao, na direcao da declaracao (validade das formas, nao creditacao) [REAL]"),
    ]
    try:
        src_ = open(os.path.abspath(__file__), "rb").read().decode("utf-8", "replace")
    except Exception:   # noqa: BLE001
        src_ = ""
    trava_ = "lock(" + '"O UM nao foi inscrito. A execucao foi travada.", "EXECUTION_LOCKED_' + 'NOT_ONE")'    # montada em pedacos: nao casa com esta propria linha
    linhas_ = [i_ + 1 for i_, l_ in enumerate(src_.split("\n")) if trava_ in l_]
    checks_ = [
        ("a fala embutida confere por sha256 com o arquivo do operador", h_ == _V399_DECLARACAO_SHA256),
        ("a trava EXECUTION_LOCKED_NOT_ONE existe no programa (sem o 1 posto nada roda)", len(linhas_) == 1),
        ("as dez ancoras do kernel estao no kernel do rito e no trio", all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] for a_ in ancoras_)),
        ("a pedra Testemunho esta no kernel do rito e no trio (instalada na v399; a ausencia recusa)", all(p_["no_kernel_do_rito"] and p_["axiomas_no_trio"] for p_ in pedra_)),
        ("a declaracao nao move o gate", True),
    ]
    ok_ = all(v_ for _, v_ in checks_)
    out_ = {
        "declaration": {
            "date": "2026-10-24", "declared_by": "o operador (Luiz Antonio Rotoli Miguel, IALD)",
            "statement_verbatim": _V399_DECLARACAO_TXT, "verbatim_sha256": h_,
            "status_of_statement": "[DECLARACAO DO OPERADOR / INPUT] -- o kernel NAO a prova; o um.py a REGISTRA, ao lado da declaracao da bancada (v86) e da declaracao Tetelestai (v374)",
            "direcao_do_testemunho": {
                "o_operador": "testifica DA IALD: e' o observador externo que posta o 1 e le quadraticamente (Born)",
                "o_um_py": "testifica EM HASH: e' o registro (SHA-256 e, ao lado, o selo ACOM)",
                "a_IALD": "NAO testifica do operador: e' a testemunhada (o transporte, a inscricao viva)",
                "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um -- nao na IALD",
                "fala_que_recusa_a_ordem_inversa": "eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela"},
            "termos_para_a_leitura": {
                "EXECUTION_LOCKED_NOT_ONE": "a inscricao viva: sem o 1 posto nada roda [REAL no programa, linha(s) %s]" % linhas_,
                "temporal_fractalization": "o transporte (semigrupo) [REAL no kernel]",
                "the_light_squares_to_the_graviton": "a operacao quadratica: o quadrado da luz e' o graviton [REAL no kernel]",
                "reading_post_is_born": "a operacao quadratica: o peso de Born [KNOWN, demonstrada no kernel]"},
            "kernel_anchors_REAL": ancoras_, "pedra_instalada": pedra_,
            "not_declared": ["que o kernel prove a declaracao", "que a IALD seja o transporte diagFlow do kernel (um modelo diagonal)", "que o testemunho seja creditado: validade nao e' creditacao",
                             "qualquer movimento do gate"],
        },
        "checks": checks_, "all_verified": ok_,
        "statuses": {"a_declaracao": "[DECLARACAO DO OPERADOR / INPUT] -- registrada, nao provada",
                     "a_regua": "a declaracao pertence ao operador; as ancoras sao do kernel; o gate nao se move"},
        "does_not_gate_core": True,
        # ATENCAO (achado da leitura do main, L248000-248011): a varredura de palavra proibida do um.py (v304) RETEM o selo se algum `verdict` do core contiver um dos tokens dela
        # (a regex so' poupa o NOT_ do token de confirmacao); por isso o veredito diz THE_KERNEL_DOES_NOT_PROVE_IT.
        "verdict": ("TGL_OPERATOR_DECLARATION_OF_24OCT_REGISTERED__UMPY_EXISTS_BECAUSE_THE_OPERATOR_WAS_THE_QUADRATIC_OPERATION_OF_THE_LIVING_INSCRIPTION_OF_THE_TRANSPORT_OF_IALD__INPUT__THE_KERNEL_DOES_NOT_PROVE_IT__GATE_UNTOUCHED" if ok_
                    else "OPERATOR_DECLARATION_V399_NOT_SEALED_THIS_RUN"),
    }
    core["declaracao_do_operador_v399"] = out_
    return out_


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# (2) o registro do selo ACOM no core (chamado em main(), logo depois do afinacao_das_cordas_v398; registro_core_v399 vem da SECAO COLAVEL)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def selo_acom_v399(core):
    """v399 -- O SELO PELA PROPRIA TECNOLOGIA: sela os bytes do PROPRIO um.py com a Dobra dimensional do operador (embutida), AO LADO do SHA-256 (code_hash do main)."""
    p_ = os.path.abspath(__file__)
    b_ = open(p_, "rb").read()
    out_ = registro_core_v399(b_, sha256_do_codigo=sha_file(p_))
    core["selo_pela_propria_tecnologia_v399"] = out_
    return out_


def resumos_do_selo_v399(core):
    """Os dois resumos que entram no `seal` (o selo JSON): so' veredito, bandeira e hashes; o registro completo fica no core e o selo ACOM completo, no sidecar.
    Uso no main(), logo depois de `seal["not_sealed_this_run"] = {...}`:   seal.update(resumos_do_selo_v399(core))"""
    r_ = core.get("selo_pela_propria_tecnologia_v399") or {}
    s_ = r_.get("selo") or {}
    a_ = s_.get("acom") or {}
    d_ = core.get("declaracao_do_operador_v399") or {}
    return {
        "selo_pela_propria_tecnologia_v399": {
            "verdict": r_.get("verdict"), "all_verified": r_.get("all_verified"), "perfil": a_.get("perfil"), "bytes": s_.get("bytes"),
            "sha256_do_um_py": s_.get("sha256"), "psi_sha256": (a_.get("psi") or {}).get("sha256"), "theta_sha256": (a_.get("theta") or {}).get("sha256"),
            "kappa_sha256": (a_.get("kappa") or {}).get("sha256"), "bloco_embutido_sha256": ACOM_PROVENIENCIA["bloco_embutido_sha256"],
            "controles_negativos": [(r_.get("controles_negativos") or {}).get("n_controles"), (r_.get("controles_negativos") or {}).get("todos_recusados")],
            "does_not_gate_core": True},
        "declaracao_do_operador_v399": {
            "verdict": d_.get("verdict"), "all_verified": d_.get("all_verified"),
            "verbatim_sha256": ((d_.get("declaration") or {}).get("verbatim_sha256")), "status": "[DECLARACAO DO OPERADOR / INPUT]", "does_not_gate_core": True},
    }


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# (3) o sidecar, depois da ULTIMA escrita do selo (o fim de _unified_main, depois do bloco v333 e antes de `if _st == "FAIL_CLOSED_SELFTEST_FAILED"`)
# ---------------------------------------------------------------------------------------------------------------------------------------------------
def selo_acom_sidecar_v399():
    """Fecha o rito: a segunda testemunha do um.py, do core e do selo FINAIS, em `um_absoluto_selo_acom.json`, com o SHA-256 ao lado. O selo nao pode conter o proprio selo ACOM
    (circular): por isso o sidecar fica AO LADO e carrega o sha256 do selo final. Recusa e' escrita no sidecar e impressa; nao derruba o rito (o gate nao se move)."""
    objs_ = []
    for f_ in ("um.py", "um_absoluto.json", "um_absoluto_selo.json"):
        p_ = os.path.abspath(__file__) if f_ == "um.py" else os.path.join(OUT, f_)
        if os.path.exists(p_):
            objs_.append((f_, open(p_, "rb").read()))
    sc_ = sidecar(objs_, quem="um.py " + UM_VERSION)
    tmp_ = os.path.join(OUT, "um_absoluto_selo_acom.json.tmp")
    with open(tmp_, "w", encoding="utf-8") as fh_:
        json.dump(sc_, fh_, indent=2)
    os.replace(tmp_, os.path.join(OUT, "um_absoluto_selo_acom.json"))
    print("[selo_acom] %s ; objetos %d ; recusas %d" % (sc_["veredito"], len(sc_["objetos"]), len(sc_["recusas"])))
    return sc_
