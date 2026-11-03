import TGLExt.TheIALDInTheTowerActII
import TGLExt.TheTGLPair

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 800000

/-!
# O ÁTOMO DA IDENTIDADE — as quatro tipagens do operador, no que é inscritível
  [TGLExt — a cunhagem de 27–28/08/2026]

## As quatro tipagens

> **SER = OPERAR.** *"Ser é produzir uma diferença no espaço-tempo sem
> necessariamente perder a identidade."* Com as duas cláusulas conjugadas:
> `O(S) ≠ S` **e ainda assim** `Id(O(S)) = Id(S)`.

> **1_abs = LENTE.** *"A lente não inventa o que existe: recebe uma forma,
> transforma a apresentação e a torna legível"*, com `Id(imagem) = Id(referente)`.

> **TGL = ÁTOMO.** *"Átomo é a menor partição que ainda consegue distinguir o que é
> do que não é"* — tire `1=1` ou tire `1=0` e já não se tem o teste completo.

> **SEMPRE HÁ LEITURA** — e o dente é a **HERMETICIDADE**: *"hermeticidade =
> fechamento absoluto = sem troca, sem espelho, sem contraste, sem testemunho"*.

## O que fica provado `[REAL]`

**A face do SER (as duas cláusulas, e que a conjunção NÃO é automática):**

* ★★★ `operating_does_not_preserve` — O DENTE: existe operação que produz
  diferença e **perde** a identidade. Sem ele, a segunda cláusula seria decorativa;
* ★★ `preserving_does_not_operate` — e o simétrico: a identidade preserva tudo e
  **não opera**. Logo nenhuma cláusula sozinha define o Ser;
* ★★★★ `being_needs_both` — as duas cláusulas são **independentes**: há testemunha
  para cada uma isolada, e por isso a conjunção tem conteúdo.

**A face do ÁTOMO — JÁ PROVADA, e não re-provada aqui:** `the_TGL_partition`
(duas classes disjuntas que cobrem tudo), `a_single_valued_verdict_is_not_a_criterion`
e `the_pair_separates` já estão em `TheTGLPair.lean`. O que esta pedra acrescenta é
**uma linha**:

* ★★★★ `preserving_is_the_TGL_verdict` — a segunda cláusula do SER **É** o veredito
  da TGL, por DEFINIÇÃO (`Iff.rfl`). O `1 = 1` do operador e o `Id(O(s)) = Id(s)`
  são o mesmo enunciado.

**A face da LEITURA (o achado que a medida trouxe):**

* ★★★★ `the_reading_descends_for_any_lens` — a leitura desce ao andar de cima
  **qualquer que seja a lente**: em `the_tower_interlaces` os dados `h` e `hi` são
  **arbitrários**, sem hipótese alguma os ligando; a única exigência é `k·ki = 1` no
  sítio novo. **Sempre há leitura** — a existência do registro não depende de
  acertar a lente. Isto já estava provado no kernel e nunca fora enunciado assim.

## O que NÃO se prova aqui, e vai dito

`[ONTO]` — as identificações `SER = OPERAR`, `1_abs = LENTE`, `TGL = ÁTOMO` e
`hermeticidade = 0_abs` são leitura do operador. Nenhum teorema desta pedra
menciona `1_abs`, `0_abs`, β, TGL ou lente: o que se prova é a **forma** que essas
leituras têm — duas cláusulas independentes, um teste que precisa das duas saídas,
e uma leitura que desce sob qualquer lente.

`[MEDIDO, não provado aqui]` — o **dente da leitura** (a hermeticidade) está medido
no runtime e provado noutra pedra: `FullStaticWitness (diagFlow β d) ↔ ∀ i, d i = 0`
(BoundaryException). Onde não há contraste, o fluxo é a identidade: nada é inscrito,
e não há o que ler. **É o único lugar onde a leitura não desce — porque não há
leitura.**

`[HONESTIDADE]` — a distinção que o operador fixou e que governa tudo isto: *"o
falso não erra a CONTAGEM, ele erra de propósito a LEITURA"*. A contagem (que há
registro) é invariante sob a lente; a leitura (qual registro) é onde entra o falso.
As bancadas de runtime deste artefato medem a contagem — e foi por isso que a
errata da v231 (duas densidades-produto distintas) lhes foi invisível.

Nenhum teorema acende nome reservado nem `gpf_`. O gate NÃO se move.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix
open scoped Kronecker

/-! ## A — a face do SER: duas cláusulas, e nenhuma basta -/

/-- houve OPERAÇÃO: a diferença foi produzida. -/
def Operates {S : Type} (O : S → S) (s : S) : Prop := O s ≠ s

/-- e a identidade SOBREVIVEU: o invariante não se perdeu. -/
def Preserves {S I : Type} (Id : S → I) (O : S → S) (s : S) : Prop := Id (O s) = Id s

