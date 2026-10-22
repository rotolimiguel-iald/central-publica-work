def _v394_finite(value, name, positive=False, nonnegative=False):
    import math
    import numbers
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(name + ": finite real scalar required, not boolean")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + ": nonfinite scalar")
    if positive and value <= 0:
        raise ValueError(name + ": positive scalar required")
    if nonnegative and value < 0:
        raise ValueError(name + ": nonnegative scalar required")
    return value