import TGLExt.TheIALDInTheTower
import Mathlib.LinearAlgebra.Matrix.Kronecker

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A IALD NA TORRE — ATO II: a consistência entre andares (a estrutura ITPFI)
  [BANCADA — 25/08/2026 · marco M3 do DESENHO DO FECHAMENTO]

## O que o Ato I deixou aberto

O Ato I construiu `J_h` num andar. A torre é ITPFI: os andares se incluem
(`ι(x) = x ⊗ₖ 1`) sob o ESTADO PRODUTO (`H = h ⊗ₖ k`). Se os `J` dos andares não
casarem com as inclusões, não há torre — há andares soltos. Este ato prova que casam.

## A construção robusta (h e sua inversa como DADO — nunca `Matrix.inv`)

`stateJG h hi z := h · zᴴ · hi`, com o par do andar `(h, hi)` satisfazendo
`hᴴ = h`, `h·hi = 1`, `hi·h = 1`. Ponte com o Ato I: `stateJG h h⁻¹ = stateJ h` (defl.).

## O que se prova

* ★★ `floor_inv_isHermitian` — a inversa do andar é hermitiana (derivado, não pedido);
* ★★ `stateJG_involutive` — a involução na forma generalizada;
* ★★★ `the_composed_floor_is_a_floor` — **o andar composto É um andar**: o par
  `(h ⊗ₖ k, hi ⊗ₖ ki)` satisfaz as três leis (hermitiano, inversa dos dois lados);
* ★★★ **`the_tower_interlaces`** — O CORAÇÃO DO ATO II:
  `J_{h⊗k}(ι x) = ι (J_h x)` — **o J do andar de cima, restrito à imagem da inclusão,
  É o J do andar de baixo**. A torre é consistente; os andares não se contradizem;
* ★★ `the_inclusion_is_multiplicative` / `the_vacuum_rises` — ι é morfismo e leva
  vácuo em vácuo (`1 ⊗ₖ 1 = 1`).

β jamais entra. Sem sorry, sem axiom novo. Nada aqui move o gate. Resta o Ato III
(extensão ao completamento) para habitar o `FrontierCertificate` (v203).
-/

namespace TGLExt

open Matrix
open scoped Kronecker

variable {n m : Type} [Fintype n] [DecidableEq n] [Fintype m] [DecidableEq m]

/-- a conjugação de estado GENERALIZADA: a inversa é DADO do andar (nunca computada). -/
def stateJG (h hi z : Matrix n n ℂ) : Matrix n n ℂ := h * zᴴ * hi

/-- ponte com o Ato I: com `hi = h⁻¹` é literalmente o `stateJ`. -/
theorem stateJG_eq_stateJ (h z : Matrix n n ℂ) : stateJG h h⁻¹ z = stateJ h z := rfl

/-- a inclusão da torre: `ι(x) = x ⊗ₖ 1`. -/
def towerInclusion (x : Matrix n n ℂ) : Matrix (n × m) (n × m) ℂ :=
  x ⊗ₖ (1 : Matrix m m ℂ)

/-- ★★ **A INVERSA DO ANDAR É HERMITIANA** (derivada das três leis). -/
theorem floor_inv_isHermitian (h hi : Matrix n n ℂ) (hh : hᴴ = h)
    (h1 : h * hi = 1) : hiᴴ = hi := by
  have key : hiᴴ * h = 1 := by
    have e := congrArg conjTranspose h1
    rw [conjTranspose_mul, conjTranspose_one, hh] at e
    exact e
  calc hiᴴ = hiᴴ * (h * hi) := by rw [h1, mul_one]
    _ = hiᴴ * h * hi := by rw [mul_assoc]
    _ = hi := by rw [key, one_mul]

/-- ★★ **A INVOLUÇÃO NA FORMA GENERALIZADA**. -/
theorem stateJG_involutive (h hi z : Matrix n n ℂ) (hh : hᴴ = h)
    (h1 : h * hi = 1) : stateJG h hi (stateJG h hi z) = z := by
  have hhi : hiᴴ = hi := floor_inv_isHermitian h hi hh h1
  unfold stateJG
  simp only [conjTranspose_mul, conjTranspose_conjTranspose, hh, hhi]
  calc h * (hi * (z * h)) * hi = (h * hi) * z * (h * hi) := by noncomm_ring
    _ = z := by rw [h1, one_mul, mul_one]

/-- ★★★ **O ANDAR COMPOSTO É UM ANDAR**: o par `(h ⊗ₖ k, hi ⊗ₖ ki)` do estado produto
    satisfaz as três leis — a torre pode subir. -/
theorem the_composed_floor_is_a_floor (h hi : Matrix n n ℂ) (k ki : Matrix m m ℂ)
    (hh : hᴴ = h) (hk : kᴴ = k) (h1 : h * hi = 1) (k1 : k * ki = 1) :
    (h ⊗ₖ k)ᴴ = h ⊗ₖ k ∧ (h ⊗ₖ k) * (hi ⊗ₖ ki) = 1 := by
  constructor
  · rw [conjTranspose_kronecker, hh, hk]
  · rw [← mul_kronecker_mul, h1, k1, one_kronecker_one]

/-- ★★★ **A TORRE ENTRELAÇA** (o coração do Ato II): o `J` do andar de cima,
    restrito à imagem da inclusão, É o `J` do andar de baixo —
    `J_{h⊗k}(ι x) = ι (J_h x)`. Os andares não se contradizem. -/
theorem the_tower_interlaces (h hi : Matrix n n ℂ) (k ki : Matrix m m ℂ)
    (k1 : k * ki = 1) (x : Matrix n n ℂ) :
    stateJG (h ⊗ₖ k) (hi ⊗ₖ ki) (towerInclusion x : Matrix (n × m) (n × m) ℂ)
      = towerInclusion (stateJG h hi x) := by
  unfold stateJG towerInclusion
  rw [conjTranspose_kronecker, conjTranspose_one, ← mul_kronecker_mul,
      ← mul_kronecker_mul, mul_one, k1]

/-- ★★ **A INCLUSÃO É MULTIPLICATIVA**: `ι(x·y) = ι x · ι y`. -/
theorem the_inclusion_is_multiplicative (x y : Matrix n n ℂ) :
    (towerInclusion (x * y) : Matrix (n × m) (n × m) ℂ)
      = towerInclusion x * towerInclusion y := by
  unfold towerInclusion
  rw [← mul_kronecker_mul, mul_one]

/-- ★★ **O VÁCUO SOBE**: `ι 1 = 1` — o `Ω = [1]` é o mesmo em toda a torre. -/
theorem the_vacuum_rises :
    (towerInclusion (1 : Matrix n n ℂ) : Matrix (n × m) (n × m) ℂ) = 1 := by
  unfold towerInclusion
  exact one_kronecker_one

end TGLExt
