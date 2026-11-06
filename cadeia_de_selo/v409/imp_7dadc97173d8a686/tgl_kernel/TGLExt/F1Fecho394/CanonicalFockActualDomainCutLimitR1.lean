import TGLExt.F1Fecho394.CanonicalFockActualModularBalanceR6
import TGLExt.F1Fecho394.GeneralRegularDomainCutR1

/-! DECLARADO / UNCOMPILED CANDIDATE, R48, 2026-10-16.
The actual domain cutoffs converge strongly to the identity on the same
full-weight Fock GNS. Positivity and the uniform contraction bound come
from regularDomainCut_bounds; the previously proved bounded-strong continuity
of the existing scalar GNS representation transports the actual limit.
No replacement representation or strong convergence premise is introduced.
This file is independent of the pending actual double-cut candidate.
The root-cut supremum, actual tracial identity and PF are still consumers.
Require terminal EXIT0 and all three axiom reports. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 8
noncomputable section
namespace F1Fecho.CanonicalFockActualDomainCutLimitR1
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace)
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open F1Fecho.CanonicalFockActualModularBalanceR6 (π J)
open TGLV350.Regular (antiunitaryConjugate RegularHilbert)
open Filter
open scoped Topology

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

abbrev domainCutElement (ε : ℝ) : core.toStarSubalgebra :=
  F1Fecho.RegularPositiveFlow.regularDomainCut fockFlow M ε
abbrev domainCut (ε : ℝ) : GNSHilbert →L[ℂ] GNSHilbert := π (domainCutElement ε)

private theorem represented_domainCut_limit
    {H K : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
    (Q : F1Fecho.RegularCovariantCore.UnitaryFlow H) (N : VonNeumannAlgebra H)
    (pi : (F1Fecho.RegularCovariantCore.core Q N).toStarSubalgebra →⋆ₐ[ℂ]
      (K →L[ℂ] K))
    (hstrong : ∀ (b : ℕ → (F1Fecho.RegularCovariantCore.core Q N).toStarSubalgebra)
      (a : (F1Fecho.RegularCovariantCore.core Q N).toStarSubalgebra) (k : ℝ),
      (∀ n, ‖(b n).val‖ ≤ k) →
      (∀ v, Tendsto (fun n => (b n).val v) atTop (𝓝 (a.val v))) →
      ∀ v, Tendsto (fun n => pi (b n) v) atTop (𝓝 (pi a v)))
    (v : K) :
    Tendsto (fun n : ℕ => pi
      (F1Fecho.RegularPositiveFlow.regularDomainCut Q N (1/((n : ℝ)+1))) v)
      atTop (𝓝 v) := by
  let q (n : ℕ) := F1Fecho.RegularPositiveFlow.regularDomainCut Q N (1/((n : ℝ)+1))
  have hb (n : ℕ) : ‖(q n).val‖ ≤ 1 := by
    have hq := F1Fecho.RegularPositiveFlow.regularDomainCut_bounds Q N
      (1/((n : ℝ)+1)) (by positivity)
    exact (CStarAlgebra.norm_le_norm_of_nonneg_of_le hq.1 hq.2).trans
      ContinuousLinearMap.norm_id_le
  have ht (x : RegularHilbert H) :
      Tendsto (fun n => (q n).val x) atTop
        (𝓝 ((1 : (F1Fecho.RegularCovariantCore.core Q N).toStarSubalgebra).val x)) := by
    change Tendsto (fun n => (q n).val x) atTop (𝓝 x)
    exact F1Fecho.RegularPositiveFlow.regularDomainCut_tendsto_identity Q N x
  have he := hstrong q 1 1 hb ht v
  simpa only [map_one, one_apply_eq_self] using he

private theorem conjugate_strong_identity
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (j : H ≃ₛₗᵢ[starRingEnd ℂ] H) (Q : ℕ → H →L[ℂ] H)
    (hQ : ∀ v, Tendsto (fun n => Q n v) atTop (𝓝 v)) (v : H) :
    Tendsto (fun n => antiunitaryConjugate (H := H) j (Q n) v) atTop (𝓝 v) := by
  have he := j.continuous.continuousAt.tendsto.comp (hQ (j.symm v))
  change Tendsto (fun n => j (Q n (j.symm v))) atTop (𝓝 v)
  simpa only [LinearIsometryEquiv.apply_symm_apply, Function.comp_def] using he

theorem domainCut_bounds (ε : ℝ) (hε : 0 < ε) :
    0 ≤ domainCut ε ∧ domainCut ε ≤ 1 :=
  ⟨F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_nonneg (domainCutElement ε)
      (show 0 ≤ domainCutElement ε from
        (F1Fecho.RegularPositiveFlow.regularDomainCut_bounds fockFlow M ε hε).1),
    (F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_monotone
      (show domainCutElement ε ≤ (1 : core.toStarSubalgebra) from
        (F1Fecho.RegularPositiveFlow.regularDomainCut_bounds fockFlow M ε hε).2)).trans_eq
        (map_one π)⟩
#print axioms domainCut_bounds

theorem domainCut_tendsto_identity (v : GNSHilbert) :
    Tendsto (fun n : ℕ => domainCut (1/((n : ℝ)+1)) v) atTop (𝓝 v) :=
  @represented_domainCut_limit F1Rede.BosonicFock.F GNSHilbert
    fockNormedAddCommGroup fockInnerProductSpace fockCompleteSpace
    nativeNormedAddCommGroup nativeInnerProductSpace nativeCompleteSpace fockFlow M π
    (fun b a k hb ht x =>
      F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_tendsto_of_uniformly_bounded
        b a k hb ht x) v
#print axioms domainCut_tendsto_identity

theorem domainCut_conjugate_tendsto_identity (v : GNSHilbert) :
    Tendsto (fun n : ℕ => antiunitaryConjugate (H := GNSHilbert) J
      (domainCut (1/((n : ℝ)+1))) v) atTop (𝓝 v) :=
  @conjugate_strong_identity GNSHilbert nativeNormedAddCommGroup
    nativeInnerProductSpace nativeCompleteSpace J
    (fun n => domainCut (1/((n : ℝ)+1))) domainCut_tendsto_identity v
#print axioms domainCut_conjugate_tendsto_identity

end F1Fecho.CanonicalFockActualDomainCutLimitR1
