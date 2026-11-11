"""Build H0DN baseline A,C without constructing or fitting observed y.

Pinned upstream preprocessing/covariance code is AST-derived in memory; original
files remain byte-identical. Run with --fetch once, then without network access.
"""
from __future__ import annotations
import argparse
import ast
import configparser
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import types
import urllib.request
import contextlib

import numpy as np
import pandas as pd
import scipy
from scipy import linalg

BASE = Path(__file__).resolve().parent
SOURCE = Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_018/h0dn_documentary_review')
COMMIT = 'cc0a4b9f36e65470d514f254a3c5cffa463fbd94'
MISSING = ['data/sn1a_calib.dat', 'data/sn1a_hf_pp.dat', 'data/sbf_calib.dat', 'data/sbf_hf.dat', 'data/megamaser.dat']
PKG = BASE / 'upstream/h0_constrainer/h0_constrainer'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_bytes(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == data:
        return
    temp = path.with_name(path.name + '.tmp')
    temp.write_bytes(data)
    assert temp.stat().st_size == len(data)
    os.replace(temp, path)


def write_json(path, obj):
    write_bytes(path, (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode())


def acquire(fetch=False):
    manifest = json.loads((SOURCE / 'UPSTREAM_MANIFEST.json').read_text('utf-8'))
    tree = json.loads((SOURCE / 'UPSTREAM_TREE.json').read_text('utf-8'))
    assert manifest['commit'] == tree['sha'] == COMMIT
    items = {x['path']: x for x in tree['tree'] if x['type'] == 'blob'}
    records = []
    paths = [x['path'] for x in manifest['files']] + MISSING
    old = {x['path']: x for x in manifest['files']}
    for rel in paths:
        dst = BASE / 'upstream' / rel
        origin = 'existing_documentary_snapshot'
        if rel in old:
            data = (SOURCE / 'upstream' / rel).read_bytes()
            assert sha(data) == old[rel]['sha256'], rel
        elif dst.exists():
            data = dst.read_bytes()
            origin = 'pinned_public_download_cached'
        else:
            if not fetch:
                raise FileNotFoundError('Missing pinned public input; rerun with --fetch: ' + rel)
            url = f'https://raw.githubusercontent.com/StefCas789/H0DN/{COMMIT}/{rel}'
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read()
            origin = 'pinned_public_download'
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert blob == items[rel]['sha'], rel
        assert len(data) == items[rel]['size'], rel
        write_bytes(dst, data)
        records.append({'path': rel, 'sha256': sha(data), 'git_blob_sha1': blob, 'bytes': len(data),
                        'url': f'https://raw.githubusercontent.com/StefCas789/H0DN/{COMMIT}/{rel}', 'origin': origin})
    return records


class RemoveFits(ast.NodeTransformer):
    def __init__(self):
        self.count = 0

    def visit_Assign(self, node):
        if any(isinstance(t, ast.Name) and t.id in {'alpha', 'alphavec', 'data', 'chisq'} for t in node.targets):
            node.value = ast.Constant(0.0)
            self.count += 1
        return self.generic_visit(node)


class ZeroObservationWrites(ast.NodeTransformer):
    def __init__(self):
        self.count = 0
        self.intercept_calls = 0

    def visit_Assign(self, node):
        if any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == 'yval' for t in node.targets):
            node.value = ast.Constant(0.0)
            self.count += 1
        # SBF magnitudes are not required by the variance-only intercept.
        if any(isinstance(t, ast.Name) and t.id == 'value' for t in node.targets):
            node.value = ast.Constant(None)
        return self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'compute_alpha':
            for keyword in node.keywords:
                if keyword.arg == 'mag':
                    keyword.value = ast.Constant(None)
            if node.args:
                node.args[0] = ast.Constant(None)
            self.intercept_calls += 1
        return self.generic_visit(node)


class ZeroMaserCenter(ast.NodeTransformer):
    def visit_Assign(self, node):
        if any(isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant) and t.slice.value == 'logh_value' for t in node.targets):
            node.value = ast.Constant(0.0)
        return self.generic_visit(node)


