import TGLExt.F1Fecho394.CanonicalFockActualDoubleCutR2
import TGLExt.F1Fecho394.CanonicalFockActualDomainCutLimitR1
import TGLExt.F1Fecho394.CanonicalFockActualInverseAdditivityR2
import TGLExt.F1Fecho394.GenericRootCutSupremumR1

/-! DECLARADO / UNCOMPILED CANDIDATE, R48, 2026-10-16.
R2 fixes only conjugate_affine: semilinearity is applied at the explicit
complex scalar (e : complex) before simplification can rewrite it as real smul.
R1 failed at that scalar step; its other three public reports had the trio.
Concrete root-cut supremum and identification with the EXISTING inverse weight.
All double-cut, positivity, commutation and convergence hypotheses are supplied
by constructed operators on the SAME original scalar-weight Fock GNS.
The represented-positive-root norm proof is reused from the generic proof
inside canonical V351QuadraticTrace; no SiteProfile is substituted for Fock.
The actual right-product norm identifies each weight cutoff. Regulator
antitonicity then identifies the all-positive-regulator supremum with the
cofinal sequence. Neither finiteness of the supremum nor traciality is assumed.
The finite star-core Tomita application, extension of traciality, total trace
and PF remain downstream obligations. Four public axiom reports are required.
Native dictionaries and the 400000 heartbeat limit are preserved. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
noncomputable section
namespace F1Fecho.CanonicalFockActualRootCutFormsR2
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace)
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open F1Fecho.CanonicalFockWeight (PositiveInput regularFockVacuum)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockWeightCompletion (scalarWeightGNSEmbedding)
open F1Fecho.CanonicalFockActualModularBalanceR6 (π T J)
open F1Fecho.CanonicalFockActualDoubleCutR2 (c C P)
open F1Fecho.CanonicalFockWeightPolar (scalarTomitaPositiveRoot)
open F1Fecho.RegularInverseWeight (PositiveRegulator cutoffWeight inverseSupremum)
open TGLV350.Regular (antiunitaryConjugate hilbertPositiveSqrt)
open Filter
open scoped Topology ENNReal

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


private theorem mapped_affine
    {𝒜 : Type*} {H : Type} [Ring 𝒜] [Algebra ℂ 𝒜] [StarRing 𝒜] [StarModule ℂ 𝒜]
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (pi : 𝒜 →⋆ₐ[ℂ] (H →L[ℂ] H)) (a : 𝒜) (e : ℝ) :
    pi (1-(e : ℂ) • a) = 1-(e : ℂ) • pi a := by
  simp only [map_sub, map_one, map_smul]

private theorem affine_commutes
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (S U V : H →L[ℂ] H) (e : ℝ)
    (hV : V = 1-(e : ℂ) • U) (hSU : Commute S U) : Commute S V := by
  change S*V = V*S
  ext1 v
  rw [hV]
  change S (v-(e : ℂ) • U v) = S v-(e : ℂ) • U (S v)
  rw [map_sub, map_smul]
  exact congrArg (fun z : H => S v-(e : ℂ) • z)
    (congrArg (fun W : H →L[ℂ] H => W v) hSU.eq)

private theorem conjugate_affine
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (j : H ≃ₛₗᵢ[starRingEnd ℂ] H) (U : H →L[ℂ] H) (e : ℝ) :
    antiunitaryConjugate (H := H) j (1-(e : ℂ) • U) =
      1-(e : ℂ) • antiunitaryConjugate (H := H) j U := by
  ext1 v
  change j (j.symm v-(e : ℂ) • U (j.symm v)) =
    v-(e : ℂ) • j (U (j.symm v))
  have hs : j ((e : ℂ) • U (j.symm v)) =
      (e : ℂ) • j (U (j.symm v)) := by
    simpa using (map_smulₛₗ j (e : ℂ) (U (j.symm v)))
  rw [map_sub, LinearIsometryEquiv.apply_symm_apply]
  exact congrArg (fun z : H => v-z) hs

private theorem P_affine (ε : ℝ) : P ε = 1-(ε : ℂ) • C ε :=
  @mapped_affine core.toStarSubalgebra GNSHilbert
    inferInstance inferInstance inferInstance inferInstance
    nativeNormedAddCommGroup nativeInnerProductSpace nativeCompleteSpace π (c ε) ε

private theorem T_commutes_P (ε : ℝ) (hε : 0 < ε) : Commute T (P ε) :=
  @affine_commutes GNSHilbert nativeNormedAddCommGroup nativeInnerProductSpace
    nativeCompleteSpace T (C ε) (P ε) ε (P_affine ε)
    (F1Fecho.CanonicalFockActualDoubleCutR2.actual_double_cut ε ε hε hε).1

