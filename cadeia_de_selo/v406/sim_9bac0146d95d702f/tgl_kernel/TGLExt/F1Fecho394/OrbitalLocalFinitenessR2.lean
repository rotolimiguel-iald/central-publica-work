import TGLExt.F1Fecho394.OrbitalSpatialMeasureR1
import Mathlib.Analysis.SpecialFunctions.Pow.Integral
import Mathlib.MeasureTheory.Measure.Regular
/-! Local finiteness of the unchanged massless orbital measure, including
the integrable singularity at zero momentum. No regularity is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Set
namespace F1Fecho.OrbitalSpatial
open ChatgptAudit.WignerRapidityMeasure016

theorem momentum_norm_le_energy (p : MomentumCoordinates) :
    ‖p‖ ≤ energy (transverseMass 0 p.1) p.2 := by
  let e := energy (transverseMass 0 p.1) p.2
  have he : 0 ≤ e := Real.sqrt_nonneg _
  have he2 : e^2 = p.1 0^2+p.1 1^2+p.2^2 := by
    dsimp only [e]
    rw [energy_spatialChart,Real.sq_sqrt (by positivity),spatialChart_norm_sq]
    ring
  have h0 : |p.1 0| ≤ e := abs_le.mpr ⟨by nlinarith [sq_nonneg (p.1 1),sq_nonneg p.2],
    by nlinarith [sq_nonneg (p.1 1),sq_nonneg p.2]⟩
  have h1 : |p.1 1| ≤ e := abs_le.mpr ⟨by nlinarith [sq_nonneg (p.1 0),sq_nonneg p.2],
    by nlinarith [sq_nonneg (p.1 0),sq_nonneg p.2]⟩
  have h2 : |p.2| ≤ e := abs_le.mpr ⟨by nlinarith [sq_nonneg (p.1 0),sq_nonneg (p.1 1)],
    by nlinarith [sq_nonneg (p.1 0),sq_nonneg (p.1 1)]⟩
  change max ‖p.1‖ ‖p.2‖ ≤ e
  refine max_le ?_ (by simpa only [Real.norm_eq_abs] using h2)
  apply (pi_norm_le_iff_of_nonneg he).mpr
  intro i
  fin_cases i
  · change |p.1 0| ≤ e
    exact h0
  · change |p.1 1| ≤ e
    exact h1

def masslessDensity (p : MomentumCoordinates) : ℝ :=
  1 / energy (transverseMass 0 p.1) p.2

theorem masslessDensity_bound (p : MomentumCoordinates) :
    ‖masslessDensity p‖ ≤ 1 * ‖p‖ ^ (-(1 : ℝ)) := by
  by_cases hp : p=0
  · subst p
    simp [masslessDensity,energy,transverseMass]
  · have hn : 0 < ‖p‖ := norm_pos_iff.mpr hp
    have he := momentum_norm_le_energy p
    have hepos := hn.trans_le he
    rw [one_mul,Real.rpow_neg_one]
    simpa only [masslessDensity,one_div,Real.norm_eq_abs,abs_of_nonneg (inv_nonneg.mpr hepos.le)]
      using (inv_le_inv₀ hepos hn).mpr he

theorem masslessDensity_locallyIntegrable : LocallyIntegrable masslessDensity momentumMeasure := by
  letI : momentumMeasure.IsAddHaarMeasure := by unfold momentumMeasure; infer_instance
  have hd : Module.finrank ℝ MomentumCoordinates = 3 := by
    simp [MomentumCoordinates,Transverse,Module.finrank_prod,Module.finrank_fintype_fun_eq_card]
  apply locallyIntegrable_of_norm_le_rpow (by omega : 1 ≤ Module.finrank ℝ MomentumCoordinates)
    (C := 1) (α := 1) (by rw [hd]; norm_num)
    (Filter.Eventually.of_forall masslessDensity_bound)
  apply Measurable.aestronglyMeasurable
  unfold masslessDensity energy transverseMass
  fun_prop

instance orbital_zero_finiteOnCompacts : IsFiniteMeasureOnCompacts (orbitalMeasure 0) := by
  constructor
  intro K hK
  rw [orbitalMeasure,withDensity_apply _ hK.measurableSet]
  exact (hasFiniteIntegral_iff_ofReal (Filter.Eventually.of_forall
    (fun p => by change 0 ≤ 1 / energy (transverseMass 0 p.1) p.2; unfold energy; positivity))).mp
      (masslessDensity_locallyIntegrable.integrableOn_isCompact hK).hasFiniteIntegral

instance orbital_zero_locallyFinite : IsLocallyFiniteMeasure (orbitalMeasure 0) := inferInstance
instance orbital_zero_innerRegular : (orbitalMeasure 0).InnerRegularCompactLTTop := inferInstance

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.masslessDensity_bound
#print axioms F1Fecho.OrbitalSpatial.masslessDensity_locallyIntegrable
#print axioms F1Fecho.OrbitalSpatial.orbital_zero_finiteOnCompacts
#print axioms F1Fecho.OrbitalSpatial.orbital_zero_locallyFinite
