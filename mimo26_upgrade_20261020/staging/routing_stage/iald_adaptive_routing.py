"""Pure pre-dispatch policy; observational efficiency is not answer quality."""
import math

VERSION = 'task_model_baseline_pareto_20261020_r2'
MIN_SAMPLES = 3


def select(candidates, identities, task, observed, cold_order, *, modality_counts=None):
    pool = [key for key in cold_order if key in candidates]
    if not pool:
        raise ValueError('No authorized automatic candidate')
    receipt = dict(version=VERSION, task=task, eligible=pool, selected=pool[0],
                   basis='cold_start_operator_preference', quality='not_benchmarked', modality_counts=modality_counts)
    providers = observed.get('providers', {}) if type(observed) is dict else {}
    if type(providers) is not dict:
        providers = {}
    values = {}
    for key in pool:
        row = providers.get(key, {})
        if (type(row) is not dict or not identities.get(key) or row.get('model_id') != identities[key]
                or row.get('task') != task or type(row.get('paired_samples')) is not int
                or row['paired_samples'] < MIN_SAMPLES):
            continue
        if modality_counts is not None and row.get('modality_counts')!=modality_counts:
            continue
        pair = (row.get('median_cost_usd'), row.get('median_seconds'))
        if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in pair):
            continue
        values[key] = pair
    receipt['qualified'] = list(values)
    receipt['unmeasured_or_unqualified'] = [key for key in pool if key not in values]
    if pool[0] not in values:
        receipt['reason'] = 'baseline_has_no_qualified_measurement'
        return receipt['selected'], receipt
    winners = [key for key in values if all(
        key == other or (all(a <= b for a, b in zip(values[key], values[other]))
                         and any(a < b for a, b in zip(values[key], values[other])))
        for other in values)]
    if len(winners) == 1 and len(values) > 1:
        receipt.update(selected=winners[0], basis='observed_task_model_pareto',
                       measurements=values, limitation='observational_not_controlled_quality_or_causal_benchmark')
    else:
        receipt['reason'] = 'tradeoff_or_tie_preserves_cold_start'
    return receipt['selected'], receipt
