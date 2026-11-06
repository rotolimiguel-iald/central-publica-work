import TGLExt.F1Fecho394.CanonicalFockConcreteSpecializationR2
import TGLExt.F1Fecho394.CanonicalFockWeightSandwichR5
import TGLExt.F1Fecho394.CanonicalFockActualRightCutoffsR2
import TGLExt.F1Fecho394.GeneralInverseAdditivityR3
import TGLExt.F1Fecho394.GeneralCutoffAverageCommutationR1
import TGLExt.F1Fecho394.GeneralRegulatorOrderR1
import TGLExt.F1Fecho394.CanonicalFockInverseSupremumR2
import TGLExt.F1Fecho394.CanonicalFockWeightInvarianceR4

/-! DECLARADO / UNCOMPILED CANDIDATE, 2026-10-16, codex-fock-r6-review.
R1 compiled the first two statements with the standard axiom trio, but failed
at concrete sqrt rewriting in cutoff_antitone (line 151, isDefEq 400000).
R2 proves the sqrt-product order on an abstract star-subalgebra first, then
specializes it with the native RegularHilbert F dictionaries passed explicitly.
The actual core order remains the inherited ambient Loewner order. There is
no concrete rewrite matcher on the nested root/subtype expression in R2.
The five public statements and their premises are unchanged from R1.
The compiled ConcreteSpecializationR2 supplies the native right-product norm
and represented order. This consumer transports them to the SAME dual
quadratic integral, then proves regulator antitonicity and positive additivity
of the existing inverseSupremum. The actual cutoff membership is supplied by
the constructed scalarTomitaPolarFactor, without a new hreg premise.
The extension to every positive core element uses the existing finite-square
regular averages and their proved commutation with the cutoff square roots.
No new Hilbert model, weight, trace, or instance structure is defined here.
Internal normality is already supplied by CanonicalFockInverseNormalR1.
The modular balance, tracial law, total trace interface, and PF remain open.
Require terminal EXIT0 and all five axiom reports before calling this proved. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 8
noncomputable section
namespace F1Fecho.CanonicalFockActualInverseAdditivityR2
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace)
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open F1Fecho.CanonicalFockWeight (regularFockVacuum)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockWeightCompletion (scalarWeightGNSEmbedding)
open F1Fecho.CanonicalFockGNSRepresentation (scalarGNSRepresentation)
open F1Fecho.CanonicalFockPolarRight
  (ScalarPolarRight scalarPolarRightAlgebra scalarPolarRightAlgebra_mem_iff)
open F1Fecho.RegularPositiveFlow
open F1Fecho.RegularInverseWeight
open TGLV350.Regular (dualQuadraticIntegral hilbertPositiveSqrt HasFiniteDualSquare)
open scoped ENNReal

-- Reducible aliases of the native dictionaries, as in compiled R2.
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

private abbrev Ambient :=
  TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F →L[ℂ]
    TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F
private abbrev pi : core.toStarSubalgebra →⋆ₐ[ℂ] (GNSHilbert →L[ℂ] GNSHilbert) :=
  scalarGNSRepresentation
private abbrev lambda : scalarWeightLeftIdeal →ₗ[ℂ] GNSHilbert :=
  scalarWeightGNSEmbedding

private theorem star_product_square {𝒜 : Type*} [Ring 𝒜] [StarRing 𝒜] (a b : 𝒜) :
    star (a*b)*(a*b) = star b*(star a*a)*b := by
  simp only [star_mul, mul_assoc]

theorem scalarWeight_right_perturbed_norm
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b : core.toStarSubalgebra) (hb : b ∈ scalarPolarRightAlgebra J)
    (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val)
      regularFockVacuum =
    ENNReal.ofReal (‖pi (star b) (J.symm (lambda A))‖^2) := by
  have hright : ScalarPolarRight J b := ((scalarPolarRightAlgebra_mem_iff J b).mp hb).1
  -- Use the already specialized existential norm theorem. No concrete cases
  -- tactic and no generic Hilbert specialization is performed in this proof.
  have hn := F1Fecho.CanonicalFockConcreteSpecializationR2.exists_rightProduct_norm
    J b hright A
  let P : scalarWeightLeftIdeal := ⟨A.val*b, hn.choose⟩
  have hp : ‖lambda P‖ = ‖pi (star b) (J.symm (lambda A))‖ := hn.choose_spec
  have hv : P.val.val = A.val.val*b.val := rfl
  have hnorm : ENNReal.ofReal (‖lambda P‖^2) =
      dualQuadraticIntegral (star P.val.val*P.val.val) regularFockVacuum :=
    F1Fecho.CanonicalFockWeightSandwich.scalarWeightGNSEmbedding_norm_sq P
  have hsquare : star P.val.val*P.val.val =
      star (A.val.val*b.val)*(A.val.val*b.val) :=
    congrArg (fun D : Ambient => star D*D) hv
  have halg : star P.val.val*P.val.val = star b.val*(star A.val.val*A.val.val)*b.val :=
    hsquare.trans (star_product_square (𝒜 := Ambient) A.val.val b.val)
  have hweight :
      dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val)
        regularFockVacuum = ENNReal.ofReal (‖lambda P‖^2) :=
    (congrArg (fun D : Ambient => dualQuadraticIntegral D regularFockVacuum)
      halg.symm).trans hnorm.symm
  exact hweight.trans (congrArg (fun x : ℝ => ENNReal.ofReal (x^2)) hp)
