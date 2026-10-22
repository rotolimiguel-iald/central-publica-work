"""Independent coordinator review of the agent's physical adapter and receipts."""
from setup_mission import ROOT,pin,save
import json,math
d=ROOT/'r2_background'
receipt=json.loads((d/'R2_R3_DELIVERY_R1.json').read_text(encoding='utf-8'))
for item in receipt['pins']:
    assert pin(item['path'])['sha256']==item['sha256'],item['path']
r=json.loads((d/'RESULT_SYNTHETIC_R1.json').read_text(encoding='utf-8'))
assert r['passed'] and all(c['passed'] for c in r['checks'])
assert r['solver_calls_attempted']==7 and r['solver_calls_returned']==7 and r['exit_code']==0
plan=json.loads((d/'PLAN_SYNTHETIC_R1.json').read_text(encoding='utf-8'))
J=r['jacobian_rows']; C=plan['synthetic_covariance_theta']; out=r['propagation']['covariance_prediction']
recomputed=[[sum(J[i][a]*C[a][b]*J[j][b] for a in range(3) for b in range(3)) for j in range(len(J))] for i in range(len(J))]
residual=max(abs(recomputed[i][j]-out[i][j]) for i in range(len(J)) for j in range(len(J)))
assert residual<1e-12
assert out[-1][-2]>0 and math.isclose(out[-1][-2],out[-1][-1],rel_tol=1e-12)
assert r['conditional_without_covariance']['unconditional'] is False
assert r['decision_eligible'] is False and r['lnB'] is None and r['statistical_sigma'] is None
save('REVIEW_BACKGROUND_R1.json',{'status':'PASS_WITH_SCOPE','reviewer':'codex-gerente-tgl',
 'builder':'/root/r69_locality_bridge','checks':['28 artifact pins reread','7 solver receipts and16 checks inspected',
 'J Ctheta J^T independently recomputed by explicit scalar sums','Shared local calibration covariance retained',
 'Code review: H5 frees BAO rd only, normalized likelihood, no observed input, no scalar K substitution'],
 'max_propagation_residual':residual,'source':pin(d/'R2_R3_DELIVERY_R1.json'),
 'reviewer_correction':'First coordinator attempt selected result.synthetic_covariance (measurement covariance), not plan.synthetic_covariance_theta. Its assertion failed. Corrected source selection; no supplier output changed or recomputed.',
 'theta_covariance_source':pin(d/'PLAN_SYNTHETIC_R1.json'),
 'evidence':[pin(d/n) for n in ['physical_background_adapter.py','RESULT_SYNTHETIC_R1.json','SOURCE_RANGE_AND_HYGIENE_R1.json']],
 'limits':['No independent rerun of CAMB','Linear propagation, synthetic covariance; no admitted posterior or global error bound',
 'Physical engine connection qualified only with synthetic inputs; no Bayes evidence, full integration or observed significance',
 'Not c1 acceptance and not full R2/R3 goal completion']})
print('PASS_WITH_SCOPE',residual)
