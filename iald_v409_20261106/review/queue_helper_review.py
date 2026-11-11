"""Independent read-only plan check and isolated authorization guard probes."""
from pathlib import Path
import importlib.util
import json
import hashlib

W = Path(__file__).resolve().parents[1]
Q = W.parent / 'scientific_memory_sync_20261106_v409'
spec = importlib.util.spec_from_file_location('reviewed_promotion', Q/'promote_v409.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
summary, source, destination = module.inputs()
manifest, preparation, plan = module.planned(summary, source, destination)
assert module.read(Q/'promotion/PLAN.json') == plan
assert module.encoded(manifest) == (Q/'MANIFEST_FINAL_CANDIDATE.json').read_bytes()
assert len(plan['files']) == 16 and not destination.exists()
fixture = W/'review'/'approval_guard_fixture'
fixture.mkdir(exist_ok=False)
module.P = fixture
module.AUTH = fixture/'SYNTHETIC_APPROVAL.json'
(fixture/'SESSION_REFERENCE.json').write_bytes(b'{"fixture_only":true}')
order = fixture/'SYNTHETIC_NOT_HUMAN_AUTHORITY.txt'
order.write_bytes(b'Synthetic guard test. Never authorizes production.')
envelope = {'operator_order':module.pin(order), 'f03':{
    'scope':'F0.3_v409_materialize_and_activate_after_final_review',
    'epoch':plan['epoch'], 'generation':plan['generation'],
    'expected_active_sha256':plan['baseline']['sha256'],
    'plan_sha256':module.pin(Q/'promotion/PLAN.json')['sha256'],
    'promotion_cli_sha256':module.pin(Q/'promote_v409.py')['sha256'],
    'reviewed_staging_plan_sha256':module.pin(Q/'PROMOTION_PLAN.json')['sha256'],
    'parent_reference_sha256':module.pin(fixture/'SESSION_REFERENCE.json')['sha256']}}
module.AUTH.write_bytes(module.encoded(envelope))
module.EXPECTED_APPROVAL_SHA256 = module.pin(module.AUTH)['sha256']
module.authorization(plan)
checks = ['derived plan identical', '16 scoped files', 'final manifest bytes identical',
          'synthetic authorization positive']
module.EXPECTED_APPROVAL_SHA256 = '0'*64
try:
    module.authorization(plan)
    raise AssertionError('Changed approval accepted')
except ValueError:
    checks.append('changed approval hash refused')
module.EXPECTED_APPROVAL_SHA256 = module.pin(module.AUTH)['sha256']
bad = {**plan, 'generation':'0'*64}
try:
    module.authorization(bad)
    raise AssertionError('Wrong generation accepted')
except ValueError:
    checks.append('wrong generation refused')
order.write_bytes(b'Changed synthetic source')
try:
    module.authorization(plan)
    raise AssertionError('Changed source accepted')
except ValueError:
    checks.append('changed source refused')
assert not destination.exists()
result = {'status':'PASS', 'reviewer':'codex-app-01a094df',
    'helper_sha256':module.pin(Q/'promote_v409.py')['sha256'],
    'executable_plan_sha256':module.pin(Q/'promotion/PLAN.json')['sha256'],
    'checks':checks, 'production_writes':0,
    'scope':'Static code review, independently reproduced plan and isolated approval guards. Materialization, final paths and activation remain gated.'}
with (W/'review/QUEUE_HELPER_R1.json').open('x',encoding='utf8') as f:
    json.dump(result,f,indent=2)
print(json.dumps(result))
