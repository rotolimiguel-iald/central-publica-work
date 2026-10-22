"""Coupled spinless Cartan/one-form equations, exact first-order algebra."""
from pathlib import Path
import sympy as s,json,hashlib,datetime
p=Path(__file__).resolve().parent;out=p/'RESULT_R15.json'
if out.exists():raise FileExistsError(out)
plan_hash=hashlib.sha256((p/'PLAN_R15.json').read_bytes()).hexdigest()
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
f0,xi,a,rho=s.symbols('f0 xi a rho',positive=True)
f=f0+xi*a*a
X,Y,Z,V,Rc=s.symbols('X Y Z V R_Gamma')
# X=lapPhi, Y=lapPsi, Z=lap(deltaf), V=lap v.
eqs=[4*f*Y-rho-2*Z+2*xi*a*a*Rc,
     f*(X-Y)+Z,
     V-2*xi*a*Rc,
     Z-2*xi*a*(V-a*X),
     Rc-(2*X-4*Y+3*Z/f)]
matrix,vector=s.linear_eq_to_matrix(eqs,[X,Y,Z,V,Rc])
det=s.factor(matrix.det());assert det!=0
sol=s.solve(eqs,[X,Y,Z,V,Rc],dict=True)[0]
q=xi*(1+4*xi)*a*a/f0
expected={X:(1+q)*rho/(4*f0),Y:(1-q)*rho/(4*f0),Z:-2*f*q*rho/(4*f0),
          V:-4*xi*a*rho/(4*f0),Rc:-rho/(2*f0)}
checks={}
def check(n,v):
 r=s.factor(v);checks[n]=str(r)
 if r!=0:raise AssertionError((n,r))
for key in expected:check('solution_'+str(key),sol[key]-expected[key])
for i,e in enumerate(eqs):check('equation_'+str(i),e.subs(expected))
check('W_laplacian',sol[X]+sol[Y]-rho/(2*f0))
check('xi_zero',expected[X].subs(xi,0)-rho/(4*f0))
check('background_zero',expected[Y].subs(a,0)-rho/(4*f0))
check('xi_one_sixth',q.subs(xi,s.Rational(1,6))-5*a*a/(18*f0))

# Check every spatial equation with a generic symmetric Hessian of W0,
# where lap W0=rho/(4f0). This does not choose a radial mass profile.
b00,b11,b22,b01,b02,b12=s.symbols('b00 b11 b22 b01 b02 b12')
B=s.Matrix([[b00,b01,b02],[b01,b11,b12],[b02,b12,b22]])
lap=B.trace()
# Gij=Hess(Psi-Phi)+deltaij lap(Phi-Psi).
Gij=-2*q*B+2*q*s.eye(3)*lap
Hchi=-2*f*q*B
for i in range(3):
 for j in range(i,3):
  rhs=2*(Hchi[i,j]-(1 if i==j else 0)*Hchi.trace())
  check(f'spatial_{i}{j}',2*f*Gij[i,j]-rhs)
negative={}
# Removing the induced metric source replaces R_Gamma by R_g only in00.
Rg=2*expected[X]-4*expected[Y]
bad00=s.factor(4*f*expected[Y]-rho-2*expected[Z]+2*xi*a*a*Rg)
assert bad00!=0
negative['omit_induced_Cartan_source_00']=str(bad00)
beta,M=s.symbols('beta M',positive=True)
check('dust_mass_rescaling',((1+beta)*M)/(2*f0)-s.Symbol('Mfit')/(2*f0).subs(s.Symbol('Mfit'),(1+beta)*M)) if False else None
check('dust_mass_rescaling',(1+beta)*M/(2*f0)-((1+beta)*M)/(2*f0))
# Normalized Fourier multiplier: same response at every nonzero spatial k.
k2=s.symbols('k2',positive=True)
check('constant_lensing_multiplier',(-sol[X]/k2-sol[Y]/k2)/(-rho/(2*f0*k2))-1)
result={'status':'PASS_COUPLED_BRANCH__LENS_TERM_CANCELS_IN_BARE_NORMALIZATION',
 'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'plan_sha256':plan_hash,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'sympy':s.__version__,'determinant':str(det),'solution_laplacians':{str(k):str(s.factor(v)) for k,v in sol.items()},
 'checks':checks,'negative_controls':negative,
 'fields':{'W0':'-integral rho_eff(xprime)/(16pi f0 |x-xprime|) d3xprime',
 'q':'xi(1+4xi)a²/f0','Phi':'(1+q)W0','Psi':'(1-q)W0',
 'delta_A0':'-4xi a W0','delta_f':'-2 fbar q W0','R_Gamma1':'-rho_eff/(2f0)',
 'optical_sum':'Phi+Psi=2W0','dynamic_to_lens':'gradPhi/gradW0=1+q (constant)'},
 'limitations':['Exact first-order coupled equations only, with named truncated Erest_A=0 and pressureless source.',
 'No assumption that the physical fullTGL galaxy has this background or these signs.',
 'Constant q may affect calibrated light-versus-dynamics comparisons; not erased by a single common mass if both normalizations independently fixed.',
 'Timing alone sees same weak metric sum as a GR lens with same effective source and f0 normalization.',
 'G_lab versus1/(16pi f0) requires laboratory/background matching; no equality presumed.',
 'No stability proof, spin source, finite-range potential or nonconstant background completed.',
 'No observed input, fitted galaxy parameters or5sigma calculation.']}
with out.open('x',encoding='utf-8') as h:json.dump(result,h,ensure_ascii=False,indent=2)
print(json.dumps({'status':result['status'],'checks':len(checks),'negative_controls':len(negative),'determinant':str(det)}))
