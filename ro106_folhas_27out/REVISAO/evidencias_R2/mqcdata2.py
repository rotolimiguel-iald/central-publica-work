import importlib.util, io, contextlib, os, itertools, numpy as np, fitz
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
os.chdir(os.environ.get("TEMP",r"C:\Windows\Temp"))
spec=importlib.util.spec_from_file_location("mqc_orig",W+r"\entrada\mqc\mqc_simulacao_celula_elementar.py"); m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
fns={"estab":"simular_estabilizacao_qubit","termo":"simular_termodinamica_invertida","trans":"simular_translacao_holografica","corr":"simular_correcao_erros_iald","conv":"simular_convergencia_alpha2","comm":"simular_comunicacao_3_camadas"}
data={}
for k,f in fns.items():
    with contextlib.redirect_stdout(io.StringIO()): r=getattr(m,f)()
    arrs={}
    for kk,v in r.items():
        try:
            a=np.asarray(v,float)
            if a.ndim==1 and len(a)>=30: arrs[kk]=a
        except Exception: pass
    data[k]=arrs
    print(k,{kk:len(v) for kk,v in arrs.items()})
def polys(pg):
    out=[]
    for dr in pg.get_drawings():
        if dr["type"]!="s": continue
        pts=[]
        for it in dr["items"]:
            if it[0]=="l":
                if not pts: pts.append((it[1].x,it[1].y))
                pts.append((it[2].x,it[2].y))
        if len(pts)>=30: out.append((np.array(pts),dr))
    return out
def tf(a,kind): 
    if kind=="lin": return a
    a=np.where(a>0,a,np.nan); return np.log10(a)

doc=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf")
def mono(a): return np.all(np.diff(a)>0)
tot=0;ok=0
for si in range(len(doc)):
    pg=doc[si]
    for P,dr in polys(pg):
        n=len(P); best=None
        for dk,arrs in data.items():
            keys=list(arrs)
            for kx in keys:
                X=arrs[kx]
                if not mono(X): continue
                for ky in keys:
                    if ky==kx or len(arrs[ky])!=len(X): continue
                    Y=arrs[ky]
                    for ty in ("lin","log"):
                        yy=tf(Y,ty)
                        if not np.isfinite(yy).all(): continue
                        # candidate axis assignment
                        for ox,oy in ((0,1),(1,0)):
                            px=P[:,ox]; py=P[:,oy]
                            # map by extents (curve spans full data extent); allow reversed orientation
                            for fx in (1,-1):
                                for fy in (1,-1):
                                    ux=(px-px.min())/(np.ptp(px) or 1); uy=(py-py.min())/(np.ptp(py) or 1)
                                    if fx<0: ux=1-ux
                                    if fy<0: uy=1-uy
                                    xd=X.min()+ux*np.ptp(X); yd=yy.min()+uy*np.ptp(yy)
                                    yi=np.interp(xd,X,yy)
                                    dev=np.abs(yi-yd).max()/(np.ptp(yy) or 1)
                                    if best is None or dev<best[0]: best=(dev,dk,kx,ky,ty,(ox,oy,fx,fy))
        tot+=1; flag=best is not None and best[0]<0.02; ok+=flag
        print(f"sheet {si+1} n={n} w={dr.get('width'):.1f} dashes={dr.get('dashes')} -> max dev {best[0]*100:.2f}% of range {best[1:4]} {'MATCH' if flag else 'no-match'}")
print("polylines>=30 pts:",tot,"matched to original-function data (<2% of range):",ok)