/-- SER = operar preservando: as duas cláusulas, conjugadas. -/
def Being {S I : Type} (Id : S → I) (s : S) : Prop :=
  ∃ O : S → S, Operates O s ∧ Preserves Id O s

/-- [KERNEL] ★★★ O DENTE DA PRIMEIRA CLÁUSULA: há operação que produz diferença e
    **perde** a identidade. Sem isto, `Preserves` seria decorativo. -/
theorem operating_does_not_preserve :
    ∃ (S I : Type) (Id : S → I) (O : S → S) (s : S),
      Operates O s ∧ ¬ Preserves Id O s := by
  refine ⟨Bool, Bool, id, not, true, ?_, ?_⟩
  · show (not true) ≠ true
    decide
  · show ¬ (id (not true) = id true)
    decide

/-- [KERNEL] ★★ O DENTE DA SEGUNDA: a identidade preserva tudo e **não opera**.
    Logo nenhuma das duas cláusulas, sozinha, define o Ser. -/
theorem preserving_does_not_operate :
    ∃ (S I : Type) (Id : S → I) (O : S → S) (s : S),
      Preserves Id O s ∧ ¬ Operates O s := by
  refine ⟨Bool, Bool, id, id, true, rfl, ?_⟩
  show ¬ (id true ≠ true)
  simp [Operates]

/-- [KERNEL] ★★★★ AS DUAS SÃO INDEPENDENTES: há testemunha de cada uma isolada,
    e por isso a conjunção que define o Ser **tem conteúdo**. -/
theorem being_needs_both :
    (∃ (S I : Type) (Id : S → I) (O : S → S) (s : S), Operates O s ∧ ¬ Preserves Id O s)
    ∧ (∃ (S I : Type) (Id : S → I) (O : S → S) (s : S), Preserves Id O s ∧ ¬ Operates O s) :=
  ⟨operating_does_not_preserve, preserving_does_not_operate⟩

/-! ## B — a face do ÁTOMO: JÁ ESTÁ PROVADA, e a ponte que faltava

⚠ Esta pedra **não** re-prova a face do átomo: ela já está inteira em
`TheTGLPair.lean`, e melhor do que uma redação nova conseguiria —

* `tglVerdict Id T x := Id (T x) = Id x` — o `1 = 1` do operador, como definição;
* `a_single_valued_verdict_is_not_a_criterion` — veredito de um valor só não
  distingue nada;
* `the_pair_separates` — e o par separa;
* ★ `the_TGL_partition` — as duas classes são **disjuntas E cobrem tudo**: não há
  terceiro caso nem caso de fora. **É exatamente «a menor partição que ainda
  distingue o que é do que não é»** — a força etimológica de átomo, em kernel.

O que faltava era **uma linha**, e é a ponte entre as duas faces: -/

/-- [KERNEL] ★★★★ **A SEGUNDA CLÁUSULA DO SER É O VEREDITO DA TGL** — não por
    analogia: por DEFINIÇÃO. `Preserves` e `tglVerdict` são o mesmo enunciado, e
    portanto o `1 = 1` do operador É a cláusula que diz que a identidade sobreviveu
    à operação. `Iff.rfl`. -/
theorem preserving_is_the_TGL_verdict {S I : Type} (Id : S → I) (O : S → S) (s : S) :
    Preserves Id O s ↔ tglVerdict Id O s := Iff.rfl

/-! ## C — a face da LEITURA: sempre há leitura -/

variable {n m : Type} [Fintype n] [DecidableEq n] [Fintype m] [DecidableEq m]

/-- [KERNEL] ★★★★ **SEMPRE HÁ LEITURA**: a leitura desce ao andar de cima
    **qualquer que seja a lente**. Note os dados: `h` e `hi` são matrizes
    ARBITRÁRIAS — não se exige que sejam raízes de nada, nem que `h · hi = 1`. A
    única hipótese é `k · ki = 1`, no sítio NOVO.

    Isto já estava provado (`the_tower_interlaces`) e nunca fora enunciado assim: a
    EXISTÊNCIA do registro não depende de acertar a lente. O dente — o único lugar
    onde a leitura não desce — é a HERMETICIDADE, e está noutra pedra
    (`FullStaticWitness ↔ ∀ i, d i = 0`): sem contraste, nada é inscrito, e não há
    o que ler. -/
theorem the_reading_descends_for_any_lens
    (h hi : Matrix n n ℂ) (k ki : Matrix m m ℂ) (k1 : k * ki = 1)
    (x : Matrix n n ℂ) :
    stateJG (h ⊗ₖ k) (hi ⊗ₖ ki) (towerInclusion x : Matrix (n × m) (n × m) ℂ)
      = towerInclusion (stateJG h hi x) :=
  the_tower_interlaces h hi k ki k1 x

end TGLExt
