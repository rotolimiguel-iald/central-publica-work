import sys,time,json,os
sys.dont_write_bytecode=True
sys.path.insert(0,'/mnt/c/IALD/Central de Patentes/work/conjunto_D_20261029/copias_somente_leitura_v1_1_2')
import numpy as np
t_imp=time.perf_counter()
import pseob_source as ps
import_s=time.perf_counter()-t_imp
duration=32.0; fs=4096; gen_rate=8192; df=1.0/duration
f=np.arange(0,int(fs/2/df)+1)*df          # data grid 0..2048 Hz
start=1.0e9; roll=0.2; geocent=start+24.0
timing=dict(start_GPS=start,duration_s=duration,roll_off_s=roll)
def one(dtau220,m1=35.0,m2=30.0,chi1=0.3,chi2=0.1):
    t0=time.perf_counter()
    r=ps.pseob_frequency_domain(f,m1,m2,500.0,chi1,chi2,0.6,0.3,dtau220,0.0,0.0,0.0,
        geocent_time=geocent,minimum_frequency=20.0,maximum_frequency=1024.0,reference_frequency=20.0,
        waveform_approximant='pSEOBNRv4HM_PA',analysis_time_contract=timing,
        generation_maximum_frequency_hz=4096.0,generation_sample_rate_hz=8192,catch_waveform_errors=True)
    dt=time.perf_counter()-t0
    p=np.asarray(r['plus']);c=np.asarray(r['cross'])
    return dt,float(np.vdot(p,p).real),float(np.vdot(c,c).real),p.shape
out=dict(import_seconds=import_s,runs=[])
cpu0=time.process_time()
for label,d in [('GR_dtau0',0.0),('dtau_-0.40',-0.40),('dtau_-0.40_again',-0.40),('dtau_+0.30',0.30)]:
    try:
        dt,pp,cc,sh=one(d)
        out['runs'].append(dict(label=label,dtau220=d,wall_s=dt,norm2_plus=pp,norm2_cross=cc,shape=list(sh)))
    except Exception as e:
        out['runs'].append(dict(label=label,dtau220=d,error=type(e).__name__,msg=str(e)[:400]))
out['cpu_total_s']=time.process_time()-cpu0
a=[r for r in out['runs'] if r.get('label')=='GR_dtau0' and 'norm2_plus' in r]
b=[r for r in out['runs'] if r.get('label')=='dtau_-0.40' and 'norm2_plus' in r]
if a and b: out['norm2_plus_ratio_dtau-0.40_over_GR']=b[0]['norm2_plus']/a[0]['norm2_plus']
print(json.dumps(out,indent=1))
