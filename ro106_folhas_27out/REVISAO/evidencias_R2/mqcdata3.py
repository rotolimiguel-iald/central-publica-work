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
with contextlib.redirect_stdout(io.StringIO()): r=m.simular_translacao_holografica()
X=np.asarray(r["t_signal"],float); Y=np.abs(np.asarray(r["L_in"],float))
for P,dr in polys(doc[3]):
    if dr.get("dashes")=="[ 11.2 5.6 ] 0":
        px,py=P[:,1],P[:,0]
        best=1
        for ox,oy in ((0,1),(1,0)):
            for fx in (1,-1):
                for fy in (1,-1):
                    px=P[:,ox];py=P[:,oy]
                    ux=(px-px.min())/np.ptp(px); uy=(py-py.min())/np.ptp(py)
                    if fx<0: ux=1-ux
                    if fy<0: uy=1-uy
                    xd=X.min()+ux*np.ptp(X); yd=Y.min()+uy*np.ptp(Y)
                    dev=np.abs(np.interp(xd,X,Y)-yd).max()/np.ptp(Y); best=min(best,dev)
        print("|L| (original) polyline vs np.abs(L_in) from original function: max dev %.3f%% of range"%(best*100))
