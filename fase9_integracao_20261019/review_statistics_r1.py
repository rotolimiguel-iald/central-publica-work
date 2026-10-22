"""Independent documentary/algebraic review; does not rerun the builder's tests."""
from setup_mission import ROOT,pin,save
import json,difflib
d=ROOT/'r4_statistics'
r=json.loads((d/'DELIVERY_R4_R2.json').read_text(encoding='utf-8'))
for item in r['evidence']:
    assert pin(item['path'])['sha256']==item['sha256'],item['path']
run=json.loads((d/'RUN_STABLE_ROOTS_R2.json').read_text(encoding='utf-8'))
assert run['exit_code']==0
for item in run['pins']+[run['log'],run['plan']]:
    assert pin(item['path'])['sha256']==item['sha256'],item['path']
delta=''.join(difflib.unified_diff((d/'tail_adapter.py').read_text().splitlines(True),(d/'tail_adapter_r2.py').read_text().splitlines(True)))
save('STATISTICS_DELTA_REVIEW_R1.txt',delta)
save('REVIEW_STATISTICS_R1.json',{
 'status':'PASS_WITH_SCOPE','reviewer':'codex-gerente-tgl','builder':'/root/r68_independent_review',
 'source':pin(d/'DELIVERY_R4_R2.json'),'delta':pin(ROOT/'STATISTICS_DELTA_REVIEW_R1.txt'),
 'checks':['Delivery and execution pins reread; R2 exit 0 and four focal controls verified from receipts',
 'Whitening gives A=I-L0^T S1^-1 L0, b=2L0^T S1^-1 d, c=-d^T S1^-1 d',
 'Equal-covariance Gaussian score law and upper tail derived independently',
 'Scalar positive quadratic takes outside interval; negative quadratic takes inside interval',
 'Scaled q root formula preserves root product and avoids center-radius cancellation',
 'GLS perpendicular residual cancels for common uniform model factors; determinant ratio reduces to variance ratio',
 'Bonferroni applies to valid component p values; finite scenario max does not certify continuous nuisance supremum',
 'General unequal multivariate covariance, unknown fixed background and observed mode are not silently calibrated'],
 'new_test_executions':0,'original_test_claim':'38 controls on R1; four focal controls on R2, not 42 rerun on R2',
 'limits':['Float64 analytic evaluation, no interval certificate for all inputs',
 'Predictive simple Gaussian sampling assumption is explicit, not a proof of uniform frequentist coverage',
 'No observed p or sigma, no full R4 satisfaction, no c1 acceptance']})
print('PASS_WITH_SCOPE')