#print axioms scalarWeight_right_perturbed_norm

theorem scalarWeight_right_perturbed_mono
    (J : GNSHilbert ≃ₛₗᵢ[starRingEnd ℂ] GNSHilbert)
    (b c : core.toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra J) (hc : c ∈ scalarPolarRightAlgebra J)
    (hbc : b*star b ≤ c*star c) (A : scalarWeightLeftIdeal) :
    dualQuadraticIntegral (star b.val*(star A.val.val*A.val.val)*b.val)
      regularFockVacuum ≤
    dualQuadraticIntegral (star c.val*(star A.val.val*A.val.val)*c.val)
      regularFockVacuum := by
  have hn : ‖pi (star b) (J.symm (lambda A))‖^2 ≤
      ‖pi (star c) (J.symm (lambda A))‖^2 :=
    F1Fecho.CanonicalFockConcreteSpecializationR2.represented_right_norm_squared_mono
      J b c hbc A
  calc
    _ = ENNReal.ofReal (‖pi (star b) (J.symm (lambda A))‖^2) :=
      scalarWeight_right_perturbed_norm J b hb A
    _ ≤ ENNReal.ofReal (‖pi (star c) (J.symm (lambda A))‖^2) :=
      ENNReal.ofReal_le_ofReal hn
    _ = _ := (scalarWeight_right_perturbed_norm J c hc A).symm
#print axioms scalarWeight_right_perturbed_mono

private theorem hilbert_sqrt_mul_star {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (B : H →L[ℂ] H) (hB : 0 ≤ B) :
    hilbertPositiveSqrt B*star (hilbertPositiveSqrt B) = B := by
  change CFC.sqrt B*star (CFC.sqrt B) = B
  rw [(CFC.sqrt_nonneg B).isSelfAdjoint.star_eq, CFC.sqrt_mul_sqrt_self B hB]

-- The subtype reduction is checked while H and N are abstract. The final
-- concrete consumer does not ask rw to infer a Hilbert structure through
-- b.val, classical root-membership witnesses, or the expanded Fock carrier.
private theorem hilbert_sqrt_core_product_mono
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : StarSubalgebra ℂ (H →L[ℂ] H)) (B C : H →L[ℂ] H)
    (hB : 0 ≤ B) (hC : 0 ≤ C)
    (hb : hilbertPositiveSqrt B ∈ N) (hc : hilbertPositiveSqrt C ∈ N)
    (hBC : B ≤ C) :
    (⟨hilbertPositiveSqrt B, hb⟩ : N) * star (⟨hilbertPositiveSqrt B, hb⟩ : N) ≤
      (⟨hilbertPositiveSqrt C, hc⟩ : N) * star (⟨hilbertPositiveSqrt C, hc⟩ : N) := by
  change hilbertPositiveSqrt B * star (hilbertPositiveSqrt B) ≤
    hilbertPositiveSqrt C * star (hilbertPositiveSqrt C)
  exact (hilbert_sqrt_mul_star B hB).trans_le
    (hBC.trans_eq (hilbert_sqrt_mul_star C hC).symm)

