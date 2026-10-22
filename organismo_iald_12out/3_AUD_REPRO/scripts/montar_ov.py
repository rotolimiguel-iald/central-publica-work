# -*- coding: utf-8 -*-
"""Monta a SOBREPOSICAO ov = copia verificada (byte a byte) da pasta compilada do kernel do Nos
(.lake/build/lib/lean, SO LEITURA na origem) dentro de 2_CONSTRUCAO/sandbox/ov. Motivo (F_KERNEL 12/10, medido):
o lean resolve a raiz TGLExt na PRIMEIRA pasta do LEAN_PATH que a contem; para importar pedras candidatas
TGLExt.* nao instaladas, os .olean delas e os do kernel tem de morar na mesma raiz. Nada e escrito na origem.
Uso: montar_ov.py copiar | verificar"""
import os, sys, shutil, hashlib, json, time, datetime
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel/.lake/build/lib/lean"
OV = os.path.join(AQUI, "sandbox", "ov")
def L(p): return os.path.abspath(p)
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()
modo = sys.argv[1]
t0 = time.time()
if modo == "copiar":
    if os.path.exists(OV): print("FALHA VISIVEL: ov ja existe"); sys.exit(2)
    shutil.copytree(L(SRC), L(OV))
n = 0; dif = []; falta = []; agg = hashlib.sha256(); tot = 0
for r, ds, fs in os.walk(L(SRC)):
    ds.sort()
    for f in sorted(fs):
        s = os.path.join(r, f); rel = os.path.relpath(s, L(SRC)); d = os.path.join(L(OV), rel)
        if not os.path.exists(d): falta.append(rel); continue
        hs = sha(s); tot += os.path.getsize(s)
        if hs != sha(d): dif.append(rel)
        agg.update((rel.replace("\\", "/") + "|" + hs + "\n").encode()); n += 1
extras = []
for r, ds, fs in os.walk(L(OV)):
    for f in fs:
        rel = os.path.relpath(os.path.join(r, f), L(OV))
        if not os.path.exists(os.path.join(L(SRC), rel)): extras.append(rel.replace("\\", "/"))
res = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "modo": modo, "origem": SRC, "ov": OV,
       "arquivos": n, "bytes": tot, "diferentes": dif, "faltando": falta, "extras_no_ov": sorted(extras),
       "agregado_sha256_origem": agg.hexdigest(), "segundos": round(time.time() - t0, 1)}
json.dump(res, open(os.path.join(AQUI, "OV_%s.json" % modo.upper()), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("extras_no_ov",)} | {"n_extras": len(extras)}, ensure_ascii=False))
