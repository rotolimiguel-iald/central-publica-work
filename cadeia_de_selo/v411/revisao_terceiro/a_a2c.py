import json, os, hashlib, base64
import a_lib
f = a_lib.Fonte(a_lib.CAND, "cand")
ns = f.carregar(["_V411_H0DN_CONTRACT", "_V411_H0DN_INSUMOS", "_V410_H0DN_INSUMOS"])
C, INS, INS10 = ns["_V411_H0DN_CONTRACT"], ns["_V411_H0DN_INSUMOS"], ns["_V410_H0DN_INSUMOS"]
res = json.load(open(os.path.join(a_lib.OUT, "a2_blobs.json"), encoding="utf-8"))
W = r"C:\IALD\Central de Patentes\work"
sha = lambda b: hashlib.sha256(b).hexdigest()
print("todos blob==origem:", all(v["blob_eq_origem"] for v in res.values()), "| todos contrato_eq:", all(v["contrato_eq"] for v in res.values()), "| n", len(res))
pinos = json.load(open(os.path.join(W, r"h0dn_bg1_v411_emenda_11nov\producao\PINOS_DE_PRODUCAO.json"), encoding="utf-8"))
sh_blob = {k: v["sha_blob"] for k, v in res.items()}
ok = {}
for campo, nome in C["pinos_por_campo"].items():
    ok[campo] = (pinos[campo]["sha256"] == sh_blob[nome], nome)
for arq in C["ordem_dos_modulos"]:
    ok["codigo:" + arq] = (pinos["codigo"][arq] == sh_blob[arq], arq)
print("pinos x blobs:", {k: v[0] for k, v in ok.items()})
print("executor (so texto):", C["executor"], "| pino:", pinos["codigo"].get("executar_abertura_v411.py", "")[:16])
for c in C["citados"]:
    p = os.path.join(W, c["rel"])
    print("citado", c["nome"], os.path.exists(p) and sha(open(p, "rb").read()) == c["sha256"] and os.path.getsize(p) == c["bytes"])
# caminhos sob kimi no contrato / insumos
ctxt = json.dumps(C, ensure_ascii=False).lower()
print("kimi no contrato:", [m for m in ("\kimi\\", "/kimi/", "kimi\\\\") if m in ctxt], "| pasta_vedada:", C["pasta_vedada"])
rels = [v["rel"] for v in C["insumos"].values()] + [c["rel"] for c in C["citados"]]
print("rel com kimi:", [r for r in rels if "kimi" in r.lower()])
# manifesto
m = json.load(open(os.path.join(a_lib.V, "MANIFESTO_INSUMOS_v411.json"), encoding="utf-8"))
print("manifesto chaves:", list(m.keys())[:14])
mt = json.dumps(m, ensure_ascii=False).lower()
print("kimi\ no manifesto:", "kimi\\\\" in mt or "/kimi/" in mt, "| ocorrencias da palavra kimi:", mt.count("kimi"))
