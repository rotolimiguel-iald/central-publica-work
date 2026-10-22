"""Explicit migration v1 -> v2 (delta mode) and rebuild from the journal.

The store never migrates implicitly: a v1 database raises
``SchemaMigrationRequired``. ``migrate(root)`` is a dry run by default; with
``apply=True`` it runs, inside ONE ``BEGIN IMMEDIATE`` transaction:

 1. deep replay of every context in v1 form (every legacy ``state_json`` and
    every event digest verified; the chain must close);
 2. whole-database byte backup (D2c) next to the database,
    ``memory.sqlite3.pre_v2_<stamp>`` + ``.sha256``, optional second copy,
    both verified by SHA-256 re-read;
 3. the v2 tables (``context_state``, ``snapshots``, ``snapshot_policy`` with its
    initial row), chain index and triggers;
 4. one ``snapshots`` row (``reason='migration_v2'``) at the head of each
    context and its ``context_state`` row (delta mode on from here);
 5. journal bootstrap: one ``legacy: true`` line per existing event, appended
    and fsynced before the commit (idempotent on re-run);
 6. ``schema_version`` 1 -> 2 (the ``metadata_no_update`` guard is dropped
    and recreated inside the transaction) and ``schema_upgrade_2_at``;
 7. commit, then ``verify(deep=True)`` through the public store for every
    context, comparing head revision/state digest/event hash with step 1.

Legacy events are not touched (their ``state_json`` stays). A v2 database is
reported as already migrated and only verified. Nothing is written on a dry
run or on any failure before step 2; a failure after step 2 leaves the backup
and rolls the transaction back.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import time
import zlib

from . import journal as _journal
from . import snapshots as _snapshots
from .store import (
    MemoryStore, IntegrityError, SchemaMigrationRequired, SCHEMA_VERSION, MAX_TEXT_BYTES,
    _SCHEMA_V2_ADDITIONS, _CHAIN_COLUMNS, _TRIGGERS_V1, _execute_ddl, _actor, _changes,
    _apply_inplace, _initial_state, _dump, _sha, _event_digest,
)


class MigrationError(IntegrityError):
    pass


def _iso():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds')


def _connect(db_path):
    conn = sqlite3.connect(str(db_path), timeout=30, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    conn.execute('PRAGMA synchronous=FULL')
    conn.execute('PRAGMA busy_timeout=30000')
    return conn


def schema_version(conn):
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if 'metadata' not in tables:
        return None
    row = conn.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()
    return row[0] if row else None


def inspect(root):
    """Metadata and counts only; no record content is returned."""
    root = Path(root)
    db_path = root / 'memory.sqlite3'
    result = {'root': str(root), 'db': str(db_path), 'exists': db_path.exists(),
              'db_bytes': db_path.stat().st_size if db_path.exists() else 0}
    if not db_path.exists():
        return result
    conn = _connect(db_path)
    try:
        result['schema_version'] = schema_version(conn)
        result['journal_mode'] = conn.execute('PRAGMA journal_mode').fetchone()[0]
        result['tables'] = sorted(r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'"))
        result['triggers'] = sorted(r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='trigger'"))
        result['indexes'] = sorted(r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='index'"))
        if 'contexts' in result['tables']:
            result['contexts'] = conn.execute('SELECT count(*) FROM contexts').fetchone()[0]
            result['events'] = conn.execute('SELECT count(*) FROM events').fetchone()[0]
            sums = conn.execute('SELECT sum(length(state_json)), sum(length(changes_json)) FROM events').fetchone()
            result['sum_state_json_chars'] = int(sums[0] or 0)
            result['sum_changes_json_chars'] = int(sums[1] or 0)
            result['legacy_events'] = conn.execute("SELECT count(*) FROM events WHERE revision>0 AND state_json<>''").fetchone()[0]
            result['delta_events'] = conn.execute("SELECT count(*) FROM events WHERE revision>0 AND state_json=''").fetchone()[0]
        if 'snapshots' in result['tables']:
            result['snapshot_rows'] = conn.execute('SELECT count(*) FROM snapshots').fetchone()[0]
        if 'context_state' in result['tables']:
            result['context_state_rows'] = conn.execute('SELECT count(*) FROM context_state').fetchone()[0]
        if 'snapshot_policy' in result['tables']:
            row = conn.execute('SELECT policy_json FROM snapshot_policy WHERE id=1').fetchone()
            result['snapshot_policy'] = json.loads(row[0]) if row else None
    finally:
        conn.close()
    backups = _snapshots.list_legacy_backups(root)
    result['legacy_backups'] = len(backups)
    result['legacy_backups_bytes'] = sum(p.stat().st_size for p in backups)
    result['journal_files'] = len(list((root / 'journal').glob('*.events.jsonl'))) if (root / 'journal').exists() else 0
    result['db_snapshots'] = len(_snapshots.list_snapshots(root / 'snapshots'))
    return result


def replay_v1_context(conn, context_id):
    """Deep v1 replay of one context: anchor, envelope, chain and every legacy state verified.

    Streams the event rows (the legacy state_json is large) and returns the head
    (revision, state_json, state_sha256, event_hash), the scope, the anchor
    line fields for the journal bootstrap and the chain lines of every event.
    """
    row = conn.execute('SELECT * FROM contexts WHERE context_id=?', (context_id,)).fetchone()
    if row is None:
        raise MigrationError(f'Context {context_id} missing')
    anchor = json.loads(row['anchor_json'])
    if _sha(row['anchor_json'].encode('utf-8')) != row['anchor_sha256'] or anchor['context_id'] != context_id:
        raise MigrationError(f'Anchor digest/identity mismatch in {context_id}')
    scope = json.loads(row['scope_json'])
    if anchor['scope'] != scope or _dump(scope) != row['scope_json']:
        raise MigrationError(f'Anchor scope mismatch in {context_id}')
    decoder = zlib.decompressobj()
    objective = decoder.decompress(row['objective_blob'], MAX_TEXT_BYTES + 1)
    if len(objective) > MAX_TEXT_BYTES or decoder.unconsumed_tail or not decoder.eof or decoder.unused_data:
        raise MigrationError(f'Objective envelope invalid in {context_id}')
    if (len(objective) != row['objective_bytes'] or _sha(objective) != row['objective_sha256']
            or anchor['objective_sha256'] != row['objective_sha256'] or anchor['objective_bytes'] != len(objective)):
        raise MigrationError(f'Inscription byte/hash mismatch in {context_id}')
    objective.decode('utf-8')
    state, known = _initial_state(), set()
    previous = row['anchor_sha256']
    head = None
    chain = []
    count = 0
    for event in conn.execute('SELECT * FROM events WHERE context_id=? ORDER BY revision', (context_id,)):
        index = count
        count += 1
        if event['revision'] != index or event['previous_hash'] != previous:
            raise MigrationError(f'Event chain gap or predecessor mismatch in {context_id} at {index}')
        actor = _actor(json.loads(event['actor_json']))
        changes = json.loads(event['changes_json'])
        if index == 0:
            if event['event_id'] != 'anchor' or changes != {'anchor_sha256': previous} or actor != anchor['actor']:
                raise MigrationError(f'Invalid anchor event in {context_id}')
        else:
            normalized = _changes(changes, actor)
            if normalized != changes:
                raise MigrationError(f'Noncanonical event changes in {context_id} at {index}')
            _apply_inplace(state, normalized, known)
        state_json = _dump(state)
        if state_json != event['state_json'] or _sha(state_json.encode('utf-8')) != event['state_sha256']:
            raise MigrationError(f'Legacy state differs from replay or digest in {context_id} at {index}')
        digest = _event_digest(context_id, index, event['event_id'], actor, changes,
                               event['state_sha256'], previous, event['created_at'])
        if digest != event['event_hash']:
            raise MigrationError(f'Event digest mismatch in {context_id} at {index}')
        previous = digest
        fields = {'context_id': context_id, 'revision': index, 'event_id': event['event_id'],
                  'actor_json': event['actor_json'], 'changes_json': event['changes_json'],
                  'state_sha256': event['state_sha256'], 'previous_hash': event['previous_hash'],
                  'event_hash': event['event_hash'], 'created_at': event['created_at'], 'legacy': True}
        if index == 0:
            fields.update(scope_json=row['scope_json'], anchor_json=row['anchor_json'],
                          objective_b64=base64.b64encode(objective).decode('ascii'))
        chain.append(('anchor' if index == 0 else 'event', fields))
        head = {'revision': index, 'state_json': state_json, 'state_sha256': event['state_sha256'],
                'event_hash': event['event_hash'], 'created_at': event['created_at']}
    if head is None:
        raise MigrationError(f'Context {context_id} has no anchor event')
    return {'context_id': context_id, 'scope': scope, 'events': count, 'head': head, 'chain': chain}


def whole_backup(db_path, second_copy_dir=None, label='pre_v2'):
    """D2c: verified byte copy of the database before a non-additive operation."""
    db_path = Path(db_path)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup = db_path.with_name(f'{db_path.name}.{label}_{stamp}')
    size, digest = _snapshots.copy_verified(db_path, backup)
    _snapshots._write_text_atomic(backup.with_name(backup.name + '.sha256'), f'{digest}  {backup.name}\n')
    result = {'path': str(backup), 'bytes': size, 'sha256': digest, 'second_copy': None}
    if second_copy_dir:
        second_dir = Path(second_copy_dir)
        second_dir.mkdir(parents=True, exist_ok=True)
        second = second_dir / backup.name
        size2, digest2 = _snapshots.copy_verified(db_path, second)
        if size2 != size or digest2 != digest:
            raise MigrationError('Second backup copy does not match the first')
        _snapshots._write_text_atomic(second.with_name(second.name + '.sha256'), f'{digest2}  {second.name}\n')
        result['second_copy'] = {'path': str(second), 'bytes': size2, 'sha256': digest2}
    return result


def verify_all(root, deep=False, snapshot_archive_dir=None):
    """Public-store verification of every context (v2 database)."""
    root = Path(root)
    store = MemoryStore(root, snapshot_archive_dir=snapshot_archive_dir)
    conn = _connect(root / 'memory.sqlite3')
    try:
        contexts = [(r[0], json.loads(r[1])) for r in conn.execute('SELECT context_id, scope_json FROM contexts ORDER BY created_at, context_id')]
    finally:
        conn.close()
    results = {}
    for context_id, scope in contexts:
        results[context_id] = store.verify(context_id, scope, deep=deep)
    return results


def migrate(root, *, apply=False, second_copy_dir=None, deep_after=True, snapshot_archive_dir=None, log=None):
    """Dry run (default) or apply the v1 -> v2 migration. Returns a receipt dict."""
    root = Path(root)
    log = log or (lambda *_: None)
    db_path = root / 'memory.sqlite3'
    started = time.time()
    receipt = {'root': str(root), 'db': str(db_path), 'apply': apply, 'started_at': _iso(),
               'before': inspect(root)}
    if not db_path.exists():
        raise MigrationError('No memory database at this root')
    conn = _connect(db_path)
    try:
        conn.execute('BEGIN IMMEDIATE')
        version = schema_version(conn)
        if version == str(SCHEMA_VERSION):
            conn.rollback()
            receipt['already_migrated'] = True
            receipt['verify_after'] = _summarize(verify_all(root, deep=deep_after, snapshot_archive_dir=snapshot_archive_dir))
            receipt['finished_at'], receipt['seconds'] = _iso(), round(time.time() - started, 3)
            return receipt
        if version != '1':
            raise MigrationError(f'Unsupported schema version {version!r}; refuse to migrate')
        found = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='trigger'")}
        if not _TRIGGERS_V1 <= found:
            raise MigrationError('v1 immutability guards missing; refuse to migrate')
        if conn.execute('PRAGMA journal_mode').fetchone()[0].lower() != 'delete':
            raise MigrationError('Unexpected journal mode; refuse unsafe byte backup')
        receipt['already_migrated'] = False
        contexts = [r[0] for r in conn.execute('SELECT context_id FROM contexts ORDER BY created_at, context_id')]
        replays = {}
        for context_id in contexts:
            log(f'replay v1 {context_id}')
            replays[context_id] = replay_v1_context(conn, context_id)
        receipt['contexts'] = {cid: {'events': r['events'], 'head_revision': r['head']['revision'],
                                     'head_state_sha256': r['head']['state_sha256'],
                                     'head_event_hash': r['head']['event_hash'],
                                     'scope': r['scope']} for cid, r in replays.items()}
        if not apply:
            conn.rollback()
            receipt['dry_run'] = True
            receipt['finished_at'], receipt['seconds'] = _iso(), round(time.time() - started, 3)
            return receipt
        log('whole-database backup')
        receipt['backup'] = whole_backup(db_path, second_copy_dir)
        log('schema v2 additions')
        _execute_ddl(conn, _SCHEMA_V2_ADDITIONS)
        # The 50-mutation / 60-minute window starts at the migration.
        conn.execute('INSERT INTO snapshot_policy VALUES (1, ?)',
                     (json.dumps(_snapshots.new_policy(time.time()), sort_keys=True),))
        at = _iso()
        for context_id, replay in replays.items():
            head = replay['head']
            conn.execute('INSERT INTO snapshots VALUES (?,?,?,?,?,?,?)',
                         (context_id, head['revision'], head['state_json'], head['state_sha256'],
                          head['event_hash'], at, 'migration_v2'))
            conn.execute('INSERT INTO context_state VALUES (?,?,?,?,?,?)',
                         (context_id, head['revision'], head['state_json'], head['state_sha256'],
                          head['event_hash'], at))
        journal_written = {}
        for context_id, replay in replays.items():
            log(f'journal bootstrap {context_id}')
            journal_written[context_id] = _journal.append_many(root / 'journal', context_id, replay['chain'])
        receipt['journal_lines_written'] = journal_written
        conn.execute('DROP TRIGGER metadata_no_update')
        conn.execute("UPDATE metadata SET value=? WHERE key='schema_version'", (str(SCHEMA_VERSION),))
        conn.execute("CREATE TRIGGER metadata_no_update BEFORE UPDATE ON metadata BEGIN SELECT RAISE(ABORT,'immutable metadata'); END")
        conn.execute('INSERT INTO metadata VALUES (?,?)', ('schema_upgrade_2_at', at))
        conn.commit()
        receipt['committed_at'] = _iso()
    except sqlite3.Error as exc:
        conn.rollback()
        raise MigrationError(f'Migration transaction failed: {exc!r}') from exc
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()
    log('verify after')
    after = verify_all(root, deep=deep_after, snapshot_archive_dir=snapshot_archive_dir)
    receipt['verify_after'] = _summarize(after)
    mismatches = []
    for context_id, replay in replays.items():
        receipt_after = after[context_id]['receipt']
        if (receipt_after['revision'] != replay['head']['revision']
                or receipt_after['state_sha256'] != replay['head']['state_sha256']
                or receipt_after['event_hash'] != replay['head']['event_hash']
                or not after[context_id]['ok']):
            mismatches.append(context_id)
    receipt['head_mismatches'] = mismatches
    receipt['after'] = inspect(root)
    receipt['ok'] = not mismatches
    receipt['finished_at'], receipt['seconds'] = _iso(), round(time.time() - started, 3)
    if mismatches:
        raise MigrationError(f'Post-migration verification mismatch in {mismatches}')
    return receipt


def _summarize(results):
    keys = ('ok', 'event_count', 'schema_version', 'deep', 'replay_from_revision', 'legacy_events',
            'delta_events', 'snapshot_rows', 'journal_ok', 'journal_lines', 'journal_voided', 'journal_orphans',
            'journal_missing_events')
    summary = {}
    for context_id, verification in results.items():
        entry = {k: verification[k] for k in keys}
        entry['receipt'] = {k: verification['receipt'][k] for k in ('revision', 'event_hash', 'state_sha256')}
        summary[context_id] = entry
    return summary


def rebuild_from_journal(journal_dir, out_root, snapshot_archive_dir=None, log=None):
    """Rebuild a v2 database from the journals alone into an EMPTY ``out_root``.

    Every un-voided line is replayed; each event's state digest and event hash
    are recomputed and must match the line. The journal files are copied into
    the new root so the rebuilt store verifies with ``journal_ok``. Returns a
    report with the head of every context.
    """
    journal_dir, out_root = Path(journal_dir), Path(out_root)
    log = log or (lambda *_: None)
    if (out_root / 'memory.sqlite3').exists():
        raise MigrationError('Refuse to rebuild into a root that already holds a database')
    store = MemoryStore(out_root, snapshot_archive_dir=snapshot_archive_dir)
    report = {'journal_dir': str(journal_dir), 'out_root': str(out_root), 'contexts': {}}
    conn = store._connect()
    try:
        conn.execute('BEGIN IMMEDIATE')
        for path in sorted(journal_dir.glob('*.events.jsonl')):
            lines, malformed, _ = _journal.read_all(path)
            chain = _journal.verify_lines(lines)
            if not chain['chain_ok']:
                raise MigrationError(f'Journal chain broken in {path.name} at seq {chain["broken_at_seq"]}')
            effective, voided = _journal.effective_events(lines)
            if not effective or sorted(effective) != list(range(len(effective))):
                raise MigrationError(f'Journal {path.name} does not hold a contiguous revision sequence')
            anchor_hash, anchor_line = effective[0]
            if anchor_line['kind'] != 'anchor':
                raise MigrationError(f'Journal {path.name} revision 0 is not an anchor line')
            context_id = anchor_line['context_id']
            log(f'rebuild {context_id} from {path.name}')
            objective = base64.b64decode(anchor_line['objective_b64'])
            anchor_json, scope_json = anchor_line['anchor_json'], anchor_line['scope_json']
            anchor = json.loads(anchor_json)
            if anchor['context_id'] != context_id or anchor['objective_sha256'] != _sha(objective):
                raise MigrationError(f'Anchor line of {context_id} does not bind its objective')
            anchor_sha = _sha(anchor_json.encode('utf-8'))
            conn.execute('INSERT INTO contexts VALUES (?,?,?,?,?,?,?,?)',
                         (context_id, scope_json, anchor_json, anchor_sha, zlib.compress(objective, 9),
                          _sha(objective), len(objective), anchor_line['created_at']))
            state, known, previous = _initial_state(), set(), anchor_sha
            head = None
            for revision in range(len(effective)):
                digest_line, line = effective[revision]
                if line['context_id'] != context_id or line['previous_hash'] != previous:
                    raise MigrationError(f'Journal chain of {context_id} does not link at revision {revision}')
                actor = _actor(json.loads(line['actor_json']))
                changes = json.loads(line['changes_json'])
                if revision == 0:
                    if changes != {'anchor_sha256': anchor_sha} or actor != anchor['actor'] or line['event_id'] != 'anchor':
                        raise MigrationError(f'Invalid anchor line in {context_id}')
                else:
                    _apply_inplace(state, _changes(changes, actor), known)
                state_json = _dump(state)
                state_sha = _sha(state_json.encode('utf-8'))
                if state_sha != line['state_sha256']:
                    raise MigrationError(f'Journal state digest of {context_id} differs at revision {revision}')
                digest = _event_digest(context_id, revision, line['event_id'], actor, changes, state_sha,
                                       previous, line['created_at'])
                if digest != line['event_hash']:
                    raise MigrationError(f'Journal event hash of {context_id} differs at revision {revision}')
                conn.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?)',
                             (context_id, revision, line['event_id'], line['actor_json'], line['changes_json'],
                              state_json if revision == 0 else '', state_sha, previous, digest, line['created_at']))
                previous = digest
                head = (revision, state_json, state_sha, digest, line['created_at'])
            revision, state_json, state_sha, digest, created_at = head
            conn.execute('INSERT INTO context_state VALUES (?,?,?,?,?,?)',
                         (context_id, revision, state_json, state_sha, digest, created_at))
            conn.execute('INSERT INTO snapshots VALUES (?,?,?,?,?,?,?)',
                         (context_id, revision, state_json, state_sha, digest, _iso(), 'rebuild'))
            report['contexts'][context_id] = {'scope': json.loads(scope_json), 'events': revision + 1,
                                              'head_revision': revision, 'head_state_sha256': state_sha,
                                              'head_event_hash': digest, 'journal_lines': len(lines),
                                              'journal_voided': len(voided), 'journal_malformed': malformed}
        conn.commit()
    except sqlite3.Error as exc:
        conn.rollback()
        raise MigrationError(f'Rebuild transaction failed: {exc!r}') from exc
    except BaseException:
        conn.rollback()
        raise
    finally:
        conn.close()
    (out_root / 'journal').mkdir(parents=True, exist_ok=True)
    for path in sorted(journal_dir.glob('*.events.jsonl')):
        _snapshots.copy_verified(path, out_root / 'journal' / path.name)
    report['verify'] = _summarize(verify_all(out_root, deep=True, snapshot_archive_dir=snapshot_archive_dir))
    report['ok'] = all(v['ok'] for v in report['verify'].values())
    if not report['ok']:
        raise MigrationError('Rebuilt database did not verify')
    return report
