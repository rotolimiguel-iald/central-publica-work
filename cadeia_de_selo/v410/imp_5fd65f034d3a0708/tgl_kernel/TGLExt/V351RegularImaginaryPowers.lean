import TGLExt.V351ScalarMultiplierCalculus
import TGLExt.V351ResolventImaginaryIntertwining
import TGLExt.V351RegularSpectralGraph
import TGLExt.V351FourierTranslation

set_option autoImplicit false
set_option maxHeartbeats 2500000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem resolventPhaseFunction_sigmoid (t a : ℝ) :
    resolventPhaseFunction t (Real.sigmoid a) =
      (resolventDamping (Real.sigmoid a) : ℂ) * modularPhase t (-a) := by
  have hr : (1-Real.sigmoid a)/Real.sigmoid a = Real.exp (-a) := by
    apply (div_eq_iff (ne_of_gt (Real.sigmoid_pos a))).mpr
    rw [mul_comm, Real.sigmoid_mul_rexp_neg, Real.sigmoid_neg]
  rw [resolventPhaseFunction, hr, Real.log_exp]

/-- Identification of the existing imaginary-power construction, not a newly
defined group. The scalar multiplier identity is discharged by rfl at its caller. -/
theorem sigmoidMultiplier_imaginaryPower
    (T : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hT : T = realScalarMultiplier (fun ξ => Real.sigmoid (2*Real.pi*ξ)) (by fun_prop)
      (fun ξ => Real.sigmoid_nonneg _) (fun ξ => Real.sigmoid_le_one _))
    (h0 : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : RegularHilbert H →L[ℂ] RegularHilbert H))
    (t : ℝ) (u : RegularHilbert H) :
    resolventImaginaryPower T h0 h1 hi hj t u = characterMultiplier (2*Real.pi*t) u := by
  subst T
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
  have hg0 : ∀ ξ, 0 ≤ g ξ := fun ξ => Real.sigmoid_nonneg _
  have hg1 : ∀ ξ, g ξ ≤ 1 := fun ξ => Real.sigmoid_le_one _
  let M := realScalarMultiplier (H := H) g hg hg0 hg1
  refine (resolventDampingOperator_denseRange M h0 h1 hi hj).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) u
  rintro _ ⟨y,rfl⟩
  rw [resolventImaginaryPower_damping]
  have hd := realScalarMultiplier_cfc_ae g hg hg0 hg1
    (fun z : ℂ => (resolventDamping z.re : ℂ))
    (by unfold resolventDamping; fun_prop) y
  rw [resolventDampingOperator_cfc M (IsSelfAdjoint.of_nonneg h0)] at hd
  have hp := realScalarMultiplier_cfc_ae g hg hg0 hg1
    (fun z : ℂ => resolventPhaseFunction t z.re)
    ((resolventPhaseFunction_continuous t).comp Complex.continuous_re) y
  apply Lp.ext
  filter_upwards [hp,hd,characterMultiplier_ae (2*Real.pi*t) (resolventDampingOperator M y)]
    with ξ hp hd hc
  change resolventPhaseOperator M t y ξ = characterMultiplier (2*Real.pi*t) (resolventDampingOperator M y) ξ
  dsimp only [resolventPhaseOperator]
  rw [hp, hc, hd]
  simp only [Complex.ofReal_re]
  rw [show g ξ = Real.sigmoid (2*Real.pi*ξ) from rfl, resolventPhaseFunction_sigmoid]
  have he : modularPhase t (-(2*Real.pi*ξ)) = characterPhase (2*Real.pi*t) ξ := by
    unfold modularPhase characterPhase
    congr 1
    push_cast
    ring
  rw [he, smul_smul, mul_comm]
  rfl

