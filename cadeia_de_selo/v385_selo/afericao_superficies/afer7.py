import json, re
T = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
want = ["2026-10-05T09:39:15","2026-10-05T10:09:10","2026-10-05T11:42:33","2026-10-05T14:21:44","2026-10-05T14:35:07","2026-10-05T14:40:13"]
hits = {w:[] for w in want}
def strip(t):
    return re.sub(r"<pasted_content>.*?</pasted_content>", "[pasted]", t, flags=re.S)
with open(T, encoding="utf-8", errors="replace") as f:
    for ln in f:
        try: o=json.loads(ln)
        except: continue
        if o.get("isCompactSummary") or o.get("isMeta"): continue
        ts=o.get("timestamp","")
        typ=o.get("type")
        txt=None
        if typ=="user":
            m=o.get("message",{}); c=m.get("content")
            if isinstance(c,str): txt=c
            elif isinstance(c,list):
                parts=[x.get("text","") for x in c if isinstance(x,dict) and x.get("type")=="text"]
                txt="\n".join(parts) if parts else None
        elif typ=="attachment":
            a=o.get("attachment",{})
            if a.get("type")=="queued_command": txt=a.get("prompt") or a.get("content") or str(a)[:500]
        if not txt: continue
        for w in want:
            if ts.startswith(w): hits[w].append((ts,typ,strip(txt)))
for w in want:
    print(f"\n===== {w} : {len(hits[w])} hit(s) =====")
    for ts,typ,txt in hits[w]:
        print(f"[{ts}] ({typ}) len={len(txt)}")
        print(txt[:3000])
