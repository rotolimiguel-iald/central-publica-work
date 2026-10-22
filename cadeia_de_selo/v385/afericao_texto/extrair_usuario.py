import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
out=[]
with open(p,encoding='utf-8') as f:
    for ln in f:
        try: o=json.loads(ln)
        except Exception: continue
        if o.get('type')!='user': continue
        ts=o.get('timestamp','')
        if not (ts.startswith('2026-10-04') or ts.startswith('2026-10-05')): continue
        m=o.get('message',{})
        c=m.get('content')
        txt=''
        if isinstance(c,str): txt=c
        elif isinstance(c,list):
            for b in c:
                if isinstance(b,dict) and b.get('type')=='text': txt+=b.get('text','')
        if not txt.strip(): continue
        if o.get('isMeta'): continue
        out.append((ts,txt))
json.dump(out,open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
for ts,t in out:
    print('=====',ts,len(t)); print(t[:600].replace('\n',' / '))
