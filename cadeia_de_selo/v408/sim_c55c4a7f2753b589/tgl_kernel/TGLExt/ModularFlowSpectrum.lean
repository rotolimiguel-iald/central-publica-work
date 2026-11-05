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
import TGLExt.ModularFlowAlgebra

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit
open TGLExt Matrix UniformSpace
noncomputable section
variable {P : SiteProfile}

def localEigenvalue (P : SiteProfile) (N : ℕ) (i j : chainIdx N) : ℝ :=
  towerW P N i / towerW P N j

theorem localEigenvalue_pos (N : ℕ) (i j : chainIdx N) : 0 < localEigenvalue P N i j :=
  div_pos (towerW_pos P N i) (towerW_pos P N j)

theorem deltaLevel_entry (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) (i j : chainIdx N) :
    towerDeltaLevel P N a i j = (localEigenvalue P N i j : ℂ) * a i j := by
  unfold towerDeltaLevel rhoMat rhoMatInv localEigenvalue
  simp only [diagonal_mul, mul_diagonal]
  push_cast
  ring

theorem deltaLevel_single (N : ℕ) (i j : chainIdx N) :
    towerDeltaLevel P N (Matrix.single i j 1) =
      (localEigenvalue P N i j : ℂ) • Matrix.single i j 1 := by
  ext k l
  rw [deltaLevel_entry]
  by_cases h : i = k ∧ j = l
  · obtain ⟨rfl,rfl⟩ := h
    simp
  · simp [h]

theorem flowLevel_single (t : ℝ) (N : ℕ) (i j : chainIdx N) :
    flowLevel P t N (Matrix.single i j 1) =
      modularPhase t (Real.log (localEigenvalue P N i j)) • Matrix.single i j 1 := by
  ext k l
  by_cases h : i = k ∧ j = l
  · obtain ⟨rfl,rfl⟩ := h
    simp [flowLevel, localEigenvalue, Real.log_div (ne_of_gt (towerW_pos P N i))
      (ne_of_gt (towerW_pos P N j))]
  · simp [flowLevel, h]

def localEigenvector (P : SiteProfile) (N : ℕ) (i j : chainIdx N) : TowerHilbert P :=
  ((tof P N (Matrix.single i j 1) : TowerPre P) : TowerHilbert P)

theorem localEigenvector_mem (N : ℕ) (i j : chainIdx N) :
    localEigenvector P N i j ∈ modularSquareDomain P :=
  levelSpace_mem_squareDomain (N := N) ⟨Matrix.single i j 1, rfl⟩

theorem delta_eigenvector (N : ℕ) (i j : chainIdx N) :
    towerDeltaClosed P ⟨localEigenvector P N i j, localEigenvector_mem N i j⟩ =
      (localEigenvalue P N i j : ℂ) • localEigenvector P N i j := by
  change towerDeltaClosed P ⟨((tof P N (Matrix.single i j 1) : TowerPre P) : TowerHilbert P),
    levelSpace_mem_squareDomain (N := N) ⟨Matrix.single i j 1, rfl⟩⟩ = _
  rw [square_local, deltaLevel_single, ← tof_smul, Completion.coe_smul]
  rfl

theorem modularFlow_eigenvector (t : ℝ) (N : ℕ) (i j : chainIdx N) :
    modularFlow P t (localEigenvector P N i j) =
      modularPhase t (Real.log (localEigenvalue P N i j)) • localEigenvector P N i j := by
  unfold localEigenvector
  rw [modularFlow_coe, flowPre_tof, flowLevel_single, ← tof_smul, Completion.coe_smul]

def localEigenvectors (P : SiteProfile) : Set (TowerHilbert P) :=
  {x | ∃ (N : ℕ) (i j : chainIdx N), x = localEigenvector P N i j}

theorem level_mem_eigenspan (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    levelEmbedding P N a ∈ Submodule.span ℂ (localEigenvectors P) := by
  rw [Matrix.matrix_eq_sum_single a]
  simp only [map_sum]
  apply Submodule.sum_mem
  intro i _
  apply Submodule.sum_mem
  intro j _
  have hs : Matrix.single i j (a i j) = (a i j) • Matrix.single i j (1 : ℂ) := by
    ext k l
    by_cases h : i = k ∧ j = l <;> simp [h]
  rw [hs, map_smul]
  apply Submodule.smul_mem
  exact Submodule.subset_span ⟨N,i,j,rfl⟩

theorem localEigenvectors_total :
    Dense (Submodule.span ℂ (localEigenvectors P) : Set (TowerHilbert P)) := by
  apply Dense.mono ?_ (towerPre_denseRange (P := P))
  rintro _ ⟨v,rfl⟩
  obtain ⟨N,a,rfl⟩ := exists_tof v
  exact level_mem_eigenspan N a

/-- Unicidade do multiplicador espectral limitado na família total de autovetores de Δ. -/
theorem modularFlow_spectral_unique (t : ℝ)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hT : ∀ (N : ℕ) (i j : chainIdx N), T (localEigenvector P N i j) =
      modularPhase t (Real.log (localEigenvalue P N i j)) • localEigenvector P N i j) :
    ∀ x : TowerHilbert P, T x = modularFlow P t x := by
  have hspan : ∀ x ∈ Submodule.span ℂ (localEigenvectors P), T x = modularFlow P t x := by
    intro x hx
    induction hx using Submodule.span_induction with
    | mem x hx =>
      obtain ⟨N,i,j,rfl⟩ := hx
      exact (hT N i j).trans (modularFlow_eigenvector t N i j).symm
    | zero =>
      rw [map_zero]
      exact (map_zero (modularFlowLinear P t)).symm
    | add x y hx hy hxe hye => rw [map_add, modularFlow_add, hxe, hye]
    | smul c x hx he => rw [map_smul, modularFlow_smul, he]
  have hclosed : IsClosed {x : TowerHilbert P | T x = modularFlow P t x} :=
    isClosed_eq T.continuous (modularFlow_continuous t)
  intro x
  exact closure_minimal hspan hclosed (localEigenvectors_total (P := P) x)

#print axioms delta_eigenvector
#print axioms modularFlow_eigenvector
#print axioms localEigenvectors_total
#print axioms modularFlow_spectral_unique
end
end ChatgptAudit
