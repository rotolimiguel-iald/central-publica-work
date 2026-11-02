import TGLExt.V350DualEnergyOnResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open scoped ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem ClosedPositiveForm.midpoint_finite_and_bound (Q : ClosedPositiveForm H)
    (r s : H) (hr : Q.value r < ⊤) (hs : Q.value s < ⊤) :
    Q.value ((1/2 : ℂ) • (r+s)) < ⊤ ∧
    (Q.value ((1/2 : ℂ) • (r+s))).toReal ≤
      ((Q.value r).toReal + (Q.value s).toReal)/2 := by
  have ha : Q.value (r+s) < ⊤ := Q.finiteDomain.add_mem hr hs
  have hm : Q.value ((1/2 : ℂ) • (r+s)) = ENNReal.ofReal (1/4) * Q.value (r+s) := by
    rw [Q.map_smul]
    norm_num
  refine ⟨by rw [hm]; exact ENNReal.mul_lt_top ENNReal.ofReal_lt_top ha, ?_⟩
  have hb := ENNReal.toReal_mono
    (ENNReal.add_ne_top.mpr ⟨ENNReal.mul_ne_top (by norm_num) (ne_of_lt hr),
      ENNReal.mul_ne_top (by norm_num) (ne_of_lt hs)⟩) (Q.add_le r s)
  rw [ENNReal.toReal_add (ENNReal.mul_ne_top (by norm_num) (ne_of_lt hr))
    (ENNReal.mul_ne_top (by norm_num) (ne_of_lt hs))] at hb
  simp only [ENNReal.toReal_mul] at hb
  norm_num at hb
  rw [hm, ENNReal.toReal_mul]
  norm_num
  linarith

theorem norm_midpoint_sub_identity (v r s : H) :
    4 * ‖(1/2 : ℂ) • (r+s)-v‖^2 + ‖r-s‖^2 =
      2*(‖r-v‖^2+‖s-v‖^2) := by
  have hp := parallelogram_law_with_norm ℂ (r-v) (s-v)
  have hsum : (r-v)+(s-v) = (2 : ℂ) • ((1/2 : ℂ) • (r+s)-v) := by
    rw [smul_sub, smul_smul]
    norm_num
    module
  have hsub : (r-v)-(s-v) = r-s := by abel
  rw [hsum,hsub,norm_smul,mul_pow] at hp
  norm_num at hp
  simpa only [smul_add] using hp

/-- Strictness comes from the distance term, not from strict positivity of Q.
Every value passed to toReal is proved finite first. -/
theorem ClosedPositiveForm.minimizer_unique (Q : ClosedPositiveForm H)
    (v r s : H)
    (hr : ∀ w : H, ENNReal.ofReal (‖r-v‖^2) + Q.value r ≤
      ENNReal.ofReal (‖w-v‖^2) + Q.value w)
    (hs : ∀ w : H, ENNReal.ofReal (‖s-v‖^2) + Q.value s ≤
      ENNReal.ofReal (‖w-v‖^2) + Q.value w) : r = s := by
  have hrf : Q.value r < ⊤ := by
    have hh := hr 0
    simp only [Q.map_zero,add_zero] at hh
    exact lt_of_le_of_lt (le_trans le_add_self hh) ENNReal.ofReal_lt_top
  have hsf : Q.value s < ⊤ := by
    have hh := hs 0
    simp only [Q.map_zero,add_zero] at hh
    exact lt_of_le_of_lt (le_trans le_add_self hh) ENNReal.ofReal_lt_top
  let m := (1/2 : ℂ) • (r+s)
  obtain ⟨hmf,hmb⟩ := Q.midpoint_finite_and_bound r s hrf hsf
  have hmid : ENNReal.ofReal (‖m-v‖^2) + Q.value m ≠ ⊤ :=
    ENNReal.add_ne_top.mpr ⟨ENNReal.ofReal_ne_top,ne_of_lt hmf⟩
  have hrr := ENNReal.toReal_mono hmid (hr m)
  have hss := ENNReal.toReal_mono hmid (hs m)
  rw [ENNReal.toReal_add ENNReal.ofReal_ne_top (ne_of_lt hrf),
    ENNReal.toReal_add ENNReal.ofReal_ne_top (ne_of_lt hmf)] at hrr
  rw [ENNReal.toReal_add ENNReal.ofReal_ne_top (ne_of_lt hsf),
    ENNReal.toReal_add ENNReal.ofReal_ne_top (ne_of_lt hmf)] at hss
  simp only [ENNReal.toReal_ofReal (sq_nonneg _)] at hrr hss
  have hid := norm_midpoint_sub_identity v r s
  change 4*‖m-v‖^2+‖r-s‖^2 = _ at hid
  change (Q.value m).toReal ≤ _ at hmb
  have hz : ‖r-s‖ = 0 := by
    nlinarith only [hrr,hss,hmb,hid,sq_nonneg ‖r-s‖]
  exact sub_eq_zero.mp (norm_eq_zero.mp hz)

#print axioms ClosedPositiveForm.midpoint_finite_and_bound
#print axioms norm_midpoint_sub_identity
#print axioms ClosedPositiveForm.minimizer_unique
end
end TGLV350.Regular
