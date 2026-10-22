"""Read source bytes and create a new manifest; never execute source scripts."""
from pathlib import Path
import datetime
import hashlib
import json
import os

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
HEAT = ROOT / 'CALOR_COMPLETO_EINSTEIN_SIGMA_069_20260909_224252_371553'

def pin(path):
    raw = path.read_bytes()
    return {'path': str(path.resolve()), 'bytes': len(raw),
            'lines': len(raw.decode('utf-8-sig').splitlines()),
            'sha256': hashlib.sha256(raw).hexdigest()}

inputs = [
    HEAT / 'COEFICIENTE_COMPLETO_UMA_VOLTA.md',
    ROOT / 'QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633' / 'OPERADOR_JACOBI_GAUGE_E_ESCOPO.md',
    HEAT / 'VERIFICACAO_CALOR_COMPLETO.json',
    HEAT / 'verify_complete_heat.py',
]
before = [pin(path) for path in inputs]
receipt = json.loads(inputs[2].read_text(encoding='utf-8'))
assert before[3]['sha256'] == receipt['script']['sha256'], 'Receipt/script mismatch.'
artifacts = [BASE / 'PARECER_OPERADOR_E_COEFICIENTE.md', Path(__file__).resolve()]
data = {
    'created_local': datetime.datetime.now().astimezone().isoformat(),
    'review_status': 'DERIVED: own written operator/trace comparison; no material error found in the specified on-shell differential scope.',
    'source_pins': before,
    'artifact_pins': [pin(path) for path in artifacts],
    'receipt_status_read': receipt['status'],
    'receipt_count_read': receipt['check_count'],
    'receipt_checks_all_recorded_true': all(item['passed'] for item in receipt['checks']),
    'receipt_script_sha256_matches_actual_bytes': True,
    'primary_source': {
        'url': 'https://arxiv.org/html/hep-th/0306138v3',
        'title': 'Heat kernel expansion: users manual',
        'version_date': '2003-09-06',
        'consulted': 'Equation 4.28; no downloaded PDF hash claimed.',
    },
    'CAS_executed_in_this_review': False,
    'heat_script_executed_in_this_review': False,
    'um_executed_or_imported': False,
    'lean_executed': False,
    'original_files_written': [],
    'non_absorption_review_reopened': False,
    'limits': ['on-shell operator', 'normalized differential contribution', 'no full measure or off-shell extension', 'no global heat kernel or Wick rotation claim', 'no interacting QME or UV conclusion'],
}
assert before == [pin(path) for path in inputs], 'An input changed during measurement.'
data['inputs_unchanged_during_measurement'] = True
raw = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
target = BASE / 'MANIFESTO_REVISAO_ELO_CALOR.json'
temp = BASE / 'MANIFESTO_REVISAO_ELO_CALOR.json.new'
assert not target.exists() and not temp.exists()
with temp.open('xb') as stream:
    stream.write(raw)
assert temp.read_bytes() == raw and len(raw) > 1000
os.rename(temp, target)
print(json.dumps({'manifest': pin(target), 'review': pin(artifacts[0]), 'receipt_count': receipt['check_count'], 'source_script_hash_matches': True}, ensure_ascii=False, indent=2))
