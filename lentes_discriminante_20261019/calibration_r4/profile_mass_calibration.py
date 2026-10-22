"""Synthetic identifiable scalar signal after mass-sheet and background profiling.

This is an explicit Gaussian-in-log planning model, not the observed lens likelihood.
Published posterior H0 errors are NOT used as component errors here.
"""
from pathlib import Path
import datetime, hashlib, json, math, re, time
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent
SPEC = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json')
UM = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')

def pin(p):
    return {'path':str(p), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def save(name, obj):
    with (ROOT/name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, allow_nan=False)

def find(obj, key):
    if isinstance(obj, dict):
        if key in obj: yield obj[key]
        for v in obj.values(): yield from find(v, key)
    elif isinstance(obj, list):
        for v in obj: yield from find(v, key)

def explicit_profile(n, signal, sd, si, sc, sb, free_common=False, free_bg=False):
    # y = a log(K) + h - m_common - m_i + e_i; null a=0.
    columns, scales = [], []
    if sb > 0 or free_bg: columns.append(np.ones(n)); scales.append(None if free_bg else sb)
    if sc > 0 or free_common: columns.append(-np.ones(n)); scales.append(None if free_common else sc)
    if si > 0:
        for i in range(n): columns.append(-np.eye(n)[:, i]); scales.append(si)
    A = np.column_stack(columns)
    prior = np.diag([0 if s is None else 1/s for s in scales])
    design = np.vstack([A/sd, prior])
    target = np.concatenate([np.full(n, signal/sd), np.zeros(len(scales))])
    fit = np.linalg.lstsq(design, target, rcond=1e-12)[0]
    residual = target - design @ fit
    return float(residual @ residual)

def main():
    for name in ['PLAN_R4.json','RESULT_R4.json']:
        if (ROOT/name).exists(): raise FileExistsError(name)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat(); tic=time.perf_counter()
    plan = {
        'status':'INPUT_SYNTHETIC_PRECOMPUTATION', 'created_utc':started,
        'model':'y_i=log(H_read_i/H_bg_reference)=a logK+h-m_common-m_i+e_i',
        'alternative':'a=1, zero nuisances (Asimov); null a=0 with nuisance profiling',
        'likelihood':'independent Gaussian log errors: delay e_i, individual mass m_i, common mass m_common, external background h. Independent calibration data centered at zero.',
        'physical_scope':'Scalar contract ONLY. Mass-sheet equivalence exact for images and Fermat differences; no claim of unchanged kinematics. Full TGL trajectory map remains OPEN.',
        'sigma_delay_log':0.04, 'sigma_individual_mass_log':0.03,
        'sigma_common_mass_log':[0,0.005,0.01,0.015,0.02,0.03],
        'sample_sizes':[1,8,11,30,100],
        'error_provenance':'All lens-component widths are INPUT planning choices, not measured errors or CosmoSIS defaults. No published H0 posterior is reused as raw delay error.',
        'sigma_background_log':'delta-method BG1 sigma/H0 from draft; exact Gaussian log assumption for this synthetic model',
        'median_target':5, 'discovery_probability_target':0.90,
        'checks':['symbolic 2D Fermat MST identity','direct nuisance least-squares vs analytic Schur value','free common mass and free background erase signal','deterministic negative copy does not add information'],
        'tolerance_chi2_absolute':1e-8, 'tolerance_free_chi2':1e-18,
        'sources':[pin(SPEC),pin(UM),pin(BASE/'reading_r3'/'SCALAR_ANCHOR_RESULT_R3.json')],
        'script':pin(Path(__file__))}
    save('PLAN_R4.json',plan)
    spec=json.loads(SPEC.read_text(encoding='utf-8'))
    law=next(x for x in find(spec,'lei') if isinstance(x,dict) and 'Omega_r' in x)
    bg=next(x['BG1'] for x in find(spec,'fundos') if isinstance(x,dict) and 'BG1' in x)
    alpha=float(re.search(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',UM.read_text(encoding='utf-8'),re.M).group(1))
    beta=alpha*math.sqrt(math.e); z=law['z_star']; om=law['Omega_m']; ort=law['Omega_r']
    E=math.sqrt(om*(1+z)**3+ort*(1+z)**4+1-om-ort)
    K=E**(2*beta/3); signal=math.log(K); sb=bg['sigma']/bg['H0']
    assert abs(K-law['K_frozen_V1'])<1e-12
    # Exact symbolic identity for arbitrary image coordinates and potential value.
    x,y,u,v,psi,lam=sp.symbols('x y u v psi lam', real=True)
    phi=((x-u)**2+(y-v)**2)/2-psi
    psi_lam=lam*psi+(1-lam)*(x*x+y*y)/2
    phi_lam=((x-lam*u)**2+(y-lam*v)**2)/2-psi_lam
    mst=sp.expand(phi_lam-lam*phi-lam*(lam-1)*(u*u+v*v)/2)
    assert mst==0
    rows=[]; max_error=0.0
    sd=plan['sigma_delay_log']; si=plan['sigma_individual_mass_log']
    # One-sided Gaussian known-sign discovery; 90% power is NOT median5.
    from statistics import NormalDist
    targets={'median5':5.0,'one_sided5_with_90percent_power':5.0+NormalDist().inv_cdf(0.90)}
    for sc in plan['sigma_common_mass_log']:
        ceiling=signal/math.hypot(sc,sb)
        needed={}
        for label,target in targets.items():
            budget=(signal/target)**2-sc*sc-sb*sb
            needed[label]=math.ceil((sd*sd+si*si)/budget) if budget>0 else None
        for n in plan['sample_sizes']:
            variance=(sd*sd+si*si)/n+sc*sc+sb*sb
            q=signal*signal/variance
            explicit=explicit_profile(n,signal,sd,si,sc,sb)
            max_error=max(max_error,abs(q-explicit)); assert abs(q-explicit)<1e-8
            rows.append({'n':n,'sigma_common_mass_log':sc,'Z_Asimov':math.sqrt(q),'profiled_chi2':explicit,
                         'ceiling_N_infinite':ceiling,'required_N':needed})
    free_mass=explicit_profile(11,signal,sd,si,0,sb,free_common=True)
    free_bg=explicit_profile(11,signal,sd,si,.01,0,free_bg=True)
    assert free_mass<1e-18 and free_bg<1e-18
    # A deterministic negative duplicates data, with singular joint covariance.
    n=11; sc=.01; C=np.eye(n)*(sd*sd+si*si)+(sc*sc+sb*sb)*np.ones((n,n))
    s=np.full(n,signal); both=np.concatenate([s,-s])
    cov=np.block([[C,-C],[-C,C]])
    q_one=float(s@np.linalg.solve(C,s)); q_both=float(both@np.linalg.pinv(cov,rcond=1e-12)@both)
    assert abs(q_one-q_both)<1e-8
    result={'status':'DERIVED_CONDITIONAL_SYNTHETIC_ONLY','beta_runtime':beta,'K_runtime':K,'logK':signal,
       'background_log_sigma':sb,'lambda_GR_imitation_for_true_lambda1':1/K,
       'mst_identity_verified':True,'mst_formula':'phi_lambda=lambda phi + lambda(lambda-1)|source|^2/2; differences scale by lambda',
       'profile_formula':'Z=logK/sqrt((sigma_delay^2+sigma_mass_individual^2)/N+sigma_mass_common^2+sigma_bg^2)',
       'targets':targets,'rows':rows,'common_mass_sigma_max_infinite_N_for_median5':math.sqrt((signal/5)**2-sb*sb),
       'common_mass_sigma_max_with_1percent_independent_mean_for_median5':math.sqrt((signal/5)**2-sb*sb-.01**2),
       'control_free_common_mass_chi2':free_mass,'control_free_background_chi2':free_bg,
       'profile_max_absolute_error':max_error,'negative_copy_control':{'chi2_original':q_one,'chi2_with_correlated_negative':q_both,'rank_original':n,'rank_augmented':int(np.linalg.matrix_rank(cov))},
       'limits':['K fixed; physical lens map OPEN','independent log-Gaussian synthetic calibrations','not observed p-value or forecast from raw data','mean mass calibration and intrinsic population scatter are different parameters','no double counting of published posterior H0 errors'],
       'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-tic,
       'plan':pin(ROOT/'PLAN_R4.json'),'script':pin(Path(__file__))}
    save('RESULT_R4.json',result)
    print(json.dumps({k:result[k] for k in ['status','logK','lambda_GR_imitation_for_true_lambda1','common_mass_sigma_max_infinite_N_for_median5','common_mass_sigma_max_with_1percent_independent_mean_for_median5','profile_max_absolute_error','negative_copy_control']}))

if __name__=='__main__': main()
