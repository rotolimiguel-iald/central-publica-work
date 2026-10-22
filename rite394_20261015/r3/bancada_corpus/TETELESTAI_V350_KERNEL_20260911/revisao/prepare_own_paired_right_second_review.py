from pathlib import Path
from datetime import datetime
import ast
import os

rev = Path(__file__).resolve().parent
raw = (rev / 'run_paired_right_first_review.py').read_text(encoding='utf-8')
replacements = {
    'Isolated first right-adjoint-pair module and eight-target auditor': 'Isolated second paired-right module and twelve-target auditor',
    "'paired_right_first_independent_'": "'paired_right_second_independent_'",
    "['core_polar_latest_run.txt','right_regularization_latest_run.txt']": "['paired_right_first_latest_run.txt']",
    "name='ScalarRightAdjointPair'": "name='ScalarCommutantSandwich'",
    'logs/ScalarRightAdjointPair_20260912_223208_355929.json': 'logs/ScalarCommutantSandwich_20260912_224208_138578.json',
    'len(targets_author)==8': 'len(targets_author)==12',
    'PARTIAL_REVIEW_INPUT_ONE_FROZEN_MODULE__FULL_MANIFEST_PENDING': 'PARTIAL_REVIEW_SECOND_FROZEN_MODULE__FULL_MANIFEST_PENDING',
    "'targets':8": "'targets':12",
    'len(targets)==len(set(targets))==8': 'len(targets)==len(set(targets))==12',
    'paired_right_first_latest_run.txt': 'paired_right_second_latest_run.txt',
    'PairedRightFirstAudit': 'PairedRightSecondAudit',
    "'exact_8_targets'": "'exact_12_targets'",
}
# Preserve the dependency pointer to the first run while renaming the output pointer.
replacements.pop('paired_right_first_latest_run.txt')
for old, new in replacements.items():
    assert old in raw, old
    raw = raw.replace(old, new)
old = "write(REV/'paired_right_first_latest_run.txt',str(RUN).encode())"
assert old in raw
raw = raw.replace(old, "write(REV/'paired_right_second_latest_run.txt',str(RUN).encode())")
old = "REV/'REVIEW_RIGHT_REGULARIZATION_INTEGRATED.md']"
assert old in raw
raw = raw.replace(old, "REV/'REVIEW_RIGHT_REGULARIZATION_INTEGRATED.md',REV/'REVIEW_PAIRED_RIGHT_DEV.md']")
ast.parse(raw)
p = rev / 'run_paired_right_second_review.py'
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
