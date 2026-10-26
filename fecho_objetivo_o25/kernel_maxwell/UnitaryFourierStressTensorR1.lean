import UnitaryFourierRealStressR2
import CoherentPointStressR2
import RealProfileMaxwellNonzeroR3

/-! Apply the derived Fourier-volume normalization to the whole existing
Maxwell stress, including its coherent kernel, on the same H1. Symmetry,
conservation, reality, translation and a nonzero classical energy witness
survive this positive constant scaling. Its null contraction is exactly the
normalized moment already constructed, not a separately chosen scalar.
This does not yet construct the Fock charge_link or a MaxwellCertificate.
No physical calibration, source, production kernel or old artifact is changed. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ

def unitaryFourierProfileStress (h : H1) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  (unitaryFourierStressScale : ℂ) * realProfileStress h μ ν x

def unitaryFourierCoherentStress (h k : H1) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  (unitaryFourierStressScale : ℂ) * coherentProfileStress h k μ ν x

private theorem constant_scaled_divergence
    (A : Fin 4 → ℝ → ℂ) (d : Fin 4 → ℂ) (c : ℂ)
    (hd : ∀ μ, HasDerivAt (A μ) (d μ) 0)
    (hc : (∑ μ : Fin 4, metricSignC μ * deriv (A μ) 0) = 0) :
    (∑ μ : Fin 4, metricSignC μ * deriv (fun t => c * A μ t) 0) = 0 := by
  simp only [(hd _).deriv] at hc
  simp only [((hd _).const_mul c).deriv]
  calc
    _ = c * (∑ μ : Fin 4, metricSignC μ * d μ) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro μ _
      ring
    _ = 0 := by rw [hc, mul_zero]

theorem unitaryFourierProfileStress_symmetric (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierProfileStress h μ ν x = unitaryFourierProfileStress h ν μ x := by
  unfold unitaryFourierProfileStress
  rw [realProfileStress_symmetric h μ ν x]

theorem unitaryFourierProfileStress_real (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    star (unitaryFourierProfileStress h μ ν x) = unitaryFourierProfileStress h μ ν x := by
  simp only [unitaryFourierProfileStress, star_mul, RCLike.star_ofReal,
    realProfileStress_real]

theorem unitaryFourierProfileStress_conserved (h : H1) (hh : RegularProfile h)
    (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4, metricSignC μ * deriv
      (fun t : ℝ => unitaryFourierProfileStress h μ ν (x + t • spacetimeBasis μ)) 0) = 0 := by
  exact constant_scaled_divergence _ _ _
    (fun μ => realProfileStress_line_hasDerivAt h hh μ μ ν x)
    (realProfileStress_conserved h hh ν x)

theorem unitaryFourierCoherentStress_conserved (h k : H1)
    (hh : RegularProfile h) (hk : RegularProfile k) (ν : Fin 4) (x : Spacetime) :
    (∑ μ : Fin 4, metricSignC μ * deriv
      (fun t : ℝ => unitaryFourierCoherentStress h k μ ν (x + t • spacetimeBasis μ)) 0) = 0 := by
  exact constant_scaled_divergence _ _ _
    (fun μ => coherentProfileStress_line_hasDerivAt h k hh hk μ μ ν x)
    (coherentProfileStress_conserved h k hh hk ν x)

theorem unitaryFourierCoherentStress_diagonal (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierCoherentStress h h μ ν x =
      Complex.exp (inner ℂ h h) * unitaryFourierProfileStress h μ ν x := by
  simp only [unitaryFourierCoherentStress, unitaryFourierProfileStress,
    coherentProfileStress_diagonal]
  ring

theorem unitaryFourierCoherentStress_translate (a : Fin 4 → ℝ) (h k : H1)
    (μ ν : Fin 4) (x : Spacetime) :
    unitaryFourierCoherentStress (U1 a h) (U1 a k) μ ν x =
      unitaryFourierCoherentStress h k μ ν (x - WithLp.toLp 2 a) := by
  unfold unitaryFourierCoherentStress
  rw [coherentProfileStress_translate]

theorem unitaryFourierProfileStress_null (h : H1) (x : NullFourierSpace) :
    (unitaryFourierProfileStress h 0 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
     unitaryFourierProfileStress h 0 1 (nullPlanePoint (x 0) (nullFourierScreen x)) +
     unitaryFourierProfileStress h 1 0 (nullPlanePoint (x 0) (nullFourierScreen x)) +
     unitaryFourierProfileStress h 1 1 (nullPlanePoint (x 0) (nullFourierScreen x))).re =
      unitaryFourierRealNullStress h x := by
  simp only [unitaryFourierProfileStress, unitaryFourierRealNullStress, realNullStress,
    Complex.add_re, Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
  ring

theorem exists_unitaryFourier_positive_stress : ∃ h : H1,
    StrongRegularProfile h ∧ 0 < (unitaryFourierProfileStress h 0 0 0).re := by
  obtain ⟨h, hh, hp⟩ := exists_strongRegular_positive_stress
  refine ⟨h, hh, ?_⟩
  simpa only [unitaryFourierProfileStress, Complex.mul_re, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero] using mul_pos unitaryFourierStressScale_pos hp

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierProfileStress_symmetric
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierProfileStress_real
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierProfileStress_conserved
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierCoherentStress_conserved
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierCoherentStress_diagonal
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierCoherentStress_translate
#print axioms F1Fecho.MaxwellGlobal.unitaryFourierProfileStress_null
#print axioms F1Fecho.MaxwellGlobal.exists_unitaryFourier_positive_stress
