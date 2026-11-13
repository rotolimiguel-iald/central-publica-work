import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
h = rd(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_textos\positivo\nos\HANDOFF_v411_CUSTODIA.md")
for n in ("README_H0DN_v411", "README_H0DN_EN_v411"):
    m = re.search(r"<!-- INICIO_%s -->(.*?)<!-- FIM_%s -->" % (n, n), h, re.S)
    print(n, "->", m.group(1).strip()[:400])
