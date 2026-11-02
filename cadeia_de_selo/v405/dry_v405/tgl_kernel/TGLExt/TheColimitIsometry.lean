import TGLExt.TheProfileIsometry
import TGLExt.TheColimitDuality

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A ISOMETRIA NO COLIMITE — o degrau que autoriza a última dobra
  [BANCADA — 26/08/2026 · marco M4 · ordem «pague»]

## Por que este degrau, e não outro

A dobra que resta é a **extensão ao completamento**. Ela é autorizada por **uma** coisa:
a conjugação ser **uniformemente contínua** — e isso vem da **isometria**. A v234 provou
a isometria **no andar**, contra `tInner`. Aqui ela sobe ao **colimite**, contra
`innerPre`, que é o produto interno de que o completamento se faz.

A prova é a mesma que já se usou três vezes nesta arquitetura, e é a razão de a
comutação com o empurrão ter sido provada tão cedo: leva-se os dois pontos a um andar
comum, aplica-se a isometria do andar, e volta-se.

## O que se prova

* ★★★ **`profileJpre_anti_isometric`** — `⟨J x, J y⟩ = conj ⟨x, y⟩` **no colimite
  inteiro**, contra o produto interno de que o completamento se faz.

## O QUE ISTO AUTORIZA (e o que ainda não)
Autoriza: `J` é isométrica no pré-espaço, logo **uniformemente contínua**, logo
**estende-se ao completamento** pelo mecanismo já provado (v225) — e as identidades
pontuais (involução, vácuo, dualidade) **viajam por densidade**. NÃO autoriza ainda: as
cláusulas do certificado, que falam de **operadores contínuos** e do **BICOMUTANTE**.
A dobra restante continua restante. β jamais entra. Nada move o gate.
-/

namespace TGLExt

open Matrix

variable {P : SiteProfile}

/-- ★★★ **A ISOMETRIA NO COLIMITE**: `⟨J x, J y⟩ = conj ⟨x, y⟩` na torre inteira. -/
theorem profileJpre_anti_isometric (P : SiteProfile) (x y : TowerPre P) :
    innerPre P (profileJpre P x) (profileJpre P y)
      = star (innerPre P x y) := by
  obtain ⟨N, a, rfl⟩ := exists_tof x
  obtain ⟨M, b, rfl⟩ := exists_tof y
  have hN : N ≤ N ⊔ M := le_sup_left
  have hM : M ≤ N ⊔ M := le_sup_right
  rw [profileJpre_tof, profileJpre_tof, innerPre_tof_at hN hM,
      innerPre_tof_at hN hM, profileJ_commutes_with_tPush P hN a,
      profileJ_commutes_with_tPush P hM b, profileJ_is_anti_isometric]

end TGLExt
