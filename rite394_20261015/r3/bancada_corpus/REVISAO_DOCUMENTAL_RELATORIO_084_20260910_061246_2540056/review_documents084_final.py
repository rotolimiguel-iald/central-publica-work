from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
HERE = Path(__file__).resolve().parent
BASE = ROOT / 'REEXAME_SUFICIENCIA_084_20260910'
RELATIVE = [
 'REEXAME_SUFICIENCIA_084_20260910/REEXAME_SUFICIENCIA.md',
 'REEXAME_SUFICIENCIA_084_20260910/MEMORIA_DE_TRABALHO_084.md',
 'REEXAME_SUFICIENCIA_084_20260910/DESENHO_DO_FECHAMENTO_ADENDO_084.md',
 'REEXAME_SUFICIENCIA_084_20260910/ESTADO_CANONICO_084.json',
 'REEXAME_SUFICIENCIA_084_20260910/PROVENIENCIA_HELPERS_084.json',
 'REEXAME_SUFICIENCIA_084_20260910/capture_current084.py',
 'REEXAME_SUFICIENCIA_084_20260910/finalize_delivery084.py',
 'REVISOES_RAIZ_084_20260910/PARECER_FORMA_NORMAL_E_CANAL_EULER_084.md',
 'REVISOES_RAIZ_084_20260910/REGISTRO_REVISAO_RAIZ_084.json',
 'REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md',
 'REDUCAO_ISOTROPIA_CE_084_20260910/MANIFESTO_REDUCAO_ISOTROPIA_084.json',
 'REVISAO_REDUCAO_ISOTROPIA_084_20260910/PARECER_ELIMINACAO_FINITA_E_CANAL_EULER_084.md',
 'REVISAO_REDUCAO_ISOTROPIA_084_20260910/REGISTRO_REVISAO_REDUCAO_ISOTROPIA_084.json',
 'REVISAO_REDUCAO_ISOTROPIA_084_20260910/PROVENIENCIA_EMISSOR_PORTAVEL_084.json',
 'CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md',
 'CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/MANIFESTO_CORRENTE_NECESSARIA_084.json',
 'REVISAO_CORRENTE_NECESSARIA_084_20260910_061100_677142/PARECER_EULER_E_GRADIENTE_084.md',
 'REVISAO_CORRENTE_NECESSARIA_084_20260910_061100_677142/REGISTRO_REVISAO_EULER_E_GRADIENTE_084.json',
 'REEXAME_SUFICIENCIA_083_20260910/ESTADO_CANONICO_083.json',
 'REEXAME_SUFICIENCIA_083_20260910/capture_current083.py',
 'REEXAME_SUFICIENCIA_083_20260910/finalize_delivery083.py',
 'CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md',
 'REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md',
 'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md',
 'OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md',
 'COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md',
]
SOURCES = [ROOT / s for s in RELATIVE]

def pin(path):
    p = Path(path).resolve()
    assert p.is_relative_to(ROOT), 'Never reopen canonical originals'
    raw = p.read_bytes()
    return {'path': p.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def new_json(path, value):
    assert path.resolve().is_relative_to(HERE) and not path.exists()
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_name(path.name + '.pending')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    return pin(path)

before_path = HERE / 'PINS_ANTES_DOCUMENTOS_084.json'
if sys.argv[1] == 'capture':
    value = {'created_utc': datetime.now(timezone.utc).isoformat(),
             'measurement_scope': 'Initial measurement after orientation reading, before new review publication',
             'sources_before': [pin(p) for p in SOURCES], 'helper_before': pin(__file__)}
    print(json.dumps(new_json(before_path, value), ensure_ascii=False))
    raise SystemExit(0)
assert sys.argv[1] == 'finalize'
before = json.loads(before_path.read_bytes())
checks = []
linked = {}
records = {}
canonical_occurrences = []

def check(name, condition, detail=None):
    row = {'name': name, 'passed': bool(condition), 'kind': 'DOCUMENTARY'}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)

snapshot = json.loads((BASE / 'ESTADO_CANONICO_084.json').read_bytes())
prior = json.loads((ROOT / RELATIVE[18]).read_bytes())
prior_canonical = {Path(p['path']).as_posix(): p for p in prior['pins']
                   if not Path(p['path']).resolve().is_relative_to(ROOT)}

def walk(value, origin):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and re.fullmatch('[0-9a-f]{64}', str(value.get('sha256', ''))):
            p = Path(value['path']).resolve()
            if p.is_relative_to(ROOT):
                actual = pin(p)
                records[actual['path']] = actual
                check('recorded_pin:' + origin, actual['sha256'] == value['sha256'] and
                      ('bytes' not in value or actual['bytes'] == value['bytes']), actual['path'])
            else:
                key = p.as_posix()
                old = prior_canonical.get(key)
                check('canonical_pin_JSON_only:' + origin, old is not None and
                      old['sha256'] == value['sha256'] and old['bytes'] == value['bytes'], key)
                canonical_occurrences.append({'origin': origin, 'record': value,
                                              'scope': 'Compared to stored083 JSON; original not reopened'})
        for k, child in value.items():
            walk(child, origin + '.' + k)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            walk(child, origin + '[' + str(i) + ']')

