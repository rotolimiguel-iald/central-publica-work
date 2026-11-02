"""Explicit aligned-spin pSEOBNRv4HM_PA source for the registered pilot.

Source preparation only. No waveform is computed on import. Masses are detector
frame solar masses; distance Mpc; deformation parameters are fractional QNM
frequency/damping-time changes in LAL's pSEOB convention.
"""
import numpy as np
import time
import os,json
from pathlib import Path
from datetime import datetime,timezone

STOP_UTC_TIMESTAMP = None
COST_COUNTER = None
EDOM_LOG = None

def set_deadline(timestamp):
    global STOP_UTC_TIMESTAMP
    if not np.isfinite(timestamp) or timestamp<=time.time():raise ValueError('Invalid source deadline')
    STOP_UTC_TIMESTAMP=float(timestamp)

def set_cost_counter(counter):
    global COST_COUNTER
    if len(counter)!=3:raise ValueError("Source counter requires calls, seconds, EDOM")
    COST_COUNTER=counter


def set_edom_log(path):
    global EDOM_LOG
    path=Path(path)
    if path.name!='EDOM_LOG.jsonl' or path.is_symlink():raise ValueError('Explicit job EDOM log required')
    with path.open('xb'):pass
    EDOM_LOG=path


def generation_grid(frequency_array, generation_maximum, generation_rate, analysis_maximum):
    f=np.asarray(frequency_array,dtype=float)
    if f.ndim!=1 or len(f)<2 or not np.isfinite(f).all() or f[0]!=0 or not np.all(np.diff(f)>0):raise ValueError('Invalid uniform zero-origin grid')
    df=f[1]-f[0]
    if not np.allclose(f,np.arange(len(f))*df,rtol=0,atol=1e-9):raise ValueError('Nonuniform data frequency bins')
    if generation_rate not in (4096,8192) or not np.isfinite([generation_maximum,analysis_maximum]).all():raise ValueError('Unsupported generation sampling')
    if not 0<analysis_maximum<=generation_maximum<=generation_rate/2 or f[-1]>generation_rate/2:raise ValueError('Generation bandwidth does not contain data grid')
    # SimInspiralFD infers its time step from f_max. These qualified pairs remove ambiguity.
    if generation_maximum!=generation_rate/2:raise ValueError('Qualified generation requires fmax=fs/2')
    bins=int(round((generation_rate/2)/df))
    if not np.isclose(bins*df,generation_rate/2,rtol=0,atol=1e-9):raise ValueError('Generation Nyquist is off grid')
    g=np.arange(bins+1,dtype=float)*df
    if not np.allclose(g[:len(f)],f,rtol=0,atol=1e-9):raise ValueError('Incompatible generation/data bins')
    return g


def record_edom(parameters,generation_maximum):
    if EDOM_LOG is None or COST_COUNTER is None:raise RuntimeError('EDOM logging was not configured; no silent prior rejection')
    raw=(json.dumps(dict(at=datetime.now(timezone.utc).isoformat(),parameters=parameters,
         generation_maximum_frequency_hz=generation_maximum,status='DOMAIN_RETURNED_NONE'),allow_nan=False)+'\n').encode()
    with COST_COUNTER.get_lock():
        fd=os.open(EDOM_LOG,os.O_WRONLY|os.O_APPEND)
        try:
            if os.write(fd,raw)!=len(raw):raise OSError('Short EDOM record')
        finally:os.close(fd)
        COST_COUNTER[2]+=1


def validate_polarizations(result,frequencies,minimum,maximum):
    if result is None:return None
    f=np.asarray(frequencies,dtype=float)
    if f.ndim!=1 or len(f)<2 or not np.isfinite(f).all() or not np.all(np.diff(f)>0):raise ValueError('Invalid frequency grid')
    if not isinstance(result,dict) or not {'plus','cross'}<=set(result):raise RuntimeError('Malformed waveform response')
    arrays=[np.asarray(result[k]) for k in ('plus','cross')]
    if any(a.shape!=f.shape or not np.isfinite(a).all() for a in arrays):raise RuntimeError('Nonfinite/wrong-shape waveform')
    mask=(f>=minimum)&(f<=maximum)
    if not mask.any() or not any(np.any(a[mask]!=0) for a in arrays):raise RuntimeError('Jointly zero active-band waveform')
    return result

