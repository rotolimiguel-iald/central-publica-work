from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import sympy as S
import json,os,hashlib
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'CONTROLE_EINSTEIN_QUADRATICO_079_20260910'
sources=[
ROOT/'FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md',
ROOT/'compute_linear_einstein078_new.py']
def pin(p):
    b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
before=[pin(p) for p in sources]
started=datetime.now(timezone.utc).isoformat()
OUT.mkdir(exist_ok=False)
tau,x,y,z=S.symbols('tau x y z',real=True)
ell=S.symbols('ell',positive=True)
k=S.symbols('k',nonzero=True,real=True)
coords=[tau,x,y,z]
f=S.Function('f')(z)
eta=S.diag(1,-1,-1,-1)
a2=ell**2/z**2
g0=a2*eta
gi0=eta/a2
gam=S.zeros(4)
gam[1,1]=f*S.cos(k*tau);gam[2,2]=-gam[1,1]
gam[1,2]=gam[2,1]=f*S.sin(k*tau)
h=a2*gam
H=gi0*h
gi1=-H*gi0
gi2=H*H*gi0
def simp(q):return S.simplify(S.expand(q))
def smat(M):return M.applyfunc(simp)
def iszero(M):return all(simp(q)==0 for q in M)
@lru_cache(None)
def d0(i,j,r):return S.diff(g0[i,j],coords[r])
@lru_cache(None)
def d1(i,j,r):return S.diff(h[i,j],coords[r])
@lru_cache(None)
def Gamma(n,a,b,c):
    if n==2:return simp(-sum(H[a,e]*Gamma(1,e,b,c) for e in range(4)))
    inverse=gi0 if n==0 else gi1
    result=sum(inverse[a,e]*(d0(e,c,b)+d0(e,b,c)-d0(b,c,e)) for e in range(4))/2
    if n==1:
        result+=sum(gi0[a,e]*(d1(e,c,b)+d1(e,b,c)-d1(b,c,e)) for e in range(4))/2
    return simp(result)
def Ric(n,b,d):
    return simp(sum(
        S.diff(Gamma(n,a,b,d),coords[a])-S.diff(Gamma(n,a,b,a),coords[d])
        +sum(Gamma(m,a,e,a)*Gamma(n-m,e,b,d)-Gamma(m,a,e,d)*Gamma(n-m,e,b,a)
             for e in range(4) for m in range(n+1))
        for a in range(4)))
checks=[]
def check(name,condition):
    checks.append({'name':name,'passed':bool(condition)})
    assert condition,name
check('inverse_first_order',iszero(gi0*h+gi1*g0))
check('inverse_second_order',iszero(gi1*h+gi2*g0))
ric=[S.Matrix(4,4,lambda i,j:Ric(n,i,j)) for n in range(3)]
scalar=[simp(S.trace(gi0*ric[0])),
simp(S.trace(gi0*ric[1]+gi1*ric[0])),
simp(S.trace(gi0*ric[2]+gi1*ric[1]+gi2*ric[0]))]
Lambda=3/ell**2
F0=smat(ric[0]-g0*scalar[0]/2+Lambda*g0)
F1=smat(ric[1]-(g0*scalar[1]+h*scalar[0])/2+Lambda*h)
F2=smat(ric[2]-(g0*scalar[2]+h*scalar[1])/2)
check('background_einstein',iszero(F0))
# Coefficient of sqrt(abs(det(g))) g^{-1} F(g) g^{-1}; F0=0.
sqrtg0=ell**4/z**4
source2=smat(sqrtg0*(gi0*F2*gi0+gi1*F1*gi0+gi0*F1*gi1+S.trace(H)*gi0*F1*gi0/2))
T=S.eye(4);T[1,1]=T[2,2]=0;T[1,2]=-1;T[2,1]=1
Y=S.diag(1,1,-1,1)
check('quarter_rotation_h_is_negative',iszero(T.T*h*T+h))
check('reflection_h_reverses_k',iszero(Y.T*h*Y-h.subs(k,-k)))
check('quadratic_einstein_symmetric',iszero(F2-F2.T))
check('quadratic_einstein_quarter_rotation_invariant',iszero(T.T*F2*T-F2))
check('quadratic_einstein_reflection_invariant',iszero(Y.T*F2*Y-F2))
check('quadratic_einstein_even_in_k',iszero(F2.subs(k,-k)-F2))
check('quadratic_density_source_even_in_k',iszero(source2.subs(k,-k)-source2))
point_data={S.diff(f,z,2):2/z,S.diff(f,z):1,f:0}
atpoint=lambda M:smat(M.subs(point_data,simultaneous=True).subs(tau,0))
pF2=atpoint(F2);pric2=atpoint(ric[2])
check('point_quadratic_einstein_value',iszero(pF2-S.diag(S.Rational(3,4),-S.Rational(1,4),-S.Rational(1,4),-S.Rational(1,4))))
check('point_quadratic_ricci_value',iszero(pric2-S.diag(0,S.Rational(1,2),S.Rational(1,2),S.Rational(1,2))))
# These are direct full-function identities for arbitrary f(z), not a numerical +/-k sample.
after=[pin(p) for p in sources];assert before==after
fmt=lambda M:[[str(simp(M[i,j])) for j in range(4)] for i in range(4)]
record={
'status':'PASS_EXACT_QUADRATIC_EINSTEIN_PARITY_AND_POINT_CONTROL',
'started_utc':started,'created_utc':datetime.now(timezone.utc).isoformat(),
'coordinates':['tau','x','y','z'],'signature':[1,-1,-1,-1],
'coefficient_convention':'g_epsilon=g0+epsilon*h; F2 is the coefficient of epsilon^2, not its second derivative.',
'background':'g0=(ell/z)^2 diag(+---), z spatial, Lambda=3/ell^2',
'profile':'f(z) arbitrary for full parity controls; point f=0,fprime=1,fsecond=2/z,tau=0.',
'curvature_convention':'R^a_bcd=partial_c Gamma^a_bd-partial_d Gamma^a_bc+Gamma^a_ec Gamma^e_bd-Gamma^a_ed Gamma^e_bc; Ric_bd=R^a_bad',
'quadratic_ricci':fmt(ric[2]),'quadratic_scalar':str(scalar[2]),
'quadratic_einstein':fmt(F2),'quadratic_metric_density_source_without_action_prefactor':fmt(source2),
'point_quadratic_einstein':fmt(pF2),'point_quadratic_ricci':fmt(pric2),
'checks':checks,'checks_total':len(checks),'checks_passed':sum(c['passed'] for c in checks),
'inputs':before,'inputs_unchanged_since_before_symbolic_calculation':before==after,
'script':pin(Path(__file__).resolve()),'sympy_version':S.__version__,
'new_lean_compilations':0,'um_executed_or_imported':False,'originals_written':False,
'limits':'Finite symbolic matrix controls for arbitrary f(z). All-jet odd-functional argument is written separately and requires independent review. Does not solve lower-correction equations, prove anomaly removal or QME.'}
raw=(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
dest=OUT/'RESULTADO_EINSTEIN_QUADRATICO_079.json'
tmp=dest.with_name(dest.name+'.tmp')
with tmp.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
assert tmp.read_bytes()==raw;tmp.rename(dest);assert dest.read_bytes()==raw
print(json.dumps({'status':record['status'],'checks':len(checks),'quadratic_einstein':fmt(F2),'result':pin(dest)},ensure_ascii=True),flush=True)

