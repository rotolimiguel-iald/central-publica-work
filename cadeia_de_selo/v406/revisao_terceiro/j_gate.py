# -*- coding: utf-8 -*-
"""Revisor terceiro v406: o gate e as chaves intocadas no core do ensaio a seco == core da base v405 (hash canonico por chave); o que mudou no core."""
import hashlib, json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
b = json.load(open(R + "base_v405/um_absoluto.json", encoding="utf-8"))["core"]
d = json.load(open(R + "dry_v406/core_ensaio.json", encoding="utf-8"))["core"]
H = lambda o: hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]
for k in ("qg_closure", "neutrino_mass", "ramo_b_preregistration_v386", "ledger_errata_v386", "ga_mass_audit", "joint_coincidence_result_v3", "witness_rigidity", "beta", "alpha"):
    print("%-30s %s %s %s" % (k, "IGUAL " if H(b[k]) == H(d[k]) else "DIFERE", H(b[k]), H(d[k])))
def dif(a, c, p=""):
    out = []
    if isinstance(a, dict) and isinstance(c, dict):
        for k in set(a) | set(c):
            if k not in a or k not in c: out.append(p + "/" + k + " (so' em um)")
            else: out += dif(a[k], c[k], p + "/" + k)
    elif a != c: out.append(p)
    return out
print("witness_layers difere em:", dif(b["witness_layers"], d["witness_layers"]))
print("qg_closure difere em:", dif(b["qg_closure"], d["qg_closure"]))
print("chaves novas:", sorted(set(d) - set(b)), "| sumidas:", sorted(set(b) - set(d)))
print("chaves mudadas (%d):" % len([k for k in b if k in d and H(b[k]) != H(d[k])]), [k for k in b if k in d and H(b[k]) != H(d[k])])
