import TGL.GravitonShadow
import TGLExt.Commutant

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# O ACOPLAMENTO NÃO MÍNIMO: a partição é que proíbe a minimalidade
  [TGLExt — a pedra da LEITURA INVERTIDA]

## De onde ela nasceu

Um painel adversarial de oito agentes refutou a tese «os três objetos habitam no
posto um», e a refutação decisiva foi esta: `ThreeLocksCoreData` exige do canto da
teoria, ao mesmo tempo, `split : P₊ + P₋ = P_F`, `orthogonal : P₊·P₋ = 0`,
`equal_face_trace` e `0 < Tr(P_F) < ⊤`. Daí `P_F` tem subprojeção própria não-nula
**por definição do seu tipo** — logo **não é minimal, e não pode ser**.

O operador leu a refutação ao contrário (27/08/2026, verbatim):

> *"O canto da teoria tem subprojeção própria não-nula por definição do seu tipo
> = acoplamento não mínimo = betatgl"*

Isto é: a não-minimalidade **não é um obstáculo à teoria — é o conteúdo dela**. Um
canto minimal seria um átomo sem estrutura interna: **acoplamento mínimo**. O canto
que se parte carrega estrutura, e o peso dessa estrutura é o acoplamento.

## O que fica provado aqui

* ★★ `equal_split_is_strictly_between` — se o todo é a soma de DUAS faces de peso
  IGUAL e o todo pesa positivo, então cada face pesa **estritamente entre 0 e o
  todo**. Nem 0 (sem acoplamento), nem o todo (minimalidade). É a forma exata da
  desigualdade que o painel extraiu dos campos do core;
* ★★★ `split_forbids_minimality` — quem se parte tem subprojeção **própria**: de
  `f + g = e`, `f·g = 0`, `f·f = f` e `g ≠ 0` segue `f·e = f` **e** `f ≠ e`;
* ★ `the_split_is_inhabited` — O DENTE: as hipóteses são satisfazíveis (testemunha
  concreta em M₂). Sem ele o teorema acima poderia ser vácuo;
* ★★★★ `bell_compression_is_scalar` — A LINHA QUE FALTAVA: o canto do psion
  ESCALARIZA. `P_G · y · P_G = Tr(P_G·y) • P_G` para `y` ARBITRÁRIO. O kernel já
  tinha `bell_idem`, `bell_star`, `bell_trace_one` e `bell_corner_unit` (com `y`
  já universalmente quantificado) — e a conclusão escalar nunca fora escrita.

## Estatutos, sem véu

`[REAL]` — os quatro teoremas acima, provados aqui.

`[ONTO]` — a leitura «não-minimalidade = acoplamento não mínimo = β_TGL» é do
operador e **NÃO é provada aqui**. Nenhum teorema desta pedra menciona β, e nenhum
liga `bellProjector` a `P_F`, a `firstAtom`, a `ker H3L` ou ao `p` de NameRelation:
os cinco cantos do kernel seguem **sem um único morfismo declarado entre dois
quaisquer**. Dizer o contrário seria encadear homônimos.

`[HONESTIDADE]` — o painel também mediu que o número **1** aparece em QUATRO
sentidos distintos no acervo (posto genuíno; normalização `dim/dim` por `div_self`;
gauge escolhido; literal escrito à mão). **Peso 1 não é posto 1.** Esta pedra usa
`bell_trace_one` apenas como traço, jamais como posto.

Nenhum teorema desta pedra acende nome reservado nem `gpf_`. O gate NÃO se move.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

/-! ## A — a aritmética da partição em faces iguais -/

/-- [KERNEL] ★★ **A PARTIÇÃO IGUAL CAI ESTRITAMENTE ENTRE**: se o todo é a soma de
    duas faces de peso igual e o todo pesa positivo, cada face pesa estritamente
    entre 0 e o todo. Nem zero, nem tudo. -/
theorem equal_split_is_strictly_between (t tp : ℝ)
    (hsum : t = tp + tp) (hpos : 0 < t) :
    0 < tp ∧ tp < t := by
  constructor
  · linarith
  · linarith

