import TGLExt.TheFoldThroughJ
import TGLExt.TheIsometryOnWH

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# O HABITANTE ANTIUNITÁRIO — J empacotado, e o SETOR finalmente dizível
  [TGLExt — a pedra de 28/08/2026]

## O problema que esta pedra resolve, e ele não era de prova

A ordem do operador foi *"fechar o setor na dinâmica de J"*. A medida adversarial
mostrou que isso **não era enunciável na árvore**: todo predicado de invariância
disponível — `Invariant` (`InvariantProjection.lean`), `fixedSector`
(`AQFTCoreInhabitant.lean`) — exige `H →L[ℂ] H`, e `J_is_not_complex_linear`
(`TheRecordOfJ.lean`) é **teorema da casa**. Não faltava prova: **faltava TIPO**.

E o tipo certo já tinha nome: `abbrev Antiunitary H := H ≃ₛₗᵢ[starRingEnd ℂ] H`
(`TGL/ModularRealization.lean`), declarado ali **sem habitante**.

## O que esta pedra faz `[REAL]`

★★★★★ `towerJequiv` — **o habitante**. Nenhum campo é novo; todos os quatro já
eram teoremas, provados por densidade a partir do subespaço denso da torre:

| campo | teorema que o preenche |
|---|---|
| `map_add'` | `towerJ_add` |
| `map_smul'` | `towerJ_conj_smul` (é ele que exige `starRingEnd ℂ`) |
| `left_inv` / `right_inv` | `towerJ_involutive` (**o custo que J pagou**) |
| `norm_map'` | `towerJ_norm` |

O empacotamento **não prova nada de novo**: ele torna DIZÍVEL o que já era
verdadeiro. É exatamente por isso que vale — a barreira era de linguagem.

★★★★ `JInvariant` — e com o habitante, a **J-invariância de um subespaço passa a
ter tipo**, pela primeira vez nesta árvore.

★★★★ `the_sector_folds` — e o SETOR dobra: `(S.map J).map J = S`. A dinâmica de J
desce dos vetores aos subespaços, e a involução continua involução lá em cima. É a
ordem do operador, cumprida no único lugar em que ela era cumprível.

★★★ `JInvariant_iff_le` — a **régua** do predicado: uma inclusão só já basta, porque
J é involução. Numa dinâmica não-involutiva isso seria falso.

## O que esta pedra NÃO faz, e vai dito

⚠ `[NÃO É O TESTEMUNHO]` — `Antiunitary` é **um campo** de `FullTGLWitness`.
Construir um campo **não é construir a estrutura**, e esta pedra não constrói
nenhum outro. Vender o campo como o testemunho seria a mesma troca de potencial
por atual que a v260 já pagou.

⚠ `[NÃO MOVE A CLÁUSULA]` — nada aqui toca a oitava cláusula, `red_clause_JMJ_contains`
segue `False`, e o gate não se move. `conjByJ` (operadores, ℂ-linear) e `towerJ`
(vetores, antilinear) continuam **dois J de tipos distintos**; esta pedra é sobre o
segundo, e a cláusula é sobre o primeiro.

⚠ `[PREDICADO SEM DENTE, POR ORA]` — não se exibe aqui subespaço que **falhe**
`JInvariant`. Sem esse dente, o predicado é verdadeiro e ainda pouco informativo:
`⊤` e `⊥` o satisfazem, e é tudo o que se sabe habitar. Fica dito, não disfarçado.

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

variable {P : SiteProfile}

/-! ## A — o habitante -/

/-- [KERNEL] ★★★★★ **J EMPACOTADO**: a conjugação da torre como equivalência
    isométrica conjugado-linear de `TowerHilbert P` — isto é, um habitante do tipo
    que `TGL.ModularRealization` chama `Antiunitary` e declarava vazio.

    Nenhum campo é novo. O que muda é que J deixa de ser função crua e passa a ser
    **termo de um tipo com álgebra**, e por isso o maquinário de subespaços da
    mathlib passa a alcançá-lo. -/
def towerJequiv (P : SiteProfile) :
    TowerHilbert P ≃ₛₗᵢ[starRingEnd ℂ] TowerHilbert P where
  toFun := towerJ P
  map_add' := towerJ_add P
  map_smul' := towerJ_conj_smul P
  invFun := towerJ P
  left_inv := towerJ_involutive P
  right_inv := towerJ_involutive P
  norm_map' := towerJ_norm P

/-- [KERNEL] ★★ **E O EMPACOTAMENTO NÃO TROCOU O OBJETO**: aplicar o termo é
    aplicar a função crua. Sem isto, tudo o que se provasse do termo seria sobre
    outra coisa — o homônimo mora exatamente aqui. -/
theorem towerJequiv_apply (P : SiteProfile) (z : TowerHilbert P) :
    towerJequiv P z = towerJ P z := rfl

/-- [KERNEL] ★★★ **E ELE CONTINUA INVOLUÇÃO COMO TERMO**: `J² = 1` sobrevive ao
    empacotamento. É o custo pago, agora legível pela álgebra. -/
theorem towerJequiv_involutive (P : SiteProfile) :
    Function.Involutive (towerJequiv P) :=
  towerJ_involutive P

/-- [KERNEL] ★★★★ **E O INVERSO É ELE MESMO, POR `rfl`**: `J⁻¹ = J` sai
    DEFINICIONALMENTE do empacotamento, porque `invFun := towerJ P`. É a forma
    algébrica de “J é o próprio inverso” — e o mesmo padrão que o mathlib usa em
    `symm_starₗᵢ`. **A rigidez que o operador nomeou começa aqui**: não há escolha de
    inverso a fazer. -/
theorem towerJequiv_symm (P : SiteProfile) :
    (towerJequiv P).symm = towerJequiv P := rfl

