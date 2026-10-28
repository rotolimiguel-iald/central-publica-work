import TGL.ModularRealization

set_option autoImplicit false

/-!
# ProbeFiniteFullWitness -- controle negativo do v24   [DIAGNOSTICO]

Tenta montar `TGLModularRealization` sobre um Hilbert de DIMENSAO FINITA --
na formulacao mais afiada: mesmo dadas TODAS as outras camadas como hipoteses,
a finitude SOZINHA deve bloquear (campo `infiniteHilbert : ¬ FiniteDimensional`).
NAO importado por TGL.lean; fora do lake build. VEREDITO = returncode.

Honestidade: a falha deste probe NAO afirma `TYPE_III1_PROVED` -- dimensao
infinita e' condicao NECESSARIA, nao suficiente, para tipo III_1.
-/

namespace TGL.ProbeFiniteFullWitness

open TGL.SpecificAQFT TGL.ModularRealization

/-- PAREDE: fornecemos `FiniteDimensional` exatamente onde o tipo exige a negacao. -/
noncomputable example (W : TGLSpecificAQFTWitness) (hfin : FiniteDimensional ℂ W.H)
    (D : WedgeModularData W) (C : ContinuousCoreData W D)
    (T : ThreeLocksCoreData W D C) :
    TGLModularRealization W where
  infiniteHilbert := hfin
  modular := D
  core := C
  threeLocks := T

#eval IO.println "PROBE_FINITE_FULL_WITNESS_COMPILES__TYPE_ADMITS_FINITE_MODEL"

end TGL.ProbeFiniteFullWitness
