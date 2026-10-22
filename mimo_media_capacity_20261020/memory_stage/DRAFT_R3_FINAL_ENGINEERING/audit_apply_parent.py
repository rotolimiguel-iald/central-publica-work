"""Audit by default. Parent-only reviewed application of eight additive memories."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import uuid

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[1]
PLAN = HERE / 'PLAN_DRAFT.json'
REFERENCE = WORK / 'SESSION_REFERENCE.json'
OWNER = 'codex-app-01a094df'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def no_reparse(path):
    for item in [Path(path), *Path(path).parents]:
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), 'st_file_attributes', 0) & 0x400):
            raise RuntimeError('Reparse point refused')


def verify(entry):
    path = Path(entry['path'])
    no_reparse(path)
    raw = path.read_bytes()
    if digest(raw) != entry['sha256'] or ('bytes' in entry and len(raw) != entry['bytes']):
        raise RuntimeError('Changed pin: ' + str(path))


def save_new(path, value):
    with Path(path).open('xb') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2).encode())
        stream.flush()
        os.fsync(stream.fileno())


def audit(plan):
    if Path(plan['reference']) != REFERENCE or len(plan['surfaces']) != 8 or len({r['path'].casefold() for r in plan['surfaces']}) != 8:
        raise RuntimeError('Wrong mission or surface set')
    verify(plan['apply_candidate'])
    for entry in plan['sources']['sources']:
        verify(entry)
        if Path(entry['path']).name in ('FINAL_RUNTIME_PINS_R8.json', 'SCIENCE_BASELINE.json'):
            for artifact in read(entry['path'])['files']:
                verify(artifact)
    verify(plan['index_policy'])
    for row in plan['surfaces']:
        verify(dict(path=row['path'], sha256=row['before_sha256'], bytes=row['before_bytes']))
        verify(row['append'])
        if Path(row['path']).name == 'MEMORY.md' or 'escritorio' in row['path'].casefold():
            raise RuntimeError('Forbidden surface')
        raw = Path(row['path']).read_bytes()
        suffix = Path(row['append']['path']).read_bytes()
        if plan['marker'].encode() in raw or plan['marker'].encode() not in suffix:
            raise RuntimeError('Marker mismatch or already applied')
        if len(raw + suffix) != row['expected_after_bytes'] or digest(raw + suffix) != row['expected_after_sha256']:
            raise RuntimeError('Expected append hash mismatch')


def owner_preflight(path):
    path = Path(path).resolve(strict=True)
    no_reparse(path)
    if not path.is_relative_to(WORK.resolve()):
        raise RuntimeError('Preflight outside mission')
    check = read(path)
    if not check.get('ok') or not check['result'].get('ready') or check['result']['task_id'] != 'deploy':
        raise RuntimeError('Ready deploy preflight required')
    cp = subprocess.run(['C:/Python314/python.exe', '-B', '-X', 'utf8', 'C:/IALD/MEMORIA_IALD/mission_cli.py'], input=json.dumps({'operation': 'project', 'reference': str(REFERENCE), 'max_chars': 125000}), capture_output=True, text=True, encoding='utf-8')
    current = json.loads(cp.stdout)
    if cp.returncode or not current.get('ok'):
        raise RuntimeError('Fresh mission project failed')
    old, new = check['result'], current['result']
    for key in ('context_id', 'scope', 'revision', 'state_sha256'):
        if old['receipt'][key] != new['receipt'][key]:
            raise RuntimeError('Stale preflight')
    if old['projection_sha256'] != new['projection_sha256']:
        raise RuntimeError('Stale projection')
    task = next(t for t in new['projection']['active'] if t['id'] == 'deploy')
    lease = task['lease']
    if task['status'] != 'working' or lease['owner'] != OWNER or lease['id'] != old['lease_id'] or lease['expires_at'] <= time.time():
        raise RuntimeError('Current parent lease required')
    return current['result']['receipt']


def append_one(row):
    target = Path(row['path'])
    no_reparse(target)
    before = target.read_bytes()
    if digest(before) != row['before_sha256']:
        raise RuntimeError('Immediate CAS refused')
    suffix = Path(row['append']['path']).read_bytes()
    if digest(suffix) != row['append']['sha256']:
        raise RuntimeError('Append changed')
    after = before + suffix
    if digest(after) != row['expected_after_sha256'] or len(after) != row['expected_after_bytes'] or len(after) <= len(before):
        raise RuntimeError('Unexpected result')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    backup = target.with_name(target.name + '.bak_' + stamp)
    with backup.open('xb') as stream:
        stream.write(before)
        stream.flush()
        os.fsync(stream.fileno())
    if backup.read_bytes() != before:
        raise RuntimeError('Immediate byte backup failed')
    temporary = target.with_name(target.name + '.tmp_' + uuid.uuid4().hex)
    with temporary.open('xb') as stream:
        stream.write(after)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != after or target.read_bytes() != before:
        raise RuntimeError('Temporary verify or final CAS failed; backup retained')
    no_reparse(target)
    os.replace(temporary, target)
    if target.read_bytes() != after:
        # Restore the exact immediate byte backup on failed post-write verification.
        recovery = target.with_name(target.name + '.restore_' + uuid.uuid4().hex)
        with recovery.open('xb') as stream:
            stream.write(backup.read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(recovery, target)
        raise RuntimeError('Write verification failed; original restored from backup')
    return dict(path=str(target), backup=str(backup), before_sha256=digest(before), after_sha256=digest(after), bytes=len(after))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    for option in ('review', 'go', 'preflight'):
        parser.add_argument('--' + option, type=Path)
    args = parser.parse_args()
    plan = read(PLAN)
    audit(plan)
    plan_sha = digest(PLAN.read_bytes())
    if not args.apply:
        print(json.dumps({'status': 'PASS_AUDIT_ONLY', 'plan_sha256': plan_sha, 'surfaces': 8, 'writes': 0}))
        return
    if not all((args.review, args.go, args.preflight)):
        raise RuntimeError('Independent memory review + parent GO + fresh parent preflight required')
    for path in (args.review, args.go):
        no_reparse(path)
        if not path.resolve().is_relative_to(WORK.resolve()):
            raise RuntimeError('Authorization outside mission')
    review, go = read(args.review), read(args.go)
    if review.get('status') != 'PASS' or review.get('scope') != 'MEMORY_8_SURFACES' or review.get('actor') != plan['reviewer_actor'] or review.get('actor') == plan['actor']['id'] or review.get('plan_sha256') != plan_sha or review.get('candidate_sha256') != plan['apply_candidate']['sha256']:
        raise RuntimeError('Distinct exact memory review required; publisher review is insufficient')
    if go.get('go') is not True or go.get('actor') != OWNER or go.get('reference') != str(REFERENCE) or go.get('plan_sha256') != plan_sha or go.get('review_sha256') != digest(args.review.read_bytes()) or go.get('candidate_sha256') != plan['apply_candidate']['sha256']:
        raise RuntimeError('Parent GO not bound to exact review/plan/script')
    fresh = owner_preflight(args.preflight)
    audit(plan)
    save_new(HERE / 'APPLY_INTENT.json', {'plan_sha256': plan_sha, 'review': str(args.review), 'go': str(args.go), 'preflight': fresh, 'no_repeat': True})
    applied = []
    try:
        for row in plan['surfaces']:
            applied.append(append_one(row))
        verify(plan['index_policy'])
    except Exception as error:
        save_new(HERE / 'APPLY_PARTIAL_FAILURE.json', {'status': 'FAILED_NO_AUTOMATIC_RETRY', 'applied': applied, 'error': str(error), 'backups_retained': True})
        raise
    save_new(HERE / 'APPLIED.json', {'status': 'APPLIED_8_ADDITIVE_SURFACES', 'plan_sha256': plan_sha, 'applied': applied, 'backups_retained': True, 'index_unchanged': True, 'board_or_map_moved': False})


if __name__ == '__main__':
    main()
