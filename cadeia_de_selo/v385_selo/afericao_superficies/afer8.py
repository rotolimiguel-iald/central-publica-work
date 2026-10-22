import json, re
T = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
# assistant text messages between 13:30 and 14:22 UTC that mention 'subpasta'
rows=[]
with open(T, encoding="utf-8", errors="replace") as f:
    for ln in f:
        try: o=json.loads(ln)
        except: continue
        if o.get("isCompactSummary") or o.get("isMeta"): continue
        ts=o.get("timestamp",""); typ=o.get("type")
        if not ts.startswith("2026-10-05T1"): continue
        if typ!="assistant": continue
        c=o.get("message",{}).get("content")
        if isinstance(c,list):
            txt="\n".join(x.get("text","") for x in c if isinstance(x,dict) and x.get("type")=="text")
        else: txt=str(c)
        if "subpasta" in txt or "preregistro_dois_lados" in txt or "preregistro_pilar_quantico_v384" in txt:
            rows.append((ts,txt))
for ts,txt in rows:
    if "2026-10-05T13:" <= ts <= "2026-10-05T14:22" or "preregistro_dois_lados_v383" in txt:
        print("=====",ts, len(txt)); 
        for m in re.finditer(r"[^\n]*(subpasta|preregistro_dois_lados|preregistro_pilar_quantico_v384)[^\n]*", txt):
            print("   ", m.group(0)[:600])
