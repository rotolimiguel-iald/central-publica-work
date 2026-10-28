import fitz, numpy as np, sys
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
files={"apr":W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf","aprALT":W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf","mqc":W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf"}
dpi=600; sc=dpi/72
for k,p in files.items():
    O=fitz.open(p); T=fitz.open(p); G=fitz.open(p)
    for pg in T:
        pg.add_redact_annot(pg.rect); pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED,text=fitz.PDF_REDACT_TEXT_NONE)
    for pg in G:
        pg.add_redact_annot(pg.rect); pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,graphics=fitz.PDF_REDACT_LINE_ART_NONE,text=fitz.PDF_REDACT_TEXT_REMOVE)
    for i in range(len(O)):
        pt=T[i].get_pixmap(dpi=dpi,colorspace=fitz.csGRAY); pgx=G[i].get_pixmap(dpi=dpi,colorspace=fitz.csGRAY)
        Tm=np.frombuffer(pt.samples,dtype=np.uint8).reshape(pt.h,pt.w)<128
        Gm=np.frombuffer(pgx.samples,dtype=np.uint8).reshape(pgx.h,pgx.w)<128
        hits=[]
        for w in O[i].get_text("words"):
            x0,y0,x1,y1,txt=w[:5]
            xs0,xs1=int(x0*sc)-1,int(x1*sc)+1; ys0,ys1=int(y0*sc)-1,int(y1*sc)+1
            sub=Tm[ys0:ys1,xs0:xs1]
            if not sub.any(): continue
            rows=np.where(sub.any(1))[0]; cols=np.where(sub.any(0))[0]
            bx0,bx1=xs0+cols.min(),xs0+cols.max(); by0,by1=ys0+rows.min(),ys0+rows.max()
            # strict: graphics ink INSIDE the tight ink bbox (pad 0)  and near (pad 3px = 0.13 mm)
            inside=int(Gm[by0:by1+1,bx0:bx1+1].sum()); near=int(Gm[max(by0-3,0):by1+4,max(bx0-3,0):bx1+4].sum())
            if near>0: hits.append((txt,inside,near,(round(x0,1),round(y0,1))))
        print(k,"sheet",i+1,"words",len(O[i].get_text('words')),"words with graphics ink within 0.13mm of the text ink:",len(hits),hits[:8])
