import hashlib, json, os, sys, time
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
def sha16(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1<<20), b""):
            h.update(b)
    return h.hexdigest()[:16]
c = os.path.join(V, "um_v411_candidato.py")
r = {"quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "candidato_sha16_no_inicio": sha16(c), "candidato_bytes": os.path.getsize(c),
     "bak_sha16": sha16(c + ".bak_20261112_195053")}
print(r)
out = os.path.join(V, "revisao_terceiro", "ESTADO_REVISAO_v411.CU.json")
json.dump({"inicio": r, "itens": {}}, open(out, "w", encoding="utf-8"), indent=1)
for k in ("A","B","C"):
    d = json.load(open(os.path.join(V,"revisao_terceiro","REVISAO_TERCEIRO_v411.R1.%s.json"%k), encoding="utf-8"))
    print(k, list(d.keys()))
    for a in d["achados"]:
        print(" ", a.get("id"), a.get("sev"), "|", str(a.get("onde"))[:100])
