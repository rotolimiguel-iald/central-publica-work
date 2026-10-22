# -*- coding: utf-8 -*-
"""Lê (só leitura) o core um_absoluto.json v386 e extrai as chaves ligadas a BBN/CMB/N_eff/D1/bancada. Escreve só na lente."""
import json, hashlib, os, sys
OUT = os.path.dirname(os.path.abspath(__file__))
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
P = os.path.join(NOS, "um_absoluto.json")
b = open(P, "rb").read()
print("core bytes", len(b), "sha16", hashlib.sha256(b).hexdigest()[:16])
d = json.loads(b.decode("utf-8"))
print("top-level keys", len(d))
pat = ("evidence_audit", "d1_", "bancada_fases", "neff", "rho_plus_p", "bbn", "cmb", "nivel2", "juiz", "planck", "version", "ledger", "cobranc")
want = [k for k in d if any(s in k.lower() for s in pat)]
print("matching keys:", want)
sel = {k: d[k] for k in want}
json.dump(sel, open(os.path.join(OUT, "core_v386_sel.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k in want:
    v = d[k]
    if isinstance(v, dict):
        vd = v.get("verdict") or v.get("veredito")
        vals = v.get("values")
        print("\n##", k, "| verdict:", vd)
        if isinstance(vals, dict):
            small = {kk: vv for kk, vv in vals.items() if isinstance(vv, (int, float, str, bool)) or vv is None}
            print("   values:", json.dumps(small, ensure_ascii=False)[:900])
    else:
        print("\n##", k, "=", str(v)[:300])

# diff dos dois 13_nivel2_resultado.json (original vs cópia do Nós)
a = json.load(open(r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_resultado.json", encoding="utf-8"))
c = json.load(open(os.path.join(NOS, "nivel2_mcmc", "13_nivel2_resultado.json"), encoding="utf-8"))
def flat(o, p=""):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(flat(v, p + "/" + k))
    else:
        out[p] = o
    return out
fa, fc = flat(a), flat(c)
diff = {k: (fa.get(k), fc.get(k)) for k in set(fa) | set(fc) if fa.get(k) != fc.get(k)}
print("\n## diff 13_nivel2_resultado.json original vs Nós:", json.dumps(diff, ensure_ascii=False)[:1500])
