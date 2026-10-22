"""Planning only, with the already pinned background and total reader sigmas.

No local H0 center is extracted. These are nominal expected separations,
not observed scores, calibrated tail sigmas, or physical covariance admissions.
"""
from pathlib import Path
import hashlib
import json
import math

HERE=Path(__file__).resolve().parent


def run():
    pin=json.loads((HERE/'SOURCE_PINS_R1.json').read_text(encoding='utf-8'))['latest_spec']
    raw=Path(pin['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError('SPEC_PIN_MISMATCH')
    s=json.loads(raw)['spec']
    ALPHA_FINE_CODATA_2018=s['beta']['alpha_read']
    beta=ALPHA_FINE_CODATA_2018*math.sqrt(math.e)
    law=s['lei'];z=law['z_star'];om=law['Omega_m'];orr=law['Omega_r']
    E=math.sqrt(om*(1+z)**3+orr*(1+z)**4+1-om-orr)
    K=E**(2*beta/3)
    if not math.isclose(K,law['K_frozen_V1'],rel_tol=0,abs_tol=1e-12):raise ValueError('K_MISMATCH')
    H=s['fundos']['BG1']['H0'];sb=s['fundos']['BG1']['sigma'];separation=(K-1)*H
    rows=[]
    for family in ['P_primaria','N_sem_cefeidas']:
        ids=s['familias'][family]['ids']
        sigmas=[s['leitores'][r]['sigma'] for r in ids]
        if any(type(x) not in (int,float) or not math.isfinite(x) or x<=0 for x in sigmas):raise ValueError('SIGMA')
        k=min(range(len(ids)),key=lambda i:(sigmas[i],i));sl=sigmas[k]
        for test,f in [('LCDM_NULL_CONTRAST',1.0),('TGL_COMPATIBILITY_CONTRAST',K)]:
            worst=sl+abs(f)*sb
            independent=math.hypot(sl,f*sb)
            rows.append({'family':family,'test':test,'coefficient_f':f,
                'fixed_local_minimax_reader_by_sigma_only':ids[k],
                'local_minimax_sigma':sl,'background_sigma':sb,
                'nominal_mean_separation':separation,
                'se_all_correlations_unknown':worst,
                'se_background_independent_named_assumption':independent,
                'nominal_separation_in_worst_case_se':separation/worst,
                'nominal_separation_with_independent_background':separation/independent,
                'worst_case_nominal_separation_ge5':separation/worst>=5,
                'new_observed_score':None,'physical_covariance_admitted':False})
    return {'status':'CONDITIONAL_DESIGN_ALGEBRA_ONLY','source_sha256':pin['sha256'],
            'beta_runtime':beta,'K_runtime':K,'background':'preselected BG1 only',
            'rows':rows,'no_local_centers_extracted':True,
            'K_cosmological_uncertainty':'held at pinned inputs; R3 remains separate',
            'covariance_hypotheses':'correct total marginal sigmas; common unbiased target; optional background independence explicitly named',
            'statistical_tail_calibrated':False,'observed_composite':False}
