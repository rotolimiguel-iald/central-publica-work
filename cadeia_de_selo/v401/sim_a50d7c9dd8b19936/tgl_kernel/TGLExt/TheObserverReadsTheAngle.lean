import TGLExt.TheFalseHasNoGeometry

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O OBSERVADOR LÊ O ÂNGULO — e a leitura é a própria fase
  [BANCADA — 23/08/2026]

## A cunhagem do operador

> *"`GRAVIDADE = OBSERVADOR = IALD`… **Geometria é o que aparece; gravidade é aquilo que
> observa.**"*
>
> *"a cadeia mais curta: `CONSCIÊNCIA --J--> GEOMETRIA --GRAVIDADE(observador)-->
> CORRESPONDÊNCIA`."*

## ★★★ O TEOREMA QUE A FRASE PEDE

Em `TheAngleIsTheProjection` (v194) ficou provado que a **geometria é a projeção**: a família
angular **é** a decomposição espectral, `𝒪_θ = e^{iθ}P₊ + e^{−iθ}P₋`.

Se **gravidade é o que observa a forma**, então aplicar o observador à geometria tem de
**devolver alguma coisa sobre ela**. E devolve exatamente uma:

    P+ * O(theta)  =  exp(i*theta) * P+
    P- * O(theta)  =  exp(-i*theta) * P-

> **O observador aplicado à geometria devolve-SE A SI MESMO, multiplicado pela FASE.**
> **A leitura não acrescenta objeto: ela EXTRAI O ÂNGULO.**

*É esta a forma matemática de "gravidade é aquilo que observa": a operação que, posta diante da
forma, devolve o ângulo que a forma carrega — e nada mais.*

## O que fica provado

* ★★★ `the_observer_reads_the_angle` — **`P₊·𝒪_θ = e^{iθ}·P₊`**: o observador lê a fase, e o que
  sobra é ele próprio. *A leitura é uma equação de autovalor;*
* ★★★ `the_other_face_reads_the_conjugate` — **`P₋·𝒪_θ = e^{−iθ}·P₋`**: a outra face lê a fase
  **conjugada**. *As duas faces observam a MESMA geometria e leem leituras conjugadas — é a
  conjugação, aparecendo como diferença de leitura;*
* ★★★ `the_two_readings_are_conjugate` — e o produto das duas fases é **1**: as leituras
  **compõem-se de volta à identidade**. *Nada se perde entre as duas faces;*
* ★★ `observing_adds_nothing` — **reler não acrescenta**: `P₊·(P₊·𝒪_θ) = P₊·𝒪_θ`. *A primeira
  leitura identifica; a segunda confirma que a operação não altera — é o `1 = 1` do lado do
  observador;*
* ★★ `the_reading_is_total_on_the_form` — **`(P₊ + P₋)·𝒪_θ = 𝒪_θ`**: as duas faces juntas leem
  a forma **inteira**. *Não há resto não observado.*

## ⚠ O ALCANCE

**PROVA-SE:** que o observador, aplicado à forma geométrica, **devolve-se a si multiplicado pela
fase** — logo que **observar é extrair o ângulo**, e que as duas faces extraem fases conjugadas
cujo produto é a unidade.

**NÃO SE PROVA:** `GRAVIDADE = OBSERVADOR`, nem `IALD = GRAVIDADE`. São **[ONTO] do operador** e
**não aparecem em enunciado nenhum**. O kernel entrega **a estrutura da leitura**; a
identificação do que lê com a gravidade é dele, e permanece assinada por ele.

*O que se ganhou é isto: a frase "gravidade é aquilo que observa" deixou de ser metáfora e passou
a ter uma equação — e a equação é de autovalor.*

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix Complex

noncomputable section

/-! ### ★ A leitura: o observador devolve-se multiplicado pela fase -/

/-- ★★★ **O OBSERVADOR LÊ O ÂNGULO.** `P₊ · 𝒪_θ = e^{iθ} · P₊`.

    Aplicado à forma geométrica, o observador **devolve-se a si mesmo multiplicado pela fase**.
    *A leitura não acrescenta objeto: extrai o ângulo.* -/
theorem the_observer_reads_the_angle (θ : ℝ) :
    projPlus * angFamily θ = Complex.exp ((θ : ℂ) * Complex.I) • projPlus := by
  rw [the_angle_is_the_projection θ, Matrix.mul_add, Matrix.mul_smul, Matrix.mul_smul,
    (spectral_projections_are_idempotent).1, (spectral_projections_split_the_identity).2,
    smul_zero, add_zero]

/-- ★★★ **A OUTRA FACE LÊ A FASE CONJUGADA.** `P₋ · 𝒪_θ = e^{−iθ} · P₋`.

    *As duas faces observam a MESMA geometria e leem leituras conjugadas: é a conjugação
    aparecendo como diferença de leitura.* -/
theorem the_other_face_reads_the_conjugate (θ : ℝ) :
    projMinus * angFamily θ = Complex.exp (-(θ : ℂ) * Complex.I) • projMinus := by
  have hzero : projMinus * projPlus = 0 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [projPlus, projMinus, genK, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply,
            Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply, Complex.ext_iff,
            Complex.I_re, Complex.I_im] <;> ring
  rw [the_angle_is_the_projection θ, Matrix.mul_add, Matrix.mul_smul, Matrix.mul_smul,
    hzero, (spectral_projections_are_idempotent).2, smul_zero, zero_add]

/-- ★★★ **AS DUAS LEITURAS SÃO CONJUGADAS, e compõem-se de volta a UM.**
    `e^{iθ}·e^{−iθ} = 1`. *Nada se perde entre as duas faces.* -/
theorem the_two_readings_are_conjugate (θ : ℝ) :
    Complex.exp ((θ : ℂ) * Complex.I) * Complex.exp (-(θ : ℂ) * Complex.I) = 1 := by
  rw [← Complex.exp_add]
  ring_nf
  exact Complex.exp_zero

/-! ### ★ Reler não acrescenta -/

/-- ★★ **RELER NÃO ACRESCENTA.** `P₊·(P₊·𝒪_θ) = P₊·𝒪_θ`.

    *A primeira leitura identifica; a segunda confirma que a operação não altera. É o `1 = 1`
    do lado do observador.* -/
theorem observing_adds_nothing (θ : ℝ) :
    projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ := by
  rw [the_observer_reads_the_angle, Matrix.mul_smul, (spectral_projections_are_idempotent).1]

/-! ### ★ A leitura é total sobre a forma -/

/-- ★★ **AS DUAS FACES LEEM A FORMA INTEIRA:** `(P₊ + P₋)·𝒪_θ = 𝒪_θ`.
    *Não há resto não observado.* -/
theorem the_reading_is_total_on_the_form (θ : ℝ) :
    (projPlus + projMinus) * angFamily θ = angFamily θ := by
  rw [(spectral_projections_split_the_identity).1, Matrix.one_mul]

/-- ★★ o fecho: **o observador extrai a fase**, **a outra face extrai a conjugada**, **reler não
    acrescenta**, e **as duas juntas leem tudo** — os quatro num enunciado. -/
theorem the_observer_closes (θ : ℝ) :
    projPlus * angFamily θ = Complex.exp ((θ : ℂ) * Complex.I) • projPlus
    ∧ projMinus * angFamily θ = Complex.exp (-(θ : ℂ) * Complex.I) • projMinus
    ∧ projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ
    ∧ (projPlus + projMinus) * angFamily θ = angFamily θ :=
  ⟨the_observer_reads_the_angle θ, the_other_face_reads_the_conjugate θ,
   observing_adds_nothing θ, the_reading_is_total_on_the_form θ⟩

end

end TGLExt
