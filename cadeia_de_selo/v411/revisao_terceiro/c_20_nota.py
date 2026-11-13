import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
EN = r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos"
h = rd(EN + r"\HANDOFF_v411_CUSTODIA.md")
m = re.search(r"<!-- INICIO_NOTA_EN_v411 -->(.*?)<!-- FIM_NOTA_EN_v411 -->", h, re.S)
print(m.group(1)[880:])
core = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
print("livro:", {k: v for k, v in (core["estatuto_da_prova_v391"].get("prova_2_ritos") or {}).items() if not isinstance(v, (list, dict))})
