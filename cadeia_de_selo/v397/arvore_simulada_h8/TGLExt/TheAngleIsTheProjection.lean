import TGLExt.TheHorizonInvariance

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O ÂNGULO **É** A PROJEÇÃO — um gerador, três leituras
  [BANCADA — 23/08/2026]

## A cunhagem do operador

> *"`GEOMETRIA = CONSCIÊNCIA CONJUGADA = GRÁVITON = J = ÂNGULO = PROJEÇÃO`… não devemos escrever
> `J → projeção → geometria` como se fossem três objetos distintos. **O que muda é apenas ONDE a
> mesma identidade está sendo lida.**"*

## ⚠ A DELIMITAÇÃO QUE O ESCRIBA DEVE, antes de qualquer prova

**A identidade ESTRITA seria erro de tipo, e isso precisa ficar dito:** `J` é **antilinear**
(provado em `TheRecordOfJ`: `J_is_not_complex_linear`); `θ_M` é um **real**; uma projeção é
**idempotente linear** (`Π² = Π`), enquanto `J² = I`. **Não são o mesmo objeto.**

**Mas a leitura estrutural do operador é exata, e é ela que se prova aqui:** existe **UM
gerador** do qual o ângulo e a projeção se leem, e **eles não são construções sucessivas — são
a mesma decomposição escrita de dois modos**.

## ★★★ O TEOREMA

Seja `K` com **`K² = −1`** (o gerador de `TheAngleIsTheBridge`, cuja quadratura negativa é o que
torna o parâmetro *angular*). Então:

    P± := (1 ∓ i·K)/2       sao projecoes, ortogonais, e somam 1
    cos θ · 1 + sin θ · K   =   e^{iθ}·P₊  +  e^{−iθ}·P₋

> **A família angular É a decomposição espectral das projeções do seu próprio gerador.**
> Não há "primeiro o ângulo, depois a projeção": **há uma decomposição, lida por fase ou lida
> por peso.**

## O que fica provado

* ★★★ `generator_sq_neg_one` — **`K² = −1`**: o gerador é estrutura complexa (a raiz de tudo);
* ★★★ `spectral_projections_are_idempotent` — **`P±² = P±`**: são projeções de facto;
* ★★★ `spectral_projections_split_the_identity` — **`P₊ + P₋ = 1`** e **`P₊·P₋ = 0`**: partem a
  identidade, disjuntas e exaustivas;
* ★★★ **`the_angle_is_the_projection`** — **`cos θ·1 + sin θ·K = e^{iθ}P₊ + e^{−iθ}P₋`**.
  *A face angular e a face projetiva são a MESMA decomposição;*
* ★★ `the_generator_is_the_difference_of_the_faces` — **`K = i·(P₊ − P₋)`**: o gerador **é** a
  diferença das duas faces. *Ele não precede as projeções nem as sucede: é a assimetria delas;*
* ★★ `at_the_right_angle_the_family_is_the_generator` — em `θ = π/2` a família **é** o gerador:
  *o regime extremo devolve o próprio gerador, e é ali que* `TheEmptying` *põe o piso.*

## ⚠ O ALCANCE

**PROVA-SE:** que **ângulo e projeção são leituras de uma só decomposição**, gerada por `K²=−1`
— o que sustenta, na parte formalizável, o colapso que o operador enunciou.

**NÃO SE PROVA:** `J = gráviton`, `= geometria`, `= consciência conjugada`. Essas identificações
são **[ONTO] do operador** e **não aparecem em enunciado nenhum**. E em particular **não** se
prova que `J` (antilinear) seja igual a `K` (linear): são objetos distintos, e o kernel distingue.

*O que o kernel entrega é o núcleo demonstrável da intuição: onde o operador via cinco nomes, há
uma decomposição e cinco leituras dela — e duas dessas leituras (ângulo, projeção) ficam agora
provadamente idênticas.*

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix Complex

noncomputable section

/-- O GERADOR, sobre ℂ: a mesma matriz de `rotGen`, agora com escalares complexos para que as
    projeções espectrais existam. -/
def genK : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; -1, 0]

/-- A face `+`: `P₊ = (1 − i·K)/2`. -/
def projPlus : Matrix (Fin 2) (Fin 2) ℂ := (1 / 2 : ℂ) • (1 - Complex.I • genK)

/-- A face `−`: `P₋ = (1 + i·K)/2`. -/
def projMinus : Matrix (Fin 2) (Fin 2) ℂ := (1 / 2 : ℂ) • (1 + Complex.I • genK)

