import fitz
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
d=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf")
for si in (3,4,5,6):
    pg=d[si]; drs=pg.get_drawings()
    legs=[(k,dr["rect"]) for k,dr in enumerate(drs) if dr.get("fill")==(1.0,1.0,1.0) and dr["type"] in ("fs","f") and dr["rect"].width>50 and dr["rect"].height>20 and dr["rect"].width<420]
    print("sheet",si+1,"candidate legend/text boxes:",[tuple(round(x) for x in r) for k,r in legs])
    for k,r in legs:
        for k2,dr in enumerate(drs[:k]):
            if dr["type"]!="s" or dr.get("color") is None: continue
            pts=[]
            for it in dr["items"]:
                if it[0]=="l": pts+=[it[1],it[2]]
                elif it[0]=="c": pts+=[it[1],it[4]]
            if len(pts)<15: continue
            inside=sum(1 for p in pts if r.x0<p.x<r.x1 and r.y0<p.y<r.y1)
            if inside: print(f"   box {tuple(round(x) for x in r)} hides {inside}/{len(pts)} pts of path bbox {tuple(round(x) for x in dr['rect'])} dashes={dr.get('dashes')}")
