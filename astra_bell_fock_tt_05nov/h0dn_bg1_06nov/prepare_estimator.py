"""Build and freeze inference from covariance only; no observed data input."""
from pathlib import Path
import hashlib, json, numpy as np
from scipy.stats import norm
from estimator import geometry, pin

BASE=Path(__file__).resolve().parent

def write_new(path,raw):
    if path.exists(): raise FileExistsError(path)
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_bytes(raw)
    assert tmp.stat().st_size==len(raw);tmp.replace(path)

def main():
    network=BASE/'network'/'network.npz'
    background=BASE/'background'/'BG1.json'
    b=json.loads(background.read_text(encoding='utf-8'))
    with np.load(network,allow_pickle=False) as d:
        A=d['A'];C=d['C'];c=d['c_cepheid'];h_index=int(d['h_index'])
    models,metadata,null=geometry(A,C,c,h_index)
    cb=np.asarray(b['covariance'],float)
    gh=np.asarray(b['gradient_h'],float);gk=np.asarray(b['gradient_k'],float)
    if np.linalg.eigvalsh(cb).min()<=0:raise ValueError('BG covariance not positive definite')
    vb=float(gh@cb@gh);vbt=float((gh+gk)@cb@(gh+gk))
    logK=float(b['logK']);weights=np.stack([m['influence'] for m in models.values()])
    vs=np.array([m['variance_h'] for m in models.values()])
    sd0=np.sqrt(vs+vb);sdt=np.sqrt(vs+vbt)
    names=list(models)
    manifest={'status':'CONDITIONAL_GAUSSIAN_PROSPECTIVE','network_geometry':metadata,
              'background_variance_logH':vb,'background_variance_logHK':vbt,
              'K':b['K'],'logK':logK,'models':{}}
    for i,(name,m) in enumerate(models.items()):
        row={k:v for k,v in m.items() if k!='influence'}
        D=logK/sd0[i]
        row.update(sd_null=float(sd0[i]),sd_tgl=float(sdt[i]),D=float(D),
                   power_at_5sigma=float(norm.sf(5-D)),
                   delta_C_to_shift_5sigma_mag=float(5*sd0[i]/m['response_cepheid']) if abs(m['response_cepheid'])>1e-12 else None)
        row['omitted_bias_stress']=[{'delta_mag':delta,'mean_Z_null':float(m['response_cepheid']*delta/sd0[i]),
                                    'false_positive_probability':float(norm.sf(5-m['response_cepheid']*delta/sd0[i]))}
                                    for delta in [-.05,.05]]
        row['unmodelled_random_mode_stress']=[]
        for tau in [.01,.03,.05,.10]:
            truevar=sd0[i]**2+(m['response_cepheid']*tau)**2
            row['unmodelled_random_mode_stress'].append({'extra_sd_mag':tau,
                'fixed_score_true_null_sd':float(np.sqrt(truevar)/sd0[i]),
                'actual_alpha_if_unadjusted':float(norm.sf(5*sd0[i]/np.sqrt(truevar))),
                'D_if_conservatively_recalibrated':float(logK/np.sqrt(truevar)),
                'power_if_conservatively_recalibrated':float(norm.sf(5-logK/np.sqrt(truevar)))})
        manifest['models'][name]=row
    # Explicit joint covariance: published network plus independent background block.
    joint=np.zeros((C.shape[0]+len(gh),)*2);joint[:len(C),:len(C)]=C;joint[len(C):,len(C):]=cb
    out=BASE/'estimator_frozen.npz'
    with out.open('xb') as f:
        np.savez_compressed(f,weights=weights,null_basis=null,gradient_h=gh,gradient_k=gk,
            sd_null=sd0,sd_tgl=sdt,logK=logK,H0=float(b['H0']),model_names=np.asarray(names),
            C_joint=joint,signal_local=A[:,h_index]*logK)
    write_new(BASE/'PROSPECTIVE_GEOMETRY.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8'))
    files=[BASE/'analysis_plan.json',BASE/'estimator.py',Path(__file__),network,BASE/'network'/'MANIFEST.json',background,BASE/'background'/'build_bg1.py',out,BASE/'PROSPECTIVE_GEOMETRY.json']
    freeze={'status':'FROZEN_BEFORE_MASKED_INJECTIONS','scope':'covariance-only design; known public historical aggregates are not blind',
            'files':[pin(p) for p in files], 'null_alpha':float(norm.sf(5)),
            'joint_cross_block':'zero under conditional independence of local network and Planck+DESI BG1; not empirical covariance measurement'}
    write_new(BASE/'FREEZE.json',json.dumps(freeze,ensure_ascii=False,indent=2).encode('utf-8'))
    print(json.dumps(manifest,ensure_ascii=False))

if __name__=='__main__':main()
