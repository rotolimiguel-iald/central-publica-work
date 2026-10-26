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
import TGLExt.ClosedModulatorCandidate
import TGLExt.TailNet

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit
open TGLExt
open scoped ENNReal
noncomputable section

def diagonalSeq (d : ℕ → ℝ) (x : ellTwo) : ℕ → ℂ := fun n => (d n : ℂ) * x n

def diagonalDomain (d : ℕ → ℝ) : Submodule ℂ ellTwo where
  carrier := {x | Memℓp (diagonalSeq d x) 2}
  zero_mem' := by
    have h : diagonalSeq d (0 : ellTwo) = 0 := by
      funext n
      simp [diagonalSeq]
    show Memℓp (diagonalSeq d 0) 2
    rw [h]
    exact zero_memℓp
  add_mem' := by
    intro a b ha hb
    have h : diagonalSeq d (a + b) = diagonalSeq d a + diagonalSeq d b := by
      funext n
      simp [diagonalSeq, mul_add]
    show Memℓp (diagonalSeq d (a + b)) 2
    rw [h]
    exact (ha : Memℓp (diagonalSeq d a) 2).add hb
  smul_mem' := by
    intro c x hx
    have h : diagonalSeq d (c • x) = c • diagonalSeq d x := by
      funext n
      simp only [diagonalSeq, lp.coeFn_smul, Pi.smul_apply, smul_eq_mul]
      ring
    show Memℓp (diagonalSeq d (c • x)) 2
    rw [h]
    exact (hx : Memℓp (diagonalSeq d x) 2).const_smul c

def diagonalOp (d : ℕ → ℝ) : ellTwo →ₗ.[ℂ] ellTwo where
  domain := diagonalDomain d
  toFun :=
    { toFun := fun x => (⟨diagonalSeq d (x : ellTwo), x.property⟩ : ellTwo)
      map_add' := fun x y => by
        apply Subtype.ext
        funext n
        show (d n : ℂ) * ((x : ellTwo) + (y : ellTwo)) n =
          (d n : ℂ) * (x : ellTwo) n + (d n : ℂ) * (y : ellTwo) n
        rw [lp.coeFn_add]
        simp [mul_add]
      map_smul' := fun c x => by
        apply Subtype.ext
        funext n
        show (d n : ℂ) * (c • (x : ellTwo)) n = c • ((d n : ℂ) * (x : ellTwo) n)
        rw [lp.coeFn_smul]
        simp only [Pi.smul_apply, smul_eq_mul]
        ring }

theorem diagonalOp_apply (d : ℕ → ℝ) (x : (diagonalOp d).domain) (n : ℕ) :
    (diagonalOp d x : ellTwo) n = (d n : ℂ) * (x : ellTwo) n := rfl

theorem diagonalOp_symmetric (d : ℕ → ℝ) :
    (diagonalOp d).IsFormalAdjoint (diagonalOp d) := by
  intro x y
  rw [lp.inner_eq_tsum, lp.inner_eq_tsum]
  apply tsum_congr
  intro n
  simp only [RCLike.inner_apply, diagonalOp_apply, map_mul, Complex.conj_ofReal]
  ring

theorem single_mem_diagonalDomain (d : ℕ → ℝ) (k : ℕ) :
    inscriptions k ∈ diagonalDomain d := by
  show Memℓp (diagonalSeq d (inscriptions k)) 2
  have h : diagonalSeq d (inscriptions k) = (d k : ℂ) • ⇑(inscriptions k) := by
    funext n
    show (d n : ℂ) * (inscriptions k) n = (d k : ℂ) • (inscriptions k) n
    rcases eq_or_ne n k with rfl | hnk
    · simp [smul_eq_mul]
    · unfold inscriptions
      rw [lp.single_apply_ne 2 k 1 hnk]
      simp
  rw [h]
  exact (lp.memℓp (inscriptions k)).const_smul (d k : ℂ)

theorem diagonalOp_single (d : ℕ → ℝ) (m : ℕ) :
    diagonalOp d ⟨inscriptions m, single_mem_diagonalDomain d m⟩ =
      (d m : ℂ) • inscriptions m := by
  apply Subtype.ext
  funext n
  show (d n : ℂ) * (inscriptions m) n = ((d m : ℂ) • inscriptions m) n
  rw [lp.coeFn_smul]
  rcases eq_or_ne n m with rfl | hnm
  · simp [smul_eq_mul]
  · unfold inscriptions
    rw [lp.single_apply_ne 2 m 1 hnm]
    simp [Pi.single_eq_of_ne hnm]