for path in SOURCES:
    if path.suffix == '.json':
        obj = json.loads(path.read_bytes())
        walk(obj, path.name)
        if 'checks' in obj:
            seq = obj['checks']
            total = obj.get('checks_total', obj.get('total', len(seq)))
            passed = obj.get('checks_passed', obj.get('passed', sum(bool(c.get('passed')) for c in seq)))
            check('receipt_count:' + path.name, total == len(seq) and passed == sum(bool(c.get('passed')) for c in seq))
            check('receipt_no_failed_checks:' + path.name, all(c.get('passed') for c in seq))
    elif path.suffix == '.md':
        for i, target in enumerate(re.findall(r'\]\(<([A-Za-z]:/[^>]+)>\)', path.read_text(encoding='utf-8-sig'))):
            match = re.match(r'^(.*?)(?::(\d+))?$', target)
            p = Path(match.group(1)).resolve()
            check('local_link:' + path.name + ':' + str(i), p.is_relative_to(ROOT) and p.is_file(), target)
            if p.is_file() and p.is_relative_to(ROOT):
                linked[p.as_posix()] = pin(p)
                if match.group(2):
                    check('link_line:' + path.name + ':' + str(i), 1 <= int(match.group(2)) <= len(p.read_bytes().splitlines()), target)

modules = snapshot['modules']
names = [v['module'] for v in modules]
check('snapshot_98_unique_modules', len(names) == len(set(names)) == 98)
check('snapshot_77_presence', sum(v['present'] for v in modules) == snapshot['present'] == 77)
check('snapshot_21_absence', [v['module'] for v in modules if not v['present']] == snapshot['absent'] and len(snapshot['absent']) == 21)
check('snapshot_683_embedded', snapshot['embedded_files'] == 683)
check('snapshot_four_unchanged', len(snapshot['comparison_with_delivery083']) == 4 and all(v['unchanged'] for v in snapshot['comparison_with_delivery083']))
check('snapshot_stability_and_seal', snapshot['status'] == 'READ_ONLY_STABLE_SNAPSHOT' and snapshot['all_read_sources_unchanged'] and snapshot['seal_um_hash_matches'])
check('snapshot_no_execution_writes', snapshot['um_executed_or_imported'] is False and snapshot['originals_written'] is False)
report = (BASE / 'REEXAME_SUFICIENCIA.md').read_text(encoding='utf-8-sig')
for name, text in snapshot['seal_excerpt'].items():
    check('report_seal_literal:' + name, text in report)
um_pin = next(p for p in snapshot['pins'] if p['path'].endswith('/Nós/um.py'))
check('report_um_bytes_hash', str(um_pin['bytes']) in report and um_pin['sha256'] in report)
for filename in ('capture_current', 'finalize_delivery'):
    old = (ROOT / ('REEXAME_SUFICIENCIA_083_20260910/' + filename + '083.py')).read_bytes()
    new = (BASE / (filename + '084.py')).read_bytes()
    adapted = old.replace(b'083', b'084').replace(b'082', b'083')
    if filename == 'finalize_delivery':
        # The new delivery has zero mathematical and combined integrity controls.
        adapted = adapted.replace(b"== 10", b"== 0").replace(b"== 1", b"== 0")
        adapted = adapted.replace(b'derivadas_Weyl_e_limite_do_detector', b'criterio_da_corrente_e_canal_Euler')
    check('helper_provenance_adaptation:' + filename, new == adapted)

for old in before['sources_before']:
    check('source_preserved:' + old['path'], pin(old['path']) == old)
check('review_capture_helper_preserved', pin(HERE / 'review_documents084.py') == before['helper_before'])

pending = HERE / 'PARECER_RELATORIO_084.md.pending'
raw = pending.read_bytes()
review = raw.decode('utf-8')
check('review_utf8_nonempty', len(raw) > 5000 and '\x00' not in review)
for i, target in enumerate(re.findall(r'\]\(<([A-Za-z]:/[^>]+)>\)', review)):
    p = Path(re.sub(r':\d+$', '', target)).resolve()
    check('review_local_link:' + str(i), p.is_relative_to(ROOT) and p.is_file(), target)
assert all(c['passed'] for c in checks), [c for c in checks if not c['passed']]
final = HERE / 'PARECER_RELATORIO_084.md'
assert not final.exists()
pending.rename(final)
after = [pin(p) for p in SOURCES]
check('preserved_after_review_publication', after == before['sources_before'])
assert all(c['passed'] for c in checks)
receipt = {
 'created_utc': datetime.now(timezone.utc).isoformat(),
 'status': 'PASS_DOCUMENTARY_REVIEW_084_DECLARED_SCOPE',
 'sources_before': before['sources_before'], 'sources_after': after,
 'all_sources_unchanged': after == before['sources_before'],
 'recorded_local_pins_verified': list(records.values()),
 'linked_local_files': list(linked.values()),
 'canonical_pin_occurrences_compared_as_JSON_only': canonical_occurrences,
 'checks': checks, 'checks_total': len(checks), 'checks_passed': sum(c['passed'] for c in checks),
 'review': pin(final), 'helper': pin(__file__), 'initial_capture': pin(before_path),
 'new_mathematical_executions': 0, 'new_CAS_runs': 0, 'new_lean_compilations': 0,
 'um_executed_or_imported': False, 'canonical_originals_reopened': False,
 'previous_files_modified': False,
 'scope': 'Documentary consistency of084 narratives, stored snapshot, mathematical sources and distinct reviews; no new approval of mathematics authored earlier;085 and sister-session inspection excluded',
 'not_attested': ['Final delivery084 manifest/result/tunnel completion', 'Fresh canonical state after stored084 snapshot', 'Universal reconstruction, causal QME or UV'],
 'material_documentary_defects': []
}
result = new_json(HERE / 'RECIBO_REVISAO_DOCUMENTAL_084.json', receipt)
print(json.dumps({'review': pin(final), 'receipt': result, 'checks': str(receipt['checks_passed']) + '/' + str(len(checks)), 'sources': len(SOURCES), 'unique_recorded_local_pins': len(records), 'canonical_occurrences_JSON_only': len(canonical_occurrences)}, ensure_ascii=False))
