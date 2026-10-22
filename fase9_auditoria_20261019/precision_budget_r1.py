"""Algebraic precision budget from existing sigma-only design endpoints."""
from setup_audit import ROOT,pin,save
from pathlib import Path
import json,math
spec_path=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json')
if (ROOT/'PRECISION_RESULT_R1.json').exists():raise FileExistsError('result exists')
spec=json.loads(spec_path.read_text(encoding='utf-8'))['spec']
law=spec['lei'];beta=spec['beta']['alpha_read']*math.sqrt(math.e)
z=law['z_star'];om=law['Omega_m'];orad=law['Omega_r'];E=math.sqrt(om*(1+z)**3+orad*(1+z)**4+1-om-orad)
K=E**(2*beta/3)
assert math.isclose(K,law['K_frozen_V1'],abs_tol=1e-12,rel_tol=0)
assert math.isclose(beta,spec['beta']['beta_runtime'],abs_tol=1e-15,rel_tol=0)
rows=[]
for family,key in [('primary','five_masers_decision'),('no_cepheids','without_cepheids_diagnostic')]:
    for bg in ['BG1','BG2','BG3']:
        H=spec['fundos'][bg]['H0'];sb=spec['fundos'][bg]['sigma'];sep=(K-1)*H
        critical_variance=(sep/5)**2-(K*sb)**2
        sides={}
        for side in ['minimum','maximum']:
            e=spec['covariancia'][key][side];sl=e['sigma_comb']
            p=sep/math.sqrt(sl*sl+(K*sb)**2)
            assert math.isclose(p,e['power_only_sigma'][bg],rel_tol=1e-12)
            margin=critical_variance-sl*sl
            sides[side]={'sigma_comb':sl,'nominal_sigma':p,'variance_margin':margin,
              'independent_extra_sigma_budget':math.sqrt(margin) if margin>=0 else None,
              'required_local_sigma_reduction_fraction':max(0,1-math.sqrt(critical_variance)/sl) if critical_variance>0 else None}
        rows.append({'family':family,'background':bg,'background_role':spec['fundos'][bg]['papel'],
          'sigma_comb_for_5':math.sqrt(critical_variance) if critical_variance>0 else None,'endpoints':sides})
save('PRECISION_RESULT_R1.json',{'status':'PASS_ALGEBRAIC_PLANNING_ONLY','plan':pin(ROOT/'PRECISION_PLAN_R1.json'),
 'script':pin(__file__),'source':pin(spec_path),'beta_runtime':beta,'K_runtime':K,'rows':rows,'endpoint_comparisons':12,
 'new_observed_Z':None,'new_observed_verdict':None,'centers_used':'Only preselected background H0; no local reader H0 centers',
 'not_changed':['beta','sources','sigma values','covariance grid','family choice','verdict thresholds','gate']})
print(json.dumps({'K':K,'primary_BG1':rows[0],'no_Cepheid_BG1':rows[3]},ensure_ascii=False))
