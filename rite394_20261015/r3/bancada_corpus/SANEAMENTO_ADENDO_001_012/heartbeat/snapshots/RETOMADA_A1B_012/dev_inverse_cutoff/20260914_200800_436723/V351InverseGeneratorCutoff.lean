import TGLExt.V351RegularGeneratorDualScaling

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section

/-- B_epsilon=(h+epsilon)^{-1}, obtained from the existing resolvent by the
dual action. The inverse equation is proved below for epsilon>0. -/
def regularInverseGeneratorCutoff (P : SiteProfile) (ε : ℝ) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) :=
  ε⁻¹ • dualAmbient (Real.log ε) (regularSpectralResolvent P)

theorem regularInverseGeneratorCutoff_mem (P : SiteProfile) (ε : ℝ) :
    regularInverseGeneratorCutoff P ε ∈ regularCoreAlgebra P := by
  have hm : dualAmbient (Real.log ε) (regularSpectralResolvent P) ∈ regularCoreAlgebra P :=
    (regularDualAction P (Real.log ε)
      ⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩).property
  change (ε⁻¹ : ℝ) • dualAmbient (Real.log ε) (regularSpectralResolvent P) ∈ _
  rw [real_smul]
  exact (regularCoreAlgebra P).toStarSubalgebra.smul_mem hm _

theorem regularInverseGeneratorCutoff_nonneg (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff P ε :=
  smul_nonneg (inv_nonneg.mpr hε.le)
    (dualAmbient_nonneg _ _ (regularSpectralResolvent_nonneg P))

theorem regularInverseGeneratorCutoff_le (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε ≤
      ε⁻¹ • (1 : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) := by
  have h := OrderHomClass.monotone (dualAmbient (H := TowerHilbert P) (Real.log ε))
    (regularSpectralResolvent_le_one P)
  rw [map_one] at h
  exact smul_le_smul_of_nonneg_left h (inv_nonneg.mpr hε.le)

theorem regularInverseGeneratorCutoff_one (P : SiteProfile) :
    regularInverseGeneratorCutoff P 1 = regularSpectralResolvent P := by
  simp only [regularInverseGeneratorCutoff, inv_one, Real.log_one, dualAmbient_zero,
    StarAlgEquiv.refl_apply, one_smul]

/-- The image belongs to the domain of the same h and solves (h+epsilon)y=x. -/
theorem regularInverseGeneratorCutoff_graph (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (x : RegularHilbert (TowerHilbert P)) :
    (regularInverseGeneratorCutoff P ε x,
      x-(ε : ℂ) • regularInverseGeneratorCutoff P ε x) ∈
        (regularPositiveGenerator P).graph := by
  let R := regularSpectralResolvent P
  let s := Real.log ε
  let z := characterMultiplier (-s) x
  have hg : (R z,z-R z) ∈ (regularPositiveGenerator P).graph := by
    change (R z,z-R z) ∈ (resolventGraphOperator R (regularSpectralResolvent_injective P)).graph
    rw [resolvent_graph_equation]
    change R z-R (R z) = R (z-R z)
    rw [map_sub]
  have ht := regularPositiveGenerator_dual_graph P s (R z) (z-R z) hg
  have hs : Real.exp s = ε := Real.exp_log hε
  have hi : characterMultiplier s z = x := characterMultiplier_inverse s x
  have he : (ε : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr hε.ne'
  have hc : regularInverseGeneratorCutoff P ε x =
      (ε⁻¹ : ℂ) • characterMultiplier s (R z) := by
    rw [regularInverseGeneratorCutoff,dualAmbient_apply,characterMultiplier_star]
    rfl
  have hx : (ε : ℂ) • regularInverseGeneratorCutoff P ε x = characterMultiplier s (R z) := by
    rw [hc,smul_smul,mul_inv_cancel₀ he,one_smul]
  have hh := (regularPositiveGenerator P).graph.smul_mem (ε⁻¹ : ℂ) ht
  change ((ε⁻¹ : ℂ) • characterMultiplier s (R z),
    (ε⁻¹ : ℂ) • ((Real.exp s : ℂ) • characterMultiplier s (z-R z))) ∈ _ at hh
  rw [hs,smul_smul,inv_mul_cancel₀ he,one_smul,map_sub,hi,← hc,← hx] at hh
  exact hh

/-- The regulator transforms together with the cutoff. Its sign follows
from the already proved dual action on the generator. -/
theorem regularInverseGeneratorCutoff_dual (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (s : ℝ) :
    dualAmbient s (regularInverseGeneratorCutoff P ε) =
      Real.exp s • regularInverseGeneratorCutoff P (ε*Real.exp s) := by
  unfold regularInverseGeneratorCutoff
  rw [real_smul,real_smul,real_smul,map_smul]
  have ht : dualAmbient s (dualAmbient (Real.log ε) (regularSpectralResolvent P)) =
      dualAmbient (Real.log ε+s) (regularSpectralResolvent P) := by
    rw [dualAmbient_add]
    rfl
  rw [ht,Real.log_mul hε.ne' (Real.exp_ne_zero s),Real.log_exp,smul_smul]
  have he : (Real.exp s : ℂ) * ((ε*Real.exp s)⁻¹ : ℝ) = (ε⁻¹ : ℝ) := by
    push_cast
    field_simp
  rw [he]

#print axioms regularInverseGeneratorCutoff
#print axioms regularInverseGeneratorCutoff_mem
#print axioms regularInverseGeneratorCutoff_nonneg
#print axioms regularInverseGeneratorCutoff_le
#print axioms regularInverseGeneratorCutoff_one
#print axioms regularInverseGeneratorCutoff_graph
#print axioms regularInverseGeneratorCutoff_dual
end
end TGLV350.Regular
