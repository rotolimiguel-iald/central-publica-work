import json, hashlib, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
b = open(p,"rb").read()
d = json.loads(b.decode("utf-8"))
core = d.get("core", d)
def find(obj, needle, path="", out=None):
    if out is None: out=[]
    if isinstance(obj, dict):
        for k,v in obj.items():
            if needle in k.lower(): out.append(path+"/"+k)
            find(v, needle, path+"/"+k, out)
    elif isinstance(obj, list):
        for i,v in enumerate(obj): find(v, needle, path+f"[{i}]", out)
    return out
for n in ["audit_ringdown","contradictions_declared","branch_b","tau_star","gw250114","delta_tau"]:
    r = find(core, n)
    print("==", n, len(r)); 
    for x in r[:30]: print("   ", x)
for k in ["ringdown_dephasing_protocol","ringdown_dephasing_result","ringdown_dephasing_amendment_v2","ringdown_dephasing_result_v2","ringdown_scope_v376"]:
    print("\n######", k)
    print(json.dumps(core[k], ensure_ascii=False, indent=1)[:12000])
