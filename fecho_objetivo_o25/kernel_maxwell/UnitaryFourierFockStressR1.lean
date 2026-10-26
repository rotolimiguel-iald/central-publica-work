import UnitaryFourierStressTensorR2
import RegularFockStressTranslationR3
import RegularFockStressBoostR3
import RegularFockStressWeakConservationR2

/-! Carry the derived Fourier normalization into the actual regular Fock form.
The domain, coefficients, translations and boosts are the existing ones. This
is constant scaling of the previously constructed form; no new representation
or domain is selected. Conservation and covariance survive the same scaling.
The null-plane integral and equality with the Fock boost charge are still
separate obligations. This is not a complete MaxwellCertificate. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory TGLExt TGLExt.ImportedSQ
open F1Fecho.CoherentKernel F1Fecho.CovariantTensor F1Fecho.SpacetimeLorentz

def unitaryFourierPointStressForm (ψ χ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  (unitaryFourierStressScale : ℂ) * pointStressForm ψ χ μ ν x

theorem unitaryFourierPointStressForm_exponential (h k : RegularLabel)
    (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm (regularExponential h) (regularExponential k) μ ν x =
      unitaryFourierCoherentStress h.val k.val μ ν x := by
  simp only [unitaryFourierPointStressForm, unitaryFourierCoherentStress,
    pointStressForm_exponential]

theorem unitaryFourierPointStressForm_hermitian (ψ χ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    (starRingEnd ℂ) (unitaryFourierPointStressForm ψ χ μ ν x) =
      unitaryFourierPointStressForm χ ψ μ ν x := by
  simp only [unitaryFourierPointStressForm, map_mul, Complex.conj_ofReal,
    pointStressForm_hermitian]

theorem unitaryFourierPointStressForm_diagonal_real (ψ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    (unitaryFourierPointStressForm ψ ψ μ ν x).im = 0 := by
  simp only [unitaryFourierPointStressForm, Complex.mul_im, Complex.ofReal_re,
    Complex.ofReal_im, pointStressForm_diagonal_real, mul_zero, zero_mul, add_zero]

theorem unitaryFourierPointStressForm_add_left (ψ χ ζ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm (ψ + χ) ζ μ ν x =
      unitaryFourierPointStressForm ψ ζ μ ν x + unitaryFourierPointStressForm χ ζ μ ν x := by
  simp only [unitaryFourierPointStressForm, pointStressForm_add_left, mul_add]

theorem unitaryFourierPointStressForm_add_right (ψ χ ζ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm ψ (χ + ζ) μ ν x =
      unitaryFourierPointStressForm ψ χ μ ν x + unitaryFourierPointStressForm ψ ζ μ ν x := by
  simp only [unitaryFourierPointStressForm, pointStressForm_add_right, mul_add]

theorem unitaryFourierPointStressForm_smul_left (z : ℂ) (ψ χ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm (z • ψ) χ μ ν x =
      (starRingEnd ℂ) z * unitaryFourierPointStressForm ψ χ μ ν x := by
  simp only [unitaryFourierPointStressForm, pointStressForm_smul_left]
  ring

theorem unitaryFourierPointStressForm_smul_right (z : ℂ) (ψ χ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm ψ (z • χ) μ ν x =
      z * unitaryFourierPointStressForm ψ χ μ ν x := by
  simp only [unitaryFourierPointStressForm, pointStressForm_smul_right]
  ring

theorem unitaryFourierPointStressForm_symmetric (ψ χ : regularFockDomain)
    (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm ψ χ μ ν x = unitaryFourierPointStressForm ψ χ ν μ x := by
  unfold unitaryFourierPointStressForm
  rw [pointStressForm_symmetric]

theorem unitaryFourierPointStressForm_conserved (ψ χ : regularFockDomain)
    (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4, metricSignC μ * deriv
      (fun t : ℝ => unitaryFourierPointStressForm ψ χ μ ν (x + t • spacetimeBasis μ)) 0) = 0 := by
  have hc := pointStressForm_conserved ψ χ ν x
  simp only [(pointStressForm_line_hasDerivAt ψ χ _ _ _ x).deriv] at hc
  simp only [unitaryFourierPointStressForm,
    ((pointStressForm_line_hasDerivAt ψ χ _ _ _ x).const_mul
      (unitaryFourierStressScale : ℂ)).deriv]
  calc
    _ = (unitaryFourierStressScale : ℂ) *
        (∑ μ : Fin 4, metricSignC μ *
          finiteKernel (fun h k : RegularLabel => deriv
            (fun t : ℝ => coherentProfileStress h.val k.val μ ν (x + t • spacetimeBasis μ)) 0)
            (regularCoefficients ψ) (regularCoefficients χ)) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro μ _
      ring
    _ = 0 := by rw [hc, mul_zero]

theorem unitaryFourierPointStressForm_weak_conserved (ψ χ : regularFockDomain)
    (ν : Fin 4) (f : Spacetime → ℂ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (hc : HasCompactSupport f) :
    (∑ μ : Fin 4, ∫ x, metricSignC μ * unitaryFourierPointStressForm ψ χ μ ν x *
      fderiv ℝ f x (spacetimeBasis μ)) = 0 := by
  have he (μ : Fin 4) :
      (fun x => metricSignC μ * unitaryFourierPointStressForm ψ χ μ ν x *
        fderiv ℝ f x (spacetimeBasis μ)) =
      (fun x => (unitaryFourierStressScale : ℂ) *
        (metricSignC μ * pointStressForm ψ χ μ ν x * fderiv ℝ f x (spacetimeBasis μ))) := by
    funext x
    unfold unitaryFourierPointStressForm
    ring
  simp only [he, integral_const_mul, ← Finset.mul_sum,
    pointStressForm_weak_conserved ψ χ ν f hf hc, mul_zero]

theorem unitaryFourierPointStressForm_translate (a : Fin 4 → ℝ)
    (ψ χ : regularFockDomain) (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm (regularGamma (U1 a) (strongRegularProfile_U1 a) ψ)
      (regularGamma (U1 a) (strongRegularProfile_U1 a) χ) μ ν x =
      unitaryFourierPointStressForm ψ χ μ ν (x - WithLp.toLp 2 a) := by
  unfold unitaryFourierPointStressForm
  rw [pointStressForm_translate]

theorem unitaryFourierPointStressForm_boost (s : ℝ) (ψ χ : regularFockDomain)
    (x : Spacetime) :
    (fun μ ν => unitaryFourierPointStressForm
      (regularGamma (B0 s) (strongRegularProfile_B0 s) ψ)
      (regularGamma (B0 s) (strongRegularProfile_B0 s) χ) μ ν x) =
      pull (complexBoost (-s)) (fun μ ν =>
        unitaryFourierPointStressForm ψ χ μ ν ((action (theBoost s)).symm x)) := by
  have h := congrArg (fun F : TensorValue => (unitaryFourierStressScale : ℂ) • F)
    (pointStressForm_boost s ψ χ x)
  rw [← map_smul] at h
  exact h

theorem unitaryFourierPointStressForm_vacuum (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierPointStressForm regularVacuum regularVacuum μ ν x = 0 := by
  simp only [unitaryFourierPointStressForm, pointStressForm_vacuum, mul_zero]

theorem unitaryFourierPointStressForm_nontrivial :
    ∃ ψ : regularFockDomain, 0 < (unitaryFourierPointStressForm ψ ψ 0 0 0).re := by
  obtain ⟨ψ, hp⟩ := pointStressForm_nontrivial
  refine ⟨ψ, ?_⟩
  simpa only [unitaryFourierPointStressForm, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero] using mul_pos unitaryFourierStressScale_pos hp

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_exponential
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_hermitian
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_diagonal_real
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_add_left
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_add_right
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_smul_left
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_smul_right
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_symmetric
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_conserved
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_weak_conserved
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_translate
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_boost
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_vacuum
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierPointStressForm_nontrivial
