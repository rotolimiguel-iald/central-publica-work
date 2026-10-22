from pathlib import Path
import ast
from datetime import datetime
import os
import re

rev = Path(__file__).resolve().parent
raw = (rev / 'review_right_regularization_integration.py').read_text(encoding='utf-8')
changes = {
    'this two-module integration': 'this three-module integration',
    "OLD=Path((REV/'gaussian_polar_integrated_latest_run.txt').read_text().strip())": "OLD=Path((REV/'right_regularization_integrated_latest_run.txt').read_text().strip())",
    "DEV=Path((REV/'right_regularization_latest_run.txt').read_text().strip())": "DEV=Path((REV/'paired_right_final_latest_run.txt').read_text().strip())",
    "PTR=REV/'right_regularization_integrated_latest_run.txt'": "PTR=REV/'paired_right_integrated_latest_run.txt'",
    "REV/('right_regularization_integrated_'": "REV/('paired_right_integrated_'",
    'gaussian_polar_custody.json': 'right_regularization_custody.json',
    'gaussian_polar_custody_verification.json': 'right_regularization_custody_verification.json',
    'right_regularization_draft_status.json': 'paired_right_draft_status.json',
    'RELATORIO_REGULARIZACAO_COMUTANTE_DEV.md': 'RELATORIO_ALGEBRA_DIREITA_ADJUNTO_DEV.md',
    'make_right_regularization_helpers.py': 'make_paired_right_helpers.py',
    'prepare_right_regularization_stage.py': 'prepare_paired_right_stage.py',
    'record_right_regularization_progress.py': 'record_paired_right_progress.py',
    'verify_right_regularization_custody.py': 'verify_paired_right_custody.py',
    'REVIEW_RIGHT_REGULARIZATION_DEV.md': 'REVIEW_PAIRED_RIGHT_DEV.md',
    "assert all(v is True for k,v in C.items() if k!='records')": "assert all(v is True for v in C.values() if isinstance(v,bool))",
    "assert hf(DEV/'manifest.json')==V['manifest_sha256'] and hf(DEV/'compilation.json')==V['compilation_sha256']": "assert hf(DEV/'verification.json')==load(DEV/'final_review_pin.json')['verification_sha256']\n    assert hf(DEV/'compilation.json')==V['compilations'][str(DEV)]",
    "assert len(M['sources'])==2": "assert len(M['sources'])==3",
    "V['own_runs']=[{'path':str(DEV),'manifest_sha256':hf(DEV/'manifest.json'),'compilation_sha256':hf(DEV/'compilation.json')}]": "V['own_runs']=[{'path':p,'manifest_sha256':hf(Path(p)/'manifest.json'),'compilation_sha256':h} for p,h in V['compilations'].items()]",
    'all_two_import_rewrites_literal': 'all_three_import_rewrites_literal',
    "pending=['right_regularization_custody.json','right_regularization_custody_verification.json','RELATORIO_REGULARIZACAO_COMUTANTE_INTEGRADA.md']": "pending=['paired_right_custody.json','paired_right_custody_verification.json','RELATORIO_ALGEBRA_DIREITA_ADJUNTO_INTEGRADA.md']",
    "assert len(changed)==4": "assert len(changed)==5",
    "rows[-4:]": "rows[-5:]",
    "'new_author_compilations':4": "'new_author_compilations':5",
    'full_weight_right_regularization_and_commutant_approximation_does_not_discharge_KMS_trace_or_physical_frontier': 'original_adjoint_pairs_and_generated_right_star_algebra_does_not_discharge_KMS_trace_or_physical_frontier',
}
for old,new in changes.items():
    assert old in raw, old
    raw = raw.replace(old,new)
counts = {'893':'896','6882':'6901','6901':'6930','191':'194','187':'189','98':'99','19':'29'}
raw = re.sub(r'\b(?:893|6882|6901|191|187|98|19)\b',lambda m:counts[m.group(0)],raw)
old = "'make_paired_right_helpers.py','prepare_paired_right_stage.py'"
assert old in raw
raw = raw.replace(old,"'make_paired_right_helpers.py','record_paired_right_draft.py','prepare_paired_right_stage.py'")
old = "    diffs={}\n"
assert old in raw
raw = raw.replace(old,"""    HS=load(DEV/'helper_static_inspection.json')
    for n,pin in HS['helpers'].items():assert hf(ROOT/n)==pin['sha256']
    for n,pin in HS['proposed_changes'].items():assert hf(ROOT/n)==pin['candidate_text_sha256']
    diffs={}
""")
ast.parse(raw)
path = rev / 'review_paired_right_integration.py'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
if path.exists():
    old = path.read_bytes()
    backup = path.with_name(path.name+'.bak_'+stamp)
    backup.write_bytes(old)
    assert backup.read_bytes() == old
data = raw.encode('utf-8')
tmp = path.with_name(path.name+'.tmp_'+stamp)
tmp.write_bytes(data)
assert tmp.read_bytes()==data
os.replace(tmp,path)
assert path.read_bytes()==data
print(path)
