import json, hashlib, os, time
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
tot=0;bad=0
for n in ("050576","050579"):
    d=json.load(open(W+f"\CONFERENCIA_{n}.json",encoding="utf-8"))
    for e in d["entradas_sha256"]:
        p=e["arquivo"]
        if not os.path.exists(p): print(n,"MISSING",p); bad+=1; continue
        h=hashlib.sha256(open(p,"rb").read()).hexdigest()
        mt=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(p)))
        ok = (h==e["sha256"])
        tot+=1; bad+= (not ok)
        inside = p.lower().startswith(W.lower())
        print(n,"OK " if ok else "DIFF",mt,"inside_kit" if inside else "EXTERNAL",os.path.relpath(p,"C:\IALD\Central de Patentes") if p.lower().startswith("c:\iald\central de patentes") else p)
print("total",tot,"bad",bad)
