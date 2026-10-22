import ExpectationAlgebra
import AperiodicVectorAverage

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Expectation047

open TGLExt Filter ChatgptAudit.Aperiodic046
open scoped Topology

noncomputable section

/-- The constructed averages yield the GNS norm bound; uniqueness transfers it to every contract. -/
theorem expectation_gns_norm_le (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    ‖I.E A (hOmega P)‖ ≤ ‖A (hOmega P)‖ := by
  have hl := (aperiodic_expectation_spec P A hA).2.2 (hOmega P)
  have hb (n : ℕ) :
      ‖periodAverage P ((n : ℝ) + 1) (by positivity) A (hOmega P)‖ ≤
        ‖A (hOmega P)‖ := by
    rw [period_average_omega_eq_vector_average]
    change ‖modularAverageVector P ((n : ℝ) + 1) (A (hOmega P))‖ ≤ _
    exact modular_average_vector_bound P ((n : ℝ) + 1) (by positivity) _
  have h := le_of_tendsto hl.norm (Filter.Eventually.of_forall hb)
  have he := the_expectation_is_unique I (aperiodicExpectationInput P) A hA
  change I.E A = aperiodicExpectation P A at he
  rw [he]
  exact h

/-- The GNS metric contracts on pairs of factor elements. -/
theorem expectation_gns_dist_le (P : SiteProfile) (I : ExpectationInput P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P) :
    dist (I.E A (hOmega P)) (I.E B (hOmega P)) ≤
      dist (A (hOmega P)) (B (hOmega P)) := by
  have h := expectation_gns_norm_le P I (A - B) ((theFactorObject P).sub_mem hA hB)
  rw [expectation_sub P I A B hA hB] at h
  simpa only [dist_eq_norm, _root_.sub_apply] using h

/-- Convergence in the GNS metric is preserved for an arbitrary index filter. -/
theorem expectation_omega_tendsto (P : SiteProfile) (I : ExpectationInput P)
    {ι : Type*} (l : Filter ι)
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : ∀ i, A i ∈ theFactorObject P) (hB : B ∈ theFactorObject P)
    (hlim : Tendsto (fun i => A i (hOmega P)) l (𝓝 (B (hOmega P)))) :
    Tendsto (fun i => I.E (A i) (hOmega P)) l (𝓝 (I.E B (hOmega P))) := by
  rw [Metric.tendsto_nhds] at hlim ⊢
  intro ε hε
  filter_upwards [hlim ε hε] with i hi
  exact lt_of_le_of_lt (expectation_gns_dist_le P I (A i) B (hA i) hB) hi

