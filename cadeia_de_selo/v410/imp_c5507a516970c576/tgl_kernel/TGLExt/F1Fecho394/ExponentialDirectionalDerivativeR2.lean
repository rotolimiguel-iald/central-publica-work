import TGLExt.F1Fecho394.ExponentialCreationVectorR2
/-! Strong holomorphy and the directional derivative of the existing
exponential vectors. The vector Cauchy formula follows from the scalar Gram
kernel and totality. Hence creation is an actual Hilbert derivative. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Complex Metric Filter Topology
namespace F1Fecho.Creation
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential

theorem exponential_cauchy (f g : H1) (w : ℂ) (hw : w ∈ ball (0:ℂ) 1) :
    ((2*Real.pi*I:ℂ)⁻¹ • ∮ z in C(0,1), (z-w)⁻¹ • exponential (g+z•f)) =
      exponential (g+w•f) := by
  have hv : CircleIntegrable (fun z : ℂ => (z-w)⁻¹ • exponential (g+z•f)) 0 1 := by
    apply ContinuousOn.circleIntegrable (by norm_num)
    apply ((continuousOn_id.sub continuousOn_const).inv₀ ?_).smul
      ((ConcreteWeyl.exponential_continuous.comp
        (continuous_const.add (continuous_id.smul continuous_const))).continuousOn)
    intro z hz he
    have he' := sub_eq_zero.mp he
    change z = w at he'
    subst z
    exact (ne_of_lt hw) hz
  apply sub_eq_zero.mp
  apply exponential_orthogonal_zero
  intro h
  apply inner_eq_zero_symm.mp
  rw [inner_sub_right]
  apply sub_eq_zero.mpr
  let L : F →L[ℂ] ℂ := innerSL ℂ (exponential h)
  let v : ℂ → ℂ := fun z => Complex.exp (inner ℂ h g + z * inner ℂ h f)
  have hd : DifferentiableOn ℂ v (closedBall 0 1) := by
    intro z hz
    exact (((((hasDerivAt_id z).mul_const (inner ℂ h f)).const_add
      (inner ℂ h g)).cexp).differentiableAt).differentiableWithinAt
  have hc := DifferentiableOn.circleIntegral_sub_inv_smul hd hw
  have hm : (fun z => L ((z-w)⁻¹ • exponential (g+z•f))) = fun z => (z-w)⁻¹ • v z := by
    funext z
    simp only [L,innerSL_apply_apply,inner_smul_right,exponential_inner,
      inner_add_right,inner_smul_right,v,smul_eq_mul]
  change L ((2*Real.pi*I:ℂ)⁻¹ • ∮ z in C(0,1), (z-w)⁻¹ • exponential (g+z•f)) = _
  rw [map_smul,map_circleIntegral L _ hv,hm,hc,smul_smul,
    inv_mul_cancel₀ two_pi_I_ne_zero,one_smul]
  simp only [v,exponential_inner,inner_add_right,inner_smul_right]

theorem exponential_line_analytic_zero (f g : H1) :
    AnalyticAt ℂ (fun z : ℂ => exponential (g+z•f)) 0 := by
  have hi : CircleIntegrable (fun z : ℂ => exponential (g+z•f)) 0 (1:NNReal) :=
    (ConcreteWeyl.exponential_continuous.comp
      (continuous_const.add (continuous_id.smul continuous_const))).continuousOn.circleIntegrable (by norm_num)
  have hp := hasFPowerSeriesOn_cauchy_integral (R := (1:NNReal)) hi (by norm_num : (0:NNReal)<1)
  apply hp.analyticAt.congr
  filter_upwards [ball_mem_nhds (0:ℂ) (by norm_num : (0:ℝ)<1)] with w hw
  exact exponential_cauchy f g w hw

theorem exponential_line_hasDerivAt (f g : H1) :
    HasDerivAt (fun z : ℂ => exponential (g+z•f)) (creationVector f g) 0 := by
  have hd := (exponential_line_analytic_zero f g).differentiableAt.hasDerivAt
  have he : deriv (fun z : ℂ => exponential (g+z•f)) 0 = creationVector f g := by
    apply sub_eq_zero.mp
    apply exponential_orthogonal_zero
    intro h
    apply inner_eq_zero_symm.mp
    rw [inner_sub_right]
    apply sub_eq_zero.mpr
    have hl := ((innerSL ℂ (exponential h)).hasFDerivAt).comp_hasDerivAt 0 hd
    have hs : HasDerivAt (fun z : ℂ => Complex.exp (inner ℂ h g + z * inner ℂ h f))
        (Complex.exp (inner ℂ h g) * inner ℂ h f) 0 := by
      simpa only [id_eq,zero_mul,add_zero,one_mul] using
        (((hasDerivAt_id (0:ℂ)).mul_const (inner ℂ h f)).const_add (inner ℂ h g)).cexp
    have hr := hl.unique (by simpa only [Function.comp_def,innerSL_apply_apply,
      exponential_inner,inner_add_right,inner_smul_right] using hs)
    rw [exponential_inner_creationVector]
    exact hr.trans (mul_comm _ _)
  rwa [he] at hd

end F1Fecho.Creation
#print axioms F1Fecho.Creation.exponential_cauchy
#print axioms F1Fecho.Creation.exponential_line_analytic_zero
#print axioms F1Fecho.Creation.exponential_line_hasDerivAt
