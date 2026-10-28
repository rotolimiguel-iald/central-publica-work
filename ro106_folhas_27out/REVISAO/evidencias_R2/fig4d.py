import importlib.util, sys, numpy as np, fitz, os
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
# --- regenerate the data with the ORIGINAL script function, unaltered (own harness)
os.chdir(os.environ.get("TEMP",r"C:\Windows\Temp"))
spec=importlib.util.spec_from_file_location("mqc_orig",W+r"\entrada\mqc\mqc_simulacao_celula_elementar.py"); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
dados=m.simular_translacao_holografica()
x=np.asarray(dados["alpha2_sweep"],float); y=np.asarray(dados["corr_sweep"],float)
print("function data: n=",len(x),"x range",x[0],x[-1],"y range",y.min(),y.max())
print("vertices in 0.00167-0.00225:",[(float(a),float(b)) for a,b in zip(x,y) if 0.00167<=a<=0.00225])
# --- vector polyline in the new sheet 4
d=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf"); pg=d[3]
cands=[]
for dr in pg.get_drawings():
    if dr["type"]=="s" and dr.get("color")==(0,0,0):
        pts=[]
        for it in dr["items"]:
            if it[0]=="l":
                if not pts: pts.append(it[1])
                pts.append(it[2])
        if len(pts)==50: cands.append((dr,pts))
print("polylines with exactly 50 vertices on sheet 4:",len(cands))
for dr,pts in cands:
    P=np.array([(p.x,p.y) for p in pts])
    # sheet is rotated: data x -> page y (up the page, inverse), data y -> page x. Fit affine: page = a*data + b for each coordinate separately
    # try both assignments
    for name,(cx,cy) in {"x->pagey,y->pagex":(1,0),"x->pagex,y->pagey":(0,1)}.items():
        ax=np.polyfit(x,P[:,cx],1); ay=np.polyfit(y,P[:,cy],1)
        rx=P[:,cx]-np.polyval(ax,x); ry=P[:,cy]-np.polyval(ay,y)
        print("  fit",name,"max residual (pt): x-map",float(np.abs(rx).max()),"y-map",float(np.abs(ry).max()))
