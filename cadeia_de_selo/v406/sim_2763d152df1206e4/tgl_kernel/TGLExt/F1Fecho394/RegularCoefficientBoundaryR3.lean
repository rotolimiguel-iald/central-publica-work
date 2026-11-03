import TGLExt.F1Fecho394.PositiveCoefficientBoundaryR4
import TGLExt.F1Fecho394.RegularMaxwellEnergyR2
import TGLExt.F1Fecho394.PhysicalSmearTranslationR2
import TGLExt.F1Fecho394.OrbitalContractionAnalyticR1

/-! Finite first moments for all matrix coefficients whose second vector is
an actual Maxwell Schwartz smearing. Circular basis transport preserves the
pointwise norm. This supplies the regularity needed by boundary uniqueness. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter
open scoped InnerProductSpace ENNReal
namespace F1Fecho.RegularCoefficient
open TGLExt.ImportedSQ F1Fecho.MaxwellGlobal F1Fecho.MaxwellLocalization
open F1Fecho.OrbitalScreen ChatgptAudit.WignerRapidityMeasure016
open ChatgptAudit.WignerOrbit016 ChatgptAudit.PositiveEnergy016

theorem circularSmear_energySquare (f : SchwartzTensor) :
    EnergySquareProfile (circularSmear f) := by
  intro m
  apply ((physicalSmear_strongRegular f).2 m).congr
  filter_upwards [fiberLiftMap_ae circularFiber.symm (physicalSmearCLM f)] with y hy
  change shellEnergy y^m*‖physicalSmearCLM f y‖^2=
    shellEnergy y^m*‖fiberLiftMap circularFiber.symm (physicalSmearCLM f) y‖^2
  rw [hy,circularFiber.symm.norm_map]

theorem coefficient_first_moment (p : MomentumCoordinates→ℝ) (hp : Measurable p)
    (hn : ∀y,0≤p y) (hb : ∀y,p y≤2*shellEnergy y)
    (ξ ψ : H1) (hψ : EnergySquareProfile ψ) :
    Integrable (fun y=>p y*‖inner ℂ (ξ y) (ψ y)‖) (orbitalMeasure 0) := by
  have hi : Integrable (fun y=>‖ξ y‖^2) (orbitalMeasure 0) :=
    (Lp.memLp ξ).integrable_norm_pow (by norm_num : (2:ℕ)≠0)
  apply (hi.add (hψ 2)).mono'
  · exact hp.aestronglyMeasurable.mul
      ((Lp.aestronglyMeasurable ξ).inner (Lp.aestronglyMeasurable ψ)).norm
  · apply ae_of_all
    intro y
    rw [Real.norm_of_nonneg (mul_nonneg (hn y) (norm_nonneg _))]
    have he:=shellEnergy_nonneg y
    have hinner:=norm_inner_le_norm (𝕜:=ℂ) (ξ y) (ψ y)
    have hstep : p y*‖inner ℂ (ξ y) (ψ y)‖≤2*shellEnergy y*(‖ξ y‖*‖ψ y‖) :=
      mul_le_mul (hb y) hinner (norm_nonneg _) (by positivity)
    exact hstep.trans (by
      change 2*shellEnergy y*(‖ξ y‖*‖ψ y‖)≤‖ξ y‖^2+shellEnergy y^2*‖ψ y‖^2
      nlinarith [sq_nonneg (‖ξ y‖-shellEnergy y*‖ψ y‖)])

theorem coefficient_eq_inner_V (a : Fin 4→ℝ)
    (ha : a∈TGLExt.ContratoQGv31.forwardCone) (ξ ψ : H1) (z : ℂ) (hz : 0≤z.im) :
    PositiveCoefficientBoundary.coefficient (orbitalMeasure 0)
      (fun y=>ChatgptAudit.WignerOrbit016.orbitPairing a (shellMomentum 0 y))
      (fun y=>inner ℂ (ξ y) (ψ y)) z =inner ℂ ξ (OrbitalContraction.V a ha z ψ) := by
  rw [PositiveCoefficientBoundary.coefficient,L2.inner_def]
  apply integral_congr_ae
  filter_upwards [OrbitalContraction.V_ae a ha z hz ψ] with y hy
  rw [hy,inner_smul_right]

theorem positive_ray_implies_all_times (a : Fin 4→ℝ)
    (ha : a∈TGLExt.ContratoQGv31.forwardCone)
    (hb : ∀y,ChatgptAudit.WignerOrbit016.orbitPairing a (shellMomentum 0 y)≤2*shellEnergy y)
    (ξ ψ : H1) (hψ : EnergySquareProfile ψ)
    (hz : ∀t:ℝ,0<t→inner ℂ ξ (U1 (t • a) ψ)=0) :
    ∀t:ℝ,inner ℂ ξ (U1 (t • a) ψ)=0 := by
  have hv:=PositiveCoefficientBoundary.vanishes_from_positive_ray (orbitalMeasure 0)
    _ (orbitalEnergy_measurable 0 a) (OrbitalContraction.energy_nonneg a ha)
    _ (L2.integrable_inner (𝕜:=ℂ) ξ ψ)
    (coefficient_first_moment _ (orbitalEnergy_measurable 0 a)
      (OrbitalContraction.energy_nonneg a ha) hb ξ ψ hψ)
    (fun t ht=>by rw [coefficient_eq_inner_V a ha ξ ψ t (by simp),OrbitalContraction.V_boundary]; exact hz t ht)
  intro t
  have ht:=hv (t:ℂ) (by simp [HalfPlaneBoundary.upper])
  rwa [coefficient_eq_inner_V a ha ξ ψ t (by simp),OrbitalContraction.V_boundary] at ht

end F1Fecho.RegularCoefficient
#print axioms F1Fecho.RegularCoefficient.circularSmear_energySquare
#print axioms F1Fecho.RegularCoefficient.coefficient_first_moment
#print axioms F1Fecho.RegularCoefficient.positive_ray_implies_all_times
