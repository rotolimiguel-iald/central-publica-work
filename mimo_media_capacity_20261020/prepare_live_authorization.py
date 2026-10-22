"""Record existing human scope and synthetic fixture pins, not a new consent."""
from pathlib import Path
import hashlib
import json

W = Path(__file__).resolve().parent
OLD = W.parent / 'mimo26_upgrade_20261020'
def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))

value = dict(
    status='EXISTING_HUMAN_SCOPE_RECORDED_NOT_SENT',
    current_request=pin(W/'ORIGINAL.txt'),
    previous_specific_approval=pin(OLD/'LIVE_OPERATOR_APPROVAL.json'),
    previous_known_four_calls=pin(OLD/'live_stage/FOUR_CALLS_COST.json'),
    synthetic_assets=pin(W/'TEST_ASSETS.json'),
    destination=['api.xiaomimimo.com', 'api.typesafe.ai'],
    data='Existing public v394 science, synthetic tone audio and solid-red video; scoped operational test state and attachment custody references to JEV only',
    excluded=['private Atlas', 'credentials', 'personal media', 'other conversations'],
    ceiling_usd=1.0,
    previous_known_estimate_usd=0.0706696812,
    maximum_remaining_estimate_usd=0.9293303188,
    scope_note='Proportional update tests under the current request and previously explicit MiMo v2/JEV v3 approvals. Endpoint must match existing configured vendor; no new credential, terms or destination expansion. Existing app consent is rechecked, not granted by this receipt.',
)
with (W/'LIVE_AUTHORIZATION_SCOPE.json').open('xb') as stream:
    stream.write(json.dumps(value,ensure_ascii=False,indent=2).encode())
print('Existing human scope recorded; no provider request or consent change')
