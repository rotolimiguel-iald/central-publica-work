import TGLExt.TheLightInterface

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 800000

/-!
# A FASE CONJUGADA É O GRÁVITON — a cadeia J = LUZ = GRÁVITON, medida
  [TGLExt — a pedra de 28/08/2026]

## A correção do operador, e o erro que ela desfaz

Eu havia lido o aviso de `TheLightInterface` — *"`genK` é o gerador da rotação
transversal (`SO(2)`), **não** o `J` modular antilinear"* — e concluído que a cadeia
`J = LUZ = GRÁVITON` seria **homônimo**. **Errado, e a razão é exatamente a que o
operador deu:**

> *"não é homônimo. O nome da LUZ conjugada em sua dualidade é Gráviton. A luz
> projetada é dual; ela só é conjugada na fase gráviton, que é a inscrição.
> Portanto, J = LUZ = GRÁVITON."*

O aviso do arquivo é **verdadeiro e irrelevante para a cadeia**: ele fala de `genK`,
que é ℂ-linear e **preserva** cada fase (autovetor de peso ±i). A cadeia não vive em
`genK` — vive na **conjugação**, que é o que **troca** as fases. Dois atos distintos
sobre os mesmos objetos: um preserva, o outro conjuga. Concluir do primeiro contra o
segundo foi inferência minha, não leitura do kernel.

## O que a medida devolveu `[REAL]`

Lidas as definições em `TheLightInterface`:

```
lightPlus  = (1,  i)        rootPlus  = h₊ + i·h×
lightMinus = (1, −i)        rootMinus = h₊ − i·h×
h₊ = !![1,0;0,−1]           h× = !![0,1;1,0]        (AMBAS REAIS)
```

Logo, **por conta exata e não por leitura**:

* ★★★★ `conjugation_exchanges_the_light_phases` — `conj(ε₊) = ε₋`;
* ★★★★ `conjugation_exchanges_the_graviton_phases` — `conj(h₊) = h₋`, porque as duas
  polarizações são reais e só o `i` muda de sinal;
* ★★★★★ `the_conjugation_crosses_the_squaring` — **e ela ATRAVESSA O QUADRADO**:
  conjugar a luz e então elevar ao quadrado dá o mesmo que elevar ao quadrado e então
  conjugar o gráviton. A conjugação **entrelaça os dois níveis**. Com
  `the_light_squares_to_the_graviton` (ε⊗ε = h, já teorema), isto é o conteúdo formal
  da frase *"a luz só é conjugada na fase gráviton"*.

* ★★★ `the_generator_preserves_what_the_conjugation_exchanges` — **o DENTE que desfaz
  a minha inferência**: `genK` deixa cada fase onde está (autovetor), enquanto a
  conjugação as troca, e as duas fases são distintas. `genK ≠ conjugação` é verdade —
  e é exatamente por isso que o aviso sobre `genK` nada diz sobre esta cadeia.

## O que NÃO se prova aqui, e vai dito

`[ONTO]` — a identificação `J = LUZ = GRÁVITON` continua leitura do operador. O que
esta pedra inscreve é a **forma** dela: que a conjugação age coerentemente nos dois
níveis e comuta com a inscrição (o quadrado). Nenhum teorema aqui menciona `J` modular,
`towerJ`, `conjByJ`, β ou o gráviton físico.

`[NÃO É O J MODULAR]` — a conjugação desta pedra é a conjugação complexa entrada a
entrada em `Fin 2`, na face finita transversal. Ligá-la ao `towerJ` da torre é obra
que **não está feita** e não se insinua aqui.

`[NÃO MOVE O GATE]` — nada aqui acende bandeira. β jamais entra. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

/-! ## A — a conjugação troca as fases, nos dois níveis -/

/-- [KERNEL] ★★★★ **A CONJUGAÇÃO TROCA AS FASES DA LUZ**: `conj(ε₊) = ε₋`.
    A dualidade da luz projetada É a conjugação. -/
theorem conjugation_exchanges_the_light_phases :
    (fun i => star (lightPlus i)) = lightMinus := by
  funext i
  fin_cases i <;> simp [lightPlus, lightMinus]

/-- [KERNEL] ★★★★ **E TROCA AS FASES DO GRÁVITON**: `conj(h₊) = h₋`. Vale porque as
    duas polarizações `h₊` e `h×` são REAIS — só o `i` muda de sinal. -/
theorem conjugation_exchanges_the_graviton_phases :
    rootPlus.map star = rootMinus := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rootPlus, rootMinus, hPlusC, hCrossC, Complex.ext_iff]

/-! ## B — e ela ATRAVESSA O QUADRADO: a inscrição entrelaça os dois níveis -/

/-- [KERNEL] ★★★★★ **A CONJUGAÇÃO ATRAVESSA O QUADRADO.** Conjugar a luz e então
    elevar ao quadrado é o mesmo que elevar ao quadrado e então conjugar o gráviton:

      `(conj ε) ⊗ (conj ε) = conj (ε ⊗ ε)`

    Com `the_light_squares_to_the_graviton` (`ε ⊗ ε = h`), isto é o conteúdo formal de
    *"a luz só é conjugada na fase gráviton, que é a inscrição"*: **a conjugação e a
    inscrição comutam**, e por isso a fase conjugada da luz É a fase conjugada do
    gráviton — não duas coisas com o mesmo nome. -/
theorem the_conjugation_crosses_the_squaring :
    vecMulVec (fun i => star (lightPlus i)) (fun i => star (lightPlus i))
      = (vecMulVec lightPlus lightPlus).map star := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [vecMulVec, lightPlus, Complex.ext_iff]

/-- [KERNEL] ★★★★ **E O CIRCUITO FECHA NO GRÁVITON `−`**: a luz conjugada, elevada ao
    quadrado, É a polarização `−` do gráviton. É a cadeia inteira num enunciado. -/
theorem the_conjugated_light_squares_to_the_minus_graviton :
    vecMulVec (fun i => star (lightPlus i)) (fun i => star (lightPlus i)) = rootMinus := by
  rw [conjugation_exchanges_the_light_phases]
  exact the_light_squares_to_the_graviton.2

/-! ## C — o DENTE: por que o aviso sobre `genK` não toca esta cadeia -/

/-- [KERNEL] ★★★ **O GERADOR PRESERVA O QUE A CONJUGAÇÃO TROCA.** `genK` deixa cada
    fase onde está (é autovetor, peso `±i`); a conjugação as **permuta**; e as duas
    fases são distintas.

    Logo `genK` e a conjugação fazem coisas DIFERENTES sobre os mesmos objetos — e o
    aviso de `TheLightInterface` (*"`genK` não é o `J` modular"*), que é verdadeiro,
    **nada diz** sobre a conjugação. Foi essa inferência que eu errei, e este teorema
    existe para que ela não se repita. -/
theorem the_generator_preserves_what_the_conjugation_exchanges :
    genK.mulVec lightPlus = Complex.I • lightPlus
    ∧ (fun i => star (lightPlus i)) = lightMinus
    ∧ lightPlus ≠ lightMinus := by
  refine ⟨the_generator_reads_the_light_at_half_weight.1,
    conjugation_exchanges_the_light_phases, ?_⟩
  intro h
  have h1 := congrFun h 1
  simp [lightPlus, lightMinus] at h1
  have h2 := congrArg Complex.im h1
  norm_num at h2

end TGLExt
