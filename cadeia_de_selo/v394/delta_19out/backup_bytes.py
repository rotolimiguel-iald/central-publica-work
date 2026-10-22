# -*- coding: utf-8 -*-
"""backup_bytes.py -- DELTA 19/10 (rodada d19c): copia de BYTES (regra do backup imediato) de cada arquivo dado, na mesma pasta, como <arquivo>.bak_<STAMP>_c1d19c; verifica igualdade; recusa se o backup ja existe.
uso: python -I -B -X utf8 backup_bytes.py <STAMP> <arquivo> [<arquivo> ...]   (caminhos absolutos ou relativos a V = pasta pai desta pasta; arquivo inexistente e' dito e pulado)"""
import hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
stamp, arqs = sys.argv[1], sys.argv[2:]
assert stamp.replace("_", "").isdigit() and len(stamp) == 15, "STAMP deve ser AAAAMMDD_HHMMSS"
rc = 0
for a in arqs:
    p = a if os.path.isabs(a) else os.path.join(V, a)
    if not os.path.isfile(p):
        print("INEXISTENTE (pulado):", p); continue
    b = open(p, "rb").read(); bak = p + ".bak_%s_c1d19c" % stamp
    if os.path.exists(bak):
        print("JA EXISTE (nao sobrescrevo):", bak); rc = 2; continue
    open(bak, "wb").write(b)
    ok = open(bak, "rb").read() == b
    print("%s %s -> %s (%d B, sha16 %s)" % ("OK " if ok else "FALHOU", os.path.basename(p), os.path.basename(bak), len(b), hashlib.sha256(b).hexdigest()[:16]))
    rc |= 0 if ok else 1
sys.exit(rc)
