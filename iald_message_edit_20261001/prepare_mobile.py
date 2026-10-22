"""Bounded 4.1 release preparation: iOS 27 -> 28, Android 24 -> 25.

Default is read-only verification. --apply changes exactly four mobile files.
The web source must already have been deployed separately by the main agent.
"""
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
ASSETS = ('iald.js', 'iald.css')
IOS = 'ios/App/App.xcodeproj/project.pbxproj'
ANDROID = 'android/app/build.gradle'
TARGETS = ('www/iald.js', 'www/iald.css', IOS, ANDROID)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git_state(repo):
    def git(*args):
        result = subprocess.run(
            ['git', '-c', 'safe.directory=' + repo.as_posix(),
             '--no-optional-locks', '-C', str(repo), *args],
            capture_output=True, text=True, encoding='utf-8', check=True,
            timeout=30)
        return result.stdout.strip()
    return dict(head=git('rev-parse', 'HEAD'),
                branch=git('branch', '--show-current'),
                status=git('status', '--porcelain=v1', '--untracked-files=all'))


def make_plan(work, root, baseline):
    repo = root / 'iald-app'
    state = git_state(repo)
    require(state['head'] == baseline['head'], 'Mobile HEAD changed')
    require(state['branch'] == baseline['branch'], 'Mobile branch changed')
    require(not state['status'], 'Mobile worktree has concurrent changes')
    require(set(baseline['sha256']) == set(TARGETS), 'Unexpected baseline targets')
    old = {}
    for relative in TARGETS:
        path = repo / relative
        require(path.resolve().is_relative_to(repo.resolve()), 'Target escapes mobile repository')
        old[relative] = path.read_bytes()
        require(sha(old[relative]) == baseline['sha256'][relative],
                'Baseline changed: ' + relative)
    sources = {}
    updated = {}
    for name in ASSETS:
        staged = work / 'stage' / name
        deployed = root / 'app' / name
        raw = staged.read_bytes()
        require(bool(raw), 'Empty staged asset: ' + name)
        require(sha(deployed.read_bytes()) == sha(raw),
                'Deploy web from this stage first: ' + name)
        sources[str(staged)] = sha(raw)
        sources[str(deployed)] = sha(raw)
        updated['www/' + name] = raw
    ios = old[IOS]
    android = old[ANDROID]
    require(re.findall(rb'CURRENT_PROJECT_VERSION\s*=\s*([^;]+);', ios) == [b'27', b'27'],
            'Expected exactly two iOS build 27 settings')
    require(re.findall(rb'MARKETING_VERSION\s*=\s*([^;]+);', ios) == [b'4.1', b'4.1'],
            'Expected iOS marketing version 4.1')
    require(re.findall(rb'\bversionCode\s+(\d+)', android) == [b'24'],
            'Expected exactly one Android versionCode 24')
    require(re.findall(rb'\bversionName\s+"([^"]+)"', android) == [b'4.1'],
            'Expected Android versionName 4.1')
    updated[IOS] = re.sub(rb'(CURRENT_PROJECT_VERSION\s*=\s*)27(?=;)', rb'\g<1>28', ios)
    updated[ANDROID] = re.sub(rb'(\bversionCode\s+)24\b', rb'\g<1>25', android)
    return dict(repo=repo, state=state, sources=sources,
                files=[dict(path=repo / rel, relative=rel, before=old[rel], after=updated[rel])
                       for rel in TARGETS])


def verify_sources(plan):
    for path, expected in plan['sources'].items():
        require(sha(Path(path).read_bytes()) == expected,
                'Source changed after preflight: ' + path)


def summary(plan):
    return dict(ios='4.1 (28)', android='4.1 (25)', head=plan['state']['head'],
                source_sha256=plan['sources'], files=[dict(
                    path=str(row['path']), before_sha256=sha(row['before']),
                    after_sha256=sha(row['after'])) for row in plan['files']])


def apply_plan(plan, work):
    # This lock serializes this preparer; byte CAS still checks external writers.
    lock = work / '.prepare_mobile.lock'
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(descriptor)
    changed = []
    backup_dir = None
    try:
        require(git_state(plan['repo']) == plan['state'], 'Mobile Git state changed after preflight')
        verify_sources(plan)
        for row in plan['files']:
            require(row['path'].read_bytes() == row['before'],
                    'CAS failed before writes: ' + row['relative'])
        stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
        backup_dir = work / 'backups' / ('mobile_' + stamp)
        backup_dir.mkdir(parents=True, exist_ok=False)
        require(backup_dir.stat().st_dev == plan['repo'].stat().st_dev,
                'Atomic replacement requires W and mobile repo on the same volume')
        prepared = []
        for row in plan['files']:
            name = row['relative'].replace('/', '__')
            backup = backup_dir / (name + '.before')
            with backup.open('xb') as handle:
                handle.write(row['before'])
                handle.flush()
                os.fsync(handle.fileno())
            require(backup.read_bytes() == row['before'], 'Backup verification failed')
            candidate = backup_dir / (name + '.candidate')
            with candidate.open('xb') as handle:
                handle.write(row['after'])
                handle.flush()
                os.fsync(handle.fileno())
            require(candidate.read_bytes() == row['after'] and candidate.stat().st_size > 0,
                    'Candidate verification failed')
            prepared.append((row, candidate))
        # All backups and candidates exist outside www before the first mutation.
        require(git_state(plan['repo']) == plan['state'], 'Mobile Git state changed during preparation')
        for row, candidate in prepared:
            verify_sources(plan)
            require(row['path'].read_bytes() == row['before'],
                    'CAS failed: ' + row['relative'])
            os.replace(candidate, row['path'])
            changed.append(row['relative'])
            require(row['path'].read_bytes() == row['after'],
                    'Write verification failed: ' + row['relative'])
        verify_sources(plan)
        for row in plan['files']:
            require(row['path'].read_bytes() == row['after'], 'Concurrent change after write')
        receipt = dict(summary(plan), status='prepared', backups=str(backup_dir),
                       changed=changed, at=datetime.now(timezone.utc).isoformat())
        raw = (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        candidate = backup_dir / 'receipt.candidate'
        with candidate.open('xb') as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        require(candidate.read_bytes() == raw, 'Receipt verification failed')
        os.replace(candidate, work / 'mobile_prepared.json')
        return receipt
    except Exception as exc:
        raise RuntimeError('Preparation failed; changed=' + repr(changed)
                           + '; backups=' + str(backup_dir) + '; ' + str(exc)) from exc
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Apply after read-only preflight')
    args = parser.parse_args()
    baseline = json.loads((WORK / 'mobile_baseline.json').read_bytes())
    plan = make_plan(WORK, ROOT, baseline)
    result = apply_plan(plan, WORK) if args.apply else dict(summary(plan), status='check_only')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
