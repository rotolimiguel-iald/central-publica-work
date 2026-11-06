import json, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
d = json.load(open(R + "PINO_RECIBO_PRE_SELO_v409.json", encoding="utf-8"))
print(json.dumps(d["adendo_de_pino_do_t12"], ensure_ascii=False, indent=1)[:1800])
print("Nos um.py sha256 hoje:", hashlib.sha256(open("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/um.py", "rb").read()).hexdigest())
s = json.load(open(R + "SESSION_REFERENCE_prep_v409.json", encoding="utf-8"))
print({k: (v if not isinstance(v, (dict, list)) else str(v)[:200]) for k, v in s.items()})
