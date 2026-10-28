import fitz, numpy as np, json, sys
from scipy import ndimage
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
doc=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf")
FR={5:[(214,1536,101,1310),(1817,3139,101,1310),(3420,4742,101,1310)],
    6:[(171,1539,125,1236),(1772,3139,125,1236),(3372,4740,125,1236)],
    7:[(237,2062,95,1300),(2316,4141,95,1300)]}
FIG={5:"5",6:"6",7:"7"}
def axes_rects(pg):
    rs=[dr["rect"] for dr in pg.get_drawings() if dr["type"]=="f" and dr.get("fill")==(1.0,1.0,1.0) and dr["rect"].width>300 and dr["rect"].height>100 and dr["rect"].height<300]
    rs=sorted(rs,key=lambda r:(round(r.y0/100),r.x0))
    return rs
def selected(pg,R):
    inn=fitz.Rect(R.x0+3,R.y0+3,R.x1-3,R.y1-3)
    drs=pg.get_drawings()
    legends=[dr["rect"] for dr in drs if dr["type"]=="fs" and dr.get("fill")==(1.0,1.0,1.0) and dr["rect"].width>60 and dr["rect"].height>20 and inn.contains(dr["rect"]) ]
    sel=[]
    for dr in drs:
        r=dr["rect"]
        if not inn.contains(r): continue
        if dr.get("fill")==(1.0,1.0,1.0) and dr.get("color") is None: continue
        da=dr.get("dashes")
        if da and da.startswith("[ .7 2.45"): continue      # dotted grid
        if any(L.contains(r) or L.intersects(r) and (r.width<L.width and r.height<L.height and L.contains(fitz.Point((r.x0+r.x1)/2,(r.y0+r.y1)/2))) for L in legends): continue
        if dr["type"]=="s" and dr.get("color")!=(0,0,0): continue
        sel.append(dr)
    return sel
def render_selected(pg,R,sel,size):
    d=fitz.open(); p=d.new_page(width=pg.rect.width,height=pg.rect.height); sh=p.new_shape()
    for dr in sel:
        for it in dr["items"]:
            k=it[0]
            if k=="l": sh.draw_line(it[1],it[2])
            elif k=="c": sh.draw_bezier(it[1],it[2],it[3],it[4])
            elif k=="re": sh.draw_rect(it[1])
            elif k=="qu": sh.draw_quad(it[1])
        dashes=dr.get("dashes"); dashes=None if dashes in (None,"[] 0") else dashes
        sh.finish(fill=dr.get("fill"),color=dr.get("color"),width=max(dr.get("width") or 0,1.0) if dr.get("color") is not None else 0,dashes=dashes,closePath=bool(dr.get("closePath")))
    sh.commit()
    w,h=size
    pm=p.get_pixmap(matrix=fitz.Matrix(w/R.width,h/R.height),clip=R,colorspace=fitz.csGRAY)
    a=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)
    m=a<128
    out=np.zeros((h,w),bool); hh=min(h,m.shape[0]); ww=min(w,m.shape[1]); out[:hh,:ww]=m[:hh,:ww]
    return out
def ncc(a,b,mask):
    a=a[mask]; b=b[mask]; a=a-a.mean(); b=b-b.mean()
    den=np.sqrt((a*a).sum()*(b*b).sum()); return float((a*b).sum()/den) if den>0 else 0.0
THR=int(sys.argv[1]) if len(sys.argv)>1 else 150
res={}
for sheet in (5,6,7):
    F=np.load(f"filed_fig{sheet}.npy"); pg=doc[sheet-1]; rects=axes_rects(pg)
    print("sheet",sheet,"axes patches:",[tuple(round(x,1) for x in r) for r in rects])
    for idx,((x0,x1,y0,y1),R) in enumerate(zip(FR[sheet],rects)):
        sel=selected(pg,R)
        w,h=x1-x0,y1-y0
        Mn=render_selected(pg,R,sel,(w,h))
        Mf=F[y0:y1,x0:x1]<THR
        ins=6
        Mn[:ins,:]=0;Mn[-ins:,:]=0;Mn[:,:ins]=0;Mn[:,-ins:]=0
        Mf[:ins,:]=0;Mf[-ins:,:]=0;Mf[:,:ins]=0;Mf[:,-ins:]=0
        band=ndimage.binary_dilation(Mn,iterations=30)
        gn=ndimage.gaussian_filter(Mn.astype(float),4); 
        best=(-2,None)
        for dy in range(-14,15,2):
            for dx in range(-14,15,2):
                f2=np.roll(np.roll(Mf,dy,0),dx,1)
                gf=ndimage.gaussian_filter(f2.astype(float),4)
                c=ncc(gf,gn,band)
                if c>best[0]: best=(c,(dx,dy))
        c0=ncc(ndimage.gaussian_filter(Mf.astype(float),4),gn,band)
        # precision/recall at 8px tolerance
        dn=ndimage.binary_dilation(Mn,iterations=8); df=ndimage.binary_dilation(Mf,iterations=8)
        P=float((Mn&df).sum()/max(Mn.sum(),1)); Rr=float((Mf&band&dn).sum()/max((Mf&band).sum(),1))
        print(f"  fig {sheet} panel {'abc'[idx]}: drawings {len(sel)} | NCC unshifted {c0:.3f} | NCC best after alignment {best[0]:.3f} shift(px) {best[1]} | new-ink on filed ink (8px) {P:.3f} | filed-ink in band on new ink {Rr:.3f}")
        res[f"{sheet}{'abc'[idx]}"]=dict(ncc_unshifted=c0,ncc_aligned=best[0],shift=best[1],precision=P,recall=Rr)
json.dump(res,open("corr.json","w"),indent=1)
