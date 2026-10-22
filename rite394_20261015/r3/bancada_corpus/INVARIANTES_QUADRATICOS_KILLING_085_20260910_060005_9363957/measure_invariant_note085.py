from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
HERE = Path(__file__).resolve().parent
SOURCES = [
    ROOT / 'GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md',
    ROOT / 'COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md',
    ROOT / 'SUBSETOR_ANTIFIELD_PURO_079_20260910_041018_659161/ANTIFIELD_PURO_FATORACAO_BIANCHI_E_DELTA.md',
    ROOT / 'PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md',
    ROOT / 'COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md',
    ROOT / 'REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md',
    ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md',
    ROOT / 'REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md',
]

def pin(path):
    p = Path(path).resolve()
    if not p.is_relative_to(ROOT):
        raise RuntimeError('Only Chatgpt sources')
    raw = p.read_bytes()
    return {'path': str(p), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def new_json(path, obj):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    tmp = path.with_name(path.name + '.pending')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    return pin(path)

before_path = HERE / 'PINS_ANTES_INVARIANTES_085.json'
if sys.argv[1] == 'capture':
    obj = {'created_utc': datetime.now(timezone.utc).isoformat(),
           'sources_before': [pin(p) for p in SOURCES], 'helper_before': pin(__file__)}
    print(json.dumps(new_json(before_path, obj), ensure_ascii=False))
elif sys.argv[1] == 'finalize':
    before = json.loads(before_path.read_bytes())
    checks = []
    def check(name, value):
        checks.append({'name': name, 'passed': bool(value), 'kind': 'DOCUMENTARY'})
    for i, old in enumerate(before['sources_before']):
        check('source_unchanged_' + str(i), pin(old['path']) == old)
    check('helper_unchanged', pin(__file__) == before['helper_before'])
    final = HERE / 'N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md'
    draft = final.with_name(final.name + '.pending')
    raw = draft.read_bytes()
    text = raw.decode('utf-8')
    check('new_note_utf8_nonempty', len(raw) > 10000 and '\x00' not in text)
    for i, target in enumerate(re.findall(r'\]\(<([A-Za-z]:/[^>]+)>\)', text)):
        path = Path(re.sub(r':\d+$', '', target)).resolve()
        check('local_link_' + str(i), path.is_relative_to(ROOT) and path.is_file())
    assert all(c['passed'] for c in checks), checks
    assert not final.exists()
    draft.rename(final)
    after = [pin(p) for p in SOURCES]
    check('sources_preserved_after_publication', after == before['sources_before'])
    obj = {
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'DERIVED_WRITTEN_085_AWAITING_SPECIFIC_INDEPENDENT_REVIEW',
        'sources_before': before['sources_before'], 'sources_after': after,
        'all_sources_unchanged': after == before['sources_before'],
        'artifacts': [pin(final), pin(before_path), pin(__file__)],
        'primary_sources_read': [{
            'url': 'https://arxiv.org/pdf/hep-th/0002245v3',
            'reference': 'BBH2000 Theorem6.2 eq6.17; Theorem6.5(i); Appendix6.B eqs6.44-6.49 and end of linear proof',
            'scope': 'Ordinary characteristic H0 from local acyclic KT for strictly linear irreducible Lagrangian system; no Whitehead'
        }],
        'checks': checks, 'passed': sum(c['passed'] for c in checks), 'total': len(checks),
        'all_checks_documentary': True, 'new_mathematical_executions': 0,
        'new_lean_runs': 0, 'um_py_executed_or_imported': False,
        'existing_files_modified': False, 'external_approval_attributed': False,
        'scope': 'N^g=0 in fixed-curvature scalar-extension finite-jet quadratic module; eliminates only Euler coefficient channel of084; no divergence solution or general QME',
        'custody_note': 'Only existing final paths pinned; no renamed temporary artifact referenced.'
    }
    receipt = new_json(HERE / 'MANIFESTO_INVARIANTES_QUADRATICOS_085.json', obj)
    print(json.dumps({'note': pin(final), 'manifest': receipt, 'documentary_checks': str(obj['passed']) + '/' + str(obj['total'])}, ensure_ascii=False))
else:
    raise RuntimeError('Unknown mode')
