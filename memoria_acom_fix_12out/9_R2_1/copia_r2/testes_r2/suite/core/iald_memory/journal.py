"""Append-only, hash-chained per-context journal of memory mutations (D2a).

One JSONL file per context under ``<state>/journal/``. Every mutation of the
store is appended and fsynced here BEFORE the SQLite commit, so the journal is
the immediate backup of the mutation. Lines are never rewritten or deleted: a
line whose mutation never committed (process death between append and commit)
is voided by a later ``void`` line that references it. The ``anchor`` line
carries scope, anchor and the original inscription (base64), so the journals
alone rebuild every context (see ``migrate.rebuild_from_journal``).

Line format (ASCII JSON, sorted keys, one per line)::

    {"seq", "kind": "anchor"|"event"|"void", "context_id", "revision", "event_id",
     "actor_json", "changes_json", "state_sha256", "previous_hash", "event_hash",
     "created_at", "legacy", "prev_line_sha256", "line_sha256"}

``line_sha256 = sha256(prev_line_sha256 + canonical(line without line_sha256))``.
The anchor line adds ``scope_json``, ``anchor_json`` and ``objective_b64``; a
void line has ``voids_seq``, ``voids_line_sha256`` and ``reason``.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote

KINDS = ('anchor', 'event', 'void')
_RESERVED = {'CON', 'PRN', 'AUX', 'NUL'} | {f'COM{i}' for i in range(1, 10)} | {f'LPT{i}' for i in range(1, 10)}
_CHUNK = 256 * 1024


class JournalError(ValueError):
    """Visible refusal: the journal could not be read or extended consistently."""


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def line_digest(previous, fields):
    return hashlib.sha256((previous + canonical(fields)).encode('ascii')).hexdigest()


def path_for(journal_dir, context_id):
    # ':' is a valid identifier character, not a valid NTFS one. R2 (13/10/2026, review B, case collision):
    # NTFS compares names case-insensitively, so 'CtxCase' and 'ctxcase' shared one journal and both
    # contexts failed verify. ASCII upper-case letters are percent-escaped as well ('A' -> '%41'): every
    # remaining letter is lower-case or a hex digit inside an escape, so the name is unique up to case.
    name = ''.join('%%%02X' % ord(c) if 'A' <= c <= 'Z' else quote(c, safe='-_.') for c in context_id)
    if name.split('.')[0].upper() in _RESERVED:
        name = '_' + name
    return Path(journal_dir) / (name + '.events.jsonl')


def _parse(raw):
    try:
        line = json.loads(raw.decode('ascii'))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if (not isinstance(line, dict) or type(line.get('seq')) is not int or line.get('kind') not in KINDS
            or not isinstance(line.get('line_sha256'), str) or not isinstance(line.get('prev_line_sha256'), str)):
        return None
    return line


def read_all(path):
    """All lines in file order. Returns (lines, malformed_count, ends_with_newline)."""
    path = Path(path)
    if not path.exists():
        return [], 0, True
    raw = path.read_bytes()
    if not raw:
        return [], 0, True
    ends = raw.endswith(b'\n')
    lines, malformed = [], 0
    for chunk in raw.split(b'\n'):
        if not chunk:
            continue
        line = _parse(chunk)
        if line is None:
            malformed += 1
        else:
            lines.append(line)
    return lines, malformed, ends


def _tail_bytes(handle, size, minimum_lines):
    """Bytes from the start of a line boundary to EOF holding at least ``minimum_lines`` lines."""
    offset, buffer = size, b''
    while offset > 0:
        step = min(_CHUNK, offset)
        offset -= step
        handle.seek(offset)
        buffer = handle.read(step) + buffer
        if buffer.count(b'\n') > minimum_lines:
            break
    if offset > 0:
        cut = buffer.find(b'\n')
        buffer = buffer[cut + 1:]
    return buffer


def _trailing(handle, size, committed):
    """Return (last_line, uncommitted_trailing_lines, ends_with_newline).

    Walks back from the end of the open file over lines that are neither
    voided, void lines, nor committed in the database. ``committed`` maps
    revision to event hash as the database sees it under the writer lock.
    """
    if size == 0:
        return None, [], True
    need = 4
    while True:
        buffer = _tail_bytes(handle, size, need)
        chunks = [c for c in buffer.split(b'\n') if c]
        parsed = [(_parse(c), c) for c in chunks]
        ends = buffer.endswith(b'\n')
        last = next((line for line, _ in reversed(parsed) if line is not None), None)
        if last is None and len(buffer) < size:
            need *= 4
            continue
        uncommitted = []
        complete = True
        for line, _ in reversed(parsed):
            if line is None:
                continue
            if line['kind'] == 'void':
                break
            if committed.get(line.get('revision')) == line.get('event_hash'):
                break
            uncommitted.append(line)
        else:
            complete = len(buffer) >= size
        if not complete:
            need *= 4
            continue
        uncommitted.reverse()
        return last, uncommitted, ends


def _stat_tail(path):
    st = os.stat(path)
    return st.st_size, st.st_mtime_ns


def append(journal_dir, context_id, kind, fields, committed, created_at, cached_tail=None):
    """Append one line (voiding trailing uncommitted lines first) with fsync.

    ``fields`` are the mutation fields without seq/kind/prev/line digests.
    ``cached_tail`` is the value returned by the previous COMMITTED append of
    this process for the same context: ``{'size', 'mtime_ns', 'last'}``. It is
    used only when the file's size and mtime_ns are still exactly those (one
    ``stat``); otherwise the tail is read from the file. Re-opening a file that
    was just modified costs ~4.5 ms on the operator's machine (antivirus scan
    on open, measured 12/10/2026); ``stat`` costs 0.03 ms.
    Returns ``(line, tail)``: the appended line (dict, including
    ``line_sha256``) and the new tail record for the caller's cache.
    """
    if kind not in ('anchor', 'event'):
        raise JournalError('Only anchor and event lines are appended by the store')
    journal_dir = Path(journal_dir)
    journal_dir.mkdir(parents=True, exist_ok=True)
    path = path_for(journal_dir, context_id)
    # Read-only tail, then append-only write: the two cheap open modes on
    # Windows ('r+b' measured ~20x slower on the operator's machine, 12/10/2026).
    if path.exists():
        if (cached_tail and _stat_tail(path) == (cached_tail['size'], cached_tail['mtime_ns'])
                and cached_tail['last'] is not None):
            last, orphans, ends = cached_tail['last'], [], True
        else:
            with path.open('rb') as handle:
                handle.seek(0, os.SEEK_END)
                last, orphans, ends = _trailing(handle, handle.tell(), committed)
    else:
        last, orphans, ends = None, [], True
    seq = last['seq'] + 1 if last else 1
    previous = last['line_sha256'] if last else ''
    out = []
    for orphan in orphans:
        void = {'seq': seq, 'kind': 'void', 'context_id': context_id, 'voids_seq': orphan['seq'],
                'voids_line_sha256': orphan['line_sha256'], 'reason': 'not_committed',
                'created_at': created_at, 'prev_line_sha256': previous}
        void['line_sha256'] = line_digest(previous, void)
        out.append(void)
        previous, seq = void['line_sha256'], seq + 1
    line = dict(fields, seq=seq, kind=kind, prev_line_sha256=previous)
    line['line_sha256'] = line_digest(previous, line)
    out.append(line)
    payload = b''.join(canonical(item).encode('ascii') + b'\n' for item in out)
    if not ends:
        payload = b'\n' + payload  # a truncated last line (crash mid-write) stays visible and malformed
    with path.open('ab') as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    size, mtime_ns = _stat_tail(path)
    return line, {'size': size, 'mtime_ns': mtime_ns, 'last': line}


def append_many(journal_dir, context_id, lines):
    """Bootstrap/bulk append of already-built lines (anchor/event), chained, one fsync.

    Used by the migration: lines are appended after the existing tail; a line
    whose (revision, event_hash) already exists un-voided in the journal is
    skipped (idempotent re-run). Returns the number of lines written.
    """
    journal_dir = Path(journal_dir)
    journal_dir.mkdir(parents=True, exist_ok=True)
    path = path_for(journal_dir, context_id)
    existing, malformed, ends = read_all(path)
    chain = verify_lines(existing)
    if not chain['chain_ok']:
        raise JournalError('Existing journal chain is broken; refuse to extend it')
    voided = {l['voids_seq'] for l in existing if l['kind'] == 'void'}
    present = {(l.get('revision'), l.get('event_hash')) for l in existing if l['kind'] != 'void' and l['seq'] not in voided}
    seq = existing[-1]['seq'] + 1 if existing else 1
    previous = existing[-1]['line_sha256'] if existing else ''
    out = []
    for kind, fields in lines:
        if kind not in ('anchor', 'event'):
            raise JournalError('Only anchor and event lines can be bootstrapped')
        if (fields['revision'], fields['event_hash']) in present:
            continue
        line = dict(fields, seq=seq, kind=kind, prev_line_sha256=previous)
        line['line_sha256'] = line_digest(previous, line)
        out.append(line)
        previous, seq = line['line_sha256'], seq + 1
    if not out:
        return 0
    payload = b''.join(canonical(item).encode('ascii') + b'\n' for item in out)
    if not ends:
        payload = b'\n' + payload
    with path.open('ab') as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return len(out)


def verify_lines(lines):
    """Verify seq continuity and the digest chain of parsed lines."""
    previous, expected = '', 1
    broken_at = None
    for line in lines:
        fields = dict(line)
        digest = fields.pop('line_sha256')
        if line['seq'] != expected or line['prev_line_sha256'] != previous or line_digest(previous, fields) != digest:
            broken_at = line['seq']
            break
        previous, expected = digest, expected + 1
    return {'chain_ok': broken_at is None, 'broken_at_seq': broken_at, 'lines': len(lines)}


def effective_events(lines):
    """Map revision -> (event_hash, line) of the last un-voided anchor/event line per revision."""
    voided = {l['voids_seq'] for l in lines if l['kind'] == 'void'}
    effective = {}
    for line in lines:
        if line['kind'] != 'void' and line['seq'] not in voided:
            effective[line['revision']] = (line['event_hash'], line)
    return effective, voided


def verify_chain(path, db_events):
    """Compare the journal with the database view of one context.

    ``db_events`` is a list of (revision, event_hash). ``ok`` requires the file
    to exist, the digest chain to hold and every database event to have an
    un-voided line with the same hash. Orphans (lines not in the database) and
    malformed lines are counted, not hidden.
    """
    path = Path(path)
    lines, malformed, ends = read_all(path)
    chain = verify_lines(lines)
    effective, voided = effective_events(lines)
    db = dict(db_events)
    missing = [rev for rev, digest in db_events if effective.get(rev, (None,))[0] != digest]
    orphans = [l['seq'] for l in lines if l['kind'] != 'void' and l['seq'] not in voided
               and db.get(l['revision']) != l['event_hash']]
    return {'path': str(path), 'exists': path.exists(), 'lines': len(lines), 'malformed_lines': malformed,
            'ends_with_newline': ends, 'chain_ok': chain['chain_ok'], 'broken_at_seq': chain['broken_at_seq'],
            'voided': len(voided), 'orphans': len(orphans), 'orphan_seqs': orphans,
            'missing_events': len(missing), 'missing_revisions': missing,
            'ok': path.exists() and chain['chain_ok'] and not missing}
