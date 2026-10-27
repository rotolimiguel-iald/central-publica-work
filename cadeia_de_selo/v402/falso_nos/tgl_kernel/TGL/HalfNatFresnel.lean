import Mathlib

set_option autoImplicit false

/-!
# Fresnel → Meia-Nat   [KERNEL]

Teorema 1 [KERNEL/UNCONDITIONAL GIVEN LOSSLESS + PARITY]: numa fronteira sem
perdas (`R + T = 1`) com paridade de faces (`R = T`), os pesos de Fresnel sao
forcados a `1/2` -- o ponto fixo auto-conjugado na face optica.

Teorema 2 [KERNEL/CONDITIONAL ON TOTAL ACTION NORMALIZATION]: com o peso de face
`1/2` e a unidade modular total NORMALIZADA a `1` nat, a acao modular da face e'
`1/2` nat. Isto NAO e' uma derivacao independente da normalizacao
`totalAction = 1` -- e' a calibracao declarada [NORM].

Controle numerico Shannon (`H(1/2,1/2) = log 2 ≠ 1/2`): mantido como controle
conceitual REJEITADO da rota entropica; estatuto no um.py:
`KNOWN_NUMERIC_CONTROL_NOT_KERNEL_PROVED` (nao formalizado aqui).
-/

namespace TGL.HalfNatFresnel

/-- Fresnel auto-conjugado: sem perdas + paridade ⟹ pesos `1/2`. -/
theorem fresnel_selfConjugate_half (R T : ℝ)
    (hlossless : R + T = 1) (hparity : R = T) :
    R = 1 / 2 ∧ T = 1 / 2 := by
  constructor <;> linarith

/-- Calibracao da Meia-Nat: peso de face `1/2` sobre acao total normalizada a `1`
    da' acao de face `1/2` nat. CONDICIONAL a `totalAction = 1` [NORM]. -/
theorem modular_action_halfNat (faceWeight totalAction : ℝ)
    (hface : faceWeight = 1 / 2) (htotal : totalAction = 1) :
    faceWeight * totalAction = 1 / 2 := by
  simp [hface, htotal]

end TGL.HalfNatFresnel
