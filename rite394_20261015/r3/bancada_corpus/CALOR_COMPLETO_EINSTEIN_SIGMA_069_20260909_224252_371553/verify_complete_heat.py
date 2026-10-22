"""Exact contractions of the actual coupled 13x13 operator. No um.py or Lean."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
import sympy as S
OUT=Path(__file__).resolve().parent
z,H=S.symbols("z H",real=True)
s=S.Integer(4); lam=S.Rational(3,4)
sg=[S.Integer(1),S.Integer(-1),S.Integer(-1),S.Integer(-1)]
g=S.diag(*sg); pairs=[(i,j) for i in range(4) for j in range(i,4)]
zero3=S.zeros(3,1)
u=[zero3.copy()]+[z*S.eye(3)[:,i] for i in range(3)]
B=[[zero3.copy() for j in range(4)]for i in range(4)]
for i in range(1,4): B[0][i]=B[i][0]=-H*u[i]
def kd(i,j):return S.Integer(i==j)
R=[[[[S.Integer(0) for l in range(4)]for k in range(4)]for j in range(4)]for i in range(4)]
def setR(a,b,c,d,value):
    for i,j,k,l,sgn in [(a,b,c,d,1),(b,a,c,d,-1),(a,b,d,c,-1),(b,a,d,c,1),(c,d,a,b,1),(d,c,a,b,-1),(c,d,b,a,-1),(d,c,b,a,1)]:
        R[i][j][k][l]=sgn*value
for i in range(1,4):setR(0,i,0,i,-S.Rational(1,4))
for i in range(1,4):
    for j in range(i+1,4):setR(i,j,i,j,-(2*z*z-S.Rational(1,4)))
Ric=S.Matrix(4,4,lambda i,j:sum(sg[k]*R[k][i][k][j] for k in range(4)))
Rs=S.expand(sum(sg[i]*Ric[i,i] for i in range(4)))
R2=S.expand(sum(sg[i]*sg[j]*sg[k]*sg[l]*R[i][j][k][l]**2 for i in range(4) for j in range(4) for k in range(4) for l in range(4)))
Ric2=S.expand(sum(sg[i]*sg[j]*Ric[i,j]**2 for i in range(4) for j in range(4)))
W=S.Matrix(4,4,lambda i,j:(u[i].T*u[j])[0]);Q=S.expand(sum(sg[i]*W[i,i]for i in range(4)))
U=sum((sg[i]*u[i]*u[i].T for i in range(4)),S.zeros(3))
def trh(h):return sum(sg[i]*h[i,i]for i in range(4))
def ctr(h,T):return sum(sg[i]*sg[j]*h[i,j]*T[i,j]for i in range(4)for j in range(4))
def bc(h):return sum((sg[i]*sg[j]*h[i,j]*B[i][j]for i in range(4)for j in range(4)),S.zeros(3,1))
def itr(h):return h-g*trh(h)/2
def unpack(v):
    h=S.zeros(4)
    for k,(i,j)in enumerate(pairs):h[i,j]=h[j,i]=v[k]
    return h,v[10:13,0]
def pack(h,xi):return S.Matrix([h[i,j]for i,j in pairs]+list(xi))
def op(fn):return S.Matrix.hstack(*(fn(*unpack(S.eye(13)[:,i]))for i in range(13)))
def om(r,us):
    def f(h,xi):
        hh=S.Matrix(4,4,lambda i,j:s*(g[i,r]*(us[j].T*xi)[0]+g[j,r]*(us[i].T*xi)[0]))
        xx=-sum((sg[j]*us[j]*h[r,j]for j in range(4)),S.zeros(3,1))/2+us[r]*trh(h)/4
        return pack(hh,xx)
    return op(f)
omega=[om(r,u)for r in range(4)]
dw=[[om(j,B[i])for j in range(4)]for i in range(4)]
def Rmap(h):return S.Matrix(4,4,lambda i,j:sum(R[i][k][j][l]*sg[k]*sg[l]*h[k,l]for k in range(4)for l in range(4)))
def SW(h):return S.Matrix(4,4,lambda i,j:sum(sg[k]*(W[i,k]*h[k,j]+W[j,k]*h[k,i])for k in range(4)))
def LR(h):
    return S.Matrix(4,4,lambda i,j:sum(sg[k]*(Ric[k,i]*h[k,j]+Ric[k,j]*h[k,i])for k in range(4))/2)-Rmap(h)-Rs*h/2+g*ctr(h,Ric)/2
def vraw(h,xi):
    dt=-Q*h/2+g*ctr(h,W)/2
    return pack(-2*itr(LR(h)+lam*h-s*dt), (Q*S.eye(3)-U)*xi-bc(h))
V=op(vraw)
divom=sum((sg[i]*dw[i][i]for i in range(4)),S.zeros(13))
om2=sum((sg[i]*omega[i]*omega[i]for i in range(4)),S.zeros(13))
E=(V-divom-om2).applyfunc(S.expand)
def eclaimed(h,xi):
    hh=2*Rmap(h)-s*(SW(h)+W*trh(h))/2-2*s*S.Matrix(4,4,lambda i,j:(B[i][j].T*xi)[0])
    xx=-bc(h)/2+(Q*S.eye(3)+(2*s-1)*U)*xi
    return pack(hh,xx)
EC=op(eclaimed)
def curv0(r,t):
    def f(h,xi):
        hh=S.Matrix(4,4,lambda i,j:-sum(sg[k]*(R[k][i][r][t]*h[k,j]+R[k][j][r][t]*h[i,k])for k in range(4)))
        xx=(u[r]*u[t].T-u[t]*u[r].T)*xi
        return pack(hh,xx)
    return op(f)
Omega={}
GhostOmega={}
for r in range(4):
    for t in range(r+1,4):
        Omega[r,t]=(curv0(r,t)+dw[r][t]-dw[t][r]+omega[r]*omega[t]-omega[t]*omega[r]).applyfunc(S.expand)
        GhostOmega[r,t]=S.Matrix(4,4,lambda i,j:-sg[j]*R[j][i][r][t])
Egh=Ric*g
def red(x):return S.factor(S.expand(x).subs(H**2,z*z-S.Rational(1,4)))
def Otrace(om):return red(2*sum(sg[r]*sg[t]*S.trace(A*A)for (r,t),A in om.items()))
trE=red(S.trace(E));trE2=red(S.trace(E*E));trOm2=Otrace(Omega)
trEg=red(S.trace(Egh));trEg2=red(S.trace(Egh*Egh));trOg2=Otrace(GhostOmega)
W2=red(S.trace(W*g*W*g))
B2=red(sum(sg[i]*sg[j]*(B[i][j].T*B[i][j])[0]for i in range(4)for j in range(4)))
def box(f):return S.expand((-z**3+z/2)*S.diff(f,z)+(z*z-S.Rational(1,4))*z*z*S.diff(f,z,2))
geobase=(5*Rs**2-2*Ric2+2*R2)/360+box(Rs)/30
b4bos=red(box(trE)/6+Rs*trE/6+trE2/2+trOm2/12+13*geobase)
b4gh=red(box(trEg)/6+Rs*trEg/6+trEg2/2+trOg2/12+4*geobase)
b4=red(b4bos/2-b4gh)
checks=[]
def check(name,residual):
    if isinstance(residual,S.MatrixBase):
        rr=[S.factor(v)for v in residual];ok=all(v==0 for v in rr);summary="0"if ok else str([v for v in rr if v!=0])
    else:
        rr=S.factor(residual);ok=rr==0;summary=str(rr)
    checks.append({"name":name,"passed":bool(ok),"residual":summary})
check("on_shell_Ricci",Ric-lam*g-s*W)
check("sigma_tension",sum((sg[i]*B[i][i]for i in range(4)),S.zeros(3,1)))
check("E_from_actual_Hessian_equals_claimed_blocks",E-EC)
check("trace_E_general_identity",trE-(-Rs+(2-s)*Q))
check("trace_E_squared_general_identity",trE2-red(3*R2+(s*s/2+4*s+1)*Q**2+(13*s*s/2-4*s+1)*W2+2*s*B2))
itrmat=S.Matrix.hstack(*(S.Matrix([itr(unpack(S.eye(13)[:,i])[0])[a,b]for a,b in pairs])for i in range(10)))
Gmetric=S.diag(*[sg[i]*sg[j]*(1 if i==j else 2)for i,j in pairs])
F=S.diag(*([1]*13));F[:10,:10]=-Gmetric*itrmat/(4*s);F[10:,10:]=-S.eye(3)
check("effective_E_symmetric_in_physical_fiber",F*E-E.T*F)
for r in range(4):check("effective_connection_preserves_fiber_"+str(r),F*omega[r]+omega[r].T*F)
for (r,t),O in Omega.items():
    check("effective_curvature_target_block_"+str(r)+str(t),O[10:,10:]-(1+s)*(u[r]*u[t].T-u[t]*u[r].T))
check("ghost_trace_E_R",trEg-Rs)
check("ghost_trace_E_squared_Ricci_squared",trEg2-Ric2)
check("ghost_curvature_trace_minus_Riemann_squared",trOg2+R2)
check("box_inverse_a_squared",box(z*z)-z*z/2)
check("five_physical_degrees_leading_heat",S.Rational(13,2)-4-S.Rational(5,2))
# Algebraic vacuum Einstein cross-check for arbitrary R and Riemann squared:
rv,riemv=S.symbols("R RiemannSquared")
gb=(5*rv**2-2*rv**2/4+2*riemv)/360
puremetric=rv*(-rv)/6+3*riemv/2-6*riemv/12+10*gb
pureghost=rv*rv/6+(rv**2/4)/2-riemv/12+4*gb
pure= S.factor(puremetric/2-pureghost)
check("pure_Einstein_known_coefficient",pure-(-S.Rational(29,80)*rv**2+S.Rational(53,90)*riemv))
check("zero_sigma_background_vacuum_plus_three_scalars",b4.subs(z,0)-(pure+S.Rational(3,2)*gb).subs({rv:3,riemv:S.Rational(3,2)}))
output={"status":"PASS_EXACT_COUPLED_HEAT_CONTRACTIONS__NOT_LEAN"if all(c["passed"]for c in checks)else"FAIL",
 "created_utc":datetime.now(timezone.utc).isoformat(),"sympy_version":S.__version__,"checks":checks,"check_count":len(checks),
 "expressions":{k:str(v)for k,v in {"R":Rs,"RicciSquared":Ric2,"RiemannSquared":R2,"Q":Q,"W2":W2,"B2":B2,"tr_E":trE,"tr_E2":trE2,"tr_Omega2":trOm2,"tr_E_ghost":trEg,"tr_E2_ghost":trEg2,"tr_Omega2_ghost":trOg2,"box_tr_E":box(trE),"box_R":box(Rs),"b4_bosonic_13":b4bos,"b4_ghost_4":b4gh,"one_half_boson_minus_ghost":b4,"pure_Einstein_combination":pure}.items()},
 "scope":"Exact matrix contractions of supplied on-shell jets and universal heat formula; not proof of global Wick rotation, determinant, measure, anomalies or UV completeness.",
 "script":{"path":str(Path(__file__).resolve()),"bytes":len(Path(__file__).read_bytes()),"sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
 "um_executed_or_imported":False,"lean_executed":False,"originals_written":False}
raw=(json.dumps(output,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
p=OUT/"VERIFICACAO_CALOR_COMPLETO.json";tmp=p.with_suffix(".tmp")
assert not p.exists()and not tmp.exists()
with tmp.open("xb")as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==raw;os.replace(tmp,p);assert p.read_bytes()==raw
print(json.dumps(output,ensure_ascii=False,indent=2))
if output["status"]=="FAIL":raise SystemExit(1)
