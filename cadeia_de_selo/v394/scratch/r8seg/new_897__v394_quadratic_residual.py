def _v394_quadratic_residual(state, target):
    import math
    import numpy as np
    state = _v394_matrix(state, 'quadratic state')
    target = _v394_matrix(target, 'quadratic target')
    delta = _v394_read(state) - target
    with np.errstate(over='ignore', invalid='ignore'):
        value = float(np.vdot(delta, delta).real)
    if not math.isfinite(value) or value < 0:
        raise ValueError('unrepresentable quadratic residual')
    return value