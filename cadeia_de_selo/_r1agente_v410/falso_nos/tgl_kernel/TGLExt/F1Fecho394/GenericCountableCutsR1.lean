import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Tactic.Linarith
/-! A countable family of bounded intervals detects equality almost everywhere. -/
set_option autoImplicit false
namespace F1Fecho.GenericCountableCuts
open MeasureTheory Filter
 theorem ae_eq_of_ioc {E : Type*} (f g : ℝ → E)
    (h : ∀ n : ℕ, ∀ᵐ s : ℝ, s ∈ Set.Ioc (-(n : ℝ)) (n : ℝ) → f s = g s) :
    f =ᵐ[volume] g := by
  filter_upwards [ae_all_iff.mpr h] with s hs
  obtain ⟨n,hn⟩ := exists_nat_gt |s|
  apply hs n
  constructor
  · have hl := neg_abs_le s
    linarith
  · exact le_trans (le_abs_self s) hn.le
end F1Fecho.GenericCountableCuts
#print axioms F1Fecho.GenericCountableCuts.ae_eq_of_ioc
