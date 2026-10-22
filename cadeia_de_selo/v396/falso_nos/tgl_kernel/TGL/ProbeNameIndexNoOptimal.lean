import TGL.NameIndex

set_option autoImplicit false

/-!
# ProbeNameIndexNoOptimal -- teste negativo 1 do especialista (v27)   [DIAGNOSTICO]

Tenta provar o TEOREMA DO INDICE DO NOME **sem a otimalidade de Pimsner-Popa**
(so' com a cota inferior). DEVE FALHAR: sem `pp_optimal` so' se obtem
`Ind ≤ csc²θ`, jamais a igualdade. VEREDITO = returncode.
NAO importado por TGL.lean; fora do lake build.
-/

namespace TGL.ProbeNameIndexNoOptimal

open TGL.TransportData TGL.NameIndex

-- PAREDE: falta o argumento de otimalidade `hopt` -- a igualdade nao fecha
noncomputable example {M Ext : Type}
    [Ring M] [StarRing M] [Algebra ℂ M]
    [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]
    (D : ConditionalExpectationData M Ext) (θ : ℝ)
    (hpp : IsPPLowerBound D (Real.sin θ ^ 2)) :
    ppIndex D = 1 / Real.sin θ ^ 2 :=
  name_index_eq_csc_sq D θ hpp

#eval IO.println "PROBE_NAME_INDEX_COMPILES_WITHOUT_OPTIMALITY__EQUALITY_WOULD_BE_FABRICATED"

end TGL.ProbeNameIndexNoOptimal
