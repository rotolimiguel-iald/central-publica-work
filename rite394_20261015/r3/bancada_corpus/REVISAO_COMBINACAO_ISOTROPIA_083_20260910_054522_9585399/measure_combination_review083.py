from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt')
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / 'COMBINACAO_TT_E_FALHA_ISOTROPIA_083_20260910'
NOTE = SOURCE / 'COMBINACAO_NO_DETECTOR_E_CONTRAEXEMPLO_ISOTROPIA.md'
MANIFEST = SOURCE / 'MANIFESTO_COMBINACAO_E_FALHA_083.json'

def pin(path):
    p = Path(path).resolve()
    raw = p.read_bytes()
    return {'path': str(p), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def new_json(path, obj):
    assert path.is_relative_to(ROOT) and not path.exists()
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_name(path.name + '.pending')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    return pin(path)

manifest = json.loads(MANIFEST.read_bytes())
sources = [NOTE, MANIFEST, Path(manifest['script_after']['path'])]
sources += [Path(p['path']) for p in manifest['sources_after']]
assert len(sources) == len(set(map(str, sources)))
before_path = HERE / 'PINS_ANTES_COMBINACAO_083.json'
if sys.argv[1] == 'capture':
    before = {'created_utc': datetime.now(timezone.utc).isoformat(),
              'sources_before': [pin(p) for p in sources], 'helper_before': pin(__file__)}
    print(json.dumps(new_json(before_path, before), ensure_ascii=False))
elif sys.argv[1] == 'finalize':
    before = json.loads(before_path.read_bytes())
    checks = []
    def check(name, passed):
        checks.append({'name': name, 'passed': bool(passed), 'kind': 'DOCUMENTARY'})
    for i, old in enumerate(before['sources_before']):
        check('source_unchanged_' + str(i), old == pin(old['path']))
    check('helper_unchanged', pin(__file__) == before['helper_before'])
    expected = manifest['sources_before'] + manifest['sources_after']
    expected += [manifest['script_before'], manifest['script_after']] + manifest['artifacts']
    for i, old in enumerate(expected):
        check('manifest_pin_' + str(i), pin(old['path']) == old)
    check('manifest_sources_before_after', manifest['sources_before'] == manifest['sources_after'])
    links = re.findall(r'\]\(<([A-Za-z]:/[^>]+)>\)', NOTE.read_text(encoding='utf-8'))
    for i, target in enumerate(links):
        check('source_link_' + str(i), Path(re.sub(r':\d+$', '', target)).is_file())
    final = HERE / 'PARECER_COMBINACAO_E_RESIDUO_ISOTROPIA_083.md'
    draft = final.with_name(final.name + '.pending')
    raw = draft.read_bytes()
    check('review_utf8_nonempty', len(raw) > 5000 and '\x00' not in raw.decode('utf-8'))
    if not all(c['passed'] for c in checks):
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))
    assert not final.exists()
    draft.rename(final)
    after = [pin(p) for p in sources]
    check('sources_preserved_after_publication', after == before['sources_before'])
    result = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'DERIVED_INDEPENDENT_WRITTEN_REVIEW_NO_MATERIAL_ERROR_IN_STATED_DOMAIN',
        'sources_before': before['sources_before'], 'sources_after': after,
        'all_sources_unchanged': after == before['sources_before'],
        'artifacts': [pin(final), pin(before_path), pin(__file__)],
        'checks': checks, 'passed': sum(c['passed'] for c in checks), 'total': len(checks),
        'all_checks_documentary': True, 'new_mathematical_executions': 0,
        'new_cas_controls': 0, 'new_lean_runs': 0,
        'um_py_executed_or_imported': False, 'existing_files_modified': False,
        'external_approval_attributed': False,
        'primary_reference_checked': 'https://arxiv.org/pdf/1805.03751v2, Section 3 equations22-25 and flatness paragraph, read during this session',
        'scope': 'One prescribed combination fails modulo s0 despite passing the full original TT detector; no universal no-go',
        'custody_note': 'Only existing final artifacts pinned; no renamed temporary pin.'
    }
    receipt = new_json(HERE / 'RECIBO_REVISAO_COMBINACAO_083.json', result)
    print(json.dumps({'review': pin(final), 'receipt': receipt,
                      'checks': str(result['passed']) + '/' + str(result['total']),
                      'sources': len(after)}, ensure_ascii=False))
else:
    raise RuntimeError('Unknown mode')
