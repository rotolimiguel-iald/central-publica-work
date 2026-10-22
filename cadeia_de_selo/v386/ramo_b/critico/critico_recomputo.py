# -*- coding: utf-8 -*-
"""critico_recomputo.py — crítico de completude (ramo B, v386). Só leitura fora desta pasta.
(1) poder EXATO (-x/(1+x)) vs LINEAR (-x) sobre as mesmas sigmas/spins do PODER_CEGO_RAMO_B.json (nenhum valor central lido);
(2) RINGDOWN_5SIGMA_V1.json: contagem de test_candidates / calibration;
(3) C4_CATALOG_220.json: priors de dtau220 (sem ler medianas);
(4) core v385: the_ledger_of_charges_v383 (R6, F2, regra de canal) e ringdown_dephasing_protocol (vereditos permitidos/proibidos)."""
import json, hashlib, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
PC = os.path.join(HERE, "..", "pre_registro", "PODER_CEGO_RAMO_B.json")
R = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
CORE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
def sha16(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()[:16]
out = {"fontes": {}}
pc = json.load(open(PC, encoding="utf-8")); out["fontes"]["PODER_CEGO_RAMO_B.json"] = sha16(PC)
beta = pc["beta"]; out["beta_lido_do_json"] = beta
# (1) poder exato vs linear
res = {}
for nome, r in pc["resultados"].items():
    e = r["GWTC5_31_std"]
    W = 0.0; Slin = 0.0; Sexa = 0.0
    for p in e["per_event"]:
        s = p["sigma"]; x = beta * p["k"] * p["N_a"]
        w = 1/s**2; W += w; Slin += w*(-x); Sexa += w*(-x/(1+x))
    sc = 1/math.sqrt(W)
    res[nome] = {"sigma_comb": sc, "delta_lin": Slin/W, "poder_lin": abs(Slin/W)/sc, "delta_exato": Sexa/W, "poder_exato": abs(Sexa/W)/sc,
                 "poder_lin_no_json": e["power"], "razao_exato_sobre_lin": (abs(Sexa/W)/sc)/(abs(Slin/W)/sc)}
out["poder_31_exato_vs_linear"] = res
# k_min pelas duas regras (sobre o delta medio ponderado k=1)
d1 = abs(res["k=1 (GM/c^3)"]["delta_lin"])
out["k_min_duas_regras"] = {"regra_fase6_sist_rel_0p3 (sigma_sys/|delta|<=0.3)": {"0.029": 0.029/0.3/d1, "0.038": 0.038/0.3/d1},
                            "regra_fisica (sigma_sys <= |delta|/5)": {"0.029": 5*0.029/d1, "0.038": 5*0.038/d1}}
# (2) RINGDOWN_5SIGMA_V1
p5 = os.path.join(R, "RINGDOWN_5SIGMA_V1.json")
try:
    j5 = json.load(open(p5, encoding="utf-8")); out["fontes"]["RINGDOWN_5SIGMA_V1.json"] = sha16(p5)
    def find(o, key, acc):
        if isinstance(o, dict):
            for k,v in o.items():
                if k == key: acc.append(v)
                find(v, key, acc)
        elif isinstance(o, list):
            for v in o: find(v, key, acc)
    acc=[]; find(j5, "test_candidates", acc); out["RINGDOWN_5SIGMA_V1.test_candidates_n"] = [len(a) if isinstance(a,(list,dict)) else str(a)[:80] for a in acc]
    acc=[]; find(j5, "calibration_event_ids", acc); out["RINGDOWN_5SIGMA_V1.calibration_n"] = [len(a) if isinstance(a,(list,dict)) else str(a)[:80] for a in acc]
    out["RINGDOWN_5SIGMA_V1.top_keys"] = list(j5.keys())[:40]
except Exception as ex:
    out["RINGDOWN_5SIGMA_V1"] = "ERRO: %s" % ex
# (3) priors do C4
pc4 = os.path.join(R, "C4_CATALOG_220.json")
j4 = json.load(open(pc4, encoding="utf-8")); out["fontes"]["C4_CATALOG_220.json"] = sha16(pc4)
priors = {}
for row in j4["rows"]:
    pr = json.dumps(row.get("prior"), sort_keys=True)
    priors[pr] = priors.get(pr, 0) + 1
out["C4_priors_dtau220_contagem"] = priors
out["C4_row_keys"] = list(j4["rows"][0].keys())
# (4) core
core = json.load(open(CORE, encoding="utf-8")); out["fontes"]["um_absoluto.json"] = sha16(CORE)
c = core.get("core", core)
L = c.get("the_ledger_of_charges_v383", {})
out["ledger_keys"] = list(L.keys())
rr = L.get("readings_ratified_20261002", {})
out["ledger_R6"] = rr.get("R6") if isinstance(rr, dict) else str(rr)[:300]
out["ledger_corrections_beside_keys"] = list(L.get("corrections_beside_20261002", {}).keys()) if isinstance(L.get("corrections_beside_20261002"), dict) else str(L.get("corrections_beside_20261002"))[:500]
led = L.get("ledger", [])
out["ledger_n"] = len(led)
out["ledger_entries_short"] = [{k: (str(v)[:160]) for k, v in (e.items() if isinstance(e, dict) else {}) if k in ("id","name","side","law","reading","outcome","status","channel","lado","lei","leitura","desfecho")} for e in led] if isinstance(led, list) else str(led)[:500]
for k in ("rules","rule","one_channel_per_law","channel_rule","ledger_rules"):
    if k in L: out["ledger_rule_"+k] = str(L[k])[:800]
out["ledger_verdict"] = str(L.get("verdict",""))[:1200]
P = c.get("ringdown_dephasing_protocol", {})
out["protocol_keys"] = list(P.keys())
for k in ("allowed_verdicts","forbidden_verdicts","verdicts_allowed","verdicts_forbidden"):
    if k in P: out["protocol_"+k] = P[k]
rec = P.get("record", {})
if isinstance(rec, dict):
    for k in ("allowed_verdicts","forbidden_verdicts","hypothesis","observable","branch_A","branch_B"):
        if k in rec: out["protocol_record_"+k] = rec[k]
    hyp = rec.get("hypothesis", {})
    if isinstance(hyp, dict):
        for k in ("allowed_verdicts","forbidden_verdicts","law","observable","branch_A","branch_B"):
            if k in hyp: out["protocol_hyp_"+k] = hyp[k]
S = c.get("ringdown_scope_v376", {})
out["scope_keys"] = list(S.keys())
out["scope_branch_B_concurrent_values"] = S.get("branch_B_concurrent_values")
out["scope_audit_declared"] = str(S.get("audit_ringdown_contradictions_declared"))[:1500]
json.dump(out, open(os.path.join(HERE, "CRITICO_RECOMPUTO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)[:12000])
