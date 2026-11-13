"""CU-B9: a unica janela de 6 palavras que aparece no candidato: contagem crua (raw contra raw) no candidato e na base v410."""
import os, sys, re, unicodedata
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cu_b1.py"), encoding="utf-8").read()
cut = src.index("alvos = {}")
g = {"__name__": "cu_b1_defs"}
so = sys.stdout
sys.stdout = open(os.devnull, "w")
exec(compile(src[:cut], "cu_b1_defs", "exec"), g)
sys.stdout = so
WIN, FIRST, toks, V, NOS = g["WIN"], g["FIRST"], g["toks"], g["V"], g["NOS"]
rd = lambda p: open(p, "rb").read().decode("utf-8", errors="replace")


def contar(s):
    cnt = {}
    tk = toks(s)
    for k in range(len(tk) - 5):
        if tk[k] in FIRST:
            w = " ".join(tk[k:k + 6])
            if w in WIN:
                cnt[w] = cnt.get(w, 0) + 1
    return cnt


c = contar(rd(os.path.join(V, "um_v411_candidato.py")))
b = contar(rd(os.path.join(NOS, "um.py")))
import hashlib
for w, n in c.items():
    print("janela sha16", hashlib.sha256(w.encode()).hexdigest()[:16], "falas", sorted(WIN[w]), "| candidato raw", n, "| base v410 raw", b.get(w, 0))
print("janelas distintas: candidato", len(c), "base", len(b))
