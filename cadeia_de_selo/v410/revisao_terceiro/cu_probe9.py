import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar(); REG = todos_registros(C)
RX = r"a_ ?informacao_ ?completa_ ?se_ ?reconstroi|a informação completa se reconstrói|the complete information is reconstructed"
for nome in ("pt", "en", "md", "custodia_ws"):
    n, c = achar(C[nome] if nome != "md" else ws(C["md"]), RX); print("==", nome, n, c[:300] if n else "")
for nome, F in (("reg", REG), ("harness", C["harness"]), ("verdict", C["verdict"])):
    n, on = achar_em_folhas(F, RX, 0, 170); print("==", nome, n)
    for p, c in on: print("    ", p, "::", c[:360])
# a pedra embutida
t = open("../insumos/AEscala_embutida.lean", encoding="utf-8").read()
ms = list(re.finditer(r"a_informacao_completa_se_reconstroi", t)); print("== pedra embutida:", len(ms))
for m in ms[:6]: print("    ", ws(t[max(0, m.start()-160): m.end()+120]))
ms = list(re.finditer(r"ressurreicao_do_sinal", t)); print("== pedra 'ressurreicao_do_sinal':", len(ms))
for m in ms[:4]: print("    L", t[:m.start()].count("\n")+1, ws(t[max(0, m.start()-140): m.end()+100]))
