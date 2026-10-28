import fitz, numpy as np, json, sys
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
sc=sys.argv[1]
out={}
for n in ("050576","050579"):
    d=fitz.open(f"{W}\FOLHAS_SUBSTITUTIVAS_{n}.pdf")
    res=[]
    for i,pg in enumerate(d):
        # 600 dpi, no antialias
        mat=fitz.Matrix(600/72,600/72)
        pix=pg.get_pixmap(matrix=mat,colorspace=fitz.csGRAY,alpha=False)
        fitz.TOOLS.set_aa_level(0)
        pix0=pg.get_pixmap(matrix=mat,colorspace=fitz.csGRAY,alpha=False)
        fitz.TOOLS.set_aa_level(8)
        a=np.frombuffer(pix0.samples,dtype=np.uint8).reshape(pix0.h,pix0.w)
        a8=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.h,pix.w)
        gray0=int(((a>0)&(a<255)).sum())
        gray_aa=int(((a8>0)&(a8<255)).sum())
        ink=a<128
        ys,xs=np.where(ink)
        dpi=600; cm=lambda px:px/dpi*2.54
        H,Wd=a.shape
        bbox=(cm(xs.min()),cm(ys.min()),cm(Wd-xs.max()),cm(H-ys.max()))  # left, top, right, bottom margins in cm
        res.append(dict(page=i+1,size_cm=(round(Wd/dpi*2.54,3),round(H/dpi*2.54,3)),margin_left=round(bbox[0],3),margin_top=round(bbox[1],3),margin_right=round(bbox[2],3),margin_bottom=round(bbox[3],3),gray_noaa=gray0,gray_aa=gray_aa,inkpix=int(ink.sum())))
        pg2=pg.get_pixmap(dpi=300); pg2.save(f"{sc}/new_{n}_p{i+1}.png")
        # also save a 600dpi png? skip
    out[n]=res
    for r in res: print(n,r)
json.dump(out,open(f"{sc}/measure_independent.json","w"),indent=1)
