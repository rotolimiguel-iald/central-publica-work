import TGLExt.Ergodicity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A SEÇÃO ERGÓDICA EQUIVARIANTE — face finita
  [TGLExt — a condicional «seção ergódica equivariante» do pacote
   TGL_SOLDERED_BREUER_HILBERT_PACKAGE ganha a sua face finita]

O v56 nomeou o único aberto (o pacote soldado de Breuer–Hilbert) com
três condicionais; uma delas é a SEÇÃO ERGÓDICA EQUIVARIANTE. A sombra
130_ a construiu numericamente sobre a rede de Powers (a seção espectral
comuta com o shift da rede); esta pedra prova a FACE FINITA em kernel:

* `specExpect` — a seção espectral GERAL (pesos DEGENERADOS permitidos:
  é onde a equivariância vive — a rede homogênea tem pesos repetidos que
  o shift permuta). No caso injetivo colapsa em `diagExpect`
  (`specExpect_of_injective`).
* `specExpect_one`, `specExpect_idem` — é esperança (unital, idempotente);
* `rhoD_commute_specExpect` — cai no CENTRALIZADOR de ρ_D;
* `sigma_fixed_specExpect` — é FIXA pelo fluxo modular;
* `trace_rhoD_specExpect` — preserva o estado (a seção não gasta);
* ★ `sigma_fixed_iff_specExpect` — O SETOR FIXO É A SEÇÃO, MESMO
  DEGENERADO: `(∀ t, σₜ(x) = x) ↔ x = specExpect d x` — generaliza
  estritamente o `sigma_fixed_iff_diag` (que exigia d injetivo);
* ★ `specExpect_equivariant` — A EQUIVARIÂNCIA: toda simetria
  `e : Equiv.Perm n` que preserva o peso (`d ∘ e = d`) comuta com a
  seção: `E(x ∘ e) = E(x) ∘ e` (em forma de `submatrix`) — a seção que
  nasce do fluxo respeita TODA simetria do estado. O que a sombra 130_
  mediu vira TEOREMA.

HONESTIDADE: face FINITA. O contínuo (Davies/N3), a subordinação
Poisson–Cauchy e o III₁ genuíno seguem onde estão — a condicional do
pacote NÃO fecha aqui; ganha o primeiro degrau em kernel. β JAMAIS
entra no Lean. Sem sorry, sem axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {n : Type} [Fintype n] [DecidableEq n]

open scoped Classical in
/-- A SEÇÃO ESPECTRAL GERAL: mantém as entradas de peso igual
    (`d i = d j`), zera as demais. Com pesos degenerados mantém BLOCOS —
    o caso da rede homogênea, onde a equivariância vive. -/
def specExpect (d : n → ℝ) (x : Matrix n n ℂ) : Matrix n n ℂ :=
  of fun i j => if d i = d j then x i j else 0

open scoped Classical in
@[simp] theorem specExpect_apply (d : n → ℝ) (x : Matrix n n ℂ) (i j : n) :
    specExpect d x i j = if d i = d j then x i j else 0 := rfl

/-- No caso NÃO-degenerado a seção espectral é a esperança diagonal:
    `specExpect` estende `diagExpect`, não o substitui. -/
theorem specExpect_of_injective (d : n → ℝ) (hinj : Function.Injective d)
    (x : Matrix n n ℂ) : specExpect d x = diagExpect x := by
  ext i j
  by_cases hij : i = j
  · subst hij
    simp [diagExpect, diag]
  · have hd : d i ≠ d j := fun hc => hij (hinj hc)
    simp [hd, diagExpect, hij]

/-- A seção é UNITAL: `E(1) = 1` — a esperança não inventa nem perde o Um. -/
theorem specExpect_one (d : n → ℝ) : specExpect d (1 : Matrix n n ℂ) = 1 := by
  ext i j
  by_cases hij : i = j
  · subst hij; simp
  · simp [Matrix.one_apply_ne hij, ite_self]

/-- A seção é IDEMPOTENTE: `E(E(x)) = E(x)` — guardar duas vezes é guardar. -/
theorem specExpect_idem (d : n → ℝ) (x : Matrix n n ℂ) :
    specExpect d (specExpect d x) = specExpect d x := by
  ext i j
  by_cases h : d i = d j
  · simp [h]
  · simp [h]

/-- A seção cai no CENTRALIZADOR do estado: `[ρ_D, E(x)] = 0` — o setor
    onde o traço emerge (G2) recebe a seção. -/
