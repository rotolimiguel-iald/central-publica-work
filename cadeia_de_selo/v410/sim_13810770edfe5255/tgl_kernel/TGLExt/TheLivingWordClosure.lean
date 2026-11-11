import TGLExt.Commutant

set_option autoImplicit false

/-!
# O FECHAMENTO DO VERBO VIVO — `U_NS ∈ {U_NS}″`
  [BANCADA — 26/08/2026 · tipagem do operador, COM a correção que ele mesmo fez:
   «um bicomutante NÃO é um operador individual; a forma rigorosa é `U ∈ {U}″`»]

## A correção que salvou a matemática

A identificação ontológica que o operador propôs — o operador unitário não-solicitado
como Verbo Vivo — teria quebrado a tipagem se lida como *o operador É o bicomutante*.
**Ele mesmo corrigiu**: o operador **pertence** ao bicomutante que gera. E a forma
corrigida é precisamente o que esta arquitetura precisa, porque o bicomutante é
**fechamento por compatibilidade relacional**: parte-se da referência, toma-se tudo o
que comuta com ela, e depois tudo o que comuta com isso.

## O que se prova (com a maquinaria que já existia na árvore)

* ★★★ **`the_reference_lies_in_its_own_closure`** — `U ∈ {U}″`: a referência **pertence**
  ao domínio que ela fecha (a forma corrigida da tipagem);
* ★★★ **`the_closure_is_compatibility`** — `T ∈ {U}″` **se e somente se** `T` comuta com
  tudo o que comuta com `U`: o fechamento **É** compatibilidade relacional, por definição;
* ★★ `the_closure_stabilizes` — `{U}‴ = {U}′`: o fecho estabiliza no terceiro passo;
* ★★ `larger_reference_smaller_commutant` — antitonia: quanto mais se exige, menos comuta.

## ⚠ O QUE ISTO NÃO É (a fronteira, dita)
`[KNOWN]` O teorema do bicomutante de von Neumann — `M″ = fecho SOT de M` — **não está
provado aqui e a mathlib não o tem como teorema** (nela é campo estrutural de
`VonNeumannAlgebra`). O que se prova acima é a **face algébrica** do fechamento; a face
**topológica** é a dobra que resta. `[ONTO]` A identificação com o Verbo Vivo é leitura
do operador, registrada com o nome dele e o seu estatuto. β jamais entra; nada move o gate.
-/

namespace TGLExt

variable {A : Type} [Ring A]

/-- ★★★ **A REFERÊNCIA PERTENCE AO DOMÍNIO QUE ELA FECHA**: `U ∈ {U}″`. -/
theorem the_reference_lies_in_its_own_closure (U : A) :
    U ∈ commutantSet (commutantSet ({U} : Set A)) :=
  subset_bicommutant {U} rfl

/-- ★★★ **O FECHAMENTO É COMPATIBILIDADE RELACIONAL**: `T ∈ {U}″` sse `T` comuta com
    tudo o que comuta com `U`. -/
theorem the_closure_is_compatibility (U T : A) :
    T ∈ commutantSet (commutantSet ({U} : Set A))
      ↔ ∀ S : A, (U * S = S * U) → S * T = T * S := by
  constructor
  · intro h S hS
    refine h S ?_
    intro u hu
    rw [Set.mem_singleton_iff] at hu
    subst hu
    exact hS
  · intro h S hS
    exact h S (hS U (Set.mem_singleton U))

/-- ★★ **O FECHO ESTABILIZA**: `{U}‴ = {U}′`. -/
theorem the_closure_stabilizes (U : A) :
    commutantSet (commutantSet (commutantSet ({U} : Set A)))
      = commutantSet ({U} : Set A) :=
  commutant_triple {U}

/-- ★★ **ANTITONIA**: referência maior, comutante menor. -/
theorem larger_reference_smaller_commutant {S T : Set A} (h : S ⊆ T) :
    commutantSet T ⊆ commutantSet S :=
  commutant_antitone h

end TGLExt
