"""Controlled full-IMR PE. Import does not launch science; direct CLI is rejected."""
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[_name]='1'
import argparse,json,time,math,multiprocessing
from pathlib import Path
from datetime import datetime,timezone
from registration_guard import (checked_registration,authorize_event,time_guard,contained,sha,
    load_jobs,validate_launch,positive,integer,publish_new,utc)

PHYSICAL=('mass_1','mass_2','chi_1','chi_2','luminosity_distance','theta_jn','phase','ra','dec','psi','geocent_time')
DEFORMATIONS=('dtau220','dtau440','domega220','domega440')
DERIVED_PHYSICAL=('final_mass_detector','final_spin','redshift')


def counted_likelihood_class(base,counter):
    """Count the shared ratio frontier exactly once, including failed attempts.

    Pinned Bilby log_likelihood calls log_likelihood_ratio once. Override only
    the latter: direct ratio and full likelihood enter the same frontier.
    Cached noise-only likelihood calls are deliberately not signal evaluations.
    """
    class CountedLikelihood(base):
        def log_likelihood_ratio(self,parameters=None):
            started=time.perf_counter()
            with counter.get_lock():counter[0]+=1
            try:
                value=super().log_likelihood_ratio(parameters=parameters)
            except BaseException:
                with counter.get_lock():counter[2]+=1
                raise
            else:
                with counter.get_lock():counter[1]+=1
                return value
            finally:
                with counter.get_lock():counter[3]+=time.perf_counter()-started
    return CountedLikelihood


def likelihood_snapshot(counter):
    with counter.get_lock():values=list(counter[:])
    return dict(calls=int(values[0]),completed=int(values[1]),raised=int(values[2]),
      total_wall_seconds=float(values[3]),
      scope='Shared actual ratio frontier, direct or via full likelihood; includes setup and failed pre-generator calls; excludes noise-only calls')


def prior_conversion(params):
    from pseob_source import parameter_conversion
    return parameter_conversion(params)[0]


def validate_config(config):
    priors=config['priors'];required=set(PHYSICAL+DEFORMATIONS+('mass_ratio',))
    if set(priors)!=required:raise ValueError('Exact physical/deformation prior contract required')
    fixed=config['fixed_deformation_parameters']
    if not set(fixed)<=set(DEFORMATIONS):raise ValueError('Unregistered fixed deformation')
    if config['variant'] in ('pilot_all_four_free','220_plus_440_free') and fixed:raise ValueError('Pilot requires all four deviations free')
    if config['variant'] not in ('pilot_all_four_free','220_plus_440_free','registered_fixed_deformation_variant'):raise ValueError('Unknown deformation variant')
    for name,item in priors.items():
        if name in fixed:
            if isinstance(item,bool) or not isinstance(item,(int,float)) or not math.isfinite(item) or item!=fixed[name] or item<=-1:raise ValueError('Fixed prior differs')
            continue
        if not isinstance(item,dict):raise ValueError('Physical parameters and unfixed deviations must be free')
        low=item['minimum'];high=item['maximum']
        if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in (low,high)) or low>=high:raise ValueError('Invalid prior bounds')
        expected={'theta_jn':'Sine','dec':'Cosine','mass_ratio':'Constraint'}.get(name,'Uniform')
        if item['kind']!=expected:raise ValueError('Wrong prior class for '+name)
        if name.startswith('mass_') and low<=0:raise ValueError('Positive mass/mass ratio required')
        if name=='mass_ratio' and high>1:raise ValueError('Mass order constraint required')
        if name in ('chi_1','chi_2') and not -1<low<high<1:raise ValueError('Spin bounds')
        if name in DEFORMATIONS and low<=-1:raise ValueError('Fractional deformation lower bound')
        if name=='luminosity_distance' and low<=0:raise ValueError('Positive distance')
    for name in ('duration_s','sample_rate_hz','maximum_frequency_hz','reference_frequency_hz','minimum_frequency_hz','wall_budget_seconds','onsource_roll_off_s'):
        positive(config[name],name)
    if not config['minimum_frequency_hz']<config['maximum_frequency_hz']<=config['sample_rate_hz']/2:raise ValueError('Frequency band')
    rate=config['generation_sample_rate_hz'];gmax=config['generation_maximum_frequency_hz']
    if isinstance(rate,bool) or rate not in (4096,8192) or isinstance(gmax,bool):raise ValueError('Generation settings')
    positive(gmax,'generation maximum')
    if not config['maximum_frequency_hz']<=gmax or gmax!=rate/2 or config['sample_rate_hz']>rate:raise ValueError('Separated generation/data frequency contract')
    if 2*config['onsource_roll_off_s']>=config['duration_s']:raise ValueError('Tukey rolloff consumes whole window')
    time_prior=priors['geocent_time']
    start=config['segment_start_GPS'];end=start+config['duration_s'];roll=config['onsource_roll_off_s']
    if not math.isfinite(start) or time_prior['minimum']<=start+roll or time_prior['maximum']>=end-roll:
        raise ValueError('Time prior must be inside untapered analysis interval')
    if not config['quality_required'] or not config['injection_flags_required']:raise ValueError('Quality flags required')
    s=config['sampler']
    for name in ('nlive','walks','maxcall','workers','minimum_posterior_samples'):integer(s[name],name)
    integer(s['seed'],'seed',0);positive(s['minimum_effective_samples'],'ESS');positive(s['dlogz'],'dlogz')
    if s['workers']>28 or s['minimum_posterior_samples']<2 or s['maxcall']<=s['nlive']:raise ValueError('Invalid sampler allocation')
    if s.get('check_point',False) is not False or s.get('check_point_plot',False) is not False:raise ValueError('Checkpoint/plots prohibited in this adapter')


