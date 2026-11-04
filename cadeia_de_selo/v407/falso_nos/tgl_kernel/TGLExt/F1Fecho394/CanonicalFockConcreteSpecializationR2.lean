import TGLExt.F1Fecho394.CanonicalFockRightPolarBridgeR5
import TGLExt.F1Fecho394.GenericHilbertStarNormOrderR1
import TGLExt.F1Fecho394.CanonicalFockGNSOrderR4

/-! R46 candidate, 2026-10-16. R1 printed all five declarations with the trio,
but EXIT1 rejected the local irreducibility attribute before the declarations.
This R2 removes that unsupported attribute; no unsafe reducibility override.
R44 showed that the native normed/inner/star dictionaries and native polar
witness agree, but even Hilbert-only generic specialization exhausts whnf.
This file caches the EXISTING concrete dictionaries while GNSHilbert is
transparent, with the original type abbreviation left transparent.
The generic norm/order applications receive their Hilbert dictionaries
explicitly. No replacement Hilbert space, transported norm, added premise,
new axiom, or larger heartbeat budget is introduced.
The three public consumer statements are the R5 statements unchanged.
The two Hilbert-only checks precede them so a failure has a bounded boundary.
A printed stage is not success: require EXIT0 and all five axiom reports.
Actual trace/PF and the complete R7 criterion remain open. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 12
noncomputable section
namespace F1Fecho.CanonicalFockConcreteSpecializationR2
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace)
open F1Fecho.CanonicalFockRegular (core)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockPolarRight (ScalarPolarRight)
open TGLV350.Regular (antiunitaryConjugate)

-- Capture native structures before changing elaborator transparency.
-- These are reducible aliases of the old dictionaries, not new structures.
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

-- Both typed aliases still denote the original representation and embedding.
private abbrev pi : core.toStarSubalgebra →⋆ₐ[ℂ] (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.CanonicalFockGNSRepresentation.scalarGNSRepresentation
private abbrev lambda : scalarWeightLeftIdeal →ₗ[ℂ] GNSHilbert :=
  F1Fecho.CanonicalFockWeightCompletion.scalarWeightGNSEmbedding

private theorem norm_from_polar_identity
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (B : H →L[ℂ] H) (u v : H)
    (h : u = antiunitaryConjugate (H := H) J B v) : ‖u‖ = ‖B (J.symm v)‖ :=
  (congrArg (fun z : H => ‖z‖) h).trans (J.norm_map (B (J.symm v)))

-- The proof-indexed witness is eliminated while its proposition is abstract.
-- This is the R4/R5 generic proof, with no concrete subtype cases tactic.
private theorem exists_norm_from_polar_identity
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    {P : Prop} (u : P → H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (B : H →L[ℂ] H) (v : H)
    (h : ∃ p : P, u p = antiunitaryConjugate (H := H) J B v) :
    ∃ p : P, ‖u p‖ = ‖B (J.symm v)‖ :=
  Exists.elim h (fun p hp =>
    Exists.intro p (norm_from_polar_identity (H := H) J B (u p) v hp))

-- Kernel conversion and the actual GNS orbit-closure definition are unchanged.
-- No irreducibility attribute: native dictionaries suffice in the measured R1 attempt.

theorem norm_specialization
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (B : GNSHilbert →L[ℂ] GNSHilbert) (u v : GNSHilbert)
    (h : u = antiunitaryConjugate (H := GNSHilbert) J B v) :
    ‖u‖ = ‖B (J.symm v)‖ :=
  @norm_from_polar_identity GNSHilbert nativeNormedAddCommGroup
    nativeInnerProductSpace nativeCompleteSpace J B u v h
#print axioms norm_specialization

theorem order_specialization
    (B C : GNSHilbert →L[ℂ] GNSHilbert)
    (hBC : B * star B ≤ C * star C) (v : GNSHilbert) :
    ‖star B v‖ ^ 2 ≤ ‖star C v‖ ^ 2 :=
  @F1Fecho.GenericHilbertStarNormOrder.star_apply_norm_sq_mono
    GNSHilbert nativeNormedAddCommGroup nativeInnerProductSpace
    nativeCompleteSpace B C hBC v
#print axioms order_specialization

theorem exists_rightProduct_norm
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert) (b : core.toStarSubalgebra)
    (hb : ScalarPolarRight J b) (A : scalarWeightLeftIdeal) :
    ∃ h : A.val * b ∈ scalarWeightLeftIdeal,
      ‖lambda ⟨A.val * b, h⟩‖ = ‖pi (star b) (J.symm (lambda A))‖ := by
  exact @exists_norm_from_polar_identity GNSHilbert nativeNormedAddCommGroup
    nativeInnerProductSpace nativeCompleteSpace
    (A.val * b ∈ scalarWeightLeftIdeal)
    (fun hmem => lambda ⟨A.val * b, hmem⟩)
    J (pi (star b)) (lambda A) (hb A)
#print axioms exists_rightProduct_norm

theorem represented_right_norm_squared_mono
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert) (b c : core.toStarSubalgebra)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal) :
    ‖pi (star b) (J.symm (lambda A))‖^2 ≤
      ‖pi (star c) (J.symm (lambda A))‖^2 := by
  have ho : pi (b * star b) ≤ pi (c * star c) :=
    F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_monotone hbc
  have hp : pi b * star (pi b) ≤ pi c * star (pi c) := by
    simpa only [map_mul, map_star] using ho
  have hstarb : pi (star b) = star (pi b) := map_star pi b
  have hstarc : pi (star c) = star (pi c) := map_star pi c
  have hn := order_specialization (pi b) (pi c) hp (J.symm (lambda A))
  calc
    ‖pi (star b) (J.symm (lambda A))‖^2 =
        ‖star (pi b) (J.symm (lambda A))‖^2 :=
      congrArg (fun D : GNSHilbert →L[ℂ] GNSHilbert =>
        ‖D (J.symm (lambda A))‖^2) hstarb
    _ ≤ ‖star (pi c) (J.symm (lambda A))‖^2 := hn
    _ = ‖pi (star c) (J.symm (lambda A))‖^2 :=
      (congrArg (fun D : GNSHilbert →L[ℂ] GNSHilbert =>
        ‖D (J.symm (lambda A))‖^2) hstarc).symm
#print axioms represented_right_norm_squared_mono

theorem conjugate_regular_right (t : ℝ) :
    antiunitaryConjugate (H := GNSHilbert) F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor
      (F1Fecho.CanonicalFockRegularRightGNS.regularRightGNS t) =
      pi (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement (-t)) := by
  have raw := F1Fecho.CanonicalFockRightPolar.scalarTomitaPolar_conjugate_regular_right t
  have checked :
      antiunitaryConjugate (H := GNSHilbert) F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor
        (F1Fecho.CanonicalFockRegularRightGNS.regularRightGNS t) =
        pi (star (F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement t)) := raw
  have hs := F1Fecho.CanonicalFockRegularRightGNS.regularRightCoreElement_star t
  have mapped := congrArg (fun b : core.toStarSubalgebra => pi b) hs
  exact checked.trans mapped
#print axioms conjugate_regular_right

end F1Fecho.CanonicalFockConcreteSpecializationR2
