import fitz, numpy as np, difflib
from scipy import ndimage
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
new=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf"); old=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf.bak_20261027_103927")
var=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf"); alt=fitz.open(W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf")
def raster(pg,dpi=300):
    pm=pg.get_pixmap(dpi=dpi,colorspace=fitz.csGRAY); return np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)
print("== R2 backup -> R3 main, per sheet: text diff and pixel diff (300 dpi)")
for i in range(6):
    ta=old[i].get_text().split("\n"); tb=new[i].get_text().split("\n")
    td=[x for x in difflib.unified_diff(ta,tb,lineterm="",n=0) if not x.startswith(("---","+++","@@"))]
    A=raster(old[i])<128; B=raster(new[i])<128; d=A^B
    lab,n=ndimage.label(ndimage.binary_dilation(d,iterations=8))
    H=old[i].rect.height
    cl=[(int(d[sl].sum()),tuple(round(v/300*72) for v in (sl[1].start,sl[1].stop,sl[0].start,sl[0].stop))) for sl in ndimage.find_objects(lab)]
    print(" sheet",i+1,"text diff:",td if td else "none","| pixel-diff px",int(d.sum()),"clusters (px,(x0,x1,y0,y1)pt):",cl[:6])
print("== VARIANTE_PHOT vs main: sheets 2-6 text and pixels")
for i in range(1,6):
    same_t = var[i].get_text()==new[i].get_text()
    pa=raster(var[i],300); pb=raster(new[i],300)
    print(" sheet",i+1,"text identical:",same_t,"| pixels identical at 300 dpi:",bool(np.array_equal(pa,pb)),"| drawings identical count:",len(var[i].get_drawings())==len(new[i].get_drawings()))
print("== VARIANTE sheet 1 vs ALTERNATIVA sheet 1:",var[0].get_text()==alt[0].get_text(),bool(np.array_equal(raster(var[0],300),raster(alt[0],300))))
print("== main sheet 1 vs variant sheet 1 text diff:",[x for x in difflib.unified_diff(new[0].get_text().split("\n"),var[0].get_text().split("\n"),lineterm="",n=0) if not x.startswith(("---","+++","@@"))])
# raw content-stream bytes of sheets 2-6
import hashlib
def cs(pg,doc): 
    return hashlib.sha256(b"".join(doc.xref_stream(x) for x in pg.get_contents())).hexdigest()[:12]
print("content-stream hashes sheets 2-6 main vs variant:",[(cs(new[i],new),cs(var[i],var)) for i in range(1,6)])
print("variant pages:",len(var),"size",var[0].rect, "A4?", abs(var[0].rect.width-595.28)<0.1)
