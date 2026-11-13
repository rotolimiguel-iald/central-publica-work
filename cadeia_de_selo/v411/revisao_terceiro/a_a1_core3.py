import json, os, difflib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
b = json.load(open(os.path.join(V, "base_v410", "um_absoluto.json"), encoding="utf-8"))["core"]
c = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
x, y = b["estatuto_da_prova_v391"]["verdict"], c["estatuto_da_prova_v391"]["verdict"]
sm = difflib.SequenceMatcher(None, x, y)
for op in sm.get_opcodes():
    if op[0] != "equal": print(op[0], repr(x[op[1]:op[2]]), "->", repr(y[op[3]:op[4]]))
print(len(x), len(y))
print(b["estatuto_da_prova_v391"]["certificacao"].keys())
print(json.dumps(b["estatuto_da_prova_v391"]["certificacao"], ensure_ascii=False)[:600])
# selo_pela v399 other diffs list names only
import itertools
bb, cc = b["selo_pela_propria_tecnologia_v399"], c["selo_pela_propria_tecnologia_v399"]
def walk(x, y, p, out):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x)|set(y), key=str):
            if k in x and k in y: walk(x[k], y[k], p+"/"+str(k), out)
            else: out.append(p+"/"+str(k)+" (ausente de um lado)")
    elif isinstance(x, list) and isinstance(y, list):
        for i,(u,v) in enumerate(zip(x,y)): walk(u,v,p+"[%d]"%i,out)
        if len(x)!=len(y): out.append(p+" len")
    elif x!=y: out.append(p)
o=[]; walk(bb,cc,"",o)
print(len(o)); print([s[-70:] for s in o[14:]])
# o gate
print(b["qg_closure"]["gate"]["verdict"] == c["qg_closure"]["gate"]["verdict"], json.dumps(b["qg_closure"],sort_keys=True)==json.dumps(c["qg_closure"],sort_keys=True))