theorem rhoD_commute_specExpect (d : n → ℝ) (x : Matrix n n ℂ) :
    rhoD d * specExpect d x = specExpect d x * rhoD d := by
  ext i j
  by_cases h : d i = d j
  · simp [rhoD, diagonal_mul, mul_diagonal, h, mul_comm]
  · simp [rhoD, diagonal_mul, mul_diagonal, h]

/-- A seção é FIXA pelo fluxo modular: `σₜ(E(x)) = E(x)` — nas entradas
    mantidas os pesos coincidem e a fase modular vale 1. -/
theorem sigma_fixed_specExpect (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (x : Matrix n n ℂ) (t : ℝ) :
    sigma (rhoD d) t (specExpect d x) = specExpect d x := by
  ext i j
  rw [sigma_diagonal_apply d hd t]
  by_cases h : d i = d j
  · simp [h]
  · simp [h]

/-- A seção PRESERVA O ESTADO: `Tr(ρ_D E(x)) = Tr(ρ_D x)` — guardar não
    gasta (a diagonal é mantida inteira). -/
theorem trace_rhoD_specExpect (d : n → ℝ) (x : Matrix n n ℂ) :
    (rhoD d * specExpect d x).trace = (rhoD d * x).trace := by
  simp only [Matrix.trace, Matrix.diag, rhoD, diagonal_mul]
  exact Finset.sum_congr rfl fun i _ => by simp

/-- ★ O SETOR FIXO É A SEÇÃO — MESMO DEGENERADO: `(∀ t, σₜ(x) = x) ↔
    x = specExpect d x`. Generaliza `sigma_fixed_iff_diag` (que pedia
    `d` injetivo): a obstrução nunca foi o ÍNDICE repetido, é o PESO
    distinto — em `t★ = π/(log dᵢ − log dⱼ)` a fase vira −1 e a entrada
    morre. -/
theorem sigma_fixed_iff_specExpect (d : n → ℝ) (hd : ∀ i, 0 < d i)
    (x : Matrix n n ℂ) :
    (∀ t, sigma (rhoD d) t x = x) ↔ x = specExpect d x := by
  constructor
  · intro h
    ext i j
    by_cases hdij : d i = d j
    · simp [hdij]
    · have hlog : Real.log (d i) ≠ Real.log (d j) := fun hc =>
        hdij (Real.log_injOn_pos (Set.mem_Ioi.mpr (hd i))
          (Set.mem_Ioi.mpr (hd j)) hc)
      have hr : Real.log (d i) - Real.log (d j) ≠ 0 := sub_ne_zero.mpr hlog
      have hkey : Complex.exp (((Real.pi / (Real.log (d i) - Real.log (d j)) : ℝ) : ℂ)
          * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))) * x i j
          = x i j := by
        rw [← sigma_diagonal_apply d hd (Real.pi / (Real.log (d i) - Real.log (d j))) x i j]
        exact Matrix.ext_iff.mpr (h _) i j
      have harg : ((Real.pi / (Real.log (d i) - Real.log (d j)) : ℝ) : ℂ)
          * Complex.I * ((Real.log (d i) : ℂ) - (Real.log (d j) : ℂ))
          = (Real.pi : ℂ) * Complex.I := by
        rw [mul_right_comm, ← Complex.ofReal_sub, ← Complex.ofReal_mul,
          div_mul_cancel₀ _ hr]
      rw [harg, Complex.exp_pi_mul_I, neg_one_mul] at hkey
      have hx0 : x i j = 0 := add_self_eq_zero.mp (neg_eq_iff_add_eq_zero.mp hkey)
      simp [hdij, hx0]
  · intro hx t
    rw [hx]
    exact sigma_fixed_specExpect d hd x t

/-- ★★ A EQUIVARIÂNCIA — o teorema da pedra: toda simetria da rede que
    preserva o peso comuta com a seção. Para `e : Equiv.Perm n` com
    `d ∘ e = d`: `E(x ∘ (e,e)) = E(x) ∘ (e,e)` (conjugação pela
    permutação, em forma de `submatrix`). A seção ergódica que nasce do
    fluxo respeita TODA simetria do estado — a condicional do pacote,
    face finita, agora TEOREMA. -/
theorem specExpect_equivariant (d : n → ℝ) (e : Equiv.Perm n)
    (hde : ∀ i, d (e i) = d i) (x : Matrix n n ℂ) :
    specExpect d (x.submatrix e e) = (specExpect d x).submatrix e e := by
  ext i j
  by_cases h : d i = d j
  · simp [Matrix.submatrix_apply, hde, h]
  · simp [Matrix.submatrix_apply, hde, h]

end

end TGLExt
