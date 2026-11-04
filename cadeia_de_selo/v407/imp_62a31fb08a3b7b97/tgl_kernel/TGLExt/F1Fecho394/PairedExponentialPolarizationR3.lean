import TGLExt.F1Fecho394.ExponentialTomitaR2
import Mathlib.Analysis.InnerProductSpace.Dual
import Mathlib.Analysis.Normed.Module.HahnBanach
import Mathlib.Analysis.Normed.Group.Quotient
import Mathlib.Topology.Algebra.Module.ContinuousLinearMap.Quotient
/-! Analytic polarization in both graph coordinates, on the same Fock.
This lemma is about graph closure, not merely totality in the first coordinate. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open Filter Topology
namespace F1Fecho.PairedExponential
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicSectors
open F1Fecho.Exponential F1Fecho.WedgeExponential

variable (K : Submodule ℝ H1) (A : H1 → H1)
variable (hadd : ∀ x y, A (x+y) = A x + A y)
variable (hreal : ∀ (t : ℝ) x, A (t • x) = t • A x)

def pairCoefficient (v w : F) (x y : H1) (n : ℕ) : ℂ :=
  coefficient v x n + coefficient w y n

theorem pair_scalar_series (v w : F) (x y : H1) (z : ℂ) :
    HasSum (fun n => z^n * pairCoefficient v w x y n)
      (inner ℂ v (exponential (z•x)) + inner ℂ w (exponential (z•y))) := by
  simpa only [pairCoefficient,mul_add] using (scalar_series v x z).add (scalar_series w y z)

include hreal in
theorem pair_coefficients_zero (v w : F)
    (hv : ∀ x ∈ K, inner ℂ v (exponential x) + inner ℂ w (exponential (A x)) = 0)
    (x : H1) (hx : x ∈ K) (n : ℕ) : pairCoefficient v w x (A x) n = 0 := by
  have hp : HasFPowerSeriesAt (0 : ℝ → ℂ)
      (realSeries (pairCoefficient v w x (A x))) 0 := by
    apply hasFPowerSeriesAt_iff.mpr
    apply Filter.Eventually.of_forall
    intro t
    have hs := pair_scalar_series v w x (A x) (t : ℂ)
    have hz : inner ℂ v (exponential ((t:ℂ)•x)) +
        inner ℂ w (exponential ((t:ℂ)•A x)) = 0 := by
      rw [ofReal_smul_H1,ofReal_smul_H1,← hreal]
      exact hv (t•x) (K.smul_mem t hx)
    simpa only [realSeries_coeff,Complex.real_smul,Complex.ofReal_pow,hz,Pi.zero_apply] using hs
  have he := hp.apply_eq_zero n (1 : ℝ)
  simpa [realSeries] using he

include hreal in
theorem pair_pure_zero (v w : F)
    (hv : ∀ x ∈ K, inner ℂ v (exponential x) + inner ℂ w (exponential (A x)) = 0)
    (x : H1) (hx : x ∈ K) (n : ℕ) :
    inner ℂ (v n) (pureTensor n x) + inner ℂ (w n) (pureTensor n (A x)) = 0 := by
  have h := pair_coefficients_zero K A hreal v w hv x hx n
  unfold pairCoefficient coefficient component at h
  rw [_root_.inner_smul_right (v n) (pureTensor n x) (weight n : ℂ),
    _root_.inner_smul_right (w n) (pureTensor n (A x)) (weight n : ℂ),← mul_add] at h
  exact (mul_eq_zero.mp h).resolve_left (by exact_mod_cast (ne_of_gt (weight_pos n)))

include hadd hreal in
theorem pair_pure_zero_complexification (v w : F)
    (hv : ∀ x ∈ K, inner ℂ v (exponential x) + inner ℂ w (exponential (A x)) = 0)
    (x y : H1) (hx : x ∈ K) (hy : y ∈ K) (n : ℕ) :
    inner ℂ (v n) (pureTensor n (x+Complex.I•y)) +
      inner ℂ (w n) (pureTensor n (A x+Complex.I•A y)) = 0 := by
  let P : ℂ → ℂ := fun z =>
    inner ℂ (v n : TensorHilbert n) (pureCompleted n (x+z•y)) +
    inner ℂ (w n : TensorHilbert n) (pureCompleted n (A x+z•A y))
  have ha : AnalyticOnNhd ℂ P Set.univ := by
    intro z _
    apply AnalyticAt.add
    · exact ((innerSL ℂ (v n : TensorHilbert n)).analyticAt _).comp
        ((analytic_pureCompleted n _).comp (analyticAt_const.add (analyticAt_id.smul analyticAt_const)))
    · exact ((innerSL ℂ (w n : TensorHilbert n)).analyticAt _).comp
        ((analytic_pureCompleted n _).comp (analyticAt_const.add (analyticAt_id.smul analyticAt_const)))
  have hr : ∀ t : ℝ, P t = 0 := by
    intro t
    have h := pair_pure_zero K A hreal v w hv (x+t•y) (K.add_mem hx (K.smul_mem t hy)) n
    rw [hadd,hreal] at h
    change inner ℂ (v n : TensorHilbert n) (pureCompleted n (x+t•y)) +
      inner ℂ (w n : TensorHilbert n) (pureCompleted n (A x+t•A y)) = 0 at h
    simpa only [P,ofReal_smul_H1] using h
  exact analytic_zero_from_real P ha hr Complex.I

include hadd hreal in
theorem pair_orthogonal_complexification (v w : F)
    (hv : ∀ x ∈ K, inner ℂ v (exponential x) + inner ℂ w (exponential (A x)) = 0)
    (x y : H1) (hx : x ∈ K) (hy : y ∈ K) :
    inner ℂ v (exponential (x+Complex.I•y)) +
      inner ℂ w (exponential (A x+Complex.I•A y)) = 0 := by
  have hs := pair_scalar_series v w (x+Complex.I•y) (A x+Complex.I•A y) 1
  have hz : ∀ n, pairCoefficient v w (x+Complex.I•y) (A x+Complex.I•A y) n = 0 := by
    intro n
    unfold pairCoefficient coefficient component
    rw [_root_.inner_smul_right (v n) (pureTensor n (x+Complex.I•y)) (weight n : ℂ),
      _root_.inner_smul_right (w n) (pureTensor n (A x+Complex.I•A y)) (weight n : ℂ),← mul_add,
      pair_pure_zero_complexification K A hadd hreal v w hv x y hx hy n,mul_zero]
  simp only [hz,mul_zero,one_smul] at hs
  exact hs.unique (hasSum_zero (α := ℂ) (β := ℕ))

end F1Fecho.PairedExponential
#print axioms F1Fecho.PairedExponential.pair_coefficients_zero
#print axioms F1Fecho.PairedExponential.pair_pure_zero_complexification
#print axioms F1Fecho.PairedExponential.pair_orthogonal_complexification
