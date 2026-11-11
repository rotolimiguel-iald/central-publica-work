import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar(); REG = todos_registros(C)
for nome, t in (("md", ws(C["md"])), ("pt", C["pt"]), ("en", C["en"]), ("custodia", C["custodia_ws"])):
    ms = list(re.finditer(r"INPUT/dicionário a leitura do operador|INPUT/dictionary the operator|a leitura do operador\]|the operator[’']s reading\]", t))
    print("==", nome, len(ms))
    for m in ms[:4]: print("    ", ctx(t, m, 170))
n, on = achar_em_folhas(REG, r"INPUT/dicionario a leitura do operador|INPUT/dicionário a leitura do operador|a leitura do operador \(que esse limiar", 0, 170); print("== reg", n)
for p, c in on: print("   ", p, "::", c[:420])
