import AperiodicPhaseAverage

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Aperiodic046

open TGLExt Matrix MeasureTheory Filter
open scoped Topology

noncomputable section

/-- Projecting a finite-time average is exactly the local finite matrix average. -/
theorem period_average_prefix_vector (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (N : ℕ) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N (periodAverage P T hT A) (hOmega P) =
      levelEmbeddingCLM P N (flowAverage P T N (expectationMatrix P N A)) := by
  rw [expectation_omega, (period_average_operator T hT A).1]
  have ho (t : ℝ) : modularConjugation P t A (hOmega P) =
      modularFlow P t (A (hOmega P)) := by
    change modularFlow P t (A (modularFlow P (-t) (hOmega P))) = _
    rw [modularFlow_fixes_omega]
  simp_rw [ho]
  rw [(levelProject P N).map_smul_of_tower,
    ← (levelProject P N).intervalIntegral_comp_comm
      ((modularFlow_strongly_continuous (A (hOmega P))).intervalIntegrable 0 T)]
  simp_rw [project_flow_commutes, ← expectation_omega]
  change T⁻¹ • (∫ t in (0 : ℝ)..T,
    modularFlow P t (towerPi P (expectationMatrix P N A) (hOmega P))) = _
  simp_rw [towerPi_omega]
  exact local_average_eq_embedding P T N (expectationMatrix P N A)

/-- Each finite cut of the time averages has the spectral-pinching limit. -/
theorem period_average_prefix_omega_limit (P : SiteProfile) (N : ℕ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    Tendsto
      (fun n : ℕ => towerExpectation P N
        (periodAverage P ((n : ℝ) + 1) (by positivity) A) (hOmega P))
      atTop (𝓝 (levelEmbedding P N
        (specExpect (towerW P N) (expectationMatrix P N A)))) := by
  have h := ((levelEmbeddingCLM P N).continuous.tendsto
      (specExpect (towerW P N) (expectationMatrix P N A))).comp
    (flow_average_limit P N (expectationMatrix P N A))
  have he : levelEmbeddingCLM P N
      (specExpect (towerW P N) (expectationMatrix P N A)) =
      levelEmbedding P N (specExpect (towerW P N) (expectationMatrix P N A)) := rfl
  rw [he] at h
  apply h.congr'
  exact Filter.Eventually.of_forall (fun n =>
    (period_average_prefix_vector P ((n : ℝ) + 1) (by positivity) N A).symm)

/-- A limit on Ω forces the exact prefix identity; existence of that limit is separate. -/
theorem aperiodic_average_prefix_of_limit (P : SiteProfile) (N : ℕ)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hlim : Tendsto
      (fun n : ℕ => periodAverage P ((n : ℝ) + 1) (by positivity) A (hOmega P))
      atTop (𝓝 (B (hOmega P)))) :
    towerExpectation P N B =
      towerPi P (specExpect (towerW P N) (expectationMatrix P N A)) := by
  apply factor_eq_of_omega (expectation_mem_factor _ _) (towerPi_mem_factor _)
  rw [towerPi_omega]
  have h : Tendsto
      (fun n : ℕ => towerExpectation P N
        (periodAverage P ((n : ℝ) + 1) (by positivity) A) (hOmega P))
      atTop (𝓝 (towerExpectation P N B (hOmega P))) := by
    simpa only [expectation_omega, Function.comp_apply] using
      ((levelProject P N).continuous.tendsto (B (hOmega P))).comp hlim
  exact tendsto_nhds_unique h (period_average_prefix_omega_limit P N A)

#print axioms period_average_prefix_vector
#print axioms period_average_prefix_omega_limit
#print axioms aperiodic_average_prefix_of_limit

end

end ChatgptAudit.Aperiodic046
