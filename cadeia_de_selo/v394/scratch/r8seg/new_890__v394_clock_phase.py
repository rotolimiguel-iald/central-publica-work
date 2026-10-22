def _v394_clock_phase(phase_lift, omega):
    # phase_lift is an explicitly unwrapped phase difference, not principal Arg.
    phase_lift = _v394_finite(phase_lift, 'unwrapped phase difference')
    omega = _v394_finite(omega, 'angular frequency', positive=True)
    if phase_lift < 0:
        raise ValueError('positive-helicity forward phase lift required')
    result = (phase_lift/omega)*0.5 if phase_lift <= omega else (phase_lift*0.5)/omega
    import math
    if not math.isfinite(result) or (phase_lift > 0 and result <= 0):
        raise ValueError('phase clock overflow or underflow')
    return result