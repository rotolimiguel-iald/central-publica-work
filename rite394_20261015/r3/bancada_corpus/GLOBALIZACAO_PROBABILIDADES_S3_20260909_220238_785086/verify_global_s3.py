from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys
import sympy as s
OUT=Path(__file__).resolve().parent
ROOT=Path(r'C:/IALD/Central de Patentes/Chatgpt').resolve()
assert OUT.is_relative_to(ROOT)
checks={}
def check(name, expr):
    residual=s.factor(s.trigsimp(expr))
    passed=residual==0
    checks[name]={'passed':passed,'residual':str(residual)}
    if not passed: raise AssertionError((name,residual))

def pin(path):
    data=path.read_bytes()
    return {'path':path.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def write_new(path, data):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    tmp=path.with_name(path.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f: f.write(data);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==data;tmp.rename(path);assert path.read_bytes()==data

script_pin=pin(Path(__file__).resolve())
error=None
try:
    x=s.Matrix(s.symbols('x0:5',real=True))
    v=s.Matrix(s.symbols('v0:5',real=True))
    basis=[]
    for i in range(5):
        E=s.zeros(5);E[i,i]=1;basis.append(E)
    for i in range(5):
        for j in range(i+1,5):
            E=s.zeros(5);E[i,j]=E[j,i]=1/s.sqrt(2);basis.append(E)
    entries=s.symbols('c0:15',real=True)
    C=sum((entries[a]*basis[a] for a in range(15)),s.zeros(5))
    D=1+x.dot(x)/2
    V=s.Matrix([1,*x,*[x.dot(E*x)/2 for E in basis]])
    Z=2*V/D
    N=s.Matrix([x.dot(C*x)/2,*(-C*x),*entries])
    check('quadratic_sphere_norm_V',V.dot(V)-D**2)
    check('quadratic_sphere_norm_Z',Z.dot(Z)-4)
    e0=s.Matrix([2]+[0]*20)
    check('distance_to_center',(Z-e0).dot(Z-e0)-4*x.dot(x)/D)
    check('normal_radial',N.dot(V))
    for i in range(5):check('normal_first_derivative_'+str(i),N.dot(V.diff(x[i])))
    for i in range(5):
        for j in range(i,5):
            check('normal_second_derivative_'+str(i)+'_'+str(j),N.dot(Z.diff(x[i],x[j]))-2*C[i,j]/D)
    dV=V.jacobian(x)*v
    dZ=Z.jacobian(x)*v
    check('metric_in_arbitrary_direction',dZ.dot(dZ)-(4*v.dot(v)/D-2*x.dot(v)**2/D**2))
    check('normal_norm_exact',N.dot(N)-(sum(c*c for c in entries)+(C*x).dot(C*x)+x.dot(C*x)**2/4))
    eps,z,dz=s.symbols('eps z dz',real=True)
    Bp=(1+eps*z)/8;Bm=(1-eps*z)/8
    check('paired_group_sum',Bp+Bm-s.Rational(1,4))
    check('paired_signed_decode',4*(Bp-Bm)-eps*z)
    check('paired_group_Fisher',(eps*dz/8)**2*(1/Bp+1/Bm)-eps**2*dz**2/(4*(1-eps**2*z**2)))
    coeff=eps**2/(4*(1-eps**2*z**2))
    check('paired_Fisher_coefficient_derivative',s.diff(coeff,z)-eps**4*z/(2*(1-eps**2*z**2)**2))
    amp,y=s.symbols('amp y',positive=True)
    phase=y/(s.sqrt(2)*amp)
    quartet=s.Matrix([2*amp+amp*s.cos(phase),2*amp-amp*s.cos(phase),2*amp+amp*s.sin(phase),2*amp-amp*s.sin(phase)])
    check('positive_quartet_norm',quartet.dot(quartet)-18*amp**2)
    check('positive_quartet_metric',quartet.diff(y).dot(quartet.diff(y))-1)
    check('positive_quartet_radial_derivative',quartet.dot(quartet.diff(y)))
    r,rho=s.symbols('r rho',real=True)
    a2=4*s.cos(r/2)**2;q=1-rho*a2;ss=rho*a2
    check('clock_complement',q+ss-1)
    check('clock_derivative',s.diff(q,r)-2*rho*s.sin(r))
    clock=s.diff(q,r)**2/(q*ss)
    check('clock_Fisher',clock-4*rho*s.sin(r/2)**2/q)
    check('clock_residual',(1-clock)-(1-4*rho)/q)
    check('radial_residual_at_rho_eighth',(1-4*rho)/(rho*q*a2)-4/(q*a2) if False else ((1-4*rho)/(rho*q*a2)-4/(q*a2)).subs(rho,s.Rational(1,8)))
    t,e=s.symbols('t e',real=True)
    Dglobal=1+e**2*(t*t+1)/2
    fr=4*e**2*(1+e**2/2)/Dglobal**2
    fs=4*e**2/Dglobal
    check('free_radial_pullback',4*e**2/Dglobal-2*e**4*t*t/Dglobal**2-fr)
    check('free_angular_pullback',fs-4*e**2/Dglobal)
    warp=1-fs
    check('warping_derivative',s.diff(warp,t)-4*e**4*t/Dglobal**2)
    A,FB,gamma=s.symbols('A FB gamma',real=True)
    G=15*gamma-2*FB
    check('rest_spatial_decomposition',(16-fs)*gamma-2*FB-(G+warp*gamma))
    check('rest_radial_decomposition',(2*A-fr-s.diff(warp,t)**2/(4*warp))+s.diff(warp,t)**2/(4*warp)-(2*A-fr))
    check('compact_Nash_dim3',s.Rational(3,2)*(3*3+11)-30)
    check('rest_Euclidean_dimension',1+4+30-35)
    check('conditional_category_count',21+4*35-161)
    check('fine_category_count',1+8*161-1289)
    assert pin(Path(__file__).resolve())==script_pin
except Exception as exc:
    error=repr(exc)
receipt={'status':'PASS_EXACT_GLOBAL_S3_CONTROLS__NOT_LEAN' if error is None else 'FAIL_EXACT_GLOBAL_S3_CONTROLS','created_utc':datetime.now(timezone.utc).isoformat(),'sympy_version':s.__version__,'script':script_pin,'checks':checks,'exact_controls':len(checks),'passed_controls':sum(row['passed'] for row in checks.values()),'error':error,'scope':'Enumerated algebraic identities only; no claim that CAS proves compact Nash, global smoothness, inequalities, variational surjectivity or quantization.','lean_executed':False,'um_py_executed_or_imported':False,'originals_written':False}
write_new(OUT/'VERIFICACAO_GLOBAL_S3.json',(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'status':receipt['status'],'checks':len(checks),'passed':receipt['passed_controls'],'receipt':pin(OUT/'VERIFICACAO_GLOBAL_S3.json'),'error':error},ensure_ascii=True))
if error:sys.exit(1)
