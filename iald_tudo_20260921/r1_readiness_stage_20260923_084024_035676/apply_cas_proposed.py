"""Proposed only. Dry-run default. Explicit --target and --apply for reviewed use.

Hash comparison and atomic replacement are not an interprocess editor lock.
Coordinate with other editors before applying. Never restarts the server.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def apply(target, execute=False):
    manifest = json.loads((HERE/'patch_manifest.json').read_bytes())
    candidate = (HERE/'iald_web_server.py').read_bytes()
    if digest(candidate) != manifest['staged_sha256']:
        raise ValueError('staged_hash_mismatch')
    target = Path(target).resolve(strict=True)
    original = target.read_bytes()
    if digest(original) != manifest['base_sha256']:
        raise ValueError('base_changed_refuse_without_writes')
    result = {'status':'DRY_RUN', 'base_sha256':digest(original),
              'staged_sha256':digest(candidate), 'target':str(target)}
    if not execute:
        return result
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    backup = target.with_name(target.name+'.bak_'+stamp)
    with backup.open('xb') as stream:
        stream.write(original)
        stream.flush()
        os.fsync(stream.fileno())
    if backup.read_bytes() != original:
        raise ValueError('backup_verification_failed')
    temporary = target.with_name(target.name+'.tmp_'+stamp)
    with temporary.open('xb') as stream:
        stream.write(candidate)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != candidate:
        raise ValueError('temporary_verification_failed')
    if target.read_bytes() != original:
        raise ValueError('concurrent_change_refused_backup_and_temp_retained')
    os.replace(temporary, target)
    if target.read_bytes() != candidate:
        raise ValueError('post_replace_verification_failed_manual_review_required')
    result.update(status='APPLIED', backup=str(backup))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(apply(args.target, args.apply), ensure_ascii=False))
    except (ValueError, OSError):
        print(json.dumps({'status':'REFUSED', 'reason':'Hash, filesystem or concurrency check failed; inspect locally. No automatic retry.'}))
        raise SystemExit(2)
