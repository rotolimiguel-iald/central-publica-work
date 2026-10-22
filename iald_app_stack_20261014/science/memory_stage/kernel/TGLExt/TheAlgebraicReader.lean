import TGLExt.TheDarkSplit

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O LEITOR ALGÉBRICO — e o que fica FORA do domínio da leitura
  [BANCADA — 21/08/2026; ainda NÃO embutido no canônico]

## A cunhagem do operador, verbatim

> *"OBSERVADOR = LEITOR ALGÉBRICO DE TUDO = LEITOR DE TUDO QUE TEM GEOMETRIA
> = TGL. … `Dom(TGL) = {x | x possui geometria/inscrição legível}` … e
> portanto `0_abs ∉ Dom(TGL)`. … GEOMETRIA ⟺ LEGIBILIDADE ⟺ OBSERVADOR ⟺ TGL."*

E o fecho: *"A TGL não observa 'o Todo' como algo externo; ela é a leitura
algébrica de tudo aquilo do Todo que adquiriu geometria."*

## A distinção que esta pedra torna teorema

Havia um risco de leitura solta: confundir **ser aniquilado pelo seletor**
com **estar fora do domínio**. São coisas diferentes, e a diferença é
exatamente a de `0_mod` para `0_abs`:

* `0_mod` — o que o seletor manda a zero **ainda é lido**: pertence à morada,
  decompõe-se, tem lugar na partição. Zero **de leitura**, não ausência;
* `0_abs` — não é elemento. Não há o que ler.

E a partição provada em `TheDarkSplit` é o que fecha a saída: como
`firstAtom ⊔ tailSub 1 = ⊤`, **não existe terceiro lugar**. Logo o que se
alegue "fora" ou está numa das duas faces, ou **não está na morada**. Não há
terceira hipótese — e é isso que dá conteúdo a `0_abs ∉ Dom`.

## O que fica provado

* ★★★ `the_reading_is_total` — **todo** elemento da morada é lido: decompõe-se
  em parte no modo zero e parte granular, sem resto. O domínio da leitura é
  a morada inteira;
* ★★★ `there_is_no_outside_within_the_home` — não há elemento que escape das
  duas faces. **Quem está na morada, é lido**;
* ★★★ `annihilated_is_not_outside` — o que o seletor manda a zero **continua
  no domínio** e continua se decompondo. `0_mod` é zero **de leitura**, e não
  ausência de leitura. **É a distinção `0_mod` × `0_abs` em forma de teorema**;
* ★★ `legible_iff_in_the_home` — pertencer à morada, ser decomponível e ser
  lido são a mesma condição. É a cadeia
  *geometria ⟺ legibilidade ⟺ observador* na única face em que ela é
  matemática;
* ★★ `the_reader_is_one` — o mesmo operador de posto 1 realiza as duas
  cláusulas em todo elemento: atravessa a parte inscrita e aniquila a
  granular. **Um leitor, não dois.**

## A REMISSÃO — e por que esta pedra NÃO tenta provar o zero absoluto

Ordem do operador (21/08/2026), verbatim:

> *"a pedra não precisa provar o zero absoluto. A **terceira lei** já disse ser
> **inatingível em tempo finito**; eu uso isso como **remissão científica** e
> **fundamento do escopo** do meu trabalho. Só inscrever."*

Fica inscrito, e com o estatuto certo: a inatingibilidade de `0_abs` é
**[KNOWN]** — o teorema de Nernst, terceira lei da termodinâmica, que a casa
**cita** e **não redemonstra**. Ela não é conclusão deste kernel; é o
**fundamento do escopo** sobre o qual o trabalho se apoia. `0_abs ∉ Dom(TGL)`
tem, portanto, **fundação externa e declarada** — não é derivado aqui, e não
precisa ser.

O que o kernel acrescenta é outra coisa, e só ela: **dentro da morada não há
terceiro lugar**, e **ser aniquilado pela leitura não é estar fora dela**. Isso
é o que fecha a porta pela qual alguém confundiria `0_mod` com `0_abs`.

