# -*- coding: utf-8 -*-
"""Varre o core v386 (só leitura) por chaves aninhadas ligadas a BBN/CMB/N_eff/D1/bancada; grava a seleção na lente."""
import json, os
OUT = os.path.dirname(os.path.abspath(__file__))
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.load(open(P, encoding="utf-8"))
print("top-level:", list(d.keys()))
pat = ("evidence_audit", "d1_camb", "bancada_fases", "neff", "rho_plus_p", "bbn", "nivel2", "juiz_la", "fase1", "fase8", "ledger_of_charges", "livro")
hits = {}
def walk(o, path, depth):
    if depth > 4:
        return
    if isinstance(o, dict):
        for k, v in o.items():
            kl = k.lower()
            if any(s in kl for s in pat):
                hits[path + "/" + k] = v
            walk(v, path + "/" + k, depth + 1)
walk(d, "", 0)
print("n hits:", len(hits))
sel = {}
for k, v in hits.items():
    if isinstance(v, dict):
        vd = v.get("verdict") or v.get("veredito") or v.get("status")
        vals = v.get("values")
        print("\n##", k, "| verdict:", (str(vd)[:400] if vd else None))
        if isinstance(vals, dict):
            small = {kk: vv for kk, vv in vals.items() if isinstance(vv, (int, float, str, bool)) or vv is None}
            print("   values:", json.dumps(small, ensure_ascii=False)[:700])
        sel[k] = v
    else:
        print("\n##", k, "=", str(v)[:300])
        sel[k] = v
json.dump(sel, open(os.path.join(OUT, "core_v386_sel.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nescrito core_v386_sel.json com", len(sel), "chaves")
