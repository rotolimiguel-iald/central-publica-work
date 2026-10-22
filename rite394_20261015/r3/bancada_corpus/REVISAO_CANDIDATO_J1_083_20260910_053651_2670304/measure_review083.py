from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt')
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'CANDIDATO_DERIVADA_WEYL_083_20260910'
NOTE = SOURCE / 'CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md'
MANIFEST = SOURCE / 'MANIFESTO_CANDIDATO_DERIVADO_083.json'
CONTROL = SOURCE / 'CONTROLE_COVARIANTE_J1_083.json'

def pin(path):
    p = Path(path).resolve()
    raw = p.read_bytes()
    return {'path': str(p), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def atomic_json_new(path, obj):
    if not path.is_relative_to(ROOT) or path.exists():
        raise RuntimeError('New files under Chatgpt only')
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_name(path.name + '.pending')
    with tmp.open('xb') as stream:
        stream.write(raw)
    if tmp.read_bytes() != raw:
        raise RuntimeError('Byte mismatch')
    tmp.rename(path)
    return pin(path)

manifest = json.loads(MANIFEST.read_bytes())
control = json.loads(CONTROL.read_bytes())
sources = [NOTE, MANIFEST, Path(manifest['script_after']['path'])]
sources += [Path(item['path']) for item in manifest['sources_after']]
assert len(sources) == len(set(map(str, sources)))
before_path = HERE / 'PINS_ANTES_J1_083.json'
if sys.argv[1] == 'capture':
    obj = {'created_utc': datetime.now(timezone.utc).isoformat(),
           'sources_before': [pin(p) for p in sources], 'helper_before': pin(__file__),
           'scope': 'Read-only source capture; no mathematical execution'}
    print(json.dumps(atomic_json_new(before_path, obj), ensure_ascii=False))
elif sys.argv[1] == 'finalize':
    before = json.loads(before_path.read_bytes())
    checks = []
    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed), 'kind': 'DOCUMENTARY'})
    for i, item in enumerate(before['sources_before']):
        check('source_unchanged_' + str(i), pin(item['path']) == item)
    check('helper_unchanged', pin(__file__) == before['helper_before'])
    for label, obj in [('manifest', manifest), ('control', control)]:
        expected = obj['sources_before'] + obj['sources_after']
        expected += [obj['script_before'], obj['script_after']] + obj.get('artifacts', [])
        for i, item in enumerate(expected):
            check(label + '_pin_' + str(i), pin(item['path']) == item)
        check(label + '_sources_before_after', obj['sources_before'] == obj['sources_after'])
    check('receipt_records_ten_predicates', len(control['checks']) == 10)
    check('receipt_records_all_predicates_true', all(v is True for v in control['checks'].values()))
    links = re.findall(r'\]\(<([A-Za-z]:/[^>]+)>\)', NOTE.read_text(encoding='utf-8'))
    for i, target in enumerate(links):
        check('source_link_' + str(i), Path(re.sub(r':\d+$', '', target)).is_file())
    final = HERE / 'PARECER_COVARIANTE_J1_E_DETECTOR_083.md'
    draft = final.with_name(final.name + '.pending')
    raw = draft.read_bytes()
    check('review_utf8_nonempty', len(raw) > 6000 and '\x00' not in raw.decode('utf-8'))
    if not all(c['passed'] for c in checks):
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))
    if final.exists():
        raise RuntimeError('Final exists')
    draft.rename(final)
    after = [pin(p) for p in sources]
    check('sources_unchanged_after_publication', after == before['sources_before'])
    result = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'DERIVED_INDEPENDENT_WRITTEN_REVIEW_NO_MATERIAL_ERROR_IN_STATED_DOMAIN',
        'sources_before': before['sources_before'], 'sources_after': after,
        'all_sources_unchanged': after == before['sources_before'],
        'artifacts': [pin(final), pin(before_path), pin(__file__)],
        'checks': checks, 'passed': sum(c['passed'] for c in checks), 'total': len(checks),
        'all_own_checks_are_documentary': True,
        'source_recorded_algebraic_predicates': 10, 'own_mathematical_reruns': 0,
        'own_cas_controls': 0, 'own_lean_controls': 0,
        'um_py_executed_or_imported': False, 'existing_files_modified': False,
        'external_approval_attributed': False,
        'scope_limits': ['One candidate; no complete CE image', 'No cancellation of A6 established',
                         'No general causal admissibility or QME', 'Excluded from delivery082'],
        'custody_note': 'All artifact pins refer to existing final paths; no pin targets renamed temporary.'
    }
    receipt = atomic_json_new(HERE / 'RECIBO_REVISAO_J1_083.json', result)
    print(json.dumps({'review': pin(final), 'receipt': receipt,
                      'checks': str(result['passed']) + '/' + str(result['total']),
                      'sources': len(after)}, ensure_ascii=False))
else:
    raise RuntimeError('Unknown mode')
