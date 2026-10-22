from pathlib import Path
import datetime
import hashlib
import json
import re
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt')
HERE = Path(__file__).resolve().parent
SRC = ROOT / 'COMPLEXO_CE_QUADRATICO_082_20260910'
MANIFEST = SRC / 'MANIFESTO_IDENTIFICACAO_CE_082.json'
NOTE = SRC / 'IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md'

def pin(path):
    p = Path(path).resolve()
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def atomic_new(path, data):
    path = Path(path)
    if not path.is_relative_to(ROOT) or path.exists():
        raise RuntimeError('New paths under Chatgpt only: ' + str(path))
    tmp = path.with_name(path.name + '.pending')
    with tmp.open('xb') as handle:
        handle.write(data)
    if tmp.read_bytes() != data or not data:
        raise RuntimeError('Byte verification failed')
    tmp.rename(path)
    return pin(path)

def json_new(path, obj):
    return atomic_new(path, (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

manifest = json.loads(MANIFEST.read_bytes())
sources = [NOTE, MANIFEST, Path(manifest['script_after']['path'])]
sources += [Path(p['path']) for p in manifest['sources_after']]
if len(set(map(str, sources))) != len(sources):
    raise RuntimeError('Duplicate sources')

if sys.argv[1] == 'capture':
    result = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'sources_before': [pin(p) for p in sources],
              'helper_before': pin(__file__),
              'scope': 'Documentary capture only; no mathematical execution'}
    print(json.dumps(json_new(HERE / 'PINS_ANTES_REVISAO_CE_082.json', result), ensure_ascii=False))
elif sys.argv[1] == 'finalize':
    before_path = HERE / 'PINS_ANTES_REVISAO_CE_082.json'
    before = json.loads(before_path.read_bytes())
    checks = []
    def check(label, value):
        checks.append({'name': label, 'passed': bool(value), 'kind': 'DOCUMENTARY'})
    for i, old in enumerate(before['sources_before']):
        check('source_unchanged_' + str(i), pin(old['path']) == old)
    check('helper_unchanged', pin(__file__) == before['helper_before'])
    expected = manifest['sources_before'] + manifest['sources_after']
    expected += [manifest['script_before'], manifest['script_after']] + manifest['artifacts']
    for i, old in enumerate(expected):
        check('manifest_pin_' + str(i), pin(old['path']) == old)
    check('manifest_before_after_identical', manifest['sources_before'] == manifest['sources_after'])
    note = NOTE.read_text(encoding='utf-8')
    links = re.findall(r'\]\(<([A-Za-z]:/[^>]+)>\)', note)
    for i, target in enumerate(links):
        plain = re.sub(r':\d+$', '', target)
        check('source_link_' + str(i), Path(plain).is_file())
    pending = HERE / 'PARECER_IDENTIFICACAO_CE_082.md.pending'
    final = HERE / 'PARECER_IDENTIFICACAO_CE_082.md'
    payload = pending.read_bytes()
    check('review_nonempty_utf8', len(payload) > 6000 and '\x00' not in payload.decode('utf-8'))
    if not all(x['passed'] for x in checks):
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))
    if final.exists():
        raise RuntimeError('Final exists')
    pending.rename(final)
    review_pin = pin(final)
    after = [pin(p) for p in sources]
    check('sources_unchanged_after_publication', after == before['sources_before'])
    result = {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status': 'DERIVED_INDEPENDENT_WRITTEN_REVIEW_NO_MATERIAL_ERROR_IN_STATED_DOMAIN',
        'sources_before': before['sources_before'], 'sources_after': after,
        'all_sources_unchanged': after == before['sources_before'],
        'artifacts': [review_pin, pin(before_path), pin(__file__)],
        'checks': checks, 'passed': sum(x['passed'] for x in checks), 'total': len(checks),
        'all_checks_are_documentary': True, 'new_mathematical_executions': 0,
        'new_cas_controls': 0, 'new_lean_controls': 0,
        'um_py_executed_or_imported': False, 'existing_files_modified': False,
        'external_approval_attributed': False,
        'primary_source_read': {'url': 'https://arxiv.org/pdf/1805.03751v2',
          'scope': 'Section 3 equations 22-25: Killing transport and flatness at constant curvature; not coefficient CE cohomology'},
        'custody_note': 'Pins name only existing final artifacts. Atomic temporary review renamed; no temporary path pinned.'
    }
    receipt = json_new(HERE / 'RECIBO_REVISAO_IDENTIFICACAO_CE_082.json', result)
    print(json.dumps({'review': review_pin, 'receipt': receipt, 'checks': str(result['passed']) + '/' + str(result['total']), 'sources': len(after)}, ensure_ascii=False))
else:
    raise RuntimeError('Unknown mode')
