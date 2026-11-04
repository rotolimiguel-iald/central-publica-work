import TGLExt.F1Fecho394.CanonicalFockActualModularBalanceR6
import TGLExt.F1Fecho394.CanonicalFockActualRightCutoffsR2
import TGLExt.F1Fecho394.GenericPolarRightCommutationR2
import TGLExt.F1Fecho394.GeneralRepresentedDoubleCutR2

/-! DECLARADO / UNCOMPILED CANDIDATE, R48, 2026-10-16.
R2 corrects three supplier namespaces caught by source inspection before build.
Concrete double-cut balance on the original full-weight Fock GNS.
The existing generic theorem is specialized with native Hilbert dictionaries.
Its cross-commutant premise follows from the proved polar-right algebra
membership of the actual spectral resolvent; no hreg, balance or trace input
is introduced. The failed CanonicalFockRightCommutationR3 is not imported.
The star-star reduction is performed on an abstract algebra before the
concrete specialization, avoiding its native representation conversion.
All three public statements use the existing pi, T and J from R47.
Strong cutoff convergence, the root-cut supremum, traciality and PF are
separate remaining consumers. Require EXIT0 and the three axiom reports. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 8
noncomputable section
namespace F1Fecho.CanonicalFockActualDoubleCutR2
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace)
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockWeightCompletion (scalarWeightGNSEmbedding)
open F1Fecho.CanonicalFockPolarRight (scalarPolarRightAlgebra)
open F1Fecho.CanonicalFockActualModularBalanceR6 (π T J r A B)
open TGLV350.Regular (antiunitaryConjugate)

-- Reducible aliases of existing dictionaries; no new Hilbert structure.
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

abbrev c (ε : ℝ) : core.toStarSubalgebra :=
  F1Fecho.RepresentedDoubleCut.cutElement fockFlow M ε
abbrev p (ε : ℝ) : core.toStarSubalgebra :=
  F1Fecho.RegularPositiveFlow.regularDomainCut fockFlow M ε
abbrev C (ε : ℝ) : GNSHilbert →L[ℂ] GNSHilbert := π (c ε)
abbrev P (ε : ℝ) : GNSHilbert →L[ℂ] GNSHilbert := π (p ε)

-- All algebraic simplification stays on abstract carriers. The native call
-- below supplies the same full dense weight ideal and its actual left action.
private theorem right_algebra_commutes
    {𝒜 : Type*} {H : Type} [Ring 𝒜] [Algebra ℂ 𝒜] [StarRing 𝒜] [StarModule ℂ 𝒜]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : Submodule ℂ 𝒜) (Λ : N →ₗ[ℂ] H)
    (pi : 𝒜 →⋆ₐ[ℂ] (H →L[ℂ] H)) (j : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hdense : DenseRange Λ)
    (hleft : ∀ a : 𝒜, ∀ x : N, ∃ hx : a*x.val ∈ N,
      Λ ⟨a*x.val,hx⟩ = pi a (Λ x))
    (b : 𝒜)
    (hb : b ∈ F1Fecho.GenericPolarRightAlgebra.scalarPolarRightAlgebra N Λ pi j)
    (a : 𝒜) : Commute (antiunitaryConjugate (H := H) j (pi b)) (pi a) := by
  have h := F1Fecho.GenericPolarRightAlgebra.commutes_left_of_right_identity
    N Λ pi j hdense hleft (star b) hb.2 a
  simpa only [star_star] using h

private theorem actual_right_algebra_commutes
    (b : core.toStarSubalgebra) (hb : b ∈ scalarPolarRightAlgebra J)
    (a : core.toStarSubalgebra) :
    Commute (antiunitaryConjugate (H := GNSHilbert) J (π b)) (π a) :=
  @right_algebra_commutes core.toStarSubalgebra GNSHilbert
    inferInstance inferInstance inferInstance inferInstance
    nativeNormedAddCommGroup nativeInnerProductSpace nativeCompleteSpace
    scalarWeightLeftIdeal scalarWeightGNSEmbedding π J
    F1Fecho.CanonicalFockWeightSandwich.scalarWeightGNSEmbedding_denseRange
    (fun a x => ⟨(F1Fecho.CanonicalFockWeightSandwich.scalarWeightLeftProduct a x).property,
      (F1Fecho.CanonicalFockWeightSandwich.scalarWeightGNSAction_intertwines a x).symm⟩)
    b hb a

theorem resolvent_conjugate_commutes (a : core.toStarSubalgebra) :
    Commute B (π a) :=
  actual_right_algebra_commutes r
    F1Fecho.CanonicalFockActualRightCutoffs.actualRegularResolvent_right a
#print axioms resolvent_conjugate_commutes

theorem inverseCutoff_conjugate_commutes (ε : ℝ) (hε : 0 < ε)
    (a : core.toStarSubalgebra) :
    Commute (antiunitaryConjugate (H := GNSHilbert) J (C ε)) (π a) :=
  actual_right_algebra_commutes (c ε)
    (F1Fecho.CanonicalFockActualRightCutoffs.actualInverseCutoff_right ε hε) a
#print axioms inverseCutoff_conjugate_commutes

private theorem A_injective : Function.Injective A :=
  @F1Fecho.RegularScalarGNSRepresentation.representation_vector_injective
    F1Rede.BosonicFock.F fockNormedAddCommGroup fockInnerProductSpace fockCompleteSpace
    F1Fecho.CanonicalFockGNS.weightContext r
    (F1Fecho.RegularPositiveFlow.regularSpectralResolvent_injective fockFlow)
private theorem base_balance :
    Commute T B ∧ Function.Injective B ∧ (1-T)*A*(1-B) = T*(1-A)*B :=
  F1Fecho.CanonicalFockActualModularBalanceR6.actual_balance

/-- The two regulators are arbitrary positive reals. Every analytic premise of
    the generic represented theorem is discharged by the existing Fock objects. -/
theorem actual_double_cut (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    Commute T (C ε) ∧
    Commute T (antiunitaryConjugate (H := GNSHilbert) J (C η)) ∧
    (1-T)*C ε*antiunitaryConjugate (H := GNSHilbert) J (P η) =
      T*P ε*antiunitaryConjugate (H := GNSHilbert) J (C η) :=
  @F1Fecho.RepresentedDoubleCut.balance
    F1Rede.BosonicFock.F GNSHilbert fockNormedAddCommGroup fockInnerProductSpace
    fockCompleteSpace nativeNormedAddCommGroup nativeInnerProductSpace nativeCompleteSpace
    fockFlow M π T J F1Fecho.CanonicalFockActualModularBalanceR6.T_commutes_A
    base_balance.1 A_injective base_balance.2.1 base_balance.2.2
    F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolar_conjugate_resolvent
    resolvent_conjugate_commutes ε η hε hη
#print axioms actual_double_cut

end F1Fecho.CanonicalFockActualDoubleCutR2
