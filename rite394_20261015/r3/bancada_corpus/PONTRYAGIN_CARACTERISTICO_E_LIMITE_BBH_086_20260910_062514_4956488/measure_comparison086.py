from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
HERE = Path(__file__).resolve().parent
SOURCES = [
 ROOT / 'REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md',
 ROOT / 'INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md',
 ROOT / 'COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md',
 ROOT / 'COMPLETAMENTO_GL_ORTOGONAL_079_20260910/CORRENTE_QUADRATICA_E_EQUIVALENCIA_DAS_CONEXOES.md',
 ROOT / 'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md',
 ROOT / 'CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md',
 ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md',
]

def pin(path):
    p = Path(path).resolve()
    assert p.is_relative_to(ROOT)
    data = p.read_bytes()
    return {'path': p.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def new_json(path, value):
    assert not path.exists() and path.resolve().is_relative_to(HERE)
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_name(path.name + '.pending')
    with tmp.open('xb') as stream:
        stream.write(data)
    assert tmp.read_bytes() == data
    tmp.rename(path)
    return pin(path)

before_path = HERE / 'PINS_ANTES_COMPARACAO_086.json'
if sys.argv[1] == 'capture':
    print(json.dumps(new_json(before_path, {'created_utc': datetime.now(timezone.utc).isoformat(),
        'sources_before': [pin(p) for p in SOURCES], 'helper_before': pin(__file__)}), ensure_ascii=False))
    raise SystemExit(0)
assert sys.argv[1] == 'finalize'
before = json.loads(before_path.read_bytes())
checks = []
def check(name, condition):
    checks.append({'name': name, 'passed': bool(condition), 'kind': 'DOCUMENTARY'})
for i, old in enumerate(before['sources_before']):
    check('source_preserved_' + str(i), pin(old['path']) == old)
check('helper_preserved', pin(__file__) == before['helper_before'])
final = HERE / 'NAO_EXATIDAO_INVARIANTE_E_LIMITE_DA_IMPORTACAO_BBH.md'
draft = final.with_name(final.name + '.pending')
raw = draft.read_bytes()
text = raw.decode('utf-8')
check('new_note_utf8_nonempty', len(raw) > 9000 and '\x00' not in text)
for i, target in enumerate(re.findall(r'\]\(<([A-Za-z]:/[^>]+)>\)', text)):
    p = Path(re.sub(r':\d+$', '', target)).resolve()
    check('local_link_' + str(i), p.is_relative_to(ROOT) and p.is_file())
assert all(c['passed'] for c in checks), checks
assert not final.exists()
draft.rename(final)
after = [pin(p) for p in SOURCES]
check('sources_preserved_after_publication', after == before['sources_before'])
assert all(c['passed'] for c in checks)
value = {
 'created_utc': datetime.now(timezone.utc).isoformat(),
 'status': 'DERIVED_COMPARISON_AND_EXPLICIT_ORDINARY_TRANSGRESSION__INVARIANT_TOP_DEGREE_OPEN',
 'sources_before': before['sources_before'], 'sources_after': after,
 'all_sources_unchanged': after == before['sources_before'],
 'artifacts': [pin(final), pin(before_path), pin(__file__)],
 'primary_sources_read': [
  {'url': 'https://arxiv.org/pdf/hep-th/9505173v2', 'scope': 'Theorem7.1(ii), eq7.32-7.33, Theorem7.2, sec8 eq8.1-8.10, sec9 eq9.8-9.9; top-degree nontriviality is an extra assumption'},
  {'url': 'https://arxiv.org/pdf/hep-th/0504169', 'observed_version': 'v2 25Apr2005', 'scope': 'Introduction eq1.7 and1.14; AppendixA.2 flat linearized covariant Poincare lemma; no curved on-shell theorem imported'},
  {'url': 'https://arxiv.org/pdf/1205.3293', 'scope': 'Theorem15 eq5.73-5.74 and sec7.3 eq7.42; distinguish strong linear tensor-form theorem from characteristic on-shell top degree'}
 ],
 'web_retrieval_limits': 'Direct versioned URLs for0504169v2 and1205.3293v1 returned cache-miss errors; unversioned arXiv PDF retrieval succeeded and was read. No failed retrieval is a cited proof.',
 'checks': checks, 'checks_total': len(checks), 'checks_passed': sum(c['passed'] for c in checks),
 'new_mathematical_executions': 0, 'new_lean_compilations': 0, 'new_CAS_runs': 0,
 'um_executed_or_imported': False, 'existing_files_modified': False,
 'scope': 'Explicit finite GL transgression, gauge-variation distinction, exact connecting-homomorphism criterion and two algebraic non-transfer counterexamples; does not decide whether J is a natural Weyl/EOM divergence',
 'stage085_modified_or_retroactively_extended': False,
 'external_review_attributed': False
}
result = new_json(HERE / 'MANIFESTO_COMPARACAO_CARACTERISTICA_086.json', value)
print(json.dumps({'note': pin(final), 'manifest': result, 'documentary_checks': str(value['checks_passed']) + '/' + str(value['checks_total'])}, ensure_ascii=False))
