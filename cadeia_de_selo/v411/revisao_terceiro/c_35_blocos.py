import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
H = r"C:\t\k411c\ensaio_topo_proposto\pos_rito_textos\positivo\nos\HANDOFF_v411_CUSTODIA.md"
h = rd(H)
blocos = [b for b in re.split(r"\n\s*\n", h) if b.strip()]
for i in (9, 10, 25):
    print("=== bloco", i, len(blocos[i]), "B"); print(blocos[i][:1500]); print()
