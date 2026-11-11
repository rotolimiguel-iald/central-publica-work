import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Analysis.InnerProductSpace.StandardSubspace
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.Tactic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000

namespace TGLV350.Regular
open ClosedSubmodule
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Conjugating the scalar places lambda in the first inner-product factor. -/
def phaseRealMap (z : ℂ) : H →L[ℝ] H :=
  ((star z) • ContinuousLinearMap.id ℂ H).restrictScalars ℝ

def phaseCompression (K : Submodule ℝ H) [CompleteSpace K] (z : ℂ) : K →L[ℝ] K :=
  K.orthogonalProjectionOnto.comp ((phaseRealMap z).comp K.subtypeL)

/-- A bounded real bilinear form. Symmetry is neither assumed nor asserted. -/
def phaseVariationalForm (K : Submodule ℝ H) [CompleteSpace K] (z : ℂ) :
    K →L[ℝ] K →L[ℝ] ℝ :=
  (innerSL ℝ).comp (phaseCompression K z)

theorem phaseVariationalForm_apply (K : Submodule ℝ H) [CompleteSpace K]
    (z : ℂ) (x y : K) :
    phaseVariationalForm K z x y = (z * inner ℂ (x : H) (y : H)).re := by
  change inner ℝ (K.orthogonalProjectionOnto ((star z) • (x : H))) y = _
  rw [K.inner_orthogonalProjectionOnto_eq_of_mem_right]
  change (inner ℂ ((star z) • (x : H)) (y : H)).re = _
  rw [inner_smul_left, starRingEnd_apply, star_star]

theorem phaseVariationalForm_diagonal (K : Submodule ℝ H) [CompleteSpace K]
    (z : ℂ) (x : K) : phaseVariationalForm K z x x = z.re * ‖x‖ ^ 2 := by
  rw [phaseVariationalForm_apply, Complex.mul_re]
  have hi : (inner ℂ (x : H) (x : H)).im = 0 := inner_self_im (𝕜 := ℂ) (x : H)
  have hr : (inner ℂ (x : H) (x : H)).re = ‖x‖ ^ 2 :=
    (norm_sq_eq_re_inner (𝕜 := ℂ) (x : H)).symm
  rw [hi, hr, mul_zero, sub_zero]

/-- Positive real part gives coercivity, including nonreal lambda. -/
theorem phaseVariationalForm_coercive (K : Submodule ℝ H) [CompleteSpace K]
    (z : ℂ) (hz : 0 < z.re) : IsCoercive (phaseVariationalForm K z) := by
  refine ⟨z.re, hz, ?_⟩
  intro x
  rw [phaseVariationalForm_diagonal, pow_two, mul_assoc]

/-- Lax-Milgram solves the real variational equation on the same closed K. -/
def phaseVariationalSolution (K : Submodule ℝ H) [CompleteSpace K]
    (z : ℂ) (hz : 0 < z.re) : H →L[ℝ] K :=
  (phaseVariationalForm_coercive K z hz).continuousLinearEquivOfBilin.symm.toContinuousLinearMap.comp
    K.orthogonalProjectionOnto

theorem phaseVariationalSolution_equation (K : Submodule ℝ H) [CompleteSpace K]
    (z : ℂ) (hz : 0 < z.re) (x : H) (v : K) :
    (inner ℂ x (v : H)).re =
      (z * inner ℂ (phaseVariationalSolution K z hz x : H) (v : H)).re := by
  let e := (phaseVariationalForm_coercive K z hz).continuousLinearEquivOfBilin
  have he : e (phaseVariationalSolution K z hz x) = K.orthogonalProjectionOnto x :=
    e.apply_symm_apply _
  calc
    _ = inner ℝ (K.orthogonalProjectionOnto x) v :=
      (K.inner_orthogonalProjectionOnto_eq_of_mem_right v x).symm
    _ = inner ℝ (e (phaseVariationalSolution K z hz x)) v :=
      congrArg (fun y : K => inner ℝ y v) he.symm
    _ = phaseVariationalForm K z (phaseVariationalSolution K z hz x) v :=
      IsCoercive.continuousLinearEquivOfBilin_apply _ _ _
    _ = _ := phaseVariationalForm_apply K z _ _

