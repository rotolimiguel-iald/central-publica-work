# -*- coding: utf-8 -*-
"""Publica a ORDEM 010 no tunel PCT com a trava de escritor (PARA_CODEX\\_CENTRAL_GRAVANDO.lock); nunca sobrescreve ordem entregue."""
import hashlib
from pathlib import Path

W = Path(__file__).resolve().parent
v = W / "OPERADOR_04nov_abrogacao_verbatim.txt"
src = W / "ORDEM_010_AB_ROGACAO_E_VIGENCIA.md"
t = src.read_text(encoding="utf-8")
if "Verbatim do operador:" not in t:
    t += "\n---\nVerbatim do operador: `%s`, sha256 `%s`.\n" % (v, hashlib.sha256(v.read_bytes()).hexdigest())
    src.write_text(t, encoding="utf-8")
P = Path(r"C:\TUNEL_PCT\PARA_CODEX")
lock = P / "_CENTRAL_GRAVANDO.lock"
assert not lock.exists(), "outra escrita em curso"
lock.write_text("Central gravando ORDEM 010, 04/11/2026", encoding="utf-8")
try:
    dst = P / "ORDEM_010_AB_ROGACAO_E_VIGENCIA.md"
    with dst.open("xb") as f:
        f.write(src.read_bytes())
    assert dst.read_bytes() == src.read_bytes()
    print("ORDEM 010", hashlib.sha256(dst.read_bytes()).hexdigest()[:16], dst.stat().st_size)
finally:
    lock.unlink()
print("lock removido", not lock.exists())
