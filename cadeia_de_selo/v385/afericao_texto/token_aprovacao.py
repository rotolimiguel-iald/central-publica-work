import json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
p=r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
TOK="AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER_RETURNS_AS_THE_FIXED_POINT_OF_THE_READING__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS"
rows=[]
with open(p,encoding='utf-8') as f:
    for i,ln in enumerate(f):
        try:o=json.loads(ln)
        except Exception: continue
        ts=o.get('timestamp','') or ''
        if not ts.startswith('2026-10-05'): continue
        ty=o.get('type')
        if ty=='assistant':
            for b in (o.get('message') or {}).get('content') or []:
                if isinstance(b,dict) and b.get('type')=='text':
                    t=b['text']
                    for m in re.finditer(r'AXIOMA__[A-Z0-9_]+',t):
                        rows.append((ts,'assistant-text',m.group(0)==TOK,m.group(0)[:80], len(m.group(0))))
        if ty=='user' or ty=='attachment':
            pass
for r in rows: print(r)
# the visible assistant texts right before key operator messages
