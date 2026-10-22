"""Prepare exactly the approved JS revision, preserving parallel edits."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
from goal16_records import ROOT, WORK, record, write_new

APP = ROOT / 'iald-app'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
memory_before = (ROOT / 'CLAUDE.md').read_bytes()
record('moderations_permission_20260915.json', {
    'task': 'T3 — permissões da chave existente', 'status': '[REAL]',
    'key_name': 'IALD Servidor', 'tracking_id': 'key_sQU85csurXocf7JL',
    'before': {'Chat completions (/v1/chat/completions)': 'Request',
               'Moderations (/v1/moderations)': 'None'},
    'after': {'Chat completions (/v1/chat/completions)': 'Request',
              'Moderations (/v1/moderations)': 'Request'},
    'verification': 'Saved and reopened editor; both permissions persisted; all other entries None.',
    'expiry': '2026-10-14', 'new_project_key_created': False,
    'server_restarted': False, 'env_modified_by_this_task': False,
}, '[REAL] Chave IALD Servidor existente editada no projeto IALD: Moderations passou de None '
   'para Request; Chat Completions Request preservado. Editor reaberto confirmou duas permissões. '
   'Demais permissões None, validade 14/10/2026 mantida. Nenhuma nova chave de projeto, alteração '
   'de IALD_MODERACAO ou reinício.', memory_before)

js_paths = [APP / p for p in ['www/iald.js', 'ios/App/App/public/iald.js',
                             'android/app/src/main/assets/public/iald.js']]
js_before = {p: p.read_bytes() for p in js_paths}
assert all(hashlib.sha256(v).hexdigest().startswith('edc227affb0550ec') for v in js_before.values())
replacements = [
    ('android/app/build.gradle', b'versionCode 15', b'versionCode 16', 1),
    ('ios/App/App.xcodeproj/project.pbxproj', b'CURRENT_PROJECT_VERSION = 15;',
     b'CURRENT_PROJECT_VERSION = 16;', 2),
]
changes = {}
for name, old, new, count in replacements:
    path = APP / name
    before = path.read_bytes()
    assert before.count(old) == count, 'Unexpected version: ' + name
    changes[path] = (before, before.replace(old, new))
ignore = APP / '.gitignore'
before = ignore.read_bytes()
assert b'ORDEM*.md' not in before
changes[ignore] = (before, before + b'\r\n# Internal operator orders\r\nORDEM*.md\r\n')

for path, (before, after) in changes.items():
    assert path.read_bytes() == before, 'Parallel change: ' + str(path)
    assert all(p.read_bytes() == v for p, v in js_before.items()), 'Approved JS changed'
    relative = path.relative_to(APP)
    backup = (APP / ('_backups_' + stamp) / relative
              if relative.parts[0] in ('android', 'ios', 'www')
              else path.with_name(path.name + '.bak_' + stamp))
    backup.parent.mkdir(parents=True, exist_ok=True)
    write_new(backup, before)
    assert backup.read_bytes() == before
    temporary = path.with_name(path.name + '.tmp_release')
    write_new(temporary, after)
    assert path.read_bytes() == before
    temporary.replace(path)
    assert path.read_bytes() == after

for kind in ['audit', 'publish']:
    source = WORK / (kind + '_mobile15.py')
    data = source.read_bytes().replace(b'mobile15', b'mobile16')
    data = data.replace(b'build 15 with usage limits, response reports and beta symbol',
                        b'build 16 with operator credit alerts and security fixes')
    write_new(WORK / (kind + '_mobile16.py'), data)
write_new(WORK / 'mobile16_preparation.json', json.dumps({
    'prepared_at': datetime.now().astimezone().isoformat(),
    'js_sha256': {str(p): hashlib.sha256(v).hexdigest() for p, v in js_before.items()},
    'changed': {str(p): {'before': hashlib.sha256(a).hexdigest(),
                         'after': hashlib.sha256(b).hexdigest()}
                for p, (a, b) in changes.items()},
    'backup_stamp': stamp,
}, indent=2).encode())
print('BUILD_16_PREPARED; T3_RECEIPT_SAVED')
