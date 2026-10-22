# -*- coding: utf-8 -*-
"""R2.1: session_memory.py do candidato lê pelo guard.read_checked (handle primeiro; review N3). Bytes LF preservados."""
from pathlib import Path
P = Path(__file__).resolve().parents[1] / 'candidato_r2_1' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'session_memory.py'
s = P.read_bytes().decode('utf-8')
assert b'\r\n' not in P.read_bytes()

old_read = '''def read_allowed_file(raw_path, log_path=None):
    # Requested name, resolved name (junctions/symlinks), hard-link count and file identity
    # are all checked BEFORE the file is opened. The refusal names the rule, never the bytes.
    reason = _guard().is_confidential_path(raw_path, log_path=log_path, where="read_allowed_file")
    if reason:
        raise ProtocolError("source_path_not_allowed:" + reason)
    path = Path(raw_path).resolve(strict=True)
    if not path.is_file():
        raise ProtocolError("source_is_not_file")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ProtocolError("source_too_large")
    return path, path.read_bytes()
'''
new_read = '''def _guarded_read(raw_path, max_bytes, log_path, where, not_file, too_large):
    # R2.1 (review N3): the requested and resolved NAMES are checked before any open; then the guard opens a
    # handle (attributes only), checks hard-link count, identity and the FINAL path of THAT handle, and reads
    # the same file object (never the name again). The refusal names the rule, never the bytes.
    guard = _guard()
    try:
        final, data = guard.read_checked(raw_path, max_bytes=max_bytes, log_path=log_path, where=where)
    except guard.PathRefused as exc:
        raise ProtocolError("source_path_not_allowed:" + exc.reason) from None
    except guard.NotRegularFile:
        raise ProtocolError(not_file) from None
    if len(data) > max_bytes:
        raise ProtocolError(too_large)
    return Path(final), data

def read_allowed_file(raw_path, log_path=None):
    return _guarded_read(raw_path, MAX_INPUT_BYTES, log_path, "read_allowed_file", "source_is_not_file",
                         "source_too_large")
'''
assert s.count(old_read) == 1
s = s.replace(old_read, new_read)

old_ref = '''    reason = _guard().is_confidential_path(raw_path, log_path=log_path, where=where)
    if reason:
        raise ProtocolError("source_path_not_allowed:" + reason)  # same code as every guarded read
    path = Path(raw_path).resolve(strict=True)
    if not path.is_file():
        raise ProtocolError("reference_is_not_file")
    if path.stat().st_size > MAX_REFERENCE_BYTES:
        raise ProtocolError("reference_too_large")
    try:
        ref = json.loads(path.read_bytes().decode("utf-8"))
'''
new_ref = '''    # Same code as every guarded read (source_path_not_allowed:<rule>); R2.1: read through the handle (N3).
    _, raw = _guarded_read(raw_path, MAX_REFERENCE_BYTES, log_path, where, "reference_is_not_file",
                           "reference_too_large")
    try:
        ref = json.loads(raw.decode("utf-8"))
'''
assert s.count(old_ref) == 1
s = s.replace(old_ref, new_ref)
P.write_bytes(s.encode('utf-8'))
print('ok', P.stat().st_size)
