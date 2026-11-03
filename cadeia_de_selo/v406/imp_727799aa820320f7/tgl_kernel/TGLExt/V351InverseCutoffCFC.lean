import TGLExt.V351SineResolventApprox
import TGLExt.V351InverseGeneratorCutoff

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory Filter
noncomputable section

/-- Globally continuous extension of t/(1+(epsilon-1)t) from [0,1].
The regulator is required positive in the consuming theorems. -/
def inverseCutoffFunction (ε : ℝ) (z : ℂ) : ℂ :=
  (z.re / max (min 1 ε) (1+(ε-1)*z.re) : ℝ)

theorem inverseCutoffFunction_continuous (ε : ℝ) (hε : 0 < ε) :
    Continuous (inverseCutoffFunction ε) := by
  have hm : 0 < min (1 : ℝ) ε := lt_min zero_lt_one hε
  unfold inverseCutoffFunction
  apply Complex.continuous_ofReal.comp
  exact Complex.continuous_re.div (continuous_const.max
    (continuous_const.add (continuous_const.mul Complex.continuous_re)))
    (fun z => ne_of_gt (hm.trans_le (le_max_left _ _)))

theorem inverseCutoffFunction_sigmoid (ε a : ℝ) (hε : 0 < ε) :
    inverseCutoffFunction ε (Real.sigmoid a) = ((ε+Real.exp (-a))⁻¹ : ℝ) := by
  have hq0 := Real.sigmoid_nonneg a
  have hq1 := Real.sigmoid_le_one a
  have hd : min (1 : ℝ) ε ≤ 1+(ε-1)*Real.sigmoid a := by
    have h1 := mul_nonneg (sub_nonneg.mpr hq1) (sub_nonneg.mpr (min_le_left (1 : ℝ) ε))
    have h2 := mul_nonneg hq0 (sub_nonneg.mpr (min_le_right (1 : ℝ) ε))
    nlinarith
  have hq := Real.sigmoid_pos a
  have he : 0 < ε+Real.exp (-a) := add_pos hε (Real.exp_pos _)
  have hid : Real.sigmoid a * (1+Real.exp (-a)) = 1 := by
    rw [Real.sigmoid_def,inv_mul_cancel₀ (ne_of_gt (by positivity : 0 < 1+Real.exp (-a)))]
  have hden : 1+(ε-1)*Real.sigmoid a = (ε+Real.exp (-a))*Real.sigmoid a := by
    nlinarith
  unfold inverseCutoffFunction
  rw [Complex.ofReal_re,max_eq_right hd,hden]
  congr 1
  field_simp

private theorem regularResolvent_cfc_coordinate (P : SiteProfile)
    (f : ℂ → ℂ) (hf : Continuous f) (x : RegularHilbert (TowerHilbert P)) :
    (regularSpectralCoordinates P).symm (cfc f (regularSpectralResolvent P) x) =ᵐ[volume]
      fun ξ => f (Real.sigmoid (2*Real.pi*ξ)) • ((regularSpectralCoordinates P).symm x) ξ := by
  let V := regularSpectralCoordinates P
  let M := realScalarMultiplier (H := TowerHilbert P) (fun ξ => Real.sigmoid (2*Real.pi*ξ))
    (by fun_prop) (fun ξ => Real.sigmoid_nonneg _) (fun ξ => Real.sigmoid_le_one _)
  have hM : 0 ≤ M := realScalarMultiplier_nonneg _ _ _ _
  have hc := StarAlgHomClass.map_cfc V.conjStarAlgEquiv f M hf.continuousOn
    (StarAlgEquiv.isometry V.conjStarAlgEquiv).continuous
    (IsSelfAdjoint.of_nonneg hM).isStarNormal
    (IsSelfAdjoint.of_nonneg (map_nonneg V.conjStarAlgEquiv hM)).isStarNormal
  change V.symm (cfc f (V.conjStarAlgEquiv M) x) =ᵐ[volume] _
  rw [← hc]
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,LinearIsometryEquiv.symm_apply_apply]
  exact realScalarMultiplier_cfc_ae _ _ _ _ f hf (V.symm x)

