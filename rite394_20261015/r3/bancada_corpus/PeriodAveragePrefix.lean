import PeriodAverageOperator
import StationaryModularPeriod
import LocalCentralizerExpectation
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit
open TGLExt Matrix MeasureTheory
noncomputable section
variable {P : SiteProfile}

def LocalPhasePeriod (P : SiteProfile) (T : ℝ) : Prop :=
  ∀ N (i j : chainIdx N),
    modularPhase T (Real.log (towerW P N i)-Real.log (towerW P N j)) = 1

theorem lattice_local_phase_period {r : ℝ} (hr : r ≠ 0) (h : SiteLogLattice P r) :
    LocalPhasePeriod P (2*Real.pi/|r|) := by
  intro N i j
  obtain ⟨k,hk⟩ := tower_log_lattice h N i j
  rw [hk,modularPhase_lattice_period hr]

theorem integral_modularPhase (T r : ℝ) (hp : modularPhase T r = 1) :
    (∫ t in (0:ℝ)..T, modularPhase t r) = if r=0 then (T:ℂ) else 0 := by
  by_cases hr : r=0
  · subst r
    simp [modularPhase]
  · rw [if_neg hr]
    have hc : (r:ℂ)*Complex.I ≠ 0 := mul_ne_zero (by exact_mod_cast hr) Complex.I_ne_zero
    have he (t : ℝ) : modularPhase t r = Complex.exp (((r:ℂ)*Complex.I)*t) := by
      unfold modularPhase
      congr 1
      push_cast
      ring
    simp_rw [he]
    rw [integral_exp_mul_complex hc,← he T]
    simp [hp]

def matrixEntryCLM (N : ℕ) (i j : chainIdx N) :
    Matrix (chainIdx N) (chainIdx N) ℂ →L[ℂ] ℂ :=
  (ContinuousLinearMap.proj j : (chainIdx N → ℂ) →L[ℂ] ℂ).comp
    (ContinuousLinearMap.proj i : (chainIdx N → chainIdx N → ℂ) →L[ℂ] (chainIdx N → ℂ))

theorem integral_flowLevel (T : ℝ) (hp : LocalPhasePeriod P T) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (∫ t in (0:ℝ)..T, flowLevel P t N a) = T • specExpect (towerW P N) a := by
  ext i j
  have hi := (matrixEntryCLM N i j).intervalIntegral_comp_comm (μ := volume)
    ((flowLevel_continuous (P := P) N a).intervalIntegrable 0 T)
  change (∫ t in (0:ℝ)..T, flowLevel P t N a i j) =
    (∫ t in (0:ℝ)..T, flowLevel P t N a) i j at hi
  rw [← hi]
  simp only [flowLevel,intervalIntegral.integral_mul_const,integral_modularPhase T _ (hp N i j)]
  have he : Real.log (towerW P N i)-Real.log (towerW P N j)=0 ↔ towerW P N i=towerW P N j := by
    rw [sub_eq_zero]
    exact ⟨Real.log_injOn_pos (towerW_pos P N i) (towerW_pos P N j),congrArg Real.log⟩
  by_cases hij : towerW P N i=towerW P N j
  · simp [hij,specExpect]
  · simp [he,hij,specExpect]

def levelEmbeddingCLM (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ →L[ℂ] TowerHilbert P :=
  { toLinearMap := levelEmbedding P N
    cont := (levelEmbedding P N).continuous_of_finiteDimensional }

theorem integral_modularFlow_local (T : ℝ) (hp : LocalPhasePeriod P T) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    (∫ t in (0:ℝ)..T, modularFlow P t (levelEmbedding P N a)) =
      T • levelEmbedding P N (specExpect (towerW P N) a) := by
  have h (t : ℝ) : modularFlow P t (levelEmbedding P N a) =
      levelEmbeddingCLM P N (flowLevel P t N a) := by
    change modularFlow P t ((tof P N a : TowerPre P) : TowerHilbert P) = _
    rw [modularFlow_coe,flowPre_tof]
    rfl
  simp_rw [h]
  rw [(levelEmbeddingCLM P N).intervalIntegral_comp_comm
    ((flowLevel_continuous (P := P) N a).intervalIntegrable 0 T),integral_flowLevel T hp,
    (levelEmbeddingCLM P N).map_smul_of_tower]
  rfl

theorem period_average_prefix (T : ℝ) (hT : 0<T) (hp : LocalPhasePeriod P T)
    (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P) :
    towerExpectation P N (periodAverage P T hT x) =
      towerPi P (specExpect (towerW P N) (expectationMatrix P N x)) := by
  apply factor_eq_of_omega (expectation_mem_factor _ _) (towerPi_mem_factor _)
  rw [expectation_omega,towerPi_omega,(period_average_operator T hT x).1]
  have ho (t : ℝ) : modularConjugation P t x (hOmega P) = modularFlow P t (x (hOmega P)) := by
    change modularFlow P t (x (modularFlow P (-t) (hOmega P))) = _
    rw [modularFlow_fixes_omega]
  simp_rw [ho]
  rw [(levelProject P N).map_smul_of_tower,← (levelProject P N).intervalIntegral_comp_comm
    ((modularFlow_strongly_continuous (x (hOmega P))).intervalIntegrable 0 T)]
  simp_rw [project_flow_commutes,← expectation_omega]
  change T⁻¹ • (∫ t in (0:ℝ)..T,
    modularFlow P t (towerPi P (expectationMatrix P N x) (hOmega P))) = _
  simp_rw [towerPi_omega]
  change T⁻¹ • (∫ t in (0:ℝ)..T,
    modularFlow P t (levelEmbedding P N (expectationMatrix P N x))) =
    levelEmbedding P N (specExpect (towerW P N) (expectationMatrix P N x))
  rw [integral_modularFlow_local T hp,smul_smul,inv_mul_cancel₀ (ne_of_gt hT),one_smul]

#print axioms lattice_local_phase_period
#print axioms integral_modularPhase
#print axioms integral_flowLevel
#print axioms integral_modularFlow_local
#print axioms period_average_prefix
end
end ChatgptAudit