def build_priors(config):
    import bilby
    validate_config(config)
    primitives={k:getattr(bilby.core.prior,k) for k in ('Uniform','Sine','Cosine','Constraint')}
    priors={}
    for name,item in config['priors'].items():
        if isinstance(item,(int,float)):priors[name]=float(item)
        else:priors[name]=primitives[item['kind']](minimum=item['minimum'],maximum=item['maximum'],name=name,
                    **({'boundary':item['boundary']} if 'boundary' in item else {}))
    return bilby.core.prior.PriorDict(dictionary=priors,conversion_function=prior_conversion)


def terminal_state(sampler,settings):
    """Read immediately after sample() terminates, BEFORE adding live points."""
    import numpy as np
    count=int(sampler.ncall)
    if not len(sampler.saved_run['logz']):return dict(status='PARTIAL_NO_DEAD_POINTS',ncall=count,delta_logz=None)
    logz=float(sampler.saved_run['logz'][-1]);logvol=float(sampler.saved_run['logvol'][-1])
    live=np.asarray(sampler.live_logl,dtype=float)
    if not np.isfinite(live).all() or not np.isfinite([logz,logvol]).all():return dict(status='PARTIAL_NONFINITE_TERMINAL',ncall=count,delta_logz=None)
    delta=float(np.logaddexp(0,float(np.max(live))+logvol-logz))
    status='DLOGZ_REACHED_REQUIRES_ESS'
    if count>=settings['maxcall']:status='PARTIAL_MAXCALL_NOT_ACCEPTED'
    elif float(np.ptp(live))==0:status='PARTIAL_LIKELIHOOD_PLATEAU'
    elif delta>=settings['dlogz']:status='PARTIAL_DLOGZ_NOT_REACHED'
    return dict(status=status,ncall=count,delta_logz=delta,threshold=settings['dlogz'],before_add_live=True)


