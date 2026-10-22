"""Install reviewed edits into owned copies and transport four existing inputs."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import shutil
import sys

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'r'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
REVIEW=Path(sys.argv[1]).resolve()
assert REVIEW.is_relative_to((ROOT/'revisao').resolve()) and REVIEW.is_file()

def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def atomic(path,raw):
    temp=path.with_name(path.name+'.tmp_'+STAMP)
    with temp.open('xb') as stream:stream.write(raw)
    assert temp.read_bytes()==raw
    os.replace(temp,path)
    assert path.read_bytes()==raw

state=json.loads((RUN/'runtime_process_02.json').read_bytes())
assert state['status']=='PROCESS_EXITED' and state['returncode']==0
archive=RUN/'completed_attempt_02'
archived=json.loads((archive/'verification.json').read_bytes())
candidate=ROOT/'reader_correction_v2/um.py'
proof=json.loads((ROOT/'reader_correction_v2/verification.json').read_bytes())
assert sha(candidate)==proof['candidate_sha256']
assert proof['regression_tests']==38 and proof['added_functions']==[]
assert proof['only_named_functions_changed'] and not proof['embedded_lean_changed']
assert not proof['principal_gate_changed']
assert sha(ROOT/'um.py')==sha(RUN/'um.py')==proof['source_sha256']
assert sha(archive/'um.py')==proof['source_sha256']
assert not (RUN/'reader_integration_manifest.json').exists()
assert not (RUN/'runtime_process_03.json').exists()
backups={}
for path in [ROOT/'um.py',RUN/'um.py']:
    raw=path.read_bytes();backup=path.with_name(path.name+'.bak_'+STAMP)
    with backup.open('xb') as stream:stream.write(raw)
    assert backup.read_bytes()==raw
    backups[str(path)]=str(backup)
    atomic(path,candidate.read_bytes())

files=[]
for name in ['manifest.json','manifest_results.json']:
    stage=json.loads((ROOT/'runtime_inputs_pending'/name).read_bytes())
    for item in stage['files']:
        source=Path(item['destination']);target=RUN/item['relative_to_runtime']
        assert target.resolve().is_relative_to(RUN.resolve())
        assert source.stat().st_size==item['bytes'] and sha(source)==item['sha256']
        assert not target.exists(), 'Omitted inputs must not overwrite existing files'
        target.parent.mkdir(parents=True,exist_ok=True)
        temp=target.with_name(target.name+'.copying_'+STAMP)
        shutil.copyfile(source,temp)
        assert temp.stat().st_size==item['bytes'] and sha(temp)==item['sha256']
        os.replace(temp,target)
        files.append(dict(item,runtime_destination=str(target)))
assert len(files)==4

# Previous outputs have byte-exact immutable copies. Remove only those named output
# files so a later missing output cannot masquerade as an emission of attempt 03.
cleared=[]
for name,entry in archived['archive_files'].items():
    generated=(name.startswith(('um_absoluto','fig_','tgl_kernel_')) or
               name in ['audit_principal.stdout.txt','formal_stage_verification.json'])
    if not generated:continue
    path=RUN/name
    assert path.parent.resolve()==RUN.resolve()
    assert sha(path)==sha(archive/name)==entry['sha256']
    path.unlink()
    cleared.append(name)

record=dict(timestamp=datetime.now().astimezone().isoformat(),
    status='READER_CORRECTION_AND_INPUTS_READY_FOR_RUN03',
    working_sha256=sha(RUN/'um.py'),previous_working_sha256=proof['source_sha256'],
    review_path=str(REVIEW),review_sha256=sha(REVIEW),
    candidate_verification_sha256=sha(ROOT/'reader_correction_v2/verification.json'),
    previous_run_archive=str(archive),archive_verification_sha256=sha(archive/'verification.json'),
    files=files,code_backups=backups,cleared_previous_outputs=cleared,
    modified_existing_functions=proof['modified_existing_functions'],added_functions=[],
    embedded_lean_changed=False,principal_gate_changed=False,
    full_runtime_of_corrected_candidate_completed=False)
atomic(RUN/'reader_integration_manifest.json',(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(dict(installed=True,working_sha256=record['working_sha256'],
    inputs=len(files),code_backups=len(backups),previous_outputs_archived_and_cleared=len(cleared))))
