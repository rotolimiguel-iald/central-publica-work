import fitz, collections
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    for i,pg in enumerate(d):
        c=collections.Counter(); dash=collections.Counter()
        for dr in pg.get_drawings():
            if dr.get("color") is not None and dr["type"] in ("s","fs"):
                w=round(dr["width"] or 0,3)
                c[w]+=1
                if dr.get("dashes") and dr["dashes"]!="[] 0": dash[(w,dr["dashes"])]+=1
        print(n,"p",i+1,"stroke widths pt:",dict(sorted(c.items())))
        print("     dashed:",dict(dash))
