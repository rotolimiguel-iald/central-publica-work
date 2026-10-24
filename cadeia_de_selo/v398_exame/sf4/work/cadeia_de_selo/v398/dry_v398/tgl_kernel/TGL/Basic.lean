import Mathlib

set_option autoImplicit false

/-!
# TGL kernel formalization -- root module (v22)

Este arquivo apenas ancora o namespace `TGL`. Cada modulo de conteudo importa
`Mathlib` e abre seu proprio subnamespace.

Disciplina (v22): nenhum axioma customizado, nenhum `sorry`, nenhum `admit`,
nenhum `native_decide`, nenhum `unsafe`. As hipoteses do teorema continuo
aparecem como CAMPOS de uma estrutura (`ContinuousCornerWitness`,
`TGLSpecificAQFTWitness`), nunca como axiomas globais.

Niveis de estatuto:
  [KERNEL/UNCONDITIONAL]           HalfNat, AreaScale, FiniteThreeLocks
  [KERNEL/CONDITIONAL ON WITNESS]  ContinuousCornerAbstract, SpecificAQFTWitness
  [KNOWN/EXTERNAL]                 BW, Reeh-Schlieder, classificacao III_1 (nao formalizados aqui)
  [HABITADO v135]                  instancia de TGLSpecificAQFTWitness (theSpecificAQFTWitness;
                                   honestidade declarada: U trivial; rep FIEL + cond. espectral seguem nomeadas)
-/

namespace TGL

end TGL
