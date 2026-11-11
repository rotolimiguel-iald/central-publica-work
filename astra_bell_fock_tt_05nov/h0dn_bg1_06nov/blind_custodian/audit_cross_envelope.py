"""Independent covariance-only fixed-estimator check; no observed data."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
with np.load(BASE/'network/network.npz', allow_pickle=False) as data:
    C = data['C'].copy()
with np.load(BASE/'estimator_frozen.npz', allow_pickle=False) as data:
    weights = data['weights'].copy()
envelope = json.loads((BASE/'cross_rung/PSD_ENVELOPE.json').read_text())
block = np.asarray(envelope['block_rows'])
outside = np.setdiff1d(np.arange(len(C)), block)
Cb = C[np.ix_(block,block)]
assert np.max(abs(Cb-np.diag(np.diag(Cb)))) < 1e-15
assert np.max(abs(C[np.ix_(block,outside)])) < 1e-15
rows = []
for i, row in enumerate(envelope['results']):
    w = weights[i]
    v = float(w@C@w)
    wo, wb = w[outside], w[block]
    vother = float(wo@C[np.ix_(outside,outside)]@wo)
    sig = np.sqrt(np.diag(Cb))
    vcal = float(np.sum((wb[:-1]*sig[:-1])**2))
    vhf = float((wb[-1]*sig[-1])**2)
    lengths = abs(wb)*sig
    bounds = dict(cross_only_sigma_min=math.sqrt(v-2*math.sqrt(vcal*vhf)),
        cross_only_sigma_max=math.sqrt(v+2*math.sqrt(vcal*vhf)),
        calibration_plus_cross_sigma_min=math.sqrt(vother+max(2*max(lengths)-sum(lengths),0)**2),
        calibration_plus_cross_sigma_max=math.sqrt(vother+sum(lengths)**2))
    errors = {k:abs(value-row[k]) for k,value in bounds.items()}
    scenarios = []
    for scenario in row['scenarios']:
        rho = scenario['rho']
        signed_sig = sig*np.sign(wb)
        modified = (1-rho)*Cb + rho*np.outer(signed_sig,signed_sig)
        fixed_sigma = math.sqrt(vother+float(wb@modified@wb))
        scenarios.append(dict(rho=rho, fixed_sigma=fixed_sigma,
            difference_from_report=abs(fixed_sigma-scenario['fixed_estimator_sigma']),
            minimum_block_eigenvalue=float(np.linalg.eigvalsh(modified)[0])))
    assert max(errors.values()) < 1e-12
    assert max(x['difference_from_report'] for x in scenarios) < 1e-12
    assert min(x['minimum_block_eigenvalue'] for x in scenarios) > 0
    rows.append(dict(model=i, bounds=bounds, bound_differences=errors, scenarios=scenarios))
report = dict(status='PASS_FIXED_ESTIMATOR_ENVELOPE_WITH_SCOPE',
    files={str(p):sha(p) for p in [BASE/'cross_rung/PSD_ENVELOPE.json',
        BASE/'cross_rung/AUDIT.json',BASE/'network/network.npz',
        BASE/'estimator_frozen.npz',Path(__file__)]},
    block_diagonal_and_independent_from_outside=True, results=rows,
    rationale='Cross-only Cauchy-Schwarz endpoints are attained by Schur-complement contractions. Full fixed-diagonal endpoints follow from vector polygon length bounds for PSD Gram matrices.',
    scope='These are exact envelopes for fixed unbiased weights in the declared covariance family, not empirical correlations, evidence against TGL, or a measured minimax GLS variance. Reoptimized GLS numbers were not independently recomputed here.',
    documentary_scope='AUDIT.json was read. Primary catalogue mappings and raw covariance comparison were not reexecuted. Missing aggregation weights/aliases and possible Cepheid double counting prohibit transplanting Pantheon+ correlations without an explicit component map.',
    no_observed_data=True, no_new_trials=True, no_primary_mutation=True)
target = HERE/'CROSS_ENVELOPE_REVIEW.json'
with target.open('xb') as handle:
    handle.write(json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(dict(path=str(target),sha256=sha(target),
    max_bound_difference=max(max(x['bound_differences'].values()) for x in rows))))
