import os, json, hashlib, datetime, sys
BASE=r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for ch in iter(lambda:f.read(1<<20),b''): h.update(ch)
    return h.hexdigest()
fz=os.path.join(BASE,"1_PREREGISTRO","FREEZE.json")
out={}
out["FREEZE.json"]={"sha256":sha(fz),"bytes":os.path.getsize(fz),"mtime_utc":datetime.datetime.fromtimestamp(os.path.getmtime(fz),datetime.timezone.utc).isoformat()}
F=json.load(open(fz,encoding='utf-8'))
out["freeze_keys"]=list(F.keys())
cong=F.get("congelado_em_utc")
out["congelado_em_utc"]=cong
t0=datetime.datetime.fromisoformat(cong)
for k in ("PREREGISTRO.json","PREREGISTRO.md"):
    p=os.path.join(BASE,"1_PREREGISTRO",k)
    out[k]={"sha256":sha(p),"bytes":os.path.getsize(p),"mtime_utc":datetime.datetime.fromtimestamp(os.path.getmtime(p),datetime.timezone.utc).isoformat()}
# all files in 1_PREREGISTRO: mtime after freeze?
later=[]
for root,d,fs in os.walk(os.path.join(BASE,"1_PREREGISTRO")):
    for f in fs:
        p=os.path.join(root,f); mt=datetime.datetime.fromtimestamp(os.path.getmtime(p),datetime.timezone.utc)
        if mt>t0: later.append((os.path.relpath(p,BASE),mt.isoformat()))
out["1_PREREGISTRO_files_after_freeze"]=later
# 2_OPTICO and 3_KERNEL: earliest mtime, any before freeze
res={}
for sub in ("2_OPTICO","3_KERNEL","5_R2","4_RELATORIO"):
    n=0; before=[]; earliest=None; latest=None
    for root,d,fs in os.walk(os.path.join(BASE,sub)):
        for f in fs:
            p=os.path.join(root,f); mt=datetime.datetime.fromtimestamp(os.path.getmtime(p),datetime.timezone.utc); n+=1
            if earliest is None or mt<earliest: earliest=mt
            if latest is None or mt>latest: latest=mt
            if mt<=t0: before.append((os.path.relpath(p,BASE),mt.isoformat(),sha(p)[:16]))
    res[sub]={"n_files":n,"earliest":earliest.isoformat() if earliest else None,"latest":latest.isoformat() if latest else None,"files_at_or_before_freeze":before}
out["subpastas"]=res
# freeze anexos check
anex=F.get("anexos") or F.get("anexos_conferidos") or F.get("arquivos")
out["freeze_anexos_type"]=type(anex).__name__
if isinstance(anex,list):
    ok=0; bad=[]
    for a in anex:
        p=a.get("arquivo") or a.get("path")
        if p and not os.path.isabs(p): p=os.path.join(BASE,"1_PREREGISTRO",p)
        if p and os.path.exists(p):
            s=sha(p); b=os.path.getsize(p)
            if s==a.get("sha256") and b==a.get("bytes"): ok+=1
            else: bad.append((p,s[:16],a.get("sha256","")[:16],b,a.get("bytes")))
        else: bad.append((p,"MISSING"))
    out["anexos_ok"]=ok; out["anexos_bad"]=bad
json.dump(out,open("AUD_FREEZE.json","w",encoding='utf-8'),indent=1,ensure_ascii=False)
print(json.dumps(out,indent=1,ensure_ascii=False)[:6000])
