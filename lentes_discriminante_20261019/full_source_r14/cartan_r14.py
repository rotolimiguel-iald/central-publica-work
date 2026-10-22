"""Check the already eliminated Cartan kinetic variation, with metric-dependent f."""
from pathlib import Path
import sympy as s,json,hashlib
p=Path(__file__).resolve().parent;out=p/'CARTAN_RESULT_R14.json'
if out.exists():raise FileExistsError(out)
x=s.symbols('x',real=True);f=s.Function('f')(x)
H=3/(2*f);L=H*s.diff(f,x)**2
Euler=s.diff(L,f)-s.diff(s.diff(L,s.diff(f,x)),x)
expected=3*s.diff(f,x)**2/(2*f*f)-3*s.diff(f,x,2)/f
check1=s.simplify(Euler-expected);assert check1==0
fbar,xi,Ak,boxdf,Rg=s.symbols('fbar xi Ak boxdf Rg')
Ef1=-3*boxdf/fbar
Tkin1=-2*xi*Ak**2*Ef1
Rgamma=Rg-3*boxdf/fbar
check2=s.simplify((-2*xi*Rg*Ak**2+Tkin1)-(-2*xi*Rgamma*Ak**2));assert check2==0
result={'status':'PASS_CONDITIONAL_SPINLESS_CARTAN','plan_sha256':hashlib.sha256((p/'PLAN_CARTAN_R14.json').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'checks':{'Euler_reduction':str(check1),'null_source_combination':str(check2)},
 'formulae':{'effective_kinetic':'3/(2f)*(partial f)^2','Ef':'3/(2f²)*(partial f)^2-3/f*box f',
 'Tkin':'-3/f df tensor df +3/(2f) g (df)^2 -2xi Ef A tensor A',
 'Tkin_linear':'6xi/fbar Abar tensor Abar box(deltaf)',
 'combined_null_curvature':'-2xi [R_g1-3box(deltaf)/fbar]*(Abar.k)^2'},
 'scope':'One-dimensional Euler identity tests coefficient algebra; Lorentzian formula follows contraction/product rule analytically. Spinless connection, f connection-independent, fixed asymptotic f; not the complete Dirac action.'}
with out.open('x',encoding='utf-8') as h:json.dump(result,h,indent=2)
print(json.dumps({'status':result['status'],'checks':2}))
