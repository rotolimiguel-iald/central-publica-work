import TGLExt.TheImportedSecondQuantization
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Tactic
/-! The actual orbital multiplier exp(i z p.a) on the massless H1.
For Im z>=0 it is contractive. The lower half-plane value is set to zero;
only holomorphy above and continuity on the closed upper half-plane are used. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter Set
open scoped InnerProductSpace ENNReal Topology
namespace F1Fecho.OrbitalContraction
open TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGL.SpecificAQFT
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016
open ChatgptAudit.PositiveEnergy016 ChatgptAudit.UnitMultiplier016

def boundedWeight {X : Type*} [MeasurableSpace X] (μ : Measure X)
    (u : X → ℂ) (hu : Measurable u) (hn : ∀ x, ‖u x‖ ≤ 1) : Lp ℂ ∞ μ :=
  (memLp_top_of_bound hu.aestronglyMeasurable 1 (ae_of_all _ hn)).toLp u

def boundedMultiplier {X E : Type*} [MeasurableSpace X]
    [NormedAddCommGroup E] [NormedSpace ℂ E] (μ : Measure X)
    (u : X → ℂ) (hu : Measurable u) (hn : ∀ x, ‖u x‖ ≤ 1) :
    Lp E 2 μ →L[ℂ] Lp E 2 μ :=
  (ContinuousLinearMap.lsmul ℂ ℂ).holderL μ ∞ 2 2 (boundedWeight μ u hu hn)

theorem boundedMultiplier_ae {X E : Type*} [MeasurableSpace X]
    [NormedAddCommGroup E] [NormedSpace ℂ E] (μ : Measure X)
    (u : X → ℂ) (hu : Measurable u) (hn : ∀ x, ‖u x‖ ≤ 1) (f : Lp E 2 μ) :
    boundedMultiplier μ u hu hn f =ᵐ[μ] fun x => u x • f x := by
  have h := (ContinuousLinearMap.lsmul ℂ ℂ).coeFn_holder
    (r := 2) (boundedWeight μ u hu hn) f
  have hw : boundedWeight μ u hu hn =ᵐ[μ] u := MemLp.coeFn_toLp _
  filter_upwards [h,hw] with x hx hwx
  simpa only [boundedMultiplier,ContinuousLinearMap.holderL_apply_apply,
    ContinuousLinearMap.lsmul_apply,hwx] using hx

theorem boundedMultiplier_norm {X E : Type*} [MeasurableSpace X]
    [NormedAddCommGroup E] [NormedSpace ℂ E] (μ : Measure X)
    (u : X → ℂ) (hu : Measurable u) (hn : ∀ x, ‖u x‖ ≤ 1) :
    ‖boundedMultiplier (E := E) μ u hu hn‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro f
  simp only [one_mul]
  apply Lp.norm_le_norm_of_ae_le
  filter_upwards [boundedMultiplier_ae μ u hu hn f] with x hx
  rw [hx,norm_smul]
  exact (mul_le_mul_of_nonneg_right (hn x) (norm_nonneg _)).trans_eq (one_mul _)