theorem phaseVariationalSolution_unique (K : Submodule ℝ H) [CompleteSpace K]
    (z : ℂ) (hz : 0 < z.re) (x : H) (u : K)
    (hu : ∀ v : K, (inner ℂ x (v : H)).re = (z * inner ℂ (u : H) (v : H)).re) :
    u = phaseVariationalSolution K z hz x := by
  apply (phaseVariationalForm_coercive K z hz).continuousLinearEquivOfBilin.injective
  apply ext_inner_right ℝ
  intro v
  rw [IsCoercive.continuousLinearEquivOfBilin_apply,
    IsCoercive.continuousLinearEquivOfBilin_apply,
    phaseVariationalForm_apply, phaseVariationalForm_apply]
  exact (hu v).symm.trans (phaseVariationalSolution_equation K z hz x v)

/-- This controls the solution vector, not the associated multiplication operator. -/
theorem phaseVariationalSolution_bound (K : Submodule ℝ H) [CompleteSpace K]
    (z : ℂ) (hz : 0 < z.re) (x : H) :
    z.re * ‖phaseVariationalSolution K z hz x‖ ≤ ‖x‖ := by
  let u := phaseVariationalSolution K z hz x
  have he := phaseVariationalSolution_equation K z hz x u
  have hd := phaseVariationalForm_diagonal K z u
  rw [phaseVariationalForm_apply] at hd
  have hb := re_inner_le_norm (𝕜 := ℂ) x (u : H)
  have hu := norm_nonneg u
  have hx := norm_nonneg x
  change (inner ℂ x (u : H)).re ≤ ‖x‖ * ‖u‖ at hb
  change z.re * ‖u‖ ≤ ‖x‖
  by_cases hzero : ‖u‖ = 0
  · rw [hzero, mul_zero]
    exact hx
  · have hpos : 0 < ‖u‖ := lt_of_le_of_ne hu (Ne.symm hzero)
    nlinarith [he.trans hd, hb]

theorem phaseVariationalSolution_unit_real_bound (K : Submodule ℝ H) [CompleteSpace K]
    (z : ℂ) (hz : z.re = 1) (x : H) :
    ‖phaseVariationalSolution K z (by rw [hz]; norm_num) x‖ ≤ ‖x‖ := by
  have h := phaseVariationalSolution_bound K z (by rw [hz]; norm_num) x
  have he : z.re * ‖phaseVariationalSolution K z (by rw [hz]; norm_num) x‖ =
      ‖phaseVariationalSolution K z (by rw [hz]; norm_num) x‖ :=
    (congrArg (fun c : ℝ => c * ‖phaseVariationalSolution K z (by rw [hz]; norm_num) x‖) hz).trans (one_mul _)
  exact he ▸ h

theorem phaseVariationalSolution_one (K : Submodule ℝ H) [CompleteSpace K] (x : H) :
    phaseVariationalSolution K 1 (by norm_num) x = K.orthogonalProjectionOnto x := by
  apply (phaseVariationalSolution_unique K 1 (by norm_num) x (K.orthogonalProjectionOnto x) ?_).symm
  intro v
  rw [one_mul]
  exact (K.inner_orthogonalProjectionOnto_eq_of_mem_right v x).symm

#print axioms phaseRealMap
#print axioms phaseCompression
#print axioms phaseVariationalForm
#print axioms phaseVariationalForm_apply
#print axioms phaseVariationalForm_diagonal
#print axioms phaseVariationalForm_coercive
#print axioms phaseVariationalSolution
#print axioms phaseVariationalSolution_equation
#print axioms phaseVariationalSolution_unique
#print axioms phaseVariationalSolution_bound
#print axioms phaseVariationalSolution_unit_real_bound
#print axioms phaseVariationalSolution_one
end
end TGLV350.Regular
