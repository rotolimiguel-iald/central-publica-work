from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
HERE = Path(__file__).resolve().parent
DELIVERY = ROOT / 'REEXAME_SUFICIENCIA_083_20260910'
REVIEWS = ROOT / 'REVISOES_RAIZ_083_20260910'
J1 = ROOT / 'CANDIDATO_DERIVADA_WEYL_083_20260910'
COMBO = ROOT / 'COMBINACAO_TT_E_FALHA_ISOTROPIA_083_20260910'
ROOT_RECORD = REVIEWS / 'REGISTRO_RAIZ_J1_E_COMBINACAO_083.json'
NARRATIVES = [DELIVERY / x for x in ['REEXAME_SUFICIENCIA.md',
              'MEMORIA_DE_TRABALHO_083.md', 'DESENHO_DO_FECHAMENTO_ADENDO_083.md']]

def pin(path):
    p = Path(path).resolve()
    if not p.is_relative_to(ROOT):
        raise RuntimeError('Original read prohibited in this review: ' + str(p))
    raw = p.read_bytes()
    return {'path': str(p), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def load(path):
    pin(path)
    return json.loads(Path(path).read_bytes())

def same(actual, expected):
    return actual['bytes'] == expected['bytes'] and actual['sha256'] == expected['sha256']

def new_json(path, obj):
    if not path.resolve().is_relative_to(ROOT) or path.exists():
        raise RuntimeError('New files under Chatgpt only')
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temp = path.with_name(path.name + '.pending')
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.read_bytes() != raw:
        raise RuntimeError('Byte mismatch')
    temp.rename(path)
    return pin(path)

sources = NARRATIVES + [DELIVERY / x for x in ['ESTADO_CANONICO_083.json',
    'PROVENIENCIA_AUXILIARES_083.json', 'capture_current083.py', 'finalize_delivery083.py']]
sources += [REVIEWS / 'PARECER_J1_E_FALHA_DA_COMBINACAO_083.md', ROOT_RECORD,
    ROOT / 'REEXAME_SUFICIENCIA_082_20260910/ESTADO_CANONICO_082.json',
    J1 / 'MANIFESTO_CANDIDATO_DERIVADO_083.json',
    COMBO / 'MANIFESTO_COMBINACAO_E_FALHA_083.json',
    ROOT / 'REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/RECIBO_REVISAO_J1_083.json',
    ROOT / 'REVISAO_COMBINACAO_ISOTROPIA_083_20260910_054522_9585399/RECIBO_REVISAO_COMBINACAO_083.json']
sources += [Path(item['path']) for item in load(ROOT_RECORD)['sources_before']]
sources = list(dict.fromkeys(p.resolve() for p in sources))
before_path = HERE / 'PINS_ANTES_DOCUMENTOS_083.json'

if sys.argv[1] == 'capture':
    before = {'created_utc': datetime.now(timezone.utc).isoformat(),
              'sources_before': [pin(p) for p in sources], 'helper_before': pin(__file__),
              'no_originals_read': True}
    print(json.dumps(new_json(before_path, before), ensure_ascii=False))
elif sys.argv[1] == 'finalize':
    before = load(before_path)
    checks = []
    external_records = []
    measured = {}
    def check(name, value):
        checks.append({'name': name, 'passed': bool(value), 'kind': 'DOCUMENTARY'})
    def verify(value, origin):
        if isinstance(value, dict):
            if isinstance(value.get('path'), str) and re.fullmatch('[0-9a-f]{64}', str(value.get('sha256', ''))):
                p = Path(value['path']).resolve()
                if not p.is_relative_to(ROOT):
                    external_records.append({'origin': origin, 'record': value,
                                             'action': 'NOT_REOPENED; compared only through stored snapshots'})
                else:
                    actual = pin(p)
                    measured[str(p)] = actual
                    check('recorded_pin:' + origin, same(actual, value))
            for key, child in value.items():
                verify(child, origin + '.' + key)
        elif isinstance(value, list):
            for i, child in enumerate(value):
                verify(child, origin + '[' + str(i) + ']')
    for i, old in enumerate(before['sources_before']):
        check('source_unchanged_' + str(i), old == pin(old['path']))
    check('helper_unchanged', before['helper_before'] == pin(__file__))
    for source in sources:
        if source.suffix == '.json':
            verify(load(source), source.name)
    cap = load(DELIVERY / 'ESTADO_CANONICO_083.json')
    prior = load(ROOT / 'REEXAME_SUFICIENCIA_082_20260910/ESTADO_CANONICO_082.json')
    check('capture_embedded_683', cap['embedded_files'] == 683)
    check('capture_98_unique_modules', len(cap['modules']) == len({m['module'] for m in cap['modules']}) == 98)
    check('capture_77_present', sum(m['present'] for m in cap['modules']) == cap['present'] == 77)
    check('capture_21_absent', [m['module'] for m in cap['modules'] if not m['present']] == cap['absent'] and len(cap['absent']) == 21)
    old_external = {p['path']: p for p in prior['pins'] if not Path(p['path']).resolve().is_relative_to(ROOT)}
    current_external = {p['path']: p for p in cap['pins'] if not Path(p['path']).resolve().is_relative_to(ROOT)}
    check('four_canonical_pins_equal_stored082', len(current_external) == 4 and current_external == old_external)
    check('four_capture_comparisons_true', len(cap['comparison_with_delivery082']) == 4 and all(x['unchanged'] for x in cap['comparison_with_delivery082']))
    check('presence_same_as082', cap['modules'] == prior['modules'] and cap['embedded_files'] == prior['embedded_files'])
    check('snapshot_records_stability_and_seal', cap['status'] == 'READ_ONLY_STABLE_SNAPSHOT' and cap['seal_um_hash_matches'] and cap['all_read_sources_unchanged'])
    check('snapshot_records_no_execution_or_write', cap['um_executed_or_imported'] is False and cap['originals_written'] is False)
    check('uv_wall_open_in_record', 'OPEN' in cap['seal_excerpt']['renormalization_wall_verdict'])
    provenance = load(DELIVERY / 'PROVENIENCIA_AUXILIARES_083.json')
    for i, row in enumerate(provenance['records']):
        p = Path(row['source_before']['path']).resolve()
        check('helper_source_within_Chatgpt_' + str(i), p.is_relative_to(ROOT))
        raw = p.read_bytes()
        for j, change in enumerate(row['changes']):
            old, new = change['old'].encode(), change['new'].encode()
            check('helper_replacement_count_' + str(i) + '_' + str(j), raw.count(old) == change['count'])
            raw = raw.replace(old, new)
        check('helper_copy_exact_' + str(i), raw == Path(row['target']['path']).read_bytes())
    math_record = load(J1 / 'CONTROLE_COVARIANTE_J1_083.json')
    check('ten_recorded_algebraic_predicates_true', len(math_record['checks']) == 10 and all(v is True for v in math_record['checks'].values()))
    code = (J1 / 'compute_covariant_j1_new.py').read_text(encoding='utf-8')
    check('one_combined_integrity_guard', code.count('if before!=after or self_before!=self_after:') == 1)
    check('two_recorded_integrity_equalities_true', math_record['all_sources_unchanged'] is True and math_record['script_unchanged'] is True)
    check('three_math_sources_and_self_pinned', len(math_record['sources_before']) == 3 and math_record['sources_before'] == math_record['sources_after'] and math_record['script_before'] == math_record['script_after'])
    for narrative in NARRATIVES:
        content = narrative.read_text(encoding='utf-8')
        check('explicit084_exclusion:' + narrative.name, '084' in content and 'excluíd' in content)
        for i, target in enumerate(re.findall(r'\]\(<([A-Za-z]:/[^>]+)>\)', content)):
            p = Path(re.sub(r':\d+$', '', target)).resolve()
            check('local_link:' + narrative.name + ':' + str(i), p.is_relative_to(ROOT) and p.is_file())
    final = HERE / 'PARECER_RELATORIO_083.md'
    draft = final.with_name(final.name + '.pending')
    raw = draft.read_bytes()
    check('review_utf8_nonempty', len(raw) > 4000 and '\x00' not in raw.decode('utf-8'))
    for key, item in measured.items():
        check('referenced_local_pin_preserved:' + key, pin(key) == item)
    if not all(c['passed'] for c in checks):
        raise RuntimeError(json.dumps([c for c in checks if not c['passed']], ensure_ascii=False))
    if final.exists():
        raise RuntimeError('Final exists')
    draft.rename(final)
    after = [pin(p) for p in sources]
    check('all_main_sources_preserved_after_publication', after == before['sources_before'])
    result = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'PASS_DOCUMENTARY_CONSISTENCY_ONLY_NOT_NEW_MATHEMATICAL_REVIEW',
        'sources_before': before['sources_before'], 'sources_after': after,
        'all_sources_unchanged': after == before['sources_before'],
        'local_referenced_pins': list(measured.values()),
        'canonical_records_not_reopened': external_records,
        'artifacts': [pin(final), pin(before_path), pin(__file__)],
        'checks': checks, 'passed': sum(c['passed'] for c in checks), 'total': len(checks),
        'all_checks_documentary': True, 'originals_reopened': False,
        'mathematical_reruns': 0, 'new_lean_runs': 0, 'um_py_executed_or_imported': False,
        'existing_files_modified': False, 'external_approval_attributed': False,
        'prior_own_mathematical_reviews': 'Separate antecedents, not approved again by this documentary check',
        'source_counts': {'algebraic_predicates': 10, 'combined_integrity_guard': 1, 'recorded_integrity_equalities': 2},
        'scope': 'Three narratives083, stored capture/provenance and root review; excludes084 and final delivery publication'
    }
    receipt = new_json(HERE / 'RECIBO_REVISAO_DOCUMENTAL_083.json', result)
    print(json.dumps({'review': pin(final), 'receipt': receipt, 'checks': str(result['passed']) + '/' + str(result['total']),
                      'main_sources': len(after), 'local_referenced_pins': len(measured),
                      'canonical_record_occurrences_not_reopened': len(external_records)}, ensure_ascii=False))
else:
    raise RuntimeError('Unknown mode')
