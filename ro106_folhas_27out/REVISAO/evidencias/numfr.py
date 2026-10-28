import fitz, re
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    N=len(d); figs=[]
    for i,pg in enumerate(d):
        cx=pg.rect.width/2
        words=pg.get_text("words")
        num=[w for w in words if re.fullmatch(r"\d+/\d+",w[4])]
        fg=[w[4] for w in words if False]
        txt=pg.get_text()
        figlist=re.findall(r"Figura\s+(\d+)",txt)
        figs+= [int(x) for x in figlist]
        for w in num:
            xc=(w[0]+w[2])/2; yt=w[1]
            print(n,"sheet",i+1,"label",w[4],"centre offset (mm)",round((xc-cx)/72*25.4,2),"bbox top (cm from edge)",round(w[1]/72*2.54,2),"bottom",round(w[3]/72*2.54,2),"expected",f"{i+1}/{N}", "OK" if w[4]==f"{i+1}/{N}" else "MISMATCH")
        # frames: any stroked rect/path whose bbox covers > 80% of usable area
        ux0,uy0,ux1,uy1=2.5/2.54*72,2.5/2.54*72,pg.rect.width-1.5/2.54*72,pg.rect.height-1.0/2.54*72
        big=[]
        for dr in pg.get_drawings():
            r=dr["rect"]
            if dr["type"] in ("s","fs") and r.width>0.85*(ux1-ux0) and r.height>0.65*(uy1-uy0): big.append(tuple(round(x) for x in r))
        print("    figures on sheet:",figlist,"large (>85% w, >65% h of usable) stroked shapes:",big)
    print(n,"figure sequence:",figs)
