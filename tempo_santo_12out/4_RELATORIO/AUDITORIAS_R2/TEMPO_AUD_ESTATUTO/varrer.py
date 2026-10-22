import re,json,os,glob
base=r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
files=[os.path.join(base,p) for p in [
 r"3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.lean",
 r"3_KERNEL\rodada_2\RESULTADO_KERNEL.json",
 r"3_KERNEL\rodada_2\ACHADOS_FORA_DO_PREREGISTRO.json",
 r"2_OPTICO\rodada_2\RESULTADO_OPTICO.json",
 r"2_OPTICO\rodada_2\ACHADOS_FORA_DO_PREREGISTRO.json",
 r"2_OPTICO\rodada_2\run_optico.py",
 r"1_PREREGISTRO\PREREGISTRO.md",
 r"5_R2\0_ADENDO\ADENDO_R2.md",
 r"5_R2\2_REENSAIO\RESULTADO_REENSAIO_R2.json",
 r"4_RELATORIO\RELATORIO_FINAL.md"]]
pats={"CONFIRMED":r"CONFIRMED","confirmad":r"confirmad[ao]","nao_provou":r"n[ãa]o provou","pos_dicao":r"p[óo]s-?di[çc][ãa]o","beta_medido":r"(β|beta)[^.\n]{0,40}medid|medid[oa][^.\n]{0,40}(β|beta)","provado":r"\bprovad[ao]s?\b","PROVED":r"\bPROVED\b"}
out={}
for f in files:
    try: t=open(f,encoding='utf-8',errors='replace').read()
    except Exception as e: out[f]=str(e); continue
    r={}
    for k,p in pats.items():
        ms=[m for m in re.finditer(p,t)]
        if ms:
            r[k]={"n":len(ms),"ex":[t[max(0,m.start()-80):m.end()+60].replace("\n"," ") for m in ms[:4]]}
    out[os.path.relpath(f,base)]=r
json.dump(out,open("VARREDURA_PALAVRAS_AUD.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for f,r in out.items():
    print("==",f)
    if isinstance(r,str): print(r); continue
    for k,v in r.items():
        print(" ",k,v["n"])
        for e in v["ex"]: print("     ",e[:200])
