import fitz, numpy as np, re
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
def measure(pdf, fontfilter=None, dpi=600):
    d=fitz.open(pdf); out=[]; sizes=[]
    for pi in range(len(d)):
        pg=d[pi]
        pm=pg.get_pixmap(dpi=dpi,colorspace=fitz.csGRAY)
        a=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w); sc=dpi/72
        for b in pg.get_text("dict")["blocks"]:
            for l in b.get("lines",[]):
                for s in l["spans"]:
                    if s["text"].strip(): sizes.append(s["size"])
                if abs(l["dir"][0]-1)>1e-3: continue
                for s in l["spans"]:
                    t=s["text"].strip()
                    if not t or not re.fullmatch(r"[0-9]+",t): continue
                    x0,y0,x1,y1=s["bbox"]; ox,oy=s["origin"]
                    ys0=int((oy-0.9*s["size"])*sc); ys1=int((oy+0.08*s["size"])*sc)
                    sub=a[ys0:ys1,int(x0*sc)+1:int(x1*sc)-1]<128
                    rows=np.where(sub.any(1))[0]
                    if len(rows)==0: continue
                    out.append((pi+1,t,s["font"],round(s["size"],2),(rows.max()-rows.min()+1)/dpi*2.54))
    return out,sizes
for name,p in (("apr",W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf"),("aprALT",W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf"),("mqc",W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf")):
    r,sz=measure(p)
    print(name,"digit-only horizontal spans:",len(r),"min height cm",round(min(t[-1] for t in r),3) if r else None,"| min text span size pt",round(min(sz),2),"max",round(max(sz),2))
