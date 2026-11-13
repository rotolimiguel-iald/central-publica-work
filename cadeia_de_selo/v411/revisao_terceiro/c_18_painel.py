import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
T = json.load(open(V + r"\TOPO_RATIFICADO_v411.json", encoding="utf-8"))
print(T["painel_readme_pt"]); print(); print(T["painel_readme_en"]); print(); print(T["regras"])
