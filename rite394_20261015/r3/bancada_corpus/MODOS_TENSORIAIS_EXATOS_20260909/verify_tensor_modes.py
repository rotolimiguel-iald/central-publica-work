from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,sys
import sympy as s

OUT=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
assert OUT.is_relative_to(ROOT)
eta,p,eps,u,v,c,kappa=s.symbols('eta p eps u v c kappa',real=True)
a=2/s.cosh(eta);t=s.tanh(eta)
f=(p-s.I*t)*s.exp(-s.I*p*eta)
checks={}
def check(name,value):
    reduced=s.simplify(s.expand_complex(value))
    assert reduced==0,(name,reduced)
    checks[name]={'residual':str(reduced),'passed':True}
check('conformal_scale',s.diff(a,eta,2)/a-(1-2/s.cosh(eta)**2))
check('tanh_first_jet',s.diff(t,eta)-(1-t*t))
check('unnormalized_darboux_ode',s.diff(f,eta,2)+(p*p+2/s.cosh(eta)**2)*f)
check('unnormalized_wronskian',f*s.conjugate(s.diff(f,eta))-s.diff(f,eta)*s.conjugate(f)-2*s.I*p*(p*p+1))
check('amplitude_square',f*s.conjugate(f)-(p*p+t*t))
x=[s.exp(eps*u),s.exp(eps*v),s.exp(-eps*(u+v))]
R3=2*(-sum(z*z for z in x)+2*(x[0]*x[1]+x[0]*x[2]+x[1]*x[2]))/s.prod(x)
norm2=u*u+v*v+(u+v)**2
check('berger_determinant_one',s.prod(x)-1)
check('berger_background_curvature',R3.subs(eps,0)-6)
check('berger_first_variation',s.diff(R3,eps).subs(eps,0))
check('berger_tt_second_order_coefficient',s.diff(R3,eps,2).subs(eps,0)/2+2*norm2)
matter=-c*a*sum(1/z for z in x)/2
check('sigma_tt_second_order_coefficient',s.diff(matter,eps,2).subs(eps,0)/2+c*a*norm2/4)
total_second=(a/(2*kappa)*s.diff(R3,eps,2).subs(eps,0)/2+s.diff(matter,eps,2).subs(eps,0)/2)
check('berger_tt_matches_general_operator',total_second+a/(8*kappa)*(6+2+2*kappa*c)*norm2)
ell=s.symbols('ell',integer=True,nonnegative=True)
check('tensor_canonical_frequency',(ell*(ell+2)-2+10)-1-((ell+1)**2+6))
data={'status':'PASS_EXACT_SYMBOLIC_CONTROLS__NOT_LEAN','created_utc':datetime.now(timezone.utc).isoformat(),
      'sympy_version':s.__version__,'checks':checks,'count':len(checks),
      'interpretation':'Exact mode ODE and Wronskian; homogeneous l=2 tensor curvature control. This script is not proof of general TT reduction, spectral completeness, Hadamard condition or coupled quantization.',
      'source':{'path':Path(__file__).as_posix(),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
      'um_executed_or_imported':False,'originals_written':False}
raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
target=OUT/'VERIFICACAO_MODOS_TT.json';assert not target.exists()
tmp=OUT/'VERIFICACAO_MODOS_TT.json.tmp'
with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==raw
tmp.rename(target);assert target.read_bytes()==raw
print(json.dumps({'status':data['status'],'count':len(checks),'receipt':target.as_posix()}))