theorem energy_nonneg (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (x : MomentumCoordinates) :
    0 ≤ orbitPairing a (shellMomentum 0 x) := by
  apply orbitalEnergy_nonnegative 0 a ha.1
  have h := ha.2
  unfold minkowskiSq at h
  linarith

def V (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (z : ℂ) : H1 →L[ℂ] H1 :=
  if hz : 0 ≤ z.im then
    boundedMultiplier (orbitalMeasure 0) (fun x => spectralPhase z (orbitPairing a (shellMomentum 0 x)))
      (spectralPhase_measurable _ (orbitalEnergy_measurable 0 a) z)
      (fun x => spectralPhase_norm_le_one z _ hz (energy_nonneg a ha x))
  else 0

theorem V_norm (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (z : ℂ) : ‖V a ha z‖ ≤ 1 := by
  unfold V
  split
  · exact boundedMultiplier_norm _ _ _ _
  · simp

theorem V_ae (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (z : ℂ) (hz : 0 ≤ z.im) (f : H1) :
    V a ha z f =ᵐ[orbitalMeasure 0]
      fun x => spectralPhase z (orbitPairing a (shellMomentum 0 x)) • f x := by
  rw [V,dif_pos hz]
  exact boundedMultiplier_ae _ _ _ _ f

theorem V_boundary (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (t : ℝ) (f : H1) :
    V a ha t f = U1 (t • a) f := by
  apply Lp.ext
  have ht : (0:ℝ) ≤ (t:ℂ).im := by simp
  have h1 := V_ae a ha t ht f
  have h2 := unitMultiplier_ae (orbitalMeasure 0) (orbitalPhase 0 (t • a))
    (orbitalPhase_continuous 0 (t • a)).measurable (orbitalPhase_norm 0 (t • a)) f
  filter_upwards [h1,h2] with x hx hy
  rw [hx,orbitalPhase_real_parameter]
  exact hy.symm

theorem density_integral (a : Fin 4 → ℝ) (ha : a ∈ forwardCone)
    (z : ℂ) (hz : 0 ≤ z.im) (f : H1) :
    spectralIntegral (stateDensityMeasure (orbitalMeasure 0) f)
      (fun x => orbitPairing a (shellMomentum 0 x)) z = inner ℂ f (V a ha z f) := by
  have hw : AEMeasurable (fun x => ENNReal.ofReal (‖f x‖^2)) (orbitalMeasure 0) :=
    ((Lp.aestronglyMeasurable f).norm.aemeasurable.pow_const 2).ennreal_ofReal
  rw [spectralIntegral,stateDensityMeasure,
    integral_withDensity_eq_integral_toReal_smul₀ hw (ae_of_all _ fun _ => ENNReal.ofReal_lt_top),L2.inner_def]
  apply integral_congr_ae
  filter_upwards [V_ae a ha z hz f] with x hx
  rw [hx,inner_smul_right,inner_self_eq_norm_sq_to_K]
  simp [ENNReal.toReal_ofReal,sq_nonneg,Complex.real_smul,mul_comm]

theorem diagonal_analytic (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (f : H1) :
    DiffContOnCl ℂ (fun z => inner ℂ f (V a ha z f)) upperHalf := by
  let ν := stateDensityMeasure (orbitalMeasure 0) f
  letI : IsFiniteMeasure ν := stateDensityMeasure_finite _ f
  have hp : a 1^2+a 2^2+a 3^2 ≤ a 0^2 := by
    have h := ha.2
    unfold minkowskiSq at h
    linarith
  have hd := orbitalSpectralIntegral_holomorphic 0 a ha.1 hp ν
  have hc := spectralIntegral_continuous_closed ν _ (orbitalEnergy_measurable 0 a)
    (energy_nonneg a ha)
  constructor
  · apply hd.congr
    intro z hz
    exact (density_integral a ha z hz.le f).symm
  · change ContinuousOn _ (closure {z : ℂ | 0 < z.im})
    rw [Complex.closure_setOf_lt_im]
    apply hc.congr
    intro z hz
    exact (density_integral a ha z hz f).symm

theorem coefficient_polarization (T : H1 →L[ℂ] H1) (x y : H1) :
    inner ℂ x (T y) = (inner ℂ (x+y) (T (x+y)) - inner ℂ (x-y) (T (x-y)) -
      Complex.I*inner ℂ (x+Complex.I • y) (T (x+Complex.I • y)) +
      Complex.I*inner ℂ (x-Complex.I • y) (T (x-Complex.I • y))) / 4 := by
  simp only [map_add,map_sub,inner_add_left,inner_add_right,map_smul,inner_smul_left,
    inner_smul_right,Complex.conj_I,← pow_two,Complex.I_sq,inner_sub_left,inner_sub_right,
    mul_add,← mul_assoc,mul_neg,neg_neg,one_mul,neg_one_mul,mul_sub,sub_sub]
  ring

theorem coefficient_analytic (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (f g : H1) :
    DiffContOnCl ℂ (fun z => inner ℂ f (V a ha z g)) upperHalf := by
  have h := (((diagonal_analytic a ha (f+g)).sub (diagonal_analytic a ha (f-g))).sub
    ((diagonal_analytic a ha (f+Complex.I • g)).const_smul Complex.I)).add
    ((diagonal_analytic a ha (f-Complex.I • g)).const_smul Complex.I)
  have h' := h.const_smul (1/4:ℂ)
  convert h' using 1
  funext z
  simp only [Pi.smul_apply,Pi.add_apply,Pi.sub_apply,smul_eq_mul]
  rw [coefficient_polarization]
  ring

end F1Fecho.OrbitalContraction
#print axioms F1Fecho.OrbitalContraction.V_norm
#print axioms F1Fecho.OrbitalContraction.V_boundary
#print axioms F1Fecho.OrbitalContraction.coefficient_analytic