/-- a família angular, escrita por extenso. -/
def angFamily (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (Real.cos θ : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) + (Real.sin θ : ℂ) • genK

/-- tática desta pedra: tudo é conta entrada a entrada em `Fin 2`, com `I² = −1` à mão. -/
macro "duas" : tactic =>
  `(tactic| (ext i j; fin_cases i <;> fin_cases j <;>
      simp [genK, projPlus, projMinus, angFamily, Matrix.mul_apply, Fin.sum_univ_two,
            Matrix.one_apply, Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply,
            Complex.ext_iff, Complex.I_re, Complex.I_im] <;> ring))

/-! ### ★ A raiz: o gerador é estrutura complexa -/

/-- ★★★ **`K² = −1`.** É desta quadratura negativa que sai tudo o mais — inclusive o facto de o
    parâmetro ser **angular**, e não linear. -/
theorem generator_sq_neg_one : genK * genK = -1 := by duas

/-! ### ★ As projeções espectrais -/

/-- ★★★ **`P±` SÃO PROJEÇÕES:** `P±² = P±`. -/
theorem spectral_projections_are_idempotent :
    projPlus * projPlus = projPlus ∧ projMinus * projMinus = projMinus := by
  constructor <;> duas

/-- ★★★ **PARTEM A IDENTIDADE:** `P₊ + P₋ = 1` e `P₊·P₋ = 0` — disjuntas e exaustivas.
    *É a mesma forma de `TheDarkSplit`, agora na face espectral do gerador.* -/
theorem spectral_projections_split_the_identity :
    projPlus + projMinus = 1 ∧ projPlus * projMinus = 0 := by
  constructor <;> duas

/-! ### ★★★ O teorema: a família angular É a decomposição espectral -/

/-- ★★★ **O ÂNGULO É A PROJEÇÃO.**

    `cos θ · 1 + sin θ · K  =  e^{iθ}·P₊ + e^{−iθ}·P₋`

    A face **angular** e a face **projetiva** não são objetos sucessivos: são **a mesma
    decomposição**, uma lida por fase e a outra por peso. *É o núcleo demonstrável do colapso
    que o operador enunciou.* -/
theorem the_angle_is_the_projection (θ : ℝ) :
    angFamily θ
      = Complex.exp (θ * Complex.I) • projPlus
        + Complex.exp (-(θ : ℂ) * Complex.I) • projMinus := by
  have hp : Complex.exp ((θ : ℂ) * Complex.I)
      = (Real.cos θ : ℂ) + (Real.sin θ : ℂ) * Complex.I := by
    rw [Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin]
  have hm : Complex.exp (-(θ : ℂ) * Complex.I)
      = (Real.cos θ : ℂ) - (Real.sin θ : ℂ) * Complex.I := by
    have hneg : (-(θ : ℂ)) = ((-θ : ℝ) : ℂ) := by push_cast; ring
    rw [hneg, Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin,
      Real.cos_neg, Real.sin_neg]
    push_cast
    ring
  rw [hp, hm]
  duas

/-! ### ★ O gerador é a diferença das faces -/

/-- ★★ **`K = i·(P₊ − P₋)`** — o gerador **é** a diferença das duas faces.
    *Ele não precede as projeções nem as sucede: é a assimetria delas.* -/
theorem the_generator_is_the_difference_of_the_faces :
    genK = Complex.I • (projPlus - projMinus) := by duas

/-! ### ★ O regime extremo -/

/-- ★★ **NO ÂNGULO RETO A FAMÍLIA É O GERADOR:** `𝒪(π/2) = K`.
    *O regime extremo devolve o próprio gerador — e é ali que o piso de `TheEmptying` se põe.* -/
theorem at_the_right_angle_the_family_is_the_generator :
    angFamily (Real.pi / 2) = genK := by
  unfold angFamily
  rw [Real.cos_pi_div_two, Real.sin_pi_div_two]
  simp

/-- ★★ o fecho: **um gerador com `K² = −1`**, **duas projeções que partem a identidade**, e
    **a família angular igual à decomposição espectral delas** — os três num enunciado. -/
theorem one_generator_three_readings (θ : ℝ) :
    genK * genK = -1
    ∧ (projPlus + projMinus = 1 ∧ projPlus * projMinus = 0)
    ∧ angFamily θ = Complex.exp (θ * Complex.I) • projPlus
        + Complex.exp (-(θ : ℂ) * Complex.I) • projMinus :=
  ⟨generator_sq_neg_one, spectral_projections_split_the_identity,
   the_angle_is_the_projection θ⟩

end

end TGLExt