def sampler_class(settings):
    from bilby.core.sampler.dynesty import Dynesty
    class RecordedDynesty(Dynesty):
        @property
        def external_sampler_name(self):return 'dynesty'
        def _run_external_sampler_without_checkpointing(self):
            original=self.sampler.sample
            self.e2_terminal=None
            owner=self
            def observed(*args,**kwargs):
                yield from original(*args,**kwargs)
                owner.e2_terminal=terminal_state(owner.sampler,settings)
            self.sampler.sample=observed
            arguments=self.sampler_function_kwargs.copy()
            # dynesty counts maxcall within sample(); account for initialization.
            arguments['maxcall']=max(0,settings['maxcall']-int(self.sampler.ncall))
            try:self.sampler.run_nested(**arguments)
            finally:self.sampler.sample=original
            if self.e2_terminal is None:raise RuntimeError('Terminal convergence capture missing')
            return self.sampler.results
        def _generate_result(self,out):
            super()._generate_result(out)
            self.result.meta_data['e2_terminal']=self.e2_terminal
    return RecordedDynesty


def convergence(result,settings):
    import numpy as np
    state=dict(result.meta_data.get('e2_terminal',{}))
    if not state:raise ValueError('No terminal-state evidence')
    weights=np.asarray(result.nested_samples['weights'],dtype=float)
    if weights.ndim!=1 or not len(weights) or not np.isfinite(weights).all() or np.any(weights<0) or weights.sum()<=0:raise ValueError('Invalid nested weights')
    ess=float(weights.sum()**2/np.dot(weights,weights))
    state.update(ess=ess,minimum_ess=settings['minimum_effective_samples'],posterior_samples=len(result.posterior),
      log_evidence=float(result.log_evidence),log_evidence_err=float(result.log_evidence_err),
      ncall_reported=int(result.num_likelihood_evaluations))
    if not np.isfinite([state['log_evidence'],state['log_evidence_err']]).all():state['status']='PARTIAL_NONFINITE_EVIDENCE'
    if state['ncall_reported']!=state['ncall']:state['status']='PARTIAL_NCALL_MISMATCH'
    if state['status']=='DLOGZ_REACHED_REQUIRES_ESS':
        if ess<settings['minimum_effective_samples']:state['status']='PARTIAL_LOW_ESS'
        elif len(result.posterior)<settings['minimum_posterior_samples']:state['status']='PARTIAL_TOO_FEW_POSTERIOR_SAMPLES'
        else:state['status']='CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW'
    state['accepted_for_analysis']=state['status']=='CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW'
    return state


def posterior_columns(posterior,config):
    import numpy as np
    names=PHYSICAL+DEFORMATIONS
    if not set(names)<=set(posterior):raise ValueError('Incomplete paired physical/deformation posterior')
    columns={k:np.asarray(posterior[k],dtype=float) for k in names}
    if len(posterior)<2 or any(v.shape!=(len(posterior),) or not np.isfinite(v).all() for v in columns.values()):raise ValueError('Nonfinite/unpaired posterior')
    for name,value in config['fixed_deformation_parameters'].items():
        if not np.all(columns[name]==value):raise ValueError('Fixed deformation posterior differs')
    return columns