def load_module(name, transformer=None):
    code = (PKG / (name + '.py')).read_text('utf-8')
    tree = ast.parse(code)
    if transformer:
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)
        write_bytes(BASE / 'derived' / (name + '_variance_only.py'), (ast.unparse(tree) + '\n').encode())
    mod = types.ModuleType('h0_constrainer.' + name)
    mod.__package__ = 'h0_constrainer'
    mod.__file__ = str(PKG / (name + '.py'))
    sys.modules[mod.__name__] = mod
    setattr(sys.modules['h0_constrainer'], name, mod)
    exec(compile(tree, mod.__file__, 'exec'), mod.__dict__)
    return mod, tree


def build_only():
    package = types.ModuleType('h0_constrainer')
    package.__path__ = [str(PKG)]
    sys.modules['h0_constrainer'] = package
    config_reader, _ = load_module('config_reader')
    data_loader, _ = load_module('data_loader', ZeroMaserCenter())
    remove_fits = RemoveFits()
    intercept, intercept_tree = load_module('intercept', remove_fits)
    assert remove_fits.count == 9, remove_fits.count
    assert not any(isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id == 'mag' for n in ast.walk(intercept_tree))
    zero_writes = ZeroObservationWrites()
    equations, _ = load_module('equations', zero_writes)
    assert zero_writes.count == 15, zero_writes.count
    assert zero_writes.intercept_calls == 5

    # Keep the original main function only through build_equations. Never import
    # or execute the original solver, logger, CLI, or package __init__.
    tree = ast.parse((PKG / 'main.py').read_text('utf-8'))
    function = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'main')
    end = next(i for i, x in enumerate(function.body) if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'eq_data' for t in x.targets))
    function.body = function.body[:end + 1] + [ast.Return(ast.Call(func=ast.Name(id='locals', ctx=ast.Load()), args=[], keywords=[]))]
    tree = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(tree)
    assert not any(isinstance(n, ast.Name) and n.id in {'solver', 'logger'} for n in ast.walk(tree))
    write_bytes(BASE / 'derived/main_build_only.py', (ast.unparse(tree) + '\n').encode())
    namespace = dict(os=os, sys=sys, np=np, pd=pd, config_reader=config_reader, data_loader=data_loader, equations=equations)
    exec(compile(tree, 'main_build_only.py', 'exec'), namespace)

    config = configparser.ConfigParser()
    config.read(BASE / 'upstream/h0_constrainer/configs/base_variants_config.ini')
    config['DEFAULT']['datadir'] = str((BASE / 'upstream/data').resolve()) + os.sep
    config['DEFAULT']['verbose'] = 'False'
    config['DEFAULT']['warn'] = 'False'
    config['DEFAULT']['logfile'] = 'none'
    config['DEFAULT']['savefile'] = 'none'
    text = io.StringIO()
    config.write(text)
    write_bytes(BASE / 'baseline_build_only.ini', text.getvalue().encode())
    # No stdout should be emitted with these upstream flags. Fail rather than
    # copying an unexpected potentially observed value into a durable log.
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        state = namespace['main'](str(BASE / 'baseline_build_only.ini'))
    if captured.getvalue():
        raise RuntimeError('Unexpected upstream stdout; withheld from durable output')
    assert np.count_nonzero(state['eq_data']['yval']) == 0

    # Poison every magnitude/modulus center used by equation construction, in
    # memory only. The covariance and design must be bit-identical. The maser
    # distance/velocity normalization of its uncertainty is explicitly retained.
    poisoned = state.copy()
    for name in ['host_df', 'sn1a_calib_df', 'sbf_calib_df', 'sn1a_hf_df', 'sbf_hf_df', 'mm_df']:
        poisoned[name] = state[name].copy(deep=True)
        for column in ['mu_host', 'm0_Bi', 'mb', 'm110', 'M110', 'logh_value']:
            if column in poisoned[name]:
                poisoned[name][column] = np.nan
    call = next(x.value for x in function.body if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'eq_data' for t in x.targets))
    probe = eval(compile(ast.Expression(call), 'centers_poisoned_probe', 'eval'), {'equations': equations}, poisoned)
    assert np.array_equal(probe['coeffs'], state['eq_data']['coeffs'])
    assert np.array_equal(probe['covar'], state['eq_data']['covar'])
    assert np.count_nonzero(probe['yval']) == 0

    # Validate AST-derived uncertainty calculation against unchanged upstream
    # using synthetic inputs exclusively, across simple and correlated modes.
    original = {}
    exec(compile((PKG / 'intercept.py').read_text('utf-8'), 'synthetic_intercept_reference', 'exec'), original)
    synthetic = dict(mag=np.array([15., 16., 17.]), mag_err=np.array([.1, .12, .11]), vcorr=np.array([3000., 5000., 7000.]))
    checks = [{'equation_centers_poisoned_to_nan': True, 'A_C_bit_identical': True}]
    for mode in range(3):
        args = synthetic.copy()
        if mode:
            args.update(vcmb=np.array([3100., 5100., 7100.]), vhel=np.array([3050., 5050., 7050.]))
        if mode == 2:
            args['covar'] = np.eye(3) * .01 + np.ones((3, 3)) * .001
        ref = original['compute_alpha'](**args)
        args['mag'] = None
        got = intercept.compute_alpha(**args)
        assert ref[1] == got[1] and ref[3] == got[3]
        assert got[0] == got[2] == 0
        checks.append({'synthetic_mode': mode, 'same_uncertainty_and_ndof': True})
    return state, checks, {'intercept_assignments_disabled': remove_fits.count,
                           'observation_writes_zeroed': zero_writes.count,
                           'intercept_calls_without_magnitudes': zero_writes.intercept_calls}


