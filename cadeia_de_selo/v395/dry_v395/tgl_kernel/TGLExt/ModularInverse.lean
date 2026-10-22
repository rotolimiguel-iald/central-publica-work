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
import TGLExt.TomitaAdjoint

set_option autoImplicit false
set_option maxHeartbeats 500000

namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

/-- A relação JAJ=A⁻¹ é expressa no gráfico, sem estender o domínio por decreto. -/
theorem modulator_reciprocal (x : closedTomitaDomain P) :
    ∃ hy : towerJ P (closedModulatorCandidate P x) ∈ closedTomitaDomain P,
      closedModulatorCandidate P ⟨towerJ P (closedModulatorCandidate P x), hy⟩ =
        towerJ P (x : TowerHilbert P) := by
  have hy : towerJ P (closedModulatorCandidate P x) ∈ closedTomitaDomain P := by
    rw [candidate_factorization]
    exact closedTomita_maps_domain x
  refine ⟨hy, ?_⟩
  have hz : (⟨towerJ P (closedModulatorCandidate P x), hy⟩ : closedTomitaDomain P) =
      ⟨closedTomita P x, closedTomita_maps_domain x⟩ := Subtype.ext (candidate_factorization x)
  calc
    _ = closedModulatorCandidate P ⟨closedTomita P x, closedTomita_maps_domain x⟩ :=
      congrArg (fun z : closedTomitaDomain P => closedModulatorCandidate P z) hz
    _ = _ := by
      change towerJ P (closedTomita P ⟨closedTomita P x, closedTomita_maps_domain x⟩) = _
      rw [closedTomita_involutive]

theorem delta_reciprocal (x : modularSquareDomain P) :
    ∃ hy : towerJ P (towerDeltaClosed P x) ∈ modularSquareDomain P,
      towerDeltaClosed P ⟨towerJ P (towerDeltaClosed P x), hy⟩ =
        towerJ P (x : TowerHilbert P) := by
  obtain ⟨h1, e1⟩ := modulator_reciprocal (squareInput P x)
  obtain ⟨h2, e2⟩ := modulator_reciprocal (squareMid P x)
  have hy : towerJ P (towerDeltaClosed P x) ∈ modularSquareDomain P := by
    apply (squareDomain_iff _).mpr
    refine ⟨h2, ?_⟩
    exact e2.symm ▸ h1
  refine ⟨hy, ?_⟩
  have hm : squareMid P ⟨towerJ P (towerDeltaClosed P x), hy⟩ =
      ⟨towerJ P (closedModulatorCandidate P (squareInput P x)), h1⟩ := Subtype.ext e2
  change closedModulatorCandidate P (squareMid P ⟨towerJ P (towerDeltaClosed P x), hy⟩) = _
  rw [hm]
  exact e1

/-- Forma completa de JΔJ=Δ⁻¹, como equivalência de gráficos. -/
theorem delta_graph_J_swap (x y : TowerHilbert P) :
    (x, y) ∈ (towerDeltaClosed P).graph ↔
      (towerJ P y, towerJ P x) ∈ (towerDeltaClosed P).graph := by
  have forward (a b : TowerHilbert P) (h : (a,b) ∈ (towerDeltaClosed P).graph) :
      (towerJ P b, towerJ P a) ∈ (towerDeltaClosed P).graph := by
    rw [LinearPMap.mem_graph_iff] at h ⊢
    obtain ⟨z, hz, heq⟩ := h
    dsimp only at hz heq
    obtain ⟨hy, ey⟩ := delta_reciprocal z
    rw [← hz, ← heq]
    exact ⟨⟨towerJ P (towerDeltaClosed P z), hy⟩, rfl, ey⟩
  constructor
  · exact forward x y
  · intro h
    simpa only [towerJ_involutive] using forward (towerJ P y) (towerJ P x) h

theorem delta_injective :
    Function.Injective (fun x : modularSquareDomain P => towerDeltaClosed P x) := by
  intro x y h
  have hm : squareMid P x = squareMid P y := modulatorCandidate_injective h
  have hfirst : squareInput P x = squareInput P y :=
    modulatorCandidate_injective (congrArg Subtype.val hm)
  apply Subtype.ext
  exact congrArg (fun z : (closedModulatorCandidate P).domain => (z : TowerHilbert P)) hfirst

theorem delta_positive_selfadjoint (P : SiteProfile) :
    IsSelfAdjoint (towerDeltaClosed P) ∧
      ∀ x : modularSquareDomain P,
        0 ≤ (inner ℂ (x : TowerHilbert P) (towerDeltaClosed P x)).re :=
  ⟨delta_selfadjoint, delta_positive⟩

#print axioms delta_reciprocal
#print axioms delta_graph_J_swap
#print axioms delta_injective
#print axioms delta_positive_selfadjoint
end
end ChatgptAudit
