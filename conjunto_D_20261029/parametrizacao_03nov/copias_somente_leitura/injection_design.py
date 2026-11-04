"""Witnessed free-source recovery injections in actual off-source noise.

The recovery model remains pSEOBNRv4HM_PA. Alternative-family GR injections
measure mismatch. No claim that an envelope deformation equals pSEOB DTau.
"""
import numpy as np
from pseob_source import pseob_frequency_domain,parameter_conversion
from temporal_contract import validate_time_contract


def aligned_gr_xphm(frequency_array,mass_1,mass_2,luminosity_distance,chi_1,chi_2,theta_jn,phase,geocent_time=None,**kwargs):
    import bilby
    if not np.isfinite([mass_1,mass_2,luminosity_distance,chi_1,chi_2,theta_jn,phase]).all():raise ValueError('Invalid injection source')
    timing=kwargs.pop('analysis_time_contract',None)
    validate_time_contract(mass_1,mass_2,chi_1,chi_2,kwargs['minimum_frequency'],geocent_time,timing)
    args={k:v for k,v in kwargs.items() if k not in ('waveform_approximant','dtau220','dtau440','domega220','domega440')}
    result=bilby.gw.source.lal_binary_black_hole(frequency_array,mass_1,mass_2,luminosity_distance,
      abs(chi_1),0. if chi_1>=0 else np.pi,0.,abs(chi_2),0. if chi_2>=0 else np.pi,0.,theta_jn,phase,
      waveform_approximant='IMRPhenomXPHM',**args)
    if result is None:raise ValueError('Injection waveform failed')
    if set(result)!= {'plus','cross'} or any(np.asarray(v).shape!=np.asarray(frequency_array).shape or not np.isfinite(v).all() for v in result.values()):raise ValueError('Invalid injection polarizations')
    if sum(float(np.vdot(v,v).real) for v in result.values())<=0:raise ValueError('Zero injection waveform')
    return result


def validate_truth_support(params,priors):
    required={'mass_1','mass_2','luminosity_distance','chi_1','chi_2','theta_jn','phase','ra','dec','psi','geocent_time',
              'dtau220','dtau440','domega220','domega440'}
    if set(priors)!=required|{'mass_ratio'} or not required<=set(params):raise ValueError('Complete registered recovery prior and injection truth required')
    if set(params)-required-{'mass_ratio'}:raise ValueError('Unknown injection truth coordinate')
    if params['mass_1']<=0 or params['mass_2']<=0:raise ValueError('Invalid injection mass')
    q=params['mass_2']/params['mass_1']
    if 'mass_ratio' in params and params['mass_ratio']!=q:raise ValueError('Injection mass ratio inconsistent')
    for name in sorted(required|{'mass_ratio'}):
        v=q if name=='mass_ratio' else params[name];p=priors[name]
        if p['kind'] not in ('Uniform','Sine','Cosine','Constraint'):raise ValueError('Unsupported truth prior')
        if not np.isfinite(v) or not p['minimum']<=v<=p['maximum']:raise ValueError('Injection truth outside recovery prior: '+name)
    if q>1:raise ValueError('Injection masses not ordered')
    return True


