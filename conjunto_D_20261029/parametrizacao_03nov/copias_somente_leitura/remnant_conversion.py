"""Named GR remnant/cosmology bridge for paired custom-PE samples.

This is a model INPUT, not independently measured inspiral-only remnant data.
No waveform generation occurs here. All source rows are retained in order.
"""
from pathlib import Path
import hashlib
import numpy as np


def derive(columns,config,time_guard):
    import lal,lalsimulation as ls
    import astropy.units as u
    from astropy.cosmology import FlatLambdaCDM,z_at_value,Planck18
    cfg=config['remnant_conversion_INPUT']
    if cfg['remnant_fit']!='LAL_SEOBNRv4_aligned_NR_fit' or cfg['cosmology_name']!='Planck18_external_INPUT':raise ValueError('Unregistered remnant/cosmology bridge')
    path=Path(cfg['cosmology_source_path'])
    if hashlib.sha256(path.read_bytes()).hexdigest()!=cfg['cosmology_source_sha256']:raise ValueError('Cosmology input changed')
    pars=cfg['cosmology_parameters']
    reference={'H0_km_s_Mpc':float(Planck18.H0.value),'Om0':float(Planck18.Om0),
      'Tcmb0_K':float(Planck18.Tcmb0.value),'Neff':float(Planck18.Neff),
      'm_nu_eV':Planck18.m_nu.value.tolist(),'Ob0':float(Planck18.Ob0)}
    if pars!=reference:raise ValueError('Parameters do not match the pinned named Planck18 input')
    cosmology=FlatLambdaCDM(H0=pars['H0_km_s_Mpc']*u.km/u.s/u.Mpc,Om0=pars['Om0'],
      Tcmb0=pars['Tcmb0_K']*u.K,Neff=pars['Neff'],m_nu=np.array(pars['m_nu_eV'])*u.eV,Ob0=pars['Ob0'])
    source=[np.asarray(columns[k],float) for k in ('mass_1','mass_2','chi_1','chi_2','luminosity_distance')]
    if not source or len(source[0])<2 or any(a.shape!=source[0].shape or a.ndim!=1 or not np.isfinite(a).all() for a in source):raise ValueError('Invalid paired conversion input')
    mf=[];af=[];z=[]
    for j,(m1,m2,s1,s2,dl) in enumerate(zip(*source)):
        if j%16==0:time_guard()
        if m1<=0 or m2<=0 or dl<=0 or abs(s1)>=1 or abs(s2)>=1:raise ValueError('Invalid physical conversion row')
        # The LAL/PESummary interface returns success, fractional mass, final spin.
        ret=ls.SimIMREOBFinalMassSpin(float(m1*lal.MSUN_SI),float(m2*lal.MSUN_SI),
          [0.,0.,float(s1)],[0.,0.,float(s2)],ls.SEOBNRv4)
        if len(ret)!=3 or ret[0]!=0:raise ValueError('LAL remnant fit failed')
        fraction,spin=float(ret[1]),float(ret[2])
        if not np.isfinite([fraction,spin]).all() or not 0<fraction<=1 or abs(spin)>=1:raise ValueError('Unphysical remnant fit')
        redshift=float(z_at_value(cosmology.luminosity_distance,float(dl)*u.Mpc,zmin=1e-9,zmax=20,ztol=1e-8))
        if not np.isfinite(redshift) or redshift<0:raise ValueError('Distance-redshift inversion failed')
        mf.append(fraction*(m1+m2));af.append(spin);z.append(redshift)
    result={'final_mass_detector':np.array(mf),'final_spin':np.array(af),'redshift':np.array(z)}
    return result,{'status':'DERIVED_PAIRED_GR_FIT_WITH_EXTERNAL_COSMOLOGY_INPUT','N':len(mf),
      'remnant_fit':cfg['remnant_fit'],'mass_frame':'Detector-frame solar masses; final mass fraction times detector m1+m2',
      'cosmology':pars,'cosmology_source_sha256':cfg['cosmology_source_sha256'],
      'source':'https://lscsoft.docs.ligo.org/pesummary/latest/_modules/pesummary/gw/conversions/remnant.html',
      'scope':'Aligned GR fit applied to free component-source posterior; not an independent remnant measurement; preserves negative final spin for explicit downstream domain handling',
      'same_order_no_thinning':True}
