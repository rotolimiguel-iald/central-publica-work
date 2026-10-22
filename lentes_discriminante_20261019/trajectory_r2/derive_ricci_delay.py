"""Derive the literal Ricci-FF action; conditional synthetic scales, no observed data."""
from pathlib import Path
import datetime, hashlib, json, math, re
import sympy as s

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')

def pin(path):
    raw = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def save(name, obj):
    raw = json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8')
    with (ROOT / name).open('xb') as f:
        f.write(raw)

def main():
    for name in ['RICCI_CALCULATION_PLAN_R2.json', 'RICCI_CALCULATION_RESULT_R2.json']:
        if (ROOT / name).exists():
            raise FileExistsError(name)
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save('RICCI_CALCULATION_PLAN_R2.json', {
        'created_utc': start, 'status': 'INPUT_ANALYTIC_AND_SYNTHETIC_ONLY',
        'action': '-F_ab F^ab/4 + q R_ab F^{ac} F^b_c',
        'conventions': 'metric (-+++), symmetric Ricci, q=beta*l_P^2; local inertial geometric optics, first order qR',
        'background': 'fixed weak GR dust metric, negligible photon backreaction, no claim full TGL metric constructed',
        'checks': ['six independent exact action derivatives versus antisymmetric H',
                   'transverse diagonal-Ricci dispersion derived from H',
                   'vacuum R_ab=0', 'R_ab=Lambda*g_ab gives no cone displacement'],
        'synthetic_column_differences_kg_m2': [1, 10, 1000],
        'lens_redshift': 0.5,
        'scope': 'Illustrative matter columns, NOT lens data, NOT a forecast of the full TGL. No observed likelihood or gate.',
        'script': pin(Path(__file__)), 'canonical_program': pin(SOURCE)
    })
    g = s.diag(-1, 1, 1, 1)
    pairs = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    fs = s.symbols('f01 f02 f03 f12 f13 f23')
    F = s.zeros(4)
    for (a, b), f in zip(pairs, fs):
        F[a,b], F[b,a] = f, -f
    R = s.zeros(4)
    for a in range(4):
        for b in range(a, 4):
            R[a,b] = R[b,a] = s.Symbol(f'r{a}{b}')
    q = s.Symbol('q', real=True)
    Fu = g*F*g
    L = -sum(F[a,b]*Fu[a,b] for a in range(4) for b in range(4))/4
    L += q*sum(R[a,b]*Fu[a,c]*g[c,c]*Fu[b,c]
               for a in range(4) for b in range(4) for c in range(4))
    # H=-2*dL/dF when both antisymmetric entries are varied together.
    # Hence dL/df_ab=-H^ab for the six independent f_ab, a<b.
    B = (g*R)*Fu
    H = Fu - 2*q*(B - B.T)
    derivative_checks = [s.expand(s.diff(L,f)+H[a,b]) == 0
                         for (a,b), f in zip(pairs,fs)]
    assert all(derivative_checks)
    assert H + H.T == s.zeros(4)
    w,k = s.symbols('w k', real=True)
    kc = s.Matrix([-w,0,0,k])
    ac = s.Matrix([0,1,0,0])
    Fp = kc*ac.T - ac*kc.T
    diagR = {R[a,b]: 0 for a in range(4) for b in range(a+1,4)}
    Hp = H.subs(dict(zip(fs,[Fp[a,b] for a,b in pairs]))).subs(diagR)
    equation = s.expand((kc.T*Hp)[1])
    expected = -w*w+k*k - 2*q*(R[0,0]*w*w+R[3,3]*k*k+(-w*w+k*k)*R[1,1])
    assert s.expand(equation-expected) == 0
    n2 = s.solve(equation.subs(k*k,s.Symbol('n2')*w*w), s.Symbol('n2'))[0]
    dn2 = s.simplify(s.diff(n2,q).subs(q,0))
    assert s.simplify(dn2-2*(R[0,0]+R[3,3])) == 0
    lam = s.Symbol('Lambda')
    constant_curvature = s.simplify(equation.subs({R[0,0]:-lam,R[1,1]:lam,R[3,3]:lam}))
    assert s.expand(constant_curvature-(1-4*q*lam)*(-w*w+k*k)) == 0
    assert s.expand(equation.subs({R[0,0]:0,R[1,1]:0,R[3,3]:0})-(-w*w+k*k)) == 0
    text = SOURCE.read_text(encoding='utf-8')
    constants = {}
    for name in ['ALPHA_FINE_CODATA_2018','C_LIGHT','G_NEWTON','HBAR']:
        match = re.search(r'^\s*'+name+r'\s*=\s*([0-9.eE+-]+)\s*(?:#.*)?$',text,re.M)
        if not match:
            raise RuntimeError('Missing canonical numeric constant '+name)
        constants[name] = {'value': float(match.group(1)), 'line': text[:match.start()].count('\n')+1}
    alpha,c,G,hbar = [constants[n]['value'] for n in ['ALPHA_FINE_CODATA_2018','C_LIGHT','G_NEWTON','HBAR']]
    beta = alpha*math.sqrt(math.e)
    lp2 = hbar*G/c**3
    qgeom = beta*lp2
    z = 0.5
    rows = []
    for dSigma in [1,10,1000]:
        dt = (1+z)*8*math.pi*qgeom*G*dSigma/c**3
        rows.append({'delta_column_kg_m2':dSigma,'delta_delay_s':dt,
                     'ideal_sigma_delay_for_median_5_s':abs(dt)/5})
    save('RICCI_CALCULATION_RESULT_R2.json', {
        'status':'DERIVED_CONDITIONAL_LITERAL_OPERATOR_NOT_FULL_TGL',
        'started_utc':start, 'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'exact_derivative_checks':derivative_checks, 'H_antisymmetric':True,
        'dispersion_diagonal_Ricci':str(equation), 'n_squared_exact_diagonal':str(n2),
        'd_n_squared_dq_at_zero':str(dn2),
        'constant_curvature_only_rescales_Maxwell':str(constant_curvature),
        'vacuum_extra_delay_zero':True,
        'general_first_order_cone':'(g^{ab}-2q R^{ab}) k_a k_b=0 + O(q^2)',
        'general_path_delay':'(1+z_l)*q/c * integral R_ab ell^a ell^b dl; ell=(1,n)',
        'dust_path_difference':'(1+z_l)*8*pi*q*G/c^3 * (Sigma_i-Sigma_j)',
        'constants_from_program':constants, 'beta_runtime':beta, 'planck_length_squared_m2':lp2,
        'q_m2':qgeom, 'synthetic_rows':rows,
        'scope':'Dust Ricci from leading GR Einstein equation; weak static thin lens; first-order geometric optics; no metric response, dispersion extension, stochastic delay or cosmological distance law inferred.',
        'plan':pin(ROOT/'RICCI_CALCULATION_PLAN_R2.json'), 'script':pin(Path(__file__)),
        'canonical_program':pin(SOURCE), 'sympy_version':s.__version__
    })
    print(json.dumps({'checks':len(derivative_checks)+3,'q_m2':qgeom,'synthetic_rows':rows},ensure_ascii=False))

if __name__ == '__main__':
    main()
