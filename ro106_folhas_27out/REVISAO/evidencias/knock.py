import fitz, numpy as np
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
def seg_in_rect(p,q,r,n=12):
    for t in np.linspace(0,1,n):
        x=p.x+(q.x-p.x)*t; y=p.y+(q.y-p.y)*t
        if r.x0<x<r.x1 and r.y0<y<r.y1: return True
    return False
def stroke_pts(dr):
    segs=[]
    for it in dr["items"]:
        if it[0]=="l": segs.append((it[1],it[2]))
        elif it[0]=="c": segs.append((it[1],it[4]))
        elif it[0]=="re":
            r=it[1]; 
            for a,b in ((r.tl,r.tr),(r.tr,r.br),(r.br,r.bl),(r.bl,r.tl)): segs.append((a,b))
        elif it[0]=="qu":
            q=it[1]
            for a,b in ((q.ul,q.ur),(q.ur,q.lr),(q.lr,q.ll),(q.ll,q.ul)): segs.append((a,b))
    return segs
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    for i,pg in enumerate(d):
        drs=pg.get_drawings()
        whites=[(k,dr) for k,dr in enumerate(drs) if dr.get("fill")==(1.0,1.0,1.0) and dr["rect"].width>3 and dr["rect"].height>3 and dr["rect"].width*dr["rect"].height<600*800*0.2]
        out=[]
        for k,wdr in whites:
            r=wdr["rect"]
            rr=fitz.Rect(r.x0+0.3,r.y0+0.3,r.x1-0.3,r.y1-0.3)
            hit=0
            for k2,dr in enumerate(drs):
                if k2>=k: break
                if dr.get("color") is None or dr["type"] not in ("s","fs"): continue
                if not dr["rect"].intersects(rr): continue
                if any(seg_in_rect(a,b,rr) for a,b in stroke_pts(dr)): hit+=1
            if hit: out.append((tuple(round(x) for x in r),hit,wdr.get("color")))
        print(n,"sheet",i+1,"white fills covering earlier strokes:",len(out),out[:8])
