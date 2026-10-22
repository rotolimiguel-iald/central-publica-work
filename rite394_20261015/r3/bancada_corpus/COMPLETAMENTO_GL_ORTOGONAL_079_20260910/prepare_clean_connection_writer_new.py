from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt/COMPLETAMENTO_GL_ORTOGONAL_079_20260910').resolve()
SOURCE = ROOT / 'write_connection_comparison_new.py'
TARGET = ROOT / 'write_connection_comparison_clean_new.py'


def pin(path):
    data = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def emit(path, data):
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.read_bytes() != data:
        raise RuntimeError('TEMP_BYTE_MISMATCH')
    if path.exists():
        raise FileExistsError(path)
    temp.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError('FINAL_BYTE_MISMATCH')


before = pin(SOURCE)
raw = SOURCE.read_bytes()
if raw.count(bytes([0])) != 1:
    raise RuntimeError('UNEXPECTED_NULL_COUNT')
clean = raw.replace(bytes([0]), b'')
ast.parse(clean)
emit(TARGET, clean)
after = pin(SOURCE)
if before != after:
    raise RuntimeError('SOURCE_CHANGED')
record = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'kind': 'exclusive_clean_copy_of_unexecuted_note_writer',
    'source_before': before,
    'source_after': after,
    'source_unchanged': True,
    'target': pin(TARGET),
    'creator': pin(Path(__file__).resolve()),
    'change': {'removed_null_bytes': 1, 'all_other_bytes_preserved': clean == raw.replace(bytes([0]), b'')},
    'failure_preserved': 'AST parse of original writer failed: source code string cannot contain null bytes; original never executed',
    'validation': 'ast.parse(target_bytes) passed; target not executed by this helper',
    'originals_or_frozen_sources_modified': False,
}
path = ROOT / 'PROVENIENCIA_WRITER_LIMPO_079.json'
emit(path, (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'target': pin(TARGET), 'provenance': pin(path), 'source_unchanged': True}, ensure_ascii=False))
