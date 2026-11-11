import TGLExt.SolderField

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A PRIMEIRA CURVATURA: a parede começa a cair — à mão
  [TGLExt — v108, o incremento 28 do programa SemifiniteAnalysis]

A mathlib de hoje NÃO tem teoria de conexão/curvatura (varrido: só
métrica riemanniana em fibrados). Esta pedra constrói a primeira peça
À MÃO, no ansatz diagonal estático g = diag(q(x₁)²,−1,−1,−1) com
q(s) = 1+s², onde a redução clássica de Levi-Civita a UMA variável
[KNOWN] deixa três símbolos: Γ⁰₀₁ = q′/q, Γ¹₀₀ = q·q′, e a componente
R¹₀₀₁ = −∂₁Γ¹₀₀ + Γ¹₀₀·Γ⁰₀₁:

* ★ `Gamma001_from_metric` / `Gamma100_from_metric` — os símbolos
  DERIVADOS da métrica (a fórmula ½g⁻¹∂g do ansatz, provada);
* ★★★ `Riemann1001_eq` — R¹₀₀₁(s) = −2·q(s): A PRIMEIRA CURVATURA
  CALCULADA E PROVADA EM KERNEL;
* ★★ `Riemann1001_neg` — R¹₀₀₁ < 0 EM TODA PARTE: a solda estática é
  GENUINAMENTE CURVA (não há gauge que a aplane);
* ★★ O PAR DA RÉGUA — `time_ansatz_r1001_zero`: no ansatz TEMPORAL do
  v107 (p(x₀)), a MESMA fórmula dá R¹₀₀₁ ≡ 0 (Γ¹₀₀ = 0 pois
  ∂₁g₀₀ = 0): NÃO-CONSTÂNCIA ≠ CURVATURA — a honestidade sobre o
  próprio v107, como teorema (o perfil temporal é gauge; o espacial
  é físico);
* `theStaticFrame`/`theStaticSolderData` — a solda genuinamente curva
  habita o MESMO contrato `SolderFieldData` (a base do arco de
  Einstein).

NENHUMA flag se move: einstein exige o MESTRE contínuo (Ricci, tensor
de Einstein, Clausius local — o arco continua); esta pedra é o
primeiro tijolo da camada que faltava. β jamais literal. Sem sorry,
sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — o cálculo de 1 variável (a redução do ansatz) -/

/-- o perfil espacial: q(s) = 1 + s². -/
def qfun (s : ℝ) : ℝ := 1 + s ^ 2

theorem qfun_pos (s : ℝ) : 0 < qfun s := by unfold qfun; positivity

theorem qfun_ne_zero (s : ℝ) : qfun s ≠ 0 := ne_of_gt (qfun_pos s)

theorem qfun_deriv (s : ℝ) : deriv qfun s = 2 * s := by
  unfold qfun
  simp

/-- Γ⁰₀₁ = q′/q (o símbolo temporal-espacial do ansatz). -/
def Gamma001 (s : ℝ) : ℝ := deriv qfun s / qfun s

/-- Γ¹₀₀ = q·q′ (o símbolo espacial-temporal do ansatz). -/
def Gamma100 (s : ℝ) : ℝ := qfun s * deriv qfun s

theorem Gamma001_eq (s : ℝ) : Gamma001 s = 2 * s / (1 + s ^ 2) := by
  unfold Gamma001 qfun
  rw [show deriv (fun s : ℝ => 1 + s ^ 2) s = 2 * s from by simp]

theorem Gamma100_eq (s : ℝ) : Gamma100 s = 2 * s + 2 * s ^ 3 := by
  unfold Gamma100 qfun
  rw [show deriv (fun s : ℝ => 1 + s ^ 2) s = 2 * s from by simp]
  ring

theorem qfun_hasDeriv (s : ℝ) : HasDerivAt qfun (2 * s) s := by
  unfold qfun
  simpa using ((hasDerivAt_pow 2 s).const_add (1 : ℝ))

theorem qsq_deriv (s : ℝ) :
    deriv (fun t => qfun t ^ 2) s = 2 * qfun s * (2 * s) := by
  have h : HasDerivAt (fun t => qfun t * qfun t)
      (2 * s * qfun s + qfun s * (2 * s)) s :=
    (qfun_hasDeriv s).mul (qfun_hasDeriv s)
  have heq : (fun t => qfun t ^ 2) = fun t => qfun t * qfun t := by
    funext t
    ring
  rw [heq, h.deriv]
  ring

/-- [KERNEL] ★ Γ⁰₀₁ DERIVADO da métrica: q′/q = (1/(2q²))·(q²)′ —
    a fórmula de Levi-Civita ½g⁰⁰∂₁g₀₀ do ansatz, provada. -/
