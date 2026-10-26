import Mathlib

/-! Exact first-moment Plancherel formula in the mathlib 2-pi convention.
This fixes the Fourier coefficient before any null-plane charge consumer. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.WeightedPlancherel
open MeasureTheory FourierTransform SchwartzMap
open scoped FourierTransform LineDeriv
variable {V H : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
  [FiniteDimensional ℝ V] [MeasurableSpace V] [BorelSpace V]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem inverse_parseval (f g : 𝓢(V,H)) :
    (∫x,inner ℂ (𝓕⁻ f x) (𝓕⁻ g x))=∫p,inner ℂ (f p) (g p) := by
  simpa using (integral_inner_fourier_fourier (𝓕⁻ f) (𝓕⁻ g)).symm

theorem weighted_inverse_parseval (f g : 𝓢(V,H)) (m : V) :
    (∫x,(inner ℝ x m:ℂ)*inner ℂ (𝓕⁻ f x) (𝓕⁻ g x))=
      (Complex.I/(2*Real.pi:ℝ))*∫p,inner ℂ (f p) ((∂_{m} g) p) := by
  have ht : (fun x : V=>inner ℝ x m).HasTemperateGrowth := by fun_prop
  have hp:=inverse_parseval f (∂_{m} g)
  rw [SchwartzMap.fourierInv_lineDerivOp_eq] at hp
  have he : (∫x,inner ℂ (𝓕⁻ f x)
      ((-(2*Real.pi*Complex.I) • SchwartzMap.smulLeftCLM H
        (fun x : V=>inner ℝ x m) (𝓕⁻ g)) x))=
      (-(2*Real.pi*Complex.I)) *
        ∫x,(inner ℝ x m:ℂ)*inner ℂ (𝓕⁻ f x) (𝓕⁻ g x) := by
    simp only [SchwartzMap.smul_apply,SchwartzMap.smulLeftCLM_apply_apply ht,
      inner_smul_right,inner_smul_right_real,←mul_assoc,integral_const_mul]
  rw [he] at hp
  rw [←hp]
  have hc : (Complex.I/(2*Real.pi:ℝ)) * (-(2*Real.pi*Complex.I))=(1:ℂ) := by
    push_cast
    field_simp [Real.pi_ne_zero]
    simp [Complex.I_sq]
  rw [←mul_assoc,hc,one_mul]

end F1Fecho.WeightedPlancherel
#print axioms F1Fecho.WeightedPlancherel.inverse_parseval
#print axioms F1Fecho.WeightedPlancherel.weighted_inverse_parseval
