from pathlib import Path
import hashlib, os

base = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\maxwell_global')
src = base / 'CompactBoostStrongDerivativeReductionR1.lean'
dst = base / 'CompactBoostStrongDerivativeReductionR2.lean'
s = src.read_text(encoding='utf-8')
changes = [
('  exact (hc.fderiv_apply ℝ momentumLongitudinalDirection).smul_left',
 '''  simpa only [compactBoostGenerator, Pi.smul_apply] using
    (hc.fderiv_apply ℝ momentumLongitudinalDirection).smul_left
      (f := fun y : MomentumCoordinates => -shellEnergy y)'''),
('(Real.hasDerivAt_cosh 0).comp 0', '(Real.hasDerivAt_cosh (-(0 : ℝ))).comp 0'),
('(Real.hasDerivAt_sinh 0).comp 0', '(Real.hasDerivAt_sinh (-(0 : ℝ))).comp 0'),
('      simpa only [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)] using hy',
 '''      rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg (‖r i y - d y‖))]
      exact hy'''),
('    rw [← F1Fecho.SmoothLinearMomentumCutoff.l2_integral_norm_sq (orbitalMeasure 0)]',
 '''    have hnorm (u : H1) : (∫ y, ‖u y‖ ^ 2 ∂orbitalMeasure 0) = ‖u‖ ^ 2 := by
      have h := congrArg (RCLike.re : ℂ → ℝ) (L2.inner_def (𝕜 := ℂ) u u)
      rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) u u)] at h
      simpa only [inner_self_eq_norm_sq] using h.symm
    rw [← hnorm (F i - D)]'''),
('LinearIsometryEquiv.refl_apply', 'LinearIsometryEquiv.coe_refl, id_eq'),
]
for old, new in changes:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
data = s.encode('utf-8')
tmp = dst.with_suffix('.lean.tmp_r45')
with tmp.open('xb') as f:
    f.write(data)
assert tmp.read_bytes() == data
os.rename(tmp, dst)
print({'path': str(dst), 'sha256': hashlib.sha256(dst.read_bytes()).hexdigest(), 'bytes': len(data)})
