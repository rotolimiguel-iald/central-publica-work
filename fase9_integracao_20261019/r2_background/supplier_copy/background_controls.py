"""Five data-independent CAMB background controls. Default: validation, NO science.

Run mode is for a subsequent ROOT-approved unit. No observational inputs, fitting,
likelihood, table extrapolation, network, or historical motor imports are supported.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from fractions import Fraction

HERE=Path(__file__).resolve().parent
C_KM_S=299792.458

def read(name):return json.loads((HERE/name).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(path,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    tmp=path.with_name(path.name+'.new')
    if path.exists():raise FileExistsError(path)
    with tmp.open('xb') as f:f.write(data)
    if tmp.stat().st_size!=len(data):raise RuntimeError('Incomplete write')
    tmp.rename(path)
def require(ok,why):
    if not ok:raise ValueError(why)
def check_theta(theta,p):
    require(len(theta)==3,'Three cosmological coordinates required')
    for name,value in zip(p['prior']['coordinates'],theta):
        require(isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value),'Non-finite coordinate')
        lo,hi=p['prior']['bounds'][name]
        require(lo<=value<=hi,'OUTSIDE_PRIOR_DOMAIN_ERROR: '+name)
def validate(p):
    require(p['scope']=='PREDICTIONS_ONLY_NO_OBSERVED_CENTERS_NO_LIKELIHOOD_NO_EVIDENCE_NO_NETWORK','Wrong scope')
    require(p['prior']['coordinates']==['H0','ombh2','omch2'],'Unexpected coordinates')
    vol=Fraction(1)
    for a,b in p['prior']['bounds'].values():vol*=Fraction(str(b))-Fraction(str(a))
    require(vol==Fraction(p['prior']['volume_exact']) and Fraction(p['prior']['density_exact'])*vol==1,'Prior not normalized')
    require(len(p['points'])==5 and len(p['accuracy_profiles'])==2,'Control budget changed')
    require(len({x['id'] for x in p['points']})==5,'Duplicate point ID')
    for point in p['points']:check_theta(point['theta'],p)
    require(p['resources']['max_solver_calls']==10,'Unexpected call budget')
    require(p['background']['omk']==0 and p['background']['w']==-1 and p['background']['wa']==0,'Not flat Lambda background')
    require(p['h5_candidate']['CMB']=='standard rstar and DMstar unchanged','H5 changes CMB')
    for z in p['redshifts']['low_z_controls']:require(0<=z<=3,'Redshift outside candidate domain')
    require(p['table_alternative']['padded_nodes']==math.prod(p['table_alternative']['padded_shape']),'Grid count error')
    bbn=read('BBN_METADATA.json'); b=p['background']
    dn=b['nnu']-b['standard_neutrino_neff']
    require(bbn['delta_N_domain'][0]<=dn<=bbn['delta_N_domain'][1],'BBN Neff coverage missing')
    lo,hi=p['prior']['bounds']['ombh2']
    # TCMB equals table reference, hence no baryon-temperature rescaling here.
    require(b['TCMB_K']==2.7255,'Re-check BBN temperature domain first')
    require(bbn['ombh2_domain'][0]<=lo<hi<=bbn['ombh2_domain'][1],'BBN baryon domain missing')
    return {'status':'CONTRACT_VALIDATED_NO_SOLVER','solver_calls':0,'prior_volume':str(vol),'density':str(1/vol),'points':5,'planned_solver_calls':10}

def check_delivery():
    manifest=read('MANIFESTO_ENTREGA.json')
    indexed={x['name']:x for x in manifest['files']}
    for name in ('PROTOCOL.json','RUNTIME_METADATA.json','BBN_METADATA.json','background_controls.py'):
        require(name in indexed and sha(HERE/name)==indexed[name]['sha256'],'Delivery pin mismatch: '+name)

def runtime_check():
    info=read('RUNTIME_METADATA.json')
    for name,version in info['packages'].items():
        require(importlib.metadata.version(name)==version,'Runtime version changed: '+name)
    spec=importlib.util.find_spec('camb')
    require(spec is not None,'CAMB unavailable')
    root=Path(spec.origin).parent
    for item in info['package_files']:
        f=root/item['relative_path']
        require(f.is_file() and sha(f)==item['sha256'],'CAMB file changed: '+item['relative_path'])
    return info

def execute_worker_once(p,point_id,profile_id,output,solver=None):
    """Persist an exclusive logical claim BEFORE any solver, even for direct CLI.

    Claims survive failure, interruption and success. Output renaming never creates
    a new attempt for the same protocol/point/profile. A claim without terminal
    receipt means uncertain; neither main nor this worker retries it.
    """
    output=Path(output).resolve()
    require(output.is_relative_to(HERE.resolve()),'Worker output outside unit')
    require(output.parent.is_dir(),'Worker parent directory missing')
    require(point_id in {x['id'] for x in p['points']},'Unknown control point')
    require(profile_id in p['accuracy_profiles'],'Unknown accuracy profile')
    if output.exists() or output.with_name(output.name+'.new').exists() or output.with_name(output.name+'.claim.json').exists():
        raise FileExistsError('Existing output or partial output; solver not invoked')
    logical={'request_id':p['request_id'],'protocol_sha256':sha(HERE/'PROTOCOL.json'),
             'point_id':point_id,'profile_id':profile_id}
    key=hashlib.sha256(json.dumps(logical,sort_keys=True).encode()).hexdigest()
    claims=HERE/'worker_claims';claims.mkdir(exist_ok=True)
    claim=claims/(key+'.claim.json')
    terminal=claims/(key+'.terminal.json')
    if terminal.exists():raise FileExistsError('Terminal attempt already recorded; no retry')
    payload={**logical,'output':str(output),'engine_sha256':sha(Path(__file__)),
             'status':'CLAIMED_MAY_HAVE_RUN_NO_RETRY','pid':os.getpid(),'timestamp_unix':time.time()}
    # open(x) is the atomic cross-process admission decision, not exists().
    # A partial claim is deliberately retained and blocks later entry.
    with claim.open('x',encoding='utf-8') as f:
        json.dump(payload,f,sort_keys=True,allow_nan=False)
        f.flush();os.fsync(f.fileno())
    try:
        # Reserve the output as well: distinct logical attempts cannot race for it.
        with output.with_name(output.name+'.claim.json').open('x',encoding='utf-8') as f:
            json.dump(payload,f,sort_keys=True,allow_nan=False)
            f.flush();os.fsync(f.fileno())
        # Re-check after claiming, before a solver can spend resources.
        if output.exists() or output.with_name(output.name+'.new').exists():
            raise FileExistsError('Output appeared after claim; no solver invoked')
        result=(solver or prediction_worker)(p,point_id,profile_id)
        write_new(output,result)
        write_new(terminal,{'status':'RESULT_WRITTEN_NO_RETRY','claim':str(claim),
                           'output':str(output),'output_sha256':sha(output)})
        return result
    except BaseException as exc:
        # Abrupt process death can prevent this receipt, but not erase the claim.
        if not terminal.exists():
            write_new(terminal,{'status':'FAILED_OR_INTERRUPTED_NO_RETRY','claim':str(claim),
                               'error_type':type(exc).__name__,'error':str(exc)})
        raise


def prediction_worker(p,point_id,profile_id):
    # This function alone imports CAMB/numpy. Never called by validation.
    runtime_check()
    import camb
    import numpy as np
    import resource
    point=next(x for x in p['points'] if x['id']==point_id)
    profile=p['accuracy_profiles'][profile_id]; b=p['background']
    H0,wb,wc=point['theta'];check_theta(point['theta'],p)
    start=time.perf_counter()
    pars=camb.CAMBparams()
    pars.set_classes(recombination_model=b['recombination_class'])
    pars.Recomb.set_params(recfast_approx_model=b['recfast_approx_model'])
    pars.set_dark_energy(w=b['w'],wa=b['wa'],dark_energy_model=b['dark_energy_model'])
    pars.set_cosmology(H0=H0,ombh2=wb,omch2=wc,omk=b['omk'],mnu=b['mnu_eV'],
      neutrino_hierarchy=b['neutrino_hierarchy'],num_massive_neutrinos=b['num_massive_neutrinos'],
      nnu=b['nnu'],standard_neutrino_neff=b['standard_neutrino_neff'],meffsterile=b['meffsterile'],
      TCMB=b['TCMB_K'],YHe=None,bbn_predictor=b['bbn_predictor'],tau=b['tau'])
    pars.set_accuracy(AccuracyBoost=profile['AccuracyBoost'])
    pars.WantCls=False;pars.WantTransfer=False;pars.WantDerivedParameters=True
    require(0<pars.YHe<1,'Invalid BBN helium fraction')
    data=camb.get_background(pars,no_thermo=False)
    derived=data.get_derived_params()
    zs=float(derived['zstar']);zd=float(derived['zdrag'])
    rs=float(derived['rstar']);rd=float(derived['rdrag'])
    zsarr=np.array(p['redshifts']['low_z_controls'],dtype=float)
    hs=np.asarray(data.hubble_parameter(zsarr),dtype=float)
    # Array interface explicitly uses tol; scalar CAMB distance ignores that argument.
    dm=np.asarray(data.comoving_radial_distance(zsarr,tol=profile['distance_array_tol']),dtype=float)
    dh=C_KM_S/hs;dv=np.cbrt(zsarr*dm**2*dh)
    dmstar=float(data.comoving_radial_distance(np.array([zs]),tol=profile['distance_array_tol'])[0])
    elaw=float(data.hubble_parameter(p['redshifts']['z_star_law']))/H0
    estar=float(data.hubble_parameter(zs))/H0
    om=sum(float(data.get_Omega(k,z=0)) for k in ('cdm','baryon','nu'))
    out={'point_id':point_id,'profile':profile_id,'theta':point['theta'],'YHe':float(pars.YHe),
      'zstar':zs,'zdrag':zd,'rstar_Mpc':rs,'rdrag_Mpc':rd,'DMstar_Mpc':dmstar,
      'E_law':elaw,'E_at_zstar':estar,'I_law':(2/3)*math.log(elaw),'Omega_m0':om,
      'R':math.sqrt(om)*H0*dmstar/C_KM_S,'lA':math.pi*dmstar/rs,
      'low_z':[{'z':float(z),'H_km_s_Mpc':float(h),'E':float(h/H0),'DM_Mpc':float(m),
                'DH_Mpc':float(d),'DV_Mpc':float(v),'DM_over_rd':float(m/rd),'DH_over_rd':float(d/rd),'DV_over_rd':float(v/rd)}
               for z,h,m,d,v in zip(zsarr,hs,dm,dh,dv)],
      'H5_BAO_only':[{'rd_Mpc':r,'q':r/rd,'q_prior_density':rd/30,
                     'DM_over_rd':(dm/r).tolist(),'DH_over_rd':(dh/r).tolist(),'DV_over_rd':(dv/r).tolist()}
                    for r in p['h5_candidate']['theory_control_rd_Mpc']],
      'full_CAMBparams':str(pars),'elapsed_solver_seconds':time.perf_counter()-start,
      'peak_worker_rss_KiB_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'physics_status':'STANDARD_BACKGROUND_THEORY_CONTROL_NOT_OBSERVATION'}
    for k in ('zstar','zdrag','rstar_Mpc','rdrag_Mpc','DMstar_Mpc','E_law','E_at_zstar','Omega_m0','R','lA'):
        require(math.isfinite(out[k]) and out[k]>0,'Invalid positive prediction: '+k)
    require(math.isfinite(out['I_law']),'Invalid I_law')
    require(np.all(np.isfinite(hs)) and np.all(hs>0),'Invalid H')
    require(np.all(np.isfinite(dm)) and np.all(dm>=0),'Invalid distance')
    require(abs(hs[0]/H0-1)<=p['precision']['E0_absolute_tolerance'],'E(0) normalization failure')
    require(abs(dm[0])<=p['precision']['z0_DM_absolute_Mpc'],'DM(0) failure')
    require(abs(dv[0])<=p['precision']['z0_DV_absolute_Mpc'],'DV(0) failure')
    require(np.all(np.diff(dm)>0),'Distances not monotonic on positive z grid')
    return out

def compare(a,b,p):
    errors={}
    fields=('YHe','zstar','zdrag','rstar_Mpc','rdrag_Mpc','DMstar_Mpc','E_law','E_at_zstar','I_law','Omega_m0','R','lA')
    def rel(key,x,y):
        require(math.isfinite(x) and math.isfinite(y),'Nonfinite comparison')
        if y==0:
            require(x==0,'Zero-reference mismatch: '+key); errors[key]=0.0
        else:errors[key]=abs(x-y)/abs(y)
    for k in fields:rel(k,a[k],b[k])
    for i,(x,y) in enumerate(zip(a['low_z'],b['low_z'])):
        require(x['z']==y['z'],'Redshift mismatch')
        for k in ('H_km_s_Mpc','E','DM_Mpc','DH_Mpc','DV_Mpc','DM_over_rd','DH_over_rd','DV_over_rd'):
            rel(f'z{i}/{k}',x[k],y[k])
    worst=max(errors,key=errors.get)
    return {'status':'PASS_AT_LISTED_POINT' if errors[worst]<=p['precision']['relative_prediction_tolerance'] else 'PRECISION_CONTROL_FAILED',
            'maximum_relative_difference':errors[worst],'worst_field':worst,'relative_differences':errors}

def run_controls(p,output_name):
    require(Path(output_name).name==output_name and output_name not in ('.','..'),'Output must be a new local folder name')
    check_delivery();runtime_check()
    outdir=HERE/output_name;outdir.mkdir(exist_ok=False)
    started=time.monotonic();results=[];measurements=[];calls=0
    receipt={'status':'IN_PROGRESS','protocol_sha256':sha(HERE/'PROTOCOL.json'),'engine_sha256':sha(Path(__file__)),
             'scope':p['scope'],'observed_inputs':False,'solver_calls_attempted':0,'results':results,'measurements':measurements}
    try:
        for point in p['points']:
            pair={}
            for profile in ('baseline','reference'):
                remaining=p['resources']['total_timeout_seconds']-(time.monotonic()-started)
                require(remaining>0,'Total time budget exhausted')
                calls+=1;require(calls<=p['resources']['max_solver_calls'],'Call budget exhausted')
                filename=f'{point["id"]}_{profile}.json'
                cmd=[sys.executable,str(Path(__file__).resolve()),'--worker',point['id'],profile,'--worker-output',str(outdir/filename)]
                env=dict(os.environ)
                env.update({n:'1' for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')})
                env['PYTHONDONTWRITEBYTECODE']='1'
                t=time.perf_counter()
                proc=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=min(remaining,p['resources']['timeout_seconds_per_worker']))
                elapsed=time.perf_counter()-t
                require(proc.returncode==0,f'COMPUTATIONAL_FAILURE_NO_ZERO_LIKELIHOOD: {point["id"]}/{profile}: {proc.stderr[-4000:]}')
                pair[profile]=json.loads((outdir/filename).read_text())
                measurements.append({'point':point['id'],'profile':profile,'wall_seconds':elapsed,'peak_worker_rss_KiB':pair[profile]['peak_worker_rss_KiB_linux']})
            comparison=compare(pair['baseline'],pair['reference'],p)
            results.append({'point':point['id'],**comparison})
            require(comparison['status']=='PASS_AT_LISTED_POINT','Precision tolerance exceeded; no automatic retry')
        receipt['status']='FIVE_THEORY_CONTROLS_PASS_NOT_FULL_PRIOR_QUALIFIED'
    except Exception as exc:
        receipt['status']='STOPPED_COMPUTATIONAL_OR_PRECISION_FAILURE'
        receipt['error']=f'{type(exc).__name__}: {exc}'
    receipt['solver_calls_attempted']=calls
    receipt['elapsed_total_seconds']=time.monotonic()-started
    write_new(outdir/'CONTROL_RECEIPT.json',receipt)
    print(json.dumps({'status':receipt['status'],'receipt':str(outdir/'CONTROL_RECEIPT.json')}))
    return 0 if receipt['status']=='FIVE_THEORY_CONTROLS_PASS_NOT_FULL_PRIOR_QUALIFIED' else 1

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate-only',action='store_true')
    parser.add_argument('--run-controls',action='store_true')
    parser.add_argument('--ack-root-review',action='store_true')
    parser.add_argument('--output',default='theory_controls_01')
    parser.add_argument('--worker',nargs=2,help=argparse.SUPPRESS)
    parser.add_argument('--worker-output',help=argparse.SUPPRESS)
    args=parser.parse_args();p=read('PROTOCOL.json');summary=validate(p)
    if args.worker:
        check_delivery()
        output=Path(args.worker_output).resolve()
        require(output.is_relative_to(HERE.resolve()),'Worker output outside unit')
        execute_worker_once(p,*args.worker,output);return 0
    if not args.run_controls:
        print(json.dumps(summary));return 0
    require(not args.validate_only and args.ack_root_review,'Explicit subsequent ROOT review acknowledgment required')
    return run_controls(p,args.output)
if __name__=='__main__':sys.exit(main())