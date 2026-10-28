import fitz, numpy as np, sys
from PIL import Image
p=r"C:\IALD\Central de Patentes\EPCT\BR102026003460-6_MQC\RECIBOS\DOCUMENTOS_OFICIAIS_WIPO_20261004\PCTBR2026050579-appb-000003-pt-20261004.pdf"
d=fitz.open(p)
def imgs(i):
    pg=d[i]; items=[]
    for x in pg.get_images(full=True):
        r=pg.get_image_rects(x[0])[0]
        pm=fitz.Pixmap(d,x[0])
        a=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)
        items.append((r.y0,a))
    items.sort(key=lambda t:t[0]); return [a for _,a in items]
sheet2=imgs(20); sheet3=imgs(21)
F={4:sheet2[0],5:sheet2[1],6:sheet2[2],7:sheet3[0],8:sheet3[1]}
for k,a in F.items():
    Image.fromarray(a).save(f"filedraw_fig{k}.png")
    print(k,a.shape)
    dark=a<150
    H,W=a.shape
    # vertical lines: columns with long run of dark
    colsum=dark.sum(0); rowsum=dark.sum(1)
    vx=[x for x in range(W) if colsum[x]>0.45*H]
    hy=[y for y in range(H) if rowsum[y]>0.15*W]
    def groups(v):
        g=[];s=None;pr=None
        for x in v:
            if s is None: s=x
            elif x!=pr+1: g.append((s,pr)); s=x
            pr=x
        if s is not None: g.append((s,pr))
        return g
    print("  vertical-lines",groups(vx)); print("  horizontal-lines",groups(hy))
