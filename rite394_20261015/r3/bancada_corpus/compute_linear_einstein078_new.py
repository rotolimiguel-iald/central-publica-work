from pathlib import Path
from datetime import datetime,timezone
from functools import lru_cache
import sympy as S
import os,json,hashlib
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt')
OUT=ROOT/'CONTROLE_EINSTEIN_LINEARIZADO_078_20260910'
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
gamma=S.zeros(4)
gamma[1,1]=f*S.cos(k*tau);gamma[2,2]=-gamma[1,1]
gamma[1,2]=gamma[2,1]=f*S.sin(k*tau)
h=a2*gamma
gi1=-(gi0*h*gi0)
def simp(q):return S.simplify(S.expand(q))
@lru_cache(None)
def d0(i,j,r):return S.diff(g0[i,j],coords[r])
@lru_cache(None)
def d1(i,j,r):return S.diff(h[i,j],coords[r])
@lru_cache(None)
def G0(a,b,c):
    return simp(sum(gi0[a,e]*(d0(e,c,b)+d0(e,b,c)-d0(b,c,e)) for e in range(4))/2)
@lru_cache(None)
def G1(a,b,c):
    return simp(sum(gi1[a,e]*(d0(e,c,b)+d0(e,b,c)-d0(b,c,e))+gi0[a,e]*(d1(e,c,b)+d1(e,b,c)-d1(b,c,e)) for e in range(4))/2)
def Ric0(b,d):
    return simp(sum(S.diff(G0(a,b,d),coords[a])-S.diff(G0(a,b,a),coords[d])+sum(G0(a,e,a)*G0(e,b,d)-G0(a,e,d)*G0(e,b,a) for e in range(4)) for a in range(4)))
def Ric1(b,d):
    return simp(sum(S.diff(G1(a,b,d),coords[a])-S.diff(G1(a,b,a),coords[d])+sum(G1(a,e,a)*G0(e,b,d)+G0(a,e,a)*G1(e,b,d)-G1(a,e,d)*G0(e,b,a)-G0(a,e,d)*G1(e,b,a) for e in range(4)) for a in range(4)))
checks=[]
def check(name,condition):
    checks.append({'name':name,'passed':bool(condition)})
    assert condition,name
Lambda=3/ell**2
ric0=S.Matrix(4,4,Ric0)
ric1=S.Matrix(4,4,Ric1)
ode=S.diff(f,z,2)-2*S.diff(f,z)/z+k*k*f
expected=S.zeros(4)
expected[1,1]=ode*S.cos(k*tau)/2
expected[2,2]=-expected[1,1]
expected[1,2]=expected[2,1]=ode*S.sin(k*tau)/2
res=ric1-Lambda*h
for i in range(4):
    for j in range(4):
        check('background_einstein_'+str((i,j)),simp(ric0[i,j]-Lambda*g0[i,j])==0)
        check('linearized_einstein_ode_'+str((i,j)),simp(res[i,j]-expected[i,j])==0)
check('flat_trace_free',S.trace(eta*gamma)==0)
for b in range(4):
    check('flat_divergence_free_'+str(b),simp(sum(eta[a,a]*S.diff(gamma[a,b],coords[a]) for a in range(4)))==0)
f1=S.cos(k*z)+k*z*S.sin(k*z)
f2=S.sin(k*z)-k*z*S.cos(k*z)
for i,sol in enumerate([f1,f2]):
    check('ode_solution_'+str(i),simp(S.diff(sol,z,2)-2*S.diff(sol,z)/z+k*k*sol)==0)
check('wronskian',simp(f1*S.diff(f2,z)-S.diff(f1,z)*f2-k**3*z**2)==0)
z0=S.symbols('z0',positive=True)
killings=[S.Matrix([1,0,0,0]),S.Matrix([0,1,0,0]),S.Matrix([0,0,1,0]),S.Matrix([tau,x,y,z])/z0]
for n,v in enumerate(killings):
    for i in range(4):
        for j in range(4):
            Lie=sum(v[r]*d0(i,j,r)+g0[r,j]*S.diff(v[r],coords[i])+g0[i,r]*S.diff(v[r],coords[j]) for r in range(4))
            check('killing_'+str((n,i,j)),simp(Lie)==0)
values=S.Matrix.hstack(*(v.subs({tau:0,x:0,y:0,z:z0}) for v in killings))
check('killing_values_basis',values==S.eye(4))
def format_matrix(M):return [[str(simp(M[i,j])) for j in range(4)] for i in range(4)]
source=Path(__file__).resolve()
pin=lambda p:{'path':p.as_posix(),'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
inputs=[ROOT/'RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md']
before=[pin(p) for p in inputs]
record={'status':'PASS_EXACT_DIRECT_CONNECTION_LINEARIZED_EINSTEIN_CONTROL',
'created_utc':datetime.now(timezone.utc).isoformat(),
'coordinates':['tau','x','y','z'],'signature':[1,-1,-1,-1],
'curvature_convention':'R^a_bcd=partial_c Gamma^a_bd-partial_d Gamma^a_bc+Gamma^a_ec Gamma^e_bd-Gamma^a_ed Gamma^e_bc; Ric_bd=R^a_bad.',
'background':'g0=(ell/z)^2 diag(1,-1,-1,-1); z spatial, ell>0, z>0.',
'ricci_background':format_matrix(ric0),'linearized_ricci_minus_Lambda_h':format_matrix(res),
'ode':str(ode),'wronskian':str(k**3*z**2),'killing_values':format_matrix(values),
'checks':checks,'checks_total':len(checks),'checks_passed':sum(c['passed'] for c in checks),
'sympy_version':S.__version__,'source':pin(source),'inputs':before,
'input_sources_unchanged':before==[pin(p) for p in inputs],
'limits':'Direct first-order connection/Ricci and Killing controls. Does not evaluate all jets by CAS or prove BRST non-exactness; these require the written identity and its independent review. No um.py or Lean executed.'}
assert record['input_sources_unchanged']
raw=(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode()
target=OUT/'RESULTADO_EINSTEIN_LINEARIZADO_078.json'
temp=target.with_suffix('.tmp')
with temp.open('xb') as out:out.write(raw);out.flush();os.fsync(out.fileno())
assert temp.read_bytes()==raw;temp.rename(target);assert target.read_bytes()==raw
print(json.dumps({'status':record['status'],'checks':len(checks),'result':pin(target)}),flush=True)

