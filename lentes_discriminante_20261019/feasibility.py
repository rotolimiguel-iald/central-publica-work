"""Conditional lensing sensitivity, not an observed TGL test or lens prediction."""
from pathlib import Path
import json, math, re, hashlib, urllib.request, datetime
ROOT=Path(__file__).resolve().parent
def new(name,data):
    raw=(data if isinstance(data,str) else json.dumps(data,ensure_ascii=False,indent=2)).encode('utf-8')
    with (ROOT/name).open('xb') as f:f.write(raw)
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
if __name__=='__main__':
    new('FORECAST_PLAN.json',{'status':'INPUT_PLANNING_ONLY','observed_data':False,
      'signal':'delta=c_response*beta; c_response=1 is an illustrative assumption, NOT a derived lensing law',
      'statistical_model':'independent identical Gaussian fractional errors plus one common Gaussian calibration offset',
      'sigma_independent':[0.01,0.03,0.05,0.1],'sigma_common':[0,0.001,0.003],
      'criterion':'median Gaussian separation delta/sigma_total >=5; not 90% discovery power and not an observed p-value',
      'nuisance_control':'unconstrained common offset exactly absorbs a common fractional signal',
      'two_models':'same nuisance freedom; preregister physical response and selection before observed verdict'})
    p=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
    text=p.read_text(encoding='utf-8'); m=re.search(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*$',text,re.M)
    assert m
    alpha=float(m.group(1)); beta=alpha*math.sqrt(math.e)
    rows=[]
    for s in [0.01,0.03,0.05,0.1]:
        for common in [0,0.001,0.003]:
            denominator=(beta/5)**2-common**2
            n=math.ceil(s*s/denominator) if denominator>0 else None
            rows.append({'sigma_independent':s,'sigma_common':common,'minimum_N':n,
                         'median_Z_at_N':beta/math.sqrt(s*s/n+common**2) if n else None})
    # Exact algebraic identity: beta*1 is in the span of the free mass/calibration offset.
    new('FORECAST_RESULT.json',{'status':'DERIVED_CONDITIONAL_NOT_TGL_LENS_PREDICTION',
        'canonical_program':pin(p),'alpha_line':text[:m.start()].count('\n')+1,
        'alpha':alpha,'beta_runtime':beta,'fractional_precision_for_median_5sigma':beta/5,
        'median_separation_if_fractional_sigma_0p033':beta/0.033,
        'last_ratio_scope':'pure scalar illustration, NOT TDCOSMO beta inference; H0 uncertainty is not beta uncertainty',
        'rows':rows,'free_common_offset_residual_squared':0,
        'no_observed_test':True,'no_provider_call':True,'gate_changed':False,
        'plan':pin(ROOT/'FORECAST_PLAN.json'),'script':pin(Path(__file__))})
    print(json.dumps({'beta':beta,'precision':beta/5,'N_5percent_no_systematics':next(r['minimum_N'] for r in rows if r['sigma_independent']==0.05 and r['sigma_common']==0)},ensure_ascii=False))
