import TGLExt.TheSelectorIsNotEnough

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O SELETOR PODE RECUSAR — onde o mecanismo deixa de ser mostrador e vira teste
  [BANCADA — 22/08/2026; o elo aberto, atacado pela raiz]

## O problema, como ficou depois de `TheSelectorIsNotEnough`

Aquela pedra provou que na face 2×2 **o ângulo de comutação é um mostrador livre**: para todo
`θ` existe um par que comuta exatamente ali. Um mecanismo que **só sabe dizer SIM** não prediz
coisa alguma. Ficou então a pergunta certa, e é ela que esta pedra responde:

> **ONDE o seletor deixa de ser universal?**

## A CONTAGEM QUE DÁ A RESPOSTA

`[A, α_θ(B)] = 0` com `A`, `B` simétricos: o comutador de dois simétricos é **antissimétrico**,
logo a equação tem **`dim so(n)` componentes independentes** — contra **uma** incógnita, `θ`:

| face | equações (`n(n−1)/2`) | incógnitas | veredito |
|---|---|---|---|
| **2×2** | **1** | 1 | *determinado* — **sempre há solução**: mostrador livre |
| **3×3** | **3** | 1 | **sobredeterminado por 2** — genericamente **NÃO há solução** |
| `n×n` | `n(n−1)/2` | 1 | sobredeterminação cresce como `n²` |

**É por isso que o 2×2 não podia predizer: não é defeito do mecanismo, é aritmética de
contagem.** Uma equação, uma incógnita: sempre resolve. **A partir de 3×3 o sistema é
sobredeterminado, e então dizer SIM passa a ser informação.**

## O que fica provado

* ★★★ `the_selector_can_refuse` — **existe par `(A,B)` em 3×3 que NÃO comuta para NENHUM `θ`.**
  Exibido e provado: as componentes `(2,0)` e `(2,1)` do comutador exigem
  **simultaneamente** `cos 2θ = 0` **e** `sin 2θ = 0`, o que a identidade pitagórica proíbe.
  ***Isto era IMPOSSÍVEL na face 2×2***;
* ★★★ `the_selector_can_accept` — e o contraste: outro par, na **mesma** face 3×3, comuta em
  `θ = π/4`. Logo a recusa **não é** rigidez do aparelho: é **discriminação**;
* ★★ `the_selector_is_a_genuine_test` — os dois num enunciado: **o mesmo mecanismo aceita um par
  e recusa outro.** *Um teste que não pode reprovar não é teste* — é a mesma régua fail-closed
  que rege a casa inteira, agora do lado do seletor.

## O QUE ISTO ENTREGA AO PROBLEMA ABERTO

**A forma forte exigia:** o par tem de ser **derivado** da estrutura, declarado **antes** do
cálculo do ângulo, e **estável em faces de dimensão diferente**. Esta pedra mostra **por que a
terceira exigência era a decisiva, e onde ela morde**:

> **Em dimensão ≥ 3 a existência de solução já é, ela própria, uma condição não-trivial sobre
> o par.** Um par genérico **não comuta em ângulo nenhum**. Portanto, se a teoria **fornecer**
> um par — os observáveis efetivos do campo psiônico — e esse par **admitir** um ângulo de
> comutação, esse ângulo **não foi escolhido: foi imposto por um sistema sobredeterminado**.

**É essa a diferença entre ajuste e predição, e ela agora tem lugar exato:** não está no
seletor nem no ângulo — **está na dimensão em que o par vive**.

## O QUE ESTA PEDRA NÃO FAZ — dito sem rodeio

**NÃO deriva `θ_M`.** Não exibe o par da teoria, não calcula ângulo nenhum, e **não afirma que
exista** par admissível dando `θ_M`. O que ela entrega é o **critério de admissibilidade** e a
**razão estrutural** de o problema ser bem-posto em dimensão ≥ 3 e mal-posto em 2×2.

O elo continua **`[OPEN]`**, e agora com endereço: **construir os observáveis efetivos do campo
psiônico numa face de dimensão ≥ 3, declará-los antes, e verificar se o sistema
sobredeterminado admite solução — e em que ângulo.** Se admitir, é predição. Se não admitir,
**é um negativo honesto e vale como resultado**, pela régua da casa.

`[ONTO]`/`[LEGAL]` do operador, fora de todo enunciado: a leitura Grundnorm ganha aqui a sua
forma mais precisa — **a norma fundamental é RECONHECIDA num sistema que podia recusá-la**.
Reconhecimento sem possibilidade de recusa seria imposição, não reconhecimento.

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix Real

noncomputable section

/-! ### A face 3×3: a família e os observáveis declarados -/

