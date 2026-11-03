import TGLExt.V350ScalarRightPairVector

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

private theorem commutingSelfadjointProduct {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (T R : H →L[ℂ] H)
    (hT : star T = T) (hR : star R = R) (h : Commute T R) : star (T*R) = T*R := by
  calc
    _ = star R * star T := ContinuousLinearMap.adjoint_comp T R
    _ = R*T := congrArg₂ (fun A B : H →L[ℂ] H => A*B) hR hT
    _ = _ := h.eq.symm

theorem scalarGNSCommutant_commutes (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hT : T ∈ scalarGNSCommutant P)
    (a : (regularCoreAlgebra P).toStarSubalgebra) : Commute T (scalarGNSRepresentation P a) := by
  change T ∈ StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P)) at hT
  rw [StarSubalgebra.mem_centralizer_iff] at hT
  exact (hT _ ⟨a,rfl⟩).1.symm

private theorem selfadjointRightValue (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a) : star a.val = a.val := by
  change (star a).val = a.val
  exact congrArg (fun b : scalarPairedRightAlgebra P => b.val) ha

private theorem commutingRightVectorEquation {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] (T R A : H →L[ℂ] H) (x v : H)
    (hr : R x = A v) (hc : Commute T A) : (T*R) x = A (T v) :=
  (congrArg T hr).trans (congrArg (fun B : H →L[ℂ] H => B v) hc.eq)

/-- Multiplying a selfadjoint right pair by a commuting selfadjoint member
of the full commutant preserves the pair, even if T is not itself in E. -/
def scalarSelfadjointRightPairMultiplier (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hT : T ∈ scalarGNSCommutant P)
    (hTs : star T = T) (hTa : Commute T a.val) : ScalarRightAdjointPair P (T*a.val) where
  vector := T (scalarRightPairVector P a)
  adjointVector := T (scalarRightPairVector P a)
  right := by
    intro x
    refine commutingRightVectorEquation T a.val (scalarGNSRepresentation P x.val)
      (scalarWeightGNSEmbedding P x) (scalarRightPairVector P a) ?_ ?_
    · exact (scalarPairedRightChoice P a).right x
    · exact scalarGNSCommutant_commutes P T hT x.val
  adjoint := by
    intro x
    have hs := commutingSelfadjointProduct T a.val hTs (selfadjointRightValue P a ha) hTa
    apply (congrArg (fun R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
      R (scalarWeightGNSEmbedding P x)) hs).trans
    refine commutingRightVectorEquation T a.val (scalarGNSRepresentation P x.val)
      (scalarWeightGNSEmbedding P x) (scalarRightPairVector P a) ?_ ?_
    · exact (scalarPairedRightChoice P a).right x
    · exact scalarGNSCommutant_commutes P T hT x.val

def scalarSelfadjointRightMultiplier (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hT : T ∈ scalarGNSCommutant P)
    (hTs : star T = T) (hTa : Commute T a.val) : scalarPairedRightAlgebra P :=
  ⟨T*a.val, ⟨scalarSelfadjointRightPairMultiplier P a ha T hT hTs hTa⟩⟩

theorem scalarSelfadjointRightMultiplier_star (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hT : T ∈ scalarGNSCommutant P)
    (hTs : star T = T) (hTa : Commute T a.val) :
    star (scalarSelfadjointRightMultiplier P a ha T hT hTs hTa) =
      scalarSelfadjointRightMultiplier P a ha T hT hTs hTa := by
  apply Subtype.ext
  exact commutingSelfadjointProduct T a.val hTs (selfadjointRightValue P a ha) hTa

theorem scalarSelfadjointRightMultiplier_vector (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) (ha : star a = a)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hT : T ∈ scalarGNSCommutant P)
    (hTs : star T = T) (hTa : Commute T a.val) :
    scalarRightPairVector P (scalarSelfadjointRightMultiplier P a ha T hT hTs hTa) =
      T (scalarRightPairVector P a) :=
  scalarRightPairVector_of_pair P _ (scalarSelfadjointRightPairMultiplier P a ha T hT hTs hTa)

/-- The pair vector is supported on the norm closure of the multiplier range.
No uniform bound on the approximate-unit GNS vectors is required. -/
theorem scalarRightAdjointPair_vector_mem_range_closure (P : SiteProfile)
    (R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (d : ScalarRightAdjointPair P R) :
    d.vector ∈ closure (Set.range R) := by
  have ht : Tendsto (fun h : ℝ => scalarGNSRepresentation P
      ⟨regularAverage P h,regularAverage_mem P h⟩ d.vector) (𝓝[>] 0) (𝓝 d.vector) :=
    (scalarGNSAverage_tendsto P d.vector).mono_left
    (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  apply isClosed_closure.mem_of_tendsto ht
  filter_upwards [self_mem_nhdsWithin] with h hh
  let e : scalarWeightLeftIdeal P := Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P)
    ⟨⟨regularAverage P h,regularAverage_mem P h⟩,regularAverage_hasFiniteDualSquare P h hh⟩
  exact subset_closure ⟨scalarWeightGNSEmbedding P e, d.right e⟩

theorem scalarRightPairVector_mem_range_closure (P : SiteProfile)
    (a : scalarPairedRightAlgebra P) : scalarRightPairVector P a ∈ closure (Set.range a.val) :=
  scalarRightAdjointPair_vector_mem_range_closure P a.val (scalarPairedRightChoice P a)

#print axioms scalarGNSCommutant_commutes
#print axioms scalarSelfadjointRightPairMultiplier
#print axioms scalarSelfadjointRightMultiplier
#print axioms scalarSelfadjointRightMultiplier_star
#print axioms scalarSelfadjointRightMultiplier_vector
#print axioms scalarRightAdjointPair_vector_mem_range_closure
#print axioms scalarRightPairVector_mem_range_closure
end
end TGLV350.Regular
