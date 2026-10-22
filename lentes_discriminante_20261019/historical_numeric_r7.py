"""Audit printed historical lens numbers; no physical fit or observed data."""
from pathlib import Path
import json, hashlib, math, datetime
from fractions import Fraction

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'historical_r7'
SOURCE = Path(r'C:\IALD\IMac LA\Física - TGL\Projetos Python\papers_latex\tgl_observables_paper\tgl_cosmological_observables.tex')

def pin(p):
    b = Path(p).read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def save(name, obj):
    with (OUT / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for name in ['PLAN_R7.json', 'NUMERIC_R7.json']:
        if (OUT / name).exists():
            raise FileExistsError(name)
    lines = SOURCE.read_text(encoding='utf-8').splitlines()
    save('PLAN_R7.json', {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': pin(SOURCE), 'script': pin(__file__),
        'scope': 'Arithmetic and SI dimensional consistency of historical printed formulas; not a repaired TGL prediction.',
        'excerpts': [{'start': a, 'end': b, 'text': '\n'.join(lines[a-1:b])}
                     for a,b in [(43,57),(155,185)]],
        'tests': ['Evaluate printed 10^16*0.1*(2e5/3e10)^4 exactly.',
                  'Evaluate same coefficients with speed200km/s and c in SI, flag validity rather than promote result.',
                  'Evaluate hbar/(m*v) for5meV/c² and200km/s; compare to2.7kpc.',
                  'Record missing units/normalization for K0 and the path integral.'],
        'no_observed_data': True, 'no_parameter_fit': True,
        'constants': {'c_m_s': 299792458, 'hbar_J_s': 1.054571817e-34,
                      'eV_J': 1.602176634e-19, 'kpc_m': 3.0856775814913673e19},
        'constants_scope': 'SI constants and kpc conversion, not inferred from lens observations; hbar rounded conventional value.',
        'beta_not_used': 'xi=0.1 is the historical printed INPUT; it is not substituted by betaTGL.'})
    coefficient = Fraction(10**16, 10)
    printed = coefficient * Fraction(2*10**5, 3*10**10)**4
    c = 299792458
    velocity = 200000
    coherent_si = coefficient * Fraction(velocity, c)**4
    hbar, ev, kpc = 1.054571817e-34, 1.602176634e-19, 3.0856775814913673e19
    mass_kg = 0.005*ev/c**2
    length_m = hbar/(mass_kg*velocity)
    required_mass_ev = hbar*c**2/(2.7*kpc*velocity*ev)
    # Independent route through hbar*c in eV*m and v/c.
    route2_m = (hbar*c/ev)/(0.005*(velocity/c))
    assert math.isclose(length_m, route2_m, rel_tol=2e-15)
    save('NUMERIC_R7.json', {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'plan': pin(OUT/'PLAN_R7.json'), 'source': pin(SOURCE),
        'statute': 'DERIVED arithmetic; historical physical premises DECLARADO',
        'printed_delay_excess_exact': str(printed),
        'printed_delay_excess_fraction': float(printed),
        'printed_delay_excess_percent': 100*float(printed),
        'claimed_delay_excess_fraction': 0.1,
        'claim_over_printed_expression': 0.1/float(printed),
        'same_coefficients_SI_excess_fraction': float(coherent_si),
        'SI_scope': 'Not a new forecast: changing c to SI does not validate alpha or repair absent dimensions. Result is far outside a small perturbation.',
        'debroglie_length_m': length_m,
        'debroglie_length_kpc': length_m/kpc,
        'claimed_length_kpc': 2.7,
        'claimed_over_calculated_length': 2.7*kpc/length_m,
        'mass_eV_c2_required_for_2p7kpc': required_mass_ev,
        'mass_scope': 'Algebraic inverse check only; not a fitted or proposed TGL particle mass.',
        'dimensional_gaps': [
            'If |Psi|²/M_Pl² is dimensionless, its integral over physical dl has length; the printed multiplicative delay correction lacks an explicit inverse length or dimensionless path convention.',
            'For K0=L_star*sqrt(rho_mass), K0² has SI kg/m; G*M_lens² has kg*m³/s², so alpha has s²/m⁴, not dimensionless. A different rho/units convention must be supplied, not presumed.',
            'A proportionality |Psi|² proportional rho_DM alone does not specify its coefficient or a solution of the scalar/modular EOM.'],
        'conclusion': 'Printed10percent and2.7kpc cannot be imported as calibrated predictions from these formulas. No observed5sigma.'})
    print(json.dumps(json.loads((OUT/'NUMERIC_R7.json').read_text(encoding='utf-8')), ensure_ascii=False))
