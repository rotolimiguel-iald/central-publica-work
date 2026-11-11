import TGLExt.F1Fecho394.GeneralRegularDualScalingR2
import TGLExt.F1Fecho394.GeneralRegularAffiliationR1
/-! The original v351 inverse-generator cutoff reused on any concrete
regular flow. The cutoff is the inverse of h+epsilon on the SAME graph,
and belongs to the SAME generic regular core. No trace is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular TGLExt ChatgptAudit
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
/-- B_epsilon=(h+epsilon)^{-1}, obtained from the existing resolvent by the
dual action. The inverse equation is proved below for epsilon>0. -/
def regularInverseGeneratorCutoff (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (ε : ℝ) :
    RegularHilbert (H) →L[ℂ] RegularHilbert (H) :=
  (ε⁻¹ : ℂ) • dualAmbient (Real.log ε) (regularSpectralResolvent B)

theorem regularInverseGeneratorCutoff_mem (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (ε : ℝ) :
    regularInverseGeneratorCutoff B ε ∈ RegularCovariantCore.core B M := by
  have hm : dualAmbient (Real.log ε) (regularSpectralResolvent B) ∈ RegularCovariantCore.core B M :=
    (RegularCovariantCore.dualAction B M (Real.log ε)
      ⟨regularSpectralResolvent B,regularSpectralResolvent_mem B M⟩).property
  exact (RegularCovariantCore.core B M).toStarSubalgebra.smul_mem hm _

theorem regularInverseGeneratorCutoff_nonneg (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff B ε := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
    (dualAmbient_nonneg (Real.log ε) _ (regularSpectralResolvent_nonneg B))).smul_of_nonneg
  exact_mod_cast inv_nonneg.mpr hε.le

theorem regularInverseGeneratorCutoff_le (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff B ε ≤
      (ε⁻¹ : ℂ) • (1 : RegularHilbert (H) →L[ℂ] RegularHilbert (H)) := by
  have h := OrderHomClass.monotone (dualAmbient (H := H) (Real.log ε))
    (regularSpectralResolvent_le_one B)
  rw [map_one] at h
  apply sub_nonneg.mp
  rw [regularInverseGeneratorCutoff, ← smul_sub]
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ((ContinuousLinearMap.nonneg_iff_isPositive _).mp (sub_nonneg.mpr h)).smul_of_nonneg
  exact_mod_cast inv_nonneg.mpr hε.le

theorem regularInverseGeneratorCutoff_one (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) :
    regularInverseGeneratorCutoff B 1 = regularSpectralResolvent B := by
  simp only [regularInverseGeneratorCutoff, Complex.ofReal_one, inv_one, Real.log_one,
    dualAmbient_zero, one_smul]
  rfl

/-- The image belongs to the domain of the same h and solves (h+epsilon)y=x. -/
theorem regularInverseGeneratorCutoff_graph (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (ε : ℝ) (hε : 0 < ε)
    (x : RegularHilbert (H)) :
    (regularInverseGeneratorCutoff B ε x,
      x-(ε : ℂ) • regularInverseGeneratorCutoff B ε x) ∈
        (regularPositiveGenerator B).graph := by
  let R := regularSpectralResolvent B
  let s := Real.log ε
  let z := characterMultiplier (-s) x
  have hg : (R z,z-R z) ∈ (regularPositiveGenerator B).graph := by
    change (R z,z-R z) ∈ (resolventGraphOperator R (regularSpectralResolvent_injective B)).graph
    rw [resolvent_graph_equation]
    change R z-R (R z) = R (z-R z)
    rw [map_sub]
  have ht := regularPositiveGenerator_dual_graph B s (R z) (z-R z) hg
  have hs : Real.exp s = ε := Real.exp_log hε
  have hi : characterMultiplier s z = x := characterMultiplier_inverse s x
  have he : (ε : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr hε.ne'
  have hc : regularInverseGeneratorCutoff B ε x =
      (ε⁻¹ : ℂ) • characterMultiplier s (R z) := by
    rw [regularInverseGeneratorCutoff,dualAmbient_apply,characterMultiplier_star]
    rfl
  have hx : (ε : ℂ) • regularInverseGeneratorCutoff B ε x = characterMultiplier s (R z) := by
    rw [hc,smul_smul,mul_inv_cancel₀ he,one_smul]
  have hh := (regularPositiveGenerator B).graph.smul_mem (ε⁻¹ : ℂ) ht
  change ((ε⁻¹ : ℂ) • characterMultiplier s (R z),
    (ε⁻¹ : ℂ) • ((Real.exp s : ℂ) • characterMultiplier s (z-R z))) ∈ _ at hh
  rw [hs,smul_smul,inv_mul_cancel₀ he,one_smul,map_sub,hi,← hc,← hx] at hh
  exact hh

/-- The regulator transforms together with the cutoff. Its sign follows
from the already proved dual action on the generator. -/
theorem regularInverseGeneratorCutoff_dual (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (ε : ℝ) (hε : 0 < ε)
    (s : ℝ) :
    dualAmbient s (regularInverseGeneratorCutoff B ε) =
      (Real.exp s : ℂ) • regularInverseGeneratorCutoff B (ε*Real.exp s) := by
  unfold regularInverseGeneratorCutoff
  rw [map_smul]
  have ht : dualAmbient s (dualAmbient (Real.log ε) (regularSpectralResolvent B)) =
      dualAmbient (Real.log ε+s) (regularSpectralResolvent B) := by
    rw [dualAmbient_add]
    rfl
  rw [ht,Real.log_mul hε.ne' (Real.exp_ne_zero s),Real.log_exp,smul_smul]
  have he : (Real.exp s : ℂ) * ((ε*Real.exp s)⁻¹ : ℂ) = (ε⁻¹ : ℂ) := by
    push_cast
    field_simp
  rw [Complex.ofReal_mul,he]

/-- Both inverse directions on the actual graph; uniqueness uses positivity,
without a spectral gap for h itself. -/
theorem regularInverseGeneratorCutoff_graph_iff (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (ε : ℝ) (hε : 0 < ε)
    (x y : RegularHilbert (H)) :
    (x,y) ∈ (regularPositiveGenerator B).graph ↔
      regularInverseGeneratorCutoff B ε (y+(ε : ℂ) • x) = x := by
  constructor
  · intro hxy
    let u := regularInverseGeneratorCutoff B ε (y+(ε : ℂ) • x)
    have hu := regularInverseGeneratorCutoff_graph B ε hε (y+(ε : ℂ) • x)
    have hd : (u-x,-(ε : ℂ) • (u-x)) ∈ (regularPositiveGenerator B).graph := by
      have hh := (regularPositiveGenerator B).graph.sub_mem hu hxy
      change (u-x,(y+(ε : ℂ) • x-(ε : ℂ) • u)-y) ∈ _ at hh
      have he : (y+(ε : ℂ) • x-(ε : ℂ) • u)-y = -(ε : ℂ) • (u-x) := by
        rw [neg_smul,smul_sub]
        abel
      rwa [he] at hh
    obtain ⟨v,hv,hh⟩ := (LinearPMap.mem_graph_iff (regularPositiveGenerator B)).mp hd
    have hp := regularPositiveGenerator_positive B v
    rw [hh,hv,inner_smul_right,Complex.mul_re,Complex.neg_re,Complex.ofReal_re,
      Complex.neg_im,Complex.ofReal_im,neg_zero,zero_mul,sub_zero] at hp
    change 0 ≤ -ε * RCLike.re (inner ℂ (u-x) (u-x)) at hp
    rw [inner_self_eq_norm_sq] at hp
    have hn : ‖u-x‖ = 0 := by
      have hm : ε * ‖u-x‖^2 ≤ 0 := by linarith
      have hsq : ‖u-x‖^2 ≤ 0 := by
        by_contra h
        have hpos := mul_pos hε (lt_of_not_ge h)
        linarith
      nlinarith [norm_nonneg (u-x)]
    exact sub_eq_zero.mp (norm_eq_zero.mp hn)
  · intro h
    have hh := regularInverseGeneratorCutoff_graph B ε hε (y+(ε : ℂ) • x)
    rw [h] at hh
    simpa only [add_sub_cancel_right] using hh


end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_mem
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_nonneg
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_le
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_one
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_graph
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_dual
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_graph_iff
