import TGLExt.F1Fecho394.LowerGaussianControlR2

/-! Finite linear combinations of real exponential modes form an algebra.
This pays the finite hyperbolic coefficient decomposition used by Maxwell. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RapidityPolynomial

def mode (k : ℝ) (z : ℂ) : ℂ := Complex.exp ((k:ℂ)*z)
def span : Submodule ℂ (ℂ → ℂ) := Submodule.span ℂ (Set.range mode)

theorem mode_mem (k : ℝ) : mode k ∈ span := Submodule.subset_span ⟨k,rfl⟩

theorem mode_mul (k l : ℝ) : mode k * mode l = mode (k+l) := by
  funext z
  simp only [Pi.mul_apply,mode,Complex.ofReal_add,add_mul,Complex.exp_add]

theorem one_mem : (1 : ℂ → ℂ) ∈ span := by
  have he : mode 0 = (1 : ℂ → ℂ) := by
    funext z
    simp [mode]
  rw [←he]
  exact mode_mem 0

theorem const_mem (c : ℂ) : (fun _ : ℂ => c) ∈ span := by
  have he : (fun _ : ℂ => c) = c • (1 : ℂ → ℂ) := by
    funext z
    simp
  rw [he]
  exact span.smul_mem c one_mem

theorem mode_mul_mem (k : ℝ) (g : ℂ → ℂ) (hg : g ∈ span) : mode k*g ∈ span := by
  induction hg using Submodule.span_induction with
  | mem g hg =>
    obtain ⟨l,rfl⟩ := hg
    rw [mode_mul]
    exact mode_mem _
  | zero => simpa only [mul_zero] using span.zero_mem
  | add g h hg hh ihg ihh =>
    rw [mul_add]
    exact span.add_mem ihg ihh
  | smul c g hg ih =>
    rw [mul_smul_comm]
    exact span.smul_mem c ih

theorem mul_mem (f g : ℂ → ℂ) (hf : f ∈ span) (hg : g ∈ span) : f*g ∈ span := by
  induction hf using Submodule.span_induction with
  | mem f hf =>
    obtain ⟨k,rfl⟩ := hf
    exact mode_mul_mem k g hg
  | zero => simpa only [zero_mul] using span.zero_mem
  | add f h hf hh ihf ihh =>
    rw [add_mul]
    exact span.add_mem ihf ihh
  | smul c f hf ih =>
    rw [smul_mul_assoc]
    exact span.smul_mem c ih

theorem cosh_mem : Complex.cosh ∈ span := by
  have he : Complex.cosh = (2⁻¹:ℂ) • (mode 1+mode (-1)) := by
    funext z
    simp [Complex.cosh,mode,div_eq_mul_inv]
    ring
  rw [he]
  exact span.smul_mem _ (span.add_mem (mode_mem 1) (mode_mem (-1)))

theorem sinh_mem : Complex.sinh ∈ span := by
  have he : Complex.sinh = (2⁻¹:ℂ) • (mode 1-mode (-1)) := by
    funext z
    simp [Complex.sinh,mode,div_eq_mul_inv]
    ring
  rw [he]
  exact span.smul_mem _ (span.sub_mem (mode_mem 1) (mode_mem (-1)))

end F1Fecho.RapidityPolynomial
#print axioms F1Fecho.RapidityPolynomial.mul_mem
#print axioms F1Fecho.RapidityPolynomial.cosh_mem
#print axioms F1Fecho.RapidityPolynomial.sinh_mem
