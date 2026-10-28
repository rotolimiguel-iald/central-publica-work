import fitz, numpy as np
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
d=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf")
for i,pg in enumerate(d):
    drs=pg.get_drawings()
    # polylines = data
    polys=[]
    for k,dr in enumerate(drs):
        pts=[]
        for it in dr["items"]:
            if it[0]=="l": pts+= [it[1],it[2]]
            elif it[0]=="c": pts+=[it[1],it[4]]
        if len(pts)>=60 and dr.get("color") is not None and dr["type"]=="s": polys.append((k,pts,dr))
    # legend frames: white fill + black stroke with sizable rect
    legs=[(k,dr) for k,dr in enumerate(drs) if dr["type"]=="fs" and dr.get("fill")==(1.0,1.0,1.0) and dr["rect"].width>60 and dr["rect"].height>25 and dr["rect"].width<400]
    for k,dr in legs:
        r=dr["rect"]
        for kp,pts,pd in polys:
            if kp>=k: continue   # curve drawn before legend
            inside=sum(1 for p in pts if r.x0<p.x<r.x1 and r.y0<p.y<r.y1)
            tot=len(pts)
            if inside>0:
                # visible length hidden: fraction of points hidden
                print(f"sheet {i+1}: legend rect {tuple(round(x) for x in r)} hides {inside}/{tot} pts of data polyline bbox {tuple(round(x) for x in pd['rect'])} dashes {pd.get('dashes')} w={pd['width']}")
