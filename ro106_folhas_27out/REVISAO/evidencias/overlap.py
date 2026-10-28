import fitz, numpy as np, json, sys
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
dpi=600; sc=dpi/72
res={}
for n in ("050576","050579"):
    orig=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    to=fitz.open(f"textonly_{n}.pdf"); go=fitz.open(f"gonly_{n}.pdf")
    res[n]=[]
    for i in range(len(orig)):
        pt=to[i].get_pixmap(dpi=dpi,colorspace=fitz.csGRAY); pgx=go[i].get_pixmap(dpi=dpi,colorspace=fitz.csGRAY)
        T=np.frombuffer(pt.samples,dtype=np.uint8).reshape(pt.h,pt.w)<128
        G=np.frombuffer(pgx.samples,dtype=np.uint8).reshape(pgx.h,pgx.w)<128
        words=orig[i].get_text("words")
        hits=[]
        for w in words:
            x0,y0,x1,y1,txt=w[:5]
            xs0,xs1=int(x0*sc)-1,int(x1*sc)+1; ys0,ys1=int(y0*sc)-1,int(y1*sc)+1
            sub=T[ys0:ys1,xs0:xs1]
            if not sub.any(): continue
            rows=np.where(sub.any(1))[0]; cols=np.where(sub.any(0))[0]
            bx0,bx1=xs0+cols.min(),xs0+cols.max(); by0,by1=ys0+rows.min(),ys0+rows.max()
            pad=int(0.02*sc)  # ~0.7 mm? no: 0.02pt*8.3=0.17px -> use 3 px
            pad=3
            g=G[max(by0-pad,0):by1+pad+1, max(bx0-pad,0):bx1+pad+1]
            # exclude pixels that are part of the glyph ink itself? graphics-only has no glyphs.
            cnt=int(g.sum())
            if cnt>0: hits.append((txt,cnt,(round(x0,1),round(y0,1))))
        res[n].append(hits)
        print(n,"sheet",i+1,"words",len(words),"words with graphics ink within ink-bbox+3px:",len(hits))
        for h in sorted(hits,key=lambda t:-t[1])[:12]: print("    ",h)
