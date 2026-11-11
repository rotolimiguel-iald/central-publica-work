import TGLExt.F1Fecho394.WedgeLaplaceKernelR2

/-! Explicit derivative estimates for the actual rapidity Laplace kernel.
They provide a first-Schwartz-moment dominator for local differentiation. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.WedgeLaplace

def longitudinalDeriv (m t x : ℝ) (z : ℂ) : ℂ :=
  (m:ℂ)*(((t-x)/2:ℝ)*Complex.exp z-((t+x)/2:ℝ)*Complex.exp (-z))

theorem longitudinal_hasDerivAt (m t x : ℝ) (z : ℂ) :
    HasDerivAt (longitudinal m t x) (longitudinalDeriv m t x z) z := by
  have h := (((Complex.hasDerivAt_exp z).const_mul (((t-x)/2:ℝ):ℂ)).add
    (((Complex.hasDerivAt_exp (-z)).comp z (hasDerivAt_id z).neg).const_mul
      (((t+x)/2:ℝ):ℂ))).const_mul (m:ℂ)
  exact h.congr_deriv (by dsimp only [longitudinalDeriv]; ring)

def kernelDeriv (m t x v : ℝ) (z : ℂ) : ℂ :=
  Complex.I*longitudinalDeriv m t x z*kernel m t x v z

theorem kernel_hasDerivAt (m t x v : ℝ) (z : ℂ) :
    HasDerivAt (kernel m t x v) (kernelDeriv m t x v z) z := by
  have h := (Complex.hasDerivAt_exp _).comp z
    (((longitudinal_hasDerivAt m t x z).sub_const (v:ℂ)).const_mul Complex.I)
  exact h.congr_deriv (by dsimp only [kernel,kernelDeriv]; ring)

theorem half_sum_abs_le (t x : ℝ) : |(t+x)/2| ≤ |t|+|x| := by
  rw [abs_div,abs_of_pos (by norm_num : (0:ℝ)<2)]
  have h:=abs_add_le t x
  have ht:=abs_nonneg t
  have hx:=abs_nonneg x
  linarith

theorem half_sub_abs_le (t x : ℝ) : |(t-x)/2| ≤ |t|+|x| := by
  simpa [sub_eq_add_neg] using half_sum_abs_le t (-x)

theorem longitudinalDeriv_bound (m t x M : ℝ) (z : ℂ) (hz : |z.re| ≤ M) :
    ‖longitudinalDeriv m t x z‖ ≤ 2* |m| * (|t|+|x|)*Real.exp M := by
  have hp : ‖Complex.exp z‖ ≤ Real.exp M := by
    rw [Complex.norm_exp]
    exact Real.exp_le_exp.mpr ((le_abs_self z.re).trans hz)
  have hn : ‖Complex.exp (-z)‖ ≤ Real.exp M := by
    rw [Complex.norm_exp,Complex.neg_re]
    exact Real.exp_le_exp.mpr ((neg_le_abs z.re).trans hz)
  have ha : ‖(((t-x)/2:ℝ):ℂ)*Complex.exp z‖ ≤ (|t|+|x|)*Real.exp M := by
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    exact mul_le_mul (half_sub_abs_le t x) hp (norm_nonneg _) (by positivity)
  have hb : ‖(((t+x)/2:ℝ):ℂ)*Complex.exp (-z)‖ ≤ (|t|+|x|)*Real.exp M := by
    rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
    exact mul_le_mul (half_sum_abs_le t x) hn (norm_nonneg _) (by positivity)
  unfold longitudinalDeriv
  rw [norm_mul,Complex.norm_real,Real.norm_eq_abs]
  have hs := norm_sub_le ((((t-x)/2:ℝ):ℂ)*Complex.exp z)
    ((((t+x)/2:ℝ):ℂ)*Complex.exp (-z))
  calc
    _ ≤ |m| * ((|t|+|x|)*Real.exp M+(|t|+|x|)*Real.exp M) :=
      mul_le_mul_of_nonneg_left (hs.trans (add_le_add ha hb)) (abs_nonneg _)
    _ = _ := by ring

theorem kernelDeriv_bound (m t x v M r θ : ℝ) (hm : 0 ≤ m) (hw : |t| ≤ x)
    (hθ : 0 ≤ θ) (hπ : θ ≤ Real.pi) (hr : |r| ≤ M) :
    ‖kernelDeriv m t x v ((r:ℂ)-Complex.I*θ)‖ ≤
      2* |m| * (|t|+|x|)*Real.exp M := by
  rw [kernelDeriv,norm_mul,norm_mul,Complex.norm_I,one_mul]
  have hk:=kernel_norm_le_one_on_right_wedge m t x v r θ hm hw hθ hπ
  calc
    _ ≤ ‖longitudinalDeriv m t x ((r:ℂ)-Complex.I*θ)‖ :=
      mul_le_of_le_one_right (norm_nonneg _) hk
    _ ≤ _ := longitudinalDeriv_bound m t x M _ (by simpa using hr)

end F1Fecho.WedgeLaplace
#print axioms F1Fecho.WedgeLaplace.longitudinal_hasDerivAt
#print axioms F1Fecho.WedgeLaplace.kernel_hasDerivAt
#print axioms F1Fecho.WedgeLaplace.longitudinalDeriv_bound
#print axioms F1Fecho.WedgeLaplace.kernelDeriv_bound