/-- A rotação no plano `xy` da face 3×3 — a mesma lei angular, uma dimensão acima. -/
def rot3 (θ : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![Real.cos θ, -Real.sin θ, 0; Real.sin θ, Real.cos θ, 0; 0, 0, 1]

/-- O transposto de `R_θ`, escrito por extenso (e provado ser o transposto logo abaixo) — para
    que o cálculo entrada a entrada feche sem depender da redução do `ᵀ` em `Fin 3`. -/
def rot3T (θ : ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![Real.cos θ, Real.sin θ, 0; -Real.sin θ, Real.cos θ, 0; 0, 0, 1]

/-- `rot3T` **é** o transposto de `rot3` — a definição por extenso não é atalho, é notação. -/
theorem rot3T_eq_transpose (θ : ℝ) : rot3T θ = (rot3 θ)ᵀ := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [rot3, rot3T]

/-- `α³_θ(B) = R_θ B R_θᵀ`. -/
def alpha3 (θ : ℝ) (B : Matrix (Fin 3) (Fin 3) ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  rot3 θ * B * rot3T θ

/-- O observável conjugado, no bloco `xy` (o mesmo `B` de sempre, uma dimensão acima). -/
def obsB3 : Matrix (Fin 3) (Fin 3) ℝ := !![1, 0, 0; 0, -1, 0; 0, 0, 0]

/-- O par que **RECUSA**: acopla `x` a `z` — **fora** do plano onde a família age. -/
def obsA3out : Matrix (Fin 3) (Fin 3) ℝ := !![0, 0, 1; 0, 0, 0; 1, 0, 0]

/-- O par que **ACEITA**: vive **dentro** do plano `xy`. -/
def obsA3in : Matrix (Fin 3) (Fin 3) ℝ := !![0, 1, 0; 1, 0, 0; 0, 0, 0]

/-! ### O teorema: o seletor pode dizer NÃO -/

/-- ★★ As duas componentes que carregam a sobredeterminação: `(2,0) = cos 2θ` e
    `(2,1) = sin 2θ`. É delas que sai a recusa. -/
theorem comm_out_entries (θ : ℝ) :
    (obsA3out * alpha3 θ obsB3 - alpha3 θ obsB3 * obsA3out) 2 0
        = Real.cos θ ^ 2 - Real.sin θ ^ 2
    ∧ (obsA3out * alpha3 θ obsB3 - alpha3 θ obsB3 * obsA3out) 2 1
        = 2 * Real.sin θ * Real.cos θ := by
  constructor <;>
    simp [obsA3out, obsB3, alpha3, rot3, rot3T, Matrix.mul_apply, Fin.sum_univ_three] <;> ring

/-- ★★★ **O SELETOR PODE RECUSAR.** Para o par `(A_out, B)`, o comutador **não se anula em
    ângulo nenhum**.

    A razão é a sobredeterminação: as componentes `(2,0)` e `(2,1)` valem `cos 2θ` e `sin 2θ`,
    e anular **as duas** exigiria `cos²θ = sin²θ` **e** `sin θ cos θ = 0` ao mesmo tempo — o que
    a identidade pitagórica proíbe.

    **Isto era impossível na face 2×2**, onde há uma só equação para uma só incógnita. -/
theorem the_selector_can_refuse (θ : ℝ) :
    obsA3out * alpha3 θ obsB3 ≠ alpha3 θ obsB3 * obsA3out := by
  intro h
  obtain ⟨e0, e1⟩ := comm_out_entries θ
  rw [sub_eq_zero_of_eq h] at e0 e1
  simp only [Matrix.zero_apply] at e0 e1
  have hp := Real.sin_sq_add_cos_sq θ
  have h1 : Real.cos θ ^ 2 = Real.sin θ ^ 2 := by linarith
  have h2 : Real.sin θ * Real.cos θ = 0 := by linarith
  have hs2 : Real.sin θ ^ 2 = 1 / 2 := by linarith
  rcases mul_eq_zero.mp h2 with hs | hc
  · rw [hs] at hs2; norm_num at hs2
  · have hz : Real.sin θ ^ 2 = 0 := by rw [← h1, hc]; ring
    rw [hz] at hs2; norm_num at hs2

/-- ★★ o critério para o par que vive **dentro** do plano: comuta exatamente onde
    `cos²θ = sin²θ`. -/
theorem commute_in_iff (θ : ℝ) :
    obsA3in * alpha3 θ obsB3 = alpha3 θ obsB3 * obsA3in
      ↔ Real.cos θ ^ 2 = Real.sin θ ^ 2 := by
  constructor
  · intro h
    have h01 := congrFun (congrFun h 0) 1
    simp [obsA3in, obsB3, alpha3, rot3, rot3T, Matrix.mul_apply, Fin.sum_univ_three] at h01
    nlinarith [h01]
  · intro h
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [obsA3in, obsB3, alpha3, rot3, rot3T, Matrix.mul_apply, Fin.sum_univ_three] <;>
      nlinarith [h]

/-- ★★★ **E PODE ACEITAR — na MESMA face.** O par `(A_in, B)`, que vive dentro do plano onde a
    família age, comuta em `θ = π/4`.

    Logo a recusa do teorema anterior **não é rigidez do aparelho**: é **discriminação**. -/
theorem the_selector_can_accept :
    obsA3in * alpha3 (Real.pi / 4) obsB3 = alpha3 (Real.pi / 4) obsB3 * obsA3in := by
  rw [commute_in_iff, Real.cos_pi_div_four, Real.sin_pi_div_four]

/-- ★★ **O SELETOR É TESTE GENUÍNO.** O mesmo mecanismo, na mesma face, **aceita um par e
    recusa outro**. *Um teste que não pode reprovar não é teste* — é a régua fail-closed da
    casa, agora do lado do seletor. -/
theorem the_selector_is_a_genuine_test :
    (obsA3in * alpha3 (Real.pi / 4) obsB3 = alpha3 (Real.pi / 4) obsB3 * obsA3in)
    ∧ (∀ θ : ℝ, obsA3out * alpha3 θ obsB3 ≠ alpha3 θ obsB3 * obsA3out) :=
  ⟨the_selector_can_accept, the_selector_can_refuse⟩

end

end TGLExt
