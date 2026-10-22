"""Symbolic calibration, identifiability and conditional precision, no observed input."""
import sympy as s,json,hashlib,datetime
from pathlib import Path
p=Path(__file__).resolve().parent; out=p/'RESULT_R16.json'
if out.exists():raise FileExistsError(out)
f,D,C,G=s.symbols('f D C G',positive=True)
q,ql,Cg,M=s.symbols('q ql Cg M',positive=True)
pi=s.pi
root=C*(1+s.sqrt(1+64*pi*G*D/C))/(32*pi*G)
checks={}
def check(n,v):
    r=s.simplify(v);checks[n]=str(r)
    if r!=0:raise AssertionError((n,r))
check('calibration_positive_root',16*pi*G*root**2-C*root-C*D)
check('zero_amplitude_limit',root.subs(D,0)-C/(16*pi*G))
Ml=Cg*M/(C*(1+ql));Md=Cg*(1+q)*M/(C*(1+ql))
check('ratio_cancels_mass_and_lab',Md/Ml-(1+q))
check('optical_ratio',Ml/Md-1/(1+q))
vl,vd,cld=s.symbols('vL vD cLD',real=True)
cov=s.Matrix([[vl,cld],[cld,vd]])
J=s.Matrix([[1,0],[1,1/(1+q)]])
F=J.T*cov.inv()*J
varq=s.factor(F.inv()[1,1])
check('full_covariance_varq',varq-(1+q)**2*(vl+vd-2*cld))
check('contrast_covariance',(s.Matrix([[-1,1]])*cov*s.Matrix([-1,1]))[0]-(vl+vd-2*cld))
check('fisher_positive_det',s.factor(F.det())-1/((1+q)**2*(vl*vd-cld**2)))
lensJ=s.Matrix([[1,0]])
check('lens_only_rank_defect',(lensJ.T*lensJ/vl).det())
bad=s.factor((C*(f+D)/(16*pi*f*f)/G-1).subs(f,1/(16*pi*G)))
assert bad!=0
ignored_cov=s.expand((1+q)**2*(vl+vd)-varq)
assert ignored_cov!=0
record={'status':'PASS_CONDITIONAL_CALIBRATION__NO_NUMERIC_SIGMA',
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'plan_sha256':hashlib.sha256((p/'PLAN_R16.json').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'sympy':s.__version__,'checks':checks,'negative_controls':{'bare_equals_measured_residual':str(bad),'ignore_cross_covariance_variance_error':str(ignored_cov)},
 'formulae':{'f0_positive_root':str(root),'Mlens_over_trueMass':str(Ml/M),'Mdyn_over_trueMass':str(Md/M),'Var_q':str(varq),'forecast_Z_logcontrast':'abs(log(1+q_TGL))/sqrt(vL+vD-2cLD)','required_logcontrast_sigma_5':'abs(log(1+q_TGL))/5'},
 'forecast_sigma':None,'observed_sigma':None,'reason':'No independently fixed field amplitude or observational covariance. Null is unknown, not zero significance.',
 'conditions':['Covariance positive definite; log observables Gaussian approximation and all relevant nuisance covariance included.', 'q is a local diagnostic symbol, not the canonical optical q in1=q^2+alpha^2.', 'Fisher invertibility presumes a common physical mass and source tracer model; independent unconstrained mass factors restore degeneracy.', 'No chosen numerical q or fit; test of q=0 alone is not unique theory discrimination.']}
with out.open('x',encoding='utf-8') as h:json.dump(record,h,ensure_ascii=False,indent=2)
print(json.dumps({'status':record['status'],'checks':len(checks),'negative_controls':2}))
