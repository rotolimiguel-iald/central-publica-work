# -*- coding: utf-8 -*-
"""beta = alpha*ONE*sqrt(e) em runtime; alpha lido nos BYTES do um.py (nao executado). Estatuto: [DERIVED]."""
import hashlib, json, math, os, re, sys, time
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
PR = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.json"
b = open(UM, "rb").read()
lines = b.split(b"\n")
l5557 = lines[5556].decode("utf-8", "replace").rstrip("\r")
l95 = lines[94].decode("utf-8", "replace").rstrip("\r")
m1 = re.match(r"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l5557)
m2 = re.match(r"^SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", l95)
alpha = float(m1.group(1))
ONE = 1.0
beta = alpha * ONE * math.sqrt(math.e)
pr = json.load(open(PR, encoding="utf-8"))


def find_beta(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "beta_runtime" and isinstance(v, float):
                return v
            r = find_beta(v)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_beta(v)
            if r is not None:
                return r
    return None


conf = find_beta(pr)
out = {"estatuto": "[DERIVED: alpha lido nos bytes do um.py (l.5557 embutida; l.95 topo) e beta calculado em runtime; nao e medida]",
       "um_py": UM, "um_py_sha256": hashlib.sha256(b).hexdigest(), "um_py_bytes": len(b), "executado": False,
       "l5557": l5557, "l95": l95, "literal_5557": m1.group(1), "literal_95": m2.group(1),
       "literais_iguais": m1.group(1) == m2.group(1),
       "alpha": alpha, "sqrt_e": math.sqrt(math.e), "beta_runtime": beta, "beta_hex": beta.hex(),
       "beta_conferencia_lida_do_PREREGISTRO": conf, "dif_abs": (abs(beta - conf) if conf is not None else None),
       "quando_local": time.strftime("%Y-%m-%d %H:%M:%S")}
outp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "BETA_RUNTIME_RELATORIO_R2.json")
with open(outp + ".tmp", "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
os.replace(outp + ".tmp", outp)
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
