"""Validate completed attempt 02 and preserve its actual outputs before repairs."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import re
import shutil

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'r'
ARCHIVE = RUN / 'completed_attempt_02'

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def read(name):
    return json.loads((RUN / name).read_bytes())

state = read('runtime_process_02.json')
assert state['status'] == 'PROCESS_EXITED' and state['returncode'] == 0
assert state['working_sha256'] == state['program_sha256_after'] == sha(RUN/'um.py') == sha(ROOT/'um.py')
data = read('um_absoluto.json')
seal = read('um_absoluto_selo.json')
manifest = read('tgl_kernel_proof_manifest.json')
kernel = data['core']['kernel_formalization']
assert kernel['all_verified'] is True and kernel['formal_release_ready'] is True
assert seal['fail_closed_selftest'] == 'FAIL_CLOSED_SELFTEST_PASSED'
assert seal['rite_checkpoints']['switch_on'] is False and seal['rite_checkpoints']['reused'] == 0
assert seal['qg_closure_verdict'] == data['core']['qg_closure']['gate']['verdict']
assert seal['result_hash'] == data['result_hash_before_external_comparison']
assert seal['identity'] == data['verdict']['IDENTITY']
gate = {k:v for k,v in kernel.items() if k.startswith(('qgc_', 'qgp_'))}
assert len(gate) == 11 and all(value is True for value in gate.values())
sealed_files = {name: sha(RUN/name) for name in seal['sha256']}
assert sealed_files == seal['sha256'] and len(sealed_files) == 13
formal_files = {name: sha(RUN/'tgl_kernel'/name) for name in manifest['formal_files_sha256']}
assert formal_files == manifest['formal_files_sha256'] and len(formal_files) == 922
axioms = manifest['axiom_report']
assert axioms == kernel['axiom_report']
assert all(set(value) <= {'propext','Classical.choice','Quot.sound'} for value in axioms.values())
def capture(stage, kind):
    return (RUN/f'tgl_kernel_{kind}_capture{stage}.txt').read_text(encoding='utf-8')

def parse_axioms(blob):
    result = {}
    for match in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", blob, re.S):
        name, raw_values = match.groups()
        values = [value.strip() for value in raw_values.replace('\n',' ').split(',') if value.strip()]
        if name in result:
            assert result[name] == values
        result[name] = values
    for match in re.finditer(r"'([\w.']+)' does not depend on any axioms", blob):
        name = match.group(1)
        assert name not in result or result[name] == []
        result[name] = []
    return result

principal_audit = parse_axioms(capture('', 'audit'))
principal_all = parse_axioms(capture('', 'build') + capture('', 'audit'))
assert len(principal_audit) == 7133 and principal_all == axioms
restored = capture('_selftest_restored', 'build') + capture('_selftest_restored', 'audit')
restored_axioms = parse_axioms(restored)
assert restored_axioms == axioms
tampered = (RUN/'tgl_kernel_audit_capture_selftest_tampered.txt').read_text(encoding='utf-8')
assert 'sorryAx' in tampered and 'sorryAx' not in restored
baseline = json.loads((ROOT/'fontes/um_absoluto_selo.json').read_bytes())
new_unsealed = {key: sorted(set(values) - set(baseline['not_sealed_this_run'].get(key, [])))
                for key, values in seal['not_sealed_this_run'].items()}
assert not ARCHIVE.exists(), 'Archive must never overwrite an earlier run'
ARCHIVE.mkdir()
files = sorted(path for path in RUN.iterdir() if path.is_file())
copied = {}
for source in files:
    target = ARCHIVE/source.name
    original_hash = sha(source)
    shutil.copyfile(source, target)
    assert sha(target) == sha(source) == original_hash
    copied[source.name] = dict(bytes=target.stat().st_size, sha256=original_hash)
result = dict(timestamp=datetime.now().astimezone().isoformat(),
              status='FULL_RUNTIME_EXITED_ZERO_SELFTEST_PASSED__AUXILIARY_INTEGRATION_REPAIRS_PENDING',
              process=state, gate=gate, gate_verdict=seal['qg_closure_verdict'],
              selftest=seal['fail_closed_selftest'], rite_checkpoints=seal['rite_checkpoints'],
              sealed_file_hashes_verified=sealed_files, formal_source_files_verified=len(formal_files),
              restored_axiom_terms_verified=len(restored_axioms),
              principal_audit_terms_verified=len(principal_audit),
              report_terms_from_build_and_audit=len(axioms),
              author_check_correction='The report combines build and Audit output; 7133 refers only to Audit. No output changed.',
              result_hash_consistency_verified=True,
              result_hash_independently_reconstructed=False,
              new_unsealed_vs_baseline=new_unsealed, archive_files=copied,
              full_task_complete=False, new_mathematical_requirements=[])
raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
output=ARCHIVE/'verification.json';temporary=output.with_suffix('.tmp')
with temporary.open('xb') as stream:stream.write(raw)
assert temporary.read_bytes()==raw
os.replace(temporary,output)
print(json.dumps(dict(verified=True, archive=str(ARCHIVE), files=len(copied),
                     verification_sha256=sha(output), selftest=result['selftest'],
                     new_unsealed=new_unsealed),ensure_ascii=False))
