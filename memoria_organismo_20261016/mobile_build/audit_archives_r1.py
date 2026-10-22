"""Reuse reviewed release-audit functions on public APK/AAB only; no build."""
import ast
from collections import Counter
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
sys.path.insert(0, str(WORK))
from mission_io import pin, save, call

OLD = Path('C:/IALD/Central de Patentes/work/iald_monthly_wallet_20261007/audit_mobile.py')
ATTEMPT = HERE / 'attempts/20261017T003613_760785Z'
BUILD = ATTEMPT / 'RESULT_R1.json'
PLAN = HERE / 'ANDROID28_BUILD_PLAN_R1.json'
ROOT = Path('C:/IALD/projetos_pyhton/IALD/iald-app')
plan = json.loads(PLAN.read_bytes())
build = json.loads(BUILD.read_bytes())
assert build['plan'] == pin(PLAN) and build['build']['exit_code'] == 0
assert build['protected_inputs_unchanged'] and build['init_markers_present']
for item in [build['build']['log'], *[x['log'] for x in build['artifacts']['inspections'].values()]]:
    assert pin(item['path']) == item

# Execute only the named pure/parser/public-archive verification functions;
# do not import or execute the old full audit (fixed paths/version/publishing).
tree = ast.parse(OLD.read_text(encoding='utf-8'))
names = {'sha', 'run', 'name_issues', 'secret_matches', 'signatures', 'protobuf_fields', 'manifest_attributes'}
selected = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name in names]
assert {x.name for x in selected} == names
pattern_node = next(x for x in tree.body if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PATTERNS' for t in x.targets))
namespace = {'hashlib': hashlib, 'subprocess': subprocess, 're': re, 'PurePosixPath': PurePosixPath,
             'PATTERNS': ast.literal_eval(pattern_node.value), 'TOOLS': {k: Path(v) for k, v in plan['tools'].items()}}
exec(compile(ast.Module(body=selected, type_ignores=[]), str(OLD), 'exec'), namespace)
sha = namespace['sha']
paths = {k: Path(build['artifacts'][k]['path']) for k in ('apk', 'aab')}
paths['previous_apk'] = Path(plan['baseline_apk']['path'])
for key in ('apk', 'aab'):
    assert pin(paths[key]) == build['artifacts'][key]
assert pin(paths['previous_apk']) == plan['baseline_apk']
signature = namespace['signatures'](paths)
native_root = ROOT / 'android/app/src/main/assets/public'
native = {}
for p in native_root.rglob('*'):
    if not p.is_file():
        continue
    relative = p.relative_to(native_root).as_posix()
    assert not namespace['name_issues'](relative)
    native[relative] = digest = sha(p.read_bytes())
packages = {}
checks = {}
for key in ('apk', 'aab'):
    path = paths[key]
    prefix = ('base/' if key == 'aab' else '') + 'assets/public/'
    with zipfile.ZipFile(path) as archive:
        names_all = [x.filename for x in archive.infolist() if not x.is_dir()]
        duplicate = [n for n, count in Counter(names_all).items() if count > 1]
        bad_names, findings, public = [], [], {}
        for name in names_all:
            bad = namespace['name_issues'](name)
            if bad:
                bad_names.append({'file': name, 'categories': bad})
                continue  # Never read a member identified as confidential.
            content = archive.read(name)
            if matches := namespace['secret_matches'](content):
                findings.append({'file': name, 'matches': matches})
            if name.startswith(prefix):
                public[name[len(prefix):]] = sha(content)
        registry = ('base/' if key == 'aab' else '') + 'assets/capacitor.plugins.json'
        registry_match = sha(archive.read(registry)) == sha((ROOT / 'android/app/src/main/assets/capacitor.plugins.json').read_bytes())
        item = {'artifact': pin(path), 'bytes': path.stat().st_size, 'entries': len(names_all),
                'duplicate_entries': duplicate, 'crc_error': archive.testzip(), 'public_assets': len(public),
                'public_asset_sha256': public, 'assets_equal_native': public == native,
                'registry_equal_native': registry_match, 'forbidden_names': bad_names, 'secret_patterns': findings}
        if key == 'aab':
            item['manifest'] = namespace['manifest_attributes'](archive.read('base/manifest/AndroidManifest.xml'))
        packages[key] = item
        checks[key + '_zip'] = not duplicate and item['crc_error'] is None
        checks[key + '_assets'] = public == native and registry_match and public.get('iald.js') == plan['accepted_js_sha256']
        checks[key + '_names_patterns'] = not bad_names and not findings
apk_meta = signature['apk_metadata']['attributes']
aab_meta = packages['aab']['manifest']
checks['apk_manifest_28'] = signature['apk_metadata']['exit_code'] == 0 and all(apk_meta.get(k) == v for k, v in {'name': 'br.ia.IALD', 'versionCode': '28', 'versionName': '4.1'}.items())
checks['aab_manifest_28'] = all(aab_meta.get(k) == v for k, v in {'package': 'br.ia.IALD', 'versionCode': '28', 'compiled_versionCode': 28, 'versionName': '4.1'}.items())
checks['apk_signatures'] = signature['apk']['verified'] and signature['previous_apk']['verified']
signed = signature['aab_signature']
checks['aab_signed_all_entries'] = signed['exit_code'] == 0 and signed['jar_verified'] and not signed['unsigned_entries_warning'] and signed['signed_entries'] > 0 and signed['certificate_exit_code'] == 0
checks['same_certificate_as_27'] = signature['all_same_certificate']
checks['artifacts_unchanged'] = signature['artifacts_unchanged_during_verification'] and all(pin(paths[k]) == build['artifacts'][k] for k in ('apk', 'aab'))
checks['protected_source_inputs_unchanged'] = all(pin(x['path']) == x for x in plan['protected_inputs'] + plan['candidate_files'])
server = Path('C:/IALD/projetos_pyhton/IALD/iald_web_server.py')
server_ast = ast.parse(server.read_text(encoding='utf-8'))
public_routes = ast.literal_eval(next(x.value for x in server_ast.body if isinstance(x, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'PUBLIC_ROUTES' for t in x.targets)))
assert 'serve_download' not in public_routes
projection, projected = call('mission_cli.py', {'operation': 'project', 'reference': str(WORK / 'SESSION_REFERENCE.json'),
    'actor': {'kind': 'agent', 'id': 'codex-mission-memory-review'}, 'max_chars': 125000}, 'android28_archive_return')
report = {'schema': 'iald-mobile-archive-review/v1', 'status': 'PASS_ARCHIVES_WITH_SCOPE' if all(checks.values()) else 'FAIL',
          'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'reviewer': 'codex-mission-memory-review',
          'reference': pin(WORK / 'SESSION_REFERENCE.json'), 'revision': projection['receipt']['revision'], 'project': pin(projected),
          'build_result': pin(BUILD), 'build_plan': pin(PLAN), 'audit_script': pin(__file__),
          'reused_source': pin(OLD), 'reused_functions': [{'name': x.name, 'line': x.lineno, 'end_line': x.end_lineno} for x in selected],
          'checks': checks, 'apk': packages['apk'], 'aab': packages['aab'], 'signature_evidence': signature,
          'source_endpoint': {'pin': pin(server), 'authentication_lines': [4188, 4208, 4224], 'route_lines': [4453, 4456, 4462, 4469],
                              'path': '/downloads/IALD-4.1-28.apk', 'public_route': False, 'live_http_checked': False},
          'limits': ['Artifact audit by author of the candidate runner; root independently reviewed runner before execution.',
                     'No rebuild, keystore/private-key access, signing operation, source edit, publication or store/device action.',
                     'Public certificate is self-signed and JAR has no timestamp; warnings retained, signature content and identity verified.',
                     'Six existing secret patterns and filename checks are bounded detection, not proof that every possible secret is absent.',
                     'TestFlight remains pending login; source push does not imply a new iOS build or group availability.',
                     'Archive PASS is technical APK/AAB validation; D/global mission acceptance remains separate.']}
out = HERE / 'ARCHIVE_REVIEW_R1.json'
save(out, report)
print(json.dumps({'review': pin(out), 'status': report['status'], 'checks': len(checks),
                  'failed': [k for k,v in checks.items() if not v], 'aab_manifest': aab_meta,
                  'apk': packages['apk']['artifact'], 'aab': packages['aab']['artifact']}, ensure_ascii=False))
raise SystemExit(0 if all(checks.values()) else 1)
