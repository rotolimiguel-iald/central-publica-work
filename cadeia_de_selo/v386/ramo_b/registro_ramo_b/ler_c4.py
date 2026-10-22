import json, hashlib, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
base = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN"
for name in ["C4_CATALOG_COMBINATION.json","C4_GWTC3_COMBINATION.json","C4_GWTC3_PUBLISHED_COMBINATION.json","C3_PREDICTION_COMPATIBILITY.json","C4_FREE_CLOCK_ORACLE.json"]:
    p = base + "\\" + name
    try:
        b = open(p,"rb").read()
    except Exception as e:
        print("AUSENTE", name, e); continue
    print("\n####", name, hashlib.sha256(b).hexdigest()[:16], len(b))
    d = json.loads(b.decode("utf-8"))
    def walk(o, path="", depth=0):
        if isinstance(o, dict):
            for k,v in o.items():
                if isinstance(v,(dict,list)) and depth<2: walk(v, path+"/"+k, depth+1)
                elif not isinstance(v,(dict,list)): print(path+"/"+k, "=", str(v)[:160])
        elif isinstance(o, list):
            print(path, "= list[%d]" % len(o))
            for i,v in enumerate(o[:3]): walk(v, path+f"[{i}]", depth+1)
    walk(d)
