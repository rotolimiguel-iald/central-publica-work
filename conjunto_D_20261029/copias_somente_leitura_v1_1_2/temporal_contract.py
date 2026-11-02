"""Shared conservative LAL time bounds, not a waveform support certificate."""
import math


def validate_time_contract(mass_1,mass_2,chi_1,chi_2,minimum_frequency,
                           geocent_time,timing,dtau220=0.,dtau440=0.):
    import lal
    import lalsimulation as ls
    values=[mass_1,mass_2,chi_1,chi_2,minimum_frequency,geocent_time,dtau220,dtau440]
    if timing is None or any(not isinstance(v,(float,int)) or not math.isfinite(v) for v in values):
        raise ValueError('Finite source and analysis time contract required')
    if min(mass_1,mass_2,minimum_frequency)<=0 or max(abs(chi_1),abs(chi_2))>=1 or min(dtau220,dtau440)<=-1:
        raise ValueError('Invalid source domain for temporal bounds')
    start,duration,roll=[float(timing[k]) for k in ('start_GPS','duration_s','roll_off_s')]
    if not all(math.isfinite(v) for v in (start,duration,roll)) or roll<0 or duration<=2*roll:
        raise ValueError('Invalid time-window contract')
    m1,m2=mass_1*lal.MSUN_SI,mass_2*lal.MSUN_SI
    inspiral=ls.SimInspiralChirpTimeBound(minimum_frequency,m1,m2,chi_1,chi_2)
    merger=ls.SimInspiralMergeTimeBound(m1,m2)
    spin=ls.SimInspiralFinalBlackHoleSpinBound(chi_1,chi_2)
    tail=ls.SimInspiralRingdownTimeBound(m1+m2,spin)*max(1.,1+dtau220,1+dtau440)
    if not all(math.isfinite(v) and v>=0 for v in (inspiral,merger,tail)):
        raise RuntimeError('Invalid LAL duration bounds')
    margins=[geocent_time-.022-inspiral-merger-(start+roll),start+duration-roll-(geocent_time+.022+tail)]
    if min(margins)<0:raise RuntimeError('WINDOW_BOUND_VIOLATION_ABORT_NOT_PRIOR_REJECTION; widen registered segment')
    return {'inspiral_bound_s':inspiral,'merger_bound_s':merger,'tail_bound_s':tail,
            'margins_s':margins,'scope':'Generic conservative LAL bounds; neither exact family support nor FFT leakage certified'}
