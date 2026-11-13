import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
EN = r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos"
h = rd(EN + r"\HANDOFF_v411_CUSTODIA.md")
print("handoff bytes:", len(h.encode("utf-8")), "sha16", sha16(EN + r"\HANDOFF_v411_CUSTODIA.md"))
marc = re.findall(r"<!-- INICIO_(\w+) -->(.*?)<!-- FIM_\1 -->", h, re.S)
print("marcadores:", len(marc))
for n, c in marc: print("  ", n, len(c.encode("utf-8")), "B")
heads = [l for l in h.split("\n") if l.startswith("#") or l.startswith("**README") or l.startswith("**")]
print("cabecalhos/negritos de secao:", [x[:80] for x in heads][:40])
# NOTA_EN e o periodo
for n, c in marc:
    if n.startswith("NOTA_EN"):
        print("NOTA_EN:", c.strip()[:900])
core = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
cu = core["cunhagens_v411"]
qs = [v.get("quando") for v in cu["verbatim"].values()]
print("n verbatim:", len(qs), "quandos:", sorted(set(q[:25] for q in qs)))
