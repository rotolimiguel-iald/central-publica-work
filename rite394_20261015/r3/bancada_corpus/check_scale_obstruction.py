"""Exact curvature and conformal-scale controls. Writes only new workbench files."""
from pathlib import Path
from datetime import datetime
import json
import sympy as s

root = Path(__file__).resolve().parent
t = s.symbols('t', positive=True)
x,y,z = s.symbols('x y z', real=True)
coords = (t,x,y,z)

def scalar_curvature(metric):
    inv = metric.inv()
    gamma = [[[s.simplify(sum(inv[a,k]*(s.diff(metric[k,c],coords[b])+
        s.diff(metric[k,b],coords[c])-s.diff(metric[b,c],coords[k]))/2
        for k in range(4))) for c in range(4)] for b in range(4)] for a in range(4)]
    ric = s.zeros(4)
    for b in range(4):
        for d in range(4):
            ric[b,d] = s.simplify(sum(s.diff(gamma[a][d][b],coords[a])-
                s.diff(gamma[a][a][b],coords[d])+
                sum(gamma[a][a][k]*gamma[k][d][b]-gamma[a][d][k]*gamma[k][a][b]
                    for k in range(4)) for a in range(4)))
    return s.simplify(sum(inv[b,d]*ric[b,d] for b in range(4) for d in range(4)))

g = s.diag(-1,1,1,1)/t**2
r1,r2 = scalar_curvature(g),scalar_curvature(4*g)
assert r1 == 12 and r2 == 3
v = s.Matrix(s.symbols('v0:4', real=True))
assert s.simplify((v.T*(4*g)*v)[0]-4*(v.T*g*v)[0]) == 0
c,u,trace = s.symbols('c u trace', positive=True)
assert s.simplify(c*(s.exp(-u)*trace)-s.exp(-u)*(c*trace)) == 0
out = {'status':'REAL_EXACT_SYMBOLIC', 'metric':'t^(-2) diag(-1,1,1,1), t>0',
       'rescale':4, 'scalar_curvature':[str(r1),str(r2)],
       'same_null_cones':True,'not_locally_isometric':'distinct constant scalar curvatures',
       'trace_scaling_homogeneous':True,
       'scope':'Geometric obstruction only; no CGMA network constructed by this script.'}
target = root / ('escala_controle_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
data = json.dumps(out,ensure_ascii=False,indent=2).encode('utf-8')
temporary = target.with_suffix('.json.tmp')
with temporary.open('xb') as f: f.write(data)
assert temporary.stat().st_size == len(data)
temporary.rename(target)
print(target)
print(json.dumps(out,ensure_ascii=False))
