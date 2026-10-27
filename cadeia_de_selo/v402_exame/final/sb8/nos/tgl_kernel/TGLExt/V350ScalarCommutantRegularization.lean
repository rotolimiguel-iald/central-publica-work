import TGLExt.V350ScalarRightRegularization
import TGLExt.V350RegularNormality

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- A bounded right multiplier on the ORIGINAL full weight ideal. This
predicate alone does not assert an adjoint vector or a Hilbert algebra. -/
def ScalarRightBounded (P : SiteProfile)
    (R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) : Prop :=
  ∃ η : ScalarGNSHilbert P, ∀ a : scalarWeightLeftIdeal P,
    R (scalarWeightGNSEmbedding P a) = scalarGNSRepresentation P a.val η

theorem scalarRightBounded_commutes (P : SiteProfile)
    (R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hR : ScalarRightBounded P R)
    (b : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute R (scalarGNSRepresentation P b) := by
  obtain ⟨η,hη⟩ := hR
  ext1 x
  refine (scalarWeightGNSEmbedding_denseRange P).induction_on x
    (isClosed_eq (by fun_prop) (by fun_prop)) ?_
  intro a
  change R (scalarGNSRepresentation P b (scalarWeightGNSEmbedding P a)) =
    scalarGNSRepresentation P b (R (scalarWeightGNSEmbedding P a))
  conv_lhs => rw [scalarWeightGNSAction_intertwines P b a]
  conv_lhs => rw [hη (scalarWeightLeftProduct P b a)]
  conv_rhs => rw [hη a]
  change scalarGNSRepresentation P (b*a.val) η = _
  rw [map_mul]
  rfl

theorem scalarRightBounded_commutant_mem (P : SiteProfile)
    (R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hR : ScalarRightBounded P R) :
    R ∈ StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P)) := by
  rw [StarSubalgebra.mem_centralizer_iff]
  rintro _ ⟨a,rfl⟩
  constructor
  · exact (scalarRightBounded_commutes P R hR a).eq.symm
  · rw [← map_star]
    exact (scalarRightBounded_commutes P R hR (star a)).eq.symm

theorem scalarRightRegularization_rightBounded (P : SiteProfile) (h : ℝ) (hh : 0 < h) :
    ScalarRightBounded P (scalarRightRegularization P h) :=
  ⟨scalarRegularizationVector P h hh,scalarRightRegularization_vector P h hh⟩

theorem scalarCommutantRegularization_rightBounded (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : ∀ a, Commute T (scalarGNSRepresentation P a)) (h : ℝ) (hh : 0 < h) :
    ScalarRightBounded P (T * scalarRightRegularization P h) := by
  refine ⟨T (scalarRegularizationVector P h hh),?_⟩
  intro a
  change T (scalarRightRegularization P h (scalarWeightGNSEmbedding P a)) = _
  rw [scalarRightRegularization_vector P h hh]
  exact congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
    B (scalarRegularizationVector P h hh)) (hT a.val).eq

theorem scalarCommutantRegularization_norm_le (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (h : ℝ) :
    ‖T * scalarRightRegularization P h‖ ≤ ‖T‖ :=
  (norm_mul_le T (scalarRightRegularization P h)).trans (by
    simpa only [mul_one] using mul_le_mul_of_nonneg_left
      (scalarRightRegularization_norm_le P h) (norm_nonneg T))

theorem scalarCommutantRegularization_tendsto (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (x : ScalarGNSHilbert P) :
    Tendsto (fun h : ℝ => (T * scalarRightRegularization P h) x)
      (𝓝[>] 0) (𝓝 (T x)) :=
  (T.continuous.continuousAt.tendsto.comp (scalarRightRegularization_tendsto P x)).mono_left
    (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))

/-- Every commutant element has concrete uniformly bounded right-multiplier
approximants. The reconstruction as J*pi(a)*J remains a separate obligation. -/
theorem scalarCommutant_rightBounded_approximation (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : T ∈ StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P))) :
    (∀ᶠ h in 𝓝[>] (0 : ℝ), ScalarRightBounded P (T * scalarRightRegularization P h)) ∧
    (∀ h : ℝ, ‖T * scalarRightRegularization P h‖ ≤ ‖T‖) ∧
    (∀ x, Tendsto (fun h : ℝ => (T * scalarRightRegularization P h) x)
      (𝓝[>] 0) (𝓝 (T x))) := by
  refine ⟨?_,scalarCommutantRegularization_norm_le P T,scalarCommutantRegularization_tendsto P T⟩
  filter_upwards [self_mem_nhdsWithin] with h hh
  apply scalarCommutantRegularization_rightBounded P T _ h hh
  intro a
  rw [StarSubalgebra.mem_centralizer_iff] at hT
  exact (hT _ (Set.mem_range_self a)).1.symm

/-- A sufficient closure criterion with a REAL reconstruction premise.
No assertion here says that the polar image is already a von Neumann algebra. -/
theorem scalarCommutant_mem_of_rightBounded (P : SiteProfile)
    (Q : VonNeumannAlgebra (ScalarGNSHilbert P))
    (hQ : ∀ R, ScalarRightBounded P R → R ∈ Q)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : T ∈ StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P))) :
    T ∈ Q := by
  obtain ⟨ha,_,ht⟩ := scalarCommutant_rightBounded_approximation P T hT
  exact vonNeumann_mem_of_strong_limit Q _ T (ha.mono (fun h hh => hQ _ hh)) ht

theorem scalarCommutant_mem_generated_rightBounded (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : T ∈ StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P))) :
    T ∈ generatedAlgebra {R | ScalarRightBounded P R} :=
  scalarCommutant_mem_of_rightBounded P _ (fun _ hR => generator_mem hR) T hT

#print axioms ScalarRightBounded
#print axioms scalarRightBounded_commutes
#print axioms scalarRightBounded_commutant_mem
#print axioms scalarRightRegularization_rightBounded
#print axioms scalarCommutantRegularization_rightBounded
#print axioms scalarCommutantRegularization_norm_le
#print axioms scalarCommutantRegularization_tendsto
#print axioms scalarCommutant_rightBounded_approximation
#print axioms scalarCommutant_mem_of_rightBounded
#print axioms scalarCommutant_mem_generated_rightBounded
end
end TGLV350.Regular
