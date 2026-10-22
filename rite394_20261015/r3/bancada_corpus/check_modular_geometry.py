"""Exact finite controls and a conformal nonuniqueness example; no archive writes."""
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
assert ROOT.name == 'Chatgpt'

def site(p, q):
    return [s.eye(2), s.diag(s.sqrt(q/p), -s.sqrt(p/q)),
            s.Matrix([[0, 1/s.sqrt(q)], [0, 0]]),
            s.Matrix([[0, 0], [1/s.sqrt(p), 0]])]

def zero(m):
    return all(s.simplify(v) == 0 for v in m)

p, q = s.symbols('p q', positive=True)
basis = site(p, q)
rho = s.diag(p, q)
root = s.diag(s.sqrt(p), s.sqrt(q))
eigenvalues = [1, 1, s.sqrt(p/q), s.sqrt(q/p)]
gram = s.Matrix(4, 4, lambda i,j: s.simplify(s.trace(rho*basis[i].H*basis[j])))
checks = {
    'symbolic_site_orthonormality': zero(gram.subs(q, 1-p) - s.eye(4)),
    'symbolic_site_positive_eigenvectors': all(zero(root*b*root.inv()-d*b)
                                             for b,d in zip(basis,eigenvalues)),
    'symbolic_site_J_permutation': all(zero(root*basis[k].H*root.inv()-basis[j])
                                      for k,j in enumerate([0,1,3,2]))}
p1,p2 = s.Rational(1,3),s.Rational(2,5)
b1,b2 = site(p1,1-p1),site(p2,1-p2)
bs = [s.kronecker_product(a,b) for a in b1 for b in b2]
r2 = s.kronecker_product(s.diag(p1,1-p1),s.diag(p2,1-p2))
g2 = s.Matrix(16,16,lambda i,j:s.simplify(s.trace(r2*bs[i].H*bs[j])))
checks['two_site_orthonormality'] = zero(g2-s.eye(16))

t,x,y,z = s.symbols('t x y z', real=True)
coords = [t,x,y,z]
eta = s.diag(1,-1,-1,-1)
metric = s.exp(2*t)*eta
inverse = metric.inv()
gamma = [[[s.simplify(sum(inverse[a,l]*(s.diff(metric[l,c],coords[b])+
    s.diff(metric[l,b],coords[c])-s.diff(metric[b,c],coords[l])) for l in range(4))/2)
    for c in range(4)] for b in range(4)] for a in range(4)]
ricci = s.Matrix(4,4,lambda b,d:s.simplify(sum(
    s.diff(gamma[a][b][d],coords[a])-s.diff(gamma[a][b][a],coords[d])+
    sum(gamma[a][a][l]*gamma[l][b][d]-gamma[a][d][l]*gamma[l][b][a]
        for l in range(4)) for a in range(4))))
scalar = s.simplify(sum(inverse[b,d]*ricci[b,d] for b in range(4) for d in range(4)))
checks['conformal_scalar_nonzero'] = s.simplify(scalar + 6*s.exp(-2*t)) == 0
v = s.Matrix(s.symbols('v0:4', real=True))
checks['same_null_cones'] = s.simplify((v.T*metric*v)[0]-s.exp(2*t)*(v.T*eta*v)[0]) == 0
assert all(checks.values()), checks
result = {'scope':'Exact finite controls, not a proof of an infinite-dimensional limit.',
          'checks':checks, 'ricci_conformal':str(ricci), 'scalar_conformal':str(scalar),
          'convention':'R_bd = d_a Gamma^a_bd - d_d Gamma^a_ba + Gamma^a_al Gamma^l_bd - Gamma^a_dl Gamma^l_ba',
          'interpretation':'Identical null cones do not fix curvature without conformal scale data.'}
target = ROOT/'controles_modular_geometria.json'
assert not target.exists(), 'Do not overwrite an existing result'
tmp = target.with_suffix('.json.tmp')
with tmp.open('x',encoding='utf-8') as f:
    f.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
assert tmp.stat().st_size > 100
tmp.rename(target)
print(json.dumps(result,ensure_ascii=False,indent=2))
