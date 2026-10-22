"""Distinct coordinator review of the finite-result correction, preserving R1."""
from setup_mission import ROOT,pin,save
import json
d=ROOT/'r2_background'
r=json.loads((d/'OVERFLOW_DELIVERY_R2.json').read_text(encoding='utf-8'))
for x in r['evidence']:
    assert pin(x['path'])['sha256']==x['sha256'],x['path']
old=json.loads((d/'R2_R3_DELIVERY_R1.json').read_text(encoding='utf-8'))
for x in old['pins']:
    assert pin(x['path'])['sha256']==x['sha256'],x['path']
result=json.loads((d/'RESULT_OVERFLOW_R2.json').read_text(encoding='utf-8'))
assert result['exit_code']==0 and result['count']==13 and all(x['passed'] for x in result['checks'])
assert result['solver_calls']==0
save('REVIEW_BACKGROUND_R2.json',{'status':'PASS_WITH_SCOPE','reviewer':'codex-gerente-tgl',
 'builder':'/root/r69_locality_bridge','source':pin(d/'OVERFLOW_DELIVERY_R2.json'),
 'prior_review':pin(ROOT/'REVIEW_BACKGROUND_R1.json'),
 'checks':['All correction pins and all original delivery pins independently reread',
 'Static diff reviewed: finite intermediate/final results now required; overflows are typed BackgroundError',
 '13 focused controls verified from preregistered script and receipts; nominal reuse matches prior outputs',
 'Zero solver calls; seven historical calls remain immutable'],
 'correction_to_prior_review':'R1 review verified nominal propagation only. Subsequent inspection identified finite-input overflow in likelihood/propagation. R2 fixes this defect; no earlier result is erased.',
 'test_executions_by_reviewer':0,'active_candidate':pin(d/'physical_background_adapter_r2.py'),
 'limits':['Same physical/synthetic scope as R1; no full prior integration or observed inference',
 'Floating-point refusal tests do not certify all rounding errors or nonlinear approximation',
 'No full R2/R3 closure or c1 acceptance']})
print('PASS_WITH_SCOPE')
