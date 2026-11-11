import TGLExt.F1Fecho394.R7SineWindowClosureProbeR5

/-! Cutoff and right-action consequences using the compiled first-resolvent module.
The full scaled trace/PF construction remains a later obligation.
No original or earlier attempt is replaced. -/
set_option autoImplicit false
set_option Elab.async false
set_option maxHeartbeats 600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
namespace F1Fecho.CanonicalFockPolarRight
open MeasureTheory Filter
open TGLV350.Regular (hilbertPositiveSqrt inverseCutoffFunction)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockRegularRightGNS F1Fecho.CanonicalFockWeightDomain
open F1Fecho.RegularPositiveFlow
open scoped Topology
theorem regularSpectralResolvent_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) :
    (⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩ :
      (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J := by
  let b (n : ℕ) : (core).toStarSubalgebra :=
    ⟨regularSineResolvent fockFlow ((n : ℝ)+1),(regularSineResolvent_right J hreg ((n : ℝ)+1)).choose⟩
  let B : (core).toStarSubalgebra :=
    ⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩
  have hb (n : ℕ) : b n ∈ scalarPolarRightAlgebra J :=
    (regularSineResolvent_right J hreg ((n : ℝ)+1)).choose_spec
  have hs (n : ℕ) : star (b n) = b n :=
    Subtype.ext (IsSelfAdjoint.of_nonneg (regularSineResolvent_nonneg fockFlow ((n : ℝ)+1))).star_eq
  have hB : star B = B :=
    Subtype.ext (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg fockFlow)).star_eq
  have hright : ScalarPolarRight J B := by
    intro A
    have ha : ∀ x, Tendsto (fun n => (star (b n)).val x) atTop (𝓝 ((star B).val x)) := by
      intro x
      simpa only [hs,hB] using regularSineResolvent_tendsto fockFlow x
    exact scalarRightAction_closed_of_bounded_strongStar J b B 1
      (fun n => regularSineResolvent_norm_le fockFlow ((n : ℝ)+1))
      (fun x => regularSineResolvent_tendsto fockFlow x) ha A (fun n => (hb n).1 A)
  change ScalarPolarRight J B ∧ ScalarPolarRight J (star B)
  rw [hB]
  exact ⟨hright,hright⟩



theorem regularInverseGeneratorCutoff_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (ε : ℝ) (hε : 0 < ε) :
    (⟨regularInverseGeneratorCutoff fockFlow ε,regularInverseGeneratorCutoff_mem fockFlow M ε⟩ :
      (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J := by
  have hm := lift_predicate_eq (fun T => T ∈ core)
    (fun z => z ∈ scalarPolarRightAlgebra J)
    (regularInverseGeneratorCutoff_cfc fockFlow ε hε)
    (scalarRightAction_cfc J
      ⟨regularSpectralResolvent fockFlow,regularSpectralResolvent_mem fockFlow M⟩
      (regularSpectralResolvent_right J hreg) (inverseCutoffFunction ε))
  exact hm.choose_spec



/-- Consume the standard real/complex CFC bridges for the original positive
square root; no independent root is introduced. -/
private theorem hilbertPositiveSqrt_complex_cfc
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T : H →L[ℂ] H) (h0 : 0 ≤ T) :
    hilbertPositiveSqrt T = cfc (fun z : ℂ => (Real.sqrt z.re : ℂ)) T := by
  rw [hilbertPositiveSqrt,CFC.sqrt_eq_real_sqrt _ h0,
    cfcₙ_eq_cfc Real.continuous_sqrt.continuousOn Real.sqrt_zero,
    cfc_real_eq_complex Real.sqrt (IsSelfAdjoint.of_nonneg h0)]

theorem scalarRightAction_sqrt (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : (core).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (h0 : 0 ≤ b.val) :
    ∃ h : hilbertPositiveSqrt b.val ∈ core,
      (⟨hilbertPositiveSqrt b.val,h⟩ : (core).toStarSubalgebra) ∈
        scalarPolarRightAlgebra J := by
  exact lift_predicate_eq (fun T => T ∈ core)
    (fun z => z ∈ scalarPolarRightAlgebra J)
    (hilbertPositiveSqrt_complex_cfc b.val h0)
    (scalarRightAction_cfc J b hb (fun z : ℂ => (Real.sqrt z.re : ℂ)))


theorem regularInverseGeneratorCutoff_sqrt_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow ε) ∈ core,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow ε),h⟩ :
        (core).toStarSubalgebra) ∈ scalarPolarRightAlgebra J :=
  scalarRightAction_sqrt J
    ⟨regularInverseGeneratorCutoff fockFlow ε,regularInverseGeneratorCutoff_mem fockFlow M ε⟩
    (regularInverseGeneratorCutoff_right J hreg ε hε) (regularInverseGeneratorCutoff_nonneg fockFlow ε hε)


end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineWindowCore
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineWindowCore_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineResolvent_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularSpectralResolvent_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularInverseGeneratorCutoff_right
#print axioms F1Fecho.CanonicalFockPolarRight.scalarRightAction_sqrt
#print axioms F1Fecho.CanonicalFockPolarRight.regularInverseGeneratorCutoff_sqrt_right


-- Separate cutoff component; commutation and weight order are not asserted here.
