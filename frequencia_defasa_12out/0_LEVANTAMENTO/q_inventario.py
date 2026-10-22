# -*- coding: utf-8 -*-
# Consulta (somente leitura) o inventario da bancada (INVENTARIO_BANCADA_CHATGPT.json) por regex nas declaracoes,
# e marca se o arquivo tambem existe no kernel do Nos (por nome de arquivo e sha16).
import json, re, sys, os, hashlib
AQUI = os.path.dirname(os.path.abspath(__file__))
INV = "C:\\IALD\\Central de Patentes\\memory\\INVENTARIO_BANCADA_CHATGPT.json"
with open(INV, "rb") as fh:
    b = fh.read()
inv = json.loads(b.decode("utf-8"))
kidx = json.load(open(os.path.join(AQUI, "KERNEL_INDICE.json"), encoding="utf-8"))
k_by_name = {}
for rel, meta in kidx["arquivos"].items():
    k_by_name.setdefault(os.path.basename(rel), []).append((rel, meta["sha16"]))
pat = re.compile(sys.argv[1], re.I)
temas = sys.argv[2] if len(sys.argv) > 2 else None
hits = []
for u in inv["unicos"]:
    ds = [d for d in u.get("decls", []) if pat.search(d)]
    if not ds:
        continue
    if temas and not any(re.search(temas, t, re.I) for t in u.get("temas", [])):
        continue
    nos = k_by_name.get(os.path.basename(u["arquivo"].replace("\\", "/")), [])
    same = [r for r, s in nos if s == u["sha16"]]
    hits.append({"arquivo": u["arquivo"], "sha16": u["sha16"], "temas": u.get("temas"), "mtime": u.get("mtime"),
                 "no_kernel_nos": bool(nos), "mesmo_sha_no_nos": bool(same), "decls": ds[:12], "n": len(ds)})
print("inventario sha16", hashlib.sha256(b).hexdigest()[:16], "gerado_em", inv.get("gerado_em"), "| hits", len(hits))
for h in hits:
    print(f'- {h["arquivo"]} [{h["sha16"]}] mtime {h["mtime"]} nos={h["no_kernel_nos"]} mesmo_sha={h["mesmo_sha_no_nos"]} temas={h["temas"]}')
    for d in h["decls"]:
        print("     ", d[:160])
