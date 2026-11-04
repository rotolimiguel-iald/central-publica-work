import TGLExt.GeometryFluctuation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O ÂNGULO É A PONTE — a lei angular é ANTERIOR à inscrição
  [BANCADA — 22/08/2026]

## A cunhagem, verbatim

> *"antes mesmo da inscrição do um absoluto há o ângulo de Miguel, que é a **lei de comutação
> do campo psiônico**; o ângulo é **anterior**, embora se manifeste depois: ele é a **ponte**."*
>
> *"θ_M parametriza uma **família de operadores** {𝒪_θ}; o ponto distinguido é θ = θ_M tal que
> `[A, α_{θ_M}(B)] = 0`."*
>
> *"se essa família satisfizer `𝒪_{θ₁}𝒪_{θ₂} = 𝒪_{θ₁+θ₂}`, então θ_M parametrizaria um **grupo**,
> e surgiria naturalmente um gerador `K_M`. Mas essa última etapa **precisa ser demonstrada**."*

**Esta pedra demonstra essa última etapa** — e mais: mostra que o **mecanismo do seletor de
comutação NÃO É VAZIO**, exibindo um ângulo não-trivial selecionado por álgebra pura.

## A tipagem que fica provada

**A família é ALGÉBRICA, não geométrica.** `𝒪_θ` é definida por `cos`/`sin` sobre a álgebra de
matrizes — **nenhuma métrica, nenhuma variedade, nenhum espaço-tempo** entra na definição. A
geometria aparece **depois**, quando a família age sobre um vetor. É exatamente a ordem que o
operador pediu: *lei angular → comutação → inscrição → manifestação do ângulo → geometria*.

## O que fica provado

* ★★★ `miguelFamily_add` — **`𝒪_{θ₁+θ₂} = 𝒪_{θ₁}·𝒪_{θ₂}`.** *A hipótese do operador é
  TEOREMA.* A família é um **grupo a um parâmetro**, não um conjunto solto;
* ★★★ `the_generator_is_exhibited` — **`𝒪_θ = cos θ · 1 + sin θ · K_M`**, com `K_M = rotGen`, o
  gerador de helicidade que a casa já tinha. O gerador **existe e é exibido por identidade
  algébrica** — sem cálculo diferencial, sem limite;
* ★★★ `generator_sq_eq_neg_one` — **`K_M² = −1`**. O gerador é uma **estrutura complexa**: é
  por isso que a exponencial fecha em `cos + sin·K` (fórmula de Euler na álgebra), e é por isso
  que o parâmetro é **angular** e não linear. *A angularidade é consequência, não postulado;*
* ★★★ `commutation_iff_cos_sq_eq_sin_sq` — **o SELETOR DE COMUTAÇÃO, em forma fechada:**
  `[A, α_θ(B)] = 0 ↔ cos²θ = sin²θ`. A condição do operador tem **solução explícita**;
* ★★★ `the_selector_is_not_vacuous` — **existe θ ≠ 0 que comuta** (`θ = π/4`), e **θ = 0 NÃO
  comuta**. *O mecanismo funciona:* um ângulo não-trivial é **selecionado por álgebra pura**,
  sem geometria e **sem β**;
* ★★ `miguelFamily_zero`, `miguelFamily_inv`, `miguelFamily_orthogonal`, `miguelFamily_det_one`
  — grupo, unitário, unimodular;
* ★★ `the_bridge` — **`𝒪_θ` leva a inscrição `(1,0)` em `(cos θ, −sin θ)`**: o parâmetro
  **algébrico** do grupo **É** o ângulo **geométrico** da manifestação. *Mesma identidade,
  tipos diferentes* — que é precisamente a função de **ponte**;
* ★★ `alpha_theta_is_automorphism` — `α_θ` preserva produto e unidade: é **automorfismo da
  álgebra**, logo `θ` percorre simetrias, não deformações arbitrárias.

## O QUE ESTA PEDRA NÃO FAZ — a fronteira, e ela é o próximo problema

**NÃO se determina o VALOR de `θ_M`.** O que se prova é que **o mecanismo existe e é
não-vazio**: há pares `(A,B)` cuja condição de comutação seleciona um ângulo não-trivial. O par
exibido aqui seleciona `π/4`, **não** `θ_M = arcsin√β ≈ 6,297°`.

