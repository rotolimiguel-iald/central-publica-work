"""Build an isolated reviewer runner for the one currently frozen module."""
from pathlib import Path
import ast
REV=Path(__file__).resolve().parent
t=(REV/'run_right_regularization_review.py').read_text(encoding='utf-8')
t=t.replace('Isolated two right-regularization modules and 19-target auditor',
            'Isolated first right-adjoint-pair module and eight-target auditor')
t=t.replace("RUN=REV/('right_regularization_independent_'", "RUN=REV/('paired_right_first_independent_'")
t=t.replace("['core_polar_latest_run.txt','gaussian_polar_latest_run.txt']",
            "['core_polar_latest_run.txt','right_regularization_latest_run.txt']")
start=t.index('artifacts=[')
end=t.index('surfaces={}',start)
t=t[:start]+'''artifacts=['right_regularization_custody.json','right_regularization_custody_verification.json']
for n in artifacts:write(RUN/n,(ROOT/n).read_bytes())
P=load(RUN/artifacts[0]);PV=load(RUN/artifacts[1])
assert hf(ROOT/artifacts[0])==PV['custody_sha256'] and PV['custody_ok']
assert PV['compiled_source_binary_pairs_reread']==191 and PV['immediate_byte_backups_and_prefixes']==34
assert hf(ROOT/'um.py')==P['working_sha256']
assert all(hf(p)==h for p,h in P['review_sha256'].items())
name='ScalarRightAdjointPair'
source=ROOT/'kernel/TGLV350'/ (name+'.lean')
log=ROOT/'logs/ScalarRightAdjointPair_20260912_223208_355929.json'
ar=load(log);binary=ROOT/'build/TGLV350'/(name+'.olean')
assert ar['returncode']==ar['lean_returncode']==0 and ar['source_unchanged_during_compile']
assert ar['sha256']==hf(source) and ar['output_sha256']==hf(binary) and ar['output_exists']
targets_author=axioms(Path(ar['stdout']).read_text(encoding='utf-8'))
assert len(targets_author)==8 and all(set(a)==allowed for a in targets_author.values())
history_paths=sorted((ROOT/'logs').glob(name+'_*.json'))
D={'status':'PARTIAL_REVIEW_INPUT_ONE_FROZEN_MODULE__FULL_MANIFEST_PENDING',
 'modules':{name:{'source_sha256':hf(source),'binary_sha256':hf(binary),'targets':8,
   'final_log':str(log),'final_log_sha256':hf(log),'stdout_sha256':hf(ar['stdout']),
   'stderr_sha256':hf(ar['stderr']),'failed_attempts':[str(p) for p in history_paths if load(p)['returncode']]}},
 'targets':{n:sorted(a) for n,a in targets_author.items()},
 'parent_custody_sha256':hf(ROOT/artifacts[0]),'integrated_working_sha256':hf(ROOT/'um.py'),
 'integrated':False,'full_29_target_review_complete':False}
save(RUN/'reviewer_input_pins.json',D)
''' +t[end:]
t=t.replace('len(targets)==len(set(targets))==19','len(targets)==len(set(targets))==8')
t=t.replace("[REV/'REVIEW_GAUSSIAN_POLAR_DEV.md',REV/'REVIEW_GAUSSIAN_POLAR_INTEGRATED.md']",
            "[REV/'REVIEW_RIGHT_REGULARIZATION_DEV.md',REV/'REVIEW_RIGHT_REGULARIZATION_INTEGRATED.md']")
t=t.replace("REV/'right_regularization_latest_run.txt'", "REV/'paired_right_first_latest_run.txt'")
t=t.replace('RightRegularizationAudit.lean','PairedRightFirstAudit.lean')
t=t.replace('len(records)==3','len(records)==2').replace("'exact_19_targets'","'exact_8_targets'")
t=t.replace("'two_binaries_equal_author'","'one_binary_equal_author'")
ast.parse(t)
p=REV/'run_paired_right_first_review.py';assert not p.exists()
raw=t.encode('utf-8');temp=p.with_name(p.name+'.tmp')
with temp.open('xb') as f:f.write(raw)
assert temp.read_bytes()==raw
temp.replace(p)
print(p)
