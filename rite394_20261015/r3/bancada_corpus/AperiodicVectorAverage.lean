import AperiodicPhaseAverage
import BoundedOmegaLimit

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Aperiodic046

open TGLExt MeasureTheory Filter
open scoped Topology

noncomputable section

/-- A normalized interval average of the actual modular flow on Hilbert vectors. -/
def modularAverageVector (P : SiteProfile) (T : ℝ)
    (v : TowerHilbert P) : TowerHilbert P :=
  T⁻¹ • ∫ t in (0 : ℝ)..T, modularFlow P t v

theorem modular_average_vector_add (P : SiteProfile) (T : ℝ)
    (v w : TowerHilbert P) :
    modularAverageVector P T (v+w) =
      modularAverageVector P T v + modularAverageVector P T w := by
  simp only [modularAverageVector, modularFlow_add]
  rw [intervalIntegral.integral_add
    ((modularFlow_strongly_continuous v).intervalIntegrable 0 T)
    ((modularFlow_strongly_continuous w).intervalIntegrable 0 T), smul_add]

theorem modular_average_vector_smul (P : SiteProfile) (T : ℝ)
    (c : ℂ) (v : TowerHilbert P) :
    modularAverageVector P T (c • v) = c • modularAverageVector P T v := by
  simp only [modularAverageVector, modularFlow_smul, intervalIntegral.integral_smul]
  exact smul_comm _ _ _

/-- This vector estimate, rather than an estimate only on AΩ, permits dense approximation. -/
theorem modular_average_vector_bound (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (v : TowerHilbert P) :
    ‖modularAverageVector P T v‖ ≤ ‖v‖ := by
  have hb := intervalIntegral.norm_integral_le_of_norm_le_const
    (a := (0 : ℝ)) (b := T)
    (fun t _ => le_of_eq (modularFlow_norm (P := P) t v))
  simp only [sub_zero, abs_of_pos hT] at hb
  calc
    ‖modularAverageVector P T v‖ =
        T⁻¹ * ‖∫ t in (0 : ℝ)..T, modularFlow P t v‖ := by
      rw [modularAverageVector, norm_smul, Real.norm_eq_abs,
        abs_of_pos (inv_pos.mpr hT)]
    _ ≤ T⁻¹ * (‖v‖ * T) :=
      mul_le_mul_of_nonneg_left hb (le_of_lt (inv_pos.mpr hT))
    _ = ‖v‖ := by field_simp

/-- The vector average as a complex continuous linear contraction. -/
def modularVectorAverage (P : SiteProfile) (T : ℝ) (hT : 0 < T) :
    TowerHilbert P →L[ℂ] TowerHilbert P :=
  ({ toFun := modularAverageVector P T
     map_add' := modular_average_vector_add P T
     map_smul' := fun c v => modular_average_vector_smul P T c v } :
    TowerHilbert P →ₗ[ℂ] TowerHilbert P).mkContinuous 1
      (fun v => by
        change ‖modularAverageVector P T v‖ ≤ 1 * ‖v‖
        simpa only [one_mul] using modular_average_vector_bound P T hT v)

theorem modular_vector_average_apply (P : SiteProfile) (T : ℝ) (hT : 0 < T)
    (v : TowerHilbert P) :
    modularVectorAverage P T hT v =
      T⁻¹ • ∫ t in (0 : ℝ)..T, modularFlow P t v := rfl

theorem modular_vector_average_norm_le_one (P : SiteProfile) (T : ℝ) (hT : 0 < T) :
    ‖modularVectorAverage P T hT‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro v
  change ‖modularAverageVector P T v‖ ≤ 1 * ‖v‖
  simpa only [one_mul] using modular_average_vector_bound P T hT v

/-- Local convergence is spectral pinching, with no common phase period. -/
theorem modular_vector_average_local_limit (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Tendsto
      (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity)
        (levelEmbedding P N a))
      atTop (𝓝 (levelEmbedding P N (specExpect (towerW P N) a))) := by
  simpa only [modular_vector_average_apply] using local_average_limit P N a

/-- The uniform contraction bound extends Cauchy convergence from the dense pre-Hilbert space. -/
theorem modular_vector_average_cauchy (P : SiteProfile) (v : TowerHilbert P) :
    CauchySeq
      (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity) v) := by
  apply bounded_local_cauchy P
    (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity))
    1 (by norm_num)
    (fun n => modular_vector_average_norm_le_one P ((n : ℝ)+1) (by positivity))
    ?_ v
  intro w
  obtain ⟨N, a, rfl⟩ := exists_tof w
  change CauchySeq
    (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity)
      (levelEmbedding P N a))
  exact (modular_vector_average_local_limit P N a).cauchySeq

