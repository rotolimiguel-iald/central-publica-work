-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT (05/09/2026) — transposta em 05/09/2026
-- Procedencia: C:\IALD\Central de Patentes\Chatgpt (bancada da outra sessao,
--   sob direcao do operador; TUNEL\TUNEL_PROTOCOLO.md).
-- Auditoria da gerencia (sessao Claude d554e796, 05/09/2026): recompilacao
--   independente 20/20 exit 0; sonda #print axioms dos teoremas de manchete =
--   [propext, Classical.choice, Quot.sound]; zero sorry; enunciados conferidos.
-- Transposicao MECANICA: apenas (a) este cabecalho, (b) "import TGLExt" (root)
--   expandido no bloco de imports da epoca, (c) imports internos da bancada
--   prefixados com TGLExt. — nada mais foi alterado. Namespace ChatgptAudit
--   PRESERVADO como marca de procedencia.
-- Estatuto: [REAL — Lean] analise modular da torre produto (S, J·S, Delta,
--   Delta^{it}, invariancia do bicomutante). NAO move gate; NAO e fisica;
--   NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.ModulatorSelfAdjoint

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit
open TGLExt Matrix Filter Topology
open scoped ComplexConjugate
noncomputable section
variable {P : SiteProfile}

theorem half_level_entry (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (i j : chainIdx N) :
    towerDeltaHalfLevel P N a i j =
      ((Real.sqrt (towerW P N i) / Real.sqrt (towerW P N j) : ℝ) : ℂ) * a i j := by
  unfold towerDeltaHalfLevel profileRoot profileRootInv
  simp only [diagonal_mul, mul_diagonal]
  push_cast
  ring

theorem half_level_quadratic (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N a (towerDeltaHalfLevel P N a) =
      ((∑ k, towerW P N k * ∑ j,
        (Real.sqrt (towerW P N j) / Real.sqrt (towerW P N k)) *
          Complex.normSq (a j k) : ℝ) : ℂ) := by
  rw [tInner_apply]
  push_cast
  apply Finset.sum_congr rfl
  intro k _
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  rw [half_level_entry]
  push_cast
  rw [Complex.normSq_eq_conj_mul_self]
  ring

theorem half_level_positive (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    0 ≤ (tInner P N a (towerDeltaHalfLevel P N a)).re := by
  rw [half_level_quadratic, Complex.ofReal_re]
  apply Finset.sum_nonneg
  intro k _
  apply mul_nonneg (le_of_lt (towerW_pos P N k))
  apply Finset.sum_nonneg
  intro j _
  exact mul_nonneg (div_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))
    (Complex.normSq_nonneg _)

theorem modulator_local_positive (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    0 ≤ (inner ℂ ((tof P N a : TowerPre P) : TowerHilbert P)
      (closedModulatorCandidate P ⟨((tof P N a : TowerPre P) : TowerHilbert P),
        local_vector_mem_domain a⟩)).re := by
  rw [modulatorCandidate_local, UniformSpace.Completion.inner_coe,
    towerPre_inner_def, innerPre_tof_same]
  exact half_level_positive N a

theorem modulator_level_positive {N : ℕ} (x : closedTomitaDomain P)
    (hx : (x : TowerHilbert P) ∈ levelSpace P N) :
    0 ≤ (inner ℂ (x : TowerHilbert P) (closedModulatorCandidate P x)).re := by
  obtain ⟨a, ha⟩ := hx
  have heq : x = ⟨((tof P N a : TowerPre P) : TowerHilbert P),
      local_vector_mem_domain a⟩ := Subtype.ext ha.symm
  rw [heq]
  exact modulator_local_positive N a

/-- Positividade no domínio completo, passada pelo limite em norma de gráfico. -/
theorem modulatorCandidate_positive (x : closedTomitaDomain P) :
    0 ≤ (inner ℂ (x : TowerHilbert P) (closedModulatorCandidate P x)).re := by
  have hi := (levelProject_tendsto (x : TowerHilbert P)).inner
    (𝕜 := ℂ) (levelProject_tendsto (closedModulatorCandidate P x))
  apply ge_of_tendsto (Complex.continuous_re.tendsto _ |>.comp hi)
  filter_upwards with N
  dsimp only [Function.comp_apply]
  rw [← modulator_projection_commutes x N]
  exact modulator_level_positive
    ⟨levelProject P N (x : TowerHilbert P),
      levelSpace_mem_domain (levelProject_mem N (x : TowerHilbert P))⟩
    (levelProject_mem N (x : TowerHilbert P))

theorem JS_positive_selfadjoint (P : SiteProfile) :
    IsSelfAdjoint (closedModulatorCandidate P) ∧
      ∀ x : closedTomitaDomain P,
        0 ≤ (inner ℂ (x : TowerHilbert P) (closedModulatorCandidate P x)).re :=
  ⟨modulatorCandidate_selfadjoint, modulatorCandidate_positive⟩

#print axioms half_level_positive
#print axioms modulatorCandidate_positive
#print axioms JS_positive_selfadjoint
end
end ChatgptAudit
