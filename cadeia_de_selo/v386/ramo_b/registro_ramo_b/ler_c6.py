import json, hashlib, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"C:\IALD\Central de Patentes\Chatgpt\ORDEM_013_RINGDOWN\C6_RESULTS.json"
b = open(p,"rb").read(); print("sha256", hashlib.sha256(b).hexdigest()[:16], len(b))
d = json.loads(b.decode("utf-8"))
def walk(o, path="", depth=0):
    if isinstance(o, dict):
        for k,v in o.items():
            if isinstance(v,(dict,list)) and depth<3: walk(v, path+"/"+k, depth+1)
            elif not isinstance(v,(dict,list)): 
                s = str(v); print(path+"/"+k, "=", s[:200])
    elif isinstance(o, list):
        for i,v in enumerate(o[:6]): walk(v, path+f"[{i}]", depth+1)
walk(d)
