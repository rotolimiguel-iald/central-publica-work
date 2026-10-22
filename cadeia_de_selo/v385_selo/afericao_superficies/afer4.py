import json, os, re, hashlib
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
C = json.load(open(os.path.join(NOS,"um_absoluto.json"), encoding="utf-8"))
print("core top keys n=", len(C))
def find(obj, pat, path="", out=None, maxlen=300):
    if out is None: out=[]
    if isinstance(obj, dict):
        for k,v in obj.items():
            if re.search(pat, k, re.I): out.append((path+"/"+k, v))
            find(v, pat, path+"/"+k, out, maxlen)
    elif isinstance(obj, list):
        for i,v in enumerate(obj): find(v, pat, f"{path}[{i}]", out, maxlen)
    return out
for pat in [r"^the_axiom_v385$", r"^quantum_pillar_reproducibility_v385$", r"^quantum_pillar_v384$"]:
    for p,v in find(C, pat):
        print(f"\n=== {p} ===")
        print(json.dumps(v, ensure_ascii=False, indent=1)[:7000])
# kernel counts
print("\n=== counts (6027 / 5998 / 29) ===")
for p,v in find(C, r"n_theorems|theorem_count|n_decl|total_decl|declarations|ladder_total|escada|n_verified|all_verified_count|n_stones|kernel_count"):
    if not isinstance(v,(dict,list)): print(" ",p,"=>",str(v)[:200])
s=json.dumps(C)
for tok in ["6027","5998","29_OF_29","29 de 29","131"]:
    print(tok, "count in core json:", s.count(tok))
