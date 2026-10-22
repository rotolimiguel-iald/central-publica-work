"""Whole-database byte snapshots and the archive of legacy backups (D2b/D2c).

Policy (evaluated on the write path, under the writer lock, before the first
write of the transaction): a byte copy of ``memory.sqlite3`` is taken when
``SNAPSHOT_EVERY_MUTATIONS`` mutations or ``SNAPSHOT_MAX_AGE_SECONDS`` have
passed since the last snapshot, whichever comes first. Without a mutation
nothing is copied (there is no daemon). The counter lives in the database
itself (table ``snapshot_policy``, one row) and is updated in the mutation's
transaction, so it counts committed mutations and costs no extra file I/O. The copy is verified (size and
SHA-256 re-read from the destination) and gets a ``.sha256`` sidecar. The
``KEEP_LOCAL`` newest snapshots stay next to the database; older ones are
MOVED (copy, verify, delete source, manifest line) to the archive directory.
If the archive is unavailable or a copy does not verify, nothing local is
deleted and a visible warning is recorded.

``archive_legacy_backups`` moves the v1 ``memory.sqlite3.bak_*`` files the same
way (keep the newest ``keep``, verify SHA-256, manifest), never deleting a
source whose copy did not verify. It never touches ``memory.sqlite3``, its
``-journal``, ``snapshots/`` or ``journal/``.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import time
import warnings

SNAPSHOT_EVERY_MUTATIONS = 50
SNAPSHOT_MAX_AGE_SECONDS = 3600
KEEP_LOCAL = 3
DEFAULT_ARCHIVE_DIR = r'D:\IALD_ARQUIVO\MEMORIA_IALD\snapshots'
ENV_ARCHIVE_DIR = 'IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR'
SNAPSHOT_PREFIX = 'memory.sqlite3.snap_'
LEGACY_BACKUP_PREFIX = 'memory.sqlite3.bak_'
COPY_BUFFER = 8 * 1024 * 1024
WARNINGS_FILE = 'AVISOS.jsonl'
MANIFEST_JSONL = 'MANIFEST.jsonl'
MANIFEST_JSON = 'MANIFEST.json'


class SnapshotError(RuntimeError):
    """A snapshot could not be taken or did not verify."""


def default_archive_dir():
    return Path(os.environ.get(ENV_ARCHIVE_DIR) or DEFAULT_ARCHIVE_DIR)


def _iso(now=None):
    return datetime.fromtimestamp(now if now is not None else time.time(), timezone.utc).isoformat(timespec='microseconds')


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        while True:
            block = handle.read(COPY_BUFFER)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def _copy_bytes(src, dst):
    """Copy bytes src -> dst with fsync; returns (bytes, sha256 of what was written)."""
    digest, total = hashlib.sha256(), 0
    with Path(src).open('rb') as source, Path(dst).open('wb') as target:
        while True:
            block = source.read(COPY_BUFFER)
            if not block:
                break
            digest.update(block)
            target.write(block)
            total += len(block)
        target.flush()
        os.fsync(target.fileno())
    return total, digest.hexdigest()


def copy_verified(src, dst):
    """Copy and verify: size equal, SHA-256 of the written stream equal to the re-read destination."""
    src, dst = Path(src), Path(dst)
    size = src.stat().st_size
    written, digest = _copy_bytes(src, dst)
    if written != size or dst.stat().st_size != size:
        raise SnapshotError(f'Copy size mismatch for {src.name}')
    if sha256_file(dst) != digest:
        raise SnapshotError(f'Copy digest mismatch for {src.name}')
    return size, digest


def _write_text_atomic(path, text):
    path = Path(path)
    temp = path.with_name(path.name + '.tmp_' + format(os.getpid(), 'x') + '_' + format(time.time_ns(), 'x'))
    data = text.encode('utf-8')
    with temp.open('wb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.stat().st_size != len(data):
        temp.unlink()
        raise SnapshotError(f'Short write for {path.name}')
    os.replace(temp, path)


def parse_policy(text):
    """Policy row stored in the database (table ``snapshot_policy``); None when absent."""
    if text is None:
        return None
    try:
        policy = json.loads(text)
    except ValueError as exc:
        raise SnapshotError('Snapshot policy row unreadable') from exc
    if not isinstance(policy, dict) or 'mutations_since_snapshot' not in policy or 'window_started_at' not in policy:
        raise SnapshotError('Snapshot policy row malformed')
    return policy


def new_policy(now):
    return {'mutations_since_snapshot': 0, 'window_started_at': now, 'last_snapshot': None,
            'last_snapshot_at': None, 'snapshots_taken': 0, 'every_mutations': SNAPSHOT_EVERY_MUTATIONS,
            'max_age_seconds': SNAPSHOT_MAX_AGE_SECONDS, 'updated_at': _iso(now)}


def due(policy, now):
    """True when the policy says a snapshot is due at this mutation (counter already incremented)."""
    return (policy['mutations_since_snapshot'] >= SNAPSHOT_EVERY_MUTATIONS
            or now - float(policy['window_started_at']) >= SNAPSHOT_MAX_AGE_SECONDS)


def take(db_path, snap_dir, now=None):
    """Byte copy of the database into snap_dir, verified, with a .sha256 sidecar."""
    db_path, snap_dir = Path(db_path), Path(snap_dir)
    now = time.time() if now is None else now
    if not db_path.exists() or db_path.stat().st_size == 0:
        raise SnapshotError('Refuse mutation of empty memory database')
    snap_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.fromtimestamp(now).strftime('%Y%m%d_%H%M%S_%f')
    temp = snap_dir / (SNAPSHOT_PREFIX + stamp + '.tmp')
    if temp.exists():
        raise SnapshotError('Snapshot temporary already exists')
    size, digest = copy_verified(db_path, temp)
    final = snap_dir / (SNAPSHOT_PREFIX + stamp + '_' + digest[:16])
    os.replace(temp, final)
    _write_text_atomic(final.with_name(final.name + '.sha256'), f'{digest}  {final.name}\n')
    return {'path': str(final), 'name': final.name, 'bytes': size, 'sha256': digest, 'at': _iso(now)}


def list_snapshots(snap_dir):
    snap_dir = Path(snap_dir)
    if not snap_dir.exists():
        return []
    return sorted(p for p in snap_dir.iterdir()
                  if p.is_file() and p.name.startswith(SNAPSHOT_PREFIX)
                  and not p.name.endswith('.sha256') and not p.name.endswith('.tmp'))


def _warn(snap_dir, message, **extra):
    record = dict(at=_iso(), message=message, **extra)
    try:
        Path(snap_dir).mkdir(parents=True, exist_ok=True)
        with (Path(snap_dir) / WARNINGS_FILE).open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + '\n')
    except OSError:
        pass
    warnings.warn('iald_memory snapshots: ' + message, RuntimeWarning, stacklevel=3)


def _manifest_line(dest_dir, entry):
    with (Path(dest_dir) / MANIFEST_JSONL).open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + '\n')
        handle.flush()
        os.fsync(handle.fileno())


def _move_verified(src, dest_dir):
    """Move one file (and its .sha256 sidecar if any) into dest_dir: copy, verify, delete source."""
    src, dest_dir = Path(src), Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dst = dest_dir / src.name
    source_sha = sha256_file(src)
    if dst.exists() and dst.stat().st_size == src.stat().st_size and sha256_file(dst) == source_sha:
        size, digest = dst.stat().st_size, source_sha  # already archived (idempotent re-run)
    else:
        partial = dst.with_name(dst.name + '.part')
        try:
            size, digest = copy_verified(src, partial)
            if digest != source_sha:
                raise SnapshotError(f'Archived copy of {src.name} does not match its source')
        except SnapshotError:
            # The partial copy is kept, renamed, as evidence; the source is never touched.
            if partial.exists():
                os.replace(partial, partial.with_name(partial.name + '.mismatch'))
            raise
        os.replace(partial, dst)
    if sha256_file(dst) != source_sha:
        raise SnapshotError(f'Archived copy of {src.name} does not verify')
    sidecar = src.with_name(src.name + '.sha256')
    if sidecar.exists():
        sidecar_dst = dest_dir / sidecar.name
        if not sidecar_dst.exists():
            copy_verified(sidecar, sidecar_dst)
        sidecar.unlink()
    src.unlink()
    entry = {'name': src.name, 'bytes': size, 'sha256': digest, 'src': str(src), 'dst': str(dst),
             'moved_at': _iso()}
    _manifest_line(dest_dir, entry)
    return entry


def prune_and_archive(snap_dir, archive_dir, keep=KEEP_LOCAL):
    """Keep the newest ``keep`` snapshots locally; move the rest to the archive, fail-safe."""
    result = {'kept': [], 'moved': [], 'failed': []}
    snapshots = list_snapshots(snap_dir)
    result['kept'] = [p.name for p in snapshots[-keep:]] if keep > 0 else []
    for path in (snapshots[:-keep] if keep > 0 else snapshots):
        try:
            result['moved'].append(_move_verified(path, archive_dir))
        except (OSError, SnapshotError) as exc:
            result['failed'].append({'name': path.name, 'error': repr(exc)})
            _warn(snap_dir, 'archive unavailable or copy did not verify; local snapshot kept',
                  name=path.name, archive_dir=str(archive_dir), error=repr(exc))
            break
    return result


def snapshot_if_due(db_path, snap_dir, archive_dir, policy, now=None):
    """Count one mutation; take, verify and archive a snapshot when the policy says so.

    ``policy`` is the current policy dict (or None). Returns ``(taken, policy)``:
    the snapshot record or None, and the updated policy the caller persists in
    the same transaction as the mutation (table ``snapshot_policy``). Raises
    SnapshotError when a due snapshot cannot be taken or verified (the caller
    fails the mutation). Nothing is written to any side file here.
    """
    now = time.time() if now is None else now
    policy = dict(policy) if policy else new_policy(now)
    policy['mutations_since_snapshot'] = int(policy['mutations_since_snapshot']) + 1
    taken = None
    if due(policy, now):
        taken = take(db_path, snap_dir, now)
        policy.update(mutations_since_snapshot=0, window_started_at=now, last_snapshot=taken['name'],
                      last_snapshot_at=taken['at'], snapshots_taken=int(policy.get('snapshots_taken', 0)) + 1)
        taken['archive'] = prune_and_archive(snap_dir, archive_dir, KEEP_LOCAL)
    policy.update(every_mutations=SNAPSHOT_EVERY_MUTATIONS, max_age_seconds=SNAPSHOT_MAX_AGE_SECONDS,
                  updated_at=_iso(now))
    return taken, policy


def list_legacy_backups(state_dir):
    state_dir = Path(state_dir)
    return sorted(p for p in state_dir.iterdir()
                  if p.is_file() and p.name.startswith(LEGACY_BACKUP_PREFIX)
                  and not p.name.endswith('.sha256') and not p.name.endswith('.part')
                  and not p.name.endswith('.mismatch'))


def archive_legacy_backups(state_dir, dest, keep=3, dry_run=False, log=None):
    """Move the v1 per-mutation backups to ``dest``, keeping the newest ``keep`` in place.

    Order is the timestamp in the name. Each file: SHA-256 of the source, copy
    with fsync, SHA-256 of the destination re-read; equal -> delete the source
    and write a manifest line; different -> keep the source and abort (what was
    moved stays recorded). Writes MANIFEST.json at the end.
    """
    state_dir, dest = Path(state_dir), Path(dest)
    log = log or (lambda *_: None)
    started = _iso()
    backups = list_legacy_backups(state_dir)
    kept = backups[-keep:] if keep > 0 else []
    to_move = backups[:-keep] if keep > 0 else backups
    report = {'state_dir': str(state_dir), 'dest': str(dest), 'keep': keep, 'dry_run': dry_run,
              'found': len(backups), 'to_move': len(to_move), 'kept': [p.name for p in kept],
              'moved': 0, 'moved_bytes': 0, 'already_archived': 0, 'failed': None, 'started_at': started}
    if dry_run:
        report['plan'] = [{'name': p.name, 'bytes': p.stat().st_size} for p in to_move]
        report['finished_at'] = _iso()
        return report
    dest.mkdir(parents=True, exist_ok=True)
    for path in to_move:
        try:
            entry = _move_verified(path, dest)
        except (OSError, SnapshotError) as exc:
            report['failed'] = {'name': path.name, 'error': repr(exc)}
            log(f'ABORT at {path.name}: {exc!r}; source kept')
            break
        report['moved'] += 1
        report['moved_bytes'] += entry['bytes']
        log(f'moved {entry["name"]} {entry["bytes"]} B sha256 {entry["sha256"][:16]}')
    manifest = dest / MANIFEST_JSONL
    report['manifest_jsonl'] = str(manifest)
    report['manifest_jsonl_sha256'] = sha256_file(manifest) if manifest.exists() else None
    report['manifest_lines'] = sum(1 for _ in manifest.open('rb')) if manifest.exists() else 0
    report['finished_at'] = _iso()
    _write_text_atomic(dest / MANIFEST_JSON, json.dumps(report, ensure_ascii=False, sort_keys=True, indent=1))
    return report
