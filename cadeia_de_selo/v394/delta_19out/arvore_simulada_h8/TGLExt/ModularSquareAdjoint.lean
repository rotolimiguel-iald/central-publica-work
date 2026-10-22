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
import TGLExt.ModularSquare

set_option autoImplicit false
set_option maxHeartbeats 400000

namespace ChatgptAudit
open TGLExt Filter Topology
noncomputable section
variable {P : SiteProfile}

theorem delta_preserves_level {N : ℕ} (x : modularSquareDomain P)
    (hx : (x : TowerHilbert P) ∈ levelSpace P N) :
    towerDeltaClosed P x ∈ levelSpace P N :=
  modulator_preserves_level (squareMid P x)
    (modulator_preserves_level (squareInput P x) hx)

def WeakDeltaPair (P : SiteProfile) (x y : TowerHilbert P) : Prop :=
  ∀ (N : ℕ) (b : levelSpace P N), inner ℂ (b : TowerHilbert P) y =
    inner ℂ (towerDeltaClosed P ⟨b, levelSpace_mem_squareDomain b.property⟩) x

theorem delta_weak_pair (x : modularSquareDomain P) :
    WeakDeltaPair P x (towerDeltaClosed P x) :=
  fun _ b => (delta_is_symmetric (P := P) ⟨b, levelSpace_mem_squareDomain b.property⟩ x).symm

theorem weak_delta_projects {x y : TowerHilbert P} (h : WeakDeltaPair P x y) (N : ℕ) :
    towerDeltaClosed P ⟨levelProject P N x,
      levelSpace_mem_squareDomain (levelProject_mem N x)⟩ = levelProject P N y := by
  let z : modularSquareDomain P :=
    ⟨levelProject P N x, levelSpace_mem_squareDomain (levelProject_mem N x)⟩
  have hz : towerDeltaClosed P z ∈ levelSpace P N :=
    delta_preserves_level z (levelProject_mem N x)
  let b : levelSpace P N := ⟨towerDeltaClosed P z - levelProject P N y,
    (levelSpace P N).sub_mem hz (levelProject_mem N y)⟩
  have hbD := delta_preserves_level
    (⟨b, levelSpace_mem_squareDomain b.property⟩ : modularSquareDomain P) b.property
  have hi : inner ℂ (b : TowerHilbert P) (towerDeltaClosed P z) =
      inner ℂ (b : TowerHilbert P) (levelProject P N y) := by
    calc
      _ = inner ℂ (towerDeltaClosed P ⟨b, levelSpace_mem_squareDomain b.property⟩)
          (levelProject P N x) :=
        (delta_is_symmetric (P := P) ⟨b, levelSpace_mem_squareDomain b.property⟩ z).symm
      _ = inner ℂ (towerDeltaClosed P ⟨b, levelSpace_mem_squareDomain b.property⟩) x :=
        levelProject_inner (P := P) (N := N) hbD x
      _ = inner ℂ (b : TowerHilbert P) y := (h N b).symm
      _ = _ := (levelProject_inner (P := P) (N := N) b.property y).symm
  apply sub_eq_zero.mp
  apply (inner_self_eq_zero (𝕜 := ℂ)).mp
  change inner ℂ (b : TowerHilbert P) (towerDeltaClosed P z - levelProject P N y) = 0
  rw [inner_sub_right, hi, sub_self]

/-- A estimativa de energia controla a primeira potência antes de afirmar domínio. -/
theorem weak_delta_energy_bound {x y : TowerHilbert P} (h : WeakDeltaPair P x y) (N : ℕ) :
    ‖closedModulatorCandidate P ⟨levelProject P N x,
      levelSpace_mem_domain (levelProject_mem N x)⟩‖ ≤ ‖x‖ + ‖y‖ + 1 := by
  let z : modularSquareDomain P :=
    ⟨levelProject P N x, levelSpace_mem_squareDomain (levelProject_mem N x)⟩
  have hi : ‖closedModulatorCandidate P (squareInput P z)‖ ^ 2 =
      (inner ℂ (levelProject P N x) (levelProject P N y)).re := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ), ← delta_quadratic]
    rw [show towerDeltaClosed P z = levelProject P N y from weak_delta_projects h N]
    rfl
  have hbound : (inner ℂ (levelProject P N x) (levelProject P N y)).re ≤ ‖x‖ * ‖y‖ :=
    (re_inner_le_norm (𝕜 := ℂ) _ _).trans
      (mul_le_mul ((levelSpace P N).norm_starProjection_apply_le x)
        ((levelSpace P N).norm_starProjection_apply_le y) (norm_nonneg _) (norm_nonneg _))
  have hn := norm_nonneg (closedModulatorCandidate P (squareInput P z))
  change ‖closedModulatorCandidate P (squareInput P z)‖ ≤ ‖x‖ + ‖y‖ + 1
  nlinarith [norm_nonneg x, norm_nonneg y, sq_nonneg (‖x‖ - ‖y‖)]

