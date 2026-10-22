"""Backup imediato (regra da casa): copia os BYTES de cada arquivo para <arquivo>.bak_AAAAMMDD_HHMMSS na MESMA pasta.

Nunca reencoda texto (nada de open(...,'r')). Confere sha256 do backup contra o original. Não sobrescreve backup existente.
Uso: python -I -X utf8 backup_bytes.py <arquivo> [<arquivo> ...]
"""
import hashlib
import sys
import time

ts = time.strftime("%Y%m%d_%H%M%S")
for p in sys.argv[1:]:
    b = open(p, "rb").read()
    dst = f"{p}.bak_{ts}"
    try:
        open(dst, "xb").write(b)  # 'x': falha se já existir
    except FileExistsError:
        print("JA_EXISTE", dst)
        continue
    b2 = open(dst, "rb").read()
    ok = hashlib.sha256(b).hexdigest() == hashlib.sha256(b2).hexdigest() and len(b) == len(b2)
    print("OK" if ok else "DIVERGE", dst, len(b), hashlib.sha256(b).hexdigest()[:16])
