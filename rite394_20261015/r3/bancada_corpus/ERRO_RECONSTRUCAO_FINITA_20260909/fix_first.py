from pathlib import Path
from datetime import datetime
import os
p=Path(__file__).resolve().parent/'FiniteResponseErrorBounds.lean'
raw=p.read_bytes();text=raw.decode('utf8')
changes=[('simp only [decodeResponse,Matrix.cons_val_zero,Matrix.cons_val_one,\n      Matrix.cons_val_two,Matrix.cons_val_three]','simp only [decodeResponse]'),
('  have ht := trace_product_error hB gi A C hgi hAC','  have ht := trace_product_error hB gi A C hgi hAC\n  have heps : 0 ≤ epsilon := (abs_nonneg _).trans (hAC 0 0)'),
('  convert! h using 1 <;> ring','  convert! h using 1; ring'),
('  rw [←abs_div,abs_of_pos h0] at hh\n  convert! hh using 1 <;> field_simp\n  <;> ring','  have he : observed/t^2-response=(observed-response*t^2)/t^2 := by\n    field_simp [ht]; ring\n  rw [he,abs_div,abs_of_pos h0]\n  calc\n    _ ≤ (noise+remainder*t^4)/t^2 := hh\n    _ = noise/t^2+remainder*t^2 := by field_simp [ht]; ring')]
for a,b in changes:assert text.count(a)==1,a;text=text.replace(a,b)
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
bak=p.with_name(p.name+'.bak_'+stamp)
with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert bak.read_bytes()==raw
data=text.encode('utf8');tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.replace(tmp,p);assert p.read_bytes()==data
print('Corrected proof tactics; immediate byte backup verified.')
