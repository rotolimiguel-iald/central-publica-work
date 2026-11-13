from b_lib import *
import re
texts = {"pt": pt(), "en": en(), "md": md(), "man": man(), "out": out()}
pats = ["Dois resultados abrem", "Two results open", "H0DN × BG1 ABERTO", "Hubble-ratio test", "painel", "provado na natureza", "proved in nature", "6,11", "6.11"]
for n,tx in texts.items():
    for p in pats:
        ms = [m.start() for m in re.finditer(re.escape(p), tx)]
        print(n, repr(p), len(ms), ms[:12])
