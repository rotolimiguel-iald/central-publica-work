import TheUnitIsTheRank

/-!
# SONDA S1' (auditor REPRO r2) — o CONTRÁRIO de cada S1.k é REFUTADO (esperado: compila, 0 erros).
-/

open TGLExt TGLExt.TheUnitIsTheRank Matrix Filter Topology

theorem s1r_1 : ¬ (rhoStar.rank = 2) := by
  rw [rhoStar_rank]
  norm_num

/-- e SEM o acoplamento: a testemunha θ = π/4 basta (a hipótese `c` de `rank_not_preserved_by_dephasing` não é
    necessária para a conclusão — ver também S3.1). -/
theorem s1r_2 : ¬ ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank := by
  intro h
  have h1 := h (Real.pi / 4)
  rw [(endpoint_rank_two_iff _).mpr probe_angles.1, (fractal_one_is_rank_one _).1] at h1
  exact absurd h1 (by norm_num)

theorem s1r_3 : ¬ ∀ θ : ℝ, 0 < Complex.normSq ((Smat θ).mulVec e1 0) → dephasingActs unitRates θ :=
  literal_transmission_does_not_force_dephasing unitRates unitRates_spec.1

theorem s1r_4 (c : TGLCoupling) : ¬ ((rhoStar * Qtheta (thetaMiguel c.beta)).trace ≠ (c.beta : ℂ)) :=
  fun h => h (leak_at_thetaMiguel c)

theorem s1r_5 : anticomm (Qtheta (Real.pi / 4)) rhoStar ≠ 0 :=
  probe_anticomm_both_sides.2.1

theorem s1r_6 : ¬ ∃ L : ℝ, Tendsto (fun k : ℕ => Real.sin (k * 1) ^ 2) atTop (𝓝 L) :=
  angular_leak_no_limit 1 probe_angles.2.2.1
