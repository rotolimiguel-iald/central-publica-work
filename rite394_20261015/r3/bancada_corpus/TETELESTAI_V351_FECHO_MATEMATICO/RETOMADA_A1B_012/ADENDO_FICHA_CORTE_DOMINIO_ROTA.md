[OPEN — rota e APIs antes do código]

2026-09-14T23:03:55.306868-03:00

Use q_delta directly. The first module supplies bounded contractions, membership/right action, inverse-product bound and strong convergence. The next consumer applies the existing right-perturbed weight comparison and WOT closure. This splits algebraic/operator estimates from the scalar finiteness proof, not duplicate definitions. No new root.

Consulta lida integralmente: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_consulta_semifinitude_limite\CONSULTA_SEMIFINITUDE_LIMITE.md

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\MetricSpace\UniformConvergence.lean:94 — 01ed18a99a0f7b7183c033776cddfcd198c3e9b9000809d4c7572d6436c63e3a

```lean
/-- If `f : α → γ → β` is a family of a functions, all of which are Lipschitz with the
same constant, then the family is uniformly equicontinuous. -/
lemma _root_.LipschitzWith.uniformEquicontinuous (f : α → γ → β) (K : ℝ≥0)
    (h : ∀ c, LipschitzWith K (f c)) : UniformEquicontinuous f := by
  rw [uniformEquicontinuous_iff_uniformContinuous]
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\MetricSpace\Lipschitz.lean:45 — eccab81f2b1ff62fdc7dccd4753a2f83dd2725cccabe2cc6e98e6a97147a6eb9

```lean
theorem lipschitzWith_iff_dist_le_mul [PseudoMetricSpace α] [PseudoMetricSpace β] {K : ℝ≥0}
    {f : α → β} : LipschitzWith K f ↔ ∀ x y, dist (f x) (f y) ≤ K * dist x y := by
  simp only [LipschitzWith, edist_nndist, dist_nndist]
  norm_cast

alias ⟨LipschitzWith.dist_le_mul, LipschitzWith.of_dist_le_mul⟩ := lipschitzWith_iff_dist_le_mul

```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecificLimits\Basic.lean:69 — dbbeb301e5b9dacc96ecd233fd05a02846a1fc88c9606f1b1d413d08aff5142e

```lean
theorem tendsto_one_div_add_atTop_nhds_zero_nat {𝕜 : Type*} [DivisionSemiring 𝕜] [CharZero 𝕜]
    [TopologicalSpace 𝕜] [ContinuousSMul ℚ≥0 𝕜] :
    Tendsto (fun n : ℕ ↦ 1 / ((n : 𝕜) + 1)) atTop (𝓝 0) :=
  suffices Tendsto (fun n : ℕ ↦ 1 / (↑(n + 1) : 𝕜)) atTop (𝓝 0) by simpa
  (tendsto_add_atTop_iff_nat 1).2 tendsto_one_div_atTop_nhds_zero_nat

theorem tendsto_algebraMap_inv_atTop_nhds_zero_nat {𝕜 : Type*} (A : Type*)
```

