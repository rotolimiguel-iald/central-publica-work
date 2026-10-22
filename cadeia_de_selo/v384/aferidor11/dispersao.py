import json,os,re,glob,sys
PK=sys.argv[1]
rows={}
for p in sorted(glob.glob(os.path.join(PK,"teste_tempo*"))):
    if not os.path.isdir(p): continue
    nm=os.path.basename(p)
    rj=os.path.join(p,"result.json")
    if not os.path.exists(rj):
        print("SEM result.json:",nm, os.listdir(p)); continue
    d=json.load(open(rj,encoding="utf-8"))
    t=d.get("timing") or {}
    info={k:(t[k].get("reps") if isinstance(t[k],dict) else None) for k in t}
    print(nm,"worker",(d.get("worker_sha256") or "")[:16],"mode",d.get("mode"),"timing reps",info)
    if re.fullmatch(r"teste_tempo_v\d+",nm) and "64" in t and (t["64"].get("reps") or 0)>=3:
        rows[nm]=d
print("\nCRITERIO (teste_tempo_v<n>, d=64 reps>=3):",list(rows))
cur="teste_tempo_v9"
custos=["pipeline_s","t1_injection_sigma0_s","t1_extra_noise_level_s"]
print("\nlista d=64 (pipeline / injecao):")
for nm,d in rows.items():
    t=d["timing"]["64"]; print(f"  {nm} ({d['worker_sha256'][:16]}): {t['pipeline_s']:.4f} / {t['t1_injection_sigma0_s']:.4f}  reps={t['reps']}")
ds=sorted({int(k) for d in rows.values() for k in d["timing"]})
print("\nds:",ds)
glob_max_cur=(0,None)
for dd in ds:
    for c in custos:
        vals={nm:d["timing"][str(dd)][c] for nm,d in rows.items() if str(dd) in d["timing"] and c in d["timing"][str(dd)]}
        if cur not in vals: print("sem corrente",dd,c); continue
        mx=max(vals.values()); mn=min(vals.values())
        mc=mx/vals[cur]; mm=mx/mn
        slowest=max(vals,key=vals.get)
        print(f"d={dd:3d} {c:24s} n={len(vals)} maior/corrente={mc:.4f} maior/menor={mm:.4f} mais_lenta={slowest} {'MM>1.25' if mm>1.25 else ''}")
        if mc>glob_max_cur[0]: glob_max_cur=(mc,(dd,c))
print("\nmaior/corrente global:",glob_max_cur)
