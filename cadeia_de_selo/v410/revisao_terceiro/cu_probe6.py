import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar(); REG = todos_registros(C)
R_ = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
PL = ws(rd(R_ + "PLANO_v410.md"))
alv = {"pt": C["pt"], "en": C["en"], "md": ws(C["md"]), "custodia": C["custodia_ws"], "plano": PL}
for k, t in alv.items():
    ms = list(re.finditer(r"62[,.]5", t))
    print("==", k, len(ms))
    for m in ms[:4]: print("     ", ctx(t, m, 160))
n, on = achar_em_folhas(REG, r"62[,.]5", 0, 150); print("== reg", n)
for p, c in on: print("    ", p, "::", c[:330])
