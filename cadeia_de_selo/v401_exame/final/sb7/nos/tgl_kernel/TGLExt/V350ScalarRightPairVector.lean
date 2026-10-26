import TGLExt.V350ScalarGaussianRightPairs

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

private theorem rightVectorValueTransport {H : Type*} (D : Set H) (F : D → H)
    (v z w : H) (h : ∃ hv : v ∈ D, F ⟨v,hv⟩ = z) (he : z = w) :
    ∃ hv : v ∈ D, F ⟨v,hv⟩ = w := by
  obtain ⟨hv,hv'⟩ := h
  exact ⟨hv,hv'.trans he⟩

theorem scalarWeightAction_separates_vectors (P : SiteProfile) (x y : ScalarGNSHilbert P)
    (hxy : ∀ a : scalarWeightLeftIdeal P,
      scalarGNSRepresentation P a.val x = scalarGNSRepresentation P a.val y) : x = y := by
  have hx := (scalarGNSAverage_tendsto P x).mono_left
    (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  have hy := (scalarGNSAverage_tendsto P y).mono_left
    (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  have he : (fun h : ℝ => scalarGNSRepresentation P
      ⟨regularAverage P h,regularAverage_mem P h⟩ x) =ᶠ[𝓝[>] 0]
      (fun h : ℝ => scalarGNSRepresentation P
      ⟨regularAverage P h,regularAverage_mem P h⟩ y) := by
    filter_upwards [self_mem_nhdsWithin] with h hh
    let e : scalarWeightLeftIdeal P := Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P)
      ⟨⟨regularAverage P h,regularAverage_mem P h⟩,regularAverage_hasFiniteDualSquare P h hh⟩
    exact hxy e
  exact tendsto_nhds_unique (hx.congr' he) hy

theorem scalarRightAdjointPair_vector_unique {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P}
    (d e : ScalarRightAdjointPair P R) : d.vector = e.vector := by
  apply scalarWeightAction_separates_vectors P
  intro a
  exact (d.right a).symm.trans (e.right a)

theorem scalarRightAdjointPair_operator_unique {P : SiteProfile}
    {R S : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P}
    (d : ScalarRightAdjointPair P R) (e : ScalarRightAdjointPair P S)
    (he : d.vector = e.vector) : R = S := by
  ext1 x
  refine (scalarWeightGNSEmbedding_denseRange P).induction_on x
    (isClosed_eq R.continuous S.continuous) ?_
  intro a
  exact (d.right a).trans ((congrArg (scalarGNSRepresentation P a.val) he).trans (e.right a).symm)

/-- Choice supplies a representative pair; the vector below is proved independent of it. -/
def scalarPairedRightChoice (P : SiteProfile) (a : scalarPairedRightAlgebra P) :
    ScalarRightAdjointPair P a.val := Classical.choice a.property

def scalarRightPairVector (P : SiteProfile) :
    scalarPairedRightAlgebra P →ₗ[ℂ] ScalarGNSHilbert P where
  toFun a := (scalarPairedRightChoice P a).vector
  map_add' a b := scalarRightAdjointPair_vector_unique
    (scalarPairedRightChoice P (a+b))
    (scalarRightAdjointPair_add (scalarPairedRightChoice P a) (scalarPairedRightChoice P b))
  map_smul' c a := scalarRightAdjointPair_vector_unique
    (scalarPairedRightChoice P (c • a))
    (scalarRightAdjointPair_smul (scalarPairedRightChoice P a) c)

theorem scalarRightPairVector_of_pair (P : SiteProfile)
    (R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (d : ScalarRightAdjointPair P R) :
    scalarRightPairVector P ⟨R,⟨d⟩⟩ = d.vector :=
  scalarRightAdjointPair_vector_unique (scalarPairedRightChoice P ⟨R,⟨d⟩⟩) d

theorem scalarRightPairVector_injective (P : SiteProfile) :
    Function.Injective (scalarRightPairVector P) := by
  intro a b h
  apply Subtype.ext
  exact scalarRightAdjointPair_operator_unique
    (scalarPairedRightChoice P a) (scalarPairedRightChoice P b) h

theorem scalarRightPairVector_mul (P : SiteProfile) (a b : scalarPairedRightAlgebra P) :
    scalarRightPairVector P (a*b) = a.val (scalarRightPairVector P b) :=
  scalarRightAdjointPair_vector_unique (scalarPairedRightChoice P (a*b))
    (scalarRightAdjointPair_mul (scalarPairedRightChoice P a) (scalarPairedRightChoice P b))

theorem scalarRightPairVector_star (P : SiteProfile) (a : scalarPairedRightAlgebra P) :
    scalarRightPairVector P (star a) = (scalarPairedRightChoice P a).adjointVector :=
  scalarRightAdjointPair_vector_unique (scalarPairedRightChoice P (star a))
    (scalarRightAdjointPair_star (scalarPairedRightChoice P a))

theorem scalarRightPairVector_original_adjoint (P : SiteProfile) (a : scalarPairedRightAlgebra P) :
    ∃ hv : scalarRightPairVector P a ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨scalarRightPairVector P a,hv⟩ = scalarRightPairVector P (star a) := by
  exact rightVectorValueTransport (H := ScalarGNSHilbert P)
    (scalarTomitaAdjointDomain P : Set (ScalarGNSHilbert P))
    (fun y => scalarTomitaAdjoint P y)
    (scalarRightPairVector P a) (scalarPairedRightChoice P a).adjointVector
    (scalarRightPairVector P (star a))
    (scalarRightAdjointPair_maximal (P := P) (R := a.val) (scalarPairedRightChoice P a))
    (scalarRightPairVector_star P a).symm

/-- Norm density of actual right-pair vectors, NOT density in the graph norm of F. -/
theorem scalarRightPairVector_denseRange (P : SiteProfile) :
    DenseRange (scalarRightPairVector P) := by
  have ho : (scalarRightPairVector P).range.orthogonal = ⊥ := by
    apply le_antisymm ?_ bot_le
    intro v hv
    change v=0
    apply scalarGaussianGNSMap_injective P
    rw [map_zero]
    apply (separating_commutant_orbit_dense
      (dualOrbitVonNeumann (regularCoreAlgebra P)) (scalarGaussianVacuum P)
      (scalarGaussianImage_separating P)).eq_zero_of_inner_right (𝕜 := ℂ)
    intro B
    rw [← (scalarGaussianGNSMap P).adjoint_inner_left]
    apply hv
    exact ⟨⟨scalarGaussianRightOperator P B.val,⟨scalarGaussianRightAdjointPair P B.val B.property⟩⟩,
      scalarRightPairVector_of_pair P _ (scalarGaussianRightAdjointPair P B.val B.property)⟩
  change Dense (Set.range (scalarRightPairVector P))
  rw [dense_iff_closure_eq]
  exact congrArg (fun V : Submodule ℂ (ScalarGNSHilbert P) => (V : Set (ScalarGNSHilbert P)))
    ((scalarRightPairVector P).range.topologicalClosure_eq_top_iff.mpr ho)

#print axioms scalarWeightAction_separates_vectors
#print axioms scalarRightAdjointPair_vector_unique
#print axioms scalarRightAdjointPair_operator_unique
#print axioms scalarPairedRightChoice
#print axioms scalarRightPairVector
#print axioms scalarRightPairVector_of_pair
#print axioms scalarRightPairVector_injective
#print axioms scalarRightPairVector_mul
#print axioms scalarRightPairVector_star
#print axioms scalarRightPairVector_original_adjoint
#print axioms scalarRightPairVector_denseRange
end
end TGLV350.Regular
