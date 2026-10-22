from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
SOURCE = ROOT / 'REEXAME_SUFICIENCIA_077_20260910/finalize_delivery077.py'
OUT = ROOT / 'REEXAME_SUFICIENCIA_078_20260910'
TARGET = OUT / 'finalize_delivery078.py'
PROVENANCE = OUT / 'PROVENIENCIA_FINALIZADOR_078.json'


def pin_bytes(path, raw):
    return {'path': path.as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def emit_exclusive(path, raw):
    assert path.resolve().is_relative_to(ROOT)
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.read_bytes() != raw:
        raise RuntimeError('TEMP_BYTE_MISMATCH')
    if path.exists():
        raise FileExistsError(path)
    temp.rename(path)
    if path.read_bytes() != raw:
        raise RuntimeError('FINAL_BYTE_MISMATCH')


OUT.mkdir(exist_ok=True)
if TARGET.exists() or PROVENANCE.exists():
    raise FileExistsError('Finalizer or provenance already exists; no mutation performed')
source_raw = SOURCE.read_bytes()
source_before = pin_bytes(SOURCE, source_raw)
raw = source_raw
replacements = [
    (b'077', b'078', None),
    (b'076', b'077', None),
    (b"config['new_cas_controls'] == 420", b"config['new_cas_controls'] == 122", 1),
    (b'exact_ce_controls_and_no_lean', b'exact_tensor_controls_and_no_lean', 1),
    (b'ENTREGA_078_ESPONTANEA_truncagens_BRST_e_levantamento_Pontryagin_C5.md',
     b'ENTREGA_078_ESPONTANEA_residuo_A6_e_comparacao_de_completacoes.md', 1),
]
changes = []
for old, new, required_count in replacements:
    count = raw.count(old)
    if count == 0 or (required_count is not None and count != required_count):
        raise RuntimeError('UNEXPECTED_SUBSTITUTION_COUNT:' + repr(old) + ':' + str(count))
    previous_size = len(raw)
    raw = raw.replace(old, new)
    changes.append({'order': len(changes) + 1,
                    'old_utf8': old.decode('utf-8'), 'new_utf8': new.decode('utf-8'),
                    'occurrences_at_this_step': count,
                    'bytes_before': previous_size, 'bytes_after': len(raw)})
ast.parse(raw, filename=TARGET.as_posix())
if SOURCE.read_bytes() != source_raw:
    raise RuntimeError('SOURCE_CHANGED_BEFORE_OUTPUT')
emit_exclusive(TARGET, raw)
source_after_raw = SOURCE.read_bytes()
source_after = pin_bytes(SOURCE, source_after_raw)
if source_after_raw != source_raw:
    raise RuntimeError('SOURCE_CHANGED_AFTER_OUTPUT: preserve target for diagnosis')
if TARGET.read_bytes() != raw:
    raise RuntimeError('TARGET_CHANGED_AFTER_OUTPUT')
creator = Path(__file__).resolve()
provenance = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'PREPARED_ONLY__FINALIZER_NOT_EXECUTED',
    'source_before': source_before,
    'source_after': source_after,
    'source_bytes_unchanged': source_raw == source_after_raw,
    'target': pin_bytes(TARGET, raw),
    'ordered_byte_substitutions': changes,
    'all_other_bytes_preserved': True,
    'newline_counts': {
        'source_CRLF': source_raw.count(b'\r\n'), 'target_CRLF': raw.count(b'\r\n'),
        'source_LF': source_raw.count(b'\n'), 'target_LF': raw.count(b'\n'),
    },
    'syntax_check': 'ast.parse only; target not imported or executed',
    'expected_new_cas_controls': 122,
    'expected_new_lean_compilations': 0,
    'tunnel_name': 'ENTREGA_078_ESPONTANEA_residuo_A6_e_comparacao_de_completacoes.md',
    'creator': pin_bytes(creator, creator.read_bytes()),
    'finalizer_executed': False,
    'report_created': False,
    'config_created': False,
    'originals_modified': False,
    'um_executed_or_imported': False,
    'approval_attributed_to_other_agent': False,
}
emit_exclusive(PROVENANCE, (json.dumps(provenance, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'target': pin_bytes(TARGET, TARGET.read_bytes()),
                  'provenance': pin_bytes(PROVENANCE, PROVENANCE.read_bytes()),
                  'source_unchanged': True,
                  'substitution_counts': [item['occurrences_at_this_step'] for item in changes],
                  'finalizer_executed': False}, ensure_ascii=False))
