import TGLExt.TheIALDInTheTowerActII

set_option autoImplicit false
set_option maxHeartbeats 1000000

/-!
# A IALD NA TORRE — ATO III, F1+F2: o produto interno GNS e a ANTIISOMETRIA de J
  [BANCADA — 26/08/2026 · marco M4 do DESENHO; item 4 da dívida com preço (v220)]

## O alicerce que faltava

Os Atos I e II construíram `J` no andar e provaram que os andares entrelaçam. Para
estender `J` ao COMPLETAMENTO (Ato III) é preciso, antes, que ele seja **isometria** —
e isometria pede o produto interno certo. O produto interno do ESTADO (GNS) é

    ⟨x, y⟩_h := tr(h² · xᴴ · y)          (ρ = h² é o estado do andar)

e o fato decisivo é que a conjugação torcida é **antiisométrica** nele:

    ⟨J x, J y⟩ = conj ⟨x, y⟩

É isso que autoriza `Completion.extend` na sub-pedra seguinte: uma aplicação
antilinear isométrica se estende ao completamento, e as identidades pontuais (a
involução, o vácuo J-fixo, a dualidade dos Atos I/II) viajam por densidade.

## ACHADO: o F1 JA ESTAVA LARGAMENTE PAGO nesta arvore

`TGLExt/GNSQuotient.lean` ja constroi, para a densidade da cadeia: a forma hermitiana,
o RADICAL como `Submodule`, o teorema de que o radical e IDEAL A ESQUERDA, a descida do
produto interno ao QUOCIENTE nas duas faces, e a acao esquerda bem-definida (o pre-fator
representado). Esta pedra NAO refaz nada disso: ela prova a face que faltava e que
nenhuma outra tinha -- **a ANTIISOMETRIA da conjugacao torcida** -- na forma geral,
parametrizada por `h` do andar, para compor com os Atos I/II. Os nomes aqui levam o
prefixo `tower` justamente para conviver com o `GNSQuotient` sem colidir.

## O que se prova

* ★★ `towerInner_conj_symm` — simetria conjugada `⟨x,y⟩ = conj ⟨y,x⟩`;
* ★★ `towerInner_add_right` / `towerInner_smul_right` — linearidade na 2ª entrada;
* ★★★ **`towerInner_stateJG_conj`** — **A ANTIISOMETRIA** `⟨Jx,Jy⟩ = conj⟨x,y⟩`;
* ★★ `towerInner_vacuum` — `⟨1,1⟩ = tr(h²)`: a norma do vácuo é o traço do estado — é 1
  exatamente quando o estado é normalizado (a face aritmética de `ω(I) = 1`).

β jamais entra. Sem sorry. Nada move o gate. Restam F3 (extensão ao completamento),
F4 (comutante em WH) e F5 (a instância do certificado v203).
-/

namespace TGLExt

open Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

/-- o produto interno GNS do estado do andar: `⟨x,y⟩ = tr(h²·xᴴ·y)`. -/
def towerInner (h x y : Matrix n n ℂ) : ℂ := (h ^ 2 * xᴴ * y).trace

theorem towerDensitySq_isHermitian (h : Matrix n n ℂ) (hherm : hᴴ = h) : (h ^ 2)ᴴ = h ^ 2 := by
  rw [pow_two, conjTranspose_mul, hherm, ← pow_two]

/-- ★★ **SIMETRIA CONJUGADA**: `⟨x,y⟩ = conj ⟨y,x⟩`. -/
theorem towerInner_conj_symm (h : Matrix n n ℂ) (hherm : hᴴ = h) (x y : Matrix n n ℂ) :
    towerInner h x y = star (towerInner h y x) := by
  unfold towerInner
  rw [← trace_conjTranspose]
  have e : (h ^ 2 * yᴴ * x)ᴴ = xᴴ * (y * h ^ 2) := by
    simp only [conjTranspose_mul, conjTranspose_conjTranspose, towerDensitySq_isHermitian h hherm]
  rw [e, trace_mul_comm]
  conv_rhs => rw [trace_mul_comm]
  rw [mul_assoc]

/-- ★★ linearidade na segunda entrada (soma). -/
theorem towerInner_add_right (h x y z : Matrix n n ℂ) :
    towerInner h x (y + z) = towerInner h x y + towerInner h x z := by
  unfold towerInner
  rw [Matrix.mul_add, trace_add]

/-- ★★ linearidade na segunda entrada (escalar). -/
theorem towerInner_smul_right (h x y : Matrix n n ℂ) (c : ℂ) :
    towerInner h x (c • y) = c * towerInner h x y := by
  unfold towerInner
  rw [Matrix.mul_smul, trace_smul, smul_eq_mul]

/-- ★★ **A NORMA DO VÁCUO É O TRAÇO DO ESTADO**: `⟨1,1⟩ = tr(h²)` — vale 1 exatamente
    quando o estado é normalizado: a face aritmética de `ω(I) = 1`. -/
theorem towerInner_vacuum (h : Matrix n n ℂ) :
    towerInner h (1 : Matrix n n ℂ) 1 = (h ^ 2).trace := by
  unfold towerInner
  rw [conjTranspose_one, mul_one, mul_one]

/-- ★★★ **A ANTIISOMETRIA DA CONJUGAÇÃO TORCIDA**: `⟨Jx, Jy⟩ = conj ⟨x,y⟩`.
    É este fato que autoriza a extensão ao completamento (Ato III). -/
theorem towerInner_stateJG_conj (h hi : Matrix n n ℂ) (hherm : hᴴ = h)
    (h1 : h * hi = 1) (h2 : hi * h = 1) (x y : Matrix n n ℂ) :
    towerInner h (stateJG h hi x) (stateJG h hi y) = star (towerInner h x y) := by
  have hhi : hiᴴ = hi := floor_inv_isHermitian h hi hherm h1
  have hJ : (stateJG h hi x)ᴴ = hi * x * h := by
    unfold stateJG
    simp only [conjTranspose_mul, hhi, hherm, conjTranspose_conjTranspose]
    noncomm_ring
  -- LADO ESQUERDO = tr(x · h² · yᴴ)
  have L : towerInner h (stateJG h hi x) (stateJG h hi y) = (x * (h * h) * yᴴ).trace := by
    unfold towerInner
    rw [hJ]
    unfold stateJG
    rw [pow_two]
    have s1 : h * h * (hi * x * h) * (h * yᴴ * hi)
        = (h * h * (hi * x * h) * (h * yᴴ)) * hi := by noncomm_ring
    rw [s1, trace_mul_comm]
    have s2 : hi * (h * h * (hi * x * h) * (h * yᴴ))
        = (hi * h) * ((h * hi) * x * (h * h) * yᴴ) := by noncomm_ring
    rw [s2, h1, h2, one_mul, one_mul]
  -- LADO DIREITO = tr(x · h² · yᴴ) TAMBÉM
  have R : star (towerInner h x y) = (x * (h * h) * yᴴ).trace := by
    unfold towerInner
    rw [← trace_conjTranspose]
    have e : (h ^ 2 * xᴴ * y)ᴴ = yᴴ * (x * (h * h)) := by
      simp only [conjTranspose_mul, conjTranspose_conjTranspose, towerDensitySq_isHermitian h hherm]
      rw [pow_two]
    rw [e, trace_mul_comm]
  rw [L, R]

end TGLExt
