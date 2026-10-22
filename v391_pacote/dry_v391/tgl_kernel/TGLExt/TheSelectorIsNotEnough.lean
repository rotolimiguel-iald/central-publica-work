import TGLExt.TheAngleIsTheBridge

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O SELETOR SOZINHO NÃO PREDIZ — a armadilha do par livre
  [BANCADA — 22/08/2026; **correção AO LADO** de `TheAngleIsTheBridge`, nunca por cima]

## Por que esta pedra existe

`TheAngleIsTheBridge` provou que o seletor de comutação **não é vazio**: existe `θ ≠ 0` que
comuta, selecionado por álgebra pura. E declarou o problema aberto como *"bem-posto"*:
**qual par `(A,B)` comuta exatamente em `θ_M`?**

**Esta pedra mostra que aquela formulação, sozinha, é FRACA DEMAIS** — e por exatamente a mesma
doença que matou o T08 no mesmo dia: **um grau de liberdade escondido, que faz o "acerto" ser
escolha e não predição.**

A lição do T08, em uma frase: *"pelo teorema do valor intermediário sempre existe `P_F` que dá α
exatamente; mas o canto que acerta traz α embutido na própria definição."* **Aqui é idêntico:
sempre existe um par que comuta em `θ_M`; mas o par que acerta traz `θ_M` embutido.**

## O que fica provado

* ★★★ `the_commutator_closed_form` — **forma fechada exata**:

      [α_φ(B), α_θ(B)] = 2·sin(2θ − 2φ) · Ω,   Ω = !![0,−1; 1,0]

  O comutador depende **SÓ da diferença `θ − φ`**;
* ★★★ `the_commuting_angle_is_a_free_dial` — consequência imediata: **para TODO `θ` existe `φ`
  (a saber, `φ = θ`) que faz a comutação cair exatamente ali.** O ângulo de comutação é um
  **mostrador livre**, não uma predição;
* ★★ `commutation_iff_sin_vanishes` — e o conjunto onde comuta é exatamente
  `{φ : sin(2θ − 2φ) = 0}`: um retículo, não um ponto distinguido.

## A CORREÇÃO — como o problema aberto tem de ser reformulado

**FORMULAÇÃO FRACA (a de `TheAngleIsTheBridge`, e ela está incompleta):**
> *"qual par `(A,B)` tem `[A, α_θ(B)] = 0` exatamente em `θ_M`?"*

Fraca porque **a resposta é trivial e vazia**: tome `A := α_{θ_M}(B)`. Acerta sempre, e não diz
nada — `θ_M` entrou pela porta dos fundos, na construção de `A`.

**FORMULAÇÃO FORTE (a que vale, e é a que fica registrada):**
> **O par `(A,B)` tem de ser DADO pela teoria — os observáveis efetivos do campo psiônico —
> e não escolhido para acertar. E a demonstração de que é dado tem de ser anterior, e
> independente, do cálculo do ângulo em que ele comuta.**

Operacionalmente, herdando a regra que nasceu no T08 (**CONSTÂNCIA ANTES DO VALOR**):

1. `A` e `B` **declarados e pré-registrados** a partir da estrutura da teoria (não do alvo);
2. o ângulo de comutação **calculado depois**, com o hash do pré-registro já fixado;
3. e **estabilidade** exigida: o mesmo par, em faces de dimensão diferente, tem de dar o mesmo
   ângulo. Um par que só funciona numa dimensão é o `P_F` do T08 outra vez.

## O ALCANCE — e por que isto NÃO desfaz a pedra anterior

**Não desfaz.** O que `TheAngleIsTheBridge` prova continua de pé, inteiro: a família **é** grupo,
o gerador **está** exibido, `K_M² = −1`, e o seletor **não é** vazio. **O que esta pedra
acrescenta é a fronteira que faltava:** *não-vazio* não é *predizente*. Na face 2×2 o seletor é
**universal** — atinge qualquer ângulo —, logo **o conteúdo preditivo não pode vir do seletor:
tem de vir do par.**

E isso é **notícia boa disfarçada de má**: o problema aberto deixou de ser *"procurar um par"*
(o que sempre acha um) e passou a ser *"derivar o par"* — que é uma pergunta com resposta certa
ou errada. **A ambiguidade saiu.**

`[ONTO]`/`[LEGAL]` do operador, fora de todo enunciado: a leitura Grundnorm continua valendo —
e ganha precisão aqui, porque em Kelsen a norma fundamental **é reconhecida na estrutura, não
escolhida por conveniência**. Escolher o par para acertar seria exatamente **pôr** a Grundnorm,
que é o que Kelsen proíbe.

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix Real

noncomputable section

/-- O gerador de rotação usado como base do comutador. -/
def omegaGen : Matrix (Fin 2) (Fin 2) ℝ := !![0, -1; 1, 0]

/-- ★★★ **A FORMA FECHADA DO COMUTADOR.**

    `[α_φ(B), α_θ(B)] = 2·sin(2θ − 2φ)·Ω`

    O comutador depende **exclusivamente da diferença** `θ − φ`. É desta identidade que sai
    tudo o que esta pedra diz. -/
theorem the_commutator_closed_form (θ φ : ℝ) :
    alphaTheta φ obsB * alphaTheta θ obsB - alphaTheta θ obsB * alphaTheta φ obsB
      = (2 * Real.sin (2 * θ - 2 * φ)) • omegaGen := by
  rw [alphaTheta_obsB, alphaTheta_obsB, Real.sin_sub, Real.sin_two_mul, Real.sin_two_mul,
    Real.cos_two_mul', Real.cos_two_mul']
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, omegaGen] <;> ring

/-- ★★ **O CONJUNTO ONDE COMUTA É UM RETÍCULO, NÃO UM PONTO.**
    `[α_φ(B), α_θ(B)] = 0 ↔ sin(2θ − 2φ) = 0`. -/
theorem commutation_iff_sin_vanishes (θ φ : ℝ) :
    alphaTheta φ obsB * alphaTheta θ obsB = alphaTheta θ obsB * alphaTheta φ obsB
      ↔ Real.sin (2 * θ - 2 * φ) = 0 := by
  rw [← sub_eq_zero, the_commutator_closed_form]
  constructor
  · intro h
    have h10 := congrFun (congrFun h 1) 0
    simp [omegaGen] at h10
    linarith
  · intro h
    rw [h]
    simp

/-- ★★★ **O ÂNGULO DE COMUTAÇÃO É UM MOSTRADOR LIVRE.**

    Para **TODO** `θ` existe `φ` que faz a comutação cair exatamente ali — a saber, `φ = θ`.
    Logo **acertar `θ_M` não é predição enquanto o par for escolhido**: o par que acerta traz
    `θ_M` embutido, exatamente como o canto `P_F` do T08 trazia α embutido.

    *É por isso que o problema aberto tem de ser DERIVAR o par, não procurá-lo.* -/
theorem the_commuting_angle_is_a_free_dial :
    ∀ θ : ℝ, ∃ φ : ℝ,
      alphaTheta φ obsB * alphaTheta θ obsB = alphaTheta θ obsB * alphaTheta φ obsB := by
  intro θ
  refine ⟨θ, ?_⟩
  rw [commutation_iff_sin_vanishes]
  simp

end

end TGLExt