def host_factors(state, n):
    arrays = {}
    records = []
    for kind, names, index, errors in [
        ('anchor', state['anchors'], state['anchor_index'], state['mu_anchor_error']),
        ('MAS', state['mas'], state['mas_index'], state['mas_error']),
        ('HMS', state['hms'], state['hms_index'], state['mu_hms_error']),
    ]:
        f = np.zeros((n, len(names)))
        for j, name in enumerate(names):
            wh = np.where(index == j)[0]
            f[wh, j] = errors[j]
            records.append({'family': kind, 'index': j, 'name': str(name), 'rows': wh.tolist(), 'sigma': float(errors[j]),
                            'upstream_semantics': 'off_diagonal_only' if kind == 'HMS' else 'all_pairs_including_diagonal'})
        arrays['factor_' + kind] = f
        arrays['factor_' + kind + '_names'] = np.array(names, dtype=str)
    return arrays, records


def numerical_checks(A, C, c, h_index):
    d, U = linalg.eigh(C)
    tol = 1e-10
    support = d > tol
    N = U[:, ~support]
    W = (U[:, support] / np.sqrt(d[support])).T
    X = W @ A
    u, s, vt = linalg.svd(X, full_matrices=False)
    assert np.linalg.matrix_rank(X) == A.shape[1]
    V = (vt.T / s**2) @ vt
    P = linalg.pinv(C, atol=tol, rtol=0)
    V_upstream = linalg.inv(A.T @ P @ A)
    B = np.column_stack([A, c])
    nuisance_rank = int(np.linalg.matrix_rank(W @ B))
    Q, sr, vtr = linalg.svd(W @ B, full_matrices=False)
    V_bias = (vtr.T / sr**2) @ vtr
    bias_response = V @ A.T @ P @ c
    scans = []
    for cutoff in [1e-8, 1e-10, 1e-12]:
        precision, rank = linalg.pinv(C, atol=cutoff, rtol=0, return_rank=True)
        cov = linalg.inv(A.T @ precision @ A)
        scans.append({'atol': cutoff, 'rank_C': int(rank), 'sigma_log10H0': float(np.sqrt(cov[h_index, h_index]))})
    result = {'symmetric_max_abs': float(np.max(np.abs(C - C.T))), 'min_eigenvalue': float(d[0]),
              'max_eigenvalue': float(d[-1]), 'min_positive_eigenvalue': float(d[support][0]),
              'rank_C': int(support.sum()), 'nullity_C': int((~support).sum()), 'rank_A': int(np.linalg.matrix_rank(A)),
              'rank_whitened_A': int(np.linalg.matrix_rank(X)), 'rank_whitened_A_plus_cepheid': nuisance_rank,
              'null_support_A_max_abs': float(np.max(np.abs(N.T @ A), initial=0)),
              'null_support_cepheid_max_abs': float(np.max(np.abs(N.T @ c), initial=0)),
              'condition_whitened_A': float(s.max()/s.min()),
              'sigma_log10H0_no_bias': float(np.sqrt(V[h_index, h_index])),
              'sigma_log10H0_free_cepheid_bias': float(np.sqrt(V_bias[h_index, h_index])),
              'sigma_cepheid_bias_mag': float(np.sqrt(V_bias[-1, -1])),
              'd_log10H0_d_ignored_cepheid_bias_mag': float(bias_response[h_index]),
              'normal_inverse_vs_whitened_SVD_max_abs': float(np.max(np.abs(V - V_upstream))),
              'cutoff_stability': scans,
              'psd_tolerance': tol, 'psd_pass': bool(d[0] >= -tol),
              'support_pass': bool(np.max(np.abs(N.T @ B), initial=0) < 1e-9)}
    assert result['psd_pass'] and result['support_pass']
    assert nuisance_rank == B.shape[1]
    return result, {'eigenvalues_C': d, 'whitener': W, 'null_basis': N, 'parameter_covariance': V,
                    'parameter_covariance_free_cepheid': V_bias, 'cepheid_bias_response': bias_response}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true')
    args = parser.parse_args()
    sources = acquire(args.fetch)
    state, tests, transformations = build_only()
    eq = state['eq_data']
    A, C = eq['coeffs'], eq['covar']
    h = int(eq['ihub'])
    hosts = state['host_df']
    host_lines = {}
    for line_number, text in enumerate((BASE / 'upstream/data/host_data.dat').read_text('utf-8').splitlines(), 1):
        fields = text.split('#', 1)[0].split()
        if len(fields) >= 6 and fields[0].lower() != 'host':
            key = (fields[0], fields[3], fields[4], fields[5])
            host_lines.setdefault(key, []).append(line_number)
    c = np.zeros(A.shape[0])
    c[:len(hosts)] = hosts['method'].astype(str).str.lower().str.startswith('ceph').to_numpy(dtype=float)
    rows = []
    for i in range(A.shape[0]):
        rows.append({'row': i, 'description': str(eq['eq_descr'][i]), 'shape': str(eq['eq_shape'][i]),
                     'covariance_description': str(eq['eq_covar'][i]), 'host': '', 'method': '', 'anchor': '', 'source': '',
                     'c_cepheid': float(c[i])})
    for i, (_, row) in enumerate(hosts.iterrows()):
        rows[i].update({key: str(row[key]) for key in ['host', 'method', 'anchor', 'source']})
        rows[i]['kind'] = 'host'
        rows[i]['MAS'] = str(row['mas_name'])
        rows[i]['HMS'] = str(row['hms_name'])
        key = tuple(str(row[k]) for k in ['host', 'method', 'anchor', 'source'])
        assert len(host_lines[key]) == 1, key
        rows[i]['source_file'] = 'data/host_data.dat'
        rows[i]['source_line'] = host_lines[key][0]
    counts = {'rows': int(A.shape[0]), 'parameters': int(A.shape[1]), 'host_rows': len(hosts),
              'cepheid_host_rows': int(c.sum())}
    for name in ['nsn1a', 'nsbf', 'nmm', 'ngroups_eq', 'nhosts']:
        counts[name] = int(eq[name])
    counts['sn1a_hubble_flow_objects'] = len(state['sn1a_hf_df'])
    counts['sbf_hubble_flow_objects'] = len(state['sbf_hf_df'])
    for label, df_name, start in [('sn1a_calibrator', 'sn1a_calib_df', 'ieq_sn1a_start'),
                                ('sbf_calibrator', 'sbf_calib_df', 'ieq_sbf_start'),
                                ('megamaser', 'mm_df', 'ieq_mm_start')]:
        df = state[df_name]
        if df is not None:
            for j, (_, row) in enumerate(df.iterrows()):
                r = rows[int(eq[start]) + j]
                r.update(kind=label, method=label)
                for key in ['host', 'name']:
                    if key in row:
                        r[key] = str(row[key])
    for label, key in [('sn1a_hubble_flow', 'ieq_h0_m1a'), ('sbf_hubble_flow', 'ieq_h0_msbf')]:
        if eq[key] is not None:
            rows[int(eq[key])].update(kind=label, method=label)
    groups = state['groups_df']
    for j, (_, row) in enumerate(groups.iterrows()):
        rows[len(hosts)+j].update(kind='group', method='group', host=str(row['host']), group=str(row['group']))
    checks, auxiliary = numerical_checks(A, C, c, h)
    factors, factor_records = host_factors(state, A.shape[0])
    host_reconstructed = np.zeros_like(C)
    host_reconstructed[np.arange(len(hosts)), np.arange(len(hosts))] = hosts['mu_error'].to_numpy() ** 2
    for kind in ['anchor', 'MAS', 'HMS']:
        term = factors['factor_' + kind] @ factors['factor_' + kind].T
        if kind == 'HMS':
            term -= np.diag(np.diag(term))
        host_reconstructed += term
    checks['host_covariance_factor_reconstruction_max_abs'] = float(np.max(np.abs(host_reconstructed[:len(hosts), :len(hosts)] - C[:len(hosts), :len(hosts)])))
    assert checks['host_covariance_factor_reconstruction_max_abs'] < 1e-15
    names = np.array([p['objname'] for p in eq['parinfo']], dtype=str)
    row_names = np.array([r['description'] for r in rows], dtype=str)
    temp = BASE / 'network.tmp.npz'
    np.savez_compressed(temp, A=A, C=C, c_cepheid=c, h_index=np.array(h, dtype=int),
                        param_names=names, row_names=row_names, **auxiliary, **factors)
    os.replace(temp, BASE / 'network.npz')
    write_json(BASE / 'rows.json', rows)
    write_json(BASE / 'factors.json', factor_records)
    write_json(BASE / 'parameters.json', [{'index': i, 'name': str(n)} for i, n in enumerate(names)])
    artifacts = {}
    for rel in ['network.npz', 'rows.json', 'parameters.json', 'factors.json', 'baseline_build_only.ini', 'build_network.py']:
        data = (BASE / rel).read_bytes()
        artifacts[rel] = {'sha256': sha(data), 'bytes': len(data)}
    for path in sorted((BASE / 'derived').glob('*.py')):
        data = path.read_bytes()
        artifacts[str(path.relative_to(BASE)).replace('\\', '/')] = {'sha256': sha(data), 'bytes': len(data)}
    manifest = {'status': 'REAL_COMPUTATIONAL_BUILD_NO_OBSERVED_FIT', 'commit': COMMIT,
                'baseline': 'upstream configs/base_variants_config.ini, output controls and isolated datadir only',
                'counts': counts, 'h_index': h, 'checks': checks, 'sources': sources, 'artifacts': artifacts,
                'transformations': transformations, 'synthetic_reference_tests': tests,
                'privacy': {'observed_y_constructed': False, 'observed_y_saved': False, 'observed_fit_executed': False,
                            'raw_public_sources_present_in_snapshot': True},
                'covariance_conditioning': ['Published uncertainties and covariance are used.',
                    'Redshifts/velocities condition peculiar-velocity variance and selection.',
                    'Megamaser nominal distance enters fractional distance uncertainty; nominal corrected velocity enters fractional velocity uncertainty.',
                    'Upstream public raw tables contain already-known centers; loaded only to reproduce source pipeline. No observed centers exported in derived products.',
                    'HMS terms add only offdiagonal covariance, with diagonal already contained in host mu_error.',
                    'No extra latent correlations introduced; missing cross-dataset covariance is not invented.'],
                'nuisance_convention': 'c_cepheid=+1 mag on retained host equations with method startswith ceph; zero on anchors/calibrators/flow/masers. A positive injected offset is added to host distance-modulus observations.',
                'runtime': {'python': sys.version.split()[0], 'numpy': np.__version__, 'scipy': scipy.__version__, 'pandas': pd.__version__}}
    write_json(BASE / 'MANIFEST.json', manifest)
    print(json.dumps({'counts': counts, 'checks': checks, 'network_sha256': artifacts['network.npz']['sha256']}, indent=2))


if __name__ == '__main__':
    main()
