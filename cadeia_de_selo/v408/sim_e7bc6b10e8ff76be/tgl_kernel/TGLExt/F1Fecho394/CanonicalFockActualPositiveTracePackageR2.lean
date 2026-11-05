import TGLExt.F1Fecho394.CanonicalFockActualInverseFinitenessR2
import TGLExt.F1Fecho394.CanonicalFockInverseNormalR1

/-! DECLARADO / UNCOMPILED CANDIDATE, R50, 2026-10-16.
Ten-field positive trace package on the SAME PositiveInput and regular Fock core.
Its value is definitionally the previously constructed inverseSupremum: neither
an arbitrary new functional nor the dual-invariant unperturbed scalar weight.
The shape follows V351RegularCoreTraceContract/Construction, but no SiteProfile
is substituted for Fock. Normality is the internal IsLUB statement; positivity
of that supremum is derived. Semifiniteness is the exact supremum over finite
positive minorants. R49 supplies the square law on every bounded core element.
All ten fields are filled from proved suppliers or the new concrete finiteness
candidate. No trace, hreg, balance, or finiteness assumption is added.
A nonzero finite positive element follows from semifiniteness and value(1)=top;
there is no second special approximate-identity construction for this witness.
This is ONLY the positive trace package. The separate total cyclic completion,
PF and complete R7 acceptance are not asserted here. No zero extension occurs.
Require both candidate builds, EXIT0 and all six public axiom reports. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
universe u
noncomputable section
namespace F1Fecho.CanonicalFockActualPositiveTracePackageR2
open TGLExt TGLV350.Regular
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open F1Fecho.CanonicalFockWeight (PositiveInput zero one add scale positiveDual regularFockVacuum)
open F1Fecho.CanonicalFockInverseSupremum (value value_zero value_scale value_dual
  value_faithful value_mono value_internal_normal value_one)
open F1Fecho.CanonicalFockActualInverseAdditivityR2 (value_add)
open F1Fecho.CanonicalFockActualInverseFinitenessR2 (value_finite_minorants)
open F1Fecho.CanonicalFockActualTracialExtensionR1 (inverseSupremum_tracial)
open F1Fecho.RegularInverseWeight (inverseSupremum)
open scoped ENNReal NNReal

private abbrev AmbientHilbert := RegularHilbert F1Rede.BosonicFock.F
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

/-- Positive square of an element of the existing represented Fock core. -/
def positiveSquare (a : core.toStarSubalgebra) : PositiveInput :=
  ⟨star a.val*a.val,(star a*a).property,star_mul_self_nonneg a.val⟩

private theorem value_faithful_zero (X : PositiveInput) : value X = 0 ↔ X = zero := by
  constructor
  · intro h
    exact Subtype.ext ((value_faithful X).mp h)
  · intro h
    exact (congrArg value h).trans value_zero

theorem value_tracial (a : core.toStarSubalgebra) :
    value (positiveSquare a) = value (positiveSquare (star a)) := by
  change inverseSupremum fockFlow regularFockVacuum (star a.val*a.val) =
    inverseSupremum fockFlow regularFockVacuum (star (star a.val)*star a.val)
  simpa only [star_star] using inverseSupremum_tracial a
#print axioms value_tracial

/-- Positivity follows from nonemptiness and the internal least upper bound. -/
theorem positive_internal_isLUB_nonneg
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → core.toStarSubalgebra) (S : core.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hS : IsLUB (Set.range A) S) : 0 ≤ S :=
  (hpos (Classical.arbitrary ι)).trans (hS.1 (Set.mem_range_self _))

theorem value_normal_internal
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → core.toStarSubalgebra) (S : core.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    value ⟨S.val,S.property,positive_internal_isLUB_nonneg A S hpos hS⟩ =
      ⨆ i, value ⟨(A i).val,(A i).property,hpos i⟩ :=
  value_internal_normal A S hpos hmono hS (positive_internal_isLUB_nonneg A S hpos hS)
#print axioms value_normal_internal

/-- Positive trace contract on the original core; ten fields, as in V351. -/
structure PositiveTraceData where
  value : PositiveInput → ℝ≥0∞
  zero : value F1Fecho.CanonicalFockWeight.zero = 0
  additive : ∀ A B, value (add A B) = value A + value B
  homogeneous : ∀ (r : ℝ≥0) A, value (scale r A) = (r : ℝ≥0∞)*value A
  monotone : ∀ A B, A.val ≤ B.val → value A ≤ value B
  faithful : ∀ A, value A = 0 ↔ A = F1Fecho.CanonicalFockWeight.zero
  normal : ∀ {ι : Type u} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → core.toStarSubalgebra) (S : core.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (_hmono : Monotone A) (hS : IsLUB (Set.range A) S),
    value ⟨S.val,S.property,positive_internal_isLUB_nonneg A S hpos hS⟩ =
      ⨆ i, value ⟨(A i).val,(A i).property,hpos i⟩
  semifinite : ∀ A, value A =
    ⨆ (B : PositiveInput) (_ : B.val ≤ A.val) (_ : value B < ⊤), value B
  tracial : ∀ a, value (positiveSquare a) = value (positiveSquare (star a))
  dual_scaling : ∀ s A, value (positiveDual s A) =
    ENNReal.ofReal (Real.exp (-s))*value A

/-- Every property is supplied; this definition has no input assumption. -/
def actualPositiveTrace : PositiveTraceData.{u} where
  value := F1Fecho.CanonicalFockInverseSupremum.value
  zero := value_zero
  additive := value_add
  homogeneous := value_scale
  monotone := value_mono
  faithful := value_faithful_zero
  normal := value_normal_internal
  semifinite := value_finite_minorants
  tracial := value_tracial
  dual_scaling := value_dual
#print axioms actualPositiveTrace

/-- The packaged value is exactly the old inverse supremum, with its normalization. -/
theorem actualPositiveTrace_value (X : PositiveInput) :
    actualPositiveTrace.{u}.value X = inverseSupremum fockFlow regularFockVacuum X.val := rfl
#print axioms actualPositiveTrace_value

/-- Semifiniteness and the already infinite unit give a finite nonzero positive value. -/
theorem exists_positive_finite : ∃ Y : PositiveInput, 0 < value Y ∧ value Y < ⊤ := by
  classical
  by_contra h
  have hz : value one = 0 := by
    apply le_antisymm ?_ bot_le
    rw [value_finite_minorants one]
    apply iSup_le
    intro Y
    apply iSup_le
    intro _
    apply iSup_le
    intro hf
    exact le_of_not_gt (fun hp => h ⟨Y,hp,hf⟩)
  exact ENNReal.top_ne_zero (value_one.symm.trans hz)
#print axioms exists_positive_finite

/-- The same infinite-unit theorem rules out the identically-zero functional. -/
theorem actualPositiveTrace_unit_infinite : actualPositiveTrace.{u}.value one = ⊤ := value_one
#print axioms actualPositiveTrace_unit_infinite

end F1Fecho.CanonicalFockActualPositiveTracePackageR2
