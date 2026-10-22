import json, re, hashlib, sys
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CORE = NOS + r"\um_absoluto.json"
SELO = NOS + r"\um_absoluto_selo.json"
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for ch in iter(lambda: f.read(1<<20), b""): h.update(ch)
    return h.hexdigest()
core = json.load(open(CORE, encoding="utf-8"))
selo = json.load(open(SELO, encoding="utf-8"))
print("sha256 core:", sha(CORE))
print("sha256 selo:", sha(SELO))
print("TOP core keys (%d):" % len(core))
for k in core: 
    v = core[k]
    print("  ", k, type(v).__name__, (len(v) if hasattr(v,'__len__') else ''))
print("TOP selo keys (%d):" % len(selo))
for k in selo:
    v = selo[k]
    print("  ", k, type(v).__name__, (len(v) if hasattr(v,'__len__') else ''))
# walk verdicts
out=[]
def walk(o, path):
    if isinstance(o, dict):
        for k,v in o.items(): walk(v, path+"/"+str(k))
    elif isinstance(o, list):
        for i,v in enumerate(o): walk(v, path+"[%d]"%i)
    elif isinstance(o, str):
        if o.startswith("TGL_"):
            out.append((path, o))
walk(core, "")
print("N strings starting with TGL_ in core:", len(out))
# unique by path
uniq_vals = set(v for _,v in out)
print("N unique TGL_ values:", len(uniq_vals))
rx_conf = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
rx_fals = re.compile(r"(?<!NOT_)(?<!UN)FALSIFIED")
cats = {"FALSIFIED":[], "NOT_FALSIFIED":[], "INCONCLUSIVE":[], "AWAITING":[], "CONFIRMED_PROVED":[]}
for p,v in out:
    if rx_fals.search(v): cats["FALSIFIED"].append((p,v))
    if "NOT_FALSIFIED" in v: cats["NOT_FALSIFIED"].append((p,v))
    if "INCONCLUSIVE" in v: cats["INCONCLUSIVE"].append((p,v))
    if "AWAITING" in v: cats["AWAITING"].append((p,v))
    if rx_conf.search(v): cats["CONFIRMED_PROVED"].append((p,v))
for c,l in cats.items():
    print("==", c, len(l), "(unique values:", len(set(v for _,v in l)), ")")
json.dump({"sha256_core":sha(CORE),"sha256_selo":sha(SELO),"n_TGL_strings":len(out),"n_unique":len(uniq_vals),
           "all":[{"path":p,"value":v} for p,v in out],
           "cats":{c:[{"path":p,"value":v} for p,v in l] for c,l in cats.items()}},
          open("inv_verdicts.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
