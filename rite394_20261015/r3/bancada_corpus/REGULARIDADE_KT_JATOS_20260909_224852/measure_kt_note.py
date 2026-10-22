"""Read-only source measurements; create one new manifest beside this script."""
from pathlib import Path
import datetime
import hashlib
import json
import os

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent

def measure(path):
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    return {
        'path': str(path.resolve()),
        'bytes': len(raw),
        'lines': len(text.splitlines()),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'mtime_ns': path.stat().st_mtime_ns,
    }

inputs = [
    ROOT / 'CLASSES_CARACTERISTICAS_C0_20260909_221649' / 'EULER_PONTRYAGIN_ON_SHELL_E_LIMITE_C0.md',
    ROOT / 'BV_ANOMALIAS_SIGMA_FORMAL_20260909_215557' / 'BV_LOCAL_SIGMA_E_RENORMALIZACAO_CONDICIONAL.md',
]
artifacts = [BASE / 'CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md', Path(__file__).resolve()]
pins_before = [measure(path) for path in inputs]
payload = {
    'created_local': datetime.datetime.now().astimezone().isoformat(),
    'scope': 'Arco 069: regularidade de jatos formais, certificado polinomial e componente C0/KT.',
    'status_math': 'DERIVED: prova escrita; nenhuma compilacao Lean ou verificacao CAS nesta rodada.',
    'status_measurements': 'REAL: bytes, linhas, SHA256 e mtimes lidos dos arquivos.',
    'original_files_written': [],
    'um_py_imported_or_executed': False,
    'lean_executed': False,
    'sources': pins_before,
    'artifacts': [measure(path) for path in artifacts],
    'primary_web_sources': [
        {'url': 'https://arxiv.org/pdf/hep-th/0002245v3',
         'title': 'Local BRST cohomology in gauge theories',
         'version_date': '2000-11-13',
         'consulted': '5.1.3, Lemma 5.1, Theorem 5.1, 6.4.2-6.4.3',
         'pdf_sha256': None},
        {'url': 'https://arxiv.org/pdf/hep-th/9505173v2',
         'title': 'Local BRST cohomology in Einstein-Yang-Mills theory',
         'version_date': '1995-06-12',
         'consulted': '2 (2.11), 3, appendices C-E',
         'pdf_sha256': None},
        {'url': 'https://arxiv.org/pdf/1509.08269v2',
         'title': 'The Jet Isomorphism Theorem of Riemannian Geometry',
         'version_date': '2026-01-13',
         'consulted': '1, 2.2, Theorem 3; pseudo-Riemannian scope in opening paragraph',
         'pdf_sha256': None},
        {'url': 'https://arxiv.org/pdf/gr-qc/9404030v1',
         'title': 'Classification of Generalized Symmetries for the Vacuum Einstein Equations',
         'version_date': '1994-04-14',
         'consulted': '2C, Theorems 2.7-2.8; scope is Ricci-flat',
         'pdf_sha256': None},
    ],
    'web_source_custody': 'URLs/version dates read using web tool. PDFs were not downloaded; no PDF hash is claimed.',
    'precise_limits': [
        'Weak equality is on the formal stationary jet surface, not one ansatz or a physical data set.',
        'Coefficient ring is natural polynomial in differentiated jets and smooth in target-chart values.',
        'No denominator in metric components, scalar gradients, or curvature invariants.',
        'Full s modulo d classification, global target topology, and interacting QME are separate.',
        'BBH normality/relative cohomology filtration is not inferred just from H0/KT regularity.',
    ],
}
pins_after = [measure(path) for path in inputs]
assert pins_before == pins_after, 'A source changed during measurement.'
payload['sources_unchanged_during_measurement'] = True
target = BASE / 'MANIFESTO_REGULARIDADE_KT.json'
temp = BASE / 'MANIFESTO_REGULARIDADE_KT.json.new'
assert not target.exists() and not temp.exists(), 'Refusing to overwrite an existing file.'
raw = (json.dumps(payload, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
with temp.open('xb') as stream:
    stream.write(raw)
assert temp.read_bytes() == raw and len(raw) > 1000
os.rename(temp, target)
print(json.dumps({'manifest': measure(target), 'artifacts': payload['artifacts'], 'sources_unchanged': True}, ensure_ascii=False, indent=2))
