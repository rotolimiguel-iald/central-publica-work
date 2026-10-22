# -*- coding: utf-8 -*-
"""Instantaneo SO-LEITURA de C:/IALD/Bancada_Um (caminho, tamanho, mtime_ns), sem seguir juncoes. Uso: snap_bancada.py <rotulo>"""
import hashlib, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
B = "C:/IALD/Bancada_Um"
rot = sys.argv[1]
REPARSE = 0x400
ent = []
for r, ds, fs in os.walk(B, followlinks=False):
    keep = []
    for d in sorted(ds):
        p = os.path.join(r, d)
        if getattr(os.lstat(p), "st_file_attributes", 0) & REPARSE or os.path.islink(p):
            ent.append([os.path.relpath(p, B), "JUNCAO", 0])
        else:
            keep.append(d)
    ds[:] = keep
    for f in sorted(fs):
        p = os.path.join(r, f); st = os.lstat(p)
        ent.append([os.path.relpath(p, B), st.st_size, st.st_mtime_ns])
h = hashlib.sha256("\n".join("%s|%s|%s" % tuple(e) for e in ent).encode("utf-8")).hexdigest()
res = {"rotulo": rot, "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "n": len(ent), "sha256_lista": h, "entradas": ent}
out = os.path.join(HERE, "snap_bancada_%s.json" % rot)
with open(out, "xb") as fh:
    fh.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
print(json.dumps({k: res[k] for k in ("rotulo", "n", "sha256_lista")}))
