import fitz, numpy as np
fitz.TOOLS.set_aa_level(0)
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
files={"apr":W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf","aprALT":W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf","mqc":W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf"}
dpi=300; mm=lambda v:int(round(v/25.4*dpi))
for k,p in files.items():
    d=fitz.open(p); out=[]
    for i,pg in enumerate(d):
        pm=pg.get_pixmap(dpi=dpi,colorspace=fitz.csGRAY); a=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)<128
        r=a[:,mm(120):]               # right strip from 120 mm
        ys=np.where(r.any(1))[0]; top=ys.min()/dpi*25.4 if len(ys) else None
        s=a[mm(105):mm(120),:mm(40)]  # nothing
        # ink between 110 and 120 mm above 35 mm (the sheet number spans ~100-110 mm)
        mid=a[:mm(35),mm(112):mm(120)]
        out.append((i+1,round(top,1) if top is not None else None,int(mid.sum()), int(a[mm(287):,:].sum())))
    print(k,"(sheet, topmost ink y in mm within x>=120mm, ink px in x112-120mm y<35mm, ink px bottom 10mm):",out)
