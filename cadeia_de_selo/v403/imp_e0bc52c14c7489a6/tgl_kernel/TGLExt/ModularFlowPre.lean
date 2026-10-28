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
import TGLExt.ModularFlowLevel

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

def flowPre (P : SiteProfile) (t : ℝ) : TowerPre P → TowerPre P :=
  Quotient.map (fun x : TowerPt => (⟨x.1, flowLevel P t x.1 x.2⟩ : TowerPt)) (by
    rintro x y ⟨K, hx, hy, heq⟩
    refine ⟨K, hx, hy, ?_⟩
    show tPush hx (flowLevel P t x.1 x.2) = tPush hy (flowLevel P t y.1 y.2)
    rw [← flowLevel_push, ← flowLevel_push, heq])

theorem flowPre_tof (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowPre P t (tof P N a) = tof P N (flowLevel P t N a) := rfl

theorem flowPre_add (t : ℝ) (x y : TowerPre P) :
    flowPre P t (x+y) = flowPre P t x + flowPre P t y := by
  obtain ⟨N,a,rfl⟩ := exists_tof x
  obtain ⟨M,b,rfl⟩ := exists_tof y
  rw [tof_add_hetero, flowPre_tof, flowPre_tof, flowPre_tof, tof_add_hetero]
  congr 1
  rw [flowLevel_add, flowLevel_push, flowLevel_push]

theorem flowPre_smul (t : ℝ) (c : ℂ) (x : TowerPre P) :
    flowPre P t (c • x) = c • flowPre P t x := by
  obtain ⟨N,a,rfl⟩ := exists_tof x
  rw [tof_smul, flowPre_tof, flowPre_tof, tof_smul, flowLevel_smul]

theorem flowPre_zero (t : ℝ) : flowPre P t 0 = 0 := by
  have h := flowPre_smul (P := P) t 0 (0 : TowerPre P)
  simpa using h

theorem flowPre_norm (t : ℝ) (x : TowerPre P) : ‖flowPre P t x‖ = ‖x‖ := by
  obtain ⟨N,a,rfl⟩ := exists_tof x
  have hi : inner ℂ (flowPre P t (tof P N a)) (flowPre P t (tof P N a)) =
      inner ℂ (tof P N a) (tof P N a) := by
    rw [flowPre_tof, towerPre_inner_def, towerPre_inner_def,
      innerPre_tof_same, innerPre_tof_same, flowLevel_inner_self]
  have hs : ‖flowPre P t (tof P N a)‖ ^ 2 = ‖tof P N a‖ ^ 2 := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ), norm_sq_eq_re_inner (𝕜 := ℂ), hi]
  nlinarith [norm_nonneg (flowPre P t (tof P N a)), norm_nonneg (tof P N a)]

def flowPreLinear (P : SiteProfile) (t : ℝ) : TowerPre P →ₗ[ℂ] TowerPre P where
  toFun := flowPre P t
  map_add' := flowPre_add t
  map_smul' := by intro c x; exact flowPre_smul t c x

theorem flowPre_isometry (t : ℝ) : Isometry (flowPre P t) := by
  apply Isometry.of_dist_eq
  intro x y
  rw [dist_eq_norm, dist_eq_norm]
  have h := (flowPreLinear P t).map_sub x y
  change flowPre P t (x-y) = flowPre P t x - flowPre P t y at h
  rw [← h, flowPre_norm]

theorem flowPre_group (s t : ℝ) (x : TowerPre P) :
    flowPre P s (flowPre P t x) = flowPre P (s+t) x := by
  obtain ⟨N,a,rfl⟩ := exists_tof x
  rw [flowPre_tof, flowPre_tof, flowPre_tof, flowLevel_group]

theorem flowPre_zero_time (x : TowerPre P) : flowPre P 0 x = x := by
  obtain ⟨N,a,rfl⟩ := exists_tof x
  rw [flowPre_tof, flowLevel_zero_time]

#print axioms flowPre
#print axioms flowPre_isometry
#print axioms flowPre_group
end
end ChatgptAudit
