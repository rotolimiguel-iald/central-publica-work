from pathlib import Path
from datetime import datetime,timezone
import sympy as s
import json,hashlib,os
OUT=Path(__file__).resolve().parent
x=s.Matrix(s.symbols('x0:4',real=True));D=1+(x.dot(x))/2
entries=s.symbols('c0:10',real=True)
basis=[]
for i in range(4):
    E=s.zeros(4);E[i,i]=1;basis.append(E)
for i in range(4):
    for j in range(i+1,4):
        E=s.zeros(4);E[i,j]=E[j,i]=1/s.sqrt(2);basis.append(E)
C=sum((entries[a]*basis[a] for a in range(10)),s.zeros(4))
V=s.Matrix([1,*x,*[(x.dot(E*x))/2 for E in basis]])
z=2*V/D
N=s.Matrix([(x.dot(C*x))/2,*(-C*x),*entries])
checks={}
def check(name,v):
    reduced=s.factor(v)
    assert reduced==0,(name,reduced)
    checks[name]={'passed':True,'residual':'0'}
check('sphere_norm_V',V.dot(V)-D**2)
check('sphere_norm_z',z.dot(z)-4)
check('distance_to_positive_chart_center',(z-s.Matrix([2]+[0]*14)).dot(z-s.Matrix([2]+[0]*14))-4*x.dot(x)/D)
check('normal_radial',N.dot(V))
for i in range(4):check(f'normal_tangent_{i}',N.dot(V.diff(x[i])))
for i in range(4):
    for j in range(i,4):
        check(f'second_form_{i}_{j}',N.dot(z.diff(x[i]).diff(x[j]))-2*C[i,j]/D)
        target=4/D*(1 if i==j else 0)-2*x[i]*x[j]/D**2
        check(f'induced_fisher_{i}_{j}',z.diff(x[i]).dot(z.diff(x[j]))-target)
check('normal_norm_identity',N.dot(N)-(sum(v*v for v in entries)+(C*x).dot(C*x)+(x.dot(C*x))**2/4))
origin={v:0 for v in x}
B=[]
for E in basis:
    normal=s.zeros(15,1)
    for i in range(4):
        for j in range(4):normal+=E[i,j]*z.diff(x[i]).diff(x[j]).subs(origin)
    normal[0]=0
    for i in range(1,5):normal[i]=0
    B.append(normal)
for i in range(10):
    for j in range(i,10):check(f'normal_gram_origin_{i}_{j}',B[i].dot(B[j])-(4 if i==j else 0))
result={'status':'PASS_EXACT_FREE_CHART_CONTROLS__NOT_LEAN','created_utc':datetime.now(timezone.utc).isoformat(),
    'sympy_version':s.__version__,'checks':checks,'count':len(checks),
    'scope':'Exact algebra for the explicit free immersion: spherical normalization, Fisher metric, normal map, second form, origin Gram. Inequality bounds, residual Nash realization and functional variational equivalence are written proofs, not established by CAS.',
    'script':{'path':Path(__file__).as_posix(),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
    'um_executed_or_imported':False,'originals_written':False}
raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode()
target=OUT/'VERIFICACAO_CARTA_LIVRE.json';assert not target.exists()
tmp=target.with_name(target.name+'.tmp')
with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==raw
tmp.rename(target);assert target.read_bytes()==raw
print(json.dumps({'status':result['status'],'count':len(checks),'receipt':target.as_posix()}))