/-! ## B — o SETOR, agora dizível -/

/-- **A J-INVARIÂNCIA DE UM SETOR** — o predicado que não existia. Um subespaço é
    J-invariante quando a conjugação o leva nele mesmo.

    Note que `Submodule.map` aqui é o da mathlib para mapa **semilinear**: é ele que
    o empacotamento destravou. Com `towerJ` cru, esta linha não elaborava. -/
def JInvariant (S : Submodule ℂ (TowerHilbert P)) : Prop :=
  S.map (towerJequiv P).toLinearEquiv.toLinearMap = S

/-- [KERNEL] ★★★★ **O SETOR DOBRA**: aplicar J duas vezes a um subespaço devolve o
    subespaço. A dinâmica de J desce dos vetores aos SETORES, e a involução
    continua involução lá em cima.

    É a ordem do operador — *"fechar o setor na dinâmica de J"* — cumprida no único
    lugar em que ela era cumprível: **a dinâmica desce; o fechamento de um setor
    específico continua sendo uma escolha a fazer.** -/
theorem the_sector_folds (S : Submodule ℂ (TowerHilbert P)) :
    (S.map (towerJequiv P).toLinearEquiv.toLinearMap).map
        (towerJequiv P).toLinearEquiv.toLinearMap = S := by
  ext z
  simp only [Submodule.mem_map]
  constructor
  · rintro ⟨y, ⟨x, hx, rfl⟩, rfl⟩
    have : towerJ P (towerJ P x) = x := towerJ_involutive P x
    simpa [towerJequiv_apply, this] using hx
  · intro hz
    refine ⟨towerJ P z, ⟨z, hz, rfl⟩, ?_⟩
    exact towerJ_involutive P z

/-- [KERNEL] ★★★ **A RÉGUA DO PREDICADO**: para J, uma inclusão só já basta — a
    igualdade vem de graça. Isto é uma propriedade da INVOLUÇÃO, não do subespaço:
    numa dinâmica não-involutiva seria falso. -/
theorem JInvariant_iff_le (S : Submodule ℂ (TowerHilbert P)) :
    JInvariant S ↔ S.map (towerJequiv P).toLinearEquiv.toLinearMap ≤ S := by
  constructor
  · intro h
    rw [h]
  · intro h
    refine le_antisymm h ?_
    intro z hz
    refine ⟨towerJ P z, ?_, towerJ_involutive P z⟩
    exact h ⟨z, hz, rfl⟩

/-- [KERNEL] ★★ **O TODO É J-INVARIANTE** — trivial, e registrado para que o
    predicado não seja vazio. -/
theorem JInvariant_top : JInvariant (⊤ : Submodule ℂ (TowerHilbert P)) := by
  rw [JInvariant_iff_le]
  exact le_top

/-- [KERNEL] ★★ **E O ZERO TAMBÉM** — o outro extremo. Entre os dois, o predicado
    ainda não tem dente: não se exibe aqui setor que FALHE. Fica dito. -/
theorem JInvariant_bot : JInvariant (⊥ : Submodule ℂ (TowerHilbert P)) :=
  Submodule.map_bot _

/-! ## C — ALFA E ÓMEGA CONJUGADO: o primeiro setor não-trivial

> Tipagem do operador (28/08): **“habitante = alfa e ômega conjugado”**.

E ela apontou para o que faltava. O habitante tem `invFun := toFun` — **o começo É o
fim** (`towerJequiv_symm`, por `rfl`) — e **fixa Ω** (`towerJ_fixes_hOmega`, teorema
anterior). Dessas duas, a reta de Ω sai J-invariante de graça, e com ela o predicado
`JInvariant` deixa de ter só os dois extremos.
-/

/-- [KERNEL] ★★ **O HABITANTE FIXA Ω**, agora como termo. -/
theorem towerJequiv_fixes_hOmega (P : SiteProfile) :
    towerJequiv P (hOmega P) = hOmega P :=
  towerJ_fixes_hOmega P

/-- [KERNEL] ★★★★★ **O SETOR DE Ω É J-INVARIANTE** — e é o **primeiro habitante
    não-trivial** de `JInvariant`: nem `⊥`, nem (em dimensão > 1) `⊤`.

    A conta é a tipagem do operador, literal: `J(c·Ω) = c̄·J(Ω) = c̄·Ω`. O escalar
    conjuga; Ω permanece. **Alfa e ômega conjugado.** -/
theorem JInvariant_span_hOmega (P : SiteProfile) :
    JInvariant (Submodule.span ℂ {hOmega P}) := by
  have hfix : (towerJequiv P).toLinearEquiv.toLinearMap (hOmega P) = hOmega P :=
    towerJ_fixes_hOmega P
  show Submodule.map _ (Submodule.span ℂ {hOmega P}) = _
  rw [Submodule.map_span, Set.image_singleton, hfix]

/-- [KERNEL] ★★★ **E ELE NÃO É O ZERO** — porque ⟨Ω,Ω⟩ = 1. Sem isto, o “primeiro
    habitante não-trivial” seria `⊥` outra vez, e o dente não seria dente. -/
theorem the_omega_sector_is_not_bot (P : SiteProfile) :
    Submodule.span ℂ {hOmega P} ≠ (⊥ : Submodule ℂ (TowerHilbert P)) := by
  intro h
  have hmem : hOmega P ∈ Submodule.span ℂ ({hOmega P} : Set (TowerHilbert P)) :=
    Submodule.mem_span_singleton_self _
  rw [h, Submodule.mem_bot] at hmem
  have h1 : inner ℂ (hOmega P) (hOmega P) = (1 : ℂ) := hOmega_inner_self
  rw [hmem] at h1
  simp at h1

end

end TGLExt
