# -*- coding: utf-8 -*-
"""MANIFESTO da pasta 4_RELATORIO ao fim do relatorio R2: sha256 de cada arquivo (somente leitura + 1 arquivo)."""
import hashlib, json, os, sys, time
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LONG = "\\\\?\\"
NOME = "MANIFESTO_4_RELATORIO_R2.json"
man = {"documento": "MANIFESTO da pasta 4_RELATORIO ao fim do relatorio R2 (sha256 de cada arquivo)",
       "quando_local": time.strftime("%Y-%m-%d %H:%M:%S"), "arquivos": []}
for dp, dn, fn in os.walk(BASE):
    dn.sort()
    for f in sorted(fn):
        if f == NOME:
            continue
        p = os.path.join(dp, f)
        b = open(LONG + p, "rb").read()
        man["arquivos"].append({"rel": os.path.relpath(p, BASE).replace("\\", "/"), "bytes": len(b),
                                "sha256": hashlib.sha256(b).hexdigest()})
man["n_arquivos"] = len(man["arquivos"])
out = os.path.join(BASE, NOME)
with open(out + ".tmp", "wb") as fo:
    fo.write(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
os.replace(out + ".tmp", out)
sys.stdout.reconfigure(encoding="utf-8")
print("n_arquivos", man["n_arquivos"])
for a in man["arquivos"]:
    if "/" not in a["rel"] or a["rel"].startswith("R2/saidas") or a["rel"].startswith("R1_preservado"):
        print(a["rel"], a["bytes"], a["sha256"][:16])
