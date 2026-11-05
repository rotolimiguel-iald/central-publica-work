import TGLExt.V351RegularFlowAbsorption
import TGLExt.V350L2PositiveMultiplier
import TGLExt.V350ResolventGraph
import Mathlib.Analysis.Fourier.LpSpace
import Mathlib.Analysis.SpecialFunctions.Sigmoid

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Positivity for the existing vector-valued scalar multiplier. The scalar
SpectralHilbert result in ContinuousModularResolvent cannot be instantiated at H. -/
theorem realScalarMultiplier_nonneg (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) :
    0 ≤ realScalarMultiplier (H := H) g hg h0 h1 := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ContinuousLinearMap.isPositive_def'.mpr
  constructor
  · change star (operatorFieldLift (realScalarField (H := H) g hg h0 h1)) =
      operatorFieldLift (realScalarField (H := H) g hg h0 h1)
    symm
    apply operatorFieldLift_star
    intro x
    change (g x : ℂ) • (1 : H →L[ℂ] H) =
      star ((g x : ℂ) • (1 : H →L[ℂ] H))
    simp
  · intro f
    change 0 ≤ (inner ℂ (realScalarMultiplier g hg h0 h1 f) f).re
    rw [L2.inner_def]
    change 0 ≤ RCLike.re (∫ x : ℝ,
      inner ℂ ((realScalarMultiplier g hg h0 h1 f) x) (f x))
    rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) (realScalarMultiplier g hg h0 h1 f) f)]
    apply integral_nonneg_of_ae
    filter_upwards [realScalarMultiplier_ae g hg h0 h1 f] with x hx
    rw [hx]
    rw [inner_smul_left]
    have hc : (starRingEnd ℂ) (g x : ℂ) = (g x : ℂ) := by simp
    rw [hc]
    change 0 ≤ ((g x : ℂ) * inner ℂ (f x) (f x)).re
    rw [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
    change 0 ≤ g x * RCLike.re (inner ℂ (f x) (f x))
    rw [inner_self_eq_norm_sq]
    exact mul_nonneg (h0 x) (sq_nonneg ‖f x‖)

theorem realScalarMultiplier_complement (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) :
    1 - realScalarMultiplier (H := H) g hg h0 h1 =
      realScalarMultiplier (fun x => 1-g x) (continuous_const.sub hg)
        (fun x => sub_nonneg.mpr (h1 x)) (fun x => sub_le_self 1 (h0 x)) := by
  ext1 f
  apply Lp.ext
  filter_upwards [realScalarMultiplier_ae g hg h0 h1 f,
    realScalarMultiplier_ae (fun x => 1-g x) (continuous_const.sub hg)
      (fun x => sub_nonneg.mpr (h1 x)) (fun x => sub_le_self 1 (h0 x)) f,
    Lp.coeFn_sub f (realScalarMultiplier g hg h0 h1 f)] with x h2 h3 h4
  change (f-realScalarMultiplier g hg h0 h1 f) x = _
  rw [h4, h3]
  simp only [Pi.sub_apply, h2, Complex.ofReal_sub, Complex.ofReal_one, sub_smul, one_smul]

theorem realScalarMultiplier_le_one (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) :
    realScalarMultiplier (H := H) g hg h0 h1 ≤ 1 := by
  apply sub_nonneg.mp
  rw [realScalarMultiplier_complement]
  exact realScalarMultiplier_nonneg _ _ _ _

/-- From the spectral L² coordinate to the original regular representation. -/
def regularSpectralCoordinates (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) ≃ₗᵢ[ℂ] RegularHilbert (TowerHilbert P) :=
  (Lp.fourierTransformₗᵢ ℝ (TowerHilbert P)).symm.trans
    (Unitary.linearIsometryEquiv (regularFlowAbsorptionUnitary P))

/-- The candidate (1+h)^{-1}, with the spectral function already in mathlib. -/
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) :=
  (regularSpectralCoordinates P).conjStarAlgEquiv
    (realScalarMultiplier (fun x => Real.sigmoid (2*Real.pi*x)) (by fun_prop)
      (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _))

theorem regularSpectralResolvent_nonneg (P : SiteProfile) :
    0 ≤ regularSpectralResolvent P := by
  exact map_nonneg (regularSpectralCoordinates P).conjStarAlgEquiv
    (realScalarMultiplier_nonneg _ _ _ _)

