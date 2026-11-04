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
import TGLExt.ModularFlowPre

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit
open TGLExt UniformSpace
noncomputable section
variable {P : SiteProfile}

def modularFlow (P : SiteProfile) (t : ℝ) : TowerHilbert P → TowerHilbert P :=
  Completion.map (flowPre P t)

theorem modularFlow_continuous (t : ℝ) : Continuous (modularFlow P t) :=
  Completion.continuous_map

theorem modularFlow_coe (t : ℝ) (x : TowerPre P) :
    modularFlow P t (x : TowerHilbert P) = ((flowPre P t x : TowerPre P) : TowerHilbert P) :=
  Completion.map_coe (flowPre_isometry t).uniformContinuous x

theorem modularFlow_group (s t : ℝ) (x : TowerHilbert P) :
    modularFlow P s (modularFlow P t x) = modularFlow P (s+t) x := by
  refine Completion.induction_on x (isClosed_eq
    ((modularFlow_continuous s).comp (modularFlow_continuous t))
    (modularFlow_continuous (s+t))) ?_
  intro a
  rw [modularFlow_coe, modularFlow_coe, flowPre_group, modularFlow_coe]

theorem modularFlow_zero_time (x : TowerHilbert P) : modularFlow P 0 x = x := by
  refine Completion.induction_on x (isClosed_eq (modularFlow_continuous 0) continuous_id) ?_
  intro a
  rw [modularFlow_coe, flowPre_zero_time]

theorem modularFlow_norm (t : ℝ) (x : TowerHilbert P) : ‖modularFlow P t x‖ = ‖x‖ := by
  refine Completion.induction_on x (isClosed_eq
    (continuous_norm.comp (modularFlow_continuous t)) continuous_norm) ?_
  intro a
  rw [modularFlow_coe, Completion.norm_coe, Completion.norm_coe, flowPre_norm]

theorem modularFlow_add (t : ℝ) (x y : TowerHilbert P) :
    modularFlow P t (x+y) = modularFlow P t x + modularFlow P t y := by
  refine Completion.induction_on₂ x y (isClosed_eq
    ((modularFlow_continuous t).comp (continuous_fst.add continuous_snd))
    (((modularFlow_continuous t).comp continuous_fst).add
      ((modularFlow_continuous t).comp continuous_snd))) ?_
  intro a b
  rw [← Completion.coe_add, modularFlow_coe, flowPre_add,
    Completion.coe_add, modularFlow_coe, modularFlow_coe]

theorem modularFlow_smul (t : ℝ) (c : ℂ) (x : TowerHilbert P) :
    modularFlow P t (c • x) = c • modularFlow P t x := by
  refine Completion.induction_on x (isClosed_eq
    ((modularFlow_continuous t).comp (continuous_const.smul continuous_id))
    (continuous_const.smul (modularFlow_continuous t))) ?_
  intro a
  rw [← Completion.coe_smul, modularFlow_coe, flowPre_smul,
    Completion.coe_smul, modularFlow_coe]

def modularFlowLinear (P : SiteProfile) (t : ℝ) : TowerHilbert P →ₗ[ℂ] TowerHilbert P where
  toFun := modularFlow P t
  map_add' := modularFlow_add t
  map_smul' := by intro c x; exact modularFlow_smul t c x

def modularFlowIsometry (P : SiteProfile) (t : ℝ) : TowerHilbert P →ₗᵢ[ℂ] TowerHilbert P where
  toLinearMap := modularFlowLinear P t
  norm_map' := modularFlow_norm t

theorem modularFlow_inverse (t : ℝ) (x : TowerHilbert P) :
    modularFlow P (-t) (modularFlow P t x) = x := by
  rw [modularFlow_group, neg_add_cancel, modularFlow_zero_time]

def modularFlowUnitary (P : SiteProfile) (t : ℝ) : TowerHilbert P ≃ₗᵢ[ℂ] TowerHilbert P :=
  { modularFlowIsometry P t with
    invFun := modularFlow P (-t)
    left_inv := modularFlow_inverse t
    right_inv := by
      intro x
      change modularFlow P t (modularFlow P (-t) x) = x
      rw [modularFlow_group, add_neg_cancel, modularFlow_zero_time] }

theorem modularFlow_local_continuous (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Continuous (fun t : ℝ => modularFlow P t ((tof P N a : TowerPre P) : TowerHilbert P)) := by
  have h := (levelEmbedding P N).continuous_of_finiteDimensional.comp
    (flowLevel_continuous (P := P) N a)
  simp only [modularFlow_coe, flowPre_tof]
  exact h

/-- Continuidade forte por aproximação local uniforme em t, usando norma unitária. -/
theorem modularFlow_strongly_continuous (x : TowerHilbert P) :
    Continuous (fun t : ℝ => modularFlow P t x) := by
  apply continuous_iff_continuousAt.mpr
  intro s
  rw [Metric.continuousAt_iff]
  intro ε hε
  obtain ⟨v,hv⟩ := Metric.denseRange_iff.mp (towerPre_denseRange (P := P)) x
    (ε/3) (by positivity)
  obtain ⟨N,a,rfl⟩ := exists_tof v
  let z : TowerHilbert P := ((tof P N a : TowerPre P) : TowerHilbert P)
  have hc : ContinuousAt (fun t : ℝ => modularFlow P t z) s :=
    (modularFlow_local_continuous (P := P) N a).continuousAt
  obtain ⟨δ,hδ,hlocal⟩ := Metric.continuousAt_iff.mp hc (ε/3) (by positivity)
  refine ⟨δ,hδ,fun t ht => ?_⟩
  have hd1 : dist (modularFlow P t x) (modularFlow P t z) = dist x z :=
    (modularFlowIsometry P t).isometry.dist_eq x z
  have hd2 : dist (modularFlow P s z) (modularFlow P s x) = dist x z := by
    exact ((modularFlowIsometry P s).isometry.dist_eq z x).trans (dist_comm z x)
  have htriangle := dist_triangle (modularFlow P t x) (modularFlow P t z) (modularFlow P s x)
  have htriangle2 := dist_triangle (modularFlow P t z) (modularFlow P s z) (modularFlow P s x)
  have hloc : dist (modularFlow P t z) (modularFlow P s z) < ε/3 := hlocal ht
  rw [hd1] at htriangle
  rw [hd2] at htriangle2
  have hv' : dist x z < ε/3 := hv
  linarith

#print axioms modularFlow_group
#print axioms modularFlowUnitary
#print axioms modularFlow_strongly_continuous
end
end ChatgptAudit
