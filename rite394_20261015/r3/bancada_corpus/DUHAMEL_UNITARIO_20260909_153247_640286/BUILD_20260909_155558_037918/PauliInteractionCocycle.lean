import SpectatorCancellation
import FiniteModularHamiltonian
import FiniteLevelExponentials
import CocycleNormLimit

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.PauliCocycle
open TGLExt Matrix Filter Topology Set ChatgptAudit ChatgptAudit.Observable035
  ChatgptAudit.UnitaryDuhamel ChatgptAudit.BoundedPerturbation
  ChatgptAudit.SpectatorCancellation ChatgptAudit.FiniteModular ChatgptAudit.FiniteLevel
  ChatgptAudit.SummableInteraction ChatgptAudit.AdmissibleInteraction
  ChatgptAudit.InteractionOrbit ChatgptAudit.CocycleLimit
noncomputable section

theorem site_x_mem_level (P : SiteProfile) {j N : ℕ} (h : j ≤ N) :
    sitePauliX P j ∈ levelOperatorAlgebra P N := by
  refine ⟨tPush h (lastSiteMatrix j pauliXMatrix), ?_⟩
  exact towerPi_compat h (lastSiteMatrix j pauliXMatrix)

theorem pauli_bond_mem_level (P : SiteProfile) {j N : ℕ} (h : j < N) :
    pauliBond P j ∈ levelOperatorAlgebra P N :=
  (levelOperatorAlgebra P N).mul_mem (site_x_mem_level P (Nat.le_of_lt h))
    (site_x_mem_level P (Nat.succ_le_of_lt h))