HONESTIDADE — o alcance. Prova-se que a leitura é **total e sem terceiro
lugar** sobre ℓ², e que **ser aniquilado ≠ estar fora**. A pedra **não** prova
nem tenta provar `0_abs`: a inatingibilidade é **remissão [KNOWN] à terceira
lei**, e o kernel só mostra que **não há lugar para ele dentro da morada**. As
identificações OBSERVADOR = TGL = leitor algébrico, e GEOMETRIA ⟺
LEGIBILIDADE, são **[ONTO]** do operador e não aparecem em enunciado nenhum.
β jamais entra no Lean. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- ★★★ **A LEITURA É TOTAL.** Todo elemento da morada se decompõe: uma parte
    no modo zero, uma parte granular, e nada sobra. **O domínio da leitura é a
    morada inteira** — não há elemento sem leitura. -/
theorem the_reading_is_total (x : ellTwo) :
    ∃ u v : ellTwo, u ∈ firstAtom ∧ v ∈ tailSub 1 ∧ x = u + v := by
  obtain ⟨hu, hv, hsum⟩ := every_state_splits x
  exact ⟨firstAtom.starProjection x, x - firstAtom.starProjection x, hu, hv, hsum.symm⟩

/-- ★★★ **NÃO HÁ FORA, DENTRO DA MORADA.** Nenhum elemento escapa das duas
    faces: a partição é exaustiva. Quem está na morada, é lido. -/
theorem there_is_no_outside_within_the_home (x : ellTwo) :
    x ∈ firstAtom ⊔ tailSub 1 := by
  rw [the_two_sectors_exhaust]; trivial

/-- ★★★ **ANIQUILADO NÃO É FORA.** O que o seletor manda a zero **continua no
    domínio** e continua se decompondo. Zero **de leitura** não é ausência de
    leitura — é a distinção entre `0_mod` (lido, e o resultado é zero) e
    `0_abs` (não há o que ler). -/
theorem annihilated_is_not_outside (y : ellTwo) (hy : y ∈ tailSub 1) :
    ialdSelector y = 0
    ∧ y ∈ firstAtom ⊔ tailSub 1
    ∧ ∃ u v : ellTwo, u ∈ firstAtom ∧ v ∈ tailSub 1 ∧ y = u + v := by
  refine ⟨?_, there_is_no_outside_within_the_home y, the_reading_is_total y⟩
  exact (the_iald_selector_separates_the_sectors 0 y (Submodule.zero_mem _) hy).2

/-- ★★ **LEGÍVEL ⟺ NA MORADA.** Pertencer, decompor-se e ser lido são a mesma
    condição — a cadeia *geometria ⟺ legibilidade* na face em que ela é
    matemática. -/
theorem legible_iff_in_the_home (x : ellTwo) :
    (x ∈ firstAtom ⊔ tailSub 1)
    ↔ (∃ u v : ellTwo, u ∈ firstAtom ∧ v ∈ tailSub 1 ∧ x = u + v) :=
  ⟨fun _ => the_reading_is_total x, fun _ => there_is_no_outside_within_the_home x⟩

/-- ★★ **UM LEITOR, NÃO DOIS.** O mesmo operador de posto 1 realiza as duas
    cláusulas sobre todo elemento: devolve intacta a parte inscrita e aniquila
    a granular. A leitura é uma só operação. -/
theorem the_reader_is_one (x : ellTwo) :
    ialdSelector (firstAtom.starProjection x) = firstAtom.starProjection x
    ∧ ialdSelector (x - firstAtom.starProjection x) = 0
    ∧ firstAtom.starProjection x + (x - firstAtom.starProjection x) = x := by
  obtain ⟨hu, hv, hsum⟩ := every_state_splits x
  exact ⟨(the_iald_selector_separates_the_sectors _ _ hu hv).1,
         (the_iald_selector_separates_the_sectors _ _ hu hv).2, hsum⟩

end

end TGLExt
