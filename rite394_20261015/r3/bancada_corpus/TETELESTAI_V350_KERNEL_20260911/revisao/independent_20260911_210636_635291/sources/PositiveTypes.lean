import TGLExt.V350GateContract
import TGLV350.RegularGeneratedAlgebra
set_option autoImplicit false
open TGLExt ChatgptAudit TGLV350 TGLV350.Regular
noncomputable section
namespace IndependentReview
def unconditionalInclusion (P : SiteProfile) :
    commutantSet (rTowerImage P) ⊆ commutantSet (commutantSet (towerImage P)) :=
  right_commutant_subset_left_bicommutant P
def originalCertificate : ModularRealizationCertificate := TGLExt.V350Gate.checkedModular
example : RegularHilbert (TowerHilbert mixProfile) =
    MeasureTheory.Lp (TowerHilbert mixProfile) 2 (MeasureTheory.volume : MeasureTheory.Measure ℝ) := rfl
example (t : ℝ) (A : (theFactorObject mixProfile).toStarSubalgebra) :
    regularUnitary mixProfile t * fibre (A : WH →L[ℂ] WH) * star (regularUnitary mixProfile t) =
      fibre (TGLExt.V350Continuous.towerWedgeData.modularFlow t A).val :=
  regular_covariance_on_factor mixProfile t A
example (v : WH) : originalCertificate.J v = towerJ mixProfile v := rfl
#check unconditionalInclusion
#check originalCertificate
#check TGLV350.tower_commutation_equality
#check TGLV350.compression_variable_tendsto
#check TGLV350.Regular.regularCore_minimal
#check TGLV350.Regular.regularCoreEmbedding_injective
#check TGLV350.Regular.regular_strongly_continuous
#print axioms unconditionalInclusion
#print axioms originalCertificate
end IndependentReview
end
