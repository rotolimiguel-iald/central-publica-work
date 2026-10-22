"""Manifesto da pasta 4_RELATORIO_R2: sha256 e bytes de cada arquivo (gerado por ultimo; o proprio manifesto fica fora)."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\4_RELATORIO_R2"
OUT = os.path.join(W, "MANIFESTO_4_RELATORIO_R2.json")
itens = []
for dp, dn, fn in os.walk(W):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        if p == OUT:
            continue
        b = open(p, "rb").read()
        itens.append({"caminho": os.path.relpath(p, W).replace("\\", "/"), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
json.dump({"pasta": W, "gerado_em": time.strftime("%Y-%m-%dT%H:%M:%S"), "n_arquivos": len(itens), "arquivos": itens},
          open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for i in itens:
    print("%-60s %s %d" % (i["caminho"], i["sha256"][:16], i["bytes"]))
