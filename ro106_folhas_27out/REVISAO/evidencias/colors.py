import fitz, collections, sys
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    for i,pg in enumerate(d):
        cs=collections.Counter(); fs=collections.Counter(); ops=collections.Counter(); widths=collections.Counter(); tcol=collections.Counter()
        for dr in pg.get_drawings():
            cs[("stroke",dr.get("color"))]+=1 if dr.get("color") is not None else 0
            fs[("fill",dr.get("fill"))]+=1 if dr.get("fill") is not None else 0
            if dr.get("color") is not None and dr.get("type") in ("s","fs"): widths[round(dr.get("width") or 0,3)]+=1
            if dr.get("fill_opacity") not in (None,1) or dr.get("stroke_opacity") not in (None,1): ops[(dr.get("fill_opacity"),dr.get("stroke_opacity"))]+=1
        for b in pg.get_text("dict")["blocks"]:
            for l in b.get("lines",[]):
                for s in l["spans"]: tcol[s["color"]]+=1
        print(n,"p",i+1,"stroke",{k[1]:v for k,v in cs.items() if v},"fill",{k[1]:v for k,v in fs.items() if v},"opac",dict(ops),"textcolors",dict(tcol))
