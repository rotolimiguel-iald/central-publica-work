import importlib.util, numpy as np, fitz, os
from PIL import Image
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
p=r"C:\IALD\Central de Patentes\EPCT\BR102026003460-6_MQC\RECIBOS\DOCUMENTOS_OFICIAIS_WIPO_20261004\PCTBR2026050579-appb-000003-pt-20261004.pdf"
d=fitz.open(p); pg=d[20]; items=[]
for x in pg.get_images(full=True):
    r=pg.get_image_rects(x[0])[0]; pm=fitz.Pixmap(d,x[0]); items.append((r.y0,np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)))
items.sort(key=lambda t:t[0]); F=items[0][1]; print("filed fig4",F.shape)
# panel d frame: x in [1043,4135]; find horizontal frame lines within that x-range, below y=1270
dark=F<120
rows=dark[:,1060:4120].sum(1)
cand=[y for y in range(1200,F.shape[0]) if rows[y]>0.9*3060]
print("long horizontal lines for panel d (y):",cand[:6],cand[-6:])

# --- own regeneration of the data
os.chdir(os.environ.get("TEMP",r"C:\Windows\Temp"))
spec=importlib.util.spec_from_file_location("mqc_orig",W+r"\entrada\mqc\mqc_simulacao_celula_elementar.py"); m=importlib.util.module_from_spec(spec); import io,contextlib
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
dados=m.simular_translacao_holografica()
x=np.asarray(dados["alpha2_sweep"],float); y=np.asarray(dados["corr_sweep"],float)
x0,x1,yt,yb=2303,4135,1519,2703
xl=(x[0]-0.05*(x[-1]-x[0]), x[-1]+0.05*(x[-1]-x[0])); yl=(y.min()-0.05*(y.max()-y.min()), y.max()+0.05*(y.max()-y.min()))
def topx(v): return x0+(v-xl[0])/(xl[1]-xl[0])*(x1-x0)
def topy(v): return yb-(v-yl[0])/(yl[1]-yl[0])*(yb-yt)
# sample dense points along the polyline
xs=np.linspace(x[0],x[-1],1200); ys=np.interp(xs,x,y)
px=topx(xs); py=topy(ys)
dark=F<130
from scipy import ndimage
near=ndimage.binary_dilation(dark,iterations=8)
hit=np.array([near[int(round(b)),int(round(a))] for a,b in zip(px,py)])
inside_hidden=(xs>=0.00167)&(xs<=0.00225)
print("predicted-curve samples on filed dark ink (tolerance 8 px): outside hidden range %.1f%%  | inside hidden range %.1f%%"%(100*hit[~inside_hidden].mean(),100*hit[inside_hidden].mean()))
# restrict to samples away from the axvline x=0.012 and from frame clutter
mask=(~inside_hidden)&(np.abs(xs-0.012)>0.0004)
print("away from the vertical dash-dot line: %.1f%%"%(100*hit[mask].mean()))
# is the hidden stretch covered by a light (box) region in the filed raster? mean grey around the hidden samples
vals=[F[int(round(b))-3:int(round(b))+4,int(round(a))-3:int(round(a))+4].mean() for a,b in zip(px[inside_hidden],py[inside_hidden])]
print("mean grey of filed raster at the hidden stretch (255=white/box): %.0f"%np.mean(vals))
