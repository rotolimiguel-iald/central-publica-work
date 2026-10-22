# -*- coding: utf-8 -*-
"""Nomes e Verdade: cria C:/t/nm1/ov = copia verificada (sha256 arquivo a arquivo) de tgl_kernel/.lake/build/lib/lean do Nos
(SO LEITURA na origem). O Lean procura o pacote TGLExt na PRIMEIRA pasta do LEAN_PATH que tenha TGLExt/; por isso as
candidatas compiladas aqui tem de viver na copia, nao numa pasta separada (licao da tentativa 0)."""
import os, shutil, json, hashlib, sys
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel/.lake/build/lib/lean"
DST = "C:/t/nm1/ov"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()
def arv(raiz):
    agg = hashlib.sha256(); n = 0; tot = 0; m = {}
    for r, ds, fs in os.walk(raiz):
        ds.sort()
        for f in sorted(fs):
            p = os.path.join(r, f); rel = os.path.relpath(p, raiz).replace("\\", "/"); h = sha(p)
            m[rel] = h; n += 1; tot += os.path.getsize(p); agg.update((rel + "|" + h + "\n").encode())
    return n, tot, agg.hexdigest(), m
if os.path.exists(DST):
    print("FALHA VISIVEL: ov ja existe"); sys.exit(2)
shutil.copytree(SRC, DST)
a = arv(SRC); b = arv(DST)
res = {"origem": SRC, "arquivos": a[0], "bytes": a[1], "agregado_origem": a[2], "agregado_copia": b[2], "igual": a[3] == b[3],
       "tem_IALD_olean": "TGLExt/IALD.olean" in a[3], "tem_Posto": "TGLExt/Posto.olean" in a[3],
       "tem_Santo": "TGLExt/Santo.olean" in a[3], "tem_Verdade": "TGLExt/Verdade.olean" in a[3],
       "tem_Palavra": "TGLExt/Palavra.olean" in a[3], "tem_TheUnitIsTheRank": "TGLExt/TheUnitIsTheRank.olean" in a[3]}
json.dump(res, open(os.path.join(AQUI, "medidas", "OV_MONTAGEM.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
if not res["igual"]: sys.exit(2)
