import fitz, numpy as np, re, json, sys
fitz.TOOLS.set_aa_level(0)   # fresh process: no AA before any render
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
files={"apr":W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf","aprALT":W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf","mqc":W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf"}
out={}
for k,p in files.items():
    d=fitz.open(p); N=len(d); rows=[]
    tot_nonbw=0
    for i,pg in enumerate(d):
        dpi=600
        pm=pg.get_pixmap(matrix=fitz.Matrix(dpi/72,dpi/72),colorspace=fitz.csRGB,alpha=False)
        b=np.frombuffer(pm.samples,dtype=np.uint8).reshape(-1,3)
        nonbw=int((~(((b==0).all(1))|((b==255).all(1)))).sum()); tot_nonbw+=nonbw
        g=b[:,0].reshape(pm.h,pm.w)
        ink=g<128; ys,xs=np.where(ink)
        cm=lambda px:px/dpi*2.54
        m=dict(left=cm(xs.min()),top=cm(ys.min()),right=cm(pm.w-1-xs.max()),bottom=cm(pm.h-1-ys.max()))
        # sheet number
        words=pg.get_text("words"); num=[w for w in words if re.fullmatch(r"\d+/\d+",w[4])]
        nn=[(w[4],round(((w[0]+w[2])/2-pg.rect.width/2)/72*25.4,2),round(w[1]/72*2.54,2)) for w in num]
        # colors in vector
        cols=set()
        for dr in pg.get_drawings():
            for c in (dr.get("color"),dr.get("fill")):
                if c is not None: cols.add(tuple(round(x,2) for x in c))
        # frames
        ux0,uy0,ux1,uy1=2.5/2.54*72,2.5/2.54*72,pg.rect.width-1.5/2.54*72,pg.rect.height-1.0/2.54*72
        big=[r for r in (dr["rect"] for dr in pg.get_drawings() if dr["type"] in("s","fs")) if r.width>0.85*(ux1-ux0) and r.height>0.65*(uy1-uy0)]
        rows.append(dict(sheet=i+1,size_cm=(round(pg.rect.width/72*2.54,2),round(pg.rect.height/72*2.54,2)),rot=pg.rotation,
            margins={a:round(float(v),3) for a,v in m.items()},ok_margins=bool(m["left"]>=2.5 and m["top"]>=2.5 and m["right"]>=1.5 and m["bottom"]>=1.0),
            nonbw_px=nonbw,images=len(pg.get_images()),vector_colors=sorted(cols),sheetno=nn,frames=len(big),
            figs=[int(x) for x in re.findall(r"Figura\s+(\d+)",pg.get_text())]))
    out[k]=rows
    print(k,"sheets",N,"total non-BW px",tot_nonbw)
    for r in rows: print("  ",r)
json.dump(out,open("reg.json","w"),indent=1,default=str)
