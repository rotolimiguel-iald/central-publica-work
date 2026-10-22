# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
for l in ("pt", "en"):
    t = open(os.path.join(NOS, "um_absoluto_%s.toc" % l), encoding="utf-8", errors="replace").read()
    ents = re.findall(r"\\contentsline \{(\w+)\}\{(.*?)\}\{(\d+)\}", t)
    print("==", l, len(ents))
    for k, (lev, tit, pg) in enumerate(ents):
        print(" %3d %-10s %4s %s" % (k, lev, pg, tit[:170]))
