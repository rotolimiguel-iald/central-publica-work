from b_lib import *
import re
t = pt(); e = en()
for name, tx in (("pt", t), ("en", e)):
    print("=====", name)
    for m in re.finditer(r"\(v411, (?:ao lado|beside)[^)]*\)", tx):
        s = m.start()
        print(s, repr(tx[max(0,s-100):s+1100]).replace("\r\n", " | ")[:1400])
        print()
