-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_007 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ModularFlowAlgebra
import Mathlib.Analysis.SpecialFunctions.Complex.Log

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit
open TGLExt Matrix UniformSpace
noncomputable section
variable {P : SiteProfile}

def SiteLogLattice (P : SiteProfile) (r : ℝ) : Prop :=
  ∀ n (i j : Fin 2), ∃ k : ℤ,
    Real.log (siteW (P.w n) i) - Real.log (siteW (P.w n) j) = k * r

theorem tower_log_lattice {r : ℝ} (h : SiteLogLattice P r) (N : ℕ)
    (i j : chainIdx N) : ∃ k : ℤ,
    Real.log (towerW P N i) - Real.log (towerW P N j) = k * r := by
  induction N with
  | zero => exact h 0 i j
  | succ n ih =>
    rcases i with ⟨i,u⟩
    rcases j with ⟨j,v⟩
    obtain ⟨k,hk⟩ := ih i j
    obtain ⟨l,hl⟩ := h (n+1) u v
    refine ⟨k+l,?_⟩
    simp only [towerW,Real.log_mul (ne_of_gt (towerW_pos P n i))
      (ne_of_gt (siteW_pos (P.pos _) (P.lt_one _) u)),
      Real.log_mul (ne_of_gt (towerW_pos P n j))
      (ne_of_gt (siteW_pos (P.pos _) (P.lt_one _) v)),Int.cast_add]
    linarith

theorem modularPhase_lattice_period {r : ℝ} (hr : r ≠ 0) (k : ℤ) :
    modularPhase (2*Real.pi/|r|) (k*r) = 1 := by
  unfold modularPhase
  have hrC : (r : ℂ) ≠ 0 := by exact_mod_cast hr
  apply Complex.exp_eq_one_iff.mpr
  rcases lt_or_gt_of_ne hr with hn | hp
  · refine ⟨-k,?_⟩
    rw [abs_of_neg hn]
    push_cast
    field_simp [hrC]
  · refine ⟨k,?_⟩
    rw [abs_of_pos hp]
    push_cast
    field_simp [hrC]

theorem lattice_flowLevel_period {r : ℝ} (hr : r ≠ 0) (h : SiteLogLattice P r)
    (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowLevel P (2*Real.pi/|r|) N a = a := by
  ext i j
  obtain ⟨k,hk⟩ := tower_log_lattice h N i j
  simp only [flowLevel,hk,modularPhase_lattice_period hr,one_mul]

theorem lattice_modular_period {r : ℝ} (hr : r ≠ 0) (h : SiteLogLattice P r) :
    modularFlow P (2*Real.pi/|r|) = id := by
  funext x
  refine Completion.induction_on x (isClosed_eq
    (modularFlow_continuous _) continuous_id) ?_
  intro v
  obtain ⟨N,a,rfl⟩ := exists_tof v
  rw [modularFlow_coe,flowPre_tof,lattice_flowLevel_period hr h]
  rfl

theorem stationary_site_log_lattice {p : ℝ} (hp : ∀ n, P.w n = p) :
    SiteLogLattice P (Real.log p - Real.log (1-p)) := by
  intro n i j
  fin_cases i <;> fin_cases j
  · exact ⟨0,by simp [siteW,hp]⟩
  · exact ⟨1,by simp [siteW,hp]⟩
  · exact ⟨-1,by simp [siteW,hp]⟩
  · exact ⟨0,by simp [siteW,hp]⟩

theorem stationary_log_gap_ne_zero {p : ℝ} (hp : ∀ n, P.w n = p) (hne : p ≠ 1/2) :
    Real.log p - Real.log (1-p) ≠ 0 := by
  have hpos : 0 < p := by rw [← hp 0]; exact P.pos 0
  have hlt : p < 1 := by rw [← hp 0]; exact P.lt_one 0
  intro h
  have he := Real.log_injOn_pos hpos (show 0 < 1-p by linarith) (sub_eq_zero.mp h)
  apply hne
  linarith

theorem stationary_modular_period {p : ℝ} (hp : ∀ n, P.w n = p) (hne : p ≠ 1/2) :
    modularFlow P (2*Real.pi/|Real.log (p/(1-p))|) = id := by
  have hpos : 0 < p := by rw [← hp 0]; exact P.pos 0
  have hlt : p < 1 := by rw [← hp 0]; exact P.lt_one 0
  rw [Real.log_div (ne_of_gt hpos) (ne_of_gt (show 0 < 1-p by linarith))]
  exact lattice_modular_period (stationary_log_gap_ne_zero hp hne) (stationary_site_log_lattice hp)

#print axioms tower_log_lattice
#print axioms modularPhase_lattice_period
#print axioms lattice_flowLevel_period
#print axioms lattice_modular_period
#print axioms stationary_site_log_lattice
#print axioms stationary_log_gap_ne_zero
#print axioms stationary_modular_period
end
end ChatgptAudit