/-- Identify the existing inverse by its already proved graph equation.
There is no new inverse, generator, or change of representation. -/
theorem regularInverseGeneratorCutoff_cfc (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε =
      cfc (inverseCutoffFunction ε) (regularSpectralResolvent P) := by
  ext1 x
  let Y := cfc (inverseCutoffFunction ε) (regularSpectralResolvent P)
  let V := regularSpectralCoordinates P
  have hh : (Y x,x-(ε : ℂ) • Y x) ∈ (regularPositiveGenerator P).graph := by
    rw [regularPositiveGenerator_graph_iff,map_sub,map_smul]
    filter_upwards [regularResolvent_cfc_coordinate P (inverseCutoffFunction ε)
        (inverseCutoffFunction_continuous ε hε) x,
      Lp.coeFn_sub (V.symm x) ((ε : ℂ) • V.symm (Y x)),
      Lp.coeFn_smul (ε : ℂ) (V.symm (Y x))] with ξ hy hs hm
    change (V.symm x-(ε : ℂ) • V.symm (Y x)) ξ =
      (Real.exp (-(2*Real.pi*ξ)) : ℂ) • (V.symm (Y x)) ξ
    rw [hs,Pi.sub_apply,hm,Pi.smul_apply]
    change (V.symm x) ξ-(ε : ℂ) • (V.symm (Y x)) ξ =
      (Real.exp (-(2*Real.pi*ξ)) : ℂ) • (V.symm (Y x)) ξ
    have hy' : (V.symm (Y x)) ξ =
        inverseCutoffFunction ε (Real.sigmoid (2*Real.pi*ξ)) • (V.symm x) ξ := hy
    rw [hy',inverseCutoffFunction_sigmoid ε _ hε]
    have hc : (1 : ℂ)-(ε : ℂ)*(((ε+Real.exp (-(2*Real.pi*ξ)))⁻¹ : ℝ) : ℂ) =
        (Real.exp (-(2*Real.pi*ξ)) : ℂ) *
          (((ε+Real.exp (-(2*Real.pi*ξ)))⁻¹ : ℝ) : ℂ) := by
      have hn : (ε+Real.exp (-(2*Real.pi*ξ)) : ℂ) ≠ 0 := by
        exact_mod_cast ne_of_gt (add_pos hε (Real.exp_pos (-(2*Real.pi*ξ))))
      simp only [Complex.ofReal_inv,Complex.ofReal_add]
      field_simp [hn]
      ring
    simpa only [sub_smul,one_smul,smul_smul] using congrArg (fun c : ℂ => c • (V.symm x) ξ) hc
  have hi := (regularInverseGeneratorCutoff_graph_iff P ε hε (Y x) (x-(ε : ℂ) • Y x)).mp hh
  simpa only [sub_add_cancel] using hi

theorem regularInverseGeneratorCutoff_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    (⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P := by
  obtain ⟨h,hb⟩ := scalarRightAction_cfc P
    ⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩
    (regularSpectralResolvent_right P) (inverseCutoffFunction ε)
  have he : (⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) = ⟨cfc (inverseCutoffFunction ε) (regularSpectralResolvent P),h⟩ :=
    Subtype.ext (regularInverseGeneratorCutoff_cfc P ε hε)
  rw [he]
  exact hb

/-- Consume the standard real/complex CFC bridges for the original positive
square root; no independent root is introduced. -/
private theorem hilbertPositiveSqrt_complex_cfc
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (h0 : 0 ≤ T) :
    hilbertPositiveSqrt T = cfc (fun z : ℂ => (Real.sqrt z.re : ℂ)) T := by
  rw [hilbertPositiveSqrt,CFC.sqrt_eq_real_sqrt _ h0,
    cfcₙ_eq_cfc Real.continuous_sqrt.continuousOn Real.sqrt_zero,
    cfc_real_eq_complex Real.sqrt (IsSelfAdjoint.of_nonneg h0)]

theorem scalarRightAction_sqrt (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (h0 : 0 ≤ b.val) :
    ∃ h : hilbertPositiveSqrt b.val ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt b.val,h⟩ : (regularCoreAlgebra P).toStarSubalgebra) ∈
        scalarPolarRightAlgebra P := by
  rw [hilbertPositiveSqrt_complex_cfc _ h0]
  exact scalarRightAction_cfc P b hb _

theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P :=
  scalarRightAction_sqrt P
    ⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩
    (regularInverseGeneratorCutoff_right P ε hε) (regularInverseGeneratorCutoff_nonneg P ε hε)

#print axioms inverseCutoffFunction
#print axioms inverseCutoffFunction_continuous
#print axioms inverseCutoffFunction_sigmoid
#print axioms regularInverseGeneratorCutoff_cfc
#print axioms regularInverseGeneratorCutoff_right
#print axioms scalarRightAction_sqrt
#print axioms regularInverseGeneratorCutoff_sqrt_right
end
end TGLV350.Regular
