import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
j = json.load(open(V + r"\pos_rito\HARNESS_TEXTOS_ENSAIO_v411.json", encoding="utf-8"))
cs = j["etapas"]["leitura_negativos"]["controles"]
print([c["controle"][:120] for c in cs if "h0dn_bg1_v411" in c["controle"] and "selo" in c["controle"].lower()])
