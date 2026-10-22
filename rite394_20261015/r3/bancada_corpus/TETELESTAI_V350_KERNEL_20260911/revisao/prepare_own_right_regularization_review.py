"""Adapt the reviewer's own isolated runner; never execute author helpers."""
from pathlib import Path
import ast

rev = Path(__file__).resolve().parent
source = (rev / 'run_gaussian_polar_review.py').read_text(encoding='utf-8')
replacements = [
    ('Isolated four Gaussian-polar modules and 34-target auditor', 'Isolated two right-regularization modules and 19-target auditor'),
    ("RUN=REV/('gaussian_polar_independent_'", "RUN=REV/('right_regularization_independent_'"),
    ("['core_polar_latest_run.txt']", "['gaussian_polar_latest_run.txt']"),
    ("artifacts=['core_polar_custody.json','core_polar_custody_verification.json',\n 'gaussian_polar_draft_status.json','RELATORIO_POLAR_GAUSSIANO_CICLICO_DEV.md',\n 'make_gaussian_polar_helpers.py','record_gaussian_polar_draft.py','prepare_gaussian_polar_stage.py',\n 'record_gaussian_polar_progress.py','verify_gaussian_polar_custody.py']",
     "artifacts=['gaussian_polar_custody.json','gaussian_polar_custody_verification.json','right_regularization_draft_status.json','RELATORIO_REGULARIZACAO_COMUTANTE_DEV.md',\n 'make_right_regularization_helpers.py','record_right_regularization_draft.py','prepare_right_regularization_stage.py',\n 'record_right_regularization_progress.py','verify_right_regularization_custody.py']"),
    ("PV['compiled_source_binary_pairs_reread']==185", "PV['compiled_source_binary_pairs_reread']==189"),
    ("ROOT/'gaussian_polar_draft_status.json'", "ROOT/'right_regularization_draft_status.json'"),
    ("ROOT/'RELATORIO_POLAR_GAUSSIANO_CICLICO_DEV.md'", "ROOT/'RELATORIO_REGULARIZACAO_COMUTANTE_DEV.md'"),
    ("len(targets)==len(set(targets))==34", "len(targets)==len(set(targets))==19"),
    ("REV.glob('REVIEW_*.md')", "[REV/'REVIEW_GAUSSIAN_POLAR_DEV.md',REV/'REVIEW_GAUSSIAN_POLAR_INTEGRATED.md']"),
    ("REV/'gaussian_polar_latest_run.txt'", "REV/'right_regularization_latest_run.txt'"),
    ('GaussianPolarAudit.lean', 'RightRegularizationAudit.lean'),
    ('len(records)==5', 'len(records)==3'),
    ("'exact_34_targets'", "'exact_19_targets'"),
    ("'four_binaries_equal_author'", "'two_binaries_equal_author'"),
]
for old, new in replacements:
    assert old in source, old
    source = source.replace(old, new)
ast.parse(source)
out = rev / 'run_right_regularization_review.py'
assert not out.exists()
raw = source.encode('utf-8')
temp = out.with_name(out.name + '.tmp')
with temp.open('xb') as f:
    f.write(raw)
assert temp.read_bytes() == raw
temp.replace(out)
assert out.read_bytes() == raw
print(out)
