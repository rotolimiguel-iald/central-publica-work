from b_lib import *
import re
C = core()["core"]
e = C["estatuto_da_prova_v391"]
print(list(e.keys()))
print(json.dumps(e["prova_2_ritos"], ensure_ascii=False)[:300])
for k in C:
    if "stress" in k.lower() or "tres_testes" in k.lower(): print("KEY", k, list(C[k].keys())[:25] if isinstance(C[k], dict) else "")
