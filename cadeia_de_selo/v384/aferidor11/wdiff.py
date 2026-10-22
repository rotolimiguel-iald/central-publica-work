import difflib,sys,io
PK=sys.argv[1]
for esc in ["B_REDUZIDO","B_AMPLIADO_D64"]:
    a=open(f"{PK}/rascunho_prereg_v11/PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_{esc}.md","rb").read().decode("utf-8").split("\n")
    b=open(f"{PK}/rascunho_prereg_v12/PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_{esc}.md","rb").read().decode("utf-8").split("\n")
    print("=====",esc,len(a),len(b))
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=="equal": continue
        print("--",op,i1+1,i2,j1+1,j2)
        for x,y in zip(a[i1:i2],b[j1:j2]):
            # word-level diff
            sw=difflib.SequenceMatcher(None,x,y,autojunk=False)
            for o,p1,p2,q1,q2 in sw.get_opcodes():
                if o=="equal": continue
                print(f"   [{o}] OLD: ...{x[max(0,p1-80):p2+80]}...")
                print(f"         NEW: ...{y[max(0,q1-80):q2+80]}...")