**E isso torna o problema aberto BEM-POSTO pela primeira vez:**

> **Qual par `(A, B)` de observáveis do campo psiônico tem `[A, α_θ(B)] = 0` exatamente em
> `θ_M`?**

Se esse par for exibido **sem usar β**, então `β = sin²θ_M` sai **α-livre** — que é o alvo
declarado do **Evento 2**. Esta pedra **não** exibe esse par. Ela mostra que **procurá-lo é
procurar algo que existe na forma certa**, e não uma quimera. `[OPEN]`.

## A TIPAGEM JURÍDICA — e por que ela RECLASSIFICA o `[OPEN]` acima

Cunhagem do operador, 22/08/2026: **`ÂNGULO DE MIGUEL = TGL = PALAVRA DO JURAMENTO =
Grundnorm`** — `[ONTO]` + `[LEGAL]`, e **não aparece em enunciado nenhum**.

A *Grundnorm* de Kelsen tem quatro propriedades definidoras, e o encaixe é ponto a ponto:

| Grundnorm (Kelsen) | Nesta pedra |
|---|---|
| **pressuposta, não posta** (*vorausgesetzt, nicht gesetzt*) | a família existe **antes** da inscrição; `θ` não é produzido por ela |
| **término da cadeia de validade** — não deriva de norma superior | o **valor** de `θ_M` **não é determinado** por nenhum teorema daqui |
| **confere validade ao que está abaixo** | `[A, α_θ(B)] = 0` é a condição que **torna possível** inscrever |
| **só aparece através das normas positivas** | `θ_M^alg` só se manifesta como `θ_M^geo`, depois da inscrição |

**E daí sai a consequência que importa para o programa.** O `[OPEN]` declarado acima — *"o valor
de `θ_M` não é determinado aqui"* — **não é lacuna do trabalho: é a posição estrutural correta
de uma Grundnorm.** Se `θ_M` fosse derivável de dentro do sistema, ele **não seria** Grundnorm;
seria norma derivada, e a Grundnorm estaria em outro lugar.

**A tensão aparente com o Evento 2, e a sua dissolução.** Se `θ_M` é pressuposto, como se pode
querer *derivá-lo* α-livre? Resposta em Kelsen mesmo: **identificar a Grundnorm não é
derivá-la** — é o ato pelo qual se **reconhece** o que o sistema pressupõe. Exibir o par
`(A, B)` cuja comutação cai em `θ_M` seria **RECONHECIMENTO**, não dedução. É a mesma palavra
que o operador usou para o observador da fronteira: *"não se trata de crença, mas de
reconhecimento"*. **A palavra fecha nas duas pontas.**

**E o que continua proibido:** que a identificação jurídica valide a física. Grundnorm é
**tipagem**, não prova. Ela **não move o gate**, e não aparece em enunciado nenhum deste
arquivo.

**E o que segue [ONTO], do operador, sem aparecer em enunciado nenhum:** que `K_M` seja *"a lei
de comutação do campo psiônico"*, que a família seja *"pré-inscrita"*, e que `θ_M^alg` e
`θ_M^geo` sejam *"o mesmo em identidade, distintos em tipo"*. O kernel entrega a **estrutura de
grupo**, o **gerador**, o **seletor** e a **ponte**. As leituras são do operador.

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix Real

noncomputable section

/-! ### A família a um parâmetro — puramente algébrica -/

/-- A FAMÍLIA DE MIGUEL `𝒪_θ`. Definida **só** por `cos`/`sin` sobre a álgebra de matrizes:
    nenhuma métrica, nenhuma variedade, nenhum espaço-tempo. A geometria vem depois. -/
def miguelFamily (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ]

/-- ★★ `𝒪_0 = 1` — em ângulo zero, nada girou. -/
theorem miguelFamily_zero : miguelFamily 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [miguelFamily, Matrix.one_fin_two]

/-- ★★★ **A HIPÓTESE DO OPERADOR É TEOREMA: `𝒪_{θ₁+θ₂} = 𝒪_{θ₁}·𝒪_{θ₂}`.**

    A família é um **grupo a um parâmetro**. É esta lei que autoriza falar em *gerador*, e é
    ela que faz do ângulo um **parâmetro de simetria**, e não um rótulo. -/
