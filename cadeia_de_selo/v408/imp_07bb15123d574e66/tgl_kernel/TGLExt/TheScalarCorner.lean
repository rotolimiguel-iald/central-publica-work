import TGL.GravitonShadow
import TGLExt.Commutant
import TGLExt.TheNonMinimalCoupling

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 800000

/-!
# O CANTO ESCALAR: a propriedade ganha nome, e o nome força o átomo
  [TGLExt — o primeiro passo contra os cinco cantos sem morfismo]

## De onde ela nasceu

Dois painéis adversariais mediram, e a medida ficou: o kernel tem **cinco cantos**
(`firstAtom` em ℓ², `ker H3L` em `EuclideanSpace`, `P_F` no core, o `p` de
`NameRelation` em M₂**(ℝ)**, `bellProjector` em M₄(ℂ)) **sem um único morfismo
declarado entre dois quaisquer**. E registraram um `NÃO ACHEI` decisivo: não existe
`End(pHp) ≅ ℂ` em parte alguma do acervo — a escalaridade do canto era enunciada
**ad hoc**, caso a caso, sem nome.

Forçar um morfismo entre dois cantos concretos seria a armadilha que os painéis
nomearam (**homônimo virar ponte**). O passo honesto é outro: **dar nome à
propriedade**, exibir uma instância medida, e provar que a propriedade **tem
conteúdo** — isto é, que nem toda projeção a satisfaz.

## O que fica provado `[REAL]`

* `ScalarCorner` — a propriedade, nomeada uma vez só: projeção auto-adjunta cuja
  compressão de **qualquer** operador devolve escalar vezes ela mesma;
* ★ `psionCorner` — o **psion** instancia a propriedade. Os três campos já estavam
  provados (`bell_idem`, `bell_star`, e a linha que o operador localizou,
  `bell_compression_is_scalar`); aqui eles passam a ser **um objeto**;
* ★★★★ `scalarCorner_forces_trace_one` — **A PROPRIEDADE FORÇA O ÁTOMO**: se um
  projetor não-nulo escalariza, então o seu traço é **exatamente 1**. Não se supõe
  posto um: ele **cai** da escalarização. É a recíproca que faltava;
* ★★ `the_identity_does_not_scalarise` — O DENTE: a identidade de M₂ **não**
  escalariza. Sem ele a propriedade poderia ser universal, logo vazia.

## Estatutos, sem véu

`[REAL]` — os quatro acima.

`[ONTO]` — a leitura do operador «posto um é de fato o um absoluto» ganha aqui
a sua face estrutural (a escalarização **força** o traço 1), mas a identificação
com `1_abs` **não é provada** e nenhum teorema desta pedra a menciona.

`[OPEN]` — o que esta pedra **não** faz, e é preciso dizer: ela tem **UMA**
instância. Não constrói morfismo entre cantos, não prova a recíproca geral
(«posto um ⟹ escalariza»), e não liga `bellProjector` a `P_F`, a `firstAtom`,
a `ker H3L` nem ao `p` de `NameRelation`. Os cinco cantos seguem **desligados**.
O que muda é que agora existe **uma propriedade nomeada** onde havia duas contas
homônimas — e o segundo canto que a instanciar será **ponte**, não coincidência.

Nenhum teorema acende nome reservado nem `gpf_`. O gate NÃO se move.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — a propriedade, nomeada -/

/-- **O CANTO ESCALAR**: projeção auto-adjunta cuja compressão de QUALQUER operador
    devolve um escalar vezes ela mesma — e o escalar é o traço contra ela. -/
structure ScalarCorner (n : Type) [Fintype n] [DecidableEq n] where
  p : Matrix n n ℂ
  idem : p * p = p
  selfadj : star p = p
  scalarises : ∀ y : Matrix n n ℂ, p * y * p = (Matrix.trace (p * y)) • p

/-! ## B — o psion instancia -/

open TGL.GravitonShadow in
/-- [KERNEL] ★ **O PSION É UM CANTO ESCALAR.** Os três campos já estavam provados
    no kernel; a linha que faltava foi localizada pelo operador em quatro palavras
    (*o que está faltando para você conectar é o psion*). Aqui eles deixam de ser
    três fatos soltos e passam a ser **um objeto**. -/
noncomputable def psionCorner : ScalarCorner (Fin 2 × Fin 2) where
  p := bellProjector
  idem := bell_idem
  selfadj := bell_star
  scalarises := bell_compression_is_scalar

/-! ## C — a propriedade força o átomo -/

/-- [KERNEL] ★★★★ **ESCALARIZAR FORÇA O TRAÇO 1**: se um projetor NÃO-NULO
    escalariza, o seu traço é exatamente 1. O posto um não é hipótese — ele CAI
    da escalarização.

    A conta é de três linhas e nunca fora feita: comprimir a IDENTIDADE dá
    `p = Tr(p) • p`, logo `(1 − Tr(p)) • p = 0`, e com `p ≠ 0` sobra `Tr(p) = 1`. -/
theorem scalarCorner_forces_trace_one (p : Matrix n n ℂ) (hidem : p * p = p)
    (hsc : ∀ y : Matrix n n ℂ, p * y * p = (Matrix.trace (p * y)) • p)
    (hne : p ≠ 0) :
    Matrix.trace p = 1 := by
  have h := hsc 1
  simp only [mul_one] at h
  rw [hidem] at h
  have h2 : ((1 : ℂ) - Matrix.trace p) • p = 0 := by
    rw [sub_smul, one_smul, ← h, sub_self]
  rcases smul_eq_zero.mp h2 with h3 | h3
  · exact (sub_eq_zero.mp h3).symm
  · exact absurd h3 hne

/-- [KERNEL] e a leitura do objeto: o traço do canto do psion é 1 — não porque se
    tenha suposto, mas porque a escalarização o obriga. -/
theorem psionCorner_trace_one : Matrix.trace psionCorner.p = 1 := by
  refine scalarCorner_forces_trace_one psionCorner.p psionCorner.idem
    psionCorner.scalarises ?_
  intro h
  have h1 : Matrix.trace psionCorner.p = 1 := TGL.GravitonShadow.bell_trace_one
  rw [h] at h1
  simp at h1

/-! ## D — o dente: nem toda projeção escalariza -/

/-- [KERNEL] ★★ **O DENTE**: a identidade de M₂ NÃO escalariza. Sem isto a
    propriedade `ScalarCorner` poderia valer para toda projeção — logo não
    distinguiria nada, e `scalarCorner_forces_trace_one` seria vácuo. -/
theorem the_identity_does_not_scalarise :
    ¬ (∀ y : Matrix (Fin 2) (Fin 2) ℂ,
        (1 : Matrix (Fin 2) (Fin 2) ℂ) * y * (1 : Matrix (Fin 2) (Fin 2) ℂ)
          = (Matrix.trace ((1 : Matrix (Fin 2) (Fin 2) ℂ) * y))
              • (1 : Matrix (Fin 2) (Fin 2) ℂ)) := by
  intro h
  have h1 := h 1
  simp only [mul_one, one_mul] at h1
  have h2 := congrFun (congrFun h1 0) 0
  simp [Matrix.one_apply, Matrix.trace_one, Fintype.card_fin] at h2

end TGLExt
