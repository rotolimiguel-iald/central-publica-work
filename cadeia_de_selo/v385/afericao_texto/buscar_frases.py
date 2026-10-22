import json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
p=r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
frases=["faz muito mais sentido léxico","não existe observador não conjugado","testemunha falsa é a testemunha estática","Não existe observador não conjugado"]
with open(p,encoding='utf-8') as f:
    for i,ln in enumerate(f):
        for fr in frases:
            if fr in ln:
                try: o=json.loads(ln)
                except Exception: o={}
                ty=o.get('type'); ts=o.get('timestamp'); op=o.get('operation'); role=(o.get('message') or {}).get('role') if isinstance(o.get('message'),dict) else None
                # locate the text
                k=ln.find(fr)
                print(f'L{i} type={ty} op={op} role={role} ts={ts} isMeta={o.get("isMeta")} | {fr}')
                print('   ...', ln[max(0,k-200):k+300].replace('\n',' / '))
