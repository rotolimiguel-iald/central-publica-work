def _v394_finite_real(name, value, *, positive=False, nonnegative=False):
    import math
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise V394PhysicalContractError(name + ": finite non-boolean real required")
    try:
        number = float(value)
    except (ValueError, OverflowError) as exc:
        raise V394PhysicalContractError(name + ": float conversion failed") from exc
    if not math.isfinite(number):
        raise V394PhysicalContractError(name + ": nonfinite value")
    if positive and number <= 0:
        raise V394PhysicalContractError(name + ": strictly positive value required")
    if nonnegative and number < 0:
        raise V394PhysicalContractError(name + ": nonnegative value required")
    return number