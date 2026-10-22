"""APK30 additive publisher. Preview by default; explicit reviewed GO required."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
WORK = HERE.parents[2]
PLAN = HERE / 'APK30_ADDITIVE_PUBLICATION_PLAN_FINAL_R3.json'
EXPECTED = Path('C:/IALD/projetos_pyhton/IALD/downloads/IALD-4.1-30.apk')
REFERENCE = WORK / 'SESSION_REFERENCE.json'
OWNER = 'codex-app-01a094df'


def pin(path):
    path = Path(path)
    digest = hashlib.sha256()
    size = 0
    with path.open('rb') as stream:
        while block := stream.read(1048576):
            digest.update(block)
            size += len(block)
    return dict(path=str(path), sha256=digest.hexdigest(), bytes=size)


def no_reparse(path):
    for item in [Path(path), *Path(path).parents]:
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), 'st_file_attributes', 0) & 0x400):
            raise RuntimeError('Reparse point refused')


def verify(entry):
    no_reparse(entry['path'])
    actual = pin(entry['path'])
    if any(actual[key] != entry[key] for key in ('path', 'sha256')) or ('bytes' in entry and actual['bytes'] != entry['bytes']):
        raise RuntimeError('Pinned file changed: ' + entry['path'])


def read(path):
    return json.loads(Path(path).read_bytes())


def exclusive_json(path, value):
    with Path(path).open('xb') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8'))
        stream.flush()
        os.fsync(stream.fileno())


def verify_plan(plan):
    if Path(plan['destination']) != EXPECTED or Path(plan['reference']) != REFERENCE:
        raise RuntimeError('Wrong target or mission')
    no_reparse(EXPECTED)
    if EXPECTED.exists():
        raise RuntimeError('Target already exists; no overwrite, including identical bytes')
    for entry in [plan['source'], plan['result'], plan['archive_audit'], plan['candidate'],
                  plan['endpoint_source']['pin'], *plan['source_pins'], *plan['preserve_existing_apks']]:
        verify(entry)
    paths = sorted(str(p) for p in EXPECTED.parent.glob('*.apk'))
    if paths != sorted(p['path'] for p in plan['preserve_existing_apks']):
        raise RuntimeError('APK set changed; refresh and review plan')
    audit, result = read(plan['archive_audit']['path']), read(plan['result']['path'])
    if audit['status'] != 'PASS' or not audit['checks'] or not all(v is True for v in audit['checks'].values()):
        raise RuntimeError('Archive audit not PASS')
    verify(audit['build_result'])
    if Path(audit['build_result']['path']) != Path(plan['result']['path']):
        raise RuntimeError('Audit/result mismatch')
    if result['build']['exit_code'] != 0 or not result['protected_inputs_unchanged']:
        raise RuntimeError('Build result refused')
    evidence = audit['signature_evidence']
    if not evidence['apk']['verified'] or not evidence['previous_apk']['verified']:
        raise RuntimeError('Signature not verified')
    if evidence['apk']['certificate_sha256'] != evidence['previous_apk']['certificate_sha256'] or evidence['apk']['certificate_sha256'] != plan['certificate_sha256']:
        raise RuntimeError('Certificate continuity refused')
    if evidence['artifact_sha256']['apk'] != plan['source']['sha256'] or result['artifacts']['apk']['sha256'] != plan['source']['sha256'] or Path(result['artifacts']['apk']['path']) != Path(plan['source']['path']):
        raise RuntimeError('APK/result/audit mismatch')


def authorize(review, go, plan_pin, plan):
    if review.get('technical_go') is not True or review.get('actor') != plan['reviewer_actor'] or review.get('actor') == plan['preparer']:
        raise RuntimeError('Distinct reviewer technical GO required')
    if review.get('plan', {}).get('sha256') != plan_pin['sha256'] or Path(review['plan']['path']) != PLAN:
        raise RuntimeError('Review not bound to exact plan')
    if review.get('candidate', {}).get('sha256') != plan['candidate']['sha256']:
        raise RuntimeError('Review not bound to executable')
    checks = review.get('four_checks', {})
    if set(checks) != set(plan['review']['checks_required']) or any(v != 'PASS' for v in checks.values()):
        raise RuntimeError('Four explicit publisher PASS checks required')
    if go.get('go') is not True or go.get('actor') != OWNER or go.get('plan_sha256') != plan_pin['sha256'] or go.get('review_sha256') != review['_actual_sha256'] or go.get('candidate_sha256') != plan['candidate']['sha256'] or go.get('reference') != str(REFERENCE):
        raise RuntimeError('Owner GO not bound to plan/review/candidate/mission')


def fresh_preflight(path):
    path = Path(path).resolve(strict=True)
    if not path.is_relative_to(WORK.resolve()):
        raise RuntimeError('Preflight outside mission')
    no_reparse(path)
    check = read(path)
    if not check.get('ok') or not check['result'].get('ready') or check['result']['task_id'] != 'deploy':
        raise RuntimeError('Ready deploy preflight required')
    payload = {'operation': 'project', 'reference': str(REFERENCE), 'max_chars': 125000}
    cp = subprocess.run(['C:/Python314/python.exe', '-B', '-X', 'utf8', 'C:/IALD/MEMORIA_IALD/mission_cli.py'], input=json.dumps(payload), capture_output=True, text=True, encoding='utf-8', check=False)
    state = json.loads(cp.stdout)
    if cp.returncode or not state.get('ok'):
        raise RuntimeError('Mission project refused')
    old, new = check['result'], state['result']
    for key in ('context_id', 'scope', 'revision', 'state_sha256'):
        if old['receipt'][key] != new['receipt'][key]:
            raise RuntimeError('Stale or different-context preflight')
    if old['projection_sha256'] != new['projection_sha256']:
        raise RuntimeError('Stale projection')
    task = next(t for t in new['projection']['active'] if t['id'] == 'deploy')
    lease = task['lease']
    if task['status'] != 'working' or lease['id'] != old['lease_id'] or lease['owner'] != OWNER or lease['expires_at'] <= time.time():
        raise RuntimeError('Current owner deploy lease required')
    return dict(preflight=pin(path), project=state)


def create_additive(source, destination, receipt_dir, expected_sha256):
    """Shared with temporary-directory fixtures; never replaces an existing target."""
    if os.name != 'nt':
        raise RuntimeError('Windows nonreplacement rename required')
    source, destination, receipt_dir = map(Path, (source, destination, receipt_dir))
    for path in (source, destination, receipt_dir):
        no_reparse(path)
    if destination.exists():
        raise RuntimeError('Existing target refused')
    if source.drive.casefold() != destination.drive.casefold() or receipt_dir.drive.casefold() != destination.drive.casefold():
        raise RuntimeError('Same volume required')
    temporary = receipt_dir / 'APK30.tmp'
    with source.open('rb') as src, temporary.open('xb') as out:
        while block := src.read(1048576):
            out.write(block)
        out.flush()
        os.fsync(out.fileno())
    if pin(temporary)['sha256'] != expected_sha256:
        raise RuntimeError('Staged APK mismatch')
    no_reparse(destination)
    os.rename(temporary, destination)  # Windows raises if a competing name exists.
    if pin(destination)['sha256'] != expected_sha256:
        raise RuntimeError('Published APK mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publish', action='store_true')
    for option in ('review', 'go', 'preflight'):
        parser.add_argument('--' + option, type=Path)
    args = parser.parse_args()
    plan = read(PLAN)
    verify_plan(plan)
    if not args.publish:
        print(json.dumps({'mode': 'PREVIEW_ONLY', 'plan': pin(PLAN), 'apk_copied': False}))
        return
    if not all((args.review, args.go, args.preflight)):
        raise RuntimeError('Review, explicit GO and fresh preflight required')
    for path in (args.review, args.go):
        no_reparse(path)
        if not path.resolve().is_relative_to(WORK.resolve()):
            raise RuntimeError('Authorization must be within own mission')
    review, go = read(args.review), read(args.go)
    review['_actual_sha256'] = pin(args.review)['sha256']
    authorize(review, go, pin(PLAN), plan)
    state = fresh_preflight(args.preflight)
    verify_plan(plan)
    exclusive_json(HERE / 'PUBLICATION_INTENT.json', {'plan': pin(PLAN), 'review': pin(args.review), 'go': pin(args.go), 'state': state, 'no_repeat': True})
    create_additive(plan['source']['path'], EXPECTED, HERE, plan['source']['sha256'])
    for entry in plan['preserve_existing_apks']:
        verify(entry)
    exclusive_json(HERE / 'PUBLICATION_RESULT.json', {'status': 'CREATED_NEW_APK30_HTTP_PENDING', 'destination': pin(EXPECTED), 'plan': pin(PLAN), 'existing_apks_preserved': len(plan['preserve_existing_apks']), 'http_verified': False, 'device_installation_verified': False})


if __name__ == '__main__':
    main()