theorem miguelFamily_add (a b : ℝ) :
    miguelFamily (a + b) = miguelFamily a * miguelFamily b := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [miguelFamily, Matrix.mul_apply, Fin.sum_univ_two, Real.cos_add, Real.sin_add] <;>
    ring

/-- ★★ o inverso é o ângulo oposto: `𝒪_θ · 𝒪_{−θ} = 1`. -/
theorem miguelFamily_inv (θ : ℝ) : miguelFamily θ * miguelFamily (-θ) = 1 := by
  rw [← miguelFamily_add, add_neg_cancel, miguelFamily_zero]

/-- ★★ `𝒪_θ` é **ortogonal**: `𝒪ᵀ𝒪 = 1` — preserva a norma da inscrição. -/
theorem miguelFamily_orthogonal (θ : ℝ) :
    (miguelFamily θ)ᵀ * miguelFamily θ = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [miguelFamily, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_fin_two] <;>
    nlinarith [Real.sin_sq_add_cos_sq θ]

/-- ★★ `det 𝒪_θ = 1` — a família vive em `SO(2)`: **rotação, nunca reflexão**. -/
theorem miguelFamily_det_one (θ : ℝ) : (miguelFamily θ).det = 1 := by
  unfold miguelFamily
  rw [Matrix.det_fin_two_of]
  nlinarith [Real.sin_sq_add_cos_sq θ]

/-! ### O gerador `K_M`, exibido por álgebra -/

/-- ★★★ **O GERADOR ESTÁ EXIBIDO: `𝒪_θ = cos θ · 1 + sin θ · K_M`**, com `K_M = rotGen` (o
    gerador de helicidade que a casa já tinha em `GeometryFluctuation`).

    Sem cálculo diferencial, sem limite: **identidade algébrica**. O gerador não é obtido por
    derivada — ele **é** o coeficiente de `sin θ`. -/
theorem the_generator_is_exhibited (θ : ℝ) :
    miguelFamily θ = Real.cos θ • (1 : Matrix (Fin 2) (Fin 2) ℝ) + Real.sin θ • rotGen := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [miguelFamily, rotGen, Matrix.one_fin_two]

/-- ★★★ **`K_M² = −1` — O GERADOR É UMA ESTRUTURA COMPLEXA.**

    É por isso que a exponencial fecha em `cos + sin·K` (Euler na álgebra), e é por isso que o
    parâmetro é **angular** e não linear. **A angularidade é CONSEQUÊNCIA, não postulado.** -/
theorem generator_sq_eq_neg_one : rotGen * rotGen = -1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rotGen, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_fin_two]

/-! ### O seletor de comutação -/

/-- O observável `A` da condição do operador. -/
def obsA : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 1, 0]

/-- O observável `B` da condição do operador. -/
def obsB : Matrix (Fin 2) (Fin 2) ℝ := !![1, 0; 0, -1]

