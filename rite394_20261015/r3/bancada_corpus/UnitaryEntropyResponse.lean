import UnitaryMarginalDynamics

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Unitary022
open Matrix Filter Topology Set ChatgptAudit.Micro021
noncomputable section

def unitaryResponse (a b frequency u v : ℝ) : ℝ :=
  frequency^2*transferCoefficient a b u v*Real.log (v^2/u^2)

theorem unitary_modular_increment (a b frequency u v t : ℝ) (hu : 0<u) (hv : 0<v) :
    modularIncrement (baseWeights u v) (pairWeights a b frequency u v t)=
      transferCoefficient a b u v*Real.sin (frequency*t)^2*Real.log (v^2/u^2) := by
  rw [Real.log_div (pow_ne_zero 2 (ne_of_gt hv)) (pow_ne_zero 2 (ne_of_gt hu))]
  simp only [modularIncrement,Fin.sum_univ_two,baseWeights,pairWeights,
    Matrix.cons_val_zero,Matrix.cons_val_one]
  ring

theorem unitary_modular_quadratic_limit (a b frequency u v : ℝ) (hu : 0<u) (hv : 0<v) :
    Tendsto (fun t => modularIncrement (baseWeights u v) (pairWeights a b frequency u v t)/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (unitaryResponse a b frequency u v)) := by
  have hl := ((frequency_sin_square_limit frequency).const_mul
    (transferCoefficient a b u v)).mul_const (Real.log (v^2/u^2))
  have he : (fun t => modularIncrement (baseWeights u v) (pairWeights a b frequency u v t)/t^2)=
      (fun t => (transferCoefficient a b u v*(Real.sin (frequency*t)^2/t^2))*Real.log (v^2/u^2)) := by
    funext t
    rw [unitary_modular_increment a b frequency u v t hu hv]
    ring
  rw [he]
  simpa only [unitaryResponse,mul_comm] using hl

theorem unitary_entropy_quadratic_limit (a b frequency u v : ℝ)
    (hs : u^2+v^2=1) (hu : 0<u) (hv : 0<v) :
    Tendsto (fun t => (finiteEntropy (pairWeights a b frequency u v t)-finiteEntropy (baseWeights u v))/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (unitaryResponse a b frequency u v)) := by
  have hl := (unitary_modular_quadratic_limit a b frequency u v hu hv).sub
    (unitary_relative_entropy_quadratic_zero a b frequency u v hs hu hv)
  have he : (fun t => (finiteEntropy (pairWeights a b frequency u v t)-finiteEntropy (baseWeights u v))/t^2)=
      (fun t => modularIncrement (baseWeights u v) (pairWeights a b frequency u v t)/t^2-
        diagonalRelativeEntropy (pairWeights a b frequency u v t) (baseWeights u v)/t^2) := by
    funext t
    rw [relative_entropy_identity]
    ring
  rw [he]
  simpa only [sub_zero] using hl

theorem unitary_marginal_modular_trace (a b frequency u v t : ℝ) (h : a^2+b^2=1) :
    (modularIncrement (baseWeights u v) (pairWeights a b frequency u v t):ℂ)=
      Matrix.trace ((partialTraceRight (correlatedDensity (evolvedPair a b frequency u v t))-
        Matrix.diagonal (fun i => (baseWeights u v i:ℂ)))*diagonalModularGenerator (baseWeights u v)) := by
  rw [correlated_right_reduction _ _ (pair_amplitude_weights a b frequency u v t h)]
  have hm := modular_increment_is_generator_trace (baseWeights u v) (pairWeights a b frequency u v t)
  have he : Matrix.diagonal (fun i => ((pairWeights a b frequency u v t i-baseWeights u v i:ℝ):ℂ))=
      Matrix.diagonal (fun i => (pairWeights a b frequency u v t i:ℂ))-
        Matrix.diagonal (fun i => (baseWeights u v i:ℂ)) := by
    ext i j
    by_cases hij : i=j
    · subst j
      simp
    · simp [Matrix.diagonal_apply_ne _ hij]
  rw [he] at hm
  exact hm

theorem unitary_heat_error_limit (a b frequency u v rate : ℝ)
    (hs : u^2+v^2=1) (hu : 0<u) (hv : 0<v) (heat : ℝ → ℝ) (coefficient : ℝ)
    (hq : Tendsto (fun t => heat t/t^2) (𝓝[<] (0:ℝ)) (𝓝 coefficient)) :
    Tendsto (fun t => microscopicHeatError (unitaryStateCurve a b frequency u v hs) rate heat t/t^2)
      (𝓝[<] (0:ℝ)) (𝓝 (coefficient-rate/(2*Real.pi)*unitaryResponse a b frequency u v)) := by
  have hl := hq.sub ((unitary_modular_quadratic_limit a b frequency u v hu hv).const_mul
    (rate/(2*Real.pi)))
  have he : (fun t => microscopicHeatError (unitaryStateCurve a b frequency u v hs) rate heat t/t^2)=
      (fun t => heat t/t^2-rate/(2*Real.pi)*
        (modularIncrement (baseWeights u v) (pairWeights a b frequency u v t)/t^2)) := by
    funext t
    dsimp [microscopicHeatError,unitaryStateCurve]
    ring
  rw [he]
  exact hl

#print axioms unitary_modular_increment
#print axioms unitary_modular_quadratic_limit
#print axioms unitary_entropy_quadratic_limit
#print axioms unitary_marginal_modular_trace
#print axioms unitary_heat_error_limit
end
end ChatgptAudit.Unitary022
