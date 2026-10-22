import json, io, sys, re, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
selo = json.load(io.open(NOS + r"\um_absoluto_selo.json", encoding="utf-8"))
core = json.load(io.open(NOS + r"\um_absoluto.json", encoding="utf-8"))
print("selo.um_version =", selo.get("um_version"), "| core.um_version =", core.get("um_version"))
print("selo keys sample:", [k for k in selo.keys()][:12])
# beta from um.py by regex
src = io.open(NOS + r"\um.py", encoding="utf-8", errors="replace").read()
m = re.search(r"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", src)
alpha = float(m.group(1)) if m else None
print("ALPHA_FINE_CODATA_2018 (regex um.py) =", alpha, "| beta = alpha*sqrt(e) =", alpha*math.sqrt(math.e) if alpha else None)
print("core.beta =", core.get("beta"))
def find(obj, key, path="core", out=None, depth=0):
    if out is None: out=[]
    if depth>7: return out
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k==key: out.append((path+"."+k, v))
            find(v, key, path+"."+k, out, depth+1)
    elif isinstance(obj, list):
        for i,v in enumerate(obj[:50]): find(v, key, path+"[%d]"%i, out, depth+1)
    return out
for key in ("bancada_fase4_v378", "bancada_fases_5_6_7_v380", "bancada_fases_v377"):
    hits = find(core, key)
    print("\n==", key, "->", [p for p,_ in hits][:3])
    if hits:
        blk = hits[0][1]
        if key=="bancada_fase4_v378":
            for sub in ("P_ladder_d1b","P_ladder_d1a","Q_pantheon_d1b","R_dr1_d1b","S_joint_d1b","T_intermediate_d1b","stacked_control","hashes","verdict","statute"):
                print("  ", sub, "=", json.dumps(blk.get(sub), ensure_ascii=False)[:900])
        elif key=="bancada_fases_5_6_7_v380":
            print("   keys:", list(blk.keys())[:40])
            for sub in ("fase5","verdict","hashes","statute"):
                print("  ", sub, "=", json.dumps(blk.get(sub), ensure_ascii=False)[:1500])
        else:
            print("   keys:", list(blk.keys())[:40])
