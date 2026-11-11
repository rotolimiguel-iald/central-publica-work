import TGLExt.F1Fecho394.GaussianLogScalarR4

/-! Continuous Gaussian spectral multipliers on the compact resolvent
coordinate; their range factors through R, with endpoint zero proved. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Filter
open scoped Topology
namespace F1Fecho.GaussianLogScalar

def gaussianSymbol (b:ℝ) : ℝ→ℝ := compactify (fun l=>Real.exp (-b*l^2))
def gaussianRangeFactor (b:ℝ) : ℝ→ℝ :=
  compactify (fun l=>Real.exp (-b*l^2)+Real.exp (-b*l^2+l))

theorem gaussianSymbol_continuous (b:ℝ) (hb:0<b) : Continuous (gaussianSymbol b) := by
  apply compactify_continuous _ (by fun_prop)
  · simpa using gaussian_linear_atTop b hb 0
  · simpa using gaussian_linear_atBot b hb 0

theorem gaussianRangeFactor_continuous (b:ℝ) (hb:0<b) : Continuous (gaussianRangeFactor b) := by
  apply compactify_continuous _ (by fun_prop)
  · simpa using (gaussian_linear_atTop b hb 0).add (gaussian_linear_atTop b hb 1)
  · simpa using (gaussian_linear_atBot b hb 0).add (gaussian_linear_atBot b hb 1)

theorem gaussianSymbol_nonneg (b x:ℝ) : 0≤gaussianSymbol b x := by
  unfold gaussianSymbol compactify
  split
  · exact le_rfl
  · exact (Real.exp_pos _).le

theorem gaussianSymbol_le_one (b:ℝ) (hb:0≤b) (x:ℝ) : gaussianSymbol b x≤1 := by
  unfold gaussianSymbol compactify
  split
  · norm_num
  · apply Real.exp_le_one_iff.mpr
    exact mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hb) (sq_nonneg _)

theorem gaussianSymbol_factors (b x:ℝ) (hx:x∈Set.Icc (0:ℝ) 1) :
    gaussianSymbol b x=x*gaussianRangeFactor b x := by
  by_cases hz:x=0 ∨ x=1
  · simp [gaussianSymbol,gaussianRangeFactor,compactify,hz]
  · have hp:0<x:=lt_of_le_of_ne hx.1 (Ne.symm (not_or.mp hz).1)
    have hq:x<1:=lt_of_le_of_ne hx.2 (not_or.mp hz).2
    have he:Real.exp (logCoordinate x)=(1-x)/x :=
      Real.exp_log (div_pos (sub_pos.mpr hq) hp)
    simp only [gaussianSymbol,gaussianRangeFactor,compactify,if_neg hz,Real.exp_add,he]
    field_simp
    <;> ring

end F1Fecho.GaussianLogScalar
#print axioms F1Fecho.GaussianLogScalar.gaussianSymbol_continuous
#print axioms F1Fecho.GaussianLogScalar.gaussianRangeFactor_continuous
#print axioms F1Fecho.GaussianLogScalar.gaussianSymbol_nonneg
#print axioms F1Fecho.GaussianLogScalar.gaussianSymbol_le_one
#print axioms F1Fecho.GaussianLogScalar.gaussianSymbol_factors
