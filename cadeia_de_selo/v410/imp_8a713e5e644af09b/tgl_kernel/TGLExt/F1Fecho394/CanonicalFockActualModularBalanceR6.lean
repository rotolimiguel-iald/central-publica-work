import TGLExt.F1Fecho394.GenericPolarModularBalanceR1
import TGLExt.F1Fecho394.GeneralRepresentedRegularResolventR4
import TGLExt.F1Fecho394.GeneralGNSVectorInjectivityR1
import TGLExt.F1Fecho394.CanonicalFockGNSOrderR4
import TGLExt.F1Fecho394.CanonicalFockRegularGNSR9
import TGLExt.F1Fecho394.CanonicalFockPolarFlipR4
import TGLExt.F1Fecho394.CanonicalFockConcreteSpecializationR2

/-! DECLARADO / UNCOMPILED CANDIDATE, 2026-10-16, codex-fock-r6-review.
Concrete bounded modular balance on the original scalar-weight Fock GNS.
R6 corrects only the complement-injectivity supplier name from the R5 attempt.
R3 stalled in native conjugate_right; R5/R6 consume its compiled R46 supplier.
The opposite conjugation and commutation transports are first proved on an
abstract Hilbert carrier, then specialized with the native dictionaries.
Each analytic premise is supplied by an existing concrete theorem. The final
balance has no premise: T, A, B and J are the existing constructed objects.
No replacement GNS, hreg, trace, modular identity, or balance input is added.
The double-cut limits, tracial law, total trace interface and PF remain open.
Require EXIT0 and all six requested axiom reports, not merely stage markers. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 12
noncomputable section
namespace F1Fecho.CanonicalFockActualModularBalanceR6
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace)
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open TGLV350.Regular (antiunitaryConjugate antiunitaryConjugateRealHom
  resolventDampingOperator resolventPhaseOperator resolventImaginaryPower)

-- Reducible aliases of existing native dictionaries, as in compiled R46.
private abbrev nativeNormedAddCommGroup : NormedAddCommGroup GNSHilbert := inferInstance
private abbrev nativeInnerProductSpace : InnerProductSpace ℂ GNSHilbert := inferInstance
private abbrev nativeNormedSpace : NormedSpace ℂ GNSHilbert := inferInstance
private abbrev nativeModule : Module ℂ GNSHilbert := inferInstance
private abbrev nativeTopologicalSpace : TopologicalSpace GNSHilbert := inferInstance
private abbrev nativeUniformSpace : UniformSpace GNSHilbert := inferInstance
private abbrev nativeCompleteSpace : CompleteSpace GNSHilbert :=
  F1Fecho.CanonicalFockGNS.gnsCompleteSpace
private abbrev nativeStar : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace
private abbrev nativeOrder : PartialOrder (GNSHilbert →L[ℂ] GNSHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := GNSHilbert)
attribute [local instance] nativeNormedAddCommGroup nativeInnerProductSpace
  nativeNormedSpace nativeModule nativeTopologicalSpace nativeUniformSpace
  nativeCompleteSpace nativeStar nativeOrder

private abbrev fockNormedAddCommGroup : NormedAddCommGroup F1Rede.BosonicFock.F := inferInstance
private abbrev fockInnerProductSpace : InnerProductSpace ℂ F1Rede.BosonicFock.F := inferInstance
private abbrev fockCompleteSpace : CompleteSpace F1Rede.BosonicFock.F := inferInstance

