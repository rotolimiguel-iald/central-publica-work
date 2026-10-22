"""Correct API/simplifier details, preserving the exact failed source bytes."""
from pathlib import Path
from datetime import datetime
import os
path = Path(__file__).resolve().parent / "ProbeResponseRecord.lean"
raw = path.read_bytes()
text = raw.decode()
assert text.count('noncomputable section') == 1
text = text.replace('noncomputable section', 'open scoped ContDiff\nnoncomputable section')
assert text.count('  field_simp [Real.pi_ne_zero]\n  ring') == 2
text = text.replace('  field_simp [Real.pi_ne_zero]\n  ring', '  field_simp [Real.pi_ne_zero] <;> ring')
old = '  simp only [finiteCovectorStressField,one_smul,covectorStressField]'
assert text.count(old) == 1
text = text.replace(old, '  simp only [finiteCovectorStressField,one_smul,covectorStressField,probe_record_metric]')
new = text.encode()
backup = path.with_name(path.name + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with backup.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
assert backup.read_bytes() == raw
temp = path.with_name(path.name + '.tmp_fix')
with temp.open('xb') as f: f.write(new); f.flush(); os.fsync(f.fileno())
assert temp.read_bytes() == new and path.read_bytes() == raw
os.replace(temp, path)
assert path.read_bytes() == new
print('Fixed simplifier completion, scope notation, and metric unfolding; byte backup preserved.')
