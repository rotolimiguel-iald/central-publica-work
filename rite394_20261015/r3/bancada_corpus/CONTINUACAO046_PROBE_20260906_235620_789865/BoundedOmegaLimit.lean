import TomitaClosability
import Mathlib.Analysis.Normed.Operator.Completeness
import Mathlib.Topology.MetricSpace.Cauchy

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Aperiodic046

open TGLExt Filter
open scoped Topology

noncomputable section

/-- Convergence on the cyclic vector propagates to each local right orbit. -/
theorem omega_limit_on_local (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ n, C n ∈ theFactorObject P)
    (z : TowerHilbert P)
    (hz : Tendsto (fun n => C n (hOmega P)) atTop (𝓝 z))
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Tendsto
      (fun n => C n ((tof P N a : TowerPre P) : TowerHilbert P))
      atTop (𝓝 (rTowerPi P a z)) := by
  rw [← rTowerPi_omega (P := P) N a]
  have he : (fun n => C n (rTowerPi P a (hOmega P))) =
      (fun n => rTowerPi P a (C n (hOmega P))) := by
    funext n
    simpa only [mul_apply_eq_comp] using
      congrArg (fun A : TowerHilbert P →L[ℂ] TowerHilbert P => A (hOmega P))
        (factor_comm_rTowerPi (hmem n) a)
  rw [he]
  exact ((rTowerPi P a).continuous.tendsto z).comp hz

