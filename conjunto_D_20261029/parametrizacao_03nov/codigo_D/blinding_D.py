# -*- coding: utf-8 -*-
"""blinding_D.py -- semente de cegueira NOVA do conjunto D (etiqueta HMAC propria; nao reaproveita a semente da 013-bis).

Cegueira PROCEDURAL no mesmo host (como no V1: "a certificacao de cegueira e deste V1"). O valor da semente nunca e
impresso nem gravado em work/log/tunel: so o sha256 (compromisso). Offsets: u = (int(HMAC-SHA256(semente, ETIQUETA+evento+':'+campo)[:8]) + .5)/2**64,
offset = ESCALA*(2u-1) em (-1, 1), somado a TODAS as amostras do campo. Estatisticas invariantes a deslocamento (std ddof=1, W90)
passam intactas; media, mediana e sinal ficam sob offset de ate +-1 (contra |delta_pred| ~ 0,4).
A assinatura de shifted_samples() e a mesma do blinding.py da 013-bis (drop-in para o pe_runner copiado).
"""
import hashlib
import hmac
import os
import stat
from pathlib import Path

import numpy as np

ETIQUETA = "RAMOB_V1_D:"
ESCALA = 1.0
CAMPOS = ("dtau220", "dtau440", "domega220", "domega440")
SEMENTE_PADRAO = "C:/Users/rotol/.iald_privado/conjunto_D_20261029/BLIND_SEED_D.bin"


def _native(p):
    p = str(p).replace(chr(92), "/")
    if os.name == "posix" and len(p) > 2 and p[1] == ":":
        return "/mnt/" + p[0].lower() + p[2:]
    return p


def _sha(path):
    return hashlib.sha256(Path(_native(path)).read_bytes()).hexdigest()


def criar_semente(caminho=SEMENTE_PADRAO):
    """Cria a semente (32 bytes de os.urandom) em modo EXCLUSIVO (nunca sobrescreve). Devolve SO o compromisso (sha256)."""
    p = Path(_native(caminho))
    p.parent.mkdir(parents=True, exist_ok=True)
    seed = os.urandom(32)
    with open(p, "xb") as f:
        f.write(seed)
        f.flush()
        os.fsync(f.fileno())
    os.chmod(p, stat.S_IREAD)
    commit = hashlib.sha256(seed).hexdigest()
    del seed
    return commit


def compromisso(caminho=SEMENTE_PADRAO):
    return _sha(caminho)


def _ler_semente(caminho, compromisso_esperado):
    p = Path(_native(caminho))
    seed = p.read_bytes()
    if len(seed) != 32:
        raise ValueError("semente de cegueira com tamanho invalido")
    if hashlib.sha256(seed).hexdigest() != compromisso_esperado:
        raise ValueError("compromisso da semente difere")
    return seed


def _offset(seed, evento, campo, escala):
    d = hmac.new(seed, (ETIQUETA + evento + ":" + campo).encode(), hashlib.sha256).digest()
    u = (int.from_bytes(d[:8], "big") + 0.5) / (2 ** 64)
    return escala * (2 * u - 1)


def shifted_samples(columns, event, registration):
    """Mesma interface do blinding.py original. Devolve amostras DESLOCADAS; o offset nunca sai desta funcao."""
    present = [k for k in CAMPOS if k in columns]
    if "dtau220" not in present:
        raise ValueError("dtau220 e o campo livre do V1 e e obrigatorio")
    n = {len(columns[k]) for k in present}
    if len(n) != 1 or next(iter(n)) < 2:
        raise ValueError("amostras pareadas nao vazias exigidas")
    b = registration["blinding"]
    seed = _ler_semente(b["seed_path"], b["seed_commitment_sha256"])
    escala = float(b.get("offset_half_range", ESCALA))
    if not np.isfinite(escala) or escala <= 0:
        raise ValueError("escala de offset invalida")
    out = {}
    for name in present:
        a = np.asarray(columns[name], dtype=float)
        if a.ndim != 1 or not np.isfinite(a).all():
            raise ValueError("amostras nao finitas antes da cegueira")
        out["blinded_" + name] = (a + _offset(seed, event, name, escala)).tolist()
    return {"status": "BLINDED_SAMPLES__NO_UNBLINDING_AUTHORIZATION", "event": event, "columns": out,
            "seed_commitment_sha256": b["seed_commitment_sha256"],
            "warning": "Offset-censored; means and signs have no physical interpretation. Raw PE files remain unread by the analyst."}


def unblind_samples(blinded_columns, event, registration):
    """So para o ato de ABERTURA (abrir_D.py), depois da autorizacao ligada ao hash do estagio cego."""
    b = registration["blinding"]
    seed = _ler_semente(b["seed_path"], b["seed_commitment_sha256"])
    escala = float(b.get("offset_half_range", ESCALA))
    out = {}
    for name, v in blinded_columns.items():
        campo = name[len("blinded_"):] if name.startswith("blinded_") else name
        out[campo] = np.asarray(v, dtype=float) - _offset(seed, event, campo, escala)
    return out


def estatisticas_invariantes(blinded_dtau220):
    """O UNICO acesso do estagio cego as amostras deslocadas: std ddof=1 e largura 90 % (q95-q05). Nada de media/mediana."""
    a = np.asarray(blinded_dtau220, dtype=float)
    if a.ndim != 1 or len(a) < 100 or not np.isfinite(a).all():
        raise ValueError("amostras insuficientes ou nao finitas")
    q = np.quantile(a, [0.05, 0.95])
    return {"sigma": float(np.std(a, ddof=1)), "w90": float(q[1] - q[0]), "n": int(len(a))}
