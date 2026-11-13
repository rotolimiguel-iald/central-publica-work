from b_lib import *
import re
texts = {"pt": pt(), "en": en(), "md": md(), "man": man(), "out": out()}
pats = ["O que a natureza decide", "What nature decides", "Lido com o acervo", "Read with the whole record", "Lê-se com o acervo", "It is read with the whole record", "5σ", "Cefeidas livres", "free Cepheids", "0 falsificada", "nenhuma foi falsificada","none was falsified","none falsified"]
for n,tx in texts.items():
    for p in pats:
        ms = [m.start() for m in re.finditer(re.escape(p), tx)]
        if ms: print(n, repr(p), len(ms), ms[:15])
print("=== MD head")
m = md()
print(m[:2500])
print("=== MD at 20324")
print(m[20100:23500])
