import WeightedSchwartzPlancherelR3

/-! Angular Fourier first moment with its exact (2 pi)^dimension factor.
The raw angular integral is not silently normalized as an isometry. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.WeightedPlancherel
open MeasureTheory FourierTransform SchwartzMap Module
open scoped FourierTransform LineDeriv
variable {V H : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
  [FiniteDimensional ℝ V] [MeasurableSpace V] [BorelSpace V]
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem weighted_forward_parseval (f g : 𝓢(V,H)) (m : V) :
    (∫x,(inner ℝ x m:ℂ)*inner ℂ (𝓕 f x) (𝓕 g x))=
      (-Complex.I/(2*Real.pi:ℝ))*∫p,inner ℂ (f p) ((∂_{m} g) p) := by
  have ht : (fun x : V=>inner ℝ x m).HasTemperateGrowth := by fun_prop
  have hp:=integral_inner_fourier_fourier f (∂_{m} g)
  rw [SchwartzMap.fourier_lineDerivOp_eq] at hp
  have he : (∫x,inner ℂ (𝓕 f x)
      (((2*Real.pi*Complex.I) • SchwartzMap.smulLeftCLM H
        (fun x : V=>inner ℝ x m) (𝓕 g)) x))=
      (2*Real.pi*Complex.I) *
        ∫x,(inner ℝ x m:ℂ)*inner ℂ (𝓕 f x) (𝓕 g x) := by
    simp only [SchwartzMap.smul_apply,SchwartzMap.smulLeftCLM_apply_apply ht,
      ←Complex.coe_smul,inner_smul_right,mul_assoc,integral_const_mul]
  rw [he] at hp
  rw [←hp]
  have hc : (-Complex.I/(2*Real.pi:ℝ)) * (2*Real.pi*Complex.I)=(1:ℂ) := by
    push_cast
    field_simp [Real.pi_ne_zero]
    simp [Complex.I_sq]
  rw [←mul_assoc,hc,one_mul]

theorem linear_weight_dilation (F : V→ℂ) (m : V) (c : ℝ) (hc : 0<c) :
    (∫x,(inner ℝ x m:ℂ)*F (c⁻¹ • x))=
      (c^(finrank ℝ V+1):ℝ) • ∫x,(inner ℝ x m:ℂ)*F x := by
  have he (x : V) : (inner ℝ x m:ℂ)*F (c⁻¹ • x)=
      c • ((inner ℝ (c⁻¹ • x) m:ℂ)*F (c⁻¹ • x)) := by
    rw [real_inner_smul_left]
    push_cast
    rw [←Complex.coe_smul,smul_eq_mul]
    field_simp [hc.ne']
  simp_rw [he]
  rw [integral_smul,Measure.integral_comp_inv_smul_of_nonneg volume _ hc.le,smul_smul]
  congr 1
  rw [pow_succ,mul_comm]

def angularForward (f : 𝓢(V,H)) (x : V) : H := 𝓕 f ((2*Real.pi)⁻¹ • x)

theorem angular_weighted_parseval (f g : 𝓢(V,H)) (m : V) :
    (∫x,(inner ℝ x m:ℂ)*inner ℂ (angularForward f x) (angularForward g x))=
      (-Complex.I*(2*Real.pi:ℝ)^(finrank ℝ V))*
        ∫p,inner ℂ (f p) ((∂_{m} g) p) := by
  have hc : 0<2*Real.pi := by positivity
  unfold angularForward
  rw [linear_weight_dilation (fun x=>inner ℂ (𝓕 f x) (𝓕 g x)) m _ hc,
    weighted_forward_parseval,←Complex.coe_smul,smul_eq_mul]
  push_cast
  rw [pow_succ]
  field_simp [Real.pi_ne_zero]

end F1Fecho.WeightedPlancherel
#print axioms F1Fecho.WeightedPlancherel.weighted_forward_parseval
#print axioms F1Fecho.WeightedPlancherel.linear_weight_dilation
#print axioms F1Fecho.WeightedPlancherel.angular_weighted_parseval
