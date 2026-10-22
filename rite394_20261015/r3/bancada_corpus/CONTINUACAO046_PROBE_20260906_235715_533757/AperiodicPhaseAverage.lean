import PeriodAveragePrefix
import Mathlib.Analysis.SpecificLimits.Basic

set_option autoImplicit false

namespace ChatgptAudit.Aperiodic046

open TGLExt Matrix MeasureTheory Filter
open scoped Topology

noncomputable section

/-- The normalized interval average of one modular phase. No period is specified. -/
def phaseAverage (T r : ℝ) : ℂ :=
  T⁻¹ • (∫ t in (0 : ℝ)..T, modularPhase t r)

/-- The zero frequency survives every nondegenerate averaging interval. -/
theorem phase_average_zero (T : ℝ) (hT : T ≠ 0) :
    phaseAverage T 0 = 1 := by
  have hz (t : ℝ) : modularPhase t 0 = 1 := by
    simp [modularPhase]
  unfold phaseAverage
  simp_rw [hz]
  rw [intervalIntegral.integral_const, sub_zero, smul_smul,
    inv_mul_cancel₀ hT, one_smul]

/-- An exact primitive for a nonzero frequency; no endpoint phase is assumed. -/
theorem integral_phase_nonzero (T r : ℝ) (hr : r ≠ 0) :
    (∫ t in (0 : ℝ)..T, modularPhase t r) =
      (modularPhase T r - 1) / ((r : ℂ) * Complex.I) := by
  have hc : (r : ℂ) * Complex.I ≠ 0 :=
    mul_ne_zero (by exact_mod_cast hr) Complex.I_ne_zero
  have he (t : ℝ) :
      modularPhase t r = Complex.exp (((r : ℂ) * Complex.I) * t) := by
    unfold modularPhase
    congr 1
    push_cast
    ring
  simp_rw [he]
  rw [integral_exp_mul_complex hc]
  simp only [Complex.ofReal_zero, mul_zero, Complex.exp_zero]

/-- The nonresonant average is bounded by an explicit inverse-length estimate. -/
theorem phase_average_norm_le (T r : ℝ) (hT : 0 < T) (hr : r ≠ 0) :
    ‖phaseAverage T r‖ ≤ T⁻¹ * (2 / |r|) := by
  have hn : ‖modularPhase T r - 1‖ ≤ 2 := by
    calc
      ‖modularPhase T r - 1‖ ≤ ‖modularPhase T r‖ + ‖(1 : ℂ)‖ :=
        norm_sub_le _ _
      _ = 2 := by rw [modularPhase_norm, norm_one]; norm_num
  have hd : ‖(r : ℂ) * Complex.I‖ = |r| := by simp
  calc
    ‖phaseAverage T r‖ = T⁻¹ * (‖modularPhase T r - 1‖ / |r|) := by
      rw [phaseAverage, integral_phase_nonzero T r hr, norm_smul,
        norm_div, hd, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hT)]
    _ ≤ T⁻¹ * (2 / |r|) :=
      mul_le_mul_of_nonneg_left
        (div_le_div_of_nonneg_right hn (abs_nonneg r)) (inv_nonneg.mpr hT.le)

/-- Cesaro cancellation at every nonzero real frequency. -/
theorem phase_average_nonzero_limit (r : ℝ) (hr : r ≠ 0) :
    Tendsto (fun n : ℕ => phaseAverage ((n : ℝ) + 1) r)
      atTop (𝓝 0) := by
  apply squeeze_zero_norm (fun n : ℕ => phase_average_norm_le ((n : ℝ) + 1) r
    (by positivity) hr)
  have hi : Tendsto (fun n : ℕ => ((n : ℝ) + 1)⁻¹) atTop (𝓝 0) := by
    simpa only [one_div] using
      (tendsto_one_div_add_atTop_nhds_zero_nat :
        Tendsto (fun n : ℕ => 1 / ((n : ℝ) + 1)) atTop (𝓝 0))
  simpa only [zero_mul] using hi.mul_const (2 / |r|)

/-- Resonant and nonresonant frequencies are handled without a common period. -/
theorem phase_average_limit (r : ℝ) :
    Tendsto (fun n : ℕ => phaseAverage ((n : ℝ) + 1) r)
      atTop (𝓝 (if r = 0 then 1 else 0)) := by
  by_cases hr : r = 0
  · rw [if_pos hr]
    subst r
    have he : (fun n : ℕ => phaseAverage ((n : ℝ) + 1) 0) =
        fun _ : ℕ => (1 : ℂ) := by
      funext n
      exact phase_average_zero _ (ne_of_gt (by positivity))
    rw [he]
    exact tendsto_const_nhds
  · rw [if_neg hr]
    exact phase_average_nonzero_limit r hr

