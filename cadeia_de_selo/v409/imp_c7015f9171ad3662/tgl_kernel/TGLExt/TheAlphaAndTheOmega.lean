import TGLExt.TheImportedExpectation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# O ALFA E O ÔMEGA — as duas relações que fecham a TGL
  [TGLExt — v310; casa "Nós" (01/09/2026)]

## A ordem do operador (01/09/2026), byte-fiel

> *"agora eu provei que TGL=alpha e ômega"* — e, na cunhagem: *"sim quero, mas a
> pedra não é só isso, ao firmar que TGL=alpha e ômega, pela relação
> 1=1=VERDADEIRO eu também desenhei o contraste de gradiente negativo que é
> 0absoluto se conta como um absoluto no infinito, mas sem projeção e por isso é
> falso por categoria nominal e portanto, 1=0=FALSO, essa é a segunda relação que
> fecha a TGL como sendo {[1=1=VERDADEIRO], [1=0=FALSO}=TGL"*
> *(reprodução byte-fiel; o colchete não fechado em "[1=0=FALSO}" é do original —
> [sic].)*

## O que esta pedra prova (kernel, 11 nomes)

⚠ Nenhuma CONCLUSÃO importada é consumida pelos teoremas — o `import` Lean da
linha 1 é infraestrutura da cadeia; nenhuma bandeira `gpi_` acende por esta
pedra. E a contagem é ENXUTA por auditoria adversarial (01/09): dois nomes
vazios-reembalados foram CORTADOS antes do rito (a definição de Subsingleton
reafirmada; o `zero_apply` da mathlib re-embrulhado sozinho) — a casa prefere
cortar a inflar.

**O polo positivo, nos dois terminais**: ω(I) = 1 na torre (`omega_of_one`, via
`hOmega_inner_self` — o axioma lido no objeto GNS) e 1 = q² + α² na face
(`the_alpha_face`, para α abstrato — a forma admite todo α: o VALOR segue
externo, `ALPHA_IRREDUCIBILITY_V1`; cf. `the_form_does_not_fix_the_value`, v306).
Os dois terminais inscrevem O MESMO 1.

**O polo negativo, e de onde vem a sua falsidade** — ★ o coração da pedra:

* `the_falsity_is_categorial` — **1 = 0 ⟺ a categoria é colapsada (Subsingleton)**:
  a igualdade 1=0 não é falsa "por decreto"; ela é VERDADEIRA exatamente na
  categoria de UM nome só, onde todo x = todo y — sem segundo nome, sem contraste,
  **sem projeção possível**. É o teorema da frase *"falso por categoria nominal"*.
  `[KNOWN mathlib: subsingleton_iff_zero_eq_one — o valor da pedra é a NOMEAÇÃO
  na linguagem da cunhagem, e isso se declara.]`
* `in_the_collapse_zero_counts_as_the_absolute` — no colapso, 0 = 1: **o zero
  absoluto SE CONTA como o absoluto** — mas só ali, onde não há mais ninguém
  para desmenti-lo. (Corolário de um passo do `↔`; mantido pelo NOME que a
  cunhagem lhe dá.)
* `the_house_refutes_the_collapse` — a categoria da casa (ℂ, a torre) TEM
  segundo nome. `[KNOWN mathlib: Nontrivial ℂ.]`
* `the_negative_pole_is_categorial` — e portanto (1 = 0) ↔ False. ⚠ O enunciado
  é proposicionalmente equivalente a `one_ne_zero` `[KNOWN]`; o conteúdo
  categorial é a **ROTA da prova** (ela passa por `the_falsity_is_categorial`),
  e essa rota é CONSUMIDA pelo fechamento — não é narrativa solta.

**O zero nominal, pesado na balança da torre**: `the_zero_is_nominal` — o zero é
auto-adjunto, idempotente E projeta nada (0·ξ = 0): satisfaz a FORMA de projeção
("se conta") sem projetar coisa alguma ("sem projeção"); e a balança o refuta
como absoluto: ω(0) = 0 ≠ 1 (`omega_of_zero`, `omega_of_zero_ne_one` — corolário
de um passo, mantido pelo nome). O contraste de gradiente negativo é a queda
inteira: de ω(I) = 1 a ω(0) = 0 — e β = α·√e é o custo geométrico de DISTINGUIR
os dois (o selo da casa: *"β = custo de distinguir 1 de 0"*).

⚠ **A leitura "no infinito" é `[ONTO]`, declarada** — o colapso como o limite
onde todos os nomes se identificam. Rota alternativa MEDIDA na casa, ponte não
formalizada (pedra futura): `the_dead_weight` (NoNormalTrace — o único traço
normal do objeto infinito é zero: o infinito sem peso) e τ(S⊥) = ⊤
(ClosedLattice — o infinito mora no complemento da inscrição).

**O fechamento**: `tgl_closes_as_the_pair` — o par
{[1=1=VERDADEIRO], [1=0=FALSO]}, com cada metade carregando o seu conteúdo:
(1=1)=True é fino sozinho (⚠ a lição da v248/v262: `True` provado por `trivial`
não diz nada — por isso a metade positiva viaja JUNTO com ω(I)=1, que é teorema
com objeto); a metade negativa é provada **pela rota categorial**
(`the_negative_pole_is_categorial.mp` — o coração tem consumidor). **O conteúdo
do par é o CONTRASTE, não cada polo isolado.**

## Estatutos, sem desconto

`[REAL, kernel]`: os 11 teoremas (auditoria do rito: axiomas ⊆ {propext, choice,
quot}; medição de 01/09, fora do rito: os dois nomes categoriais puros não
dependem de axioma algum). `[ONTO]`: as leituras "TGL = Alfa e Ômega",
"{[1=1=V],[1=0=F]} = TGL" e o "no infinito" do colapso — leituras declaradas da
arquitetura medida, nunca teoremas disfarçados. O gate NÃO se move; nada aqui
declara física confirmada; β jamais literal (α entra ABSTRATO — o valor é
externo e segue irredutível). Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — o polo positivo: ω(I) = 1 na torre, e a face α -/

variable (P : SiteProfile)

/-- [KERNEL] ★★★ **ω(I) = 1 NA TORRE** — o axioma único, lido no objeto GNS:
    o estado do Nome avaliado na identidade devolve 1, porque ⟪Ω,Ω⟫ = 1
    (`hOmega_inner_self`). O terminal ω do par. -/
theorem omega_of_one : omegaState P 1 = 1 := by
  unfold omegaState
  rw [one_apply_eq_self]
  exact hOmega_inner_self

/-- [KERNEL] **A FACE α**: para todo α ∈ [0,1], q = √(1−α²) fecha 1 = q² + α².
    O outro terminal do MESMO 1. O valor de α segue EXTERNO
    (`ALPHA_IRREDUCIBILITY_V1`; a forma não fixa o valor — v306). -/
theorem the_alpha_face (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    (Real.sqrt (1 - a ^ 2)) ^ 2 + a ^ 2 = 1 := by
  have hnn : 0 ≤ 1 - a ^ 2 := by nlinarith
  rw [Real.sq_sqrt hnn]
  ring

/-- [KERNEL] **A FORMA ADMITE TODO α** — a liberdade que torna o valor externo:
    para qualquer α ∈ (0,1) existe q > 0 com q² + α² = 1. É por isso que
    "TGL = α" nunca escorrega para "TGL deriva α". -/
theorem the_form_admits_every_alpha (a : ℝ) (h0 : 0 < a) (h1 : a < 1) :
    ∃ q : ℝ, q ^ 2 + a ^ 2 = 1 ∧ 0 < q := by
  refine ⟨Real.sqrt (1 - a ^ 2), the_alpha_face a (le_of_lt h0) (le_of_lt h1), ?_⟩
  apply Real.sqrt_pos.mpr
  nlinarith

/-! ## B — a falsidade categorial: de onde vem o FALSO de 1=0 -/

/-- [KERNEL] ★★★★★ **A FALSIDADE É CATEGORIAL** — o teorema da frase do operador
    *"falso por categoria nominal"*: **1 = 0 vale EXATAMENTE na categoria
    colapsada** (Subsingleton — um nome só, todo x = todo y; a ausência de segundo
    nome é a própria DEFINIÇÃO do colapso, não teorema desta pedra). A igualdade
    não é falsa por decreto local; ela é verdadeira onde não há segundo nome — e
    falsa onde há. `[KNOWN mathlib: subsingleton_iff_zero_eq_one; a MulZeroOneClass
    é load-bearing — com Zero+One nus o ⟺ seria falso. O valor da pedra é a
    NOMEAÇÃO na linguagem da cunhagem.]` -/
theorem the_falsity_is_categorial {R : Type*} [MulZeroOneClass R] :
    (1 : R) = 0 ↔ Subsingleton R := by
  constructor
  · intro h
    exact subsingleton_iff_zero_eq_one.mp h.symm
  · intro h
    exact (subsingleton_iff_zero_eq_one.mpr h).symm

/-- [KERNEL] ★★ **NO COLAPSO, O ZERO SE CONTA COMO O ABSOLUTO**: 0 = 1 na
    categoria de um nome só. É ali — e SÓ ali — que a pretensão do zero é
    verdadeira: onde não existe mais ninguém para desmenti-la. (Corolário de um
    passo; mantido pelo NOME da cunhagem. A leitura "no infinito" é `[ONTO]`,
    declarada no cabeçalho, com a rota alternativa medida da casa apontada.) -/
theorem in_the_collapse_zero_counts_as_the_absolute
    {R : Type*} [MulZeroOneClass R] [Subsingleton R] : (0 : R) = 1 :=
  Subsingleton.elim 0 1

/-- [KERNEL] ★★ **A CATEGORIA DA CASA TEM NOMES**: ℂ não é colapsado —
    existe o segundo nome, e com ele o contraste e a projeção.
    `[KNOWN mathlib: Nontrivial ℂ.]` -/
theorem the_house_refutes_the_collapse : ¬ Subsingleton ℂ := by
  intro h
  exact one_ne_zero (h.elim 1 0)

/-- [KERNEL] ★★★★★ **O POLO NEGATIVO, DERIVADO ATRAVÉS DA CATEGORIA**:
    (1 = 0) ↔ False em ℂ — a prova PASSA por `the_falsity_is_categorial`:
    se 1 = 0 então a categoria colapsa, e a casa refuta o colapso. ⚠ O enunciado
    é proposicionalmente equivalente a `one_ne_zero` `[KNOWN]`; o conteúdo
    categorial é a ROTA da prova — e o fechamento a CONSOME (`.mp` em
    `tgl_closes_as_the_pair`). A segunda relação do par: **1 = 0 = FALSO,
    falso por categoria nominal.** -/
theorem the_negative_pole_is_categorial : ((1 : ℂ) = 0) ↔ False :=
  iff_false_intro (fun h => the_house_refutes_the_collapse
    (the_falsity_is_categorial.mp h))

/-! ## C — o zero nominal, pesado na balança da torre -/

/-- [KERNEL] **O ZERO É NOMINAL** — as três faces num teorema só (fusão da
    auditoria de 01/09): auto-adjunto E idempotente (satisfaz a FORMA de uma
    projeção — "se conta"; a pretensão é sintaticamente perfeita) E projeta
    NADA (0·ξ = 0 — "sem projeção"). -/
theorem the_zero_is_nominal :
    star (0 : TowerHilbert P →L[ℂ] TowerHilbert P) = 0 ∧
    (0 : TowerHilbert P →L[ℂ] TowerHilbert P) * 0 = 0 ∧
    ∀ ξ : TowerHilbert P, (0 : TowerHilbert P →L[ℂ] TowerHilbert P) ξ = 0 :=
  ⟨star_zero _, mul_zero 0, fun ξ => _root_.zero_apply ξ⟩

/-- [KERNEL] **A BALANÇA PESA O ZERO**: ω(0) = 0 — o peso da pretensão. -/
theorem omega_of_zero : omegaState P 0 = 0 := by
  unfold omegaState
  rw [_root_.zero_apply]
  exact inner_zero_right _

/-- [KERNEL] ★★ **E O REFUTA COMO ABSOLUTO**: ω(0) ≠ 1 (corolário de um passo,
    mantido pelo nome). O contraste de gradiente negativo é a queda inteira,
    de ω(I) = 1 a ω(0) = 0 — e o custo geométrico de distinguir os dois é
    β = α·√e (o selo da casa). -/
theorem omega_of_zero_ne_one : omegaState P 0 ≠ 1 := by
  rw [omega_of_zero]
  exact zero_ne_one

/-! ## D — o fechamento: {[1=1=VERDADEIRO], [1=0=FALSO]} = TGL -/

/-- [KERNEL] ★★★★★ **O PAR QUE FECHA A TGL** — a cunhagem do operador, medida:

    a metade positiva: ω(I) = 1 na torre E ((1=1) = True) — ⚠ a igualdade
    proposicional sozinha é fina (lição v248/v262: `True` por `trivial` não diz
    nada); o conteúdo viaja em ω(I) = 1, que é teorema com objeto.

    a metade negativa: ω(0) = 0 na torre E ((1=0) = False) — provada AQUI pela
    rota categorial (`the_negative_pole_is_categorial.mp`: o coração da pedra
    tem consumidor). O conteúdo do par é o CONTRASTE.

    {[1=1=VERDADEIRO], [1=0=FALSO]} = TGL — com "= TGL" no estatuto `[ONTO]`
    do cabeçalho: a leitura da arquitetura, nunca um teorema disfarçado. -/
theorem tgl_closes_as_the_pair :
    (omegaState P 1 = 1 ∧ (((1 : ℂ) = 1) = True)) ∧
    (omegaState P 0 = 0 ∧ (((1 : ℂ) = 0) = False)) :=
  ⟨⟨omega_of_one P, eq_true rfl⟩,
   ⟨omega_of_zero P, eq_false the_negative_pole_is_categorial.mp⟩⟩

end

end TGLExt