private theorem C_commutes_conjugate_P (ε η : ℝ) (hη : 0 < η) :
    Commute (C ε) (antiunitaryConjugate (H := GNSHilbert) J (P η)) := by
  have he : antiunitaryConjugate (H := GNSHilbert) J (P η) =
      1-(η : ℂ) • antiunitaryConjugate (H := GNSHilbert) J (C η) :=
    (congrArg (antiunitaryConjugate (H := GNSHilbert) J) (P_affine η)).trans
      (@conjugate_affine GNSHilbert nativeNormedAddCommGroup nativeInnerProductSpace
        nativeCompleteSpace J (C η) η)
  exact @affine_commutes GNSHilbert nativeNormedAddCommGroup nativeInnerProductSpace
    nativeCompleteSpace (C ε) (antiunitaryConjugate (H := GNSHilbert) J (C η))
    (antiunitaryConjugate (H := GNSHilbert) J (P η)) η he
    (F1Fecho.CanonicalFockActualDoubleCutR2.inverseCutoff_conjugate_commutes
      η hη (c ε)).symm

private theorem C_nonneg (ε : ℝ) (hε : 0 < ε) : 0 ≤ C ε :=
  F1Fecho.CanonicalFockGNSOrder.scalarGNSRepresentation_nonneg (c ε)
    (show 0 ≤ c ε from
      F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_nonneg fockFlow ε hε)

/-- Both sides may be infinite. The root domain is the original Tomita root. -/
theorem actual_root_cut_supremum (x : scalarTomitaPositiveRoot.domain) :
    (⨆ n : ℕ, ENNReal.ofReal (inner ℂ (scalarTomitaPositiveRoot x)
      (C (1/((n : ℝ)+1)) (scalarTomitaPositiveRoot x))).re) =
    ⨆ n : ℕ, ENNReal.ofReal (inner ℂ (x : GNSHilbert)
      (antiunitaryConjugate (H := GNSHilbert) J (C (1/((n : ℝ)+1))) x)).re :=
  @F1Fecho.QuadraticTraceForms.root_cut_supremum GNSHilbert
    nativeNormedAddCommGroup nativeInnerProductSpace nativeCompleteSpace T
    F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_nonneg
    F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_le_one
    F1Fecho.CanonicalFockWeightModularOperator.scalarTomitaResolvent_injective J
    (fun n => C (1/((n : ℝ)+1))) (fun n => P (1/((n : ℝ)+1)))
    (fun n => C_nonneg _ (by positivity))
    (fun n => F1Fecho.CanonicalFockActualDomainCutLimitR1.domainCut_bounds _ (by positivity))
    F1Fecho.CanonicalFockActualDomainCutLimitR1.domainCut_tendsto_identity
    (fun n => (F1Fecho.CanonicalFockActualDoubleCutR2.actual_double_cut
      (1/((n : ℝ)+1)) (1/((n : ℝ)+1)) (by positivity) (by positivity)).1)
    (fun n => T_commutes_P _ (by positivity))
    F1Fecho.CanonicalFockWeightPolar.scalarTomitaPolar_conjugate_resolvent
    (fun n m => C_commutes_conjugate_P _ _ (by positivity))
    (fun n m => (F1Fecho.CanonicalFockActualDoubleCutR2.inverseCutoff_conjugate_commutes
      (1/((m : ℝ)+1)) (by positivity)
      (F1Fecho.CanonicalFockActualDoubleCutR2.p (1/((n : ℝ)+1)))).symm)
    (fun n m => (F1Fecho.CanonicalFockActualDoubleCutR2.actual_double_cut
      (1/((n : ℝ)+1)) (1/((m : ℝ)+1)) (by positivity) (by positivity)).2.2) x
#print axioms actual_root_cut_supremum

