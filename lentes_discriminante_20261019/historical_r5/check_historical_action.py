"""Symbolic consistency of the historical scalar-photon delay attribution.

Fixed smooth background, nonzero Z, geometric optics; not full TGL metric solution.
"""
from pathlib import Path
import datetime,hashlib,json,re,time
import sympy as sp
ROOT=Path(__file__).resolve().parent
UM=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
OLD=Path(r'C:\IALD\INDICE_DO_ACERVO\corpus\16\161c7ab84cbcdc7f3b982403a174950c038d327a.txt')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(n,d):
    with (ROOT/n).open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2,allow_nan=False)
def main():
    for n in ['PLAN_R5.json','ACTION_RESULT_R5.json']:
        if (ROOT/n).exists():raise FileExistsError(n)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); tic=time.perf_counter()
    save('PLAN_R5.json',{'status':'SYMBOLIC_PRECOMPUTATION','started_utc':start,
      'scope':'Scalar electromagnetic prefactor on fixed smooth background; geometric optics, Z nonzero. No observed likelihood. Metric backreaction and finite-frequency scattering excluded from zero-leading-delay claim.',
      'checks':['1D Euler-Lagrange reduction under A=u/sqrt(Z)','transverse principal symbol','constant-Z no direct phase delay','historical c-power consistency','SIS conditional source-coordinate scaling'],
      'inputs':'Historical coefficient3.1e8 evaluated at synthetic sigma250km/s only, not an observed sample or fitted prediction.',
      'sources':[pin(UM),pin(OLD)],'script':pin(Path(__file__))})
    x,t=sp.symbols('x t',real=True); Z=sp.Function('Z')(x); u=sp.Function('u')(x,t)
    A=u/sp.sqrt(Z)
    # Maxwell transverse scalar in a static 1D Z background, units c=1.
    reduced=sp.simplify(sp.sqrt(Z)*(sp.diff(A,t,2)-sp.diff(A,x,2)-sp.diff(Z,x)/Z*sp.diff(A,x)))
    potential=sp.diff(Z,x,2)/(2*Z)-sp.diff(Z,x)**2/(4*Z**2)
    expected=sp.diff(u,t,2)-sp.diff(u,x,2)+potential*u
    assert sp.simplify(reduced-expected)==0
    assert sp.simplify(potential-sp.diff(sp.sqrt(Z),x,2)/sp.sqrt(Z))==0
    omega,k,z0=sp.symbols('omega k z0', real=True,nonzero=True)
    principal=z0*(-omega**2+k**2)
    assert sp.simplify(principal.subs(omega,k))==0
    assert potential.subs({sp.diff(Z,x):0,sp.diff(Z,x,2):0})==0
    # Two different explicit printed definitions: c^4 vs c^2 inversion.
    xi,RE,c,alpha=sp.symbols('xi RE c alpha',positive=True)
    alpha_c4=xi*(RE/c**2)**2
    inverse_c4=sp.solve(sp.Eq(alpha,alpha_c4),xi)[0]
    printed_inverse=alpha*c**2/RE**2
    assert sp.simplify(inverse_c4/printed_inverse)==c**2
    # SIS at fixed source angle and at fixed normalized source offset.
    b,y,vdisp,d,Dc,u0=sp.symbols('b y vdisp d Dc u0',positive=True)
    b_expr=4*sp.pi*(vdisp/c)**2*d
    delay_fixed_y=2*Dc*b_expr*y
    delay_fixed_u=sp.simplify(delay_fixed_y.subs(y,u0*b_expr))
    exponent_y=sp.simplify(vdisp*sp.diff(delay_fixed_y,vdisp)/delay_fixed_y)
    exponent_u=sp.simplify(vdisp*sp.diff(delay_fixed_u,vdisp)/delay_fixed_u)
    assert exponent_y==2 and exponent_u==4
    canonical=UM.read_text(encoding='utf-8')
    c_si=float(re.search(r'^C_LIGHT\s*=\s*([0-9.eE+-]+)',canonical,re.M).group(1))
    synthetic_v=250000.0; stated_alpha=3.1e8
    fractional=stated_alpha*(synthetic_v/c_si)**4
    out={'status':'DERIVED_FIXED_BACKGROUND_NOT_FULL_TGL','principal_transverse':'Z(-omega^2+k^2); Z nonzero implies null cone',
      'reduced_equation':str(expected),'finite_frequency_effective_potential':str(potential),
      'meaning':'Smooth Z changes transport and may scatter/shift finite-frequency packets; no additional frequency-independent geometric-optics refractive delay at fixed metric. Zero or discontinuous Z outside stated scope.',
      'constant_Z_control':'No direct EM phase delay, even if background scalar modulus is nonzero.',
      'printed_c_power_ratio':str(sp.simplify(inverse_c4/printed_inverse)),
      'dimensional_caveat':'This compares explicit printed formulas. R_E physical length vs angle is not fixed uniformly in source; natural-unit conventions cannot repair mixed SI numeric use without a conversion contract.',
      'SIS_sigma_exponent_fixed_source_angle':str(exponent_y),'SIS_sigma_exponent_fixed_normalized_source_offset':str(exponent_u),
      'synthetic_source_formula_check':{'sigma_m_s':synthetic_v,'c_runtime_m_s':c_si,'historical_alpha_input':stated_alpha,'fractional_excess':fractional,'percent_excess':100*fractional,'scope':'Internal arithmetic only; no observed-data aggregate or significance.'},
      'required_physical_inputs':['same-action solution for metric and scalar profile with boundary conditions','canonical distinction xi vs beta and photon coefficient lambda','observer clock and two-path difference, including redshift convention','joint stellar dynamics and lens potential with uncertainties'],
      'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-tic,
      'plan':pin(ROOT/'PLAN_R5.json'),'script':pin(Path(__file__))}
    save('ACTION_RESULT_R5.json',out)
    print(json.dumps({'status':out['status'],'synthetic_fractional_excess':fractional,'c_power_ratio':out['printed_c_power_ratio'],'SIS_exponents':[str(exponent_y),str(exponent_u)]}))
if __name__=='__main__':main()
