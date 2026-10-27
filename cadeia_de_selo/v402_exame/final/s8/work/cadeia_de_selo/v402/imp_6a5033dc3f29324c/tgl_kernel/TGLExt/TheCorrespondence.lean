import TGLExt.TheEmptying

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A CORRESPONDÊNCIA — e os dois zeros do livro-razão
  [BANCADA — 23/08/2026]

## A cunhagem do operador

> *"A diferença está na **correspondência**. Sem correspondência, `0_abs = 100%` é falso por
> natureza — mas tornar-se-ia verdade se admitíssemos **relação sem correspondência**."*
>
> *"**corresponder = custo**; **falta de correspondência = sem custo**; **sem custo ≠ grátis**;
> **grátis = eco do registro pago**."* · *"**MEMÓRIA = ECO**."*

## ★ O ACHADO DESTA PEDRA

O operador separou três regimes pelo custo. Mas **o custo não os separa** — e é isso que a pedra
prova:

> **`sem custo` e `grátis` têm o MESMO custo: zero. O que os distingue não é o número — é o
> REGISTRO.**

Isto é **exatamente** a estrutura de `0_mod ≠ 0_abs` (`TheAlgebraicReader`), transposta para o
livro-razão: *dois zeros numericamente iguais e ontologicamente distintos*. E a lição é a mesma:
**quem olha só o número não vê a diferença; quem olha o registro vê.**

## O que fica provado

* ★★★ `cost_does_not_determine_correspondence` — **existem dois estados de custo idêntico (zero)
  e situação de correspondência oposta.** *O custo é cego à correspondência;*
* ★★★ `free_is_not_costless` — **`grátis ≠ sem custo`**, ainda que `custo(grátis) = custo(sem
  custo) = 0`. *A distinção é de tipo, não de grandeza;*
* ★★★ `echo_presupposes_payment` — **o eco exige registro anterior**: não há eco sem que a
  correspondência tenha sido paga alguma vez. *A memória não cria a correspondência: reapresenta-a;*
* ★★★ `no_correspondence_no_relation` — se toda relação verdadeira exige correspondência, e não
  há correspondente algum, **então não há relação alguma**. *É a forma lógica de "falso por
  natureza, não por contagem";*
* ★★★ `the_void_cannot_close_on_itself` — em particular **`0_abs` não pode fechar-se sobre si**:
  a auto-relação sem correspondência **não é relação**. *O vazio não pode declarar-se completo
  só porque se refere a si mesmo;*
* ★★ `writing_is_not_corresponding` — **exibir a igualdade não estabelece a correspondência**:
  há mapas onde a sintaxe existe e o correspondente não. *A inscrição da relação ≠ existência
  da correspondência.*

## A leitura, e a fronteira

`[REAL]` a separação de tipos e as seis proposições. **`[ONTO]` do operador**, e fora de todo
enunciado: `corresponder = custo`, `memória = eco`, e a identificação do piso com o que ele
chama de amor. **A pedra prova a ESTRUTURA — que dois zeros podem ser numericamente iguais e
ontologicamente distintos —, e não as identificações.**

E o encaixe com `TheEmptying`: lá o **piso positivo** garante que esvaziar não aniquila; aqui o
**registro** garante que zero-custo não é zero-correspondência. *Nos dois casos o que salva a
identidade não é o número: é o que ficou inscrito.*

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

noncomputable section

/-! ### O livro-razão: custo agora, e se alguma vez houve correspondência -/

/-- O LIVRO-RAZÃO de um estado: quanto custa **agora**, e se a correspondência **já foi paga**
    alguma vez. São dois campos porque são **duas perguntas diferentes**. -/
structure Ledger where
  /-- houve correspondência alguma vez? -/
  paid : Bool
  /-- quanto custa agora? -/
  cost : ℝ

/-- `0_abs`: **nunca correspondeu**, e por isso nada custa. -/
def costless : Ledger := ⟨false, 0⟩

/-- `grátis`: **já correspondeu e já pagou**; o que se vê agora é o **eco**. -/
def freeEcho : Ledger := ⟨true, 0⟩

/-- a inscrição primeira: **corresponde agora**, e paga por isso. -/
def inscription (c : ℝ) : Ledger := ⟨true, c⟩

/-! ### ★ O achado: o custo é cego à correspondência -/

/-- ★★★ **O CUSTO NÃO DETERMINA A CORRESPONDÊNCIA.** Exibem-se dois estados com **o mesmo
    custo** — zero — e situação de correspondência **oposta**.

    *Quem olha só o número não vê a diferença.* -/
