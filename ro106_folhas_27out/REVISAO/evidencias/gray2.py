import fitz, numpy as np, sys
fitz.TOOLS.set_aa_level(0)
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    for dpi in (600,):
        tot=[]
        for i,pg in enumerate(d):
            fitz.TOOLS.store_shrink(100)  # clear caches
            pix=pg.get_pixmap(matrix=fitz.Matrix(dpi/72,dpi/72),colorspace=fitz.csGRAY,alpha=False)
            a=np.frombuffer(pix.samples,dtype=np.uint8)
            tot.append(int(((a>0)&(a<255)).sum()))
            # RGB too, in case of colour
            pix3=pg.get_pixmap(matrix=fitz.Matrix(dpi/72,dpi/72),colorspace=fitz.csRGB,alpha=False)
            b=np.frombuffer(pix3.samples,dtype=np.uint8).reshape(-1,3)
            nonbw=int((~(((b==0).all(1))|((b==255).all(1)))).sum())
            tot[-1]=(tot[-1],nonbw)
        print(n,dpi,"(gray_in_gray, non-BW in RGB) per page:",tot)