theorem regularSpectralResolvent_le_one (P : SiteProfile) :
    regularSpectralResolvent P ≤ 1 := by
  apply sub_nonneg.mp
  have h := map_nonneg (regularSpectralCoordinates P).conjStarAlgEquiv
    (sub_nonneg.mpr (realScalarMultiplier_le_one
      (H := TowerHilbert P) (fun x => Real.sigmoid (2*Real.pi*x)) (by fun_prop)
      (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _)))
  simpa only [map_sub, map_one, regularSpectralResolvent] using h

theorem regularSpectralResolvent_injective (P : SiteProfile) :
    Function.Injective (regularSpectralResolvent P) :=
  (regularSpectralCoordinates P).injective.comp
    ((realScalarMultiplier_injective _ _ _ _ (fun _ => Real.sigmoid_pos _)).comp
      (regularSpectralCoordinates P).symm.injective)

theorem regularSpectralResolvent_complement_injective (P : SiteProfile) :
    Function.Injective (1-regularSpectralResolvent P :
      RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) := by
  let g : ℝ → ℝ := fun x => Real.sigmoid (2*Real.pi*x)
  have hg : Continuous g := by fun_prop
  have h0 : ∀ x, 0 ≤ g x := fun x => Real.sigmoid_nonneg _
  have h1 : ∀ x, g x ≤ 1 := fun x => Real.sigmoid_le_one _
  change Function.Injective (1 - (regularSpectralCoordinates P).conjStarAlgEquiv
    (realScalarMultiplier g hg h0 h1) : _ →L[ℂ] _)
  rw [← map_one (regularSpectralCoordinates P).conjStarAlgEquiv,
    ← map_sub, realScalarMultiplier_complement]
  exact (regularSpectralCoordinates P).injective.comp
    ((realScalarMultiplier_injective _ _ _ _
      (fun x => sub_pos.mpr (Real.sigmoid_lt_one _))).comp
      (regularSpectralCoordinates P).symm.injective)

/-- A positive graph on the same regular Hilbert space. Its imaginary powers,
affiliation and dual scaling are subsequent obligations, not fields assumed here. -/
def regularPositiveGenerator (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →ₗ.[ℂ] RegularHilbert (TowerHilbert P) :=
  resolventGraphOperator (regularSpectralResolvent P) (regularSpectralResolvent_injective P)

theorem regularPositiveGenerator_closed (P : SiteProfile) :
    (regularPositiveGenerator P).IsClosed :=
  resolvent_graph_closed _ _

theorem regularPositiveGenerator_domain_dense (P : SiteProfile) :
    Dense ((regularPositiveGenerator P).domain : Set (RegularHilbert (TowerHilbert P))) :=
  resolvent_graph_domain_dense _ _ (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg P))

theorem regularPositiveGenerator_selfadjoint (P : SiteProfile) :
    IsSelfAdjoint (regularPositiveGenerator P) :=
  resolvent_graph_selfadjoint _ _ (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg P))

theorem regularPositiveGenerator_positive (P : SiteProfile)
    (x : (regularPositiveGenerator P).domain) :
    0 ≤ (inner ℂ (x : RegularHilbert (TowerHilbert P)) (regularPositiveGenerator P x)).re :=
  resolvent_graph_positive _ _ (regularSpectralResolvent_nonneg P)
    (regularSpectralResolvent_le_one P) x

theorem regularPositiveGenerator_zero_kernel (P : SiteProfile)
    (x : (regularPositiveGenerator P).domain) (hx : regularPositiveGenerator P x = 0) :
    (x : RegularHilbert (TowerHilbert P)) = 0 := by
  let R := regularSpectralResolvent P
  let hi := regularSpectralResolvent_injective P
  have h : (1-R) (Continuous049.boundedGraphParameter R hi x) = (1-R) 0 := by
    change regularPositiveGenerator P x = (1-R) 0
    rw [hx, map_zero]
  have hz := regularSpectralResolvent_complement_injective P h
  have he := Continuous049.bounded_graph_parameter_apply R hi x
  rw [hz, map_zero] at he
  exact he.symm

#print axioms realScalarMultiplier_nonneg
#print axioms realScalarMultiplier_complement
#print axioms realScalarMultiplier_le_one
#print axioms regularSpectralCoordinates
#print axioms regularSpectralResolvent
#print axioms regularSpectralResolvent_nonneg
#print axioms regularSpectralResolvent_le_one
#print axioms regularSpectralResolvent_injective
#print axioms regularSpectralResolvent_complement_injective
#print axioms regularPositiveGenerator
#print axioms regularPositiveGenerator_closed
#print axioms regularPositiveGenerator_domain_dense
#print axioms regularPositiveGenerator_selfadjoint
#print axioms regularPositiveGenerator_positive
#print axioms regularPositiveGenerator_zero_kernel
end
end TGLV350.Regular
