from pathlib import Path
from datetime import datetime
import ast
import os

rev = Path(__file__).resolve().parent
raw = (rev / 'run_paired_right_first_review.py').read_text(encoding='utf-8')
changes = {
    'Isolated first right-adjoint-pair module and eight-target auditor': 'Third paired-right module and cumulative twenty-nine-target auditor; first two own binaries reused',
    "'paired_right_first_independent_'": "'paired_right_final_independent_'",
    "['core_polar_latest_run.txt','right_regularization_latest_run.txt']": "['paired_right_second_latest_run.txt']",
    "artifacts=['right_regularization_custody.json','right_regularization_custody_verification.json']": "artifacts=['right_regularization_custody.json','right_regularization_custody_verification.json',\n 'paired_right_draft_status.json','RELATORIO_ALGEBRA_DIREITA_ADJUNTO_DEV.md',\n 'make_paired_right_helpers.py','record_paired_right_draft.py','prepare_paired_right_stage.py',\n 'record_paired_right_progress.py','verify_paired_right_custody.py']",
    'len(targets)==len(set(targets))==8': 'len(targets)==len(set(targets))==29',
    "write(REV/'paired_right_first_latest_run.txt',str(RUN).encode())": "write(REV/'paired_right_final_latest_run.txt',str(RUN).encode())",
    'PairedRightFirstAudit': 'PairedRightFullAudit',
    "for rel in list(sources)+['PairedRightFullAudit.lean']:": "for rel in ['TGLV350/ScalarPairedRightAlgebra.lean','PairedRightFullAudit.lean']:",
    "'exact_8_targets'": "'exact_29_targets'",
    "'one_binary_equal_author':done and all(r.get('binary_equals_author',True) for r in records),": "'three_binaries_equal_author':done and all(r.get('binary_equals_author',True) for r in records) and len(reused_current)==2,\n 'independent_module_compilations_cumulative':3,\n 'reused_current_module_binaries_preserved':all(hf(r['frozen_binary'])==r['sha256'] for r in reused_current.values()),",
    "REV/'REVIEW_RIGHT_REGULARIZATION_INTEGRATED.md']": "REV/'REVIEW_RIGHT_REGULARIZATION_INTEGRATED.md',REV/'REVIEW_PAIRED_RIGHT_DEV.md']",
    "'sources':sources,'dependencies':deps,": "'sources':sources,'dependencies':deps,'reused_current_modules':reused_current,",
}
for old, new in changes.items():
    assert old in raw, old
    raw = raw.replace(old, new)
start = raw.index("name='ScalarRightAdjointPair'\n")
end = raw.index("surfaces={}\n", start)
raw = raw[:start] + '''D=load(RUN/'paired_right_draft_status.json')
assert len(D['modules'])==3 and len(D['targets'])==29
assert D['parent_custody_sha256']==hf(ROOT/artifacts[0])
assert D['integrated_working_sha256']==P['working_sha256']==hf(ROOT/'um.py')
assert D['report_sha256']==hf(RUN/'RELATORIO_ALGEBRA_DIREITA_ADJUNTO_DEV.md')
assert D['integrated'] is False and D['independent_review_complete'] is False
save(RUN/'reviewer_input_pins.json',D)
''' + raw[end:]
insert = raw.index('package_pins={}\n')
raw = raw[:insert] + '''reused_current={}
for name in ['ScalarRightAdjointPair','ScalarCommutantSandwich']:
    n='TGLV350.'+name;r=catalog[n];pin=D['modules'][name]
    assert hf(r['source'])==pin['source_sha256']==r['source_sha256']
    assert hf(r['binary'])==pin['binary_sha256']==r['sha256']
    assert Path(r['binary']).resolve().is_relative_to(REV)
    bp=RUN/'build/TGLV350'/(name+'.olean');write(bp,Path(r['binary']).read_bytes())
    for cp in Path(r['binary']).parent.glob(Path(r['binary']).name+'.*'):
        if cp.is_file():write(bp.with_name(cp.name),cp.read_bytes())
    reused_current[n]={**r,'frozen_binary':str(bp),'recompiled':False}
''' + raw[insert:]
ast.parse(raw)
p = rev / 'run_paired_right_final_review.py'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
if p.exists():
    old = p.read_bytes()
    backup = p.with_name(p.name + '.bak_' + stamp)
    backup.write_bytes(old)
    assert backup.read_bytes() == old
temp = p.with_name(p.name + '.tmp_' + stamp)
data = raw.encode('utf-8')
temp.write_bytes(data)
assert temp.read_bytes() == data
os.replace(temp, p)
assert p.read_bytes() == data
print(p)
