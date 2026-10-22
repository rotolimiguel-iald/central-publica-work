import json, re
T = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
want = ["2026-10-05T09:39:15","2026-10-05T10:09:10","2026-10-05T11:19:54","2026-10-05T11:28:53","2026-10-05T11:31:35","2026-10-05T11:33:36","2026-10-05T11:38:12","2026-10-05T11:42:33","2026-10-05T14:21:44","2026-10-05T14:35:07","2026-10-05T14:40:13"]
hits = {w:[] for w in want}
def totext(c):
    if isinstance(c,str): return c
    if isinstance(c,list):
        return "\n".join(x.get("text","") if isinstance(x,dict) and x.get("type")=="text" else "" for x in c)
    return str(c)
def strip(t): return re.sub(r"<pasted_content>.*?</pasted_content>", "[pasted]", t, flags=re.S)
all_user=[]
with open(T, encoding="utf-8", errors="replace") as f:
    for ln in f:
        try: o=json.loads(ln)
        except: continue
        if o.get("isCompactSummary") or o.get("isMeta"): continue
        ts=o.get("timestamp",""); typ=o.get("type"); txt=None
        if typ=="user":
            c=o.get("message",{}).get("content")
            txt=totext(c)
            if "tool_result" in str(c)[:200] and isinstance(c,list) and all(isinstance(x,dict) and x.get("type")=="tool_result" for x in c): txt=None
        elif typ=="attachment":
            a=o.get("attachment",{})
            if a.get("type")=="queued_command": txt=totext(a.get("prompt") or a.get("content") or "")
        if not txt or not txt.strip(): continue
        if ts.startswith("2026-10-05"): all_user.append((ts,typ,strip(txt)))
        for w in want:
            if ts.startswith(w): hits[w].append((ts,typ,strip(txt)))
for w in want:
    print(f"\n===== {w} : {len(hits[w])} hit(s) =====")
    for ts,typ,txt in hits[w]:
        print(f"[{ts}] ({typ}) len={len(txt)}")
        print(txt[:2500])
print("\n\n===== todas as msgs do operador em 05/10 (ts, len, 120 chars) =====")
for ts,typ,txt in all_user:
    if typ=="user" and txt.startswith("<"): continue
    print(ts, typ, len(txt), repr(txt[:120]))
