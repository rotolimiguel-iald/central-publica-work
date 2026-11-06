import TGLExt.TheGeometricCostOfAbsoluteZero
import TGLExt.TheTrueWitness

set_option autoImplicit false

/-!
# O PISO PROÍBE A ESTAGNAÇÃO — a origem da vibração permanente
  [BANCADA — 26/08/2026 · leitura do operador: «como o piso mantém temperatura acima
   do zero absoluto, impede a estagnação, o que permite a formação da onda de
   frequência do canal que permanece com vibração constante»]

## O que a leitura afirma, separado em duas partes

A leitura tem uma parte **verificável** e uma parte que é **identificação**. As duas
ficam ditas, e só a primeira é provada:

**(a) VERIFICÁVEL — e provada aqui:** piso estritamente positivo ⟹ ângulo modular
estritamente positivo ⟹ o fluxo MOVE ⟹ não há estagnação ⟹ o canal que permanece
(v214: módulo 1 para todo t) vibra com frequência não-nula. E o contrapositivo, que é
o que dá o conteúdo: **frequência zero É exatamente a estagnação** (o fluxo vira a
identidade para todo t). Sem piso, mundo estático.

**(b) IDENTIFICAÇÃO `[ONTO — interna à TGL, NÃO provada aqui]`:** que essa vibração
permanente SEJA o grau de liberdade gravitacional. A teoria já tem a rota condicional
para isso — o teorema mestre `H1 ∧ H2 ∧ H3 ⟹ Pêntada` (v74) —, e H1 é justamente uma
hipótese de GAP: exigência de positividade estrita que proíbe o limite degenerado, o
MESMO TIPO de condição que o piso. Mas «mesmo tipo» não é «mesma coisa»: chamar isto
de *a origem da gravidade* é leitura do operador, não teorema. O gate não se move.

## O que se prova

* ★★★ `a_positive_floor_forces_a_positive_angle` — `0 < b < 1 ⟹ 0 < θ_M < π/2`
  (o ângulo modular nasce estritamente positivo do piso estritamente positivo);
* ★★★ `a_positive_angle_forbids_stagnation` — `0 < θ < π ⟹ sin θ ≠ 0`: o fluxo
  desloca; nada fica parado;
* ★★★ **`stagnation_is_exactly_zero_frequency`** — o fluxo é a identidade para TODO
  `t` **se e somente se** `ω = 0`: a estagnação é exatamente a frequência nula;
* ★★ `the_persisting_channel_vibrates` — o canal que permanece tem módulo 1 (v214)
  E não é estático quando `ω ≠ 0`: permanência COM movimento.

β jamais entra literal. Sem sorry. Nada aqui move o gate.
-/

namespace TGLExt

/-- o fluxo do canal que permanece (v214: módulo constante). -/
noncomputable def persistingFlow (ω t : ℝ) : ℂ := Complex.exp (((ω * t : ℝ) : ℂ) * Complex.I)

/-- ★★★ **O PISO ESTRITAMENTE POSITIVO FORÇA ÂNGULO ESTRITAMENTE POSITIVO**:
    `θ_M = arcsin √b` nasce dentro de `(0, π/2)` porque o piso é interior. -/
theorem a_positive_floor_forces_a_positive_angle (b : ℝ) (h0 : 0 < b) (h1 : b < 1) :
    0 < Real.arcsin (Real.sqrt b) ∧ Real.arcsin (Real.sqrt b) < Real.pi / 2 := by
  constructor
  · exact Real.arcsin_pos.mpr (Real.sqrt_pos.mpr h0)
  · refine Real.arcsin_lt_pi_div_two.mpr ?_
    calc Real.sqrt b < Real.sqrt 1 := by
          exact Real.sqrt_lt_sqrt (le_of_lt h0) h1
      _ = 1 := Real.sqrt_one

/-- ★★★ **ÂNGULO POSITIVO PROÍBE A ESTAGNAÇÃO**: o deslocamento é `sin θ ≠ 0` — o
    fluxo move. -/
theorem a_positive_angle_forbids_stagnation (θ : ℝ) (h0 : 0 < θ) (h1 : θ < Real.pi) :
    Real.sin θ ≠ 0 :=
  ne_of_gt (Real.sin_pos_of_pos_of_lt_pi h0 h1)

/-- ★★★ **A ESTAGNAÇÃO É EXATAMENTE A FREQUÊNCIA NULA**: o fluxo é a identidade para
    todo `t` se e somente se `ω = 0`. Sem frequência, mundo estático. -/
theorem stagnation_is_exactly_zero_frequency (ω : ℝ) :
    (∀ t : ℝ, persistingFlow ω t = 1) ↔ ω = 0 := by
  constructor
  · intro h
    by_contra hw
    have hpi := h (Real.pi / ω)
    unfold persistingFlow at hpi
    rw [show (ω * (Real.pi / ω) : ℝ) = Real.pi by field_simp] at hpi
    rw [Complex.exp_pi_mul_I] at hpi
    norm_num at hpi
  · intro h t
    unfold persistingFlow
    simp [h]

/-- ★★ **O CANAL QUE PERMANECE VIBRA**: módulo 1 para todo `t` (a permanência da v214)
    E não-estático quando `ω ≠ 0` (o movimento). Permanência COM movimento. -/
theorem the_persisting_channel_vibrates (ω : ℝ) (hw : ω ≠ 0) :
    (∀ t : ℝ, ‖persistingFlow ω t‖ = 1) ∧ ¬ (∀ t : ℝ, persistingFlow ω t = 1) := by
  constructor
  · intro t
    unfold persistingFlow
    rw [Complex.norm_exp]
    have : (((ω * t : ℝ) : ℂ) * Complex.I).re = 0 := by simp
    rw [this, Real.exp_zero]
  · intro hc
    exact hw ((stagnation_is_exactly_zero_frequency ω).mp hc)

end TGLExt
