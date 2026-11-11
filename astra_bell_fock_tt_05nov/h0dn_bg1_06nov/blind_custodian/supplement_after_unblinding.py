"""Additive diagnostics on committed scores; no RNG and no estimator mutation."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
BASE = HERE.parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save_new(name, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    with (HERE/name).open('xb') as handle:
        handle.write(raw)

def wilson(success, n):
    p = success/n
    z = norm.ppf(.975)
    d = 1 + z*z/n
    center = (p + z*z/(2*n))/d
    radius = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return dict(success=int(success), total=int(n), estimate=p,
                ci95=[center-radius, center+radius])

freeze = json.loads((BASE/'FREEZE_R2.json').read_text(encoding='utf-8'))
for item in freeze['files']:
    assert sha(item['path']) == item['sha256'], item['path']
commit = json.loads((HERE/'SCORES_COMMIT.json').read_text())
assert sha(HERE/'SCORES_MANIFEST.json') == commit['manifest_sha256']
manifest = json.loads((HERE/'SCORES_MANIFEST.json').read_text())
result = json.loads((HERE/'UNBLINDED_RESULTS.json').read_text())
assert result['scores_commit_sha256'] == sha(HERE/'SCORES_COMMIT.json')
assert result['acknowledgment_sha256'] == sha(BASE/'ACK_SCORES.json')
with np.load(BASE/'estimator_frozen.npz', allow_pickle=False) as source:
    est = {k: source[k] for k in source.files}
with np.load(BASE/'network/network.npz', allow_pickle=False) as source:
    C = source['C'].copy()
    c = source['c_cepheid'].copy()

coverage = []
for case in result['outputs']:
    if case['kind'] != 'ordinary':
        continue
    blocks = sorted((x for x in manifest if x['case_id'] == case['id']),
                    key=lambda x: x['first'])
    scores = []
    for block in blocks:
        assert sha(block['score_path']) == block['score_sha256']
        with np.load(block['score_path'], allow_pickle=False) as source:
            scores.append(source['z_null_exact_bg'].copy())
    z = np.concatenate(scores)
    truth = case['hypothesis']*float(est['logK'])
    residual = z - truth/est['sd_null']
    coverage.append(dict(id=case['id'], hypothesis=case['hypothesis'],
        fixed_bias=case['fixed_bias'], random_sd=case['random_sd'],
        models=[dict(name=str(name), coverage95=wilson(
            np.count_nonzero(abs(residual[:,i]) <= norm.ppf(.975)), len(z)),
            residual_mean=float(residual[:,i].mean()),
            residual_sd=float(residual[:,i].std(ddof=1)))
            for i,name in enumerate(est['model_names'])]))

H0 = float(est['H0'])
n_local = C.shape[0]
sig_bg = float(np.sqrt(est['C_joint'][n_local,n_local]))
alpha = float(norm.sf(5))
quadrature = []
for index, name in enumerate(est['model_names']):
    sig_h = math.sqrt(float(est['weights'][index]@C@est['weights'][index]))
    sd0 = float(est['sd_null'][index])
    def tail(q, delta=0.):
        value, error = quad(lambda z: norm.pdf(z)*norm.sf(
            (q + math.log10(1+sig_bg*z/H0) - delta)/sig_h),
            -12., 12., epsabs=1e-17, epsrel=1e-11, limit=200)
        return float(value), float(error)
    q0 = 5*sd0
    threshold = brentq(lambda q: tail(q)[0]-alpha, 4.5*sd0, 5.5*sd0,
                      xtol=1e-15, rtol=1e-14)
    original_tail, original_error = tail(q0)
    calibrated_tail, calibrated_error = tail(threshold)
    original_power, original_power_error = tail(q0, float(est['logK']))
    calibrated_power, calibrated_power_error = tail(threshold, float(est['logK']))
    observed = next(x for x in result['outputs'] if x['kind']=='importance' and x['model']==index)
    mc_exact = next(x for x in observed['models'] if x['score']=='z_null_exact_bg')
    quadrature.append(dict(name=str(name), local_sigma=sig_h,
        original_q=q0, original_q_over_sd0=5., original_tail=original_tail,
        original_tail_quad_error=original_error,
        original_equivalent_normal_sigma=float(norm.isf(original_tail)),
        exact_future_q=threshold, exact_future_q_over_sd0=threshold/sd0,
        exact_future_tail=calibrated_tail, exact_future_tail_quad_error=calibrated_error,
        original_exact_power=original_power, original_exact_power_quad_error=original_power_error,
        exact_future_power=calibrated_power, exact_future_power_quad_error=calibrated_power_error,
        fixed_linear_power=float(norm.sf(5-float(est['logK'])/sd0)),
        exact_MC_tail=mc_exact['tail_estimate'], exact_MC_se=mc_exact['standard_error'],
        exact_MC_minus_quad_in_MC_se=(mc_exact['tail_estimate']-original_tail)/mc_exact['standard_error']))

report = dict(status='DERIVED_ADDITIVE_DIAGNOSTIC_NO_NEW_TRIALS',
    at=datetime.now(timezone.utc).isoformat(), source_sha256=sha(Path(__file__)),
    frozen_inputs_sha256=sha(BASE/'FREEZE_R2.json'),
    scores_commit_sha256=sha(HERE/'SCORES_COMMIT.json'),
    unblinded_results_sha256=sha(HERE/'UNBLINDED_RESULTS.json'),
    observed_data_read=False, RNG_calls=0, estimator_changed=False,
    H0=H0, sigma_BG_H0=sig_bg, gaussian_alpha=alpha,
    quadrature_interval=[-12,12], quadrature_epsabs=1e-17,
    omitted_integral_probability_upper_bound=float(2*norm.sf(12)),
    nonpositive_H0_log_probability=float(norm.logcdf(-H0/sig_bg)),
    positivity_scope='No clipping or redraw. Exact log is defined for positive H0; omitted numerical Gaussian mass bounds any tail contribution by <4e-33, including undefined negative H0 far beyond -12 sigma.',
    formula='Integral phi(z) sf((q+log10(1+sigma_BG*z/H0)-delta)/sigma_local) dz',
    calibration_scope='Characterization only; future q does not replace frozen threshold or change any committed result.',
    quadrature=quadrature, exact_BG_coverage=coverage,
    cost=dict(scored_full_vectors=commit['samples_scored'],
        independent_primitive_vectors=400000, ordinary_independent=200000,
        importance_independent=200000, scored_batches=commit['blocks'],
        generation_scoring_seconds=commit['elapsed_seconds'],
        remote_model_calls=0, marginal_remote_cost_usd=0,
        hardware_energy_cost='not measured',
        pairing='Both models share inputs; seven ordinary nuisance scenarios per hypothesis reuse the same 100000 primitive errors.'))
save_new('EXACT_BG_SUPPLEMENT.json', report)
print(json.dumps(dict(path=str(HERE/'EXACT_BG_SUPPLEMENT.json'),
                     sha256=sha(HERE/'EXACT_BG_SUPPLEMENT.json'),
                     quadrature=quadrature), ensure_ascii=False, indent=2))
