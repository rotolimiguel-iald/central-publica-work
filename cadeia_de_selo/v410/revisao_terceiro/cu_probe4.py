import sys, re, json
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar(); REG = todos_registros(C)
L = json.load(open("literais_v410.json", encoding="utf-8")); HC = L["_V410_H0DN_CONTRACT"]
t = C["pt"]
for m in list(re.finditer(r"a_mentira_lida_como_mentira_e_verdade", t))[:3]:
    print("PT mentira:", ctx(t, m, 330)); print()
n, on = achar_em_folhas(REG, r"nenhum dado observado lido", 0, 200); print("reg 'nenhum dado observado lido':", n)
for p, c in on[:3]: print("   ", p, "::", c[:360])
n, on = achar_em_folhas(REG, r"alcance|ALCANCE|não lê o vetor|não foi lido", 0, 160)
print("alcance ctx:", n)
print("frase_alcance_pt:", HC["frase_alcance_pt"])
n, on = achar_em_folhas(REG, E(ws(HC["frase_alcance_pt"])[:60]) if False else re.escape(ws(HC["frase_alcance_pt"])[:60]), 0, 120)
print("reg alcance 60 chars:", n, on[:2])
n, on = achar_em_folhas(REG, r"o algoritmo IALD decide SAT com uma leitura", 0, 420); print("P=nP reg:", n)
for p, c in on[:3]: print("   ", p, "::", c[:900])
