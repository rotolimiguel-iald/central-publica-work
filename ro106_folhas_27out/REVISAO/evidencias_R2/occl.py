# Independent occlusion test: replicate vector graphics (strokes + fills) of each sheet in a scratch page twice:
# A = as painted (white fills kept), B = white fills removed. Ink in B and not in A = ink hidden by white fills.
import fitz, numpy as np, sys, json
from scipy import ndimage
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
DPI=300
def replicate(pg, drop_white):
    doc=fitz.open(); np_=doc.new_page(width=pg.rect.width,height=pg.rect.height)
    sh=np_.new_shape()
    for dr in pg.get_drawings():
        fill=dr.get("fill"); color=dr.get("color")
        if drop_white and fill is not None and tuple(round(x,2) for x in fill)==(1.0,1.0,1.0): fill=None
        if drop_white and fill is None and color is None: continue
        dashes=dr.get("dashes")
        if dashes in (None,"[] 0"): dashes=None
        w=dr.get("width") or 0.0
        any_item=False
        for it in dr["items"]:
            k=it[0]
            if k=="l": sh.draw_line(it[1],it[2])
            elif k=="c": sh.draw_bezier(it[1],it[2],it[3],it[4])
            elif k=="re": sh.draw_rect(it[1])
            elif k=="qu": sh.draw_quad(it[1])
            any_item=True
        if any_item:
            sh.finish(fill=fill,color=color,width=w if color is not None else 0,dashes=dashes,closePath=bool(dr.get("closePath")),even_odd=bool(dr.get("even_odd")),lineCap=0 if dr.get("lineCap") is None else (dr["lineCap"][0] if isinstance(dr["lineCap"],(list,tuple)) else dr["lineCap"]))
    sh.commit()
    return doc
def ink(doc):
    pm=doc[0].get_pixmap(dpi=DPI,colorspace=fitz.csGRAY)
    return (np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)<128)
def run(path,label,pages=None):
    d=fitz.open(path); res=[]
    for i,pg in enumerate(d):
        if pages and (i+1) not in pages: continue
        A=ink(replicate(pg,False)); B=ink(replicate(pg,True))
        hidden=B & ~A
        # ignore single-pixel antialias/registration noise: erode-open
        hidden=ndimage.binary_opening(hidden,structure=np.ones((2,2)))
        lab,n=ndimage.label(hidden,structure=np.ones((3,3)))
        comps=[]
        for j,sl in enumerate(ndimage.find_objects(lab)):
            area=int((lab[sl]==j+1).sum())
            h=(sl[0].stop-sl[0].start)/DPI*2.54; w=(sl[1].stop-sl[1].start)/DPI*2.54
            if area<12: continue
            comps.append((area,round(w,2),round(h,2),(round(sl[1].start/DPI*2.54,1),round(sl[0].start/DPI*2.54,1))))
        big=[c for c in comps if max(c[1],c[2])>0.45]    # >0.45 cm: not a marker face
        small=[c for c in comps if max(c[1],c[2])<=0.45]
        res.append((i+1,int(hidden.sum()),len(big),len(small),sorted(big,reverse=True)[:6]))
        print(label,"sheet",i+1,"hidden-ink px",int(hidden.sum()),"| components >0.45cm:",len(big),"| marker-sized:",len(small),big[:6])
    return res
if __name__=="__main__":
    which=sys.argv[1]
    if which=="apr_before": run(W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf.bak_20261027_094406","apr_R1")
    if which=="apr": run(W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf","apr_R2")
    if which=="alt": run(W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf","aprALT_R2")
    if which=="mqc_before": run(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf.bak_20261027_094406","mqc_R1")
    if which=="mqc": run(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf","mqc_R2")
