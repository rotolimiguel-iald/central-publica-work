"""Pinned GWOSC data windows and off-source PSD; called only by registered runs."""
import hashlib
from pathlib import Path
import numpy as np

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def require_pin(path,expected):
    if digest(path)!=expected:raise ValueError('Strain content differs from receipt')

def quality_mask(handle,required_dq,required_no_injections):
    def selected(group,field,namesfield,required):
        if not required or len(set(required))!=len(required):raise ValueError('Nonempty unique flags required')
        names=[x.decode() if isinstance(x,bytes) else str(x) for x in handle[group+'/'+namesfield][()]]
        if not set(required)<=set(names):raise ValueError('Required quality flag absent')
        mask=sum(1<<names.index(x) for x in required)
        q=handle[group+'/'+field][()]
        if q.ndim!=1 or q.dtype.kind not in 'iu':raise ValueError('Quality mask must be integer vector')
        return (q&mask)==mask
    dq=selected('quality/simple','DQmask','DQShortnames',required_dq)
    inj=selected('quality/injections','Injmask','InjShortnames',required_no_injections)
    if dq.shape!=inj.shape:raise ValueError('Quality cadence mismatch')
    return dq&inj

def window(path,expected,start,duration,required_dq,required_no_injections):
    import h5py
    require_pin(path,expected)
    with h5py.File(path,'r') as h:
        raw=h['strain/Strain'];gps=float(h['meta/GPSstart'][()]);fs=1/float(raw.attrs['Xspacing'])
        if not np.isfinite([start,duration,fs,gps]).all() or duration<=0 or fs<=0 or fs!=round(fs):raise ValueError('Invalid window/sampling')
        i=int(round((start-gps)*fs));n=int(round(duration*fs))
        if n<=0 or abs(start-(gps+i/fs))>max(1e-8,np.spacing(gps)*2):raise ValueError('Fractional start requires registered timing method')
        if i<0 or i+n>len(raw) or abs(n/fs-duration)>1e-8:raise ValueError('Incomplete requested window')
        q=quality_mask(h,required_dq,required_no_injections)
        if len(q)!=round(len(raw)/fs):raise ValueError('Quality mask must be 1Hz for this reader')
        if not q[i//int(fs):(i+n-1)//int(fs)+1].all():raise ValueError('Data quality gate failed')
        a=np.asarray(raw[i:i+n],dtype=float)
        if not np.isfinite(a).all():raise ValueError('Nonfinite strain')
        return a,fs,gps+i/fs

def offsource_psd(path,expected,config):
    """First valid fixed-length block, chosen by flags/finiteness only, never PSD level."""
    import h5py
    from scipy.signal import welch
    require_pin(path,expected)
    duration=config['psd_duration_s'];segment=config['psd_segment_s'];exclusion=config['offsource_exclusion_s']
    if not np.isfinite([duration,segment,exclusion]).all() or duration!=int(duration) or segment<=0 or duration<segment or exclusion<0:raise ValueError('Invalid PSD settings')
    length=int(duration);limit=min(float(config['event_GPS'])-float(exclusion),float(config['segment_start_GPS']))
    with h5py.File(path,'r') as h:
        raw=h['strain/Strain'];gps=float(h['meta/GPSstart'][()]);fs=1/float(raw.attrs['Xspacing'])
        if fs!=round(fs):raise ValueError('Unexpected noninteger GWOSC sampling')
        q=quality_mask(h,config['quality_required'],config['injection_flags_required'])
        if len(q)!=round(len(raw)/fs):raise ValueError('Unexpected quality cadence')
        chosen=None
        for sec in range(0,len(q)-length+1):
            if gps+sec+length>limit:break
            if q[sec:sec+length].all():
                y=np.asarray(raw[int(sec*fs):int((sec+length)*fs)],dtype=float)
                if np.isfinite(y).all():chosen=sec;break
        if chosen is None:raise ValueError('No fixed-length valid off-source block')
    nperseg=int(config['psd_segment_s']*fs)
    if nperseg<2 or abs(nperseg-config['psd_segment_s']*fs)>1e-8 or len(y)<nperseg:raise ValueError('PSD segment not representable')
    f,p=welch(y,fs=fs,window='hann',nperseg=nperseg,noverlap=nperseg//2,
        detrend='constant',return_onesided=True,scaling='density',average='median')
    if not np.isfinite(p).all() or np.any(p<=0):raise ValueError('Invalid estimated PSD')
    receipt={'source_sha256':expected,'GPS_start':gps+chosen,'duration_s':length,
        'sample_rate':fs,'estimator':'scipy Welch Hann 50% overlap median corrected, one-sided strain^2/Hz',
        'selection':'First block passing registered quality and finiteness; no PSD-level scan'}
    return f,p,receipt
