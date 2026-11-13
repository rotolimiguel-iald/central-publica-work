from b_lib import *
import re
texts = {"pt": pt(), "en": en(), "md": md(), "man": man(), "out": out()}
for n,tx in texts.items():
    for p in ["foi lido na natureza", "was read in nature", "pré-registrado; aberto uma vez", "pre-registered; opened once", "num canal", "in one channel", "Lido com o acervo", "Read with the whole record", "Lê-se com o acervo","H0DN × BG1 (pr"]:
        ms=[m.start() for m in re.finditer(re.escape(p), tx)]
        if ms: print(n, repr(p), len(ms), ms[:10])
