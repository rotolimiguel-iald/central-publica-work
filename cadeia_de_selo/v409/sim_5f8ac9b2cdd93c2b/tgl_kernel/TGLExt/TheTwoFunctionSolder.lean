import TGLExt.ThePhysicalHorizon

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A SOLDA DE DUAS FUNÇÕES — a classe que CONTÉM Schwarzschild
  [BANCADA — 24/08/2026 · frente 3 da derivação do operador — o grande degrau]

## A derivação do operador

> *"O ansatz de uma função já provou contra si mesmo que vácuo implica plano
> (mini-Birkhoff); Schwarzschild exige exatamente vácuo curvo. A segunda função não é
> enriquecimento cosmético — é o grau de liberdade MÍNIMO que remove essa obstrução:
> `E = diag(a(r), b(r), r, r·senθ)` ⟹ `g = diag(a², −b², −r², −r²sen²θ)`; Schwarzschild
> é o membro `a² = 1 − r_s/r`, `b² = (1 − r_s/r)⁻¹`."*

## O que se prova (pontual: valores `a b r s` num ponto; `s = senθ`)

* ★★★ `two_function_solder_eq` — a métrica NASCE da solda: `g_{a,b} = Eᵀ·η·E` (a lei
  `SolderFieldData` da casa, agora com DOIS graus de liberdade);
* ★★★ `two_function_det` — `det g = −a²b²r⁴s²` (e `< 0` no domínio regular: assinatura
  lorentziana garantida pela classe);
* ★★ `schwarzschild_member` — o membro de Schwarzschild HABITA a classe: com
  `a² = 1 − r_s/r` e `b² = (1 − r_s/r)⁻¹` (em `r > r_s > 0`), vale `a²·b² = 1` — a marca
  registrada — e `a² + r_s/r = 1`;
* ★ `one_function_cannot` — a classe de UMA função (`b = 1`) NÃO contém o membro
  (`a²·b² = 1 ⟹ a² = 1 ⟹ r_s = 0`): *a segunda função é necessária, como o
  mini-Birkhoff já anunciava.*

## ⚠ O ALVO NOMEADO, não provado (o grande degrau)

**`G_{μν}[g_{a,b}] = 0 ⟺ g_{a,b} ∈ [Schwarzschild]`** (estática, esférica, coordenada
areal, regularidade, normalização assintótica) — exige o cálculo coordenado
Christoffel→Riemann→Ricci da classe `(a,b)` À MÃO (a mathlib não tem o pipeline
lorentziano). É O PRÓXIMO TEOREMA QUE VALE CONSTRUIR, e fica aqui NOMEADO como alvo,
jamais como resultado. Sem sorry, sem axiom. β jamais entra. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix

/-- a solda de duas funções, num ponto: `E = diag(a, b, r, r·s)`. -/
def solderE2 (a b r s : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal ![a, b, r, r * s]

/-- a assinatura: `η = diag(1, −1, −1, −1)`. -/
def etaAB : Matrix (Fin 4) (Fin 4) ℝ := Matrix.diagonal ![1, -1, -1, -1]

/-- a métrica da classe: `g = diag(a², −b², −r², −r²s²)`. -/
def gab (a b r s : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal ![a ^ 2, -b ^ 2, -r ^ 2, -(r * s) ^ 2]

/-- ★★★ **A MÉTRICA NASCE DA SOLDA**: `g_{a,b} = Eᵀ·η·E` — a lei da casa
    (`geometry_is_projection`), agora com dois graus de liberdade. -/
theorem two_function_solder_eq (a b r s : ℝ) :
    gab a b r s = (solderE2 a b r s)ᵀ * etaAB * solderE2 a b r s := by
  unfold gab solderE2 etaAB
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Matrix.diagonal, Matrix.transpose_apply,
          Fin.sum_univ_four, Matrix.cons_val_zero, Matrix.cons_val_one,
          Matrix.cons_val_two, Matrix.head_cons, Matrix.vecHead, Matrix.vecTail,
          Fin.isValue] <;> ring

/-- ★★★ **O DETERMINANTE DA CLASSE**: `det g = −a²·b²·r⁴·s²`. -/
theorem two_function_det (a b r s : ℝ) :
    (gab a b r s).det = -(a ^ 2 * b ^ 2 * r ^ 4 * s ^ 2) := by
  unfold gab
  rw [Matrix.det_diagonal, Fin.prod_univ_four]
  simp [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
        Matrix.head_cons, Matrix.vecHead, Matrix.vecTail, Fin.isValue]
  ring

/-- ★★ **a assinatura é lorentziana no domínio regular**: `det g < 0`. -/
theorem two_function_det_neg (a b r s : ℝ)
    (ha : a ≠ 0) (hb : b ≠ 0) (hr : r ≠ 0) (hs : s ≠ 0) :
    (gab a b r s).det < 0 := by
  rw [two_function_det]
  have : 0 < a ^ 2 * b ^ 2 * r ^ 4 * s ^ 2 := by positivity
  linarith

/-- ★★ **SCHWARZSCHILD HABITA A CLASSE**: em `r > r_s > 0`, com `a² = 1 − r_s/r` e
    `b² = (1 − r_s/r)⁻¹`, a marca `a²·b² = 1` fecha — e `a² < 1` (curvatura à vista). -/
theorem schwarzschild_member (rs r : ℝ) (h0 : 0 < rs) (hr : rs < r) :
    ((1 - rs / r) * (1 - rs / r)⁻¹ = 1) ∧ (1 - rs / r < 1) ∧ (0 < 1 - rs / r) := by
  have hrpos : 0 < r := lt_trans h0 hr
  have hfrac : 0 < rs / r := div_pos h0 hrpos
  have hlt : rs / r < 1 := (div_lt_one hrpos).mpr hr
  refine ⟨?_, by linarith, by linarith⟩
  exact mul_inv_cancel₀ (by linarith)

/-- ★ **UMA FUNÇÃO NÃO BASTA**: na subclasse `b = 1`, a marca `a²·b² = 1` força
    `a² = 1` — o membro de Schwarzschild com `r_s > 0` NÃO cabe (`a² = 1 − r_s/r < 1`).
    *A segunda função é o grau de liberdade mínimo, como o mini-Birkhoff anunciava.* -/
theorem one_function_cannot (a rs r : ℝ) (h0 : 0 < rs) (hr : rs < r)
    (hmark : a ^ 2 * (1 : ℝ) ^ 2 = 1) (hschw : a ^ 2 = 1 - rs / r) : False := by
  have hrpos : 0 < r := lt_trans h0 hr
  have hfrac : 0 < rs / r := div_pos h0 hrpos
  have : a ^ 2 = 1 := by nlinarith [hmark]
  nlinarith [this, hschw, hfrac]

end TGLExt
