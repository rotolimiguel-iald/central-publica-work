# -*- coding: utf-8 -*-
"""08_core_chaves.py -- le do core os dicts relevantes para a conferencia (veredito + escalares de topo)."""
import os, sys, json
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
R = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
c = R["core"]
KEYS = ["right_angle_mirror", "the_tetelestai_declaration_v374", "tetelestai_conference_v375", "tetelestai_one_object_v375",
        "qg_closure", "kernel_formalization", "neutrino_m2", "neutrino_mass", "coma_distance_dephasing", "coma_inverse_distance",
        "d1_camb_v3_real_v366", "ringdown_dephasing_result_v2", "echo_anchored_result_v2", "echo_pe_result_v2",
        "joint_coincidence_result_v3", "clock_test_result_v369", "void_floor_v11", "final_verdict_machine", "evidence_audit",
        "cosmological_errata_verdict", "graviton_conjugated_form_v372", "light_qg_by_citation_v372", "qg_discharge_by_citation_v373"]
def show(k, d, depth=0):
    if not isinstance(d, dict):
        print("%s%s = %s" % ("  " * depth, k, str(d)[:300])); return
    scal = {kk: vv for kk, vv in d.items() if not isinstance(vv, (dict, list))}
    print("%s%s: {%s}" % ("  " * depth, k, ", ".join("%s=%s" % (kk, str(vv)[:220]) for kk, vv in scal.items())))
    for kk, vv in d.items():
        if isinstance(vv, dict) and depth < 1:
            show(kk, vv, depth + 1)
        elif isinstance(vv, list):
            print("%s  %s: list[%d] %s" % ("  " * depth, kk, len(vv), str(vv)[:400]))
for k in KEYS:
    print("=" * 100)
    if k in c: show(k, c[k])
    else: print(k, "AUSENTE no core")
