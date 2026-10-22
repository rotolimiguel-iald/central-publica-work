"""Audit the explicitly selected client release files; print no credential contents."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
FILES = ['android/app/build.gradle', 'android/app/capacitor.build.gradle',
         'android/capacitor.settings.gradle', 'ios/App/App.xcodeproj/project.pbxproj',
         'ios/App/App/PrivacyInfo.xcprivacy', 'ios/App/App/capacitor.config.json',
         'ios/App/App/public/iald.js', 'ios/App/App/public/index.html',
         'ios/App/App/public/operational_deadlines.js', 'ios/App/CapApp-SPM/Package.swift',
         'package-lock.json', 'package.json', 'www/iald.js', 'www/index.html',
         'www/operational_deadlines.js']
PATTERNS = [rb'sk-(?:ant-|proj-)?[A-Za-z0-9_-]{30,}',
            rb'gh[pousr]_[A-Za-z0-9]{30,}', rb'github_pat_[A-Za-z0-9_]{30,}',
            rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']


def main():
    def git(*args):
        return subprocess.check_output(['git', '-C', str(ROOT), *args], stderr=subprocess.DEVNULL)
    if git('diff', '--cached', '--name-only').strip():
        raise ValueError('Index already contains changes')
    changed = set(git('diff', '--name-only').decode().splitlines())
    changed.update(git('ls-files', '--others', '--exclude-standard').decode().splitlines())
    if changed != set(FILES):
        raise ValueError('Working tree differs from reviewed file set')
    rows = []
    for name in FILES:
        raw = (ROOT / name).read_bytes()
        if any(re.search(pattern, raw) for pattern in PATTERNS):
            raise ValueError('Credential pattern found in ' + name)
        rows.append({'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    for name in ('iald.js', 'index.html', 'operational_deadlines.js'):
        if (ROOT / 'www' / name).read_bytes() != (ROOT / 'ios/App/App/public' / name).read_bytes():
            raise ValueError('iOS asset mismatch: ' + name)
    result = {'status': 'CLIENT_FILE_ALLOWLIST_AND_PATTERN_CHECK_PASSED',
              'time_utc': datetime.now(timezone.utc).isoformat(),
              'head': git('rev-parse', 'HEAD').decode().strip(), 'files': rows,
              'scope': '15 reviewed client files; excludes server, env, keys and private corpus',
              'limitations': 'Pattern scan complements diff review; not an exhaustive secret detector.'}
    path = Path(__file__).parent / ('mobile_publish_audit_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
    with path.open('xb') as stream:
        stream.write((json.dumps(result, indent=2) + '\n').encode())
    print(json.dumps({'status': result['status'], 'files': len(rows), 'receipt': str(path), 'head': result['head']}))


if __name__ == '__main__':
    main()
