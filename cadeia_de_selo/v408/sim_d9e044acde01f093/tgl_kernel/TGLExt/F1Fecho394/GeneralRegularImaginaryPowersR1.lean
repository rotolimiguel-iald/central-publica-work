import TGLExt.F1Fecho394.GeneralRegularPositiveGraphR2
import TGLExt.F1Fecho394.GeneralRegularAbsorptionR1
import TGLExt.V351RegularImaginaryPowers

/-! The positive graph generalizing v351 implements the SAME generic regular
unitary group. The existing sigmoid functional calculus and Fourier shift
are reused; no imaginary-power identification is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 2500000
noncomputable section
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular TGLExt ChatgptAudit MeasureTheory Filter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem regularSpectralCoordinates_character
    (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (t : ℝ)
    (u : RegularHilbert H) :
    regularSpectralCoordinates B (characterMultiplier (2*Real.pi*t) u)=
      RegularCovariantCore.regularUnitary B t (regularSpectralCoordinates B u) := by
  let F:=Lp.fourierTransformₗᵢ ℝ H
  have hf:=congrArg F.symm (fourier_shift t (F.symm u))
  change F.symm (F (shift t (F.symm u)))=
    F.symm (characterMultiplier (2*Real.pi*t) (F (F.symm u))) at hf
  have hf' : F.symm (characterMultiplier (2*Real.pi*t) u)=shift t (F.symm u) := by
    simpa only [LinearIsometryEquiv.symm_apply_apply,LinearIsometryEquiv.apply_symm_apply] using hf.symm
  change CoefficientBoost.unitary B 1 (F.symm (characterMultiplier (2*Real.pi*t) u))=
    RegularCovariantCore.regularUnitary B t (CoefficientBoost.unitary B 1 (F.symm u))
  rw [hf']
  exact absorption_shift B t (F.symm u)

/-- The powers of the already constructed positive graph equal the whole
regular group. Affiliation and dual scaling are separate obligations. -/
theorem regularPositiveGenerator_imaginaryPower (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (t : ℝ)
    (u : RegularHilbert (H)) :
    resolventImaginaryPower (regularSpectralResolvent B)
      (regularSpectralResolvent_nonneg B) (regularSpectralResolvent_le_one B)
      (regularSpectralResolvent_injective B) (regularSpectralResolvent_complement_injective B)
      t u = RegularCovariantCore.regularUnitary B t u := by
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
  have hg0 : ∀ ξ, 0 ≤ g ξ := fun ξ => Real.sigmoid_nonneg _
  have hg1 : ∀ ξ, g ξ ≤ 1 := fun ξ => Real.sigmoid_le_one _
  let M := realScalarMultiplier (H := H) g hg hg0 hg1
  have hM0 : 0 ≤ M := realScalarMultiplier_nonneg _ _ _ _
  have hM1 : M ≤ 1 := realScalarMultiplier_le_one _ _ _ _
  have hiM : Function.Injective M := realScalarMultiplier_injective _ _ _ _
    (fun ξ => Real.sigmoid_pos _)
  have hjM : Function.Injective (1-M : _ →L[ℂ] _) := by
    rw [show M = realScalarMultiplier g hg hg0 hg1 from rfl, realScalarMultiplier_complement]
    exact realScalarMultiplier_injective _ _ _ _ (fun ξ => sub_pos.mpr (Real.sigmoid_lt_one _))
  let V := regularSpectralCoordinates B
  let VL := V.toLinearIsometry.toContinuousLinearMap
  have he : regularSpectralResolvent B * VL = VL * M := by
    ext1 x
    change regularSpectralResolvent B (V x) = V (M x)
    change V (M (V.symm (V x))) = V (M x)
    rw [LinearIsometryEquiv.symm_apply_apply]
  have hh := resolventImaginaryPower_intertwines (regularSpectralResolvent B) M VL
    (regularSpectralResolvent_nonneg B) (regularSpectralResolvent_le_one B)
    (regularSpectralResolvent_injective B) (regularSpectralResolvent_complement_injective B)
    hM0 hM1 hiM hjM he t (V.symm u)
  change resolventImaginaryPower (regularSpectralResolvent B)
    (regularSpectralResolvent_nonneg B) (regularSpectralResolvent_le_one B)
    (regularSpectralResolvent_injective B) (regularSpectralResolvent_complement_injective B)
    t (V (V.symm u)) = V (resolventImaginaryPower M hM0 hM1 hiM hjM t (V.symm u)) at hh
  rw [sigmoidMultiplier_imaginaryPower M rfl hM0 hM1 hiM hjM] at hh
  rw [LinearIsometryEquiv.apply_symm_apply] at hh
  exact hh.trans ((regularSpectralCoordinates_character B t (V.symm u)).trans
    (congrArg (RegularCovariantCore.regularUnitary B t) (V.apply_symm_apply u)))


end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralCoordinates_character
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_imaginaryPower
