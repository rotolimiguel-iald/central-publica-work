import json,sys,hashlib
P=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
b=open(P,'rb').read(); print('sha16',hashlib.sha256(b).hexdigest()[:16])
d=json.loads(b)
print(list(d.keys())[:40])
c=d.get('core',d)
print(len(c))
pats=sys.argv[1:]
def walk(o,p):
    if isinstance(o,dict):
        for k,v in o.items():
            q=p+'.'+k
            if any(s.lower() in k.lower() for s in pats):
                s=json.dumps(v,ensure_ascii=False)
                print(q,'=>',s[:600])
            walk(v,q)
    elif isinstance(o,list):
        for i,v in enumerate(o[:50]): walk(v,p+f'[{i}]')
walk(c,'core')
