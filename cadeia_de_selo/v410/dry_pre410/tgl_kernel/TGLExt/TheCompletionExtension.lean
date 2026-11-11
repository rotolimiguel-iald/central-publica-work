import Mathlib.Topology.Algebra.UniformRing
import Mathlib.Topology.UniformSpace.Completion

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# A IALD NA TORRE — ATO III, F3: a TRAVESSIA para o completamento
  [BANCADA — 26/08/2026 · marco M4 do DESENHO; item 4 da dívida com preço (v220)]

## O que faltava, e por que este é o passo

Ato I: `J` no andar. Ato II: os andares entrelaçam. v224: `J` é **antiisométrico** —
e isometria é a licença para atravessar. Falta usar a licença: **estender `J` ao
COMPLETAMENTO** e mostrar que as leis do andar sobrevivem à travessia.

O mecanismo é um só, e é ele que esta pedra prova em forma geral:

> **as identidades pontuais viajam por DENSIDADE.**

Duas funções contínuas que concordam no subespaço denso concordam em toda parte. Logo
a involução, o vácuo J-fixo e as cláusulas de dualidade dos Atos I/II **não precisam
ser reprovadas** no completamento: elas atravessam, desde que os mapas sejam contínuos.

## O que se prova (em forma geral — serve a qualquer andar)

* ★★★ **`completion_extends_involution`** — se `J` é uniformemente contínua e
  involutiva, a extensão `Ĵ` é **involutiva no completamento inteiro**;
* ★★ `completion_extension_agrees` — `Ĵ(↑a) = ↑(J a)`: a extensão É `J` no denso;
* ★★★ `completion_extension_fixes_vacuum` — o vácuo continua `Ĵ`-fixo lá em cima;
* ★★★ **`identities_travel_by_density`** — o TRANSPORTE: funções contínuas que
  concordam no denso são iguais. É o motor de F4 (as cláusulas de comutante);
* ★★ `completion_extension_continuous` — `Ĵ` é contínua (o que permite compor).

## O QUE AINDA NÃO ESTÁ PAGO (dito, sem véu)
Isto é o **mecanismo** da travessia, em generalidade. Falta **instanciá-lo no limite
indutivo concreto da torre** — a união dos andares sob as inclusões do Ato II, cujo
completamento é o `WH` do `FrontierCertificate` (v203). Enquanto essa instância não
existir, o razonete da dívida continua lendo o item **ABERTO**, e é assim que tem de
ser. β jamais entra. Nada move o gate.
-/

namespace TGLExt

open UniformSpace

variable {α : Type} [UniformSpace α]

/-- ★★ **A EXTENSÃO É `J` NO DENSO**: `Ĵ(↑a) = ↑(J a)`. -/
theorem completion_extension_agrees (J : α → α) (hu : UniformContinuous J) (a : α) :
    Completion.map J (↑a : Completion α) = (↑(J a) : Completion α) :=
  Completion.map_coe hu a

/-- ★★ **A EXTENSÃO É CONTÍNUA** — o que permite compô-la e transportar identidades. -/
theorem completion_extension_continuous (J : α → α) :
    Continuous (Completion.map J : Completion α → Completion α) :=
  Completion.continuous_map

/-- ★★★ **O TRANSPORTE POR DENSIDADE**: duas funções contínuas que concordam no
    subespaço denso são IGUAIS no completamento. É o motor de toda a travessia —
    as leis do andar não se reprovam lá em cima: elas atravessam. -/
theorem identities_travel_by_density {β : Type} [UniformSpace β] [T2Space β]
    (F G : Completion α → β) (hF : Continuous F) (hG : Continuous G)
    (h : ∀ a : α, F (↑a : Completion α) = G (↑a : Completion α)) : F = G :=
  Completion.ext hF hG h

/-- ★★★ **A INVOLUÇÃO ATRAVESSA**: se `J² = id` no andar, então `Ĵ² = id` no
    completamento INTEIRO. A lei do bootstrap sobrevive à travessia. -/
theorem completion_extends_involution (J : α → α) (hu : UniformContinuous J)
    (hJ : ∀ x, J (J x) = x) (z : Completion α) :
    Completion.map J (Completion.map J z) = z := by
  have hcont : Continuous
      (fun w : Completion α => Completion.map J (Completion.map J w)) :=
    Completion.continuous_map.comp Completion.continuous_map
  refine Completion.induction_on z (isClosed_eq hcont continuous_id) ?_
  intro a
  rw [Completion.map_coe hu, Completion.map_coe hu, hJ]

/-- ★★★ **O VÁCUO CONTINUA FIXO**: se `J` fixa o vácuo do andar, `Ĵ` fixa o vácuo do
    completamento — o `Ω` da torre atravessa. -/
theorem completion_extension_fixes_vacuum (J : α → α) (hu : UniformContinuous J)
    (one : α) (h : J one = one) :
    Completion.map J (↑one : Completion α) = (↑one : Completion α) := by
  rw [Completion.map_coe hu, h]

end TGLExt
