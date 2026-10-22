"""Measure existing inputs without executing them; create a new review manifest."""
from pathlib import Path
import hashlib
import json
import datetime
import os

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent

def pin(path):
    raw = path.read_bytes()
    return {'path': str(path.resolve()), 'bytes': len(raw),
            'lines': len(raw.decode('utf-8-sig').splitlines()),
            'sha256': hashlib.sha256(raw).hexdigest()}

heat = ROOT / 'CALOR_COMPLETO_EINSTEIN_SIGMA_069_20260909_224252_371553'
source = ROOT / 'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909' / 'TERMO_QUARTICO_NAO_ABSORVIDO.md'
receipt_path = heat / 'VERIFICACAO_CALOR_COMPLETO.json'
script_path = heat / 'verify_complete_heat.py'
inputs = [source, receipt_path, script_path]
before = [pin(p) for p in inputs]
receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
script_match = before[2]['sha256'] == receipt['script']['sha256']
assert script_match, 'Receipt/script mismatch.'
artifact = BASE / 'PARECER_PROPRIO_TERMO_QUARTICO.md'
data = {
    'created_local': datetime.datetime.now().astimezone().isoformat(),
    'review_status': 'DERIVED: own written review; no material error found within stated scope.',
    'measurements_status': 'REAL: bytes, lines and SHA256 read from disk.',
    'C4_status': 'INPUT: full coupled heat coefficient accepted for this bounded review; matrices not recomputed.',
    'source_pins': before,
    'receipt_declared_status': receipt['status'],
    'receipt_check_count': receipt['check_count'],
    'receipt_checks_all_recorded_true': all(c['passed'] for c in receipt['checks']),
    'receipt_script_hash_matches_disk': script_match,
    'artifact_pins': [pin(artifact), pin(Path(__file__).resolve())],
    'originals_written': [],
    'um_executed_or_imported': False,
    'lean_executed': False,
    'heat_script_executed_in_this_review': False,
    'independent_CAS_executed': False,
}
assert before == [pin(p) for p in inputs], 'An input changed during measurement.'
data['inputs_unchanged_during_measurement'] = True
raw = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
target = BASE / 'MANIFESTO_REVISAO_NAO_ABSORCAO.json'
temp = BASE / 'MANIFESTO_REVISAO_NAO_ABSORCAO.json.new'
assert not target.exists() and not temp.exists()
with temp.open('xb') as out:
    out.write(raw)
assert temp.read_bytes() == raw and len(raw) > 1000
os.rename(temp, target)
print(json.dumps({'manifest': pin(target), 'review': pin(artifact), 'receipt_script_hash_matches': script_match}, ensure_ascii=False, indent=2))
