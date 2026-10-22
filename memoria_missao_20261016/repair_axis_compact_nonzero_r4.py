from pathlib import Path
import hashlib
import os
import json

base = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\maxwell_global')
src = base / 'AxisCompactFockNonzeroEnergyR3.lean'
dst = base / 'AxisCompactFockNonzeroEnergyR4.lean'
old = src.read_bytes()
text = old.decode('utf-8').replace('\r\n', '\n')
repairs = [(
'''  have he : inner ℂ h h = ((‖h‖ ^ 2 : ℝ) : ℂ) := by
    simpa only [Complex.ofReal_pow] using inner_self_eq_norm_sq_to_K (𝕜 := ℂ) h
  rw [coherentBoostPair, he, ← Complex.ofReal_exp]
  simp [Complex.mul_im]''',
'''  have hs : inner ℂ h h = (‖h‖ : ℂ) ^ 2 := by
    convert! inner_self_eq_norm_sq_to_K (𝕜 := ℂ) h using 1 <;> rfl
  have he : inner ℂ h h = ((‖h‖ ^ 2 : ℝ) : ℂ) := by
    calc
      inner ℂ h h = (‖h‖ : ℂ) ^ 2 := hs
      _ = ((‖h‖ ^ 2 : ℝ) : ℂ) := (Complex.ofReal_pow ‖h‖ 2).symm
  have hexp : Complex.exp (inner ℂ h h) = (Real.exp (‖h‖ ^ 2) : ℂ) := by
    calc
      Complex.exp (inner ℂ h h) = Complex.exp ((‖h‖ ^ 2 : ℝ) : ℂ) :=
        congrArg Complex.exp he
      _ = (Real.exp (‖h‖ ^ 2) : ℂ) := (Complex.ofReal_exp (‖h‖ ^ 2)).symm
  rw [coherentBoostPair, hexp]
  simp only [Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im, zero_mul, add_zero]'''), (
'''  rw [he]
  convert hb.const_mul (Complex.normSq z : ℂ) using 1
  push_cast
  ring''',
'''  have hd : (Complex.normSq z : ℂ) * (Complex.I * (b : ℂ)) =
      Complex.I * ((Complex.normSq z * b : ℝ) : ℂ) := by
    rw [Complex.ofReal_mul]
    ring
  have ht : HasDerivAt
      (fun s : ℝ => (Complex.normSq z : ℂ) * inner ℂ ψ (VF s ψ))
      ((Complex.normSq z : ℂ) * (Complex.I * (b : ℂ))) 0 := by
    convert! hb.const_mul (Complex.normSq z : ℂ) using 1 <;> rfl
  rw [he]
  convert! ht.congr_deriv hd using 1 <;> rfl''')]
for before, after in repairs:
    assert text.count(before) == 1
    text = text.replace(before, after)
data = text.encode('utf-8')
assert data.count(b'#print axioms') == 7
assert b'sorry' not in data
assert not dst.exists()
tmp = dst.with_name(dst.name + '.tmp_r4')
with tmp.open('xb') as f:
    f.write(data)
    f.flush()
    os.fsync(f.fileno())
assert tmp.read_bytes() == data
os.rename(tmp, dst)
assert src.read_bytes() == old
print(json.dumps({'path': str(dst), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'print_axioms': 7}, ensure_ascii=False))
