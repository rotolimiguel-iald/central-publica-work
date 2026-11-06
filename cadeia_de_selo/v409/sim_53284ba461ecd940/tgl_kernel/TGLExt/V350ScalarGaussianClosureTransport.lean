import TGLExt.V350ScalarGaussianGNSMap
import TGLExt.V350DualOrbitVonNeumann
import TGLExt.V350VectorTomitaClosability
import TGLExt.V350ScalarTomitaGraph

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section

theorem scalarGaussianImage_separating (P : SiteProfile)
    (B : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)))
    (hB : B ∈ dualOrbitVonNeumann (regularCoreAlgebra P))
    (hz : B (scalarGaussianVacuum P) = 0) : B = 0 := by
  obtain ⟨A,hA,rfl⟩ := (mem_dualOrbitVonNeumann_iff (regularCoreAlgebra P) B).mp hB
  rw [scalarGaussianVacuum_separating P A hA hz,map_zero]

theorem scalarGaussian_maps_graph (P : SiteProfile) :
    Set.MapsTo (Prod.map (scalarGaussianGNSMap P) (scalarGaussianGNSMap P))
      (scalarTomitaGraph P)
      (vectorTomitaGraph (dualOrbitVonNeumann (regularCoreAlgebra P)) (scalarGaussianVacuum P)) := by
  rintro p ⟨A,rfl⟩
  refine ⟨dualOrbitRepresentation A.val.val,
    (mem_dualOrbitVonNeumann_iff (regularCoreAlgebra P) _).mpr ⟨A.val.val,A.val.property,rfl⟩,?_⟩
  apply Prod.ext
  · exact scalarGaussianGNSMap_embedding P ⟨A.val,A.property.1⟩
  · change scalarGaussianGNSMap P
      (scalarGNSEmbedding P ⟨(star A).val,(star A).property.1⟩) = _
    rw [scalarGaussianGNSMap_embedding]
    change dualOrbitRepresentation (star A.val.val) (scalarGaussianVacuum P) =
      (star (dualOrbitRepresentation A.val.val)) (scalarGaussianVacuum P)
    rw [map_star]

theorem scalarGaussian_maps_graph_closure (P : SiteProfile) :
    Set.MapsTo (Prod.map (scalarGaussianGNSMap P) (scalarGaussianGNSMap P))
      (closure (scalarTomitaGraph P))
      (closure (vectorTomitaGraph (dualOrbitVonNeumann (regularCoreAlgebra P))
        (scalarGaussianVacuum P))) := by
  apply (scalarGaussian_maps_graph P).closure
  exact (scalarGaussianGNSMap P).continuous.prodMap (scalarGaussianGNSMap P).continuous

/-- The original scalar-weight GNS graph is closable. The auxiliary graph is
used only through a continuous injective map of the original Hilbert space. -/
theorem scalarTomitaGraph_closure_vertical (P : SiteProfile) (y : ScalarGNSHilbert P)
    (hy : (0,y) ∈ closure (scalarTomitaGraph P)) : y = 0 := by
  have hh := scalarGaussian_maps_graph_closure P hy
  have ht : (0,scalarGaussianGNSMap P y) ∈
      closure (vectorTomitaGraph (dualOrbitVonNeumann (regularCoreAlgebra P))
        (scalarGaussianVacuum P)) := by
    simpa only [Prod.map_apply,map_zero] using hh
  have hz := vectorTomita_closure_vertical (dualOrbitVonNeumann (regularCoreAlgebra P))
    (scalarGaussianVacuum P) (scalarGaussianImage_separating P) _ ht
  apply scalarGaussianGNSMap_injective P
  simpa only [map_zero] using hz

theorem scalarTomitaGraph_closure_single_valued (P : SiteProfile)
    (x y z : ScalarGNSHilbert P)
    (hy : (x,y) ∈ closure (scalarTomitaGraph P))
    (hz : (x,z) ∈ closure (scalarTomitaGraph P)) : y = z := by
  apply scalarGaussianGNSMap_injective P
  exact vectorTomita_closure_single_valued (dualOrbitVonNeumann (regularCoreAlgebra P))
    (scalarGaussianVacuum P) (scalarGaussianImage_separating P) _ _ _
    (scalarGaussian_maps_graph_closure P hy) (scalarGaussian_maps_graph_closure P hz)

#print axioms scalarGaussianImage_separating
#print axioms scalarGaussian_maps_graph
#print axioms scalarGaussian_maps_graph_closure
#print axioms scalarTomitaGraph_closure_vertical
#print axioms scalarTomitaGraph_closure_single_valued
end
end TGLV350.Regular
