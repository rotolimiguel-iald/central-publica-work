def _v394_channel(a, t, omega, gamma):
    import math
    a = _v394_matrix(a, "channel input")
    t = _v394_finite(t, 'time', nonnegative=True)
    omega = _v394_finite(omega, 'angular frequency', positive=True)
    gamma = _v394_finite(gamma, 'rate', nonnegative=True)
    angle = omega*t
    exposure = gamma*t
    if not math.isfinite(angle) or not math.isfinite(exposure):
        raise ValueError('derived angle or exposure overflow')
    g = _v394_geometry()
    unitary = math.cos(angle)*g['I'] + math.sin(angle)*g['K']
    reading = _v394_read(a)
    out = unitary @ (reading + math.exp(-exposure)*(a-reading)) @ unitary.conj().T
    return _v394_matrix(out, 'channel output')