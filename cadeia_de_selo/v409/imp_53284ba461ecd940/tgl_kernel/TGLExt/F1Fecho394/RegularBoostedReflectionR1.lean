import TGLExt.F1Fecho394.RegularSpectralBoostedAverageR2
import TGLExt.F1Fecho394.CoefficientConjugationR2
/-! Exact reflected interval coefficient of the adjoint regular average.
Only null endpoints are discarded in Lebesgue L2. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularBoostedReflection
open MeasureTheory TGLV350.Regular
open F1Fecho.RegularCovariantCore F1Fecho.RegularSpectralAverage
open F1Fecho.RegularSpectralBoostedAverage
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem regular_boosted_reflection (B:UnitaryFlow H) (h:ℝ) (v:H) :
    F1Fecho.RegularCovariantCore.regularUnitary B (-h) (boostedCoefficient B h v)=
      CoefficientConjugation.reflection
        (CoefficientBoost.multiplier B (-1) (coefficient h v)) := by
  have ha := (measurePreserving_sub_right volume (-h)).quasiMeasurePreserving.ae
    (boostedCoefficient_ae B h v)
  have hb := (Measure.measurePreserving_neg (volume:Measure ℝ)).quasiMeasurePreserving.ae
    (CoefficientBoost.multiplier_ae B (-1) (coefficient h v))
  have hc := (Measure.measurePreserving_neg (volume:Measure ℝ)).quasiMeasurePreserving.ae
    (coefficient_ae h v)
  apply Lp.ext
  filter_upwards [fibre_ae (boostCLM B (-h)) (shift (-h) (boostedCoefficient B h v)),
    shift_ae (-h) (boostedCoefficient B h v),ha,
    CoefficientConjugation.reflectionMap_ae
      (CoefficientBoost.multiplier B (-1) (coefficient h v)),hb,hc,
    (Ico_ae_eq_Ioc (μ:=(volume:Measure ℝ)) (a:=-h) (b:=0))]
      with t h1 h2 h3 h4 h5 h6 h7
  change fibre (boostCLM B (-h)) (shift (-h) (boostedCoefficient B h v)) t =
    CoefficientConjugation.reflectionMap _ t
  rw [h1,h2,h3,h4,h5,h6]
  have hm1 : t-(-h)∈Set.Ioc 0 h ↔ t∈Set.Ioc (-h) 0 := by
    simp only [Set.mem_Ioc]; constructor <;> intro ht <;> constructor <;> linarith [ht.1,ht.2]
  have hm2 : -t∈Set.Ioc 0 h ↔ t∈Set.Ico (-h) 0 := by
    simp only [Set.mem_Ioc,Set.mem_Ico]; constructor <;> intro ht <;> constructor <;> linarith [ht.1,ht.2]
  by_cases ht : t∈Set.Ioc (-h) 0
  · have ht' : t∈Set.Ico (-h) 0 := h7.mpr ht
    simp only [Set.indicator_of_mem (hm1.mpr ht),Set.indicator_of_mem (hm2.mpr ht')]
    change B.U (-h) (B.U (t-(-h)) v)=B.U (-1 * -t) v
    have he := congrArg (fun U:H≃ₗᵢ[ℂ]H=>U v) (B.add (-h) (t-(-h)))
    simp only [LinearIsometryEquiv.trans_apply] at he
    rw [←he]
    congr 2 <;> ring
  · have ht' : t∉Set.Ico (-h) 0 := fun hh=>ht (h7.mp hh)
    simp only [Set.indicator_of_notMem (fun hh=>ht (hm1.mp hh)),
      Set.indicator_of_notMem (fun hh=>ht' (hm2.mp hh)),map_zero]
end F1Fecho.RegularBoostedReflection
#print axioms F1Fecho.RegularBoostedReflection.regular_boosted_reflection
