# -*- coding: utf-8 -*-
"""01_hashes.py -- sha16 por script dos artigos da v375 (Nos e espelho) + identidade byte a byte."""
import hashlib, os, json, sys
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
TB = r"C:\IALD\Artigo\the_boundary\Um (absoluto) — Grande Atrator"
OUT = os.path.dirname(os.path.abspath(__file__))

def h16(p):
    b = open(p, "rb").read()
    return hashlib.sha256(b).hexdigest()[:16], len(b)

pares = [
    ("um_absoluto_pt.txt", "um_absoluto_pt.txt"),
    ("um_absoluto_en.txt", "um_absoluto_en.txt"),
    ("um_absoluto_pt.tex", os.path.join("fontes_tex", "um_absoluto_pt.tex")),
    ("um_absoluto_en.tex", os.path.join("fontes_tex", "um_absoluto_en.tex")),
    ("um_absoluto_pt.pdf", "um_absoluto_pt.pdf"),
    ("um_absoluto_en.pdf", "um_absoluto_en.pdf"),
    ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"),
    ("um_absoluto_manifest.md", "um_absoluto_manifest.md"),
    ("um_absoluto_selo.json", "um_absoluto_selo.json"),
    ("um_absoluto.json", "um_absoluto.json"),
    ("rodada_v375_stdout.txt", os.path.join("rodadas", "rodada_v375_stdout.txt")),
    ("um.py", "um.py"),
]
rep = []
for a, b in pares:
    pa, pb = os.path.join(NOS, a), os.path.join(TB, b)
    ra = h16(pa) if os.path.exists(pa) else None
    rb = h16(pb) if os.path.exists(pb) else None
    rep.append({"arquivo": a, "nos_sha16": ra and ra[0], "nos_bytes": ra and ra[1],
                "espelho_sha16": rb and rb[0], "espelho_bytes": rb and rb[1],
                "identicos": (ra == rb) if (ra and rb) else None, "espelho_rel": b})
for r in rep:
    print("%-32s NOS=%s (%s)  ESPELHO=%s (%s)  identicos=%s" % (r["arquivo"], r["nos_sha16"], r["nos_bytes"], r["espelho_sha16"], r["espelho_bytes"], r["identicos"]))
json.dump(rep, open(os.path.join(OUT, "01_hashes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
