import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
d = json.loads(open(p,"rb").read().decode("utf-8")); core = d.get("core", d)
c = core.get("clock_test_protocol_v369", {})
print(json.dumps(c.get("record",{}).get("tau_star_alternatives"), ensure_ascii=False, indent=1)[:3000])
r = core.get("clock_test_result_v369", {})
for k in ["tau_star_s","tau_star_alternatives","verdict"]:
    print(k, "=", json.dumps(r.get(k), ensure_ascii=False)[:1500])
P1 = r.get("P1",{})
for k in ["tau_star_bound_clock_95_s","tau_star_bound_clock_95_in_tP","tau_star_bound_best_s","tau_star_bound_best_in_tP","tau_star_bound_best_platform","tau_star_bound_best_kind"]:
    print(k, "=", P1.get(k))
print("P2", json.dumps(r.get("P2"), ensure_ascii=False)[:1200])
dr = core.get("dephasing_reach", {}); print("dephasing_reach.tau_star_s", dr.get("tau_star_s"), "verdict", dr.get("verdict"))
