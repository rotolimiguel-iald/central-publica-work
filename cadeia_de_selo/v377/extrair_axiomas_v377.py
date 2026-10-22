# -*- coding: utf-8 -*-
"""Extrai o relatorio de axiomas do build completo do kernel candidato (build_full.log), com a MESMA regex do verify do um.py,
e confere: rc 0, zero sorry, todas as bandeiras v377 resolvidas no trio. Grava sandbox_axiom_report__um_v377_candidato.json e sandbox_raiz_v377.json."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, "build_full.log"), encoding="utf-8", errors="replace").read()
assert t.rstrip().endswith("rc=0"), "build_full nao terminou verde"
axioms = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", t, re.S):
    axioms[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", t):
    axioms.setdefault(m.group(1), [])
sorry = len(re.findall(r"declaration uses 'sorry'", t))
flags = json.load(open(os.path.join(HERE, "BANDEIRAS_v377.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "BANDEIRAS_v377.json")) else None
fora = {k: v for k, v in axioms.items() if not set(v) <= {"propext", "Classical.choice", "Quot.sound"}}
res = {"n_axiom_report": len(axioms), "sorry_warnings": sorry, "fora_do_trio": fora}
if flags:
    res["bandeiras"] = {f: (nm in axioms and set(axioms[nm]) <= {"propext", "Classical.choice", "Quot.sound"}) for f, nm in flags}
    res["bandeiras_ok"] = sum(res["bandeiras"].values())
json.dump(axioms, open(os.path.join(HERE, "sandbox_axiom_report__um_v377_candidato.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(res, open(os.path.join(HERE, "sandbox_raiz_v377.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "bandeiras"}, ensure_ascii=False)[:2000])
if flags:
    print("bandeiras falsas:", [f for f, v in res["bandeiras"].items() if not v])
