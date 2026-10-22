from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = Path(__file__).resolve().parent
assert OUT.is_relative_to(ROOT)
pins = {}
checks = []


def check(name, condition, detail=None):
    row = {'name': name, 'passed': bool(condition)}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)
    assert condition, row


def pin(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    item = {'path': path.as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}
    if item['path'] in pins:
        assert pins[item['path']] == item, 'Changed source: ' + str(path)
    pins[item['path']] = item
    return item


def read_json(path):
    pin(path)
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def verify_recorded(value, origin):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and re.fullmatch('[0-9a-f]{64}', str(value.get('sha256', ''))):
            p = Path(value['path'])
            check('absolute_recorded_path:' + origin, p.is_absolute())
            actual = pin(p)
            check('recorded_pin:' + origin,
                  actual['sha256'] == value['sha256'] and
                  ('bytes' not in value or actual['bytes'] == value['bytes']), actual['path'])
        for key, child in value.items():
            verify_recorded(child, origin + '.' + key)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            verify_recorded(child, origin + '[' + str(i) + ']')


def new_json(path, obj):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)


config = read_json(OUT / 'CONFIG_ENTREGA_074.json')
snapshot = read_json(OUT / 'ESTADO_CANONICO_074.json')
check('snapshot_stable', snapshot['status'] == 'READ_ONLY_STABLE_SNAPSHOT'
      and snapshot['all_read_sources_unchanged'])
check('canonical_seal_matches', snapshot['seal_um_hash_matches'])
check('four_canonical_comparisons', len(snapshot['comparison_with_delivery073']) == 4)
verify_recorded(snapshot['pins'], 'snapshot074')
pin(ROOT / 'REEXAME_SUFICIENCIA_073_20260910/MANIFESTO_ENTREGA_073.json')

for name in config['source_directories']:
    directory = (ROOT / name).resolve()
    check('source_directory:' + name, directory.is_relative_to(ROOT) and directory.is_dir())
    for path in sorted(directory.iterdir()):
        if path.is_file():
            pin(path)
            if path.suffix.lower() == '.json':
                verify_recorded(read_json(path), name + '/' + path.name)

report = OUT / 'REEXAME_SUFICIENCIA.md'
tunnel = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_074_ESPONTANEA_translacao_natural_curvatura_e_completacao.md'
documents = [report, tunnel] + [OUT / name for name in
    ['MEMORIA_DE_TRABALHO_074.md', 'DESENHO_DO_FECHAMENTO_ADENDO_074.md', 'ADENDO_REVISOES_074.md']]
for path in documents:
    check('document_exists:' + path.name, path.is_file())
    pin(path)
    for i, link in enumerate(re.findall(r'\]\(<(C:/[^>]+)>\)', path.read_text(encoding='utf-8-sig'))):
        if link in [(OUT / 'MANIFESTO_ENTREGA_074.json').as_posix(),
                    (OUT / 'RESULTADO_ENTREGA_074.json').as_posix()]:
            continue
        check('document_link:' + path.name + ':' + str(i), Path(link).is_file(), link)

for filename in ['RESULTADO_ENTREGA_074.json', 'MANIFESTO_ENTREGA_074.json']:
    check('new_destination:' + filename, not (OUT / filename).exists())
check('no_new_cas_or_lean_claim', config['new_cas_controls'] == 0 and config['new_lean_compilations'] == 0)
for item in list(pins.values()):
    check('stable_before_output:' + item['path'], pin(item['path']) == item)

result = {
    'status': config['status'],
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'canonical': next(p for p in snapshot['pins'] if p['path'].endswith('/Nós/um.py')),
    'canonical_unchanged_from073': all(p['unchanged'] for p in snapshot['comparison_with_delivery073']),
    'canonical_embedded_files': snapshot['embedded_files'],
    'canonical_modules_present': snapshot['present'],
    'pending_canonical_modules': snapshot['absent'],
    'written_results': config['written_results'],
    'remaining': config['remaining'],
    'new_exact_symbolic_controls': 0,
    'new_lean_compilations': 0,
    'report': pin(report),
    'tunnel': pin(tunnel),
    'originals_written': False,
    'um_executed_or_imported': False,
    'nature_tests_run': False,
    'canonical_gate_modified': False,
    'goal_complete': False,
    'limits': config['limits']
}
new_json(OUT / 'RESULTADO_ENTREGA_074.json', result)
for path in sorted(OUT.iterdir()):
    if path.is_file():
        pin(path)
for item in list(pins.values()):
    check('stable_final:' + item['path'], pin(item['path']) == item)

manifest = {
    'status': 'PASS_DOCUMENTARY_INTEGRITY__WRITTEN_MATHEMATICS_NOT_LEAN',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'files': sorted(pins.values(), key=lambda p: p['path']),
    'checks': checks,
    'checks_total': len(checks),
    'checks_passed': sum(c['passed'] for c in checks),
    'new_cas_controls': 0,
    'new_lean_compilations': 0,
    'originals_written': False,
    'um_executed_or_imported': False,
    'goal_complete': False,
    'scope': 'Direct artifact integrity and documentary consistency; not a count of analytic theorems or proof of the full physical objective.'
}
manifest_pin = new_json(OUT / 'MANIFESTO_ENTREGA_074.json', manifest)
print(json.dumps({'status': manifest['status'], 'checks': len(checks),
                  'passed': manifest['checks_passed'], 'files': len(manifest['files']),
                  'report': pin(report), 'manifest': manifest_pin,
                  'tunnel': pin(tunnel)}, ensure_ascii=True))
