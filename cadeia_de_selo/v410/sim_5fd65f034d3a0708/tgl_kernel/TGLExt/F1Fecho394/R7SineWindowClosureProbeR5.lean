import TGLExt.F1Fecho394.CanonicalFockPolarRightClosureR10

/-! Bounded synchronous diagnostic: first resolvent only, with direct file markers.
Alternative to R10: do not import both modules with duplicate declaration names.
Explicit ambient CFC carrier and arguments; remove GNS instances only from CFC block.
Mathematical statement text and the two GNS consumer proof bodies are preserved. -/

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
/-- An explicit bounded combination of the original regular translations. -/
def regularSineWindowCore (m : ℝ) :
    (core).toStarSubalgebra :=
  (1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
    (regularRightCoreElement (-1/m) - regularRightCoreElement (1/m))

theorem regularSineWindowCore_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t, regularRightCoreElement t ∈ scalarPolarRightAlgebra J) (m : ℝ) :
    regularSineWindowCore m ∈ scalarPolarRightAlgebra J := by
  apply (scalarPolarRightAlgebra J).add_mem
  · exact (scalarPolarRightAlgebra J).smul_mem (scalarPolarRightAlgebra J).one_mem _
  · exact (scalarPolarRightAlgebra J).smul_mem ((scalarPolarRightAlgebra J).sub_mem
      (hreg (-1/m))
      (hreg (1/m))) _

theorem regularSineWindow_val (m : ℝ) :
    (regularSineWindowCore m).val=regularSineWindow fockFlow m := by rfl

theorem regularSineWindow_cfc_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t,regularRightCoreElement t∈scalarPolarRightAlgebra J) (m : ℝ) :
    ∃ hf : cfc (fun z : ℂ=>(Real.sigmoid (m*(2*z.re-1)):ℂ))
        (regularSineWindowCore m).val∈core.toStarSubalgebra,
      (⟨cfc (fun z : ℂ=>(Real.sigmoid (m*(2*z.re-1)):ℂ))
        (regularSineWindowCore m).val,hf⟩ : core.toStarSubalgebra)∈scalarPolarRightAlgebra J := by
  exact scalarRightAction_cfc J (regularSineWindowCore m)
    (regularSineWindowCore_right J hreg m) _

/-- Equality transport before specializing the concrete Fock carrier. -/
private theorem hilbert_cfc_operator_congr
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (f : ℂ → ℂ) {x y : H →L[ℂ] H} (h : x = y) : cfc f x = cfc f y := by
  exact congrArg (fun T : H →L[ℂ] H => cfc f T) h

theorem regularSineResolvent_eq_window_cfc (m : ℝ) :
    regularSineResolvent fockFlow m=
      cfc (fun z : ℂ=>(Real.sigmoid (m*(2*z.re-1)):ℂ)) (regularSineWindowCore m).val := by
  exact (regularSineResolvent_cfc fockFlow m).trans
    (hilbert_cfc_operator_congr _ (regularSineWindow_val m).symm)

theorem lift_predicate_eq {X : Type*} (P : X→Prop) (Q : Subtype P→Prop)
    {x y : X} (hxy : x=y) (hy : ∃h : P y,Q ⟨y,h⟩) : ∃h : P x,Q ⟨x,h⟩ := by
  cases hxy
  exact hy

theorem regularSineResolvent_right (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (hreg : ∀t,regularRightCoreElement t∈scalarPolarRightAlgebra J) (m : ℝ) :
    ∃ h : regularSineResolvent fockFlow m∈core,
      (⟨regularSineResolvent fockFlow m,h⟩ : core.toStarSubalgebra)∈scalarPolarRightAlgebra J := by
  exact lift_predicate_eq (fun T=>T∈core) (fun z=>z∈scalarPolarRightAlgebra J)
    (regularSineResolvent_eq_window_cfc m) (regularSineWindow_cfc_right J hreg m)

end F1Fecho.CanonicalFockPolarRight
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineWindowCore_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineWindow_cfc_right
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineResolvent_eq_window_cfc
#print axioms F1Fecho.CanonicalFockPolarRight.regularSineResolvent_right