abbrev π : core.toStarSubalgebra →⋆ₐ[ℂ] (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation
abbrev T : GNSHilbert →L[ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent
abbrev J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor
abbrev r : core.toStarSubalgebra :=
  F1Fecho.RepresentedRegularResolvent.resolventElement fockFlow M
abbrev A : GNSHilbert →L[ℂ] GNSHilbert := π r
abbrev B : GNSHilbert →L[ℂ] GNSHilbert := antiunitaryConjugate (H := GNSHilbert) J A
abbrev L (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  π (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement t)
abbrev R (t : ℝ) : GNSHilbert →L[ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockRegularRightGNS.regularRightGNS t

private theorem conjugate_of_intertwining
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (j : H ≃ₛₗᵢ[starRingEnd ℂ] H) (U V : H →L[ℂ] H)
    (h : ∀ x, j (U x) = V (j x)) : antiunitaryConjugate j U = V := by
  apply ContinuousLinearMap.ext
  intro x
  exact (TGLV350.Regular.antiunitaryConjugate_apply j U x).trans
    ((h (j.symm x)).trans (congrArg (fun z : H => V z) (j.apply_symm_apply x)))

private theorem commute_of_conjugate_complement
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (j : H ≃ₛₗᵢ[starRingEnd ℂ] H) (S U V : H →L[ℂ] H)
    (hS : antiunitaryConjugate j S = 1-S)
    (hU : antiunitaryConjugate j U = V) (hSU : Commute S U) : Commute S V := by
  have h := hSU.map (antiunitaryConjugateRealHom j)
  change Commute (antiunitaryConjugate j S) (antiunitaryConjugate j U) at h
  rw [hS, hU] at h
  simpa only [sub_sub_cancel] using (Commute.one_left V).sub_left h

private theorem commute_conjugated_right
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (j : H ≃ₛₗᵢ[starRingEnd ℂ] H) (U V C : H →L[ℂ] H)
    (hU : antiunitaryConjugate j U = V) (hUC : Commute U C) :
    Commute (antiunitaryConjugate j C) V := by
  have h := hUC.map (antiunitaryConjugateRealHom j)
  change Commute (antiunitaryConjugate j U) (antiunitaryConjugate j C) at h
  rw [hU] at h
  exact h.symm

theorem conjugate_right (t : ℝ) :
    antiunitaryConjugate (H := GNSHilbert) J (R t) = L (-t) :=
  F1Fecho.CanonicalFockConcreteSpecializationR2.conjugate_regular_right t
#print axioms conjugate_right

private theorem conjugate_right_neg (t : ℝ) :
    antiunitaryConjugate (H := GNSHilbert) J (R (-t)) = L t :=
  (conjugate_right (-t)).trans (congrArg L (neg_neg t))

theorem conjugate_left (t : ℝ) :
    antiunitaryConjugate (H := GNSHilbert) J (L t) = R (-t) := by
  have h : antiunitaryConjugate (H := GNSHilbert) J
      (π (star (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement (-t)))) =
        R (-t) :=
    @conjugate_of_intertwining GNSHilbert nativeNormedAddCommGroup
      nativeInnerProductSpace nativeCompleteSpace J
      (π (star (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement (-t))))
      (R (-t))
      (F1Fecho.CanonicalFockRightPolar.scalarTomitaPolarFactor_regular_left (-t))
  have hs : star (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement (-t)) =
      F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement t :=
    (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement_star (-t)).trans
      (congrArg F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement (neg_neg t))
  have hp := congrArg (fun q : core.toStarSubalgebra =>
    antiunitaryConjugate (H := GNSHilbert) J (π q)) hs
  exact hp.symm.trans h
#print axioms conjugate_left

theorem represented_commutes (C : GNSHilbert →L[ℂ] GNSHilbert)
    (hC : ∀ t, Commute C (L t)) : Commute C A :=
  @F1Fecho.RepresentedRegularResolvent.represented_resolvent_commutes
    F1Rede.BosonicFock.F GNSHilbert fockNormedAddCommGroup fockInnerProductSpace
    fockCompleteSpace nativeNormedAddCommGroup nativeInnerProductSpace nativeCompleteSpace
    fockFlow M π
    (fun b q c hb hq x =>
      F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_tendsto_of_uniformly_bounded
        b q c hb hq x) C hC
#print axioms represented_commutes

private theorem representation_one : π (1 : core.toStarSubalgebra) =
    (1 : GNSHilbert →L[ℂ] GNSHilbert) := map_one π
private theorem representation_complement : π (1-r : core.toStarSubalgebra) =
    (1-A : GNSHilbert →L[ℂ] GNSHilbert) :=
  (map_sub π (1 : core.toStarSubalgebra) r).trans
    (congrArg (fun C : GNSHilbert →L[ℂ] GNSHilbert => C-A) representation_one)

private theorem T_nonneg : 0 ≤ T :=
  F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_nonneg
private theorem T_le_one : T ≤ 1 :=
  F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_le_one
private theorem T_injective : Function.Injective T :=
  F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_injective
private theorem T_complement_injective : Function.Injective (1-T : GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedTomitaFlow.scalarTomitaResolvent_complement_injective
    (H := GNSHilbert)
    F1Fecho.CanonicalFockWeightModularOperator.actualClosedInput
private theorem A_nonneg : 0 ≤ A :=
  F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_nonneg r
    (show 0 ≤ r from F1Fecho.RegularPositiveFlow.regularSpectralResolvent_nonneg fockFlow)
private theorem A_le_one : A ≤ 1 :=
  (F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_monotone
    (show r ≤ (1 : core.toStarSubalgebra) from
      F1Fecho.RegularPositiveFlow.regularSpectralResolvent_le_one fockFlow)).trans_eq
        representation_one
private theorem A_injective : Function.Injective A :=
  @F1Fecho.RegularScalarGNSRepresentation.representation_vector_injective
    F1Rede.BosonicFock.F fockNormedAddCommGroup fockInnerProductSpace fockCompleteSpace
    F1Fecho.CanonicalFockGNS.weightContext r
    (F1Fecho.RegularPositiveFlow.regularSpectralResolvent_injective fockFlow)
private theorem A_complement_injective : Function.Injective (1-A : GNSHilbert →L[ℂ] GNSHilbert) := by
  have hsource : Function.Injective (1-r : core.toStarSubalgebra).val :=
    F1Fecho.RegularPositiveFlow.regularSpectralResolvent_complement_injective fockFlow
  have hrepresented : Function.Injective (π (1-r : core.toStarSubalgebra)) :=
    @F1Fecho.RegularScalarGNSRepresentation.representation_vector_injective
      F1Rede.BosonicFock.F fockNormedAddCommGroup fockInnerProductSpace fockCompleteSpace
      F1Fecho.CanonicalFockGNS.weightContext (1-r : core.toStarSubalgebra) hsource
  exact (congrArg (fun C : GNSHilbert →L[ℂ] GNSHilbert => Function.Injective C)
    representation_complement).mp hrepresented
private theorem polar_flip : antiunitaryConjugate (H := GNSHilbert) J T = 1-T :=
  F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolar_conjugate_resolvent

private theorem T_commutes_left (t : ℝ) : Commute T (L t) :=
  @commute_of_conjugate_complement GNSHilbert nativeNormedAddCommGroup
    nativeInnerProductSpace nativeCompleteSpace J T (R (-t)) (L t)
    polar_flip (conjugate_right_neg t)
    (F1Fecho.CanonicalFockRightRoot.scalarTomitaResolvent_regular_right_commutes (-t))
theorem T_commutes_A : Commute T A := represented_commutes T T_commutes_left
#print axioms T_commutes_A

private theorem right_commutes_A (t : ℝ) : Commute (R t) A :=
  F1Fecho.CanonicalFockRegularGNS.regularRightGNS_commutes_left t r
private theorem B_commutes_left (t : ℝ) : Commute B (L t) :=
  @commute_conjugated_right GNSHilbert nativeNormedAddCommGroup
    nativeInnerProductSpace nativeCompleteSpace J (R (-t)) (L t) A
    (conjugate_right_neg t) (right_commutes_A (-t))
theorem A_commutes_B : Commute A B := (represented_commutes B B_commutes_left).symm
#print axioms A_commutes_B

private theorem left_damped_phase (t : ℝ) :
    L t * resolventDampingOperator (H := GNSHilbert) A =
      resolventPhaseOperator (H := GNSHilbert) A t :=
  @F1Fecho.RepresentedRegularResolvent.represented_damped_phase
    F1Rede.BosonicFock.F GNSHilbert fockNormedAddCommGroup fockInnerProductSpace
    fockCompleteSpace nativeNormedAddCommGroup nativeInnerProductSpace nativeCompleteSpace
    fockFlow M π t
private theorem modular_implementation (t : ℝ) (x : GNSHilbert) :
    resolventImaginaryPower (H := GNSHilbert) T T_nonneg T_le_one
      T_injective T_complement_injective t x = L t (R (-t) x) :=
  F1Fecho.CanonicalFockModularIdentification.actual_modular_implementation t x

theorem actual_balance :
    let B := antiunitaryConjugate (H := GNSHilbert) J A
    Commute T B ∧ Function.Injective B ∧ (1-T)*A*(1-B) = T*(1-A)*B :=
  @F1Fecho.PolarModularBalance.balance GNSHilbert nativeNormedAddCommGroup
    nativeInnerProductSpace nativeCompleteSpace T A J
    T_nonneg T_le_one T_injective T_complement_injective
    A_nonneg A_le_one A_injective A_complement_injective L R
    T_commutes_A polar_flip A_commutes_B left_damped_phase
    conjugate_left right_commutes_A modular_implementation
#print axioms actual_balance

end F1Fecho.CanonicalFockActualModularBalanceR6
