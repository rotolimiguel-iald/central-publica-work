"""Prospective error targets derived after freeze, independent of injections."""
from pathlib import Path
import json, numpy as np
from scipy.stats import norm
BASE=Path(__file__).resolve().parent

def main():
    spec=json.loads((BASE/'PROSPECTIVE_GEOMETRY.json').read_text('utf-8'))
    bg=json.loads((BASE/'background/BG1.json').read_text('utf-8'))
    with np.load(BASE/'network/network.npz') as net:
        V=net['parameter_covariance_free_cepheid']; ih=int(net['h_index'])
    vh=float(V[ih,ih]);vc=float(V[-1,-1]);hc=float(V[ih,-1]); vb=spec['background_variance_logH'];d=spec['logK']
    targets=[]
    for power in [.5,.9,.95]:
        target_D=5+norm.ppf(power);total_sd=d/target_D;net_var=total_sd**2-vb
        needed_prior_var=hc**2/(vh-net_var)-vc if net_var<vh else None
        targets.append({'target_power':power,'target_D':float(target_D),
            'maximum_sigma_logH_network':float(np.sqrt(net_var)) if net_var>0 else None,
            'sigma_reduction_from_free_cepheid_fraction':float(1-np.sqrt(net_var/vh)) if net_var>0 else None,
            'independent_external_cepheid_bias_constraint_sd_mag':float(np.sqrt(needed_prior_var)) if needed_prior_var is not None and needed_prior_var>=0 else None,
            'condition':'Extra constraint independent of the existing network, with known mean and error model, not a reused host or calibration.'})
    margin=max(0,(d/5)**2-vh-vb)
    out={'status':'DERIVED_PLANNING_NOT_AN_ADMISSION_REQUIREMENT','independent_of_blind_labels':True,
         'cov_h_cepheid_bias':hc,'sigma_bias_internal_mag':float(np.sqrt(vc)),
         'remaining_additive_common_logH_noise_sd_for_median_5sigma':float(np.sqrt(margin)),
         'equivalent_fractional_H_noise':float(np.log(10)*np.sqrt(margin)),
         'equivalent_H_noise_at_TGL_mean':float(bg['K']*bg['H0']*np.log(10)*np.sqrt(margin)),
         'targets':targets,
         'warning':'Targets are prospective design choices, not estimates of missing systematics. No data fit, new constraint, or automatic acceptance.'}
    with (BASE/'DESIGN_MARGINS.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
    print(json.dumps(out,ensure_ascii=False))

if __name__=='__main__':main()