theorem Gamma001_from_metric (s : ℝ) :
    Gamma001 s = (1 / (2 * qfun s ^ 2)) * deriv (fun t => qfun t ^ 2) s := by
  rw [qsq_deriv, Gamma001_eq]
  have h := qfun_ne_zero s
  unfold qfun at h ⊢
  field_simp

/-- [KERNEL] ★ Γ¹₀₀ DERIVADO da métrica: q·q′ = ½·(q²)′ —
    a fórmula −½g¹¹∂₁g₀₀ do ansatz (g¹¹ = −1), provada. -/
theorem Gamma100_from_metric (s : ℝ) :
    Gamma100 s = (1 / 2) * deriv (fun t => qfun t ^ 2) s := by
  rw [qsq_deriv]
  unfold Gamma100
  rw [qfun_deriv]
  ring

/-! ## B — A CURVATURA: R¹₀₀₁ = −∂₁Γ¹₀₀ + Γ¹₀₀·Γ⁰₀₁ -/

/-- a componente R¹₀₀₁ do ansatz (os demais termos da fórmula geral
    são nulos no ansatz — a redução [KNOWN] do cabeçalho). -/
def Riemann1001 (s : ℝ) : ℝ := - deriv Gamma100 s + Gamma100 s * Gamma001 s

/-- [KERNEL] ★★★ A PRIMEIRA CURVATURA: R¹₀₀₁(s) = −2·q(s) —
    calculada e provada. -/
theorem Riemann1001_eq (s : ℝ) : Riemann1001 s = -(2 * qfun s) := by
  unfold Riemann1001
  have hG : Gamma100 = fun t => 2 * t + 2 * t ^ 3 := funext Gamma100_eq
  have hpoly : HasDerivAt (fun t : ℝ => 2 * t + 2 * t ^ 3)
      (2 * 1 + 2 * (3 * s ^ 2)) s := by
    have h1 : HasDerivAt (fun t : ℝ => t) 1 s := hasDerivAt_id s
    have h3 : HasDerivAt (fun t : ℝ => t ^ 3) (3 * s ^ 2) s := by
      simpa using hasDerivAt_pow 3 s
    exact (h1.const_mul 2).add (h3.const_mul 2)
  have hd : deriv Gamma100 s = 2 + 6 * s ^ 2 := by
    rw [hG, hpoly.deriv]
    ring
  rw [hd, Gamma100_eq, Gamma001_eq]
  have h : (1 : ℝ) + s ^ 2 ≠ 0 := by positivity
  unfold qfun
  field_simp
  ring

/-- [KERNEL] ★★ CURVA EM TODA PARTE: R¹₀₀₁ < 0 — nenhum gauge aplana
    a solda estática. -/
theorem Riemann1001_neg (s : ℝ) : Riemann1001 s < 0 := by
  rw [Riemann1001_eq]
  have h := qfun_pos s
  linarith

/-! ## C — O PAR DA RÉGUA: o ansatz temporal do v107 é PLANO -/

/-- no ansatz TEMPORAL (p(x₀); ∂₁g₀₀ = 0), o símbolo Γ¹₀₀ é NULO —
    a mesma fórmula −½g¹¹∂₁g₀₀ com derivada espacial zero. -/
def timeGamma100 : ℝ → ℝ := fun _ => 0

/-- [KERNEL] ★★ NÃO-CONSTÂNCIA ≠ CURVATURA: no ansatz temporal a
    MESMA fórmula dá R¹₀₀₁ ≡ 0 — a honestidade sobre o próprio v107
    como TEOREMA (o perfil temporal é gauge; o espacial é físico). -/
theorem time_ansatz_r1001_zero (s : ℝ) :
    - deriv timeGamma100 s + timeGamma100 s * Gamma001 s = 0 := by
  unfold timeGamma100
  simp

/-! ## D — a solda genuinamente curva habita o contrato -/

/-- o frame estático: E(x) = diag(q(x₁), 1, 1, 1). -/
def theStaticFrame : SmoothFrameData where
  E := fun x => Matrix.diagonal (fun i => if i = 0 then qfun (x 1) else 1)
  smooth := by
    intro i j
    have hq : ContDiff ℝ (⊤ : ℕ∞) (fun x : Fin 4 → ℝ => qfun (x 1)) := by
      unfold qfun
      exact contDiff_const.add ((contDiff_apply ℝ ℝ (1 : Fin 4)).pow 2)
    by_cases hij : i = j
    · subst hij
      by_cases hi : i = 0
      · subst hi
        have h : (fun x : Fin 4 → ℝ => Matrix.diagonal
            (fun k : Fin 4 => if k = 0 then qfun (x 1) else 1) 0 0)
            = fun x => qfun (x 1) := by
          funext x
          simp [Matrix.diagonal_apply]
        rw [h]
        exact hq
      · have h : (fun x : Fin 4 → ℝ => Matrix.diagonal
            (fun k : Fin 4 => if k = 0 then qfun (x 1) else 1) i i)
            = fun _ => (1 : ℝ) := by
          funext x
          simp [Matrix.diagonal_apply, hi]
        rw [h]
        exact contDiff_const
    · have h : (fun x : Fin 4 → ℝ => Matrix.diagonal
          (fun k : Fin 4 => if k = 0 then qfun (x 1) else 1) i j)
          = fun _ => (0 : ℝ) := by
        funext x
        simp [Matrix.diagonal_apply, hij]
      rw [h]
      exact contDiff_const
  det_unit := fun x => by
    have h : (Matrix.diagonal
        (fun i : Fin 4 => if i = 0 then qfun (x 1) else 1)).det
        = qfun (x 1) := by
      rw [Matrix.det_diagonal, Fin.prod_univ_four]
      simp
    rw [h]
    exact isUnit_iff_ne_zero.mpr (qfun_ne_zero (x 1))