theorem regularSpectralCoordinates_character (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    regularSpectralCoordinates P (characterMultiplier (2*Real.pi*t) u) =
      regularUnitary P t (regularSpectralCoordinates P u) := by
  let F := Lp.fourierTransformₗᵢ ℝ (TowerHilbert P)
  let W := regularFlowAbsorptionUnitary P
  have hf := congrArg F.symm (fourier_shift t (F.symm u))
  change F.symm (F (shift t (F.symm u))) =
    F.symm (characterMultiplier (2*Real.pi*t) (F (F.symm u))) at hf
  have hf' : F.symm (characterMultiplier (2*Real.pi*t) u) = shift t (F.symm u) := by
    simpa only [LinearIsometryEquiv.symm_apply_apply, LinearIsometryEquiv.apply_symm_apply] using hf.symm
  have hw : W.val * shift t = regularUnitary P t * W.val := by
    have hw0 := Unitary.star_mul_self_of_mem W.property
    calc
      W.val * shift t = W.val * shift t * (star W.val * W.val) := by rw [hw0,mul_one]
      _ = (W.val * shift t * star W.val) * W.val := by simp only [mul_assoc]
      _ = _ := by rw [regularUnitary_shift_conjugate]
  change W.val (F.symm (characterMultiplier (2*Real.pi*t) u)) =
    regularUnitary P t (W.val (F.symm u))
  rw [hf']
  exact congrArg (fun A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) =>
    A (F.symm u)) hw

/-- The powers of the already constructed positive graph equal the whole
regular group. Affiliation and dual scaling are separate obligations. -/
theorem regularPositiveGenerator_imaginaryPower (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    resolventImaginaryPower (regularSpectralResolvent P)
      (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_le_one P)
      (regularSpectralResolvent_injective P) (regularSpectralResolvent_complement_injective P)
      t u = regularUnitary P t u := by
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
  have hg0 : ∀ ξ, 0 ≤ g ξ := fun ξ => Real.sigmoid_nonneg _
  have hg1 : ∀ ξ, g ξ ≤ 1 := fun ξ => Real.sigmoid_le_one _
  let M := realScalarMultiplier (H := TowerHilbert P) g hg hg0 hg1
  have hM0 : 0 ≤ M := realScalarMultiplier_nonneg _ _ _ _
  have hM1 : M ≤ 1 := realScalarMultiplier_le_one _ _ _ _
  have hiM : Function.Injective M := realScalarMultiplier_injective _ _ _ _
    (fun ξ => Real.sigmoid_pos _)
  have hjM : Function.Injective (1-M : _ →L[ℂ] _) := by
    rw [show M = realScalarMultiplier g hg hg0 hg1 from rfl, realScalarMultiplier_complement]
    exact realScalarMultiplier_injective _ _ _ _ (fun ξ => sub_pos.mpr (Real.sigmoid_lt_one _))
  let V := regularSpectralCoordinates P
  let VL := V.toLinearIsometry.toContinuousLinearMap
  have he : regularSpectralResolvent P * VL = VL * M := by
    ext1 x
    change regularSpectralResolvent P (V x) = V (M x)
    change V (M (V.symm (V x))) = V (M x)
    rw [LinearIsometryEquiv.symm_apply_apply]
  have hh := resolventImaginaryPower_intertwines (regularSpectralResolvent P) M VL
    (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_le_one P)
    (regularSpectralResolvent_injective P) (regularSpectralResolvent_complement_injective P)
    hM0 hM1 hiM hjM he t (V.symm u)
  change resolventImaginaryPower (regularSpectralResolvent P)
    (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_le_one P)
    (regularSpectralResolvent_injective P) (regularSpectralResolvent_complement_injective P)
    t (V (V.symm u)) = V (resolventImaginaryPower M hM0 hM1 hiM hjM t (V.symm u)) at hh
  rw [sigmoidMultiplier_imaginaryPower M rfl hM0 hM1 hiM hjM] at hh
  rw [LinearIsometryEquiv.apply_symm_apply] at hh
  exact hh.trans ((regularSpectralCoordinates_character P t (V.symm u)).trans
    (congrArg (regularUnitary P t) (V.apply_symm_apply u)))

#print axioms resolventPhaseFunction_sigmoid
#print axioms sigmoidMultiplier_imaginaryPower
#print axioms regularSpectralCoordinates_character
#print axioms regularPositiveGenerator_imaginaryPower
end
end TGLV350.Regular
