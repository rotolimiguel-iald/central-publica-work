import TGLExt.F1Fecho394.RegularSpectralBoostedAverageR2
import TGLExt.F1Fecho394.CoefficientConjugationR2
import TGLExt.F1Fecho394.RegularIntervalVectorsR2
/-! Exact reflected interval coefficient of the adjoint regular average.
Only null endpoints are discarded in Lebesgue L2. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularTranslatedReflection
open MeasureTheory TGLV350.Regular
open F1Fecho.RegularCovariantCore F1Fecho.RegularSpectralAverage
open F1Fecho.RegularSpectralBoostedAverage
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem regular_boosted_reflection (B:UnitaryFlow H) (a b:ℝ) (v:H) :
    F1Fecho.RegularCovariantCore.regularUnitary B (-b) (boostedCoefficient B (b-a) v)=
      CoefficientConjugation.reflection
        (CoefficientBoost.multiplier B (-1) (LpIntervalTotality.intervalVector a b v)) := by
  have ha := (measurePreserving_sub_right volume (-b)).quasiMeasurePreserving.ae
    (boostedCoefficient_ae B (b-a) v)
  have hb := (Measure.measurePreserving_neg (volume:Measure ℝ)).quasiMeasurePreserving.ae
    (CoefficientBoost.multiplier_ae B (-1) (LpIntervalTotality.intervalVector a b v))
  have hc := (Measure.measurePreserving_neg (volume:Measure ℝ)).quasiMeasurePreserving.ae
    (RegularIntervalVectors.intervalVector_ae a b v)
  apply Lp.ext
  filter_upwards [fibre_ae (boostCLM B (-b)) (shift (-b) (boostedCoefficient B (b-a) v)),
    shift_ae (-b) (boostedCoefficient B (b-a) v),ha,
    CoefficientConjugation.reflectionMap_ae
      (CoefficientBoost.multiplier B (-1) (LpIntervalTotality.intervalVector a b v)),hb,hc,
    (Ico_ae_eq_Ioc (μ:=(volume:Measure ℝ)) (a:=-b) (b:=-a))]
      with t h1 h2 h3 h4 h5 h6 h7
  change fibre (boostCLM B (-b)) (shift (-b) (boostedCoefficient B (b-a) v)) t =
    CoefficientConjugation.reflectionMap _ t
  rw [h1,h2,h3,h4,h5,h6]
  have hm1 : t-(-b)∈Set.Ioc 0 (b-a) ↔ t∈Set.Ioc (-b) (-a) := by
    simp only [Set.mem_Ioc]; constructor <;> intro ht <;> constructor <;> linarith [ht.1,ht.2]
  have hm2 : -t∈Set.Ioc a b ↔ t∈Set.Ico (-b) (-a) := by
    simp only [Set.mem_Ioc,Set.mem_Ico]; constructor <;> intro ht <;> constructor <;> linarith [ht.1,ht.2]
  by_cases ht : t∈Set.Ioc (-b) (-a)
  · have ht' : t∈Set.Ico (-b) (-a) := h7.mpr ht
    simp only [Set.indicator_of_mem (hm1.mpr ht),Set.indicator_of_mem (hm2.mpr ht')]
    change B.U (-b) (B.U (t-(-b)) v)=B.U (-1 * -t) v
    have he := congrArg (fun U:H≃ₗᵢ[ℂ]H=>U v) (B.add (-b) (t-(-b)))
    simp only [LinearIsometryEquiv.trans_apply] at he
    rw [←he]
    congr 2 <;> ring
  · have ht' : t∉Set.Ico (-b) (-a) := fun hh=>ht (h7.mp hh)
    simp only [Set.indicator_of_notMem (fun hh=>ht (hm1.mp hh)),
      Set.indicator_of_notMem (fun hh=>ht' (hm2.mp hh)),map_zero]
end F1Fecho.RegularTranslatedReflection
#print axioms F1Fecho.RegularTranslatedReflection.regular_boosted_reflection
