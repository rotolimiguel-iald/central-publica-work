"""Freeze a reviewable deployment manifest; never writes to the live application."""
from pathlib import Path
from datetime import datetime
import ast
import hashlib
import json

work = Path(__file__).resolve().parent
root = Path(r'C:\IALD\projetos_pyhton\IALD')
stage = work / 'claude_routes_stage_20260922_154903_859968'
package = work / 'haiku_package_20260922_141841_074636'
receipt = json.loads((stage / 'receipt.json').read_bytes())
modules = ('claude_profiles', 'claude_request_guard', 'claude_native_counter',
           'claude_account_policy', 'claude_profile_pipeline', 'claude_memory_package',
           'claude_guarded_transport', 'claude_server_selection', 'claude_haiku_messages',
           'claude_route_bridge', 'claude_native_account', 'claude_context_snapshot')
rows = []

def add(source, relative, expected=None):
    raw = source.read_bytes()
    if source.suffix == '.py': ast.parse(raw.decode('utf8'))
    target = root / relative
    before = target.read_bytes() if target.exists() else None
    old = hashlib.sha256(before).hexdigest() if before is not None else None
    if expected is not None: assert old == expected, 'Concurrent source change: ' + relative
    rows.append({'source': str(source), 'relative': relative, 'old_sha256': old,
                 'new_sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})

for module in modules: add(work / (module + '.py'), module + '.py')
add(package / 'prefix.md', '.iald_runtime/haiku/prefix.md')
add(package / 'manifest.json', '.iald_runtime/haiku/manifest.json')
add(stage / 'iald.js', 'app/iald.js', receipt['original_js_sha256'])
add(stage / 'iald_web_server.py', 'iald_web_server.py', receipt['original_server_sha256'])
manifest = {'status': 'PREPARED_NOT_INSTALLED', 'feature_activation': False,
            'public_spend_activation': False, 'paid_test': False,
            'stage': str(stage), 'files': rows,
            'requirements_before_apply': ['independent integration review approved',
                'IALD_HAIKU_ATIVO absent or zero', 'original hashes still match']}
target = work / ('haiku_install_plan_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
with target.open('x', encoding='utf8') as handle:
    json.dump(manifest, handle, indent=2)
print(json.dumps({'plan': str(target), 'files': len(rows), 'activation': False}))