/-- A common operator bound extends local Cauchy convergence to every Hilbert vector. -/
theorem bounded_local_cauchy (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (bound : ℝ) (hbound : 0 ≤ bound)
    (hnorm : ∀ n, ‖C n‖ ≤ bound)
    (hlocal : ∀ w : TowerPre P,
      CauchySeq (fun n => C n (w : TowerHilbert P)))
    (v : TowerHilbert P) :
    CauchySeq (fun n => C n v) := by
  apply Metric.cauchySeq_iff.mpr
  intro ε hε
  have hden : 0 < 4 * (bound + 1) := by positivity
  obtain ⟨w, hw⟩ := (towerPre_denseRange (P := P)).exists_dist_lt v
    (div_pos hε hden)
  have hshort : bound * dist v (w : TowerHilbert P) < ε / 4 := by
    have hmul := (lt_div_iff₀ hden).mp hw
    nlinarith [dist_nonneg v (w : TowerHilbert P)]
  obtain ⟨N, hN⟩ := Metric.cauchySeq_iff.mp (hlocal w) (ε / 2) (by positivity)
  refine ⟨N, ?_⟩
  intro m hm n hn
  have hmshort : dist (C m v) (C m (w : TowerHilbert P)) < ε / 4 :=
    lt_of_le_of_lt
      ((C m).dist_le_opNorm v (w : TowerHilbert P) |>.trans
        (mul_le_mul_of_nonneg_right (hnorm m)
          (dist_nonneg v (w : TowerHilbert P)))) hshort
  have hnshort : dist (C n (w : TowerHilbert P)) (C n v) < ε / 4 := by
    rw [dist_comm]
    exact lt_of_le_of_lt
      ((C n).dist_le_opNorm v (w : TowerHilbert P) |>.trans
        (mul_le_mul_of_nonneg_right (hnorm n)
          (dist_nonneg v (w : TowerHilbert P)))) hshort
  have hmid := hN m hm n hn
  have htri := dist_triangle (C m v) (C m (w : TowerHilbert P)) (C n v)
  have htri' := dist_triangle (C m (w : TowerHilbert P))
    (C n (w : TowerHilbert P)) (C n v)
  linarith

/-- Strong limits preserve a fixed commutation relation, without a norm limit. -/
theorem strong_limit_commutes (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B Y : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hlim : ∀ v, Tendsto (fun n => C n v) atTop (𝓝 (B v)))
    (hcomm : ∀ n, Y * C n = C n * Y) :
    Y * B = B * Y := by
  ext v
  change Y (B v) = B (Y v)
  have he : (fun n => Y (C n v)) = (fun n => C n (Y v)) := by
    funext n
    simpa only [mul_apply_eq_comp] using
      congrArg (fun A : TowerHilbert P →L[ℂ] TowerHilbert P => A v) (hcomm n)
  have hl := (Y.continuous.tendsto (B v)).comp (hlim v)
  change Tendsto (fun n => Y (C n v)) atTop (𝓝 (Y (B v))) at hl
  rw [he] at hl
  exact tendsto_nhds_unique hl (hlim (Y v))

/-- Membership in the factor passes to a strong limit through its defining bicommutant. -/
theorem factor_mem_of_strong_limit (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hmem : ∀ n, C n ∈ theFactorObject P)
    (hlim : ∀ v, Tendsto (fun n => C n v) atTop (𝓝 (B v))) :
    B ∈ theFactorObject P := by
  change B ∈ StarSubalgebra.centralizer ℂ
    ((StarSubalgebra.centralizer ℂ (towerImage P) :
      StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _)
  rw [StarSubalgebra.mem_centralizer_iff]
  intro Y hY
  have hc (n : ℕ) : Y * C n = C n * Y ∧ star Y * C n = C n * star Y := by
    have hn := hmem n
    change C n ∈ StarSubalgebra.centralizer ℂ
      ((StarSubalgebra.centralizer ℂ (towerImage P) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) : Set _) at hn
    rw [StarSubalgebra.mem_centralizer_iff] at hn
    exact hn Y hY
  exact ⟨strong_limit_commutes P C B Y hlim (fun n => (hc n).1),
    strong_limit_commutes P C B (star Y) hlim (fun n => (hc n).2)⟩

/-- Construct a bounded operator in the factor from a bounded sequence and its limit on Ω.
The strong limit and the operator itself are conclusions, not inputs. -/
theorem bounded_omega_limit_lift (P : SiteProfile)
    (C : ℕ → TowerHilbert P →L[ℂ] TowerHilbert P)
    (bound : ℝ) (hbound : 0 ≤ bound)
    (hmem : ∀ n, C n ∈ theFactorObject P)
    (hnorm : ∀ n, ‖C n‖ ≤ bound)
    (z : TowerHilbert P)
    (hz : Tendsto (fun n => C n (hOmega P)) atTop (𝓝 z)) :
    ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P ∧ ‖B‖ ≤ bound ∧ B (hOmega P) = z ∧
      ∀ v, Tendsto (fun n => C n v) atTop (𝓝 (B v)) := by
  have hlocal (w : TowerPre P) :
      CauchySeq (fun n => C n (w : TowerHilbert P)) := by
    obtain ⟨N, a, rfl⟩ := exists_tof w
    exact (omega_limit_on_local P C hmem z hz N a).cauchySeq
  have hex (v : TowerHilbert P) :
      ∃ y, Tendsto (fun n => C n v) atTop (𝓝 y) :=
    cauchySeq_tendsto_of_complete
      (bounded_local_cauchy P C bound hbound hnorm hlocal v)
  choose f hf using hex
  have hrange : Bornology.IsBounded (Set.range C) := by
    refine isBounded_iff_forall_norm_le.mpr ⟨bound, ?_⟩
    rintro D ⟨n, rfl⟩
    exact hnorm n
  let B : TowerHilbert P →L[ℂ] TowerHilbert P :=
    ContinuousLinearMap.ofTendstoOfBoundedRange f C (tendsto_pi_nhds.mpr hf) hrange
  have hBlim (v : TowerHilbert P) :
      Tendsto (fun n => C n v) atTop (𝓝 (B v)) := hf v
  have hBnorm : ‖B‖ ≤ bound := by
    apply B.opNorm_le_bound hbound
    intro v
    exact le_of_tendsto (hBlim v).norm
      (Filter.Eventually.of_forall fun n => (C n).le_of_opNorm_le (hnorm n) v)
  exact ⟨B, factor_mem_of_strong_limit P C B hmem hBlim, hBnorm,
    tendsto_nhds_unique (hBlim (hOmega P)) hz, hBlim⟩

/-- The constructed factor element is uniquely determined by its value on Ω. -/
theorem omega_lift_unique (P : SiteProfile)
    (B D : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hB : B ∈ theFactorObject P) (hD : D ∈ theFactorObject P)
    (z : TowerHilbert P) (hBz : B (hOmega P) = z) (hDz : D (hOmega P) = z) :
    B = D := by
  exact factor_eq_of_omega hB hD (hBz.trans hDz.symm)

#print axioms omega_limit_on_local
#print axioms bounded_local_cauchy
#print axioms strong_limit_commutes
#print axioms factor_mem_of_strong_limit
#print axioms bounded_omega_limit_lift
#print axioms omega_lift_unique

end

end ChatgptAudit.Aperiodic046
