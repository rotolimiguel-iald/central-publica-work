"""Hash-pinned installation with immediate byte backups and conflict-safe rollback.

This module has no deployment side effects at import. The production caller must
hold the existing queue drain lock and a verified idle web maintenance window.
The caller's guard is checked before each write, never inferred from a boolean.
"""
from datetime import datetime, timezone
from pathlib import Path
import ast
import hashlib
import json
import os
import stat
import uuid


class DeploymentError(RuntimeError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_bytes())


def write_new(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    try:
        with temp.open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if temp.read_bytes() != raw:
            raise DeploymentError('Temporary bytes differ')
        # Publishing an immutable receipt must never overwrite an existing file.
        if os.name == 'nt':
            os.rename(temp, path)  # Windows rename fails if destination exists.
        else:
            os.link(temp, path)
    finally:
        if temp.exists():
            temp.unlink()
    if path.read_bytes() != raw:
        raise DeploymentError('Published bytes differ')


def receipt(path, data):
    write_new(path, (json.dumps(data, ensure_ascii=False, indent=2,
                               allow_nan=False) + '\n').encode('utf-8'))


def no_alias(path):
    """Reject symlinks/junctions before resolving an installation path."""
    path = Path(path).absolute()
    for part in (path, *path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or (
            getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)
        ):
            raise DeploymentError('Aliased installation path refused')
    return path.resolve()


def current_bytes(path):
    return path.read_bytes() if path.is_file() else None


def atomic_replace(path, raw):
    path = Path(path)
    temp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    try:
        with temp.open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if temp.read_bytes() != raw:
            raise DeploymentError('Temporary replacement differs')
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()
    if path.read_bytes() != raw:
        raise DeploymentError('Replacement differs')


def prepare(plan_path, review_path, *, work_root, allowed_destinations):
    """Validate all inputs before any destination is changed."""
    work_root = no_alias(work_root)
    plan_path, review_path = no_alias(plan_path), no_alias(review_path)
    if not plan_path.is_relative_to(work_root) or not review_path.is_relative_to(work_root):
        raise DeploymentError('Plan/review must be in this delivery workspace')
    plan_raw = plan_path.read_bytes()
    plan, review = json.loads(plan_raw), read_json(review_path)
    if review.get('status') != 'PASS' or review.get('plan_sha256') != sha(plan_raw):
        raise DeploymentError('Independent review does not cover this plan')
    if review.get('author') == plan.get('author') or not review.get('author'):
        raise DeploymentError('Distinct identified reviewer required')
    code_pin = review.get('installer_sha256')
    if code_pin != sha(Path(__file__).read_bytes()):
        raise DeploymentError('Review does not cover this installer')
    allowed = {no_alias(p) for p in allowed_destinations}
    if not allowed or not isinstance(plan.get('files'), list) or not plan['files']:
        raise DeploymentError('Empty installation plan')
    rows, seen = [], set()
    for item in plan['files']:
        source, target = no_alias(item['source']), no_alias(item['destination'])
        if not source.is_relative_to(work_root) or target not in allowed or target in seen:
            raise DeploymentError('Source/destination outside exact reviewed scope')
        if source == target or not target.parent.is_dir():
            raise DeploymentError('Unexpected target directory')
        seen.add(target)
        raw, prior = source.read_bytes(), current_bytes(target)
        if not raw or sha(raw) != item['sha256']:
            raise DeploymentError('Candidate source changed')
        if (sha(prior) if prior is not None else None) != item.get('baseline'):
            raise DeploymentError('Destination baseline changed')
        if target.suffix == '.py':
            ast.parse(raw, filename=str(target))
        backup_dir = None
        if 'backup_directory' in item:
            backup_dir = no_alias(item['backup_directory'])
            if (target.suffix != '.js' or
                not backup_dir.is_relative_to(work_root/'mobile_backups')):
                raise DeploymentError('External backup directory outside reviewed mobile backup root')
        rows.append({'source': source, 'target': target, 'raw': raw, 'prior': prior,
                     'backup_directory': backup_dir})
    if seen != allowed:
        raise DeploymentError('Plan does not match exact destination allowlist')
    return plan, sha(plan_raw), rows


def install(plan_path, review_path, *, work_root, allowed_destinations,
            assert_quiesced, evidence_dir, after_write=None):
    """Install once under caller-owned maintenance; keep every failure receipt."""
    assert_quiesced()
    plan, plan_hash, rows = prepare(plan_path, review_path, work_root=work_root,
                                   allowed_destinations=allowed_destinations)
    evidence_dir = no_alias(evidence_dir)
    if not evidence_dir.is_relative_to(no_alias(work_root)):
        raise DeploymentError('Evidence directory outside workspace')
    # Exclusive creation is the run lock. A crash leaves it for explicit recovery.
    evidence_dir.mkdir(parents=True, exist_ok=False)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    prepared, written = [], []
    result = {'schema': 'organism-installation/v1', 'plan_sha256': plan_hash,
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'files': [], 'status': 'PREPARED'}
    try:
        for index, row in enumerate(rows):
            assert_quiesced()
            target, old, raw = row['target'], row['prior'], row['raw']
            if current_bytes(target) != old:
                raise DeploymentError('Concurrent target edit before backup')
            backup = None
            if old is not None and old != raw:
                backup_dir = row['backup_directory']
                backup = (no_alias(backup_dir)/f'{index:04d}_{target.name}.bak_{stamp}'
                          if backup_dir is not None else
                          target.with_name(target.name + '.bak_' + stamp))
                write_new(backup, old)
            item = {'destination': str(target), 'source': str(row['source']),
                    'baseline': sha(old) if old is not None else None,
                    'sha256': sha(raw), 'backup': str(backup) if backup else None,
                    'changed': old != raw}
            prepared.append(item)
            receipt(evidence_dir / f'{index:04d}_prepared.json', item)
        for index, row in enumerate(rows):
            assert_quiesced()
            target, old, raw = row['target'], row['prior'], row['raw']
            no_alias(target)
            if current_bytes(target) != old:
                raise DeploymentError('Concurrent target edit before replacement')
            if old != raw:
                receipt(evidence_dir / f'{index:04d}_intent.json', prepared[index])
                written.append((index, row))
                atomic_replace(target, raw)
                receipt(evidence_dir / f'{index:04d}_installed.json', prepared[index])
                if after_write is not None:
                    after_write(index, target)
        assert_quiesced()
        for row in rows:
            if row['target'].read_bytes() != row['raw']:
                raise DeploymentError('Final verification failed')
        result.update(status='INSTALLED', files=prepared)
    except BaseException as exc:
        rollback = []
        for index, row in reversed(written):
            target, old, new = row['target'], row['prior'], row['raw']
            try:
                assert_quiesced()
                no_alias(target)
                current = current_bytes(target)
                if current == old:
                    outcome = 'ALREADY_BASELINE'
                elif current != new:
                    outcome = 'CONCURRENT_EDIT_PRESERVED'
                elif old is None:
                    target.unlink()  # Exactly one newly installed file, never recursive.
                    outcome = 'NEW_FILE_REMOVED'
                else:
                    backup = Path(prepared[index]['backup'])
                    if backup.read_bytes() != old:
                        raise DeploymentError('Rollback backup differs')
                    atomic_replace(target, old)
                    outcome = 'RESTORED_BYTES'
                rollback.append({'destination': str(target), 'outcome': outcome})
            except BaseException as restore_error:
                rollback.append({'destination': str(target), 'outcome': 'RESTORE_FAILED',
                                 'error_type': type(restore_error).__name__})
        result.update(status='FAILED', files=prepared, error_type=type(exc).__name__,
                      error=str(exc), rollback=rollback)
        receipt(evidence_dir / 'RESULT_FAILED.json', result)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        receipt(evidence_dir / 'FINAL_STATE.json', result)
    return result
