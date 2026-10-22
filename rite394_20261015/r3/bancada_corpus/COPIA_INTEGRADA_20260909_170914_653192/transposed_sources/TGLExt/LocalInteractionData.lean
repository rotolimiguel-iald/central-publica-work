import TGLExt.FiniteLevelExponentials
import TGLExt.SummableInteractionModularOrbit

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit.LocalInteraction
open TGLExt Filter Topology Set ChatgptAudit ChatgptAudit.FiniteLevel
  ChatgptAudit.SummableInteraction ChatgptAudit.InteractionOrbit ChatgptAudit.Cocycle030
noncomputable section

/-- Absolute norm summability and finite support, with no pairwise commutation requirement. -/
structure LocalInteractionData (P : SiteProfile) where
  term : ℕ → (TowerHilbert P →L[ℂ] TowerHilbert P)
  selfadjoint : ∀ j, IsSelfAdjoint (term j)
  support : ∀ j, term j ∈ levelOperatorAlgebra P (j+1)
  norm_summable : Summable (fun j => ‖term j‖)

def localPrefix (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    InteractionOperator P := ∑ j ∈ Finset.range N, D.term j

def localPotential (P : SiteProfile) (D : LocalInteractionData P) : InteractionOperator P :=
  ∑' j, D.term j

def normTail (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) : ℝ :=
  ∑' j, ‖D.term (j+N)‖

theorem local_term_summable (P : SiteProfile) (D : LocalInteractionData P) :
    Summable D.term := D.norm_summable.of_norm

theorem local_prefix_mem_level (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    localPrefix P D N ∈ levelOperatorAlgebra P N := by
  unfold localPrefix
  apply (levelOperatorAlgebra P N).sum_mem
  intro j hj
  exact finite_level_mono P (Nat.succ_le_of_lt (Finset.mem_range.mp hj)) (D.support j)

theorem local_prefix_selfadjoint (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    IsSelfAdjoint (localPrefix P D N) := by
  change star (∑ j ∈ Finset.range N, D.term j) = _
  simp only [star_sum, (D.selfadjoint _).star_eq]
  rfl

theorem local_term_mem_factor (P : SiteProfile) (D : LocalInteractionData P) (j : ℕ) :
    D.term j ∈ theFactorObject P := by
  obtain ⟨a,ha⟩ := D.support j
  rw [←ha]
  exact towerPi_mem_factor a

theorem local_prefix_mem_factor (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    localPrefix P D N ∈ theFactorObject P :=
  sum_mem (fun j _ => local_term_mem_factor P D j)

theorem local_prefix_tendsto (P : SiteProfile) (D : LocalInteractionData P) :
    Tendsto (localPrefix P D) atTop (𝓝 (localPotential P D)) :=
  (local_term_summable P D).hasSum.tendsto_sum_nat

theorem local_potential_selfadjoint (P : SiteProfile) (D : LocalInteractionData P) :
    IsSelfAdjoint (localPotential P D) := by
  change star (∑' j, D.term j) = _
  rw [tsum_star]
  simp only [(D.selfadjoint _).star_eq]
  rfl

theorem local_potential_mem_factor (P : SiteProfile) (D : LocalInteractionData P) :
    localPotential P D ∈ theFactorObject P :=
  tsum_mem (factor_norm_closed P) (fun j => local_term_mem_factor P D j)

theorem local_potential_norm_bound (P : SiteProfile) (D : LocalInteractionData P) :
    ‖localPotential P D‖ ≤ ∑' j, ‖D.term j‖ :=
  tsum_of_norm_bounded D.norm_summable.hasSum (fun _ => le_rfl)

theorem local_prefix_uniform_bound (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    ‖localPrefix P D N‖ ≤ ∑' j, ‖D.term j‖ :=
  (norm_sum_le _ _).trans (D.norm_summable.sum_le_tsum _ (fun _ _ => norm_nonneg _))

theorem norm_tail_nonnegative (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    0 ≤ normTail P D N := tsum_nonneg (fun _ => norm_nonneg _)

theorem local_prefix_add_tail (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    localPrefix P D N + (∑' j, D.term (j+N)) = localPotential P D :=
  (local_term_summable P D).sum_add_tsum_nat_add N

theorem local_potential_sub_prefix (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    localPotential P D - localPrefix P D N = ∑' j, D.term (j+N) := by
  rw [←local_prefix_add_tail P D N]
  abel

theorem local_cutoff_error (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    ‖localPotential P D - localPrefix P D N‖ ≤ normTail P D N := by
  rw [local_potential_sub_prefix]
  exact tsum_of_norm_bounded ((summable_nat_add_iff N).mpr D.norm_summable).hasSum
    (fun _ => le_rfl)

theorem norm_tail_as_remainder (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    normTail P D N = (∑' j, ‖D.term j‖) - ∑ j ∈ Finset.range N, ‖D.term j‖ := by
  have h := D.norm_summable.sum_add_tsum_nat_add N
  change (∑ j ∈ Finset.range N, ‖D.term j‖) + normTail P D N = _ at h
  linarith

theorem norm_tail_antitone (P : SiteProfile) (D : LocalInteractionData P) :
    Antitone (normTail P D) := by
  intro N M hNM
  rw [norm_tail_as_remainder,norm_tail_as_remainder]
  apply sub_le_sub_left
  exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.range_mono hNM)
    (fun j _ _ => norm_nonneg (D.term j))

theorem norm_tail_tendsto (P : SiteProfile) (D : LocalInteractionData P) :
    Tendsto (normTail P D) atTop (𝓝 0) := by
  have heq : normTail P D =
      (fun N => (∑' j, ‖D.term j‖) - ∑ j ∈ Finset.range N, ‖D.term j‖) :=
    funext (norm_tail_as_remainder P D)
  rw [heq]
  have ht : Tendsto (fun _ : ℕ => (∑' j, ‖D.term j‖)) atTop (𝓝 (∑' j, ‖D.term j‖)) :=
    tendsto_const_nhds
  simpa using ht.sub D.norm_summable.hasSum.tendsto_sum_nat

theorem local_prefix_difference (P : SiteProfile) (D : LocalInteractionData P)
    (N M : ℕ) (hNM : N ≤ M) :
    ‖localPrefix P D N - localPrefix P D M‖ ≤ 2 * normTail P D N := by
  have hn : ‖localPrefix P D N - localPotential P D‖ ≤ normTail P D N := by
    rw [norm_sub_rev]
    exact local_cutoff_error P D N
  have hm := local_cutoff_error P D M
  have ht := norm_tail_antitone P D hNM
  have he : localPrefix P D N - localPrefix P D M =
      (localPrefix P D N - localPotential P D) +
        (localPotential P D - localPrefix P D M) := by abel
  rw [he]
  exact (norm_add_le _ _).trans (by linarith)

def localOrbit (P : SiteProfile) (D : LocalInteractionData P) (t : ℝ) :
    InteractionOperator P := modularConjugation P t (localPotential P D)

def localPrefixOrbit (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) (t : ℝ) :
    InteractionOperator P := modularConjugation P t (localPrefix P D N)

theorem local_prefix_orbit_continuous (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) :
    Continuous (localPrefixOrbit P D N) := by
  obtain ⟨a,ha⟩ := local_prefix_mem_level P D N
  unfold localPrefixOrbit
  rw [←ha]
  exact local_modular_orbit_norm_continuous P N a

theorem local_orbit_cutoff_error (P : SiteProfile) (D : LocalInteractionData P) (N : ℕ) (t : ℝ) :
    ‖localOrbit P D t - localPrefixOrbit P D N t‖ ≤ normTail P D N := by
  unfold localOrbit localPrefixOrbit
  rw [←map_sub,canonical_conjugation_norm]
  exact local_cutoff_error P D N

theorem local_orbit_continuous (P : SiteProfile) (D : LocalInteractionData P) :
    Continuous (localOrbit P D) := by
  apply continuous_iff_continuousAt.mpr
  intro s
  rw [Metric.continuousAt_iff]
  intro ε hε
  obtain ⟨N,hN⟩ := Metric.tendsto_atTop.mp (local_prefix_tendsto P D)
    (ε/3) (by positivity)
  have hnear : dist (localPrefix P D N) (localPotential P D) < ε/3 := hN N le_rfl
  obtain ⟨δ,hδ,hloc⟩ := Metric.continuousAt_iff.mp
    (local_prefix_orbit_continuous P D N).continuousAt (ε/3) (by positivity)
  refine ⟨δ,hδ,fun t ht => ?_⟩
  have h1 : dist (localOrbit P D t) (localPrefixOrbit P D N t) =
      dist (localPrefix P D N) (localPotential P D) := by
    exact ((canonical_conjugation_isometry P t).dist_eq _ _).trans (dist_comm _ _)
  have h2 : dist (localPrefixOrbit P D N s) (localOrbit P D s) =
      dist (localPrefix P D N) (localPotential P D) :=
    (canonical_conjugation_isometry P s).dist_eq _ _
  have h3 := dist_triangle (localOrbit P D t) (localPrefixOrbit P D N t) (localOrbit P D s)
  have h4 := dist_triangle (localPrefixOrbit P D N t) (localPrefixOrbit P D N s) (localOrbit P D s)
  have h5 := hloc ht
  rw [h1] at h3
  rw [h2] at h4
  linarith

#print axioms LocalInteractionData
#print axioms localPrefix
#print axioms localPotential
#print axioms normTail
#print axioms local_term_summable
#print axioms local_prefix_mem_level
#print axioms local_prefix_selfadjoint
#print axioms local_term_mem_factor
#print axioms local_prefix_mem_factor
#print axioms local_prefix_tendsto
#print axioms local_potential_selfadjoint
#print axioms local_potential_mem_factor
#print axioms local_potential_norm_bound
#print axioms local_prefix_uniform_bound
#print axioms norm_tail_nonnegative
#print axioms local_prefix_add_tail
#print axioms local_potential_sub_prefix
#print axioms local_cutoff_error
#print axioms norm_tail_as_remainder
#print axioms norm_tail_antitone
#print axioms norm_tail_tendsto
#print axioms local_prefix_difference
#print axioms localOrbit
#print axioms localPrefixOrbit
#print axioms local_prefix_orbit_continuous
#print axioms local_orbit_cutoff_error
#print axioms local_orbit_continuous
end
end ChatgptAudit.LocalInteraction
