import json,sys
sys.stdout.reconfigure(encoding='utf-8')
p=r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
lo,hi=sys.argv[1],sys.argv[2]; full=sys.argv[3] if len(sys.argv)>3 else ''
with open(p,encoding='utf-8') as f:
    for ln in f:
        try:o=json.loads(ln)
        except Exception: continue
        ts=o.get('timestamp','') or ''
        if not (lo<=ts<=hi): continue
        ty=o.get('type')
        if ty=='assistant':
            for b in (o.get('message') or {}).get('content') or []:
                if isinstance(b,dict) and b.get('type')=='text' and b['text'].strip():
                    t=b['text']
                    print('### ASSIST',ts,len(t)); print(t if (full and full in ts) else t[:700]); print()
        elif ty=='user':
            c=(o.get('message') or {}).get('content')
            if isinstance(c,str) and c.strip() and '<task-notification>' not in c:
                print('### USER',ts); print(c[:1500]); print()
            elif isinstance(c,list):
                for b in c:
                    if isinstance(b,dict) and b.get('type')=='text' and '<task-notification>' not in b.get('text','') and '<system-reminder>' not in b.get('text','')[:20]:
                        print('### USER',ts); print(b['text'][:1500]); print()
        elif ty=='attachment':
            a=o.get('attachment') or {}
            if a.get('type')=='queued_command':
                pr=a.get('prompt'); t=pr if isinstance(pr,str) else ' '.join(x.get('text','') for x in pr if isinstance(x,dict))
                print('### QUEUED',ts); print(t); print()
