# -*- coding: utf-8 -*-
"""critico_recomputo2.py — complemento: vereditos do protocolo V1 (core), F2 e a correção ao lado de R6 (core), prior_dtau do C4,
critérios dos test_candidates do RINGDOWN_5SIGMA_V1, e a ILUSTRAÇÃO DA CONTAMINAÇÃO (z_excl dos k grandes a partir da deformação comum
JÁ NO REGISTRO desde 22/09 — NÃO é veredito nem poder; mostra que o desfecho do conjunto A para esses k é legível antes do pré-registro)."""
import json, hashlib, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
R = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
CORE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
def sha16(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()[:16]
out = {}
core = json.load(open(CORE, encoding="utf-8")); c = core.get("core", core)
P = c["ringdown_dephasing_protocol"]["protocol"]
out["protocol_top_keys"] = list(P.keys())
for k in ("allowed_verdicts","forbidden_verdicts","verdict_matrix","matrix","thresholds","hypothesis"):
    if k in P: out["protocol."+k] = P[k]
L = c["the_ledger_of_charges_v383"]
out["ledger.F2"] = [e for e in L["ledger"] if e.get("id") == "F2"]
out["ledger.corrections_beside.R6"] = L["corrections_beside_20261002"].get("R6")
out["ledger.corrections_beside.R6_in_the_routes"] = L["corrections_beside_20261002"].get("R6_in_the_routes")
out["ledger.corrections_beside.optics"] = str(L["corrections_beside_20261002"].get("optics"))[:900]
S = c["ringdown_scope_v376"]
out["scope.scope_fixed_in_writing"] = S.get("scope_fixed_in_writing")
out["scope.erratum_beside"] = S.get("erratum_beside")
# C4 prior_dtau
j4 = json.load(open(os.path.join(R, "C4_CATALOG_220.json"), encoding="utf-8"))
pr = {}
for row in j4["rows"]:
    key = json.dumps(row.get("prior_dtau"), sort_keys=True); pr[key] = pr.get(key, 0) + 1
out["C4.prior_dtau_contagem"] = pr
# RINGDOWN_5SIGMA_V1: criterios dos candidatos
p5 = os.path.join(R, "RINGDOWN_5SIGMA_V1.json"); j5 = json.load(open(p5, encoding="utf-8"))
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("test_candidates", "calibration_event_ids"):
                yield path + "/" + k, v
            yield from walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o[:3]): yield from walk(v, path + "[%d]" % i)
for pth, v in walk(j5):
    out["5SIGMA." + pth] = {"n": len(v), "primeiros": [str(x)[:60] for x in (v[:5] if isinstance(v, list) else list(v)[:5])]}
# procurar texto de criterio perto
for k in ("selection", "selection_criteria", "criteria", "test_set", "blind_set", "design", "notes", "status", "registered_at", "registered_utc"):
    if k in j5: out["5SIGMA.top." + k] = str(j5[k])[:600]
out["5SIGMA.top_keys"] = list(j5.keys())
# ILUSTRAÇÃO DA CONTAMINAÇÃO (não veredito): deformação comum dos 31 já no registro (memória ordem-013 l.102: +0,072 [+0,015; +0,134] a 90 %)
# usa a sigma_comb cega 0.03357 (E0_CORE/poder_cego) e as previsões EXATAS recomputadas em CRITICO_RECOMPUTO.json
rc = json.load(open(os.path.join(HERE, "CRITICO_RECOMPUTO.json"), encoding="utf-8"))
dbar_registro = 0.072  # [NÃO-CEGO — memória ordem-013 l.102; registrado 22/09; NÃO lido de dado novo]
ilus = {}
for nome, r in rc["poder_31_exato_vs_linear"].items():
    ilus[nome] = {"delta_exato_31": r["delta_exato"], "sigma_comb": r["sigma_comb"],
                  "z_excl_se_o_registro_valer_(NAO_CEGO, ilustracao)": (dbar_registro - r["delta_exato"]) / r["sigma_comb"]}
out["ILUSTRACAO_CONTAMINACAO_conjunto_A"] = {"nota": "deformacao comum +0,072 ja no registro (22/09, NAO-CEGO); nao e veredito; mostra que para k>=4pi o desfecho do conjunto A e legivel ANTES do pre-registro", "valores": ilus}
json.dump(out, open(os.path.join(HERE, "CRITICO_RECOMPUTO2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", sha16(os.path.join(HERE, "CRITICO_RECOMPUTO2.json")))
