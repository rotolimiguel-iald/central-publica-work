"""Conditional scalar completion with the existing Cartan cancellation; no data fit."""
from pathlib import Path
import hashlib, json, sys
import sympy as s

BASE = Path(__file__).resolve().parent

def pin(path):
    raw = Path(path).read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))

def emit(name, obj):
    with (BASE / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    phase = sys.argv[1]
    if phase == 'plan':
        emit('PLAN_R9.json', {
            'status': 'INPUT_CONDITIONAL_SCALAR_BRANCH_NOT_CANONICAL_IDENTIFICATION',
            'assumptions': ['Four dimensions; F>0; no connection spin source.',
                'Real scalar independent of metric; original kinetic Z; minimally coupled matter.',
                'Static weak field; constant background; V=Vprime=0 at background.',
                'Dust matter; no additional modular stress/source at this order.',
                'Cartan connection eliminated as in the existing density identity.',
                'Yukawa branch requires Z0>0 and Vsecond>=0; isolated decaying solution.',
                'Point source exterior is an analytic control, not a galaxy likelihood.'],
            'checks': ['Induced kinetic term cancels the metric mixing exactly.',
                'Trace substitution yields the sourced scalar equation.',
                'Yukawa Green solution satisfies exterior radial equation and delta normalization.',
                'Two metric potentials sum to the ordinary Weyl potential at this order.',
                'Radial force and its logarithmic contrast; massless limit removed by common offset.',
                'Z0=0 is an algebraic branch and must not be divided by zero.'],
            'source_receipt': pin(BASE / 'SOURCE_CURRENT_R9.json'),
            'script': pin(__file__), 'observed_data': False, 'parameters_fitted': False,
            'beta_amplitude_assumed': False})
        print('PLAN_WRITTEN')
        raise SystemExit(0)
    if phase != 'run':
        raise ValueError(phase)
    output = BASE / 'RESULT_R9.json'
    if output.exists():
        raise FileExistsError(output)
    plan = json.loads((BASE / 'PLAN_R9.json').read_text(encoding='utf-8'))
    for item in [plan['script'], plan['source_receipt']]:
        assert pin(item['path']) == item
    F, Z, r, M, mu = s.symbols('F0 Z0 r M mu', positive=True)
    Fp, rho, delta, lapdelta, Vpp = s.symbols('Fprime rho delta lapdelta Vsecond', real=True)
    eta = s.symbols('eta', real=True)  # 0: Cartan; 1: Levi-Civita only
    Zj = Z - (1-eta)*3*Fp**2/(2*F)
    Ricci = (rho + 3*Fp*lapdelta)/F
    scalar = s.expand(Zj*lapdelta - Vpp*delta + Fp*Ricci/2)
    expected = (Z + eta*3*Fp**2/(2*F))*lapdelta - Vpp*delta + Fp*rho/(2*F)
    checks = {'trace_substitution': s.simplify(scalar-expected),
              'cartan_kinetic_cancellation': s.simplify((Zj+3*Fp**2/(2*F)).subs(eta,0)-Z)}
    amplitude = Fp*M/(8*s.pi*F*Z)
    field = amplitude*s.exp(-mu*r)/r
    lap = s.diff(r*r*s.diff(field,r),r)/(r*r)
    checks['exterior_helmholtz'] = s.simplify(lap-mu**2*field)
    checks['delta_flux_normalization'] = s.simplify(s.limit(4*s.pi*r*r*s.diff(field,r),r,0) + Fp*M/(2*F*Z))
    W = -M/(8*s.pi*F*r)
    U = W-Fp*field/(2*F)
    spatial = W+Fp*field/(2*F)
    a = Fp**2/(2*F*Z)
    checks['weyl_sum'] = s.simplify(U+spatial-2*W)
    checks['temporal_potential'] = s.simplify(U-W*(1+a*s.exp(-mu*r)))
    checks['spatial_potential'] = s.simplify(spatial-W*(1-a*s.exp(-mu*r)))
    force_ratio = s.simplify(s.diff(U,r)/s.diff(W,r))
    checks['force_ratio'] = s.simplify(force_ratio-(1+a*(1+mu*r)*s.exp(-mu*r)))
    r1,r2 = s.symbols('r1 r2',positive=True)
    contrast = s.log(force_ratio.subs(r,r1))-s.log(force_ratio.subs(r,r2))
    checks['massless_common_offset_removed'] = s.simplify(contrast.subs(mu,0))
    checks['zero_coupling'] = s.simplify(contrast.subs(Fp,0))
    checks['zero_kinetic_algebraic_branch'] = s.simplify(scalar.subs({eta:0,Z:0})-(-Vpp*delta+Fp*rho/(2*F)))
    assert all(value == 0 for value in checks.values()), checks
    emit('RESULT_R9.json', {
        'status': 'PASS_SYMBOLIC_WITH_NAMED_ASSUMPTIONS',
        'checks': {key: str(value) for key,value in checks.items()},
        'cartan_equation': 'Z0 lap(deltaPsi) - Vsecond deltaPsi = -Fprime rho/(2 F0)',
        'cartan_mu_squared': 'Vsecond/Z0',
        'cartan_amplitude': str(a), 'point_source_field': str(field),
        'potentials': {'U':str(s.factor(U)), 'V':str(s.factor(spatial))},
        'force_ratio':str(force_ratio), 'radial_log_contrast':str(contrast),
        'covariance_of_contrast': 'C11+C22-2*C12',
        'important': ['No claim that the original one-form is this scalar.',
            'Beta does not appear without a supplied modular/background relation.',
            'Z=0 is excluded from Yukawa expressions, with a separate algebraic equation recorded.',
            'No observed likelihood, no significance calculated, no universal absence claim.',
            'Gstar=1/(8*pi*F0) in natural units is not automatically laboratory G.'],
        'plan':pin(BASE/'PLAN_R9.json'), 'script':pin(__file__),
        'sympy_version':s.__version__, 'observed_data':False})
    print(json.dumps({'status':'PASS','exact_zero_checks':len(checks), 'result':pin(output)},ensure_ascii=False))
