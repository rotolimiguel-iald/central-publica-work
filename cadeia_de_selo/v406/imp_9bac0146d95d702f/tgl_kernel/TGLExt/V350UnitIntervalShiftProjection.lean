import TGLExt.V350TranslationCorrelation
import TGLExt.V350FixedCoreLocality

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def unitCut : RegularHilbert H →L[ℂ] RegularHilbert H :=
  measurableCut (Set.Ioc (0 : ℝ) 1) measurableSet_Ioc

def unitCutFunction (f : RegularHilbert H) : ℝ → H :=
  (Set.Ioc (0 : ℝ) 1).indicator f

theorem unitCutFunction_integrable (f : RegularHilbert H) : Integrable (unitCutFunction f) := by
  have hi : IntegrableOn f (Set.Ioc (0 : ℝ) 1) volume :=
    integrableOn_Lp_of_measure_ne_top f (by norm_num) (by simp)
  exact hi.integrable_indicator measurableSet_Ioc

theorem inner_unitCut_shift (f g : RegularHilbert H) (t : ℝ) :
    inner ℂ g (unitCut (shift t (unitCut f))) =
      ∫ x : ℝ, inner ℂ (unitCutFunction g x) (unitCutFunction f (x-t)) := by
  rw [unitCut, measurableCut_inner, ← integral_indicator measurableSet_Ioc]
  apply integral_congr_ae
  filter_upwards [shift_ae t (unitCut f),
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae
      (measurableCut_ae (Set.Ioc (0 : ℝ) 1) measurableSet_Ioc f)] with x h1 h2
  have he : shift t (unitCut f) x = unitCutFunction f (x-t) := h1.trans h2
  by_cases hx : x ∈ Set.Ioc (0 : ℝ) 1
  · simp only [Set.indicator_of_mem hx, unitCutFunction] at he ⊢
    exact congrArg (fun v : H => inner ℂ (g x) v) he
  · simp only [unitCutFunction, Set.indicator_of_notMem hx, inner_zero_left]

theorem unitCut_correlation_support (f g : RegularHilbert H) (t : ℝ)
    (ht : t ∉ Set.Ioc (-2 : ℝ) 2) :
    (∫ x : ℝ, inner ℂ (unitCutFunction g x) (unitCutFunction f (x-t))) = 0 := by
  apply integral_eq_zero_of_ae
  apply Filter.Eventually.of_forall
  intro x
  by_cases hx : x ∈ Set.Ioc (0 : ℝ) 1
  · have hy : x-t ∉ Set.Ioc (0 : ℝ) 1 := by
      intro hy
      apply ht
      constructor <;> linarith [hx.1,hx.2,hy.1,hy.2]
    simp only [unitCutFunction, Set.indicator_of_notMem hy, inner_zero_right, Pi.zero_apply]
  · simp only [unitCutFunction, Set.indicator_of_notMem hx, inner_zero_left, Pi.zero_apply]

def shiftIntegralFamily : StrongIntegral.Family (H := RegularHilbert H) where
  op := shift
  continuous_apply := shift_strongly_continuous
  bound := 1
  bound_nonneg := zero_le_one
  norm_bound := fun t => ContinuousLinearMap.opNorm_le_bound _ zero_le_one
    (fun v => by rw [shift_norm, one_mul])

def intervalShiftIntegral : RegularHilbert H →L[ℂ] RegularHilbert H :=
  StrongIntegral.operatorIntegral shiftIntegralFamily (-2) 2

/-- The constant-fibre interval projection is a cut of a strong translation
integral. The integration window contains all differences of points in (0,1]. -/
theorem unitIntervalProjection_eq_cut_shift_integral :
    unitIntervalProjection (H := H) = unitCut * intervalShiftIntegral * unitCut := by
  apply ContinuousLinearMap.ext
  intro f
  apply ext_inner_left ℂ
  intro g
  symm
  change inner ℂ g (unitCut (intervalShiftIntegral (unitCut f))) = _
  have hi : inner ℂ g (unitCut (intervalShiftIntegral (unitCut f))) =
      ∫ t in (-2 : ℝ)..2, inner ℂ g (unitCut (shift t (unitCut f))) := by
    exact (((innerSL ℂ g).comp (unitCut (H := H))).intervalIntegral_comp_comm
      ((shift_strongly_continuous (unitCut f)).intervalIntegrable (-2) 2)).symm
  rw [hi]
  simp_rw [inner_unitCut_shift]
  rw [intervalIntegral.integral_of_le (by norm_num : (-2 : ℝ) ≤ 2)]
  rw [setIntegral_eq_integral_of_forall_compl_eq_zero
    (fun t ht => unitCut_correlation_support f g t ht)]
  rw [integral_translationCorrelation (unitCutFunction f) (unitCutFunction g)
    (unitCutFunction_integrable f) (unitCutFunction_integrable g)]
  rw [unitIntervalProjection_apply,
    ← inner_conj_symm g (testVector (∫ x in Set.Ioc (0 : ℝ) 1, f x)),
    inner_testVector, inner_conj_symm]
  simp only [unitCutFunction, integral_indicator measurableSet_Ioc]

theorem commutes_unitIntervalProjection
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hshift : ∀ t : ℝ, shift t * B = B * shift t)
    (hcut : unitCut * B = B * unitCut) :
    unitIntervalProjection * B = B * unitIntervalProjection := by
  have hi : B * intervalShiftIntegral = intervalShiftIntegral * B :=
    StrongIntegral.operatorIntegral_commutes shiftIntegralFamily (-2) 2 B
      (fun t => (hshift t).symm)
  rw [unitIntervalProjection_eq_cut_shift_integral]
  calc
    _ = unitCut * intervalShiftIntegral * (unitCut * B) := by rw [mul_assoc]
    _ = unitCut * intervalShiftIntegral * (B * unitCut) := by rw [hcut]
    _ = unitCut * (intervalShiftIntegral * B) * unitCut := by simp only [mul_assoc]
    _ = unitCut * (B * intervalShiftIntegral) * unitCut := by rw [hi]
    _ = B * (unitCut * intervalShiftIntegral * unitCut) := by rw [← mul_assoc, hcut]; simp only [mul_assoc]

theorem dualFixedCore_commutes_unitIntervalProjection (P : TGLExt.SiteProfile)
    (B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hB : B ∈ dualFixedCore P) :
    unitIntervalProjection * B = B * unitIntervalProjection :=
  commutes_unitIntervalProjection B
    (fun t => (dualFixedCore_commutes_shift_and_character P B hB t).1)
    (dualFixedCore_commutes_measurableCut P B hB _ measurableSet_Ioc)

#print axioms inner_unitCut_shift
#print axioms unitCut_correlation_support
#print axioms unitIntervalProjection_eq_cut_shift_integral
#print axioms commutes_unitIntervalProjection
#print axioms dualFixedCore_commutes_unitIntervalProjection
end
end TGLV350.Regular
