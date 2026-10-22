import json,math,sys
sys.stdout.reconfigure(encoding='utf-8')
MINE=r"optico\saida\tentativas\tentativa_001_ensaio\RESULTADO_OPTICO.json"
R2=r"C:\IALD\Central de Patentes\work\tempo_santo_12out\2_OPTICO\rodada_2\RESULTADO_OPTICO.json"
R1=r"C:\IALD\Central de Patentes\work\tempo_santo_12out\2_OPTICO\RESULTADO_OPTICO.json"
A=json.load(open(MINE,encoding='utf-8')); B=json.load(open(R2,encoding='utf-8')); C=json.load(open(R1,encoding='utf-8'))
SKIP={'inicio_utc','fim_utc','segundos','pasta_da_tentativa','tentativa','arquivo','copia','ambiente','runner','script_impressao_digital','anexo_achados_fora_do_preregistro'}
def walk(a,b,path,diffs,nums):
    if isinstance(a,dict) and isinstance(b,dict):
        for k in set(a)|set(b):
            if k in SKIP: continue
            if k not in a or k not in b: diffs.append((path+"/"+k,"MISSING_ONE_SIDE")); continue
            walk(a[k],b[k],path+"/"+k,diffs,nums)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): diffs.append((path,"LEN %d vs %d"%(len(a),len(b)))); return
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,path+"[%d]"%i,diffs,nums)
    elif isinstance(a,(int,float)) and not isinstance(a,bool) and isinstance(b,(int,float)) and not isinstance(b,bool):
        nums[0]+=1
        if a!=b:
            rel=abs(a-b)/max(1e-300,abs(b)); diffs.append((path,a,b,rel))
    else:
        if a!=b and not (isinstance(a,str) and ("Temp" in a or "tempo_santo" in a or "T" in a and ":" in a and len(a)<40 and a.count("-")>=2)):
            if isinstance(a,str) and isinstance(b,str) and len(a)>60 and len(b)>60: diffs.append((path,"STR_DIFF",a[:60],b[:60]))
            else: diffs.append((path,"VAL_DIFF",a,b))
for name,other in (("r2",B),("r1",C)):
    for sec in ("subitens_oticos","controles_oticos","por_afirmacao_face_otica","modelo","beta","autotestes","controles_oticos_todos_como_registrado","valido"):
        if sec not in A or sec not in other: print(name,sec,"ausente em um lado"); continue
        d=[];n=[0]; walk(A[sec],other[sec],sec,d,n)
        print(f"== mine vs {name} / {sec}: numeros comparados={n[0]} diferencas={len(d)}")
        for x in d[:25]: print("   ",x)
# key numbers
def g(R,*ks):
    x=R
    for k in ks: x=x[k]
    return x
for sub in ("T9.o",):
    for name,R in (("mine",A),("r2",B),("r1",C)):
        s=R["subitens_oticos"][sub]
        crit=[c for c in s.get("criterios",[]) if "matrix_power" in json.dumps(c) or "(c)" in c.get("nome","")]
        print(name,sub,json.dumps(crit,ensure_ascii=False)[:400])
