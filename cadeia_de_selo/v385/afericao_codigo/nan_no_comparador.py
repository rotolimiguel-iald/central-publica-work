# SO LEITURA: o comparador do candidato diante de NaN / inf (o resumo e' lido de JSON; json.load aceita NaN/Infinity)
import json, os, sys, hashlib, math, copy
sys.stdout.reconfigure(encoding="utf-8")
PK = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v385"
src = open(PK + r"\um_v385_candidato.py", encoding="utf-8").read().splitlines()
def grab(p):
    i = [k for k, l in enumerate(src) if l.startswith(p)][0]; j = i + 1
    while j < len(src) and (src[j].startswith((" ", "\t")) or src[j].strip() == ""):
        j += 1
    return "\n".join(src[i:j])
ns = {"os": os, "hashlib": hashlib, "json": json}
for p in ("def _qp_summary(", "_QP_REPRO_SKIP_V385 =", "def _qp_flat_v385(", "def quantum_pillar_reproducibility_v385("):
    exec(grab(p), ns)
R = json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar\75dc30bc9cc8d330e31f99ca\result.json", encoding="utf-8"))
S = ns["_qp_summary"](R)
prev = {"read": True, "summary": S, "verdict": R["verdict"], "sha256": "x", "finished": "x", "run_id": "x", "key": "k"}
def rec_with(mod):
    s2 = copy.deepcopy(S); mod(s2)
    return {"summary": s2, "verdict": R["verdict"], "reuse": {"reused": False}}
cases = {
  "mesmo resumo": lambda s: None,
  "NaN onde havia numero (D128.gap_rel)": lambda s: s["D128"].__setitem__("gap_rel", float("nan")),
  "inf onde havia numero (D128.gap)": lambda s: s["D128"].__setitem__("gap", float("inf")),
  "residuo de maquina 2.3e-16 -> 2.5e-16 (T2.identities.VtPF_eq_PF_d8)": lambda s: s["T2"]["identities"].__setitem__("VtPF_eq_PF_d8", 2.5e-16),
  "D128.max_re -8.86e-15 -> -1.2e-14": lambda s: s["D128"].__setitem__("max_re", -1.2e-14),
  "D128 nao rodou (prazo)": lambda s: s.__setitem__("D128", {"started": False, "ran": False, "status_code": "NOT_RUN_DEADLINE", "error": "prazo"}),
  "D128.started True->False (campo pulado pelo nome 'started')": lambda s: s["D128"].__setitem__("started", False),
}
for nm, f in cases.items():
    o = ns["quantum_pillar_reproducibility_v385"](prev, rec_with(f))
    print("%-70s -> %s | n_differ=%s max_rel=%s" % (nm, o["verdict"].replace("TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__", "")[:70], o.get("n_differ"), o.get("max_rel_diff")))
print("max(0.0, nan) =", max(0.0, float("nan")))
print("'started' em D128 do resultado da v384:", (R.get("D128") or {}).get("started"), "| entra no resumo achatado?", any(k.endswith("D128.started") for k, _ in ns["_qp_flat_v385"](S)))
