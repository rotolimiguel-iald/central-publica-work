import sys, re
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar()
def show(nome, texto, rx, n=110, k=2):
    ms = list(re.finditer(rx, texto))
    print("[%s] /%s/ -> %d" % (nome, rx, len(ms)))
    for m in ms[:k]: print("     ...", ctx(texto, m, n))
for nome in ("pt", "en"):
    show(nome, C[nome], r"e\^\(?-s")
    show(nome, C[nome], r"e\^-s")
    show(nome, C[nome], r"c\(x\)\)")
show("pt", C["pt"], r"havendo pixel de custo zero")
show("en", C["en"], r"given a zero-cost pixel")
show("pt", C["pt"], r"a dissipação sustenta a nota, e a nota é a conjugação modular")
show("pt", C["pt"], r"o limiar do Tetelestai \(")
show("pt", C["pt"], r"limiar de um pixel, a decisão exata")
show("en", C["en"], r"one-pixel threshold, the exact decision")
show("pt", C["pt"], r"no kernel\.\);")
show("pt", C["pt"], r"o fundo pesa um pixel")
show("pt", C["pt"], r"um pixel de custo 1 brilha")