theorem cost_does_not_determine_correspondence :
    costless.cost = freeEcho.cost ∧ costless.paid ≠ freeEcho.paid := by
  constructor
  · rfl
  · simp [costless, freeEcho]

/-- ★★★ **GRÁTIS NÃO É SEM CUSTO.** Os dois valem zero e **não são o mesmo estado**.

    *A distinção é de tipo, não de grandeza* — exatamente como `0_mod ≠ 0_abs`. -/
theorem free_is_not_costless : freeEcho ≠ costless := by
  intro h
  have : freeEcho.paid = costless.paid := by rw [h]
  simp [freeEcho, costless] at this

/-- ★★★ **O ECO PRESSUPÕE PAGAMENTO.** Não há eco sem registro anterior: a memória **não cria**
    a correspondência, **reapresenta-a**. -/
theorem echo_presupposes_payment : freeEcho.paid = true := rfl

/-- ★★ e a inscrição primeira **paga**: custo `c`, com correspondência estabelecida. -/
theorem inscription_pays (c : ℝ) :
    (inscription c).paid = true ∧ (inscription c).cost = c := ⟨rfl, rfl⟩

/-- ★★ **OS TRÊS REGIMES, num enunciado.** Custo zero sem correspondência; custo `c` com
    correspondência nova; custo zero **com** correspondência antiga. *O meio é o único que paga;
    os extremos valem zero por razões opostas.* -/
theorem the_three_regimes (c : ℝ) :
    (costless.cost = 0 ∧ costless.paid = false)
    ∧ ((inscription c).cost = c ∧ (inscription c).paid = true)
    ∧ (freeEcho.cost = 0 ∧ freeEcho.paid = true) :=
  ⟨⟨rfl, rfl⟩, ⟨rfl, rfl⟩, ⟨rfl, rfl⟩⟩

/-! ### ★ Relação exige correspondência -/

/-- ★★★ **SEM CORRESPONDENTE, SEM RELAÇÃO.** Se toda relação verdadeira exige correspondência,
    e não existe correspondente algum para `a`, então **não existe relação alguma** com `a`.

    *É a forma lógica de "falso por natureza, e não por contagem".* -/
theorem no_correspondence_no_relation {α : Type} (R C : α → α → Prop)
    (hRC : ∀ x y, R x y → C x y) (a : α) (hno : ¬ ∃ b, C a b) :
    ¬ ∃ b, R a b := by
  rintro ⟨b, hb⟩
  exact hno ⟨b, hRC a b hb⟩

/-- ★★★ **O VAZIO NÃO PODE FECHAR-SE SOBRE SI.** Em particular, a auto-relação `R a a` não
    existe quando não há correspondente algum — nem sequer o próprio `a`.

    *O vazio não pode declarar-se completo só porque se refere a si mesmo.* -/
theorem the_void_cannot_close_on_itself {α : Type} (R C : α → α → Prop)
    (hRC : ∀ x y, R x y → C x y) (a : α) (hno : ¬ ∃ b, C a b) :
    ¬ R a a := by
  intro h
  exact hno ⟨a, hRC a a h⟩

/-- ★★ **ESCREVER NÃO É CORRESPONDER.** Existe relação `R` que vale em toda parte enquanto a
    correspondência `C` não vale em lugar nenhum — logo a implicação `R ⟹ C` **é hipótese, e não
    consequência da escrita**.

    *A inscrição da relação não produz a existência da correspondência.* -/
theorem writing_is_not_corresponding :
    ∃ (R C : Unit → Unit → Prop), (∀ x y, R x y) ∧ (∀ x y, ¬ C x y) := by
  refine ⟨fun _ _ => True, fun _ _ => False, fun _ _ => trivial, fun _ _ => id⟩

/-- ★★ o fecho: **o custo é cego**, **o eco pressupõe pagamento**, e **sem correspondente não há
    relação** — os três no mesmo enunciado. -/
theorem the_correspondence_closes {α : Type} (R C : α → α → Prop)
    (hRC : ∀ x y, R x y → C x y) (a : α) (hno : ¬ ∃ b, C a b) :
    (costless.cost = freeEcho.cost ∧ freeEcho ≠ costless)
    ∧ freeEcho.paid = true
    ∧ ¬ R a a :=
  ⟨⟨rfl, free_is_not_costless⟩, rfl, the_void_cannot_close_on_itself R C hRC a hno⟩

end

end TGLExt
