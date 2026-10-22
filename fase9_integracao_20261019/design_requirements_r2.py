"""Conditional design requirements, no local observed centers or composite.

Reuses the pinned minimax design. This does not change the adopted primary or
estimate physical bias/correlation. Gaussian, fixed K, correct total errors and
equal null/alternative error variance are explicit assumptions for power only.
"""
from pathlib import Path
from statistics import NormalDist
import hashlib,json,math
HERE=Path(__file__).resolve().parent
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(name,data):
    with (HERE/name).open('xb') as f:f.write(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False).encode())
def main():
    for name in ['DESIGN_PLAN_R2.json','DESIGN_REQUIREMENTS_R2.json']:
        if (HERE/name).exists():raise FileExistsError(name)
    source=HERE/'r1_envelope/RESULT_R1.json'
    save('DESIGN_PLAN_R2.json',{'source':pin(source),'script':pin(Path(__file__)),
         'threshold_upper_z':5,'reference_detection_probability':.90,
         'mode':'NO_LOCAL_CENTERS; design sigmas and preselected background only',
         'assumptions':['fixed cosmology and K','Gaussian unbiased errors','equal null/alternative covariance for power',
                        'minimax single-reader design is a candidate, not adopted primary','no multiplicity adjustment in this conditional calculation']})
    d=json.loads(source.read_text(encoding='utf-8'))['nominal_design']
    r=next(x for x in d['rows'] if x['family']=='P_primaria' and x['test']=='LCDM_NULL_CONTRAST')
    delta=r['nominal_mean_separation'];s=r['local_minimax_sigma'];b=r['background_sigma']
    z=5.;z90=z+NormalDist().inv_cdf(.9);se=math.hypot(s,b)
    result={'status':'DERIVED_CONDITIONAL_DESIGN_ONLY','source':pin(source),'plan':pin(HERE/'DESIGN_PLAN_R2.json'),
        'delta_design':delta,'local_sigma':s,'background_sigma':b,'K':d['K_runtime'],
        'independent_background_nominal_z':delta/se,
        'power_at_one_sided_5sigma_independent_background':.5*math.erfc((z-delta/se)/math.sqrt(2)),
        'rho_min_to_retain_nominal_z_at_least_5':(s*s+b*b-(delta/z)**2)/(2*s*b),
        'adversarial_mean_bias_budget_for_nominal_z5_if_background_independent':delta-z*se,
        'local_sigma_max_for_nominal_z5_all_correlations':delta/z-b,
        'local_sigma_max_for_90pct_detection_at_z5_independent_background':math.sqrt((delta/z90)**2-b*b),
        'local_sigma_max_for_90pct_detection_at_z5_all_correlations':delta/z90-b,
        'rho_sign':'positive covariance reduces variance of the local minus background contrast',
        'interpretation':'rho lower bound and bias budget are required design conditions, not measured facts; 90pct thresholds assume equal sampling variance and Gaussian tails',
        'observed_z':None,'required_existing_acts_waived':False,'primary_changed':False}
    save('DESIGN_REQUIREMENTS_R2.json',result);print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