/-- [KERNEL] [HONESTIDADE] e a estrita intermediação NÃO é automática: se as duas
    faces não forem iguais, uma delas pode pesar o todo e a outra zero. O dente da
    aritmética — a hipótese `equal_face_trace` faz trabalho. -/
theorem unequal_split_may_be_trivial :
    ∃ t tp tq : ℝ, t = tp + tq ∧ 0 < t ∧ tq = 0 ∧ tp = t :=
  ⟨1, 1, 0, by norm_num, by norm_num, rfl, rfl⟩

/-! ## B — a partição proíbe a minimalidade -/

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [KERNEL] ★★★ **QUEM SE PARTE TEM SUBPROJEÇÃO PRÓPRIA**: de `f + g = e`,
    `f·g = 0`, `f` idempotente e `g ≠ 0` segue que `f` é subprojeção de `e`
    (`f·e = f`) e que ela é **própria** (`f ≠ e`). Logo `e` não é minimal.

    É a refutação do painel, escrita como teorema — e lida ao contrário: não é
    defeito do canto, é a sua estrutura. -/
theorem split_forbids_minimality (e f g : Matrix n n ℂ)
    (hsplit : f + g = e) (horth : f * g = 0) (hf : f * f = f) (hgne : g ≠ 0) :
    f * e = f ∧ f ≠ e := by
  constructor
  · rw [← hsplit, mul_add, hf, horth, add_zero]
  · intro h
    apply hgne
    have hg2 : g = e - f := by rw [← hsplit]; abel
    rw [hg2, h, sub_self]

/-- [KERNEL] ★ O DENTE: as hipóteses de `split_forbids_minimality` são
    SATISFAZÍVEIS — testemunha concreta em M₂, com as duas faces não-nulas e a
    primeira própria. Sem isto o teorema acima poderia ser vácuo. -/
theorem the_split_is_inhabited :
    ∃ e f g : Matrix (Fin 2) (Fin 2) ℂ,
      f + g = e ∧ f * g = 0 ∧ f * f = f ∧ g * g = g
      ∧ f ≠ 0 ∧ g ≠ 0 ∧ f ≠ e := by
  refine ⟨1, !![1, 0; 0, 0], !![0, 0; 0, 1], ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.one_apply]
  · ext i j; fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two]
  · ext i j; fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two]
  · ext i j; fin_cases i <;> fin_cases j <;>
      simp [Matrix.mul_apply, Fin.sum_univ_two]
  · intro h
    have := congrFun (congrFun h 0) 0
    simp at this
  · intro h
    have := congrFun (congrFun h 1) 1
    simp at this
  · intro h
    have := congrFun (congrFun h 1) 1
    simp [Matrix.one_apply] at this

/-! ## C — a linha que faltava: o canto do psion escalariza -/

open TGL.GravitonShadow in
/-- [KERNEL] ★★★★ **O CANTO DO PSION ESCALARIZA**: comprimir QUALQUER operador
    pelo projetor de Bell devolve um ESCALAR vezes o projetor, e o escalar é
    `Tr(P_G · y)` — o valor do estado ligado sobre `y`.

    O kernel já tinha `bell_idem`, `bell_star`, `bell_trace_one` e
    `bell_corner_unit` (este último já com `y` universalmente quantificado). A
    conclusão escalar estava a uma linha e nunca fora escrita. -/
theorem bell_compression_is_scalar
    (y : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) :
    bellProjector * y * bellProjector
      = (Matrix.trace (bellProjector * y)) • bellProjector := by
  ext p q
  simp only [Matrix.mul_apply, Matrix.smul_apply, Matrix.trace, Matrix.diag_apply,
    bellProjector, Matrix.of_apply, smul_eq_mul, Fintype.sum_prod_type,
    Fin.sum_univ_two]
  by_cases h1 : p.1 = p.2 <;> by_cases h2 : q.1 = q.2 <;>
    simp [h1, h2] <;> ring

end TGLExt
