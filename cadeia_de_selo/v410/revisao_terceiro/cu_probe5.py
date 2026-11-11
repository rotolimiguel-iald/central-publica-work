import sys, re, json
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar(); REG = todos_registros(C)
L = json.load(open("literais_v410.json", encoding="utf-8")); HC = L["_V410_H0DN_CONTRACT"]
for rx in (r"o executor montou esse vetor", r"não lê vetor observado", r"nenhum Z, razão ou veredito"):
    n, on = achar_em_folhas(REG, rx, 0, 200); print("reg", rx, n, [o[0] for o in on[:3]])
    for a in ("pt", "en", "md", "custodia_ws"): print("   ", a, achar(C[a], rx)[0])
print()
# registro H0DN: onde esta' a frase do alcance (o 'diz')
H = [x for x in REG if x[0].startswith("h0dn_bg1_v410")]
for p, t in H:
    if "alcance" in t.lower() or "vetor observado" in t: print(p, "::", t[:230])
