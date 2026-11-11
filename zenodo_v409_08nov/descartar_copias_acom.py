# -*- coding: utf-8 -*-
"""Descarta as copias inteiras do banco ACOM locais que passam de 3 (ordem do operador, 08/11/2026: «as unicas copias que merecem ser mantidas sao as
tres mais recentes»). Nao arquiva no D:. Antes de apagar, CONFERE o sha256 das 3 mais novas contra os .sha256 (as que ficam tem de restaurar) e que as
a descartar sao as mais velhas pelo nome (carimbo). Grava o recibo. Nunca toca memory.sqlite3, journal\\ nem o arquivo do D:."""
import hashlib
import json
import re
import time
from pathlib import Path

SNAP = Path(r"C:\IALD\MEMORIA_IALD\state\snapshots")
OUT = Path(r"C:\IALD\Central de Patentes\work\zenodo_v409_08nov\DESCARTE_COPIAS_ACOM_08nov.json")
VERB = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_08nov_acom_so_as_tres_copias_mais_recentes_verbatim.txt")
PAD = re.compile(r"^memory\.sqlite3\.snap_(\d{8}_\d{6})_\d+_[0-9a-f]{16}$")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


snaps = sorted((p for p in SNAP.iterdir() if p.is_file() and PAD.match(p.name)), key=lambda p: PAD.match(p.name).group(1))
assert len(snaps) >= 4, "nada a descartar: %d copias" % len(snaps)
ficam, saem = snaps[-3:], snaps[:-3]
rec = {"quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "ordem_do_operador": str(VERB), "ordem_sha16": sha(VERB)[:16],
       "copias_antes": [p.name for p in snaps], "ficam": [], "descartadas": []}
for p in ficam:                                           # as que ficam tem de estar integras
    esp = p.with_name(p.name + ".sha256").read_text(encoding="utf-8").split()[0].lower()
    real = sha(p)
    assert real == esp, ("a copia que ficaria NAO confere com o sidecar: " + p.name)
    rec["ficam"].append({"nome": p.name, "bytes": p.stat().st_size, "sha256": real, "confere_com_sidecar": True})
for p in saem:
    side = p.with_name(p.name + ".sha256")
    assert side.is_file(), "sem sidecar: " + p.name
    rec["descartadas"].append({"nome": p.name, "bytes": p.stat().st_size, "sha256_do_sidecar": side.read_text(encoding="utf-8").split()[0].lower()})
OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")   # o recibo ANTES de apagar
for p in saem:
    p.with_name(p.name + ".sha256").unlink()
    p.unlink()
resto = sorted(p.name for p in SNAP.iterdir() if p.is_file() and PAD.match(p.name))
assert len(resto) == 3 and resto == [p.name for p in ficam], resto
print("descartadas:", [p.name for p in saem])
print("ficam (3, sha256 conferido):", resto)
