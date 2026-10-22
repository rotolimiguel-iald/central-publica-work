"""Independent dense finite-matrix controls of the invariant trace expansion."""
from pathlib import Path
from datetime import datetime,timezone
import sympy as S,json,hashlib,os
OUT=Path(__file__).resolve().parent
s=S.symbols("s",real=True);g=S.eye(4)
u=[S.Matrix(x)for x in [(1,2,0),(0,1,3),(2,-1,1),(1,0,-2)]]
B=[[S.Matrix([((a+1)*(i+j+2)+(i+1)*(j+1))%7-3 for a in range(3)])for j in range(4)]for i in range(4)]
B[3][3]=-sum((B[i][i]for i in range(3)),S.zeros(3,1))
A=S.Matrix([[2,1,-1,0],[1,-1,2,1],[-1,2,3,-2],[0,1,-2,1]])
N=S.Matrix([[1,-1,2,0],[-1,2,0,1],[2,0,-1,-1],[0,1,-1,3]])
R=[[[[A[i,k]*N[j,l]+A[j,l]*N[i,k]-A[i,l]*N[j,k]-A[j,k]*N[i,l]for l in range(4)]for k in range(4)]for j in range(4)]for i in range(4)]
Ric=S.Matrix(4,4,lambda i,j:sum(R[k][i][k][j]for k in range(4)));Rs=S.trace(Ric)
riem2=sum(R[i][j][k][l]**2 for i in range(4)for j in range(4)for k in range(4)for l in range(4))
ric2=S.trace(Ric*Ric);W=S.Matrix(4,4,lambda i,j:(u[i].T*u[j])[0]);Q=S.trace(W);W2=S.trace(W*W)
U=sum((v*v.T for v in u),S.zeros(3));B2=sum((B[i][j].T*B[i][j])[0]for i in range(4)for j in range(4))
pairs=[(i,j)for i in range(4)for j in range(i,4)]
def un(v):
 h=S.zeros(4)
 for k,(i,j)in enumerate(pairs):h[i,j]=h[j,i]=v[k]
 return h,v[10:,0]
def pack(h,x):return S.Matrix([h[i,j]for i,j in pairs]+list(x))
def op(f):return S.Matrix.hstack(*(f(*un(S.eye(13)[:,i]))for i in range(13)))
def omega(r,us):
 return op(lambda h,x:pack(S.Matrix(4,4,lambda i,j:s*(g[i,r]*(us[j].T*x)[0]+g[j,r]*(us[i].T*x)[0])), -sum((us[j]*h[r,j]for j in range(4)),S.zeros(3,1))/2+us[r]*S.trace(h)/4))
om=[omega(r,u)for r in range(4)]
def ec(h,x):
 hh=2*S.Matrix(4,4,lambda i,j:sum(R[i][k][j][l]*h[k,l]for k in range(4)for l in range(4)))-s*(W*h+h*W+W*S.trace(h))/2-2*s*S.Matrix(4,4,lambda i,j:(B[i][j].T*x)[0])
 xx=-sum((B[i][j]*h[i,j]for i in range(4)for j in range(4)),S.zeros(3,1))/2+(Q*S.eye(3)+(2*s-1)*U)*x
 return pack(hh,xx)
E=op(ec)
Os=[]
for r in range(4):
 for t in range(r+1,4):
  O0=op(lambda h,x:pack(S.Matrix(4,4,lambda i,j:-sum(R[k][i][r][t]*h[k,j]+R[k][j][r][t]*h[i,k]for k in range(4))),(u[r]*u[t].T-u[t]*u[r].T)*x))
  Os.append(O0+omega(t,B[r])-omega(r,B[t])+om[r]*om[t]-om[t]*om[r])
trE=S.factor(S.trace(E));trE2=S.factor(S.trace(E*E));trO2=S.factor(2*sum(S.trace(O*O)for O in Os))
checks=[]
def ck(name,expr):
 v=S.factor(expr);checks.append({"name":name,"passed":bool(v==0),"residual":str(v)})
