import TGLExt.F1Fecho394.CanonicalFockGNSR5
import TGLExt.F1Fecho394.CanonicalFockFiniteStarCoreR1
import TGLExt.F1Fecho394.RegularScalarStarDensityR1
/-! Actual finite-square averages supply every approximate-identity hypothesis
of the generic GNS star-density theorem. No density conclusion is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockWeightStarDensity
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockGNS
open F1Fecho.RegularScalarTomitaGraph
open scoped Topology

def averageFamily (h : ℝ) : weightContext.algebra.toStarSubalgebra :=
  ⟨F1Fecho.RegularCoreAverage.regularAverage fockFlow h,
    F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h⟩

theorem averageFamily_finite (h : ℝ) (hh : 0<h) : HasFiniteDualSquare (averageFamily h).val :=
  F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow h hh

theorem averageFamily_bound (h : ℝ) : ‖(averageFamily h).val‖ ≤ 1 :=
  F1Fecho.RegularCoreAverage.regularAverage_norm_le_one fockFlow h

theorem averageFamily_star_strong (v : RegularHilbert F) :
    Tendsto (fun h : ℝ => star (averageFamily h).val v) (𝓝[>] 0) (𝓝 v) :=
  (F1Fecho.RegularFiniteStarCore.regularAverage_star_tendsto_identity fockFlow v).mono_left
    (nhdsWithin_mono _ (by intro h hh; exact ne_of_gt hh))

theorem starEmbedding_denseRange : DenseRange (scalarGNSStarEmbedding weightContext) :=
  F1Fecho.RegularScalarStarDensity.starEmbedding_denseRange weightContext averageFamily
    averageFamily_finite averageFamily_bound averageFamily_star_strong

theorem scalarTomitaGraph_domain_dense : Dense (Prod.fst '' scalarTomitaGraph weightContext) :=
  F1Fecho.RegularScalarStarDensity.graph_domain_dense weightContext averageFamily
    averageFamily_finite averageFamily_bound averageFamily_star_strong
end F1Fecho.CanonicalFockWeightStarDensity
#print axioms F1Fecho.CanonicalFockWeightStarDensity.averageFamily
#print axioms F1Fecho.CanonicalFockWeightStarDensity.averageFamily_finite
#print axioms F1Fecho.CanonicalFockWeightStarDensity.averageFamily_bound
#print axioms F1Fecho.CanonicalFockWeightStarDensity.averageFamily_star_strong
#print axioms F1Fecho.CanonicalFockWeightStarDensity.starEmbedding_denseRange
#print axioms F1Fecho.CanonicalFockWeightStarDensity.scalarTomitaGraph_domain_dense
