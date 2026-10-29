"""Frozen A5/A6 finite experiment; no canonical imports, production writes, or observed data."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import math
import platform
import re
import sys
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ADENDO = HERE.parent
ROOT = ADENDO.parent
PREREG = ADENDO / 'PREREGISTRO_ADENDO1_R1.json'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def finite_array(a):
    a = np.asarray(a)
    if not np.all(np.isfinite(a)):
        raise ValueError('RECUSA_NONFINITE_ARRAY')
    return a


def norm(a):
    return float(np.linalg.norm(finite_array(a)))


def packed(a):
    a = finite_array(a)
    return np.stack([a.real, a.imag], axis=-1).tolist()


def finite_tree(value):
    if isinstance(value, dict):
        for child in value.values():
            finite_tree(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            finite_tree(child)
    elif isinstance(value, (float, np.floating)) and not math.isfinite(value):
        raise ValueError('RECUSA_NONFINITE_RESULT')


def write_new(path, value):
    finite_tree(value)
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    with Path(path).open('xb') as stream:
        stream.write(raw)
    assert Path(path).read_bytes() == raw


def source_snapshot(protocol, ancestor):
    pins = [(str(PREREG), digest(PREREG))]
    pins += [(x['path'], x['sha256']) for x in protocol['reuse']]
    pins += [(x['path'], x['sha256']) for x in ancestor['source_pins']]
    for x in protocol['verbatims']:
        pins += [(x['source'], x['sha256']), (x['custody'], x['sha256'])]
    out = []
    for path, expected in pins:
        actual = digest(path)
        if actual != expected:
            raise ValueError('RECUSA_SOURCE_CHANGED: ' + path)
        out.append({'path': path, 'sha256': actual})
    return out


def alpha_from_source(ancestor):
    pin = next(x for x in ancestor['source_pins'] if Path(x['path']).name == 'um.py')
    text = Path(pin['path']).read_bytes().decode('utf-8-sig')
    matches = list(re.finditer(r'^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([^\r\n]+)\r?$', text, re.MULTILINE))
    if len(matches) != 1:
        raise ValueError('RECUSA_ALPHA_ASSIGNMENT_NOT_UNIQUE')
    alpha = ast.literal_eval(ast.parse(matches[0].group(0)).body[0].value)
    tree = ast.parse(text)
    sealed = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SEALED_CODATA_ALPHA' for t in n.targets)]
    if len(sealed) != 1 or ast.literal_eval(sealed[0].value) != alpha:
        raise ValueError('RECUSA_ALPHA_SEALED_MISMATCH')
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)) or not math.isfinite(alpha):
        raise ValueError('RECUSA_ALPHA_TYPE_OR_FINITE')
    return alpha, {'path': pin['path'], 'sha256': pin['sha256'], 'line': text[:matches[0].start()].count('\n') + 1,
                   'origin': 'unique physical assignment in embedded module; outer sealed literal cross-check; no import or execution'}


def run():
    began = datetime.now(timezone.utc).isoformat()
    timer = time.perf_counter()
    manifest = json.loads((HERE / 'RUN_MANIFEST_R1.json').read_bytes())
    if digest(__file__) != manifest['script_sha256'] or digest(PREREG) != manifest['preregister_sha256']:
        raise ValueError('RECUSA_SCRIPT_OR_PREREG_CHANGED')
    p = json.loads(PREREG.read_bytes())
    ancestor = json.loads((ROOT / 'PREREGISTRO_R1.json').read_bytes())
    before = source_snapshot(p, ancestor)
    cfg = p['numeric']
    atol, rtol = cfg['atol'], cfg['rtol']
    threshold = cfg['rank_threshold']
    band_lo, band_hi = cfg['ambiguous_singular_band']
    def close(error, scale=1.):
        if not math.isfinite(error) or not math.isfinite(scale):
            raise ValueError('RECUSA_NONFINITE_COMPARISON')
        return bool(error <= atol + rtol * scale)
    def fixed_projection(T):
        T = finite_array(T)
        singular = np.linalg.svd(T - np.eye(len(T)), full_matrices=True)
        values, vh = finite_array(singular[1]), finite_array(singular[2])
        if np.any((values >= band_lo) & (values <= band_hi)):
            raise ValueError('RECUSA_RANK_AMBIGUOUS')
        basis = vh.conj().T[:, values < threshold]
        return basis @ basis.conj().T, basis.shape[1], values

    alpha, alpha_source = alpha_from_source(ancestor)
    beta = alpha * math.sqrt(math.e)
    if not 0. < beta < .5:
        raise ValueError('RECUSA_BETA_STRICT_RANGE')
    lam = 1. - 2. * beta
    I = np.eye(2, dtype=np.complex128)
    J = np.array([[0., 1.], [1., 0.]], dtype=np.complex128)
    Y = np.array([[0., -1j], [1j, 0.]], dtype=np.complex128)
    K = np.diag([1., -1.]).astype(np.complex128)
    basis = [x / math.sqrt(2.) for x in (I, J, Y, K)]
    def vec(A):
        return np.array([np.trace(b.conj().T @ A) for b in basis])
    def superop(f):
        return np.column_stack([vec(f(b)) for b in basis])
    def adj(A):
        return J @ A @ J
    def expectation(A):
        return (A + adj(A)) / 2.
    Ad, E = superop(adj), superop(expectation)
    rng = np.random.default_rng(cfg['seed'])
    operators = [rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)) for _ in range(cfg['random_operators'])]
    random_errors = []
    for F in operators:
        EF = expectation(F)
        random_errors.append({'E_idempotence': norm(expectation(EF) - EF),
                              'Ad_E': norm(adj(EF) - EF), 'E_Ad': norm(expectation(adj(F)) - EF),
                              'scale': norm(F)})
    a5_residuals = {'J_squared_I': norm(J @ J - I), 'JKJ_negative_K': norm(J @ K @ J + K),
                    'AdJ_fixes_J': norm(adj(J) - J), 'E_fixes_J': norm(expectation(J) - J),
                    'E_squared_E': norm(E @ E - E), 'Ad_E': norm(Ad @ E - E),
                    'E_Ad': norm(E @ Ad - E), 'E_K_zero': norm(expectation(K)), 'E_I': norm(expectation(I) - I)}
    Efix, Efixdim, Efixsv = fixed_projection(E)
    a5 = {'statute': 'REAL: finite algebra only; ONTO language not tested',
          'primary_residuals': a5_residuals,
          'random_operator_checks': {'count': len(operators), 'max_residuals': {k: max(row[k] for row in random_errors) for k in ('E_idempotence', 'Ad_E', 'E_Ad')},
                                     'all_pass': all(close(row[k], row['scale']) for row in random_errors for k in ('E_idempotence', 'Ad_E', 'E_Ad'))},
          'E_fixed_dimension': Efixdim, 'E_fixed_singular_values': Efixsv.tolist(), 'E_spectral_projection_error': norm(E - Efix),
          'matrices': {key: packed(value) for key, value in [('J', J), ('K', K), ('AdJ', Ad), ('E_J', E)]},
          'independent_reader_parameter': False,
          'literal_diagnostic': {'statement': 'J composed with J equals J', 'residual': norm(J @ J - J), 'verdict': 'PASSA' if close(norm(J @ J - J)) else 'FALHA'},
          'controls': {}}
    a5['verdict'] = 'PASSA' if all(close(v) for v in a5_residuals.values()) and a5['random_operator_checks']['all_pass'] else 'FALHA'
    Jbad = 2. * J
    Ebad = superop(lambda A: (A + Jbad @ A @ Jbad) / 2.)
    a5['controls']['K_identity'] = {'hypothesis_verdict': 'RECUSA_HIPOTESE_JKJ', 'JKJ_plus_K': norm(J @ I @ J + I), 'E_K_zero_error': norm(expectation(I)), 'self_reading_J_error': norm(expectation(J) - J)}
    a5['controls']['J_bad_twice_J'] = {'hypothesis_verdict': 'RECUSA_HIPOTESE_INVOLUCAO', 'formula': 'J_bad A J_bad, not similarity with inverse',
                                     'involution_error': norm(Jbad @ Jbad - I), 'E_idempotence_error': norm(Ebad @ Ebad - Ebad),
                                     'E_Jbad_error': norm((Jbad + Jbad @ Jbad @ Jbad) / 2. - Jbad)}

    S = np.array([[math.sqrt(1. - beta), math.sqrt(beta)], [-math.sqrt(beta), math.sqrt(1. - beta)]], dtype=np.complex128)
    def D(A):
        return np.diag(np.diag(A))
    C = superop(lambda A: D(S @ D(A) @ S.conj().T))
    T = np.abs(S) ** 2
    Dsup = superop(D)
    Rpop = np.ones((2, 2), dtype=np.complex128) / 2.
    Rden = np.diag([1., 0., 0., 0.]).astype(np.complex128)
    components_pop = [(lam, np.eye(2) - Rpop)]
    components_den = [(lam, np.diag([0., 0., 0., 1.])), (0., np.diag([0., 1., 1., 0.]))]
    def assess(name, channel, exact_R, components, admissible=True, supplied=None, old_R=None):
        intrinsic, dimfix, sv = fixed_projection(channel)
        readout = intrinsic if old_R is None else old_R
        residuals = {'RT': norm(readout @ channel - readout), 'TR': norm(channel @ readout - readout),
                     'R_squared_R': norm(readout @ readout - readout), 'R_star_R': norm(readout.conj().T - readout),
                     'R_is_Fix_projection': norm(readout - intrinsic), 'intrinsic_vs_exact': norm(intrinsic - exact_R)}
        powers = []
        for n in cfg['powers']:
            actual = np.linalg.matrix_power(channel, n)
            formula = exact_R.copy()
            for value, Q in components:
                formula = formula + value ** n * Q
            powers.append({'n': n, 'distance_to_readout': norm(actual - readout), 'formula_residual': norm(actual - formula)})
        exact_transient_contraction = all(abs(value) < 1. for value, _ in components)
        A1 = bool(exact_transient_contraction and close(powers[-1]['distance_to_readout']) and all(close(x['formula_residual']) for x in powers))
        A2 = close(residuals['RT']) and close(residuals['TR'])
        A3 = all(close(residuals[k]) for k in ('R_squared_R', 'R_star_R', 'R_is_Fix_projection'))
        return {'id': name, 'admissible': admissible, 'supplied_readout': supplied, 'intrinsic_readout_reconstructed': True,
                'fixed_dimension': dimfix, 'singular_values_T_minus_I': sv.tolist(),
                'residuals': residuals, 'powers': powers, 'exact_transient_contraction': exact_transient_contraction,
                'matrices': {'T': packed(channel), 'R_intrinsic': packed(intrinsic), 'R_evaluated': packed(readout)},
                'A1': 'PASSA' if A1 else 'FALHA', 'A2': 'PASSA' if A2 else 'FALHA', 'A3': 'PASSA' if A3 else 'FALHA',
                'A1_A2_A3_survive': A1 and A2 and A3}
    primary = [assess('primary_population', T, Rpop, components_pop), assess('primary_density', C, Rden, components_den)]
    ablations = [assess('T_zero_generator', I, I, [])]
    for name in ('T_zero_boundary_angle', 'L_beta_zero'):
        ablations += [assess(name + '_population', I, I, []), assess(name + '_density', Dsup, Dsup, [(0., np.eye(4) - Dsup)])]
    ablations += [assess('L_missing_supplied_readout_population', T, Rpop, components_pop, supplied='ABSENT_INTERFACE_REFUSAL'),
                  assess('L_missing_supplied_readout_density', C, Rden, components_den, supplied='ABSENT_INTERFACE_REFUSAL')]
    old_readout = assess('diagnostic_old_R_on_identity', I, I, [], admissible=False, supplied='OLD_WRONG_R', old_R=Rpop)
    N = max(cfg['powers'])
    x, total, samples = 0., 0., []
    for n in range(N):
        total += x
        if n in cfg['powers']:
            samples.append({'n': n, 'x_n': x})
        x += 1.
    samples.append({'n': N, 'x_n': x})
    affine = {'id': 'G_no_fixed_point', 'admissible': False, 'domain': 'external affine real line; not linear/CPTP',
              'iterations': N, 'trajectory_samples': samples, 'final_x': x, 'cesaro_0_to_N_minus_1': total / N,
              'closed_formula_x_error': abs(x - N), 'closed_formula_cesaro_error': abs(total / N - (N - 1.) / 2.),
              'A1_orbit': 'FALHA', 'A1_cesaro': 'FALHA', 'A2': 'NAO_APLICAVEL', 'A3': 'NAO_APLICAVEL',
              'analytic_reason': 'x_n=n and Cesaro_N=(N-1)/2 tend to +infinity; x+1=x has no real solution'}
    zero_support = {'id': 'G_no_support', 'admissible': False, 'dimension': 0, 'available_trace': 0., 'required_trace': 1.,
                    'verdict': 'RECUSA_NAO_VACUIDADE', 'A1': 'NAO_APLICAVEL', 'A2': 'NAO_APLICAVEL', 'A3': 'NAO_APLICAVEL',
                    'reason': 'No trace-one state; empty identities do not support minimality'}
    survivors = [x['id'] for x in ablations if x['admissible'] and x['A1_A2_A3_survive']]
    after = source_snapshot(p, ancestor)
    if before != after or digest(__file__) != manifest['script_sha256'] or digest(PREREG) != manifest['preregister_sha256']:
        raise ValueError('RECUSA_SOURCE_CHANGED_DURING_RUN')
    result = {'schema': 'F1.ATRATOR.ADENDO1.numeric-result/v1', 'started_utc': began, 'finished_utc': datetime.now(timezone.utc).isoformat(),
              'seconds': time.perf_counter() - timer, 'runtime': {'python': sys.version, 'numpy': np.__version__, 'platform': platform.platform(), 'dtype': cfg['dtype'], 'seed': cfg['seed']},
              'preregister_sha256': digest(PREREG), 'script_sha256': digest(__file__), 'numeric_contract': cfg,
              'alpha': alpha, 'beta_runtime': beta, 'lambda_runtime': lam, 'alpha_source': alpha_source,
              'A5': a5, 'primary': primary,
              'A6': {'target': p['A6']['target'], 'ablations': ablations, 'surviving_admissible_ablations': survivors,
                     'verdict': 'FALHA' if survivors else 'PASSA', 'diagnostic_old_readout': old_readout,
                     'external_affine_control': affine, 'no_support_control': zero_support,
                     'missing_readout_interface': 'RECUSA_R_NAO_FORNECIDO; reconstruction of the mathematical readout tested separately',
                     'scope': 'Operational minimality only; ONTO not tested; fixed dimension is separate and A4 is not substituted'},
              'sources_before': before, 'sources_after': after, 'all_source_pins_unchanged': True,
              'no_observed_data': True, 'gate_changed': False}
    finite_tree(result)
    write_new(HERE / 'RESULTADOS_ADENDO1_R1.json', result)
    print(json.dumps({'A5': a5['verdict'], 'A6': result['A6']['verdict'], 'survivors': survivors, 'result_sha256': digest(HERE / 'RESULTADOS_ADENDO1_R1.json')}, ensure_ascii=False))


if __name__ == '__main__':
    run()