/-- The Hilbert limit is constructed by completeness for every vector. -/
theorem modular_vector_average_limit_exists (P : SiteProfile) (v : TowerHilbert P) :
    ∃ z : TowerHilbert P,
      Tendsto
        (fun n : ℕ => modularVectorAverage P ((n : ℝ)+1) (by positivity) v)
        atTop (𝓝 z) :=
  cauchySeq_tendsto_of_complete (modular_vector_average_cauchy P v)

/-- Conjugation averages on Ω are exactly the vector averages of AΩ. -/
theorem period_average_omega_eq_vector_average (P : SiteProfile) (T : ℝ)
    (hT : 0 < T) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    periodAverage P T hT A (hOmega P) =
      modularVectorAverage P T hT (A (hOmega P)) := by
  change T⁻¹ • (∫ t in (0 : ℝ)..T, modularConjugation P t A (hOmega P)) =
    T⁻¹ • (∫ t in (0 : ℝ)..T, modularFlow P t (A (hOmega P)))
  congr 1
  apply intervalIntegral.integral_congr
  intro t _
  change modularFlow P t (A (modularFlow P (-t) (hOmega P))) =
    modularFlow P t (A (hOmega P))
  rw [modularFlow_fixes_omega]

/-- Aperiodic convergence on Ω follows without assuming A belongs to the factor. -/
theorem aperiodic_average_omega_limit (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    ∃ z : TowerHilbert P,
      Tendsto
        (fun n : ℕ => periodAverage P ((n : ℝ)+1) (by positivity) A (hOmega P))
        atTop (𝓝 z) := by
  obtain ⟨z, hz⟩ := modular_vector_average_limit_exists P (A (hOmega P))
  refine ⟨z, ?_⟩
  simpa only [period_average_omega_eq_vector_average] using hz

/-- The limiting factor element and its strong convergence are conclusions.
No expectation, periodicity, or operator limit is supplied as a hypothesis. -/
theorem aperiodic_average_operator (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    ∃ B : TowerHilbert P →L[ℂ] TowerHilbert P,
      B ∈ theFactorObject P ∧ ‖B‖ ≤ ‖A‖ ∧
      ∀ v : TowerHilbert P,
        Tendsto
          (fun n : ℕ => periodAverage P ((n : ℝ)+1) (by positivity) A v)
          atTop (𝓝 (B v)) := by
  obtain ⟨z, hz⟩ := aperiodic_average_omega_limit P A
  obtain ⟨B, hB, hnorm, _, hlim⟩ := bounded_omega_limit_lift P
    (fun n : ℕ => periodAverage P ((n : ℝ)+1) (by positivity) A)
    ‖A‖ (norm_nonneg A)
    (fun n => period_average_mem_factor (P := P) ((n : ℝ)+1) (by positivity) A hA)
    (fun n => (period_average_operator (P := P) ((n : ℝ)+1) (by positivity) A).2)
    z hz
  exact ⟨B, hB, hnorm, hlim⟩

#print axioms modularAverageVector
#print axioms modular_average_vector_add
#print axioms modular_average_vector_smul
#print axioms modular_average_vector_bound
#print axioms modularVectorAverage
#print axioms modular_vector_average_apply
#print axioms modular_vector_average_norm_le_one
#print axioms modular_vector_average_local_limit
#print axioms modular_vector_average_cauchy
#print axioms modular_vector_average_limit_exists
#print axioms period_average_omega_eq_vector_average
#print axioms aperiodic_average_omega_limit
#print axioms aperiodic_average_operator

end
end ChatgptAudit.Aperiodic046