def inject_into_ifos(ifos,cfg,reg):
    import bilby
    if cfg['mode']!='calibration' or cfg['event'] not in reg['calibration_event_ids']:raise ValueError('No injection into blind-event job')
    inj=cfg['injection'];family=inj['family']
    if family not in ('pSEOBNRv4HM_PA','IMRPhenomXPHM'):raise ValueError('Unregistered injection family')
    if inj.get('noise_kind')!='REAL_OFFSOURCE':raise ValueError('This design requires actual offsource noise')
    real_gps=reg['event_reference_GPS'].get(cfg['event'])
    if real_gps is None or not np.isfinite(real_gps) or float(cfg['event_GPS'])!=float(real_gps):
        raise ValueError('Real-event GPS must match the witnessed metadata anchor')
    analysis_start=float(cfg['segment_start_GPS']);analysis_end=analysis_start+float(cfg['duration_s'])
    exclusion=float(cfg['offsource_exclusion_s'])
    if not np.isfinite([analysis_start,analysis_end,exclusion]).all() or exclusion<=0 or analysis_end<=analysis_start:
        raise ValueError('Invalid real-event exclusion interval')
    if not (analysis_end<=real_gps-exclusion or analysis_start>=real_gps+exclusion):
        raise ValueError('Calibration noise window overlaps the protected real-event interval')
    params=dict(inj['parameters']);target=float(inj['target_network_optimal_SNR'])
    validate_truth_support(params,cfg['priors'])
    if not np.isfinite(target) or target<=0:raise ValueError('Invalid target SNR')
    for name in ('dtau220','dtau440','domega220','domega440'):
        if name not in params or not np.isfinite(params[name]) or params[name]<=-1:raise ValueError('Missing/invalid injection deformation')
    if family=='IMRPhenomXPHM' and any(params[k]!=0 for k in ('dtau220','dtau440','domega220','domega440')):
        raise ValueError('No equivalent non-GR XPHM injection implemented; do not substitute an envelope')
    starts=[float(i.strain_data.start_time) for i in ifos]
    if max(starts)-min(starts)>1e-9:raise ValueError('Detector segment mismatch')
    if not all(i.strain_data.time_within_data(params['geocent_time']) for i in ifos):raise ValueError('Injection outside analysis segment')
    for i in ifos:
        detector_time=params['geocent_time']+float(i.time_delay_from_geocenter(params['ra'],params['dec'],params['geocent_time']))
        if not starts[0]+cfg['onsource_roll_off_s']<detector_time<starts[0]+cfg['duration_s']-cfg['onsource_roll_off_s']:
            raise ValueError('Injection detector arrival inside tapered region')
    for i in ifos:
        source=cfg['data'][i.name]
        if source['onsource_sha256']!=source['offsource_sha256'] or source['onsource_path']!=source['offsource_path']:
            raise ValueError('Injection analysis must explicitly reference offsource noise bytes')
    generator=bilby.gw.WaveformGenerator(duration=cfg['duration_s'],sampling_frequency=cfg['sample_rate_hz'],start_time=starts[0],
      frequency_domain_source_model=pseob_frequency_domain if family=='pSEOBNRv4HM_PA' else aligned_gr_xphm,
      parameter_conversion=parameter_conversion,
      waveform_arguments={'minimum_frequency':cfg['minimum_frequency_hz'],'maximum_frequency':cfg['maximum_frequency_hz'],
        'reference_frequency':cfg['reference_frequency_hz'],'catch_waveform_errors':False,
        'analysis_time_contract':{'start_GPS':starts[0],'duration_s':cfg['duration_s'],
          'roll_off_s':cfg['onsource_roll_off_s']}})
    pol=generator.frequency_domain_strain(params)
    if pol is None:raise ValueError('Injection waveform failed')
    def snr2(polarizations):
        values=[float(np.real(i.optimal_snr_squared(i.get_detector_response(polarizations,params)))) for i in ifos]
        if not np.isfinite(values).all() or min(values)<0 or sum(values)<=0:raise ValueError('Invalid injection SNR')
        return values
    before=snr2(pol);factor=target/np.sqrt(sum(before))
    pol={k:np.asarray(v)*factor for k,v in pol.items()};params['luminosity_distance']/=factor
    prior=cfg['priors']['luminosity_distance']
    if not prior['minimum']<params['luminosity_distance']<prior['maximum']:
        raise ValueError('Rescaled injection distance outside recovery prior; no post-result prior change')
    validate_truth_support(params,cfg['priors'])
    after=snr2(pol)
    if not np.isclose(np.sqrt(sum(after)),target,rtol=1e-8,atol=1e-10):raise ValueError('SNR scaling failed')
    for i in ifos:i.inject_signal(parameters=params,injection_polarizations=pol,raise_error=True)
    return {'status':'INJECTION_ADDED_TO_REAL_OFFSOURCE_NOISE','family':family,'parameters':params,
      'optimal_network_SNR':float(np.sqrt(sum(after))),'per_detector_optimal_SNR':dict(zip([i.name for i in ifos],np.sqrt(after).tolist())),
      'SNR_basis':'Full IMR network optimal SNR in registered PSD/band; not ringdown SNR',
      'deformation_scope':'pSEOB DTau exact parameter for that family; second-family injections are GR only',
      'time_support_scope':'Both families checked against shared conservative LAL bounds; waveform leakage not certified by these scalar bounds',
      'recovery_source_parameters':'Free according to PE priors; no remnant fixed by this injection receipt'}
