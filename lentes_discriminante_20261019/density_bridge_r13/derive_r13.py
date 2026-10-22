"""Conditional density-to-lens algebra. Never imports the scientific program."""
from pathlib import Path
import hashlib, json, datetime
import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'DERIVATION_R13.json'
if OUT.exists():
    raise FileExistsError(OUT)
plan = ROOT / 'PLAN_R13.json'
plan_hash = hashlib.sha256(plan.read_bytes()).hexdigest()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
r, R, z, a, rho, rho0, c, G, xi, C, m, eps, n = s.symbols(
    'r R z a rho rho0 c G xi C m eps n', positive=True)
theta, tc, A, ks, x = s.symbols('theta tc A kappa_s x', positive=True)
checks = {}
def check(name, expression):
    reduced = s.simplify(expression)
    checks[name] = str(reduced)
    if reduced != 0:
        raise AssertionError((name, reduced))

L2 = eps / (xi*C*G*rho*m)
check('density_spectral_substitution', (s.pi*n)**2/L2 - (s.pi*n)**2*xi*C*G*rho*m/eps)
check('clock_prefactor_squared', c*c/L2 - (xi*C*m*c*c/eps)*G*rho)
profile = rho0*a*a/(r*r+a*a)
Sigma = s.pi*rho0*a*a/s.sqrt(R*R+a*a)
M2 = 2*s.pi**2*rho0*a*a*(s.sqrt(R*R+a*a)-a)
M3 = 4*s.pi*rho0*a*a*(r-a*s.atan(r/a))
check('projected_mass_derivative', s.diff(M2,R)-2*s.pi*R*Sigma)
check('spherical_mass_derivative', s.diff(M3,r)-4*s.pi*r*r*profile)
vc2 = G*M3/r
check('circular_speed_limit', s.limit(vc2,r,s.oo)-4*s.pi*G*rho0*a*a)
alpha_hat = 4*G*M2/(c*c*R)
check('deflection_limit', s.limit(alpha_hat,R,s.oo)-8*s.pi**2*G*rho0*a*a/c**2)
root = s.sqrt(theta**2+tc**2)
F = root-tc*s.log((tc+root)/(2*tc))
alpha_reduced = A*(root-tc)/theta
check('fermat_potential_gradient', s.diff(A*F,theta)-alpha_reduced)
check('two_dimensional_poisson', s.diff(theta*s.diff(A*F,theta),theta)/theta-A/root)
check('coreless_limit', s.limit(F,tc,0,dir='+')-theta)
K2 = eps/(xi*C*G*m)
check('ruler_amplitude', (rho0*a*a).subs(a,s.sqrt(K2/rho0))-K2)
check('kinematics_lensing_relation', 8*s.pi**2*G*K2/c**2-2*s.pi*(4*s.pi*G*K2)/c**2)
primitive = s.atan(s.sinh(ks*x))/(c*ks)
check('static_null_time', s.diff(primitive,x)-1/(c*s.cosh(ks*x)))
beta, V0, hbar, t, Eref = s.symbols('beta V0 hbar t Eref', positive=True)
check('v394_fixed_spectrum_phase_beta', s.diff(2*V0*t/hbar,beta))

mp.mp.dps = 45
quadratures=[]
for RR,aa,rr in [(mp.mpf('0.2'),mp.mpf('0.7'),mp.mpf('1.3')),
                 (mp.mpf('1.1'),mp.mpf('0.3'),mp.mpf('0.8')),
                 (mp.mpf('4.0'),mp.mpf('1.2'),mp.mpf('2.0'))]:
    numeric=mp.quad(lambda zz:rr*aa*aa/(RR*RR+zz*zz+aa*aa),[-mp.inf,0,mp.inf])
    analytic=mp.pi*rr*aa*aa/mp.sqrt(RR*RR+aa*aa)
    error=abs(numeric-analytic)/abs(analytic)
    assert error < mp.mpf('1e-10')
    quadratures.append({'R':str(RR),'rc':str(aa),'rho0':str(rr),
                        'relative_error':str(error),'synthetic_dimensionless':True})

result={
 'status':'PASS_CONDITIONAL_ALGEBRA_ONLY', 'started_utc':started,
 'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'plan_sha256':plan_hash, 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'versions':{'sympy':s.__version__,'mpmath':mp.__version__},
 'symbolic_checks':checks,'quadratures':quadratures,
 'formulae':{
  'c_over_Lstar':'sqrt(xi*C*m*c^2/eps)*sqrt(G*rho)',
  'profile_b2':'rho0*rc^2/(r^2+rc^2)',
  'Sigma':'pi*rho0*rc^2/sqrt(R^2+rc^2)',
  'M_2D':'2*pi^2*rho0*rc^2*(sqrt(R^2+rc^2)-rc)',
  'M_3D':'4*pi*rho0*rc^2*(r-rc*atan(r/rc))',
  'K0_squared_conditional':'rho0*rc^2 = eps/(xi*C*G*m)',
  'v_c_infinity_squared':'4*pi*G*K0^2',
  'A':'8*pi^2*G*K0^2/c^2 * D_ls/D_s',
  'theta_c':'rc/D_l',
  'F(theta)':'sqrt(theta^2+theta_c^2)-theta_c*ln((theta_c+sqrt(theta^2+theta_c^2))/(2*theta_c))',
  'psi_halo':'A*F(|theta|)',
  'delay_ab':'D_dt/c * [ (|theta_a-y|^2-|theta_b-y|^2)/2 - A*(F(|theta_a|)-F(|theta_b|)) ]',
  'D_dt':'(1+z_l)*D_l*D_s/D_ls',
  'static_cosh_null_time':'[atan(sinh(kappa_s*x_b))-atan(sinh(kappa_s*x_a))]/(c*kappa_s)'
 },
 'limitations':[
  'The historic halo rc relation is approximate; imposing equality is named additional input.',
  'The scalar cavity is not a galactic photon propagator; no kappa_loss to kappa_modular identification.',
  'The lens equations use a named GR weak-field mass-source bridge, not the complete nonminimal action.',
  'Halo only, spherical, thin lens, small angles, infinite b=2 model; baryons and environment absent.',
  'Same effective metric/profile in GR gives the same delay. No beta-specific extra delay derived.',
  'No values of K0,rho0,rc,kappa,V0 or source position were fitted or inferred from observed delays.',
  'v394 finite construction reused by algebra only. No full build, new seal or 5sigma claimed.'
 ]}
with OUT.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'status':result['status'],'symbolic_checks':len(checks),'quadratures':len(quadratures)},ensure_ascii=False))