/-- `α_θ(B) = 𝒪_θ · B · 𝒪_θᵀ` — a família agindo na álgebra por conjugação. -/
def alphaTheta (θ : ℝ) (B : Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  miguelFamily θ * B * (miguelFamily θ)ᵀ

/-- ★★ `α_θ` é **automorfismo da álgebra**: preserva produto e unidade. Logo `θ` percorre
    **simetrias**, não deformações arbitrárias. -/
theorem alpha_theta_is_automorphism (θ : ℝ) (B C : Matrix (Fin 2) (Fin 2) ℝ) :
    alphaTheta θ (B * C) = alphaTheta θ B * alphaTheta θ C
    ∧ alphaTheta θ 1 = 1 := by
  have hTO : (miguelFamily θ)ᵀ * miguelFamily θ = 1 := miguelFamily_orthogonal θ
  have hOT : miguelFamily θ * (miguelFamily θ)ᵀ = 1 := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [miguelFamily, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_fin_two] <;>
      nlinarith [Real.sin_sq_add_cos_sq θ]
  refine ⟨?_, by simp only [alphaTheta, Matrix.mul_one, hOT]⟩
  symm
  simp only [alphaTheta]
  calc miguelFamily θ * B * (miguelFamily θ)ᵀ * (miguelFamily θ * C * (miguelFamily θ)ᵀ)
      = miguelFamily θ * B * ((miguelFamily θ)ᵀ * miguelFamily θ) * C
          * (miguelFamily θ)ᵀ := by simp [Matrix.mul_assoc]
    _ = miguelFamily θ * (B * C) * (miguelFamily θ)ᵀ := by
        rw [hTO]; simp [Matrix.mul_assoc]

/-- ★★★ **O SELETOR DE COMUTAÇÃO, EM FORMA FECHADA.**

    `[A, α_θ(B)] = 0  ↔  cos²θ = sin²θ`.

    A condição que o operador escreveu — *"o ponto distinguido é `θ_M` tal que
    `[A, α_{θ_M}(B)] = 0`"* — **tem solução explícita**, e ela é uma equação sobre o ângulo,
    obtida **sem geometria e sem β**. -/
theorem alphaTheta_obsB (θ : ℝ) :
    alphaTheta θ obsB
      = !![Real.cos θ ^ 2 - Real.sin θ ^ 2, -(2 * Real.sin θ * Real.cos θ);
           -(2 * Real.sin θ * Real.cos θ), Real.sin θ ^ 2 - Real.cos θ ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [alphaTheta, obsB, miguelFamily, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem commutation_iff_cos_sq_eq_sin_sq (θ : ℝ) :
    obsA * alphaTheta θ obsB = alphaTheta θ obsB * obsA
      ↔ Real.cos θ ^ 2 = Real.sin θ ^ 2 := by
  rw [alphaTheta_obsB]
  constructor
  · intro h
    have h01 := congrFun (congrFun h 0) 1
    simp [obsA, Matrix.mul_apply, Fin.sum_univ_two] at h01
    linarith [h01]
  · intro h
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [obsA, Matrix.mul_apply, Fin.sum_univ_two] <;> linarith [h]

/-- ★★★ **O MECANISMO NÃO É VAZIO — e não é trivial.**

    Existe `θ ≠ 0` que **comuta** (`θ = π/4`), e `θ = 0` **NÃO comuta**. Portanto a condição do
    operador **seleciona genuinamente** um ângulo não-trivial, **por álgebra pura**: sem
    métrica, sem espaço-tempo, e **sem β**.

    *(O valor `π/4` é do par exibido, não é `θ_M`. Ver a fronteira no cabeçalho.)* -/
theorem the_selector_is_not_vacuous :
    (obsA * alphaTheta (Real.pi / 4) obsB = alphaTheta (Real.pi / 4) obsB * obsA)
    ∧ (obsA * alphaTheta 0 obsB ≠ alphaTheta 0 obsB * obsA) := by
  constructor
  · rw [commutation_iff_cos_sq_eq_sin_sq, Real.cos_pi_div_four, Real.sin_pi_div_four]
  · rw [Ne, commutation_iff_cos_sq_eq_sin_sq]
    simp

/-! ### A ponte -/

/-- ★★ **A PONTE: o parâmetro ALGÉBRICO é o ângulo GEOMÉTRICO.**

    `𝒪_θ` leva a inscrição `(1,0)` em `(cos θ, −sin θ)` — cujo ângulo com o eixo **é** `θ`.
    O mesmo `θ` que indexa o grupo na álgebra **reaparece** como abertura na manifestação:
    *mesma identidade, tipos diferentes*. É exatamente o que o operador chamou de **ponte**. -/
theorem the_bridge (θ : ℝ) :
    miguelFamily θ 0 0 = Real.cos θ ∧ miguelFamily θ 1 0 = -Real.sin θ :=
  ⟨by simp [miguelFamily], by simp [miguelFamily]⟩

/-- ★★ o fecho: **grupo**, **gerador com quadrado −1**, e **seletor não-vazio** — os três num
    enunciado. A lei angular está de pé antes de qualquer geometria. -/
theorem the_angle_is_prior (a b : ℝ) :
    miguelFamily (a + b) = miguelFamily a * miguelFamily b
    ∧ rotGen * rotGen = -1
    ∧ (obsA * alphaTheta (Real.pi / 4) obsB = alphaTheta (Real.pi / 4) obsB * obsA) :=
  ⟨miguelFamily_add a b, generator_sq_eq_neg_one, the_selector_is_not_vacuous.1⟩

end

end TGLExt