def pseob_frequency_domain(frequency_array, mass_1, mass_2,
        luminosity_distance, chi_1, chi_2, theta_jn, phase,
        dtau220, dtau440, domega220=0., domega440=0., geocent_time=None, **kwargs):
    if STOP_UTC_TIMESTAMP is not None and time.time()>=STOP_UTC_TIMESTAMP:raise TimeoutError('Source deadline reached')
    import lal
    import lalsimulation as ls
    from bilby.gw.source import lal_binary_black_hole
    values=[mass_1,mass_2,luminosity_distance,chi_1,chi_2,theta_jn,
            phase,dtau220,dtau440,domega220,domega440]
    if not np.isfinite(values).all():raise ValueError('Nonfinite waveform parameters')
    if mass_1<=0 or mass_2<=0 or luminosity_distance<=0:raise ValueError('Invalid physical scale')
    if abs(chi_1)>=1 or abs(chi_2)>=1:raise ValueError('Spin outside supported Kerr range')
    if dtau220<=-1 or dtau440<=-1 or domega220<=-1 or domega440<=-1:raise ValueError('Invalid fractional QNM parameter')
    if 1+dtau440>2*max(1.,1+dtau220):raise ValueError('NATIVE_RINGDOWN_BUFFER_BOUND_REFUSED_BEFORE_LAL')
    generation_maximum=kwargs.pop('generation_maximum_frequency_hz')
    generation_rate=kwargs.pop('generation_sample_rate_hz')
    generated_grid=generation_grid(frequency_array,generation_maximum,generation_rate,kwargs['maximum_frequency'])
    # Conservative LAL temporal bounds; failure aborts PE, never trims the prior.
    timing=kwargs.pop('analysis_time_contract',None)
    from temporal_contract import validate_time_contract
    validate_time_contract(mass_1,mass_2,chi_1,chi_2,kwargs['minimum_frequency'],
                           geocent_time,timing,dtau220,dtau440)
    if kwargs.get('waveform_approximant','pSEOBNRv4HM_PA')!='pSEOBNRv4HM_PA':raise ValueError('Unregistered approximant')
    # A fresh dictionary per evaluation prevents parameter leakage between calls.
    if 'lal_waveform_dictionary' in kwargs:raise ValueError('Caller must not override deformation dictionary')
    if any(k in kwargs for k in ('DTau220','DTau440','DOmega220','DOmega440')):raise ValueError('Duplicate deformation override')
    dictionary=lal.CreateDict()
    for name,value in [('DTau220',dtau220),('DTau440',dtau440),
                       ('DOmega220',domega220),('DOmega440',domega440)]:
        getattr(ls,'SimInspiralWaveformParamsInsert'+name)(dictionary,float(value))
    options=dict(kwargs,waveform_approximant='pSEOBNRv4HM_PA',lal_waveform_dictionary=dictionary)
    options['maximum_frequency']=generation_maximum
    started=time.perf_counter()
    try:
        result=lal_binary_black_hole(generated_grid,mass_1,mass_2,
            luminosity_distance,abs(chi_1),0. if chi_1>=0 else np.pi,0.,
            abs(chi_2),0. if chi_2>=0 else np.pi,0.,theta_jn,phase,**options)
    finally:
        if COST_COUNTER is not None:
            with COST_COUNTER.get_lock():
                COST_COUNTER[0]+=1;COST_COUNTER[1]+=time.perf_counter()-started
    if result is None:
        record_edom(dict(mass_1=float(mass_1),mass_2=float(mass_2),chi_1=float(chi_1),chi_2=float(chi_2)),generation_maximum)
        return None
    validate_polarizations(result,generated_grid,kwargs['minimum_frequency'],generation_maximum)
    # Exact common Fourier bins; no interpolation, aliasing or change to the data sample grid.
    result={k:np.asarray(result[k])[:len(frequency_array)].copy() for k in ('plus','cross')}
    return validate_polarizations(result,frequency_array,kwargs['minimum_frequency'],kwargs['maximum_frequency'])

def parameter_conversion(parameters):
    """Preserve source parameters; add only the mass-order constraint coordinate."""
    out=dict(parameters)
    if 'mass_1' in out and 'mass_2' in out:
        out['mass_ratio']=out['mass_2']/out['mass_1']
    return out, ['mass_ratio'] if 'mass_ratio' not in parameters else []
