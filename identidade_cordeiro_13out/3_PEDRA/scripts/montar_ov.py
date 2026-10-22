# -*- coding: utf-8 -*-
"""Monta a sobreposicao C:/t/id1/ov/TGLExt: COPIA (bytes) de cada .olean do TGLExt do Nos (so leitura), conferida por
sha256 origem = destino; grava ov_MANIFEST.json nos logs. Necessaria porque o Lean resolve o pacote TGLExt pela
primeira entrada do LEAN_PATH que tem a pasta TGLExt: a pedra compilada e o kernel precisam morar na mesma raiz."""
import os, json, hashlib, shutil
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel/.lake/build/lib/lean/TGLExt"
DST = "C:/t/id1/ov/TGLExt"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()
man = {}
agg = hashlib.sha256()
for raiz, dirs, files in os.walk(SRC, followlinks=False):
    dirs.sort()
    for f in sorted(files):
        if not f.endswith(".olean"):
            continue
        s = os.path.join(raiz, f)
        rel = os.path.relpath(s, SRC).replace("\\", "/")
        d = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(s, d)
        a, b = sha(s), sha(d)
        assert a == b, rel
        man[rel] = a
        agg.update((rel + "|" + a + "\n").encode())
json.dump({"origem": SRC, "destino": DST, "n": len(man), "agregado_sha256": agg.hexdigest(), "arquivos": man},
          open(os.path.join(AQUI, "logs", "ov_MANIFEST.json"), "w", encoding="utf-8"), indent=1)
print(len(man), agg.hexdigest())