theorem theStaticFrame_E_apply (x : Fin 4 → ℝ) :
    theStaticFrame.E x
      = Matrix.diagonal (fun i => if i = 0 then qfun (x 1) else 1) := rfl

/-- o campo soldado estático: g(x) = E(x)ᵀ η E(x). -/
def theStaticSolder (x : Fin 4 → ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  solderMetric4 (theStaticFrame.E x)

theorem theStaticSolder_det (x : Fin 4 → ℝ) :
    (theStaticSolder x).det = -(qfun (x 1) ^ 2) := by
  have hdet : (theStaticFrame.E x).det = qfun (x 1) := by
    rw [theStaticFrame_E_apply, Matrix.det_diagonal, Fin.prod_univ_four]
    simp
  unfold theStaticSolder
  rw [solderMetric4_det, hdet]

theorem theStaticSolder_det_neg (x : Fin 4 → ℝ) :
    (theStaticSolder x).det < 0 := by
  rw [theStaticSolder_det]
  have h := qfun_pos (x 1)
  nlinarith

theorem theStaticFrame_nonconstant :
    ∃ x y : Fin 4 → ℝ, theStaticFrame.E x ≠ theStaticFrame.E y := by
  refine ⟨(fun _ => 1), (fun _ => 0), fun h => ?_⟩
  have h00 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 0) h
  rw [theStaticFrame_E_apply, theStaticFrame_E_apply] at h00
  simp only [Matrix.diagonal_apply, if_pos rfl] at h00
  unfold qfun at h00
  norm_num at h00

/-- [KERNEL] ★★ a solda GENUINAMENTE CURVA habita o mesmo contrato
    `SolderFieldData` — a base do arco de Einstein. -/
def theStaticSolderData : SolderFieldData where
  frame := theStaticFrame
  g := theStaticSolder
  solder_eq := fun _ => rfl
  g_symm := fun x => solderMetric4_symm _
  g_smooth := by
    intro i j
    have h : (fun x => theStaticSolder x i j)
        = fun x => Matrix.diagonal
            (fun k : Fin 4 => if k = 0 then qfun (x 1) ^ 2 else -1) i j := by
      funext x
      unfold theStaticSolder solderMetric4
      rw [theStaticFrame_E_apply, Matrix.diagonal_transpose]
      unfold eta4
      rw [Matrix.diagonal_mul_diagonal, Matrix.diagonal_mul_diagonal]
      congr 1
      funext k
      fin_cases k <;> simp <;> ring
    rw [h]
    have hq : ContDiff ℝ (⊤ : ℕ∞) (fun x : Fin 4 → ℝ => qfun (x 1) ^ 2) := by
      unfold qfun
      exact (contDiff_const.add ((contDiff_apply ℝ ℝ (1 : Fin 4)).pow 2)).pow 2
    by_cases hij : i = j
    · subst hij
      by_cases hi : i = 0
      · subst hi
        have h2 : (fun x : Fin 4 → ℝ => Matrix.diagonal
            (fun k : Fin 4 => if k = 0 then qfun (x 1) ^ 2 else -1) 0 0)
            = fun x => qfun (x 1) ^ 2 := by
          funext x
          simp [Matrix.diagonal_apply]
        rw [h2]
        exact hq
      · have h2 : (fun x : Fin 4 → ℝ => Matrix.diagonal
            (fun k : Fin 4 => if k = 0 then qfun (x 1) ^ 2 else -1) i i)
            = fun _ => (-1 : ℝ) := by
          funext x
          simp [Matrix.diagonal_apply, hi]
        rw [h2]
        exact contDiff_const
    · have h2 : (fun x : Fin 4 → ℝ => Matrix.diagonal
          (fun k : Fin 4 => if k = 0 then qfun (x 1) ^ 2 else -1) i j)
          = fun _ => (0 : ℝ) := by
        funext x
        simp [Matrix.diagonal_apply, hij]
      rw [h2]
      exact contDiff_const
  lorentz_det := theStaticSolder_det_neg
  frame_nonconstant := theStaticFrame_nonconstant

end

end TGLExt