-- Generic proof reused from TGLExt/V351QuadraticTrace.lean (private supplier).
-- It is instantiated below with L2(R; Fock), its actual core, and its own GNS.
private theorem represented_positive_root_norm {H K : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
    (N : StarSubalgebra ℂ (H →L[ℂ] H))
    (pi : N →⋆ₐ[ℂ] (K →L[ℂ] K)) (a : N) (ha : 0 ≤ a.val)
    (hm : hilbertPositiveSqrt a.val ∈ N) (v : K) :
    ‖pi (star (⟨hilbertPositiveSqrt a.val,hm⟩ : N)) v‖^2 =
      (inner ℂ v (pi a v)).re := by
  let b : N := ⟨hilbertPositiveSqrt a.val,hm⟩
  have hs : star b = b := Subtype.ext (CFC.sqrt_nonneg a.val).isSelfAdjoint.star_eq
  have hbb : b * star b = a := by
    rw [hs]
    exact Subtype.ext (CFC.sqrt_mul_sqrt_self a.val ha)
  have he := ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left
    (𝕜 := ℂ) (star (pi b)) v
  have hn : ‖star (pi b) v‖^2 = (inner ℂ ((pi b*star (pi b)) v) v).re := by
    simpa only [RCLike.re_eq_complex_re,ContinuousLinearMap.star_eq_adjoint,
      ContinuousLinearMap.adjoint_adjoint,ContinuousLinearMap.mul_def] using he
  change ‖pi (star b) v‖^2 = _
  rw [map_star,hn,← map_star,← map_mul,hbb]
  exact inner_re_symm (𝕜 := ℂ) _ _

/-- The actual inverse-cutoff weight on the full scalar weight left ideal. -/
theorem cutoffWeight_square_form (ε : ℝ) (hε : 0 < ε) (a : scalarWeightLeftIdeal) :
    cutoffWeight fockFlow regularFockVacuum ε (star a.val.val*a.val.val) =
      ENNReal.ofReal (inner ℂ (J.symm (scalarWeightGNSEmbedding a))
        (C ε (J.symm (scalarWeightGNSEmbedding a)))).re := by
  let hr := F1Fecho.CanonicalFockActualRightCutoffs.actualInverseCutoff_root_right ε hε
  let b : core.toStarSubalgebra :=
    ⟨hilbertPositiveSqrt (F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff
      fockFlow ε), hr.choose⟩
  have hw : cutoffWeight fockFlow regularFockVacuum ε (star a.val.val*a.val.val) =
      ENNReal.ofReal (‖π (star b) (J.symm (scalarWeightGNSEmbedding a))‖^2) :=
    F1Fecho.CanonicalFockActualInverseAdditivityR2.scalarWeight_right_perturbed_norm
      J b hr.choose_spec a
  have hn : ‖π (star b) (J.symm (scalarWeightGNSEmbedding a))‖^2 =
      (inner ℂ (J.symm (scalarWeightGNSEmbedding a))
        (C ε (J.symm (scalarWeightGNSEmbedding a)))).re :=
    @represented_positive_root_norm AmbientHilbert GNSHilbert
      ambientNormedAddCommGroup ambientInnerProductSpace ambientCompleteSpace
      nativeNormedAddCommGroup nativeInnerProductSpace nativeCompleteSpace
      core.toStarSubalgebra π (c ε)
      (F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_nonneg fockFlow ε hε)
      hr.choose (J.symm (scalarWeightGNSEmbedding a))
  exact hw.trans (congrArg ENNReal.ofReal hn)
#print axioms cutoffWeight_square_form

private theorem cofinal_regulator_supremum (f : ℝ → ℝ≥0∞)
    (hf : ∀ e d : PositiveRegulator, e.val ≤ d.val → f d.val ≤ f e.val) :
    (⨆ e : PositiveRegulator, f e.val) = ⨆ n : ℕ, f (1/((n : ℝ)+1)) := by
  apply le_antisymm
  · apply iSup_le
    intro e
    have he : ∀ᶠ n : ℕ in atTop, 1/((n : ℝ)+1) < e.val :=
      (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ)).eventually
        (eventually_lt_nhds e.property)
    obtain ⟨n, hn⟩ := he.exists
    exact le_iSup_of_le n (hf ⟨1/((n : ℝ)+1), by positivity⟩ e hn.le)
  · apply iSup_le
    intro n
    exact le_iSup (fun e : PositiveRegulator => f e.val)
      ⟨1/((n : ℝ)+1), by positivity⟩

theorem value_eq_iSup_sequence (X : PositiveInput) :
    F1Fecho.CanonicalFockInverseSupremum.value X =
      ⨆ n : ℕ, cutoffWeight fockFlow regularFockVacuum (1/((n : ℝ)+1)) X.val :=
  cofinal_regulator_supremum (fun ε => cutoffWeight fockFlow regularFockVacuum ε X.val)
    (fun e d hed => F1Fecho.CanonicalFockActualInverseAdditivityR2.cutoff_antitone e d hed X)
#print axioms value_eq_iSup_sequence

private def squareInput (a : core.toStarSubalgebra) : PositiveInput :=
  ⟨star a.val*a.val, (star a*a).property, star_mul_self_nonneg a.val⟩

/-- Identification of the existing all-regulator inverse supremum, without
    replacing it by a new quadratic-form definition. -/
theorem inverseSupremum_square_form (a : scalarWeightLeftIdeal) :
    inverseSupremum fockFlow regularFockVacuum (star a.val.val*a.val.val) =
      ⨆ n : ℕ, ENNReal.ofReal (inner ℂ (J.symm (scalarWeightGNSEmbedding a))
        (C (1/((n : ℝ)+1)) (J.symm (scalarWeightGNSEmbedding a)))).re := by
  have hsequence := value_eq_iSup_sequence (squareInput a.val)
  have hforms :
      (fun n : ℕ => cutoffWeight fockFlow regularFockVacuum (1/((n : ℝ)+1))
        (star a.val.val*a.val.val)) =
      (fun n : ℕ => ENNReal.ofReal (inner ℂ (J.symm (scalarWeightGNSEmbedding a))
        (C (1/((n : ℝ)+1)) (J.symm (scalarWeightGNSEmbedding a)))).re) :=
    funext (fun n => cutoffWeight_square_form _ (by positivity) a)
  exact hsequence.trans (congrArg (fun f : ℕ → ℝ≥0∞ => ⨆ n, f n) hforms)
#print axioms inverseSupremum_square_form

end F1Fecho.CanonicalFockActualRootCutFormsR2