theorem certified_prefix_mem_level (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    certifiedPrefix P c N ∈ levelOperatorAlgebra P N := by
  unfold certifiedPrefix interactionPrefix
  apply (levelOperatorAlgebra P N).sum_mem
  intro j hj
  exact (levelOperatorAlgebra P N).smul_mem
    (pauli_bond_mem_level P (Finset.mem_range.mp hj)) _

theorem certified_prefix_selfadjoint (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    IsSelfAdjoint (certifiedPrefix P c N) :=
  interaction_prefix_selfadjoint P c.value N

def pauliCutoffCocycle (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    Operator P := boundedCocycle (finiteModularHamiltonian P N) (certifiedPrefix P c N) t

theorem pauli_cutoff_zero (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    pauliCutoffCocycle P c N 0 = 1 := bounded_cocycle_zero _ _

theorem pauli_cutoff_unitary (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    pauliCutoffCocycle P c N t ∈ unitary _ :=
  bounded_cocycle_unitary _ _ (finite_hamiltonian_selfadjoint P N)
    (certified_prefix_selfadjoint P c N) t

theorem pauli_cutoff_continuous (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    Continuous (pauliCutoffCocycle P c N) := bounded_cocycle_continuous _ _

theorem pauli_cutoff_mem_level (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    pauliCutoffCocycle P c N t ∈ levelOperatorAlgebra P N := by
  simpa only [pauliCutoffCocycle, boundedCocycle, evolution, Complex.ofReal_neg] using
    finite_level_cocycle_mem P N _ _ (finite_hamiltonian_mem_level P N)
      (certified_prefix_mem_level P c N) t

theorem pauli_cutoff_mem_factor (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    pauliCutoffCocycle P c N t ∈ theFactorObject P := by
  obtain ⟨a,ha⟩ := pauli_cutoff_mem_level P c N t
  rw [← ha]
  exact towerPi_mem_factor a

theorem finite_inner_action_is_canonical (P : SiteProfile) (N : ℕ) (t : ℝ)
    (A : Operator P) (hA : A ∈ levelOperatorAlgebra P N) :
    innerAction (finiteModularHamiltonian P N) t A = modularConjugation P t A :=
  finite_modular_action_eq_canonical P N t A hA

/-- The finite certificate uses the canonical modular action, not a substituted action. -/
theorem pauli_cutoff_twisted (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (s t : ℝ) :
    pauliCutoffCocycle P c N (s+t) =
      pauliCutoffCocycle P c N s * modularConjugation P s (pauliCutoffCocycle P c N t) := by
  calc
    _ = pauliCutoffCocycle P c N s *
        innerAction (finiteModularHamiltonian P N) s (pauliCutoffCocycle P c N t) :=
      bounded_cocycle_twisted _ _ s t
    _ = _ := by rw [finite_inner_action_is_canonical P N s _ (pauli_cutoff_mem_level P c N t)]

theorem pauli_cutoff_derivative (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    HasDerivAt (pauliCutoffCocycle P c N)
      (pauliCutoffCocycle P c N t *
        modularConjugation P t (Complex.I • certifiedPrefix P c N)) t := by
  have h := bounded_cocycle_derivative_right (finiteModularHamiltonian P N)
    (certifiedPrefix P c N) t
  rw [finite_inner_action_is_canonical P N t _
    ((levelOperatorAlgebra P N).smul_mem (certified_prefix_mem_level P c N) Complex.I)] at h
  exact h

theorem pauli_cutoff_generator (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) :
    HasDerivAt (pauliCutoffCocycle P c N) (Complex.I • certifiedPrefix P c N) 0 :=
  bounded_cocycle_generator _ _

theorem coupling_tail_as_remainder (c : SummableCouplingData) (N : ℕ) :
    couplingTail c.value N = (∑' j, |c.value j|) - ∑ j ∈ Finset.range N, |c.value j| := by
  have h := c.norm_summable.sum_add_tsum_nat_add N
  change (∑ j ∈ Finset.range N, |c.value j|) + couplingTail c.value N = _ at h
  linarith

theorem coupling_tail_antitone (c : SummableCouplingData) : Antitone (couplingTail c.value) := by
  intro N M hNM
  rw [coupling_tail_as_remainder, coupling_tail_as_remainder]
  apply sub_le_sub_left
  exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.range_mono hNM)
    (fun j _ _ => abs_nonneg (c.value j))

theorem certified_prefix_difference (P : SiteProfile) (c : SummableCouplingData)
    (N M : ℕ) (hNM : N ≤ M) :
    ‖certifiedPrefix P c N - certifiedPrefix P c M‖ ≤ 2 * couplingTail c.value N := by
  have hn : ‖certifiedPrefix P c N - certifiedInteraction P c‖ ≤ couplingTail c.value N := by
    rw [norm_sub_rev]
    exact certified_cutoff_error P c N
  have hm := certified_cutoff_error P c M
  have ht := coupling_tail_antitone c hNM
  have he : certifiedPrefix P c N - certifiedPrefix P c M =
      (certifiedPrefix P c N - certifiedInteraction P c) +
        (certifiedInteraction P c - certifiedPrefix P c M) := by abel
  rw [he]
  exact (norm_add_le _ _).trans (by linarith)

theorem pauli_cutoff_ordered_bound (P : SiteProfile) (c : SummableCouplingData)
    (N M : ℕ) (hNM : N ≤ M) (t : ℝ) :
    ‖pauliCutoffCocycle P c N t - pauliCutoffCocycle P c M t‖ ≤
      (2 * couplingTail c.value N) * |t| := by
  have h := varying_background_duhamel
    (finiteModularHamiltonian P N) (finiteModularHamiltonian P M)
    (certifiedPrefix P c N) (certifiedPrefix P c M)
    (finite_hamiltonian_selfadjoint P M) (certified_prefix_selfadjoint P c N)
    (certified_prefix_selfadjoint P c M) (finite_spectator_commutes_base P hNM)
    (finite_spectator_commutes P hNM _ (certified_prefix_mem_level P c N)) t
  exact h.trans (mul_le_mul_of_nonneg_right (certified_prefix_difference P c N M hNM)
    (abs_nonneg t))

def pauliCutoffError (c : SummableCouplingData) (N : ℕ) : ℝ := 2 * couplingTail c.value N

theorem pauli_cutoff_error_nonnegative (c : SummableCouplingData) (N : ℕ) :
    0 ≤ pauliCutoffError c N := mul_nonneg (by norm_num) (coupling_tail_nonnegative c.value N)

theorem pauli_cutoff_error_tendsto (c : SummableCouplingData) :
    Tendsto (pauliCutoffError c) atTop (𝓝 0) := by
  change Tendsto (fun N : ℕ => (2 : ℝ) * couplingTail c.value N) atTop (𝓝 0)
  convert! (certified_tail_vanishes c).const_mul (2 : ℝ) using 1 <;> norm_num

theorem pauli_cutoff_difference_bound (P : SiteProfile) (c : SummableCouplingData)
    (N M : ℕ) (t : ℝ) :
    ‖pauliCutoffCocycle P c N t - pauliCutoffCocycle P c M t‖ ≤
      |t| * pauliCutoffError c (min N M) := by
  rcases le_total N M with h | h
  · simpa only [min_eq_left h, pauliCutoffError, mul_comm] using
      pauli_cutoff_ordered_bound P c N M h t
  · rw [norm_sub_rev, min_eq_right h]
    simpa only [pauliCutoffError, mul_comm] using pauli_cutoff_ordered_bound P c M N h t

/-- Every finite hypothesis is discharged by the concrete XX construction. -/
def pauliApproximation (P : SiteProfile) (c : SummableCouplingData) : CocycleApproximation P where
  cutoff := pauliCutoffCocycle P c
  error := pauliCutoffError c
  error_nonnegative := pauli_cutoff_error_nonnegative c
  error_tendsto := pauli_cutoff_error_tendsto c
  difference_bound := pauli_cutoff_difference_bound P c
  cutoff_continuous := pauli_cutoff_continuous P c
  cutoff_unitary := pauli_cutoff_unitary P c
  cutoff_factor := pauli_cutoff_mem_factor P c
  cutoff_twisted := pauli_cutoff_twisted P c

def pauliCocycle (P : SiteProfile) (c : SummableCouplingData) : ℝ → Operator P :=
  limitCocycle (pauliApproximation P c)

theorem pauli_cocycle_zero (P : SiteProfile) (c : SummableCouplingData) :
    pauliCocycle P c 0 = 1 := limit_cocycle_zero (pauliApproximation P c)

theorem pauli_cocycle_unitary (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    pauliCocycle P c t ∈ unitary _ := limit_cocycle_unitary (pauliApproximation P c) t

theorem pauli_cocycle_mem_factor (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    pauliCocycle P c t ∈ theFactorObject P := limit_cocycle_factor (pauliApproximation P c) t

theorem pauli_cocycle_continuous (P : SiteProfile) (c : SummableCouplingData) :
    Continuous (pauliCocycle P c) := limit_cocycle_continuous (pauliApproximation P c)

theorem pauli_cocycle_twisted (P : SiteProfile) (c : SummableCouplingData) (s t : ℝ) :
    pauliCocycle P c (s+t) = pauliCocycle P c s * modularConjugation P s (pauliCocycle P c t) :=
  limit_cocycle_twisted (pauliApproximation P c) s t

theorem pauli_cutoff_tendsto (P : SiteProfile) (c : SummableCouplingData) (t : ℝ) :
    Tendsto (fun N => pauliCutoffCocycle P c N t) atTop (𝓝 (pauliCocycle P c t)) :=
  cutoff_tendsto_limit (pauliApproximation P c) t

theorem pauli_cutoff_uniform_on_compact (P : SiteProfile) (c : SummableCouplingData)
    (K : Set ℝ) (hK : IsCompact K) :
    TendstoUniformlyOn (pauliCutoffCocycle P c) (pauliCocycle P c) atTop K :=
  cutoff_uniform_on_compact (pauliApproximation P c) K hK

theorem pauli_cocycle_cutoff_bound (P : SiteProfile) (c : SummableCouplingData) (N : ℕ) (t : ℝ) :
    ‖pauliCocycle P c t - pauliCutoffCocycle P c N t‖ ≤ |t| * pauliCutoffError c N :=
  limit_cutoff_bound (pauliApproximation P c) N t

#print axioms site_x_mem_level
#print axioms pauli_bond_mem_level
#print axioms certified_prefix_mem_level
#print axioms certified_prefix_selfadjoint
#print axioms pauliCutoffCocycle
#print axioms pauli_cutoff_zero
#print axioms pauli_cutoff_unitary
#print axioms pauli_cutoff_continuous
#print axioms pauli_cutoff_mem_level
#print axioms pauli_cutoff_mem_factor
#print axioms finite_inner_action_is_canonical
#print axioms pauli_cutoff_twisted
#print axioms pauli_cutoff_derivative
#print axioms pauli_cutoff_generator
#print axioms coupling_tail_as_remainder
#print axioms coupling_tail_antitone
#print axioms certified_prefix_difference
#print axioms pauli_cutoff_ordered_bound
#print axioms pauliCutoffError
#print axioms pauli_cutoff_error_nonnegative
#print axioms pauli_cutoff_error_tendsto
#print axioms pauli_cutoff_difference_bound
#print axioms pauliApproximation
#print axioms pauliCocycle
#print axioms pauli_cocycle_zero
#print axioms pauli_cocycle_unitary
#print axioms pauli_cocycle_mem_factor
#print axioms pauli_cocycle_continuous
#print axioms pauli_cocycle_twisted
#print axioms pauli_cutoff_tendsto
#print axioms pauli_cutoff_uniform_on_compact
#print axioms pauli_cocycle_cutoff_bound
end
end ChatgptAudit.PauliCocycle
