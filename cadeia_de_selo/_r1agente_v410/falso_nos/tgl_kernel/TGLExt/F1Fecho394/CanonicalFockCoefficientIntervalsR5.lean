import TGLExt.F1Fecho394.CanonicalFockCoefficientEmbeddingR2
import TGLExt.F1Fecho394.RegularTranslatedSpectralAdjunctionR2
import TGLExt.F1Fecho394.RegularScalarRealGraphR2
import TGLExt.F1Fecho394.CoefficientGraphCoreR3
/-! Concrete interval generators in the closed Tomita graph of the same
Fock dual weight. Both coefficients are proved from translated finite
regular averages; no equality of the completed Tomita graphs is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockCoefficientIntervals
open MeasureTheory TGLV350.Regular TGLExt.ImportedSQ F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockCoefficientGNS F1Fecho.RegularNormalizedFourier
open F1Fecho.RegularScalarTomitaGraph F1Fecho.RegularScalarRealGraph
open F1Fecho.LpIntervalTotality

 def coefficientPair : (RegularHilbert F×RegularHilbert F)→L[ℝ](GNSHilbert×GNSHilbert) :=
  { toFun := fun p=>(coefficientEmbedding p.1,coefficientEmbedding p.2)
    map_add' := fun p q=>Prod.ext (map_add coefficientEmbedding p.1 q.1)
      (map_add coefficientEmbedding p.2 q.2)
    map_smul' := by
      intro c p
      change (coefficientEmbedding ((c:ℂ) • p.1),coefficientEmbedding ((c:ℂ) • p.2))=
        ((c:ℂ) • coefficientEmbedding p.1,(c:ℂ) • coefficientEmbedding p.2)
      exact Prod.ext (map_smul coefficientEmbedding (c:ℂ) p.1)
        (map_smul coefficientEmbedding (c:ℂ) p.2)
    cont := (coefficientEmbedding.continuous.comp continuous_fst).prodMk
      (coefficientEmbedding.continuous.comp continuous_snd) }

 def coefficientGraph : Submodule ℝ (RegularHilbert F×RegularHilbert F) :=
  (closedGraph weightContext).comap coefficientPair.toLinearMap

 theorem coefficientGraph_closed : IsClosed (coefficientGraph:Set (RegularHilbert F×RegularHilbert F)) :=
  (closedGraph_closed weightContext).preimage coefficientPair.continuous

 theorem coefficientGraph_mem (f g:RegularHilbert F) :
  (f,g)∈coefficientGraph ↔ (coefficientEmbedding f,coefficientEmbedding g)∈closedGraph weightContext := Iff.rfl

 def intervalCore (A:F→L[ℂ]F) (hA:A∈M) (a b:ℝ) (hab:a<b) : finiteStarCore weightContext :=
  ⟨⟨fibre A*(regularUnitary a*RegularCoreAverage.regularAverage fockFlow (b-a)),
    core.mul_mem (fibre_mem A hA) (core.mul_mem (regular_mem a)
      (RegularCoreAverage.regularAverage_mem fockFlow M (b-a)))⟩,
    RegularTranslatedAverage.translated_finite fockFlow A a (b-a) (sub_pos.mpr hab)⟩

 theorem intervalCore_left (A:F→L[ℂ]F) (hA:A∈M) (a b:ℝ) (hab:a<b) :
    coefficientEmbedding (((b-a)⁻¹:ℝ) • intervalVector a b (A vacuum))=
      scalarGNSStarEmbedding weightContext (intervalCore A hA a b hab) := by
  apply Subtype.ext
  change spectralCode _=CanonicalFockGNS.scalarGNSOrbit _
  apply Lp.ext
  exact (RegularTranslatedSpectralAdjunction.translated_coefficient fockFlow vacuum
    fockFlow_vacuum A a b hab).trans
      (scalarGNSOrbit_ae ⟨(intervalCore A hA a b hab).val,
        (intervalCore A hA a b hab).property.1⟩).symm

 theorem intervalCore_right (A:F→L[ℂ]F) (hA:A∈M) (a b:ℝ) (hab:a<b) :
    coefficientEmbedding (((b-a)⁻¹:ℝ) • CoefficientConjugation.reflection
      (CoefficientBoost.multiplier fockFlow (-1) (intervalVector a b (star A vacuum))))=
      scalarGNSStarEmbedding weightContext (star (intervalCore A hA a b hab)) := by
  apply Subtype.ext
  change spectralCode _=CanonicalFockGNS.scalarGNSOrbit _
  apply Lp.ext
  exact (RegularTranslatedSpectralAdjunction.translated_star_coefficient fockFlow vacuum A a b hab).trans
    (scalarGNSOrbit_ae ⟨(star (intervalCore A hA a b hab)).val,
      (star (intervalCore A hA a b hab)).property.1⟩).symm

 theorem interval_pair_mem (A:F→L[ℂ]F) (hA:A∈M) (a b:ℝ) :
    (intervalVector a b (A vacuum),CoefficientConjugation.reflection
      (CoefficientBoost.multiplier fockFlow (-1) (intervalVector a b (star A vacuum))))∈coefficientGraph := by
  by_cases hab:a<b
  · have hp : (((b-a)⁻¹:ℝ) • intervalVector a b (A vacuum),
        ((b-a)⁻¹:ℝ) • CoefficientConjugation.reflection
          (CoefficientBoost.multiplier fockFlow (-1) (intervalVector a b (star A vacuum))))∈coefficientGraph := by
      apply (coefficientGraph_mem _ _).mpr
      have he : (coefficientEmbedding (((b-a)⁻¹:ℝ) • intervalVector a b (A vacuum)),
          coefficientEmbedding (((b-a)⁻¹:ℝ) • CoefficientConjugation.reflection
            (CoefficientBoost.multiplier fockFlow (-1) (intervalVector a b (star A vacuum)))))=
        (scalarGNSStarEmbedding weightContext (intervalCore A hA a b hab),
          scalarGNSStarEmbedding weightContext (star (intervalCore A hA a b hab))) := by
        apply Prod.ext
        · exact intervalCore_left A hA a b hab
        · exact intervalCore_right A hA a b hab
      have hh : (scalarGNSStarEmbedding weightContext (intervalCore A hA a b hab),
          scalarGNSStarEmbedding weightContext (star (intervalCore A hA a b hab)))∈closedGraph weightContext :=
        subset_closure ⟨intervalCore A hA a b hab,rfl⟩
      exact Eq.mpr (congrArg (fun p=>p∈closedGraph weightContext) he) hh
    have hh:=coefficientGraph.smul_mem (b-a) hp
    simpa only [Prod.smul_mk,smul_smul,mul_inv_cancel₀ (sub_pos.mpr hab).ne',one_smul] using hh
  · rw [RegularIntervalVectors.intervalVector_of_ge a b _ (le_of_not_gt hab),
      RegularIntervalVectors.intervalVector_of_ge a b _ (le_of_not_gt hab),map_zero,map_zero]
    exact coefficientGraph.zero_mem
end F1Fecho.CanonicalFockCoefficientIntervals
#print axioms F1Fecho.CanonicalFockCoefficientIntervals.coefficientGraph_closed
#print axioms F1Fecho.CanonicalFockCoefficientIntervals.intervalCore_left
#print axioms F1Fecho.CanonicalFockCoefficientIntervals.intervalCore_right
#print axioms F1Fecho.CanonicalFockCoefficientIntervals.interval_pair_mem
