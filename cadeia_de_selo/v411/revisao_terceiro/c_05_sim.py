import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
j = json.load(open(V + r"\SIMULACAO_ARVORE_NOS_21e87eb3df5098f8.json", encoding="utf-8"))
for k, v in j.items():
    print(k, json.dumps(v, ensure_ascii=False)[:260])
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
print("h8_entradas", E["h8_entradas"], "residuais", E["h8_residuais_do_nos"])
