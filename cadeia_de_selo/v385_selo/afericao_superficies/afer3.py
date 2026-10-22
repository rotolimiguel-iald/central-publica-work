import json, os, re
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
S = json.load(open(os.path.join(NOS,"um_absoluto_selo.json"), encoding="utf-8"))
print("=== the_axiom_v385 (selo) ===")
print(json.dumps(S["the_axiom_v385"], ensure_ascii=False, indent=1)[:6000])
print("\n=== quantum_pillar_v384 (selo) keys ===")
qp=S["quantum_pillar_v384"]; print(list(qp.keys()))
for k in ["verdict","branch","negatives","honest_negatives","run_dir","run_id","duration_s","elapsed_s","wall_s","gpu","env","finished","started","cached","cache_key","cache"]:
    if k in qp: print(k,"=>",str(qp[k])[:600])
print("\n=== quantum_pillar_reproducibility_v385 (selo) full ===")
print(json.dumps(S["quantum_pillar_reproducibility_v385"], ensure_ascii=False, indent=1)[:5000])
print("\n=== flags 18 ===")
flags=[k for k in S if isinstance(S[k],bool)]
print(len(flags), [(k,S[k]) for k in flags])
print("\n=== um_version / identity ===", S.get("um_version"), str(S.get("identity"))[:300])
print("the_axiom_reading_v385 =>", S.get("the_axiom_reading_v385"))
print("\n=== sha256 block full ===")
for k,v in S["sha256"].items(): print(" ",k, v[:16])
