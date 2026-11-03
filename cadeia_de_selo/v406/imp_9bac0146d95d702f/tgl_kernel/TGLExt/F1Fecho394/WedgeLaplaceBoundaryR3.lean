import TGLExt.F1Fecho394.WedgeLaplaceIntegralR3

/-! The lower-strip endpoint has the actual conjugate transverse-reflection
boundary for real scalar tests. The vector Maxwell and L2 graph consumers
remain separate; the endpoint is not assumed as a contract field. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.WedgeLaplace
open F1Fecho.MaxwellGlobal SchwartzMap

theorem longitudinal_lower_pi (m t x r : ℝ) :
    longitudinal m t x ((r:ℂ)-Complex.I*Real.pi) = -longitudinal m t x r := by
  have he : Complex.exp (Complex.I*(Real.pi:ℂ))=(-1:ℂ) := by
    simpa only [mul_comm] using Complex.exp_pi_mul_I
  have hn : -((r:ℂ)-Complex.I*Real.pi)=-(r:ℂ)+Complex.I*Real.pi := by ring
  simp only [longitudinal,hn,Complex.exp_sub,Complex.exp_add,he]
  ring

theorem kernel_lower_pi (m t x v r : ℝ) :
    kernel m t x v ((r:ℂ)-Complex.I*Real.pi)=star (kernel m t x (-v) r) := by
  simp only [kernel,longitudinal_lower_pi,longitudinal_real]
  rw [Complex.star_def,←Complex.exp_conj]
  congr 1
  simp only [map_mul,map_sub,map_neg,Complex.conj_I,Complex.conj_ofReal]
  push_cast
  ring

theorem scalarLaplace_lower_pi_real (m q₂ q₃ r : ℝ) (f : 𝓢(Spacetime,ℂ))
    (hf : ∀ x,(f x).im=0) :
    scalarLaplace m q₂ q₃ f ((r:ℂ)-Complex.I*Real.pi) =
      star (scalarLaplace m (-q₂) (-q₃) f r) := by
  rw [scalarLaplace,scalarLaplace,Complex.star_def,←integral_conj]
  apply integral_congr_ae
  apply ae_of_all
  intro x
  have hs : star (f x)=f x := by
    apply Complex.ext <;> simp [Complex.star_def,hf x]
  change kernel m (x 0) (x 1) (q₂*x 2+q₃*x 3) ((r:ℂ)-Complex.I*Real.pi) * f x =
    star (kernel m (x 0) (x 1) ((-q₂)*x 2+(-q₃)*x 3) r * f x)
  have hv : -(q₂*x 2+q₃*x 3)=(-q₂)*x 2+(-q₃)*x 3 := by ring
  rw [kernel_lower_pi,hv,star_mul,hs]
  exact mul_comm _ _

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.longitudinal_lower_pi
#print axioms F1Fecho.WedgeLaplace.kernel_lower_pi
#print axioms F1Fecho.WedgeLaplace.scalarLaplace_lower_pi_real
