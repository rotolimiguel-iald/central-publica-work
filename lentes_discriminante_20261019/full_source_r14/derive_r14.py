"""Exact weak-field source projections; does not import um.py or read observations."""
import sympy as s
import json,hashlib,datetime
from pathlib import Path
P=Path(__file__).resolve().parent
out=P/'RESULT_R14.json'
if out.exists():raise FileExistsError(out)
plan_sha=hashlib.sha256((P/'PLAN_R14.json').read_bytes()).hexdigest()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
checks={};negative={}
def check(name,x):
 z=s.simplify(x);checks[name]=str(z)
 if z!=0:raise AssertionError((name,z))
t,x,y,z=s.symbols('t x y z',real=True);coords=[t,x,y,z]
Phi=s.Function('Phi')(x,y,z);Psi=s.Function('Psi')(x,y,z)
eta=s.diag(1,-1,-1,-1);h=s.diag(2*Phi,2*Psi,2*Psi,2*Psi)
trace=sum(eta[a,a]*h[a,a] for a in range(4))
def box(f):return sum(eta[a,a]*s.diff(f,coords[a],2) for a in range(4))
def lap(f):return sum(s.diff(f,v,2) for v in [x,y,z])
Ric=s.zeros(4)
for a in range(4):
 for b in range(4):
  Ric[a,b]=(sum(eta[j,j]*(s.diff(h[j,b],coords[j],coords[a])+s.diff(h[j,a],coords[j],coords[b])) for j in range(4))-box(h[a,b])-s.diff(trace,coords[a],coords[b]))/2
R=sum(eta[a,a]*Ric[a,a] for a in range(4))
Ein=Ric-eta*R/2
check('G00',Ein[0,0]-2*lap(Psi))
check('Gii_trace',sum(Ein[i,i] for i in range(1,4))-2*lap(Phi-Psi))
check('R_scalar',R-(2*lap(Phi)-4*lap(Psi)))
check('W_from_scalar_metric',2*Ein[0,0]+sum(Ein[i,i] for i in range(1,4))-2*lap(Phi+Psi))
k=s.Matrix([1,0,0,1]);check('null_k',(k.T*eta*k)[0])
check('hkk_equals_2W',(k.T*h*k)[0]-2*(Phi+Psi))
f,xi,Ak,R1,Tkk,Uzz,dWh=s.symbols('f xi Ak R1 Tkk Uzz delta_W_h',real=True)
# In harmonic gauge with (+---), Gkk=Delta(hkk)/2=Delta(W_n).
rhs=Tkk+2*xi*Uzz-2*xi*R1*Ak**2
Wlap=rhs/(2*f)
check('harmonic_null_source',2*f*Wlap-rhs)
check('zero_vector_background',Wlap.subs(Ak,0)-(Tkk+2*xi*Uzz)/(2*f))
negative['omitted_metric_norm_term']=str(s.simplify(Wlap-(Tkk+2*xi*Uzz)/(2*f)))
assert negative['omitted_metric_norm_term']!='0'

# Localized smooth test functions; density and curvature controls are synthetic,
# not proposed solutions of all material equations.
u=s.exp(-x*x-y*y-z*z)
boundary=s.integrate(s.diff(u,z,2),(z,-s.oo,s.oo))
check('localized_hessian_projection',boundary)
integrated_curvature=s.integrate(s.exp(-x*x-y*y-z*z),(z,-s.oo,s.oo))
check('curvature_projection_nonboundary_value',integrated_curvature-s.sqrt(s.pi)*s.exp(-x*x-y*y))
negative['curvature_projection_nonzero']=str(-xi*Ak**2*integrated_curvature/f)
assert negative['curvature_projection_nonzero']!='0'
L=s.symbols('L',positive=True)
check('finite_endpoint_hessian',s.integrate(s.diff(u,z,2),(z,-L,L))-(s.diff(u,z).subs(z,L)-s.diff(u,z).subs(z,-L)))
negative['finite_endpoint_not_zero']=str(s.simplify(s.diff(u,z).subs(z,L)-s.diff(u,z).subs(z,-L)))
assert negative['finite_endpoint_not_zero']!='0'

e,theta,theta0,dy,q=s.symbols('e theta theta0 dy q',real=True)
p=s.Function('p');dp=s.Function('dp');source=s.symbols('source',real=True)
fermat=(theta-source)**2/2-p(theta)-e*dp(theta)
der=s.diff(fermat.subs(theta,theta0+e*q),e).subs(e,0).doit()
stationary=s.simplify(der.subs(source,theta0-s.diff(p(theta0),theta0)))
check('stationary_fermat_variation',stationary+dp(theta0))

result={'status':'PASS_CONDITIONAL_NULL_PROJECTION','start_utc':start,'finish_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'plan_sha256':plan_sha,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'sympy':s.__version__,'checks':checks,'negative_controls':negative,
 'formulae':{'source':'2 f G_ab = T_ab +2xi(Hess_ab u-g_ab box u)-2xi R A_a A_b',
 'linear_lensing_projection':'2 fbar Delta W_n = deltaT_kk +2xi d_z^2 delta_u -2xi R1(Abar.k)^2',
 'W_n':'h_kk/2; equals Phi+Psi when a two-scalar Newtonian metric applies',
 'projected_potential':'J_n(x_perp)=integral W_n dz',
 'projected_equation':'Delta_perp J_n = integral[deltaT_kk-2xi R1(Abar.k)^2]dz/(2fbar)+xi/fbar[d_z delta_u]_ends-[d_z W_n]_ends',
 'psi_lens':'D_ls/(D_l D_s) J_n(D_l theta)',
 'gravity_delay':'-integral W_n dz/c',
 'first_order_pair_delay':'delta Delta t_ab= -D_dt/c[delta psi(theta_a)-delta psi(theta_b)], fixed source/distances, stationary unperturbed images',
 'source_modular_local':'T_mod_ab=beta[|1+w| T_L_ab-2 L sign(1+w) partial_w/partial_g^ab], only algebraic metric-dependence of w, beta metric-independent and w!=-1'},
 'scope':['No numerical galaxy parameters or observed delays','No assertion that the Gaussian controls solve all EOM','No scalar/one-form identification','R88 signature and energy-sign limitation retained','No proof that a nonzero candidate curvature term survives solving the full coupled EOM','Born/static weak-field; finite endpoints kept, no gauge-independent isolated travel-time claim','No fullTGL source fixed and no5sigma result']}
with out.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':result['status'],'checks':len(checks),'negative_controls':len(negative)}))
