[REAL — consulta complementar durante correção, posterior à ficha inicial]

20260915_152838_290800
Fonte: C:\IALD\Central de Patentes\Chatgpt\B1_PRIME_012\kernel\.lake\packages\mathlib\Mathlib\Algebra\Module\Torsion\Free.lean
SHA256 lido: 9526ec76a1baa5ba033282df9488540720a0247a50567a470b06b99556b311a3

93: 
94: variable [IsCancelMulZero R]
95: 
96: lemma IsSMulRegular.of_ne_zero (hr : r ≠ 0) : IsSMulRegular M r :=
97:   (IsRegular.of_ne_zero hr).isSMulRegular
98: 
99: variable (M) in
100: lemma smul_right_injective (hr : r ≠ 0) : ((r • ·) : M → M).Injective :=
101:   (IsRegular.of_ne_zero hr).smul_right_injective _
102: 

O parâmetro M de smul_right_injective é explícito; consumo com M=X→Complex. Esta consulta corrigiu elaboração, sem mudar alvo, hipóteses ou enunciado. A ficha inicial permanece intacta.
