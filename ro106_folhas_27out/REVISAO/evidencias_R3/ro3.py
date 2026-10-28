import fitz, numpy as np
fitz.TOOLS.set_aa_level(0)
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
files={"apr":W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf","aprALT":W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf","variante":W+r"\FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf"}
dpi=300
for k,p in files.items():
    d=fitz.open(p); res=[]
    for i,pg in enumerate(d):
        pm=pg.get_pixmap(dpi=dpi,colorspace=fitz.csGRAY); a=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)<128
        mm=lambda v:int(round(v/25.4*dpi))
        areas={"canto sup. dir. x>=105mm,y<=40mm":a[:mm(40),mm(105):],
               "canto sup. dir. x>=120mm,y<=35mm":a[:mm(35),mm(120):],
               "margem superior y<25mm":a[:mm(25),:],
               "margem inferior y>=287mm":a[mm(287):,:],
               "margem direita x>=195mm":a[:,mm(195):]}
        res.append((i+1,{n:int(v.sum()) for n,v in areas.items()}))
    free=all(all(c==0 for c in r[1].values()) for r in res)
    print(k,"ALL FREE" if free else "OCCUPIED",[ (r[0],{n:c for n,c in r[1].items() if c}) for r in res if any(r[1].values())])
