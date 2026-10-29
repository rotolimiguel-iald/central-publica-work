import TGLExt.IsotoneNet

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 400000

/-!
# A REDE DISPARA O CANTO: as linhas que nunca foram escritas
  [TGLExt — a errata contra o escriba, feita de teoremas de uma linha]

## O que a varredura mediu

Uma varredura adversarial de sete agentes mediu, com contagem reversa de
consumidores, que os três teoremas de transporte do canto existem e **quase
nunca são aplicados**:

* `HilbertHomeData.PF_external_covariant` — **ZERO consumidores**;
* `HilbertHomeData.PF_isotone` — **ZERO consumidores**;
* `HilbertHomeData.PF_internal_fix` — **UM** consumidor, e intra-espaço.

E que a string `PF` ocorre **zero vezes** em `IsotoneNet.lean` e nos outros sete
habitantes de rede. Isto é: **o maquinário do canto e os habitantes da rede são
dois ramos que nunca se tocam** — embora `theIsotoneNet` forneça exatamente os
entrelaçamentos que aqueles teoremas consomem.

O escriba, tendo lido a estrutura e o habitante, afirmou que «os cantos são uma
rede». **Era ponte POTENCIAL vendida como ATUAL** — o mesmo defeito que ele havia
posto um cético para caçar, cometido na mesma hora.

Esta pedra corrige do único modo que corrige: **escrevendo as linhas que
faltavam**. Nenhuma delas tem prova própria; cada uma é a aplicação de um teorema
que já existia a um habitante que já existia.

## O que fica provado `[REAL]`

* ★★★★ `the_net_corners_are_isotone` — na rede CONCRETA, o canto da fibra maior
  **fixa** a imagem de todo vetor do núcleo da fibra menor. É `PF_isotone`
  disparado, pela primeira vez, sobre fibras genuinamente distintas;
* ★★★ `the_net_corner_is_externally_covariant` — o canto é covariante sob o flip;
* ★★★ `the_net_corner_is_internally_fixed` — o fluxo interno fixa o canto;
* ★★ `the_net_inclusion_is_not_surjective` e `the_net_group_is_nontrivial` — os
  DENTES, re-expostos: sem eles a rede seria degenerada e as três aplicações acima
  seriam vazias.

## Estatuto

`[REAL]` — os cinco, provados aqui por aplicação direta.

`[HONESTIDADE]` — isto **não** cria matemática nova: transforma ponte potencial em
ponte atual. O mérito, se há, é ter **medido a ausência** em vez de a declarar.

`[OPEN]` — e a fronteira não se move: `ker H3L` (em `EuclideanSpace`) e o `P_F` do
core (sobre `C.Core`) seguem **sem morfismo declarado** para esta rede. A varredura
não achou nenhum, e desta vez a ausência foi medida por contagem reversa, não por
relance.

Nenhum teorema acende nome reservado nem `gpf_`. O gate NÃO se move.
β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

/-! ## A — a isotonia, disparada na rede concreta -/

/-- [KERNEL] ★★★★ **O CANTO DA FIBRA MAIOR FIXA A IMAGEM DA MENOR**, na rede
    concreta de fibras de ℓ². É `PF_isotone` aplicado a `theIsotoneNet` — a
    aplicação que a varredura mediu como inexistente. -/
theorem the_net_corners_are_isotone {n m : ℕ} (h : n ≤ m)
    {x : fiber n} (hx : x ∈ (theIsotoneNet.net.locks n).ker) :
    theIsotoneNet.net.PF m ((theIsotoneNet.net.incl h) x)
      = (theIsotoneNet.net.incl h) x :=
  theIsotoneNet.net.PF_isotone h hx

/-! ## B — a covariância externa e a fixação interna, disparadas -/

/-- [KERNEL] ★★★ o canto da rede é COVARIANTE sob o grupo externo (o flip). -/
theorem the_net_corner_is_externally_covariant (g : Bool) (n : ℕ)
    (y : fiber (theIsotoneNet.net.act g n)) :
    theIsotoneNet.net.PF (theIsotoneNet.net.act g n) y
      = (theIsotoneNet.net.external g n)
          (theIsotoneNet.net.PF n ((theIsotoneNet.net.external g n).symm y)) :=
  theIsotoneNet.net.PF_external_covariant g n y

/-- [KERNEL] ★★★ o fluxo interno FIXA o canto da rede. -/
theorem the_net_corner_is_internally_fixed (n : ℕ) (s : ℝ) (x : fiber n) :
    theIsotoneNet.net.PF n ((theIsotoneNet.net.internal n s) x)
      = (theIsotoneNet.net.internal n s) (theIsotoneNet.net.PF n x) :=
  theIsotoneNet.net.PF_internal_fix n s x

/-! ## C — os dentes, re-expostos -/

/-- [KERNEL] ★★ O DENTE DA ISOTONIA: a inclusão da rede é genuinamente
    NÃO-sobrejetiva. Sem ele, as fibras poderiam ser todas a mesma e a isotonia
    acima não diria nada. -/
theorem the_net_inclusion_is_not_surjective :
    ∃ (O₁ O₂ : ℕ) (hle : O₁ ≤ O₂),
      ¬ Function.Surjective (theIsotoneNet.net.incl hle) :=
  theIsotoneNet.genuinely_isotone

/-- [KERNEL] ★★ O DENTE DA COVARIÂNCIA: o grupo externo é genuinamente
    não-trivial. Sem ele, a covariância seria a identidade. -/
theorem the_net_group_is_nontrivial : Nontrivial theIsotoneNet.net.G :=
  theIsotoneNet.external_nontrivial

end TGLExt
