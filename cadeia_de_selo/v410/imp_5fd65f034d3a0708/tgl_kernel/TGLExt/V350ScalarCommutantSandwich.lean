import TGLExt.V350ScalarRightAdjointPair

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

private theorem boundedRightStarMul {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (A B : H →L[ℂ] H) :
    star (A*B) = star B * star A := ContinuousLinearMap.adjoint_comp A B

private theorem boundedRightNormStar {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (A : H →L[ℂ] H) :
    ‖star A‖ = ‖A‖ := ContinuousLinearMap.adjoint.norm_map A

theorem scalarGNSCommutation_adjoint (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : ∀ a, Commute T (scalarGNSRepresentation P a)) :
    ∀ a, Commute (star T) (scalarGNSRepresentation P a) := by
  intro a
  have he := congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => star B)
    (hT (star a)).eq
  simp only [boundedRightStarMul,← map_star,_root_.star_star] at he
  exact he.symm

theorem scalarRightRegularization_adjoint_tendsto (P : SiteProfile) (x : ScalarGNSHilbert P) :
    Tendsto (fun h : ℝ => star (scalarRightRegularization P h) x) (𝓝[≠] 0) (𝓝 x) :=
  contraction_adjoint_tendsto_identity _ _ (scalarRightRegularization_norm_le P)
    (scalarRightRegularization_tendsto P) x

/-- The order is essential: elements of pi(N)' need not commute mutually. -/
def scalarCommutantSandwich (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (h : ℝ) :
    ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
  star (scalarRightRegularization P h) * T * scalarRightRegularization P h

theorem scalarCommutantSandwich_star (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (h : ℝ) :
    star (scalarCommutantSandwich P T h) = scalarCommutantSandwich P (star T) h := by
  simp only [scalarCommutantSandwich,boundedRightStarMul,_root_.star_star,mul_assoc]

theorem scalarCommutantSandwich_norm_le (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (h : ℝ) :
    ‖scalarCommutantSandwich P T h‖ ≤ ‖T‖ := by
  have hs : ‖star (scalarRightRegularization P h)‖ ≤ 1 := by
    exact (boundedRightNormStar (scalarRightRegularization P h)).le.trans
      (scalarRightRegularization_norm_le P h)
  change ‖star (scalarRightRegularization P h) * T * scalarRightRegularization P h‖ ≤ _
  calc
    _ ≤ ‖star (scalarRightRegularization P h) * T‖ :=
      scalarCommutantRegularization_norm_le P _ h
    _ ≤ ‖star (scalarRightRegularization P h)‖ * ‖T‖ :=
      norm_mul_le (star (scalarRightRegularization P h)) T
    _ ≤ ‖T‖ := by simpa only [one_mul] using
      mul_le_mul_of_nonneg_right hs (norm_nonneg T)

def scalarCommutantSandwichVector (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (h : ℝ) (hh : 0 < h) :
    ScalarGNSHilbert P :=
  star (scalarRightRegularization P h) (T (scalarRegularizationVector P h hh))

theorem scalarCommutantSandwich_right (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : ∀ a, Commute T (scalarGNSRepresentation P a)) (h : ℝ) (hh : 0 < h)
    (a : scalarWeightLeftIdeal P) :
    scalarCommutantSandwich P T h (scalarWeightGNSEmbedding P a) =
      scalarGNSRepresentation P a.val (scalarCommutantSandwichVector P T h hh) := by
  have hs := scalarGNSCommutation_adjoint P (scalarRightRegularization P h)
    (scalarRightRegularization_commutes P h) a.val
  change star (scalarRightRegularization P h)
      (T (scalarRightRegularization P h (scalarWeightGNSEmbedding P a))) = _
  calc
    _ = star (scalarRightRegularization P h)
        (T (scalarGNSRepresentation P a.val (scalarRegularizationVector P h hh))) :=
      congrArg (fun x => star (scalarRightRegularization P h) (T x))
        (scalarRightRegularization_vector P h hh a)
    _ = star (scalarRightRegularization P h)
        (scalarGNSRepresentation P a.val (T (scalarRegularizationVector P h hh))) :=
      congrArg (fun x : ScalarGNSHilbert P => star (scalarRightRegularization P h) x)
        (congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
          B (scalarRegularizationVector P h hh)) (hT a.val).eq)
    _ = _ := congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
      B (T (scalarRegularizationVector P h hh))) hs.eq

def scalarCommutantSandwichPair (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : ∀ a, Commute T (scalarGNSRepresentation P a)) (h : ℝ) (hh : 0 < h) :
    ScalarRightAdjointPair P (scalarCommutantSandwich P T h) where
  vector := scalarCommutantSandwichVector P T h hh
  adjointVector := scalarCommutantSandwichVector P (star T) h hh
  right := scalarCommutantSandwich_right P T hT h hh
  adjoint := by
    intro a
    rw [scalarCommutantSandwich_star]
    exact scalarCommutantSandwich_right P (star T) (scalarGNSCommutation_adjoint P T hT) h hh a

/-- A concrete pair in the graph of the ORIGINAL maximal F=S†. -/
theorem scalarCommutantSandwich_in_original_adjoint (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : ∀ a, Commute T (scalarGNSRepresentation P a)) (h : ℝ) (hh : 0 < h) :
    ∃ hv : scalarCommutantSandwichVector P T h hh ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨scalarCommutantSandwichVector P T h hh,hv⟩ =
        scalarCommutantSandwichVector P (star T) h hh :=
  scalarRightAdjointPair_maximal (scalarCommutantSandwichPair P T hT h hh)

theorem scalarCommutantSandwich_tendsto (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (x : ScalarGNSHilbert P) :
    Tendsto (fun h : ℝ => scalarCommutantSandwich P T h x) (𝓝[>] 0) (𝓝 (T x)) := by
  have hb (h : ℝ) : ‖star (scalarRightRegularization P h)‖ ≤ 1 := by
    exact (boundedRightNormStar (scalarRightRegularization P h)).le.trans
      (scalarRightRegularization_norm_le P h)
  have hl : Tendsto (fun h : ℝ => star (scalarRightRegularization P h) (T x))
      (𝓝[>] 0) (𝓝 (T x)) :=
    (scalarRightRegularization_adjoint_tendsto P (T x)).mono_left
      (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  exact bounded_application_tendsto (𝓝[>] (0 : ℝ))
    (fun h => star (scalarRightRegularization P h)) 1 hb
    (fun h => T (scalarRightRegularization P h x)) (T x) (T x)
    (scalarCommutantRegularization_tendsto P T x) hl

theorem scalarCommutantSandwich_star_tendsto (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (x : ScalarGNSHilbert P) :
    Tendsto (fun h : ℝ => star (scalarCommutantSandwich P T h) x)
      (𝓝[>] 0) (𝓝 (star T x)) := by
  simpa only [scalarCommutantSandwich_star] using scalarCommutantSandwich_tendsto P (star T) x

/-- Every commutant operator is approximated strongly-* with uniform bound
by operators having BOTH right-vector identities on the same full ideal. -/
theorem scalarCommutant_paired_right_approximation (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : T ∈ StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P))) :
    (∀ᶠ h in 𝓝[>] (0 : ℝ), Nonempty (ScalarRightAdjointPair P (scalarCommutantSandwich P T h))) ∧
    (∀ h : ℝ, ‖scalarCommutantSandwich P T h‖ ≤ ‖T‖) ∧
    (∀ x, Tendsto (fun h : ℝ => scalarCommutantSandwich P T h x) (𝓝[>] 0) (𝓝 (T x))) ∧
    (∀ x, Tendsto (fun h : ℝ => star (scalarCommutantSandwich P T h) x)
      (𝓝[>] 0) (𝓝 (star T x))) := by
  refine ⟨?_,scalarCommutantSandwich_norm_le P T,scalarCommutantSandwich_tendsto P T,
    scalarCommutantSandwich_star_tendsto P T⟩
  filter_upwards [self_mem_nhdsWithin] with h hh
  refine ⟨scalarCommutantSandwichPair P T ?_ h hh⟩
  intro a
  rw [StarSubalgebra.mem_centralizer_iff] at hT
  exact (hT _ (Set.mem_range_self a)).1.symm

#print axioms scalarGNSCommutation_adjoint
#print axioms scalarRightRegularization_adjoint_tendsto
#print axioms scalarCommutantSandwich
#print axioms scalarCommutantSandwich_star
#print axioms scalarCommutantSandwich_norm_le
#print axioms scalarCommutantSandwichVector
#print axioms scalarCommutantSandwich_right
#print axioms scalarCommutantSandwichPair
#print axioms scalarCommutantSandwich_in_original_adjoint
#print axioms scalarCommutantSandwich_tendsto
#print axioms scalarCommutantSandwich_star_tendsto
#print axioms scalarCommutant_paired_right_approximation
end
end TGLV350.Regular
