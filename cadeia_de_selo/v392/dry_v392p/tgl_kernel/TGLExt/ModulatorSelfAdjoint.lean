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
import TGLExt.LocalTowerProjections

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit
open TGLExt Filter Topology
noncomputable section
variable {P : SiteProfile}

/-- A condição fraca usa apenas os andares, mas testa x e y em todo H. -/
def WeakModulatorPair (P : SiteProfile) (x y : TowerHilbert P) : Prop :=
  ∀ (N : ℕ) (b : levelSpace P N),
    inner ℂ (b : TowerHilbert P) y =
      inner ℂ (closedModulatorCandidate P ⟨b, levelSpace_mem_domain b.property⟩) x

theorem modulator_weak_pair (x : closedTomitaDomain P) :
    WeakModulatorPair P x (closedModulatorCandidate P x) :=
  fun _ b => modulator_pairing_level x b

theorem weak_pair_projects {x y : TowerHilbert P} (h : WeakModulatorPair P x y) (N : ℕ) :
    closedModulatorCandidate P ⟨levelProject P N x,
      levelSpace_mem_domain (levelProject_mem N x)⟩ = levelProject P N y := by
  let z : closedTomitaDomain P :=
    ⟨levelProject P N x, levelSpace_mem_domain (levelProject_mem N x)⟩
  have hz : closedModulatorCandidate P z ∈ levelSpace P N :=
    modulator_preserves_level z (levelProject_mem N x)
  let b : levelSpace P N :=
    ⟨closedModulatorCandidate P z - levelProject P N y,
      (levelSpace P N).sub_mem hz (levelProject_mem N y)⟩
  have hbA := modulator_preserves_level
    (⟨b, levelSpace_mem_domain b.property⟩ : closedTomitaDomain P) b.property
  have hi : inner ℂ (b : TowerHilbert P) (closedModulatorCandidate P z) =
      inner ℂ (b : TowerHilbert P) (levelProject P N y) := by
    calc
      _ = inner ℂ (closedModulatorCandidate P ⟨b, levelSpace_mem_domain b.property⟩)
          (levelProject P N x) := modulator_pairing_level z b
      _ = inner ℂ (closedModulatorCandidate P ⟨b, levelSpace_mem_domain b.property⟩) x :=
        levelProject_inner hbA x
      _ = inner ℂ (b : TowerHilbert P) y := (h N b).symm
      _ = _ := (levelProject_inner b.property y).symm
  apply sub_eq_zero.mp
  apply (inner_self_eq_zero (𝕜 := ℂ)).mp
  change inner ℂ (b : TowerHilbert P)
    (closedModulatorCandidate P z - levelProject P N y) = 0
  rw [inner_sub_right, hi, sub_self]

theorem weak_pair_mem_graph {x y : TowerHilbert P} (h : WeakModulatorPair P x y) :
    (x, y) ∈ (closedModulatorCandidate P).graph := by
  apply (modulatorCandidate_is_closed (P := P)).mem_of_tendsto
    ((levelProject_tendsto x).prodMk_nhds (levelProject_tendsto y))
  filter_upwards with N
  change (levelProject P N x, levelProject P N y) ∈ (closedModulatorCandidate P).graph
  rw [LinearPMap.mem_graph_iff]
  exact ⟨⟨levelProject P N x, levelSpace_mem_domain (levelProject_mem N x)⟩,
    rfl, weak_pair_projects h N⟩

theorem modulator_graph_iff_weak (x y : TowerHilbert P) :
    (x, y) ∈ (closedModulatorCandidate P).graph ↔ WeakModulatorPair P x y := by
  constructor
  · intro h
    rw [LinearPMap.mem_graph_iff] at h
    obtain ⟨z, hx, hy⟩ := h
    dsimp only at hx hy
    rw [← hx, ← hy]
    exact modulator_weak_pair z
  · exact weak_pair_mem_graph

theorem modulator_projection_commutes (x : closedTomitaDomain P) (N : ℕ) :
    closedModulatorCandidate P ⟨levelProject P N x,
      levelSpace_mem_domain (levelProject_mem N (x : TowerHilbert P))⟩ =
        levelProject P N (closedModulatorCandidate P x) :=
  weak_pair_projects (modulator_weak_pair x) N

theorem modulator_is_symmetric :
    (closedModulatorCandidate P).IsFormalAdjoint (closedModulatorCandidate P) := by
  intro x y
  have heq (N : ℕ) :
      inner ℂ (levelProject P N (closedModulatorCandidate P x)) (y : TowerHilbert P) =
        inner ℂ (levelProject P N (x : TowerHilbert P)) (closedModulatorCandidate P y) := by
    rw [← modulator_projection_commutes x N]
    exact (modulator_pairing_level y
      ⟨levelProject P N (x : TowerHilbert P), levelProject_mem N (x : TowerHilbert P)⟩).symm
  have hleft := (levelProject_tendsto (closedModulatorCandidate P x)).inner
    (𝕜 := ℂ) (tendsto_const_nhds (x := (y : TowerHilbert P)))
  have hright := (levelProject_tendsto (x : TowerHilbert P)).inner
    (𝕜 := ℂ) (tendsto_const_nhds (x := closedModulatorCandidate P y))
  exact tendsto_nhds_unique hleft (hright.congr (fun N => (heq N).symm))

/-- O adjunto inteiro satisfaz os testes locais e, portanto, pertence ao gráfico de JS. -/
theorem modulator_adjoint_le :
    LinearPMap.adjoint (closedModulatorCandidate P) ≤ closedModulatorCandidate P := by
  apply LinearPMap.le_of_le_graph
  intro p hp
  rcases p with ⟨p, q⟩
  rw [LinearPMap.mem_graph_iff] at hp
  obtain ⟨x, hx, hy⟩ := hp
  dsimp only at hx hy
  rw [← hx, ← hy]
  apply weak_pair_mem_graph
  intro N b
  exact ((LinearPMap.adjoint_isFormalAdjoint
    (modulatorCandidate_domain_dense (P := P))).symm
      (⟨b, levelSpace_mem_domain b.property⟩ : (closedModulatorCandidate P).domain) x).symm

/-- JS da torre é auto-adjunto, sem hipótese de auto-adjunticidade ou base importada. -/
theorem modulatorCandidate_selfadjoint : IsSelfAdjoint (closedModulatorCandidate P) := by
  rw [LinearPMap.isSelfAdjoint_def]
  exact le_antisymm modulator_adjoint_le
    (modulator_is_symmetric.le_adjoint modulatorCandidate_domain_dense)

#print axioms weak_pair_mem_graph
#print axioms modulator_is_symmetric
#print axioms modulatorCandidate_selfadjoint
end
end ChatgptAudit
