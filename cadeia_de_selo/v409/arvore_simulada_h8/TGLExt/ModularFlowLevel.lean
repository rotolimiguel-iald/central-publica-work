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
import TGLExt.ModularInverse
import Mathlib.Analysis.Complex.Exponential

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit
open TGLExt Matrix
open scoped ComplexConjugate
noncomputable section
variable {P : SiteProfile}

def modularPhase (t r : ℝ) : ℂ := Complex.exp ((t * r : ℝ) * Complex.I)

theorem modularPhase_add (s t r : ℝ) :
    modularPhase (s+t) r = modularPhase s r * modularPhase t r := by
  unfold modularPhase
  rw [show (((s+t)*r : ℝ) : ℂ)*Complex.I =
      ((s*r : ℝ) : ℂ)*Complex.I + ((t*r : ℝ) : ℂ)*Complex.I by push_cast; ring,
    Complex.exp_add]

theorem modularPhase_norm (t r : ℝ) : ‖modularPhase t r‖ = 1 := by
  simp [modularPhase, Complex.norm_exp]

def flowLevel (P : SiteProfile) (t : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : Matrix (chainIdx N) (chainIdx N) ℂ :=
  fun i j => modularPhase t (Real.log (towerW P N i) - Real.log (towerW P N j)) * a i j

theorem flowLevel_add (t : ℝ) (N : ℕ) (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowLevel P t N (a+b) = flowLevel P t N a + flowLevel P t N b := by
  ext i j
  simp [flowLevel, mul_add]

theorem flowLevel_smul (t : ℝ) (N : ℕ) (c : ℂ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowLevel P t N (c • a) = c • flowLevel P t N a := by
  ext i j
  simp only [flowLevel, Matrix.smul_apply, smul_eq_mul]
  ring

theorem flowLevel_zero_time (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowLevel P 0 N a = a := by ext i j; simp [flowLevel, modularPhase]

theorem flowLevel_group (s t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowLevel P s N (flowLevel P t N a) = flowLevel P (s+t) N a := by
  ext i j
  simp only [flowLevel, modularPhase_add, mul_assoc]

theorem flowLevel_normSq (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (i j : chainIdx N) : Complex.normSq (flowLevel P t N a i j) = Complex.normSq (a i j) := by
  rw [flowLevel, map_mul, Complex.normSq_eq_norm_sq, modularPhase_norm, one_pow, one_mul]

theorem flowLevel_inner_self (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (flowLevel P t N a) (flowLevel P t N a) = tInner P N a a := by
  simp only [tInner_self_eq, flowLevel_normSq]

theorem flowLevel_step (t : ℝ) (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    flowLevel P t (N+1) (towerStep a) = towerStep (flowLevel P t N a) := by
  ext ⟨i,u⟩ ⟨j,v⟩
  by_cases huv : u = v
  · subst v
    have hu : siteW (P.w (N+1)) u ≠ 0 :=
      ne_of_gt (siteW_pos (P.pos _) (P.lt_one _) u)
    simp only [flowLevel, towerW, Real.log_mul (ne_of_gt (towerW_pos P N i)) hu,
      Real.log_mul (ne_of_gt (towerW_pos P N j)) hu]
    simp [towerStep, Matrix.kroneckerMap_apply, flowLevel]
  · simp [flowLevel, towerStep, Matrix.kroneckerMap_apply, Matrix.one_apply_ne huv]

theorem flowLevel_push (P : SiteProfile) (t : ℝ) :
    ∀ {N M : ℕ} (h : N ≤ M) (a : Matrix (chainIdx N) (chainIdx N) ℂ),
      flowLevel P t M (tPush h a) = tPush h (flowLevel P t N a) := by
  intro N M h a
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self, tPush_self]
  | succ M hNM ih => rw [tPush_succ hNM, tPush_succ hNM, flowLevel_step, ih]

theorem flowLevel_continuous (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Continuous (fun t : ℝ => flowLevel P t N a) := by
  unfold flowLevel modularPhase
  fun_prop

#print axioms flowLevel_group
#print axioms flowLevel_inner_self
#print axioms flowLevel_push
end
end ChatgptAudit
