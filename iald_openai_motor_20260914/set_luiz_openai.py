"""Set only the explicitly identified operator's motor; never emit account data."""
import copy
import json
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
TARGET = ROOT / 'iald_users.json'
RECEIPT = Path(__file__).with_name('luiz_motor_openai_20260915.json')


def new_bytes(path, payload):
    with path.open('xb') as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    if path.read_bytes() != payload:
        raise RuntimeError('Byte verification failed')


def members(text, start):
    decoder = json.JSONDecoder()
    i = start + 1
    while True:
        while text[i].isspace() or text[i] == ',':
            i += 1
        if text[i] == '}':
            return
        key, i = decoder.raw_decode(text, i)
        while text[i].isspace():
            i += 1
        assert text[i] == ':'
        i += 1
        while text[i].isspace():
            i += 1
        value_start = i
        value, i = decoder.raw_decode(text, i)
        yield key, value, value_start, i


def main():
    if RECEIPT.exists():
        raise RuntimeError('Receipt exists; inspect it instead of repeating mutation')
    original = TARGET.read_bytes()
    has_bom = original.startswith(b'\xef\xbb\xbf')
    source = original.decode('utf-8-sig')
    data = json.loads(source)
    if not isinstance(data, dict) or not isinstance(data.get('luiz'), dict):
        raise RuntimeError('Named account missing; no change')
    account = data['luiz']
    if account.get('motor') == 'openai':
        raise RuntimeError('Already OpenAI; no change')
    if account.get('motor') not in (None, '', 'nativa'):
        raise RuntimeError('Unexpected motor; no change')
    start = len(source) - len(source.lstrip())
    matches = [(a, b) for key, value, a, b in members(source, start) if key == 'luiz']
    if len(matches) != 1:
        raise RuntimeError('Ambiguous account; no change')
    a, b = matches[0]
    properties = [(c, d) for key, value, c, d in members(source, a) if key == 'motor']
    if len(properties) > 1:
        raise RuntimeError('Ambiguous motor; no change')
    if properties:
        c, d = properties[0]
        changed = source[:c] + '"openai"' + source[d:]
    else:
        whitespace = re.match(r'\s*', source[a + 1:]).group()
        separator = ',' + whitespace if account else ''
        changed = source[:a + 1] + whitespace + '"motor": "openai"' + separator + source[a + 1 + len(whitespace):]
    expected = copy.deepcopy(data)
    expected['luiz']['motor'] = 'openai'
    if json.loads(changed) != expected:
        raise RuntimeError('Unexpected semantic difference; no change')
    payload = (b'\xef\xbb\xbf' if has_bom else b'') + changed.encode('utf-8')
    stamp = datetime.now().astimezone().strftime('%Y%m%d_%H%M%S_%f')
    backup = TARGET.with_name(TARGET.name + '.bak_' + stamp)
    temporary = TARGET.with_name(TARGET.name + '.tmp_luiz_' + stamp)
    new_bytes(backup, original)
    new_bytes(temporary, payload)
    if TARGET.read_bytes() != original:
        raise RuntimeError('Concurrent edit detected; replacement cancelled')
    os.replace(temporary, TARGET)
    verified = json.loads(TARGET.read_bytes().decode('utf-8-sig'))
    if verified != expected:
        raise RuntimeError('Post-write state differs; inspect concurrency before further action')
    report = {
        'recorded_at': datetime.now().astimezone().isoformat(),
        'task': 'Motor OpenAI only for operator-identified luiz account',
        'username': 'luiz', 'before_motor': account.get('motor'), 'after_motor': 'openai',
        'only_changed_field': 'luiz.motor', 'all_other_fields_equal': True,
        'byte_backup_verified': True, 'backup_filename': backup.name,
        'consent_record_changed': False, 'server_restarted': False,
        'public_defaults_changed': False, 'runtime_response_tested': False,
    }
    receipt_tmp = RECEIPT.with_suffix('.json.tmp')
    new_bytes(receipt_tmp, json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
    os.replace(receipt_tmp, RECEIPT)
    print('OK: only luiz.motor changed to openai; byte backup and other fields verified; consent unchanged.')


if __name__ == '__main__':
    main()