theorem weak_delta_functional_bound {x y : TowerHilbert P} (h : WeakDeltaPair P x y)
    (b : (closedModulatorCandidate P).domain) :
    ‖inner ℂ x (closedModulatorCandidate P b)‖ ≤ (‖x‖ + ‖y‖ + 1) * ‖(b : TowerHilbert P)‖ := by
  have ht := ((levelProject_tendsto x).inner (𝕜 := ℂ)
    (tendsto_const_nhds (x := closedModulatorCandidate P b))).norm
  apply le_of_tendsto ht
  filter_upwards with N
  rw [← modulator_is_symmetric
    (⟨levelProject P N x, levelSpace_mem_domain (levelProject_mem N x)⟩ :
      (closedModulatorCandidate P).domain) b]
  exact (norm_inner_le_norm (𝕜 := ℂ) _ _).trans
    (mul_le_mul_of_nonneg_right (weak_delta_energy_bound h N) (norm_nonneg _))

theorem weak_delta_first_domain {x y : TowerHilbert P} (h : WeakDeltaPair P x y) :
    x ∈ (closedModulatorCandidate P).domain := by
  have hx : x ∈ (LinearPMap.adjoint (closedModulatorCandidate P)).domain := by
    rw [LinearPMap.mem_adjoint_domain_iff]
    exact AddMonoidHomClass.continuous_of_bound
      ((innerₛₗ ℂ x).comp (closedModulatorCandidate P).toFun) (‖x‖ + ‖y‖ + 1)
      (weak_delta_functional_bound h)
  rwa [LinearPMap.isSelfAdjoint_def.mp (modulatorCandidate_selfadjoint (P := P))] at hx

/-- A segunda condição de domínio segue da caracterização fraca já provada de A. -/
theorem weak_delta_second_graph {x y : TowerHilbert P} (h : WeakDeltaPair P x y) :
    (closedModulatorCandidate P ⟨x, weak_delta_first_domain h⟩, y) ∈
      (closedModulatorCandidate P).graph := by
  apply weak_pair_mem_graph
  intro N b
  let bs : modularSquareDomain P := ⟨b, levelSpace_mem_squareDomain b.property⟩
  calc
    _ = inner ℂ (towerDeltaClosed P bs) x := h N b
    _ = inner ℂ (closedModulatorCandidate P (squareInput P bs))
        (closedModulatorCandidate P ⟨x, weak_delta_first_domain h⟩) :=
      modulator_is_symmetric (squareMid P bs) ⟨x, weak_delta_first_domain h⟩
    _ = _ := rfl

theorem weak_delta_mem_graph {x y : TowerHilbert P} (h : WeakDeltaPair P x y) :
    (x, y) ∈ (towerDeltaClosed P).graph := by
  have hg := weak_delta_second_graph h
  rw [LinearPMap.mem_graph_iff] at hg
  obtain ⟨z, hz, hy⟩ := hg
  dsimp only at hz hy
  have hx2 : x ∈ modularSquareDomain P :=
    (squareDomain_iff x).mpr ⟨weak_delta_first_domain h, hz ▸ z.property⟩
  rw [LinearPMap.mem_graph_iff]
  refine ⟨⟨x, hx2⟩, rfl, ?_⟩
  have hm : squareMid P ⟨x, hx2⟩ = z := Subtype.ext hz.symm
  change closedModulatorCandidate P (squareMid P ⟨x, hx2⟩) = y
  rw [hm]
  exact hy

theorem delta_adjoint_le : LinearPMap.adjoint (towerDeltaClosed P) ≤ towerDeltaClosed P := by
  apply LinearPMap.le_of_le_graph
  rintro ⟨p,q⟩ hp
  rw [LinearPMap.mem_graph_iff] at hp
  obtain ⟨x, hx, hy⟩ := hp
  dsimp only at hx hy
  rw [← hx, ← hy]
  apply weak_delta_mem_graph
  intro N b
  exact ((LinearPMap.adjoint_isFormalAdjoint (squareDomain_dense (P := P))).symm
    (⟨b, levelSpace_mem_squareDomain b.property⟩ : (towerDeltaClosed P).domain) x).symm

theorem delta_selfadjoint : IsSelfAdjoint (towerDeltaClosed P) := by
  rw [LinearPMap.isSelfAdjoint_def]
  exact le_antisymm delta_adjoint_le (delta_is_symmetric.le_adjoint squareDomain_dense)

theorem delta_closed : (towerDeltaClosed P).IsClosed := delta_selfadjoint.isClosed

#print axioms weak_delta_energy_bound
#print axioms weak_delta_first_domain
#print axioms delta_selfadjoint
#print axioms delta_closed
end
end ChatgptAudit
