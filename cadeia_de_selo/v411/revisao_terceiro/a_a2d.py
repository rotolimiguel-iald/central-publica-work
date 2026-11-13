import json, os, hashlib
import a_lib
f = a_lib.Fonte(a_lib.CAND, "cand")
ns = f.carregar(["_V411_H0DN_CONTRACT"]); C = ns["_V411_H0DN_CONTRACT"]
W = r"C:\IALD\Central de Patentes\work"; E = os.path.join(W, "h0dn_bg1_v411_emenda_11nov")
sha = lambda b: hashlib.sha256(b).hexdigest()
for c in C["citados"]:
    for base in (E, W, os.path.join(W, "h0dn_bg1_v410_09nov")):
        p = os.path.join(base, c["rel"])
        if os.path.exists(p):
            b = open(p, "rb").read()
            print("citado", c["nome"], "| em", os.path.basename(base), "| sha ok:", sha(b) == c["sha256"], "| bytes ok:", len(b) == c["bytes"]); break
    else:
        print("citado", c["nome"], "NAO ENCONTRADO", c["rel"])