/-- Uniformly bounded operators converging on the dense local space converge on every vector. -/
theorem bounded_local_tendsto (P : SiteProfile) {ι : Type*} (l : Filter ι)
    (C : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (bound : ℝ) (hbound : 0 ≤ bound) (hnorm : ∀ i, ‖C i‖ ≤ bound)
    (hlocal : ∀ w : TowerPre P,
      Tendsto (fun i => C i (w : TowerHilbert P)) l (𝓝 (B (w : TowerHilbert P))))
    (v : TowerHilbert P) :
    Tendsto (fun i => C i v) l (𝓝 (B v)) := by
  rw [Metric.tendsto_nhds]
  intro ε hε
  have hden : 0 < 4 * (bound + ‖B‖ + 1) := by positivity
  obtain ⟨w, hw⟩ := (towerPre_denseRange (P := P)).exists_dist_lt v (div_pos hε hden)
  have hshort : bound * dist v (w : TowerHilbert P) < ε / 4 := by
    have hm := (lt_div_iff₀ hden).mp hw
    nlinarith [norm_nonneg B, (dist_nonneg : 0 ≤ dist v (w : TowerHilbert P))]
  have hBshort : ‖B‖ * dist v (w : TowerHilbert P) < ε / 4 := by
    have hm := (lt_div_iff₀ hden).mp hw
    nlinarith [(dist_nonneg : 0 ≤ dist v (w : TowerHilbert P))]
  have hmid := Metric.tendsto_nhds.mp (hlocal w) (ε / 2) (by positivity)
  filter_upwards [hmid] with i hi
  have hleft : dist (C i v) (C i (w : TowerHilbert P)) < ε / 4 :=
    lt_of_le_of_lt ((C i).dist_le_opNorm v (w : TowerHilbert P) |>.trans
      (mul_le_mul_of_nonneg_right (hnorm i)
        (dist_nonneg : 0 ≤ dist v (w : TowerHilbert P)))) hshort
  have hright : dist (B (w : TowerHilbert P)) (B v) < ε / 4 := by
    rw [dist_comm]
    exact lt_of_le_of_lt (B.dist_le_opNorm v (w : TowerHilbert P)) hBshort
  have ht := dist_triangle (C i v) (C i (w : TowerHilbert P)) (B v)
  have ht' := dist_triangle (C i (w : TowerHilbert P)) (B (w : TowerHilbert P)) (B v)
  linarith

/-- The right local orbit turns bounded convergence on Ω into strong convergence for any filter. -/
theorem bounded_omega_tendsto (P : SiteProfile) {ι : Type*} (l : Filter ι)
    (C : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (bound : ℝ) (hbound : 0 ≤ bound)
    (hmem : ∀ i, C i ∈ theFactorObject P) (hB : B ∈ theFactorObject P)
    (hnorm : ∀ i, ‖C i‖ ≤ bound)
    (hlim : Tendsto (fun i => C i (hOmega P)) l (𝓝 (B (hOmega P)))) :
    ∀ v, Tendsto (fun i => C i v) l (𝓝 (B v)) := by
  apply bounded_local_tendsto P l C B bound hbound hnorm
  intro w
  obtain ⟨N, a, rfl⟩ := exists_tof w
  rw [← rTowerPi_omega (P := P) N a]
  have hc (i : ι) : C i (rTowerPi P a (hOmega P)) =
      rTowerPi P a (C i (hOmega P)) := by
    simpa only [mul_apply_eq_comp] using
      congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P))
        (factor_comm_rTowerPi (hmem i) a)
  have hb : B (rTowerPi P a (hOmega P)) = rTowerPi P a (B (hOmega P)) := by
    simpa only [mul_apply_eq_comp] using
      congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P))
        (factor_comm_rTowerPi hB a)
  rw [hb]
  exact (((rTowerPi P a).continuous.tendsto (B (hOmega P))).comp hlim).congr'
    (Filter.Eventually.of_forall (fun i => (hc i).symm))

/-- Every expectation contract preserves bounded strong convergence, with arbitrary net indices. -/
theorem expectation_strong_tendsto_of_omega (P : SiteProfile) (I : ExpectationInput P)
    {ι : Type*} (l : Filter ι)
    (A : ι → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : ∀ i, A i ∈ theFactorObject P) (hB : B ∈ theFactorObject P)
    (bound : ℝ) (hbound : 0 ≤ bound) (hnorm : ∀ i, ‖A i‖ ≤ bound)
    (hlim : Tendsto (fun i => A i (hOmega P)) l (𝓝 (B (hOmega P)))) :
    ∀ v, Tendsto (fun i => I.E (A i) v) l (𝓝 (I.E B v)) := by
  apply bounded_omega_tendsto P l (fun i => I.E (A i)) (I.E B) bound hbound
    (fun i => (I.into (A i) (hA i)).1) (I.into B hB).1
  · intro i
    exact (expectation_norm_le P I (A i) (hA i)).trans (hnorm i)
  · exact expectation_omega_tendsto P I l A B hA hB hlim

#print axioms expectation_gns_norm_le
#print axioms expectation_gns_dist_le
#print axioms expectation_omega_tendsto
#print axioms bounded_local_tendsto
#print axioms bounded_omega_tendsto
#print axioms expectation_strong_tendsto_of_omega

end

end ChatgptAudit.Expectation047
