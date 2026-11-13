import json, os, hashlib, base64, subprocess, sys
import a_lib
f = a_lib.Fonte(a_lib.CAND, "cand")
assert f.trecho("h0dn_bg1_v411").startswith("def h0dn_bg1_v411"), "indice desalinhado"
ns = f.carregar(["_V411_H0DN_CONTRACT", "_V411_H0DN_INSUMOS", "_V410_H0DN_INSUMOS", "_V410_H0DN_CONTRACT"])
C = ns["_V411_H0DN_CONTRACT"]; INS = ns["_V411_H0DN_INSUMOS"]; INS10 = ns["_V410_H0DN_INSUMOS"]
print("contrato chaves:", list(C.keys()))
print("insumos no contrato:", list(C["insumos"].keys()))
print("embutidos:", {k: (("reuso:" + v["reuso_v410"]) if "reuso_v410" in v else len(v.get("b64", ""))) for k, v in INS.items()})
print("citados:", C["citados"] if not isinstance(C["citados"], dict) else list(C["citados"].keys()))
sha = lambda b: hashlib.sha256(b).hexdigest()
W = r"C:\IALD\Central de Patentes\work"
pinos_arq = json.load(open(os.path.join(W, r"h0dn_bg1_v411_emenda_11nov\producao\PINOS_DE_PRODUCAO.json"), encoding="utf-8"))
res = {}
for nome, pino in C["insumos"].items():
    ent = INS.get(nome)
    if isinstance(ent, dict) and "reuso_v410" in ent:
        ent = INS10.get(ent["reuso_v410"]); tipo = "reuso"
    else:
        tipo = "novo"
    b = base64.b64decode(ent["b64"].encode("ascii"), validate=True)
    origem = os.path.join(W, pino["rel"])
    ob = open(origem, "rb").read()
    res[nome] = {"tipo": tipo, "bytes": len(b), "sha_blob": sha(b), "sha_origem": sha(ob), "blob_eq_origem": b == ob, "sha_no_contrato": pino["sha256"], "contrato_eq": sha(b) == pino["sha256"] and len(b) == pino["bytes"], "rel": pino["rel"]}
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "rel"} for k, v in res.items()}, indent=0)[:6000])
json.dump(res, open(os.path.join(a_lib.OUT, "a2_blobs.json"), "w", encoding="utf-8"), indent=1)