/-- The finite matrix average of the actual local modular flow. -/
def flowAverage (P : SiteProfile) (T : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  T⁻¹ • (∫ t in (0 : ℝ)..T, flowLevel P t N a)

theorem flow_average_entry (P : SiteProfile) (T : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
    flowAverage P T N a i j =
      phaseAverage T (Real.log (towerW P N i) - Real.log (towerW P N j)) *
        a i j := by
  have hi := (matrixEntryCLM N i j).intervalIntegral_comp_comm (μ := volume)
    ((flowLevel_continuous (P := P) N a).intervalIntegrable 0 T)
  change (∫ t in (0 : ℝ)..T, flowLevel P t N a i j) =
    (∫ t in (0 : ℝ)..T, flowLevel P t N a) i j at hi
  change T⁻¹ • ((∫ t in (0 : ℝ)..T, flowLevel P t N a) i j) = _
  rw [← hi]
  simp only [flowLevel, intervalIntegral.integral_mul_const]
  rw [phaseAverage, smul_mul_assoc]

/-- The whole finite matrix converges to spectral pinching, including degenerate blocks. -/
theorem flow_average_limit (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Tendsto (fun n : ℕ => flowAverage P ((n : ℝ) + 1) N a)
      atTop (𝓝 (specExpect (towerW P N) a)) := by
  apply tendsto_pi_nhds.mpr
  intro i
  apply tendsto_pi_nhds.mpr
  intro j
  have he : Real.log (towerW P N i) - Real.log (towerW P N j) = 0 ↔
      towerW P N i = towerW P N j := by
    rw [sub_eq_zero]
    exact ⟨Real.log_injOn_pos (towerW_pos P N i) (towerW_pos P N j),
      congrArg Real.log⟩
  have h := (phase_average_limit
    (Real.log (towerW P N i) - Real.log (towerW P N j))).mul_const (a i j)
  by_cases hij : towerW P N i = towerW P N j
  · have hr := he.mpr hij
    rw [if_pos hr, one_mul] at h
    simpa only [flow_average_entry, specExpect, Matrix.of_apply, if_pos hij] using h
  · have hr : Real.log (towerW P N i) - Real.log (towerW P N j) ≠ 0 :=
      fun hzero => hij (he.mp hzero)
    rw [if_neg hr, zero_mul] at h
    simpa only [flow_average_entry, specExpect, Matrix.of_apply, if_neg hij] using h

/-- The finite matrix average is exactly the average of its existing GNS image. -/
theorem local_average_eq_embedding (P : SiteProfile) (T : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    T⁻¹ • (∫ t in (0 : ℝ)..T, modularFlow P t (levelEmbedding P N a)) =
      levelEmbeddingCLM P N (flowAverage P T N a) := by
  have h (t : ℝ) : modularFlow P t (levelEmbedding P N a) =
      levelEmbeddingCLM P N (flowLevel P t N a) := by
    change modularFlow P t ((tof P N a : TowerPre P) : TowerHilbert P) = _
    rw [modularFlow_coe, flowPre_tof]
    rfl
  simp_rw [h]
  rw [(levelEmbeddingCLM P N).intervalIntegral_comp_comm
    ((flowLevel_continuous (P := P) N a).intervalIntegrable 0 T),
    flowAverage, (levelEmbeddingCLM P N).map_smul_of_tower]

/-- Local GNS vectors have an aperiodic Cesaro limit; this is not an expectation on M. -/
theorem local_average_limit (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Tendsto
      (fun n : ℕ => ((n : ℝ) + 1)⁻¹ •
        (∫ t in (0 : ℝ)..((n : ℝ) + 1),
          modularFlow P t (levelEmbedding P N a)))
      atTop (𝓝 (levelEmbedding P N (specExpect (towerW P N) a))) := by
  have h := ((levelEmbeddingCLM P N).continuous.tendsto
    (specExpect (towerW P N) a)).comp (flow_average_limit P N a)
  simpa only [local_average_eq_embedding, Function.comp_def, levelEmbeddingCLM] using h

#print axioms phaseAverage
#print axioms phase_average_zero
#print axioms integral_phase_nonzero
#print axioms phase_average_norm_le
#print axioms phase_average_nonzero_limit
#print axioms phase_average_limit
#print axioms flowAverage
#print axioms flow_average_entry
#print axioms flow_average_limit
#print axioms local_average_eq_embedding
#print axioms local_average_limit

end

end ChatgptAudit.Aperiodic046