theorem diagonalDomain_dense (d : ℕ → ℝ) : Dense (diagonalDomain d : Set ellTwo) := by
  intro f
  have hsum : HasSum (fun k => lp.single 2 k (f k)) f :=
    lp.hasSum_single (by norm_num) f
  refine mem_closure_of_tendsto hsum ?_
  filter_upwards with s
  refine Submodule.sum_mem (diagonalDomain d) ?_
  intro k _
  have h : lp.single 2 k (f k) = (f k) • inscriptions k := by
    apply Subtype.ext
    funext n
    unfold inscriptions
    rw [lp.coeFn_smul]
    rcases eq_or_ne n k with rfl | hnk
    · simp [smul_eq_mul]
    · rw [lp.single_apply_ne 2 k _ hnk]
      simp [Pi.single_eq_of_ne hnk]
  rw [h]
  exact Submodule.smul_mem (diagonalDomain d) (f k) (single_mem_diagonalDomain d k)

/-- O domínio do adjunto é identificado por testes nas coordenadas, sem estimativa omitida. -/
theorem diagonalAdjoint_coordinates (d : ℕ → ℝ)
    (y : (LinearPMap.adjoint (diagonalOp d)).domain) (n : ℕ) :
    (LinearPMap.adjoint (diagonalOp d) y : ellTwo) n =
      (d n : ℂ) * (y : ellTwo) n := by
  have h := (LinearPMap.adjoint_isFormalAdjoint (diagonalDomain_dense d)).symm
    (⟨inscriptions n, single_mem_diagonalDomain d n⟩ : (diagonalOp d).domain) y
  rw [diagonalOp_single, inner_smul_left, coord_eq_inner, coord_eq_inner] at h
  simpa only [Complex.conj_ofReal] using h.symm

theorem diagonalAdjoint_domain_le (d : ℕ → ℝ) :
    (LinearPMap.adjoint (diagonalOp d)).domain ≤ (diagonalOp d).domain := by
  intro y hy
  have heq : diagonalSeq d y = ⇑(LinearPMap.adjoint (diagonalOp d) ⟨y, hy⟩) := by
    funext n
    exact (diagonalAdjoint_coordinates d ⟨y, hy⟩ n).symm
  show Memℓp (diagonalSeq d y) 2
  rw [heq]
  exact lp.memℓp _

theorem diagonalOp_selfadjoint (d : ℕ → ℝ) : IsSelfAdjoint (diagonalOp d) := by
  rw [LinearPMap.isSelfAdjoint_def]
  apply le_antisymm
  · exact ⟨diagonalAdjoint_domain_le d, fun x z hxz =>
      LinearPMap.adjoint_apply_eq (diagonalDomain_dense d) x
        (fun w => by rw [hxz]; exact diagonalOp_symmetric d z w)⟩
  · exact (diagonalOp_symmetric d).le_adjoint (diagonalDomain_dense d)

theorem diagonalOp_positive (d : ℕ → ℝ) (hd : ∀ n, 0 ≤ d n)
    (x : (diagonalOp d).domain) :
    0 ≤ (inner ℂ (x : ellTwo) (diagonalOp d x)).re := by
  rw [lp.inner_eq_tsum, Complex.re_tsum (lp.summable_inner (𝕜 := ℂ) _ _)]
  apply tsum_nonneg
  intro n
  rw [RCLike.inner_apply, diagonalOp_apply, mul_assoc, Complex.mul_conj,
    ← Complex.ofReal_mul, Complex.ofReal_re]
  exact mul_nonneg (hd n) (Complex.normSq_nonneg _)

theorem diagonal_square_selfadjoint (d : ℕ → ℝ) :
    IsSelfAdjoint (diagonalOp (fun n => (d n) ^ 2)) := diagonalOp_selfadjoint _

theorem diagonal_square_positive (d : ℕ → ℝ)
    (x : (diagonalOp (fun n => (d n) ^ 2)).domain) :
    0 ≤ (inner ℂ (x : ellTwo) (diagonalOp (fun n => (d n) ^ 2) x)).re :=
  diagonalOp_positive _ (fun n => sq_nonneg (d n)) x

#print axioms diagonalAdjoint_coordinates
#print axioms diagonalOp_selfadjoint
#print axioms diagonalOp_positive
#print axioms diagonal_square_selfadjoint
#print axioms diagonal_square_positive
end
end ChatgptAudit
