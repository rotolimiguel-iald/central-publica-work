from b_lib import *
import re
H = json.loads(rd(V + r"\pos_rito\HARNESS_TEXTOS_ENSAIO_v411.json"))
print(list(H.keys())[:30])
S = rd(V + r"\pos_rito\HARNESS_TEXTOS_ENSAIO_v411.json")
for pat in ["H0DN × BG1 (pré-registrado", "Hubble-ratio test", "O que a natureza decide", "What nature decides", "provado na natureza a", "proved in nature at"]:
    ms = [m.start() for m in re.finditer(re.escape(pat), S)]
    print(pat, len(ms), ms[:4])
