import json,sys,hashlib
PK=sys.argv[1]
IGN={"gerado","gerado_utc","id","titulo"}
def walk(a,b,path,out):
    if isinstance(a,dict) and isinstance(b,dict):
        for k in sorted(set(a)|set(b)):
            if k in IGN: 
                if a.get(k)!=b.get(k): out.append(("IGNORADO",path+"/"+k))
                continue
            if k not in a: out.append(("SO_V12",path+"/"+k)); continue
            if k not in b: out.append(("SO_V11",path+"/"+k)); continue
            walk(a[k],b[k],path+"/"+k,out)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): out.append(("LEN",path,len(a),len(b)))
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,f"{path}[{i}]",out)
    else:
        if a!=b: out.append(("DIF",path))
res={}
for esc in ["B_REDUZIDO","B_AMPLIADO_D64"]:
    f11=f"{PK}/rascunho_prereg_v11/PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_{esc}.json"
    f12=f"{PK}/rascunho_prereg_v12/PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_{esc}.json"
    a=json.load(open(f11,encoding="utf-8")); b=json.load(open(f12,encoding="utf-8"))
    out=[]; walk(a,b,"",out)
    print("=====",esc,"sha v11",hashlib.sha256(open(f11,'rb').read()).hexdigest()[:16],"v12",hashlib.sha256(open(f12,'rb').read()).hexdigest()[:16])
    for o in out: print("  ",o)
    res[esc]=out
# MD shas
for esc in ["B_REDUZIDO","B_AMPLIADO_D64"]:
    for v in ["v11","v12"]:
        f=f"{PK}/rascunho_prereg_{v}/PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_{esc}.md"
        print(v,esc,"md",hashlib.sha256(open(f,'rb').read()).hexdigest())
    for v in ["v11","v12"]:
        f=f"{PK}/rascunho_prereg_{v}/PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_{esc}.json"
        print(v,esc,"json",hashlib.sha256(open(f,'rb').read()).hexdigest())
for v in ["v11","v12"]:
    f=f"{PK}/rascunho_prereg_{v}/gerar_preregistro_pilar_quantico_03out.py"
    print(v,"gerador",hashlib.sha256(open(f,'rb').read()).hexdigest())
