import fitz, io
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    seen=set()
    for i,pg in enumerate(d):
        for f in pg.get_fonts(full=True):
            xref=f[0]
            if xref in seen: continue
            seen.add(xref)
            try:
                name,ext,typ,buf=d.extract_font(xref)
            except Exception as e:
                print(n,xref,"extract fail",e); continue
            if not buf: print(n,xref,f[3],"no buffer"); continue
            try:
                tt=TTFont(io.BytesIO(buf),lazy=True)
            except Exception as e:
                print(n,xref,f[3],ext,"fontTools fail",str(e)[:60]); continue
            upem=tt["head"].unitsPerEm
            gs=tt.getGlyphSet()
            order=tt.getGlyphOrder()
            res={}
            cm=tt.getBestCmap() if "cmap" in tt else {}
            for ch in "H0123456789bdfhklEA":
                gn=cm.get(ord(ch)) if cm else None
                if gn and gn in gs:
                    bp=BoundsPen(gs); gs[gn].draw(bp)
                    if bp.bounds: res[ch]=round((bp.bounds[3]-bp.bounds[1])/upem,3)
            print(n,"font",f[3],ext,"upem",upem,"nglyphs",len(order),"glyph heights (em)",res)
