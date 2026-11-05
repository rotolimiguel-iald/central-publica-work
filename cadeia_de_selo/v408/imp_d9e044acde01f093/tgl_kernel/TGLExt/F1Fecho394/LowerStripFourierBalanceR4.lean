import TGLExt.F1Fecho394.LowerGaussianContourR2

/-! The contour equality yields precisely the positive exp(2*pi^2*xi)
Fourier weight used by the canonical half-modular graph. No L2 domain or
boundary conjugation is assumed or inferred in this pointwise integral lemma. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Complex
open scoped FourierTransform
namespace F1Fecho.WedgeLaplace

def regularizedReal (b k : ℝ) (F : ℂ → ℂ) (x : ℝ) : ℂ :=
  exp ((k:ℂ)*(x:ℂ))*lowerGaussian b x*F x

def regularizedLower (b k : ℝ) (F : ℂ → ℂ) (x : ℝ) : ℂ :=
  exp ((k:ℂ)*((x:ℂ)+(-Real.pi:ℝ)*I))*
    lowerGaussian b ((x:ℂ)+(-Real.pi:ℝ)*I)*F ((x:ℂ)+(-Real.pi:ℝ)*I)

theorem regularized_real_factor (b k p x : ℝ) (F : ℂ → ℂ) :
    regularized b k p F (x:ℂ)=
      exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*regularizedReal b k F x := by
  unfold regularized regularizedReal
  rw [add_mul,exp_add]
  ring

theorem regularized_lower_factor (b k p x : ℝ) (F : ℂ → ℂ) :
    regularized b k p F ((x:ℂ)+(-Real.pi:ℝ)*I)=
      (Real.exp (-2*Real.pi^2*p):ℂ)*
        (exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*regularizedLower b k F x) := by
  have he : (-2*(Real.pi:ℂ)*I*(p:ℂ)+(k:ℂ))*((x:ℂ)+(-Real.pi:ℝ)*I)=
      ((-2*Real.pi^2*p:ℝ):ℂ)+(-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))+
        (k:ℂ)*((x:ℂ)+(-Real.pi:ℝ)*I) := by
    push_cast
    ring_nf
    simp [I_sq]
    ring
  unfold regularized regularizedLower
  rw [he,exp_add,exp_add,←ofReal_exp]
  ring

theorem regularized_integral_balance (b : ℝ) (hb : 0 < b) (k p C : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hc : ContinuousOn F lowerClosedStrip)
    (hd : DifferentiableOn ℂ F lowerOpenStrip)
    (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C) :
    (Real.exp (2*Real.pi^2*p):ℂ)*
      (∫ x : ℝ, exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*regularizedReal b k F x) =
      ∫ x : ℝ, exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*regularizedLower b k F x := by
  have h:=regularized_contour_shift b hb k p C F hC hc hd hF
  simp_rw [regularized_real_factor,regularized_lower_factor] at h
  rw [integral_const_mul] at h
  have he : (Real.exp (2*Real.pi^2*p):ℂ)*(Real.exp (-2*Real.pi^2*p):ℂ)=1 := by
    rw [←ofReal_mul,←Real.exp_add]
    ring_nf
    simp
  calc
    _ = (Real.exp (2*Real.pi^2*p):ℂ)*((Real.exp (-2*Real.pi^2*p):ℂ)*
        (∫ x : ℝ, exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*regularizedLower b k F x)) :=
      congrArg (fun z : ℂ => (Real.exp (2*Real.pi^2*p):ℂ)*z) h.symm
    _ = _ := by rw [←mul_assoc,he,one_mul]

theorem regularized_fourier_balance (b : ℝ) (hb : 0 < b) (k p C : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hc : ContinuousOn F lowerClosedStrip)
    (hd : DifferentiableOn ℂ F lowerOpenStrip)
    (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C) :
    (Real.exp (2*Real.pi^2*p):ℂ)*𝓕 (regularizedReal b k F) p =
      𝓕 (regularizedLower b k F) p := by
  have he (g : ℝ → ℂ) : 𝓕 g p =
      ∫ x : ℝ, exp (-2*(Real.pi:ℂ)*I*(p:ℂ)*(x:ℂ))*g x := by
    rw [Real.fourier_eq']
    apply integral_congr_ae
    apply ae_of_all
    intro x
    simp only [Real.inner_apply,smul_eq_mul]
    congr 1
    congr 1
    push_cast
    ring
  rw [he,he]
  exact regularized_integral_balance b hb k p C F hC hc hd hF


end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.regularized_lower_factor
#print axioms F1Fecho.WedgeLaplace.regularized_integral_balance
#print axioms F1Fecho.WedgeLaplace.regularized_fourier_balance