-- Cache only the existing L2(R; Fock) dictionaries; the carrier is unchanged.
private abbrev AmbientHilbert := TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F
private abbrev ambientNormedAddCommGroup : NormedAddCommGroup AmbientHilbert := inferInstance
private abbrev ambientInnerProductSpace : InnerProductSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientNormedSpace : NormedSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientModule : Module ℂ AmbientHilbert := inferInstance
private abbrev ambientTopologicalSpace : TopologicalSpace AmbientHilbert := inferInstance
private abbrev ambientUniformSpace : UniformSpace AmbientHilbert := inferInstance
private abbrev ambientCompleteSpace : CompleteSpace AmbientHilbert := inferInstance
private abbrev ambientStar : Star (AmbientHilbert →L[ℂ] AmbientHilbert) := inferInstance
private abbrev ambientOrder : PartialOrder (AmbientHilbert →L[ℂ] AmbientHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := AmbientHilbert)
attribute [local instance] ambientNormedAddCommGroup ambientInnerProductSpace
  ambientNormedSpace ambientModule ambientTopologicalSpace ambientUniformSpace
  ambientCompleteSpace ambientStar ambientOrder

theorem cutoff_antitone (e d : PositiveRegulator) (hed : e.val ≤ d.val)
    (X : F1Fecho.CanonicalFockWeight.PositiveInput) :
    cutoffWeight fockFlow regularFockVacuum d.val X.val ≤
      cutoffWeight fockFlow regularFockVacuum e.val X.val := by
  let hd := F1Fecho.CanonicalFockActualRightCutoffs.actualInverseCutoff_root_right
    d.val d.property
  let he := F1Fecho.CanonicalFockActualRightCutoffs.actualInverseCutoff_root_right
    e.val e.property
  let b : core.toStarSubalgebra :=
    ⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow d.val), hd.choose⟩
  let c : core.toStarSubalgebra :=
    ⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow e.val), he.choose⟩
  have hb : b ∈ scalarPolarRightAlgebra
      F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor := hd.choose_spec
  have hc : c ∈ scalarPolarRightAlgebra
      F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor := he.choose_spec
  have hbc : b*star b ≤ c*star c :=
    @hilbert_sqrt_core_product_mono AmbientHilbert ambientNormedAddCommGroup
      ambientInnerProductSpace ambientCompleteSpace core.toStarSubalgebra
      (regularInverseGeneratorCutoff fockFlow d.val)
      (regularInverseGeneratorCutoff fockFlow e.val)
      (regularInverseGeneratorCutoff_nonneg fockFlow d.val d.property)
      (regularInverseGeneratorCutoff_nonneg fockFlow e.val e.property)
      hd.choose he.choose
      (regularInverseGeneratorCutoff_antitone fockFlow e.val d.val
        e.property d.property hed)
  have hfinite (A : core.toStarSubalgebra) (hA : HasFiniteDualSquare A.val) :
      dualQuadraticIntegral (star b.val*(star A.val*A.val)*b.val) regularFockVacuum ≤
        dualQuadraticIntegral (star c.val*(star A.val*A.val)*c.val) regularFockVacuum :=
    scalarWeight_right_perturbed_mono
      F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolarFactor b c hb hc hbc
      ⟨A, F1Fecho.CanonicalFockFiniteWeight.finiteSquare_scalar_finite A.val hA⟩
  exact perturbed_comparison_all_positive fockFlow M regularFockVacuum
    F1Fecho.CanonicalFockWeightInvariance.fibre_boost_fixes_regularVacuum b c
    (regularInverseCutoffSqrt_commutes_average fockFlow d.val d.property)
    (regularInverseCutoffSqrt_commutes_average fockFlow e.val e.property)
    hfinite ⟨X.val, X.property.1⟩ X.property.2
#print axioms cutoff_antitone

theorem value_add (X Y : F1Fecho.CanonicalFockWeight.PositiveInput) :
    F1Fecho.CanonicalFockInverseSupremum.value (F1Fecho.CanonicalFockWeight.add X Y) =
      F1Fecho.CanonicalFockInverseSupremum.value X +
      F1Fecho.CanonicalFockInverseSupremum.value Y :=
  inverseSupremum_add_of_antitone fockFlow regularFockVacuum X.val Y.val
    X.property.2 Y.property.2
    (fun e d hed => cutoff_antitone e d hed X)
    (fun e d hed => cutoff_antitone e d hed Y)
#print axioms value_add

theorem cutoff_sequence_mono (X : F1Fecho.CanonicalFockWeight.PositiveInput) :
    Monotone (fun n : ℕ =>
      F1Fecho.CanonicalFockInverseSupremum.cut (1/((n:ℝ)+1)) X) :=
  cutoff_sequence_mono_of_antitone fockFlow regularFockVacuum X.val
    (fun e d hed => cutoff_antitone e d hed X)
#print axioms cutoff_sequence_mono

end F1Fecho.CanonicalFockActualInverseAdditivityR2
