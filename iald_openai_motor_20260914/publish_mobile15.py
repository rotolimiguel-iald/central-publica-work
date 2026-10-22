"""Publish only the audited mobile application to its authorized private repository."""
import hashlib
import json
from pathlib import Path
import subprocess
from datetime import datetime

WORK = Path(__file__).parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
audit = json.loads((WORK / 'mobile15_audit.json').read_bytes())

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.PIPE)

assert git('branch', '--show-current').decode().strip() == 'codex/mobile-release'
assert git('remote', 'get-url', 'origin').decode().strip() == 'https://github.com/rotolimiguel-iald/iald-app.git'
git('fetch', 'origin', 'codex/mobile-release')
assert int(git('rev-list', '--count', 'HEAD..origin/codex/mobile-release')) == 0, 'Remote advanced; integrate first'
for name, entry in audit['files'].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == entry['sha256'], 'Concurrent edit: ' + name
paths = WORK / 'mobile15_pathspec.bin'
paths.write_bytes(b'\0'.join(name.encode('utf-8') for name in audit['files']) + b'\0')
git('add', '--pathspec-from-file=' + str(paths), '--pathspec-file-nul')
staged = set(filter(None, git('diff', '--cached', '--name-only', '-z').decode().split('\0')))
assert staged and staged <= set(audit['files']), 'Unexpected staged paths'
git('diff', '--cached', '--check')
message = 'Update mobile app to build 15 with usage limits, response reports and beta symbol'
git('commit', '-m', message)
commit = git('rev-parse', 'HEAD').decode().strip()
git('push', 'origin', 'HEAD:codex/mobile-release')
remote = git('ls-remote', 'origin', 'refs/heads/codex/mobile-release').decode().split()[0]
assert remote == commit
report = {'published_at': datetime.now().astimezone().isoformat(), 'status': 'PUSH_VERIFIED',
          'repository': 'https://github.com/rotolimiguel-iald/iald-app',
          'branch': 'codex/mobile-release', 'commit': commit, 'changed_files': len(staged),
          'audit_file_count': len(audit['files']), 'apple_build_status': 'AWAITING_XCODE_CLOUD_VERIFICATION'}
(WORK / 'mobile15_publication.json').write_bytes(json.dumps(report, indent=2).encode())
print(json.dumps(report))
