def _v394_rule(state, target, tolerance=1e-10):
    import numpy as np
    state = _v394_matrix(state, 'state', density=True)
    target = _v394_matrix(target, 'target', density=True)
    tolerance = _v394_finite(tolerance, 'rule tolerance', positive=True)
    if tolerance > 1e-6:
        raise ValueError('rule tolerance exceeds pinned ceiling')
    if np.linalg.norm(_v394_read(target)-target) > tolerance:
        raise ValueError('target is not a fixed reading')
    residual = float(np.linalg.norm(_v394_read(state)-target))
    return {'admitted': residual <= tolerance, 'residual': residual,
            'tolerance': tolerance, 'target_fixed_before_evolution': True}