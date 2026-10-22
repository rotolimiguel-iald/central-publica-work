import json, os, re
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
print("rodadas dir exists:", os.path.isdir(os.path.join(NOS,"rodadas")))
S = json.load(open(os.path.join(NOS,"um_absoluto_selo.json"), encoding="utf-8"))
print("selo top keys:", list(S.keys())[:60])
def find(obj, pat, path="", out=None, maxlen=400):
    if out is None: out=[]
    if isinstance(obj, dict):
        for k,v in obj.items():
            if re.search(pat, k, re.I): out.append((path+"/"+k, str(v)[:maxlen]))
            find(v, pat, path+"/"+k, out, maxlen)
    elif isinstance(obj, list):
        for i,v in enumerate(obj): find(v, pat, f"{path}[{i}]", out, maxlen)
    return out
for pat in [r"^version$|^versao|^rodada|^run_at|timestamp|^when", r"qg_closure_verdict", r"flags_true|n_flags|^gate", r"ladder|escada|theorem_count|n_theorems|verified", r"previous|anterior|supersedes", r"final_step_name", r"the_axiom_v385", r"pillar|pilar", r"reproducib", r"sha256|hash"]:
    res = find(S, pat)
    print(f"\n=== {pat} ({len(res)}) ===")
    for p,v in res[:40]: print(" ", p, "=>", v)
