# -*- coding: utf-8 -*-
# Auditor REPRO: ao fim, as pastas do construtor e do pre-registrador continuam com os MESMOS arquivos e bytes que o
# auditor mediu no inicio (saidas/A1_FREEZE.json); nenhum __pycache__ novo; tamanho da pasta do auditor.
import os, json, hashlib
AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "C:\\IALD\\Central de Patentes\\work\\frequencia_defasa_12out\\"
A1 = json.load(open(os.path.join(AUD, "saidas", "A1_FREEZE.json"), encoding="utf-8"))
out = {"diferencas": [], "pycache": []}
for nome in ("2_OPTICO", "3_KERNEL"):
    antes = {x["arq"]: x["sha256"] for x in A1[nome]["arquivos"]}
    agora = {}
    for dp, dns, fns in os.walk(W + nome):
        for d in dns:
            if d == "__pycache__":
                out["pycache"].append(os.path.join(dp, d))
        for f in fns:
            p = os.path.join(dp, f)
            agora[os.path.relpath(p, W + nome).replace("\\", "/")] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if antes != agora:
        out["diferencas"].append([nome, sorted(set(antes) ^ set(agora)), [k for k in antes if k in agora and antes[k] != agora[k]]])
    out[nome] = len(agora)
fz = json.load(open(W + "1_PREREGISTRO\\FREEZE.json", encoding="utf-8"))
for rel, (n, s) in fz["demais_arquivos_da_pasta"].items():
    b = open(W + "1_PREREGISTRO\\" + rel.replace("/", "\\"), "rb").read()
    if (len(b), hashlib.sha256(b).hexdigest()) != (n, s):
        out["diferencas"].append(["1_PREREGISTRO", rel])
for k in ("PREREGISTRO.json", "PREREGISTRO.md"):
    b = open(W + "1_PREREGISTRO\\" + k, "rb").read()
    if hashlib.sha256(b).hexdigest() != fz[k]["sha256"]:
        out["diferencas"].append(["1_PREREGISTRO", k])
for dp, dns, fns in os.walk(W + "1_PREREGISTRO"):
    for d in dns:
        if d == "__pycache__":
            out["pycache"].append(os.path.join(dp, d))
out["n_1_PREREGISTRO"] = sum(len(f) for _, _, f in os.walk(W + "1_PREREGISTRO"))
tot = 0
nf = 0
for dp, dns, fns in os.walk("\\\\?\\" + AUD):
    for f in fns:
        tot += os.path.getsize(os.path.join(dp, f))
        nf += 1
out["pasta_auditor"] = {"arquivos": nf, "bytes": tot}
out["mapa_de_rotas_pycache"] = os.path.isdir("C:\\IALD\\MAPA_DE_ROTAS\\__pycache__")
out["veredito"] = "INTOCADOS" if not out["diferencas"] and not out["pycache"] else "ALTERADOS"
open(os.path.join(AUD, "saidas", "D_INTOCADOS.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
