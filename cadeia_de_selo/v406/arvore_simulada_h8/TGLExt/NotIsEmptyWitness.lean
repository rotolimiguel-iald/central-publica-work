import TGLExt.WedgeNet
import TGLExt.V354RegularLegacyWitness

set_option autoImplicit false

/-!
# O HABITANTE REFUTA A VACUIDADE: `¬ IsEmpty` das duas testemunhas  [TGLExt — v370, pedra da gerência]

As notas do um.py de época v23 (o `zero_abs_note` do ledger, o `not_claimed` de
`prove_interface_is_light` e a linha `0_abs` do markdown) diziam que
`IsEmpty(TGLSpecificAQFTWitness)` / `IsEmpty(FullTGLWitness)` "jamais foi demonstrado nem refutado".
Desde a v135 (`TGLExt.theSpecificAQFTWitness`, WedgeNet.lean) e desde a v354
(`TGLV354.TraceCompletion.regularFullWitness`, V354RegularLegacyWitness.lean, escopo regular) os
dois tipos estão HABITADOS, e um habitante refuta `IsEmpty` em uma linha.

O que esta pedra NÃO faz: não afirma 0_abs; não constrói o representante CANÔNICO
(`canonicalFullTGLWitness` segue [OPEN], errata v367); não move gate. `zero_abs_proved` continua
False porque a proposição do ledger (IsEmpty do tipo habitado) é FALSA.

HOMÔNIMO, dito: o 0_abs da caixa vazia (a terceira lei: `absolute_zero_unreachable_in_finite_time`,
ForbiddenBoundary.lean; `finite_reaching_protocol_exists = False` em `prove_absolute_zero_empty_box`)
é OUTRA proposição, e esta pedra não fala dela.

Origem: `W6_NotIsEmptyWitness.lean` (frente W6, sha16 203de9da849451e4), compilado isolado com
`lake env lean` a partir da pasta do kernel, os três no trio; recompilado pelo cético W6. A
transposição muda só o namespace (`W6Patches` → `TGLExt.NotIsEmptyWitness`) e este docstring.
-/

namespace TGLExt.NotIsEmptyWitness

open TGL.SpecificAQFT TGL.ModularRealization

/-- `IsEmpty TGLSpecificAQFTWitness` é FALSO: o tipo tem habitante (v135). -/
theorem not_isEmpty_TGLSpecificAQFTWitness : ¬ IsEmpty TGLSpecificAQFTWitness :=
  fun h => h.false TGLExt.theSpecificAQFTWitness

/-- `IsEmpty FullTGLWitness` é FALSO no escopo regular (v354): `regularFullWitness` é um TERMO
    do Σ-tipo, não um `Nonempty` nem uma bandeira. -/
theorem not_isEmpty_FullTGLWitness : ¬ IsEmpty FullTGLWitness :=
  fun h => h.false TGLV354.TraceCompletion.regularFullWitness

/-- a mesma coisa lida pelo lado positivo. -/
theorem nonempty_TGLSpecificAQFTWitness : Nonempty TGLSpecificAQFTWitness :=
  ⟨TGLExt.theSpecificAQFTWitness⟩

end TGLExt.NotIsEmptyWitness

#print axioms TGLExt.NotIsEmptyWitness.not_isEmpty_TGLSpecificAQFTWitness
#print axioms TGLExt.NotIsEmptyWitness.not_isEmpty_FullTGLWitness
#print axioms TGLExt.NotIsEmptyWitness.nonempty_TGLSpecificAQFTWitness
