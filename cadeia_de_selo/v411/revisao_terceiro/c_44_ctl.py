import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
j = json.load(open(V + r"\pos_rito\HARNESS_TEXTOS_ENSAIO_v411.json", encoding="utf-8"))
cs = j["etapas"]["leitura_negativos"]["controles"]
for k in ("external_ladder", "do core", "autor", "p2_ao_lado"):
    print(k, [c["controle"][:110] for c in cs if k.lower() in c["controle"].lower()][:6])
