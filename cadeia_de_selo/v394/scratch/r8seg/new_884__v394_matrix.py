def _v394_matrix(value, name, density=False):
    import numpy as np
    a = np.asarray(value, dtype=complex)
    if a.shape != (2, 2) or not np.isfinite(a).all():
        raise ValueError(name + ": finite 2 by 2 matrix required")
    if density:
        if np.linalg.norm(a-a.conj().T) > 1e-11 or abs(np.trace(a)-1) > 1e-11:
            raise ValueError(name + ": Hermitian trace-one state required")
        if np.linalg.eigvalsh(a).min() < -1e-11:
            raise ValueError(name + ": positive state required")
    return a