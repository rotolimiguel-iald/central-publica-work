import fitz, numpy as np
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
d=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf"); dpi=600; sc=dpi/72
for pi in (1,3,4,7):
    pg=d[pi]; pm=pg.get_pixmap(dpi=dpi,colorspace=fitz.csGRAY); a=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines",[]):
            for s in l["spans"]:
                if "STIX" in s["font"]:
                    x0,y0,x1,y1=s["bbox"]; ox,oy=s["origin"]
                    ys0=int((oy-1.0*s["size"])*sc); ys1=int((oy+0.2*s["size"])*sc)
                    sub=a[ys0:ys1,int(x0*sc):int(x1*sc)]<128
                    rows=np.where(sub.any(1))[0]; cols=np.where(sub.any(0))[0]
                    print("page",pi+1,repr(s["text"]),"ink rows",round((rows.max()-rows.min()+1)/sc*2.54/72*72/2.54*0+ (rows.max()-rows.min()+1)/dpi*2.54,3),"cm")
