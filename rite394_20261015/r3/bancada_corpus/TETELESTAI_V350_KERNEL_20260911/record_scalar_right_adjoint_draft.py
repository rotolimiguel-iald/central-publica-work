"""Pin the additional maximal-adjoint lemma, without changing the frozen batch."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
name = 'ScalarRightTomitaAdjoint'
source = ROOT / 'kernel/TGLV350' / (name + '.lean')
binary = ROOT / 'build/TGLV350' / (name + '.olean')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

accepted = []
for path in sorted((ROOT / 'logs').glob(name + '_*.json')):
    row = json.loads(path.read_bytes())
    if (row['returncode'] == 0 and row['source_unchanged_during_compile']
            and row['sha256'] == sha(source) and row['output_sha256'] == sha(binary)):
        accepted.append((path, row))
assert accepted
log, row = accepted[-1]
stdout, stderr = Path(row['stdout']), Path(row['stderr'])
text = stdout.read_text(encoding='utf-8')
assert stderr.read_bytes() == b''
targets = {}
for short in re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M):
    full = 'TGLV350.Regular.' + short
    match = re.search(re.escape("'" + full + "' depends on axioms: [") + r'([^]]*)\]', text)
    assert match, full
    axioms = sorted(s.strip() for s in match.group(1).split(',') if s.strip())
    assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
    targets[full] = axioms
assert len(targets) == 5
parent = ROOT / 'scalar_right_tomita_draft_status.json'
memory = ROOT / 'scalar_right_tomita_draft_memory.json'
out = ROOT / 'scalar_right_adjoint_draft_status.json'
assert not out.exists()
data = {'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'module': name, 'source_sha256': sha(source), 'binary_sha256': sha(binary),
    'log_path': str(log), 'log_sha256': sha(log),
    'stdout_sha256': sha(stdout), 'stderr_sha256': sha(stderr), 'targets': targets,
    'parent_draft_sha256': sha(parent), 'parent_memory_sha256': sha(memory),
    'working_sha256': sha(ROOT / 'um.py'),
    'statement': 'pi(y) D(Sdagger) subset D(Sdagger); Sdagger pi(y) z = R_y* Sdagger z',
    'same_maximal_adjoint': True, 'KMS_proved': False,
    'independent_review_complete': False, 'integrated': False, 'gate_changed': False,
    'memory_update_pending_review_in_this_turn': True}
raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
temp = out.with_suffix('.json.tmp')
with temp.open('xb') as stream:
    stream.write(raw)
assert temp.read_bytes() == raw
temp.replace(out)
assert out.read_bytes() == raw
print(json.dumps({'module': name, 'targets': len(targets), 'manifest_sha256': sha(out)}))
