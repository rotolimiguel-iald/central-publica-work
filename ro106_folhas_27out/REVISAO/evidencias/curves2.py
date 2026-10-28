import fitz, numpy as np
from PIL import Image
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_050579.pdf")
def poly_pts(pg, bbox_match):
    best=None
    for dr in pg.get_drawings():
        r=dr["rect"]
        if all(abs(a-b)<2 for a,b in zip((r.x0,r.y0,r.x1,r.y1),bbox_match)):
            pts=[]
            for it in dr["items"]:
                if it[0]=="l": pts+=[it[1],it[2]]
                elif it[0]=="c": pts+=[it[1],it[4]]
            if len(pts)>40: best=pts
    return np.array([(p.x,p.y) for p in best])
def filed_curve(arr, x0,x1,y0,y1, thr=150):
    sub=arr[y0:y1,x0:x1]
    dark=sub<thr
    cols=np.where(dark.any(0))[0]
    ys=np.full(sub.shape[1],np.nan)
    for c in cols:
        rows=np.where(dark[:,c])[0]
        ys[c]=rows.mean()
    xs=np.arange(sub.shape[1])
    ok=~np.isnan(ys)
    return xs[ok],ys[ok]
def norm_resample(xs,ys,flip,n=200):
    x=(xs-xs.min())/(xs.max()-xs.min())
    if flip: ys=-ys
    y=(ys-ys.min())/(ys.max()-ys.min())
    g=np.linspace(0,1,n)
    # average duplicates by sorting
    o=np.argsort(x); x=x[o]; y=y[o]
    return g,np.interp(g,x,y)
res={}
# --- Fig 5(c): filed panel 3 interior
a5=np.array(Image.open("filedraw_fig5.png"))
xs,ys=filed_curve(a5,3424,4738,159,1250)
print("filed 5c curve px",len(xs),xs.min(),xs.max(),ys.min(),ys.max())
pg=d[4]; P=poly_pts(pg,(182,568,527,694))
g,fy=norm_resample(xs,ys,True); g2,ny=norm_resample(P[:,0],P[:,1],True)
print("Fig5(c) corr",np.corrcoef(fy,ny)[0,1],"mean abs diff",np.abs(fy-ny).mean(),"max",np.abs(fy-ny).max())
# --- Fig 6(a): filed panel 1 interior; the dashed 12 line and legend present in filed? use only curve dark; first check
a6=np.array(Image.open("filedraw_fig6.png"))
print(a6.shape)