ck("dense_trace_E",trE-(-Rs+(2-s)*Q))
ck("dense_trace_E2",trE2-(3*riem2+(s*s/2+4*s+1)*Q**2+(13*s*s/2-4*s+1)*W2+2*s*B2))
ck("dense_trace_Omega2",trO2-(-6*riem2+4*s*S.trace(Ric*W)+2*s*Rs*Q+(-3*s*s+4*s+2)*W2+(-3*s*s-4*s-2)*Q**2-8*s*B2))
r,rr,ri,q,w,b,rw,br,bq=S.symbols("R Ricci2 Riemann2 Q W2 B2 RicciW BoxR BoxQ")
ee=-r+(2-s)*q
ee2=3*ri+(s*s/2+4*s+1)*q*q+(13*s*s/2-4*s+1)*w+2*s*b
oo=-6*ri+4*s*rw+2*s*r*q+(-3*s*s+4*s+2)*w+(-3*s*s-4*s-2)*q*q-8*s*b
base=(5*r*r-2*rr+2*ri)/360+br/30
by_traces=S.Rational(1,2)*((-br+(2-s)*bq)/6+r*ee/6+ee2/2+oo/12+13*base)-(br/6+r*r/6+rr/2-ri/12+4*base)
expanded=S.Rational(43,72)*ri-S.Rational(37,72)*rr-S.Rational(31,144)*r*r+r*q/6+s*rw/6+(5*s+1)*q*q/6+(9*s*s-5*s+2)*w/6+s*b/6-br/6+(2-s)*bq/12
ck("universal_supertrace_to_expanded_invariants",by_traces-expanded)
red=expanded.subs(b,bq/2-rw+q*q-w)
red_claim=S.Rational(43,72)*ri-S.Rational(37,72)*rr-S.Rational(31,144)*r*r+r*q/6+(s+S.Rational(1,6))*q*q+(3*s*s/2-s+S.Rational(1,3))*w-br/6+bq/6
ck("Bochner_reduction_algebra",red-red_claim)
x=S.symbols("x",real=True)
background={s:4,r:3-12*x,rr:48*x*x-18*x+S.Rational(9,4),ri:48*x*x-12*x+S.Rational(3,2),q:-3*x,w:3*x*x,b:-6*x*x+3*x/2,rw:12*x*x-9*x/4,br:-6*x,bq:-3*x/2}
bg=S.factor(expanded.subs(background))
ck("background_invariant_formula_matches_matrix_result",bg-(7440*x*x+1616*x-211)/96)
ck("background_Bochner_identity",(b+rw-q*q+w-bq/2).subs(background))
ck("background_total_derivative",(-br/6+(2-s)*bq/12).subs(background)-5*x/4)
output={"status":"PASS_EXACT_INVARIANT_TRACE_CONTROLS__NOT_LEAN"if all(c["passed"]for c in checks)else"FAIL","created_utc":datetime.now(timezone.utc).isoformat(),"sympy_version":S.__version__,"check_count":len(checks),"checks":checks,
 "scope":"Dense finite-matrix controls (polynomial in coupling s) plus symbolic invariant algebra. These finite checks complement, and do not replace, the written tensor-contraction proof.",
 "expressions":{"dense_trE":str(trE),"dense_trE2":str(trE2),"dense_trOmega2":str(trO2),"background_C4":str(bg)},
 "source":{"path":str(Path(__file__).resolve()),"bytes":len(Path(__file__).read_bytes()),"sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},"um_executed_or_imported":False,"lean_executed":False,"originals_written":False}
raw=(json.dumps(output,ensure_ascii=False,indent=2)+"\n").encode("utf-8");p=OUT/"VERIFICACAO_TRACOS_INVARIANTES.json";tmp=p.with_suffix(".tmp");assert not p.exists()and not tmp.exists()
with tmp.open("xb")as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==raw;os.replace(tmp,p);assert p.read_bytes()==raw
print(json.dumps(output,ensure_ascii=False,indent=2))
if output["status"]=="FAIL":raise SystemExit(1)
