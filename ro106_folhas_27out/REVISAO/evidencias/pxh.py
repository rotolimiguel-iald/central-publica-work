import fitz, numpy as np, re
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
def measure(pdf, pages, fontfilter=None, digits_only=True, dpi=600):
    d=fitz.open(pdf); out=[]
    for pi in pages:
        pg=d[pi]
        pm=pg.get_pixmap(dpi=dpi,colorspace=fitz.csGRAY)
        a=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)
        sc=dpi/72
        for b in pg.get_text("dict")["blocks"]:
            for l in b.get("lines",[]):
                if abs(l["dir"][0]-1)>1e-3: continue   # horizontal text only
                for s in l["spans"]:
                    t=s["text"].strip()
                    if not t or not re.fullmatch(r"[0-9]+",t): continue
                    if fontfilter and fontfilter not in s["font"]: continue
                    # tight search region: span bbox shrunk vertically to baseline region
                    x0,y0,x1,y1=s["bbox"]
                    ox,oy=s["origin"]
                    # digits extend from baseline up ~0.75*size; search from oy-0.9*size to oy+0.05*size
                    ys0=int((oy-0.9*s["size"])*sc); ys1=int((oy+0.08*s["size"])*sc)
                    xs0=int(x0*sc)+1; xs1=int(x1*sc)-1
                    sub=a[ys0:ys1,xs0:xs1]<128
                    rows=np.where(sub.any(1))[0]
                    if len(rows)==0: continue
                    h_px=rows.max()-rows.min()+1
                    out.append((pi+1,t,s["font"],round(s["size"],2),round(h_px/dpi*2.54,3)))
    return out
r=measure(W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf",range(6),"CMR12")
print("050576 CMR12 digit-only spans (page,text,font,size,height cm):")
hs=sorted(r,key=lambda t:t[-1])[:8]
for x in hs: print("  ",x)
print("  count",len(r),"min",min(t[-1] for t in r),"max",max(t[-1] for t in r))
r2=measure(W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf",range(6),"ArialNarrow")
print("050576 ArialNarrow digit spans: count",len(r2),"min",min(t[-1] for t in r2) if r2 else None)
r3=measure(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf",range(8),"Arial")
print("050579 ArialNarrow digit spans: count",len(r3),"min",min(t[-1] for t in r3),[x for x in sorted(r3,key=lambda t:t[-1])[:5]])
