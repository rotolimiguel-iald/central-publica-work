"""Prepared only. Default/check are read-only. Applying requires separate approval.

Reuses the previous delivery's byte backups + append + verified atomic replace.
Eight independent files are not a multi-file transaction: failures stop visibly,
preserving backups and a receipt of every already completed replacement.
"""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parent


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def publish(path, raw):
    temporary = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != raw:
        raise RuntimeError('Temporary bytes did not verify')
    os.replace(temporary, path)
    if path.read_bytes() != raw:
        raise RuntimeError('Published bytes did not verify')


def preflight(plan):
    if digest(Path(__file__).read_bytes()) != plan['script_sha256']:
        raise RuntimeError('Script pin changed')
    prior = Path(plan['previous_delivery']['path']).read_bytes()
    if digest(prior) != plan['previous_delivery']['sha256']:
        raise RuntimeError('Previous surface receipt changed')
    expected = [Path(item['path']).resolve() for item in json.loads(prior)['surfaces']]
    targets = [Path(item['path']).resolve() for item in plan['surfaces']]
    if len(set(targets)) != 8 or targets != expected:
        raise RuntimeError('Exact previous eight surfaces required')
    for evidence in plan['evidence']:
        if digest(Path(evidence['path']).read_bytes()) != evidence['sha256']:
            raise RuntimeError('Evidence changed; rebuild and review plan')
    addition = (ROOT / plan['append_file']).read_bytes()
    if digest(addition) != plan['append_sha256'] or not addition:
        raise RuntimeError('Append content changed')
    marker = plan['marker'].encode('ascii')
    if addition.count(marker) != 2:
        raise RuntimeError('Append start/end marker required')
    before = []
    for item, path in zip(plan['surfaces'], targets):
        raw = path.read_bytes()
        if digest(raw) != item['before_sha256'] or len(raw) != item['before_bytes']:
            raise RuntimeError('Surface changed; no writes; rebuild baseline')
        if marker in raw:
            raise RuntimeError('Marker already present; reconcile without duplicate append')
        after = raw + addition
        if len(after) <= len(raw) or not after.startswith(raw):
            raise RuntimeError('Append invariant failed')
        before.append((path, raw, after))
    return before


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--apply', action='store_true', help='Only after separate authorized review; never run during preparation')
    parser.add_argument('--approved-plan-sha256')
    args = parser.parse_args()
    raw_plan = (ROOT / 'PLAN.json').read_bytes()
    plan = json.loads(raw_plan)
    rows = preflight(plan)
    if not args.apply:
        print(json.dumps(dict(status='PLAN_VALID_NOT_APPLIED', surfaces=len(rows), memory_writes=0)))
        return
    if args.check or args.approved_plan_sha256 != digest(raw_plan):
        raise RuntimeError('Separate approval must identify exact plan SHA256')
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    receipt_path = ROOT / ('APPLIED_' + stamp + '.json')
    receipt = dict(status='IN_PROGRESS', plan_sha256=digest(raw_plan), surfaces=[])
    try:
        # All byte backups exist and verify before the first memory replace.
        for path, before, after in rows:
            backup = path.with_name(path.name + '.bak_' + stamp)
            with backup.open('xb') as stream:
                stream.write(before)
                stream.flush()
                os.fsync(stream.fileno())
            if backup.read_bytes() != before:
                raise RuntimeError('Immediate byte backup mismatch')
            receipt['surfaces'].append(dict(path=str(path), backup=str(backup), status='BACKED_UP',
                                            before_sha256=digest(before), after_sha256=digest(after)))
        if any(path.read_bytes() != before for path, before, after in rows):
            raise RuntimeError('Concurrent memory change before append')
        for item, (path, before, after) in zip(receipt['surfaces'], rows):
            if path.read_bytes() != before:
                raise RuntimeError('Concurrent memory change; stop without overwriting')
            publish(path, after)
            if path.stat().st_size != len(after) or not path.read_bytes().startswith(before):
                # Restore the exact saved bytes if our append was shortened.
                publish(path, Path(item['backup']).read_bytes())
                raise RuntimeError('Append size/prefix invalid; restored immediate backup')
            item['status'] = 'APPENDED_VERIFIED'
            publish(receipt_path, (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        receipt['status'] = 'APPLIED_VERIFIED'
    except BaseException:
        receipt['status'] = 'FAILED_VISIBLE_POSSIBLY_PARTIAL_RECONCILE_RECEIPT'
        raise
    finally:
        publish(receipt_path, (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


if __name__ == '__main__':
    main()
