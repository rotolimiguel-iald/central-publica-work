def _v394_clock_modulus(c0, c1, gamma):
    import math
    import numbers
    gamma = _v394_finite(gamma, 'rate for modulus clock', positive=True)
    for z in (c0, c1):
        if isinstance(z, bool) or not isinstance(z, numbers.Complex) or not math.isfinite(z.real) or not math.isfinite(z.imag) or abs(z) == 0:
            raise ValueError('nonzero finite coherence required')
    result = -(math.log(abs(c1))-math.log(abs(c0)))/gamma
    if not math.isfinite(result) or result < -1e-10/gamma:
        raise ValueError('coherence does not represent forward decay')
    return max(0., result)