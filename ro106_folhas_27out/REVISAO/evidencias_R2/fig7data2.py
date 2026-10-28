import importlib.util, io, contextlib, os, numpy as np, fitz
import matplotlib
matplotlib.use("Agg")
W = r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
RUN = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\r2\run"
os.makedirs(RUN, exist_ok=True)
os.chdir(RUN)
spec = importlib.util.spec_from_file_location("mqc_orig", W + r"\entrada\mqc\mqc_simulacao_celula_elementar.py")
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(m)
# main-flow order of the ORIGINAL script: figure functions 1..7 in sequence (random state carries over)
res = {}
with contextlib.redirect_stdout(io.StringIO()):
    m.gerar_figura_1_topologia()
    res["estab"] = m.gerar_figura_2_estabilizacao()
    res["termo"] = m.gerar_figura_3_termodinamica()
    res["trans"] = m.gerar_figura_4_translacao()
    res["corr"] = m.gerar_figura_5_correcao_erros()
    res["conv"] = m.gerar_figura_6_convergencia()
    res["comm"] = m.gerar_figura_7_comunicacao()

from scipy.spatial import cKDTree
c=res["comm"]
doc = fitz.open(W + r"\FOLHAS_SUBSTITUTIVAS_050579.pdf")
pg=doc[6]
rects=[dr["rect"] for dr in pg.get_drawings() if dr["type"]=="f" and dr.get("fill")==(1.0,1.0,1.0) and dr["rect"].width>300 and dr["rect"].height>100 and dr["rect"].height<300]
rects=sorted(rects,key=lambda r:r.y0)
def centers(R):
    inn=fitz.Rect(R.x0+3,R.y0+3,R.x1-3,R.y1-3); out=[]
    for dr in pg.get_drawings():
        r=dr["rect"]
        if inn.contains(r) and max(r.width,r.height)<14 and r.width>3 and (dr.get("fill") is not None or dr.get("color") is not None) and not (dr.get("dashes") and dr["dashes"].startswith("[ .7")):
            out.append(((r.x0+r.x1)/2,(r.y0+r.y1)/2))
    return np.array(out)
for nm,(R,ykey,ytf) in {"7a latency":(rects[0],"latencia",np.log10),"7b fidelity":(rects[1],"fidelidade",lambda a:a)}.items():
    C=centers(R)
    # exclude legend swatches: the legend is the white box; markers inside it are few; keep all but report
    xs=np.concatenate([np.log10(np.asarray(c["distancias_"+k],float)) for k in ("local","regional","global")])
    ys=np.concatenate([ytf(np.asarray(c[ykey+"_"+k],float)) for k in ("local","regional","global")])
    ok=np.isfinite(ys)&(ys>=0.99) if ykey=='fidelidade' else np.isfinite(ys)
    xs=xs[ok]; ys=ys[ok]
    # map data to page by extents; y inverted
    ux=(xs-xs.min())/np.ptp(xs); uy=(ys-ys.min())/np.ptp(ys)
    # page extents from marker centers (data extremes are markers)
    cx=C[:,0]; cy=C[:,1]
    px=cx.min()+ux*np.ptp(cx); py=cy.max()-uy*np.ptp(cy)
    if ykey=='fidelidade':
        py=R.y1-(ys-0.99)/(1.001-0.99)*R.height
    tree=cKDTree(C); d,_=tree.query(np.c_[px,py])
    print(nm,"markers found:",len(C),"data points:",len(xs),"predicted->nearest marker dist: max %.2f pt, median %.2f pt (marker size ~8 pt; panel width %.0f pt)"%(d.max(),np.median(d),R.width))
