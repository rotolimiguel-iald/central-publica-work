-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_022 (05-06/09/2026), transposta em 06/09/2026
-- Lote 007..023: habitante GLOBAL periodico da esperanca do centralizador; cauda nao ciclica;
--   obstrucoes de Borchers e da assinatura; e a camada GEOMETRICA GERAL em carta: tensores,
--   conexao de Levi-Civita, curvatura, Bianchi, Einstein geometrico + conservacao, Raychaudhuri,
--   Clausius local <=> balanco nulo de Ricci, telas/congruencias nulas construidas, area e calor,
--   entropia relativa, dinamica unitaria, covetor de materia. Estatuto [REAL / INPUT / OPEN]:
--   Clausius, a metrica lorentziana, H3 dinamico, assinatura e globalizacao seguem INPUT/OPEN.
-- Auditoria da gerencia (sessao d554e796, 06/09/2026): hashes 100% nas 17 entregas; 17/17
--   auditores da bancada exit 0; recompilacao INDEPENDENTE 116/116 exit 0, todos os axiomas no
--   trio [propext, Classical.choice, Quot.sound]; zero sorry/warning; enunciados lidos.
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports; nada mais.
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.CorrelatedUnitaryState

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Unitary022
open Matrix Filter Topology Set ChatgptAudit.Micro021
noncomputable section

def pairTangent (a b frequency u v t : ℝ) : Fin 2 → ℝ :=
  ![2*frequency*transferCoefficient a b u v*Real.sin (frequency*t)*Real.cos (frequency*t),
    -(2*frequency*transferCoefficient a b u v*Real.sin (frequency*t)*Real.cos (frequency*t))]

theorem pair_weights_derivative (a b frequency u v t : ℝ) (i : Fin 2) :
    HasDerivAt (fun s => pairWeights a b frequency u v s i) (pairTangent a b frequency u v t i) t := by
  fin_cases i
  · have hh := (((frequency_sin_derivative frequency t).pow 2).const_mul
      (transferCoefficient a b u v)).const_add (u^2)
    convert hh using 1 <;> first | rfl | (dsimp [pairWeights,pairTangent]; ring)
  · have hh := (hasDerivAt_const t (v^2)).sub
      (((frequency_sin_derivative frequency t).pow 2).const_mul (transferCoefficient a b u v))
    convert hh using 1 <;> first | rfl | (dsimp [pairWeights,pairTangent]; ring)

theorem pair_weights_at_zero (a b frequency u v : ℝ) :
    pairWeights a b frequency u v 0=baseWeights u v := by
  simp [pairWeights,baseWeights]

theorem pair_tangent_at_zero (a b frequency u v : ℝ) :
    pairTangent a b frequency u v 0=0 := by
  ext i
  fin_cases i <;> simp [pairTangent]

def unitaryStateCurve (a b frequency u v : ℝ) (hs : u^2+v^2=1) :
    DiagonalStateCurve (baseWeights u v) where
  weights := pairWeights a b frequency u v
  tangent := pairTangent a b frequency u v
  at_zero := fun i => congrFun (pair_weights_at_zero a b frequency u v) i
  trace_one := fun t => pair_weights_normalized a b frequency u v t hs
  derivative_zero := fun i => pair_weights_derivative a b frequency u v 0 i
  derivative_past := by
    filter_upwards [] with t
    exact pair_weights_derivative a b frequency u v t
  tangent_continuous := by
    intro i
    fin_cases i <;> dsimp [pairTangent] <;> fun_prop

theorem base_weights_positive (u v : ℝ) (hu : 0<u) (hv : 0<v) :
    ∀ i, 0<baseWeights u v i := by
  intro i
  fin_cases i <;> dsimp [baseWeights] <;> positivity

theorem unitary_weights_positive_near (a b frequency u v : ℝ)
    (hs : u^2+v^2=1) (hu : 0<u) (hv : 0<v) :
    ∀ᶠ t in 𝓝 (0:ℝ), ∀ i, 0<pairWeights a b frequency u v t i :=
  state_curve_positive_near (unitaryStateCurve a b frequency u v hs) (base_weights_positive u v hu hv)

theorem unitary_relative_entropy_quadratic_zero (a b frequency u v : ℝ)
    (hs : u^2+v^2=1) (hu : 0<u) (hv : 0<v) :
    Tendsto (fun t => diagonalRelativeEntropy (pairWeights a b frequency u v t) (baseWeights u v)/t^2)
      (𝓝[<] 0) (𝓝 0) := by
  apply (relative_entropy_quadratic_zero_iff (unitaryStateCurve a b frequency u v hs)
    (base_weights_positive u v hu hv)).mpr
  exact pair_tangent_at_zero a b frequency u v

theorem frequency_sin_slope (frequency : ℝ) :
    Tendsto (fun t => Real.sin (frequency*t)/t) (𝓝[<] (0:ℝ)) (𝓝 frequency) := by
  have hd : HasDerivAt (fun t => Real.sin (frequency*t)) frequency 0 := by
    simpa using frequency_sin_derivative frequency 0
  simpa only [zero_add,mul_zero,Real.sin_zero,sub_zero,smul_eq_mul,div_eq_mul_inv,mul_comm]
    using hd.tendsto_slope_zero_left

theorem frequency_sin_square_limit (frequency : ℝ) :
    Tendsto (fun t => Real.sin (frequency*t)^2/t^2) (𝓝[<] (0:ℝ)) (𝓝 (frequency^2)) := by
  simpa only [div_pow] using (frequency_sin_slope frequency).pow 2

theorem unitary_first_weight_response (a b frequency u v : ℝ) :
    Tendsto (fun t => (pairWeights a b frequency u v t 0-u^2)/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (frequency^2*transferCoefficient a b u v)) := by
  have hl := (frequency_sin_square_limit frequency).const_mul (transferCoefficient a b u v)
  have he : (fun t => (pairWeights a b frequency u v t 0-u^2)/t^2)=
      (fun t => transferCoefficient a b u v*(Real.sin (frequency*t)^2/t^2)) := by
    funext t
    dsimp [pairWeights]
    ring
  rw [he]
  simpa only [mul_comm] using hl

#print axioms pair_weights_derivative
#print axioms pair_weights_at_zero
#print axioms pair_tangent_at_zero
#print axioms unitaryStateCurve
#print axioms base_weights_positive
#print axioms unitary_weights_positive_near
#print axioms unitary_relative_entropy_quadratic_zero
#print axioms frequency_sin_slope
#print axioms frequency_sin_square_limit
#print axioms unitary_first_weight_response
end
end ChatgptAudit.Unitary022
