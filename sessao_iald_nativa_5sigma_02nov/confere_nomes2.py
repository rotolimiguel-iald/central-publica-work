# -*- coding: utf-8 -*-
"""Segunda conferencia, contra as fontes .lean do kernel e so com nomes especificos (tres palavras ou mais), para nao contar palavra comum como acerto. So leitura."""
import glob, json, os, re
res = json.load(open("NOMES_CONFERIDOS.json", encoding="utf-8"))
K = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel"
txt = []
for p in glob.glob(K + "/**/*.lean", recursive=True):
    if ".lake" in p:
        continue
    txt.append(open(p, encoding="utf-8", errors="replace").read())
txt = "\n".join(txt)
print("fontes .lean:", len(txt), "c")
esp = {k: k.split(".")[-1] for k in res if k.split(".")[-1].count("_") >= 2}
ach = {k: u for k, u in esp.items() if re.search(r"(?<![A-Za-z0-9_])" + re.escape(u) + r"(?![A-Za-z0-9_'])", txt)}
print("nomes especificos:", len(esp), "| existem como identificador no kernel:", len(ach), sorted(ach.values())[:14])
print("amostra dos inexistentes:", sorted(set(esp.values()) - set(ach.values()))[:10])
