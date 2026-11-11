import TGLExt.F1Fecho394.LowerStripContourR1
import TGLExt.O16.LightRayVerticalDecay_v4

/-! Gaussian control for a strip coefficient with one real exponential factor.
Completing the square reuses the actual O16 integrability and decay lemmas. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Complex
open scoped Topology
namespace F1Fecho.WedgeLaplace
open ChatgptAudit.LightRayCore016

def lowerGaussian (b : ℝ) (z : ℂ) : ℂ := twistedGaussian b 0 (-z)

theorem lowerGaussian_entire (b : ℝ) : Differentiable ℂ (lowerGaussian b) := by
  unfold lowerGaussian twistedGaussian
  fun_prop

theorem lowerGaussian_bound (b : ℝ) (hb : 0 < b) (x y : ℝ)
    (hy : -Real.pi ≤ y) (hy0 : y ≤ 0) :
    ‖lowerGaussian b ((x:ℂ)+(y:ℂ)*I)‖ ≤ ‖twistedGaussian b 0 (x:ℂ)‖ := by
  have he : -((x:ℂ)+(y:ℂ)*I)=((-x:ℝ):ℂ)+I*((-y:ℝ):ℂ) := by push_cast; ring
  unfold lowerGaussian
  rw [he]
  have h:=gaussian_strip_bound b hb 0 (-x) (-y) (by linarith) (by linarith)
  have hn : ‖twistedGaussian b 0 ((-x:ℝ):ℂ)‖=‖twistedGaussian b 0 (x:ℂ)‖ := by
    rw [gaussian_real_norm,gaussian_real_norm]
    congr 1
    ring
  exact h.trans_eq hn

theorem gaussian_exponential_complete_square (b : ℝ) (hb : b ≠ 0) (k x : ℝ) :
    Real.exp (k*x)*‖twistedGaussian b 0 (x:ℂ)‖ =
      Real.exp (k^2/(4*b))*‖twistedGaussian b (k/(2*b)) (x:ℂ)‖ := by
  rw [gaussian_real_norm,gaussian_real_norm,←Real.exp_add,←Real.exp_add]
  congr 1
  field_simp
  <;> ring

def regularized (b k p : ℝ) (F : ℂ → ℂ) (z : ℂ) : ℂ :=
  exp ((-2*(Real.pi:ℂ)*I*(p:ℂ)+(k:ℂ))*z)*lowerGaussian b z*F z

def regularizationBound (b k p C : ℝ) : ℝ :=
  Real.exp (2*Real.pi*|p| *Real.pi)*Real.exp (k^2/(4*b))*C

theorem regularized_strip_bound (b : ℝ) (hb : 0 < b) (k p C x y : ℝ)
    (F : ℂ → ℂ) (hC : 0 ≤ C) (hF : ∀ z ∈ lowerClosedStrip, ‖F z‖ ≤ C)
    (hy : -Real.pi ≤ y) (hy0 : y ≤ 0) :
    ‖regularized b k p F ((x:ℂ)+(y:ℂ)*I)‖ ≤
      regularizationBound b k p C*‖twistedGaussian b (k/(2*b)) (x:ℂ)‖ := by
  have hf := hF ((x:ℂ)+(y:ℂ)*I) (by simpa [lowerClosedStrip] using And.intro hy hy0)
  have he : ‖exp ((-2*(Real.pi:ℂ)*I*(p:ℂ)+(k:ℂ))*((x:ℂ)+(y:ℂ)*I))‖ =
      Real.exp (2*Real.pi*p*y+k*x) := by
    rw [norm_exp]
    congr 1
    simp [mul_re,mul_im]
    ring
  have hpy : p*y ≤ |p| *Real.pi := by
    calc
      p*y ≤ |p*y| := le_abs_self _
      _ = |p| *|y| := abs_mul _ _
      _ ≤ |p| *Real.pi := mul_le_mul_of_nonneg_left (abs_le.mpr ⟨hy,hy0.trans Real.pi_pos.le⟩) (abs_nonneg _)
  have hex : Real.exp (2*Real.pi*p*y+k*x) ≤
      Real.exp (2*Real.pi*|p| *Real.pi)*Real.exp (k*x) := by
    rw [←Real.exp_add]
    apply Real.exp_le_exp.mpr
    nlinarith [Real.pi_pos]
  unfold regularized
  rw [norm_mul,norm_mul,he]
  calc
    _ ≤ (Real.exp (2*Real.pi*|p| *Real.pi)*Real.exp (k*x))*
        ‖twistedGaussian b 0 (x:ℂ)‖*C :=
      mul_le_mul (mul_le_mul hex (lowerGaussian_bound b hb x y hy hy0)
        (norm_nonneg _) (by positivity)) hf (norm_nonneg _) (by positivity)
    _ = regularizationBound b k p C*‖twistedGaussian b (k/(2*b)) (x:ℂ)‖ := by
      rw [mul_assoc (Real.exp _) (Real.exp _) (‖twistedGaussian b 0 (x:ℂ)‖),
        gaussian_exponential_complete_square b hb.ne']
      unfold regularizationBound
      ring

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.lowerGaussian_bound
#print axioms F1Fecho.WedgeLaplace.gaussian_exponential_complete_square
#print axioms F1Fecho.WedgeLaplace.regularized_strip_bound