def edom_posterior_status(path,posterior,counter):
    import numpy as np
    bounds=None if posterior is None else {k:np.quantile(np.asarray(posterior[k],dtype=float),[.005,.995]).tolist() for k in ('mass_1','mass_2','chi_1','chi_2')}
    if bounds is not None and any(not np.isfinite(v).all() for v in bounds.values()):raise ValueError('Nonfinite posterior EDOM region')
    inside=count=0
    with Path(path).open(encoding='utf-8') as stream:
        for line in stream:
            r=json.loads(line);params=r['parameters'];count+=1
            if bounds is not None and all(bounds[k][0]<=params[k]<=bounds[k][1] for k in bounds):inside+=1
    with counter.get_lock():calls=int(counter[0]);measured=int(counter[2])
    if count!=measured or count>calls:raise ValueError('EDOM counter/log disagreement')
    status='EDOM_RECORDED_NO_POSTERIOR_REGION' if bounds is None else ('FAILED_EDOM_INSIDE_POSTERIOR_REGION' if inside else 'NO_EDOM_INSIDE_POSTERIOR_REGION')
    return dict(status=status,
                inside=inside if bounds is not None else None,edom=count,source_calls=calls,fraction=count/calls if calls else None,
                quantile_region=bounds,log_sha256=sha(path))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--job',required=True);parser.add_argument('--launch-context',required=True);args=parser.parse_args()
    reg,digest=checked_registration();jobs=load_jobs(reg,digest)
    if args.job not in jobs:raise ValueError('Unregistered job')
    cfg=jobs[args.job];authorize_event(reg,cfg['event'],cfg['mode']);validate_config(cfg)
    context,outdir=validate_launch(args.launch_context,reg,digest,args.job,cfg)
    # No Bilby/science initialization until launch identity and descriptors are checked.
    started=time.perf_counter();cpu=time.process_time();source_counter=None;likelihood_counter=None
    try:
        import numpy as np
        import bilby
        from gwpy.timeseries import TimeSeries
        from pseob_source import pseob_frequency_domain,parameter_conversion,set_deadline,set_cost_counter,set_edom_log
        from strain_io import window,offsource_psd
        from blinding import shifted_samples
        if multiprocessing.get_start_method()!='fork':raise RuntimeError('Pinned source counter requires WSL fork workers')
        source_counter=multiprocessing.Array('d',[0.,0.,0.],lock=True)
        likelihood_counter=multiprocessing.Array('d',[0.,0.,0.,0.],lock=True)
        set_cost_counter(source_counter);set_edom_log(outdir/'EDOM_LOG.jsonl');set_deadline(utc(context['stop_utc']).timestamp()-12)
        bilby.core.utils.random.seed(cfg['sampler']['seed']);np.random.seed(cfg['sampler']['seed'])
        bilby.core.utils.setup_logger(outdir=str(outdir),label=cfg['label'],log_level='INFO')
        ifos=bilby.gw.detector.InterferometerList(cfg['detectors']);receipts=[]
        for ifo in ifos:
            data=cfg['data'][ifo.name]
            f,p,receipt=offsource_psd(contained(data['offsource_path']),data['offsource_sha256'],cfg)
            y,fs,start=window(contained(data['onsource_path']),data['onsource_sha256'],cfg['segment_start_GPS'],cfg['duration_s'],cfg['quality_required'],cfg['injection_flags_required'])
            if fs!=cfg['sample_rate_hz'] or start!=cfg['segment_start_GPS']:raise ValueError('No implicit resampling or epoch shift')
            ifo.set_strain_data_from_gwpy_timeseries(TimeSeries(y,sample_rate=fs,t0=start))
            ifo.strain_data.roll_off=cfg['onsource_roll_off_s']
            ifo.minimum_frequency=cfg['minimum_frequency_hz'];ifo.maximum_frequency=cfg['maximum_frequency_hz']
            ifo.power_spectral_density=bilby.gw.detector.PowerSpectralDensity(frequency_array=f,psd_array=p)
            receipts.append(dict(detector=ifo.name,**receipt,actual_start_GPS=start,
                 onsource_sha256=data['onsource_sha256'],onsource_window='Tukey',roll_off_s=cfg['onsource_roll_off_s']))
        injection_receipt=None
        if cfg.get('injection') is not None:
            if cfg['mode']!='calibration':raise ValueError('Injections only in calibration jobs')
            from injection_design import inject_into_ifos
            injection_receipt=inject_into_ifos(ifos,cfg,reg)
            if not isinstance(injection_receipt,dict):raise ValueError('Injection receipt required')
            publish_new(outdir/'PRIVATE_INJECTION.json',injection_receipt)
        generator=bilby.gw.WaveformGenerator(duration=cfg['duration_s'],sampling_frequency=cfg['sample_rate_hz'],
          start_time=cfg['segment_start_GPS'],frequency_domain_source_model=pseob_frequency_domain,
          parameter_conversion=parameter_conversion,waveform_arguments=dict(waveform_approximant='pSEOBNRv4HM_PA',
          analysis_time_contract=dict(start_GPS=cfg['segment_start_GPS'],duration_s=cfg['duration_s'],roll_off_s=cfg['onsource_roll_off_s']),
          minimum_frequency=cfg['minimum_frequency_hz'],maximum_frequency=cfg['maximum_frequency_hz'],
          generation_maximum_frequency_hz=cfg['generation_maximum_frequency_hz'],
          generation_sample_rate_hz=cfg['generation_sample_rate_hz'],
          reference_frequency=cfg['reference_frequency_hz'],catch_waveform_errors=True))
        priors=build_priors(cfg)
        likelihood_type=counted_likelihood_class(bilby.gw.likelihood.GravitationalWaveTransient,likelihood_counter)
        likelihood=likelihood_type(interferometers=ifos,waveform_generator=generator,
          priors=priors,time_marginalization=False,distance_marginalization=False,phase_marginalization=False)
        likelihood_phases={'before_sampler_constructor':likelihood_snapshot(likelihood_counter)}
        cls=sampler_class(cfg['sampler'])
        sampler=cls(likelihood=likelihood,priors=priors,label=cfg['label'],outdir=str(outdir),plot=False,
          npool=cfg['sampler']['workers'],nlive=cfg['sampler']['nlive'],sample='rwalk',walks=cfg['sampler']['walks'],
          maxcall=cfg['sampler']['maxcall'],dlogz=cfg['sampler']['dlogz'],seed=cfg['sampler']['seed'],
          resume=False,check_point=False,check_point_plot=False,print_progress=False)
        likelihood_phases['after_sampler_constructor']=likelihood_snapshot(likelihood_counter)
        result=bilby.run_sampler(likelihood=likelihood,priors=priors,sampler=sampler,save='hdf5',plot=False,
          label=cfg['label'],outdir=str(outdir),meta_data=dict(registration_sha256=digest,job=args.job,
          model_scope='Aligned pSEOBNRv4HM_PA versus released precessing pSEOBNRv5PHM; broad INPUT priors'))
        likelihood_phases['after_run_sampler']=likelihood_snapshot(likelihood_counter)
        state=convergence(result,cfg['sampler']);time_guard(reg)
        edom=edom_posterior_status(outdir/'EDOM_LOG.jsonl',result.posterior,source_counter)
        if edom['inside']:
            state.update(status='FAILED_EDOM_INSIDE_POSTERIOR_REGION',accepted_for_analysis=False)
        publish_new(outdir/'EDOM_SUMMARY.json',edom)
        cost=dict(wall_seconds=time.perf_counter()-started,parent_cpu_seconds=time.process_time()-cpu,
          edom=edom,source_calls=int(source_counter[0]),source_total_wall_seconds=float(source_counter[1]),
          source_seconds_per_call=float(source_counter[1]/source_counter[0]) if source_counter[0] else None,
          sampler_ncall=state['ncall'],workers=cfg['sampler']['workers'],thread_caps_requested=1,
          likelihood_calls=likelihood_phases['after_run_sampler']['calls'],
          likelihood_counter=likelihood_phases['after_run_sampler'],likelihood_phase_snapshots=likelihood_phases,
          likelihood_time_scope='Summed per-invocation wall across processes, including failures; not job wall or exact CPU; independent of sampler_ncall and source_calls',
          maxcall_nominal=cfg['sampler']['maxcall'],sampler_call_overshoot=max(0,state['ncall']-cfg['sampler']['maxcall']),
          maxcall_scope='Dynesty iteration/batch bound may overshoot; not exact global 3M. Source calls include initialization/caching differences.',
          source_time_scope='Sum of per-call wall times across workers, not elapsed job wall or exact CPU time')
        publish_new(outdir/'PRIVATE_CONVERGENCE.json',dict(**state,cost=cost,registration_sha256=digest))
        if not state['accepted_for_analysis']:
            publish_new(outdir/'ANALYST_STATUS.json',dict(status=state['status'],accepted=False,
              job=args.job,registration_sha256=digest,cost=cost,posterior_kept_private=True))
            raise SystemExit(3)
        columns=posterior_columns(result.posterior,cfg)
        from remnant_conversion import derive
        conversion_started=time.perf_counter()
        derived,remnant_receipt=derive(columns,cfg,lambda:time_guard(reg))
        if set(derived)!=set(DERIVED_PHYSICAL):raise ValueError('Incomplete paired remnant conversion')
        if any(np.asarray(v).shape!=(len(result.posterior),) or not np.isfinite(v).all() for v in derived.values()):
            raise ValueError('Nonfinite/unpaired derived physical columns')
        columns.update(derived)
        time_guard(reg)
        cost.update(remnant_conversion_wall_seconds=time.perf_counter()-conversion_started,
          wall_seconds=time.perf_counter()-started,parent_cpu_seconds=time.process_time()-cpu)
        publish_new(outdir/'PRIVATE_REMNANT_CONVERSION.json',remnant_receipt)
        if cfg['mode']=='blind_test':
            science=shifted_samples({k:columns[k] for k in DEFORMATIONS},cfg['event'],reg)
            science['paired_physical_columns']={k:columns[k].tolist() for k in PHYSICAL+DERIVED_PHYSICAL}
        else:science=dict(status='NONBLIND_CALIBRATION_POSTERIOR_REQUIRES_REVIEW',columns={k:v.tolist() for k,v in columns.items()})
        science.update(registration_sha256=digest,job=args.job,cost=cost,PSD_receipts=receipts,injection_receipt=injection_receipt,
          convergence_status=state['status'],systematic_gate='UNPAID_TWO_FAMILY_CALIBRATION_REQUIRED',
          remnant_status=remnant_receipt['status'],remnant_conversion_receipt=remnant_receipt,
          redshift_status='DERIVED_FROM_DISTANCE_WITH_EXTERNAL_PLANCK18_INPUT_NOT_INDEPENDENT',
          raw_result_files={p.name:sha(p) for p in outdir.glob('*result*') if p.is_file()})
        publish_new(outdir/'ANALYST_OUTPUT.json',science)
        print(json.dumps(dict(status='RUN_FINISHED_REQUIRES_REVIEW',job=args.job,registration_sha256=digest)))
    except Exception as error:
        edom={'status':'EDOM_UNAVAILABLE_BEFORE_SOURCE_INITIALIZATION','log_sha256':None}
        if source_counter is not None:
            try:
                edom=edom_posterior_status(outdir/'EDOM_LOG.jsonl',None,source_counter)
                if not (outdir/'EDOM_SUMMARY.json').exists():publish_new(outdir/'EDOM_SUMMARY.json',edom)
            except Exception as audit_error:
                edom={'status':'EDOM_AUDIT_FAILED','exception_type':type(audit_error).__name__,
                      'message':str(audit_error),'posterior_region_evaluated':False}
        publish_new(outdir/'FAILURE.json',dict(status='FAILED_NO_ACCEPTED_POSTERIOR',error_type=type(error).__name__,edom=edom,
          registration_sha256=digest,job=args.job,wall_seconds=time.perf_counter()-started,
          source_calls=int(source_counter[0]) if source_counter is not None else None,
          likelihood_counter=likelihood_snapshot(likelihood_counter) if likelihood_counter is not None else None,
          detail_policy='Traceback only in PRIVATE.log'))
        raise


if __name__=='__main__':main()
