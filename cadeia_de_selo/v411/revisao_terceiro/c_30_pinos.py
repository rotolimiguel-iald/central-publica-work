import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
Pn = json.load(open(V + r"\PINOS_BN_v411.json", encoding="utf-8"))
print("chaves:", list(Pn))
need = "criterios esboco_R3_5 gerador_bateria driver_t12_t14 bateria_base_R2 kernel_recibo candidato esperados pins_do_candidato recibo_pre_selo selo_anterior_v410 kernel_manifesto_anterior_v410".split()
for k in need:
    d = Pn.get(k)
    if not d: print("FALTA pino", k); continue
    p = d["path"]; ok = os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == d["sha256"]
    print(("ok  " if ok else "DIVERGE"), k, p[-70:])
print("tem cadeia_de_selos:", "cadeia_de_selos" in Pn)
