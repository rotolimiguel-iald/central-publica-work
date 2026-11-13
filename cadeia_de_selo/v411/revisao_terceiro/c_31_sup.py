import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
j = json.load(open(V + r"\pos_rito\HARNESS_TEXTOS_ENSAIO_v411.json", encoding="utf-8"))
s = j["etapas"]["superficies"]
def show(o, pre="", d=0):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)) and d < 2:
                print(pre + str(k) + ":"); show(v, pre + "  ", d + 1)
            else:
                print(pre + str(k) + ": " + json.dumps(v, ensure_ascii=False)[:160])
    elif isinstance(o, list):
        for v in o[:6]:
            print(pre + "-", json.dumps(v, ensure_ascii=False)[:200])
show(s)
