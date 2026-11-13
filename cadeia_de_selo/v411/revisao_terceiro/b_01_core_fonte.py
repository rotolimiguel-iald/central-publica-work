from b_lib import *
c = core()["core"]
t = c["teste_de_veracidade_fase9_v397"]
print(type(t).__name__, list(t.keys())[:40])
def find(o, key, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            p = path+"."+k
            if key in k: print(p, '=>', json.dumps(v, ensure_ascii=False)[:200])
            find(v, key, p)
    elif isinstance(o, list):
        for i,v in enumerate(o[:50]): find(v, key, path+"[%d]"%i)
for k in ("z_disc","z_delta","lnB","ln_B","lnb"):
    find(t, k)
e = c["estatuto_da_prova_v391"]
print(json.dumps(e["prova_2_ritos"], ensure_ascii=False)[:1500])
