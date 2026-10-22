"""Reuse the finite-ideal orbit proofs on the explicitly larger scalar domain."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
orbit = (ROOT / 'kernel/TGLV350/ScalarGNSOrbit.lean').read_text(encoding='utf-8')
linear = (ROOT / 'kernel/TGLV350/ScalarGNSLinear.lean').read_text(encoding='utf-8')
first = orbit[orbit.index('theorem scalarOrbit_memLp'):orbit.index('#print axioms')]
first = first.replace('(hA : HasFiniteDualSquare A)', '(hA : HasFiniteScalarSquare P A)')
first = first.replace('have hq := HasFiniteDualSquare.scalar_finite P A hA', 'have hq := hA')
first = first.replace('simp only [dualQuadraticIntegral, dualQuadraticIntegrand_star_mul] at hq',
    'simp only [HasFiniteScalarSquare, dualQuadraticIntegral, dualQuadraticIntegrand_star_mul] at hq')
second = linear[linear.index('theorem scalarGNSOrbit_ae'):linear.index('#print axioms')]
body = first + second
for old, new in [('scalarOrbit_memLp', 'scalarWeightOrbit_memLp'),
                 ('finiteDualLeftIdeal', 'scalarWeightLeftIdeal'),
                 ('scalarGNSOrbit', 'scalarWeightOrbit'),
                 ('scalarGNSLinear', 'scalarWeightLinear')]:
    body = body.replace(old, new)
text = '''import TGLV350.ScalarWeightDomain
import TGLV350.ScalarGNSLinear

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt MeasureTheory
open scoped ENNReal NNReal
noncomputable section

''' + body + '''
theorem scalarWeightOrbit_uniform (P : SiteProfile) (A : finiteDualLeftIdeal P) :
    scalarWeightOrbit P (Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) A) =
      scalarGNSOrbit P A := rfl

theorem scalarWeightOrbit_norm_sq_real (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    ‖scalarWeightOrbit P A‖ ^ 2 = dualHaarFactor *
      ∫ s : ℝ, ‖dualAmbient s A.val.val (regularVacuum P)‖ ^ 2 := by
  unfold scalarWeightOrbit
  rw [norm_smul,mul_pow,Real.norm_eq_abs,sq_abs,Real.sq_sqrt dualHaarFactor_pos.le,
    ← Fourier.integral_norm_sq_eq_L2 _ (scalarWeightOrbit_memLp P A.val.val A.property)]

'''
names = ['scalarWeightOrbit_memLp', 'scalarWeightOrbit', 'scalarWeightOrbit_norm_sq',
    'scalarWeightOrbit_ae', 'scalarWeightOrbit_add', 'scalarWeightOrbit_smul',
    'scalarWeightLinear', 'scalarWeightOrbit_zero_iff', 'scalarWeightLinear_injective',
    'scalarWeightOrbit_uniform', 'scalarWeightOrbit_norm_sq_real']
text += ''.join('#print axioms ' + name + '\n' for name in names)
text += 'end\nend TGLV350.Regular\n'
target = ROOT / 'kernel/TGLV350/ScalarWeightOrbit.lean'
assert not target.exists()
raw = text.encode('utf-8')
temporary = target.with_suffix('.lean.tmp')
with temporary.open('xb') as stream:
    stream.write(raw)
assert temporary.read_bytes() == raw
temporary.replace(target)
assert target.read_bytes() == raw
print('Created ScalarWeightOrbit.lean with 11 audit targets; original sources read only.')
