import TGLExt.F1Fecho394.RegularScalarGaussianGNSR2
import TGLExt.V350DualOrbitVonNeumann
import TGLExt.V350VectorTomitaClosability
import TGLExt.F1Fecho394.RegularScalarTomitaGraphR1
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.RegularScalarTomitaClosure
open TGLExt TGLV350.Regular F1Fecho.RegularScalarGNS
open F1Fecho.RegularScalarGaussian F1Fecho.RegularScalarGaussianGNS F1Fecho.RegularScalarTomitaGraph
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
noncomputable section

theorem scalarGaussianImage_separating (D : Context H)
    (B : RegularHilbert (RegularHilbert H) →L[ℂ]
      RegularHilbert (RegularHilbert H))
    (hB : B ∈ dualOrbitVonNeumann D.algebra)
    (hz : B (scalarGaussianVacuum D) = 0) : B = 0 := by
  obtain ⟨A,hA,rfl⟩ := (mem_dualOrbitVonNeumann_iff D.algebra B).mp hB
  rw [scalarGaussianVacuum_separating D A hA hz,map_zero]

theorem scalarGaussian_maps_graph (D : Context H) :
    Set.MapsTo (Prod.map (scalarGaussianGNSMap D) (scalarGaussianGNSMap D))
      (scalarTomitaGraph D)
      (vectorTomitaGraph (dualOrbitVonNeumann D.algebra) (scalarGaussianVacuum D)) := by
  rintro p ⟨A,rfl⟩
  refine ⟨dualOrbitRepresentation A.val.val,
    (mem_dualOrbitVonNeumann_iff D.algebra _).mpr ⟨A.val.val,A.val.property,rfl⟩,?_⟩
  apply Prod.ext
  · exact scalarGaussianGNSMap_embedding D ⟨A.val,A.property.1⟩
  · change scalarGaussianGNSMap D
      (GNSEmbedding D ⟨(star A).val,(star A).property.1⟩) = _
    rw [scalarGaussianGNSMap_embedding]
    change dualOrbitRepresentation (star A.val.val) (scalarGaussianVacuum D) =
      (star (dualOrbitRepresentation A.val.val)) (scalarGaussianVacuum D)
    rw [map_star]

theorem scalarGaussian_maps_graph_closure (D : Context H) :
    Set.MapsTo (Prod.map (scalarGaussianGNSMap D) (scalarGaussianGNSMap D))
      (closure (scalarTomitaGraph D))
      (closure (vectorTomitaGraph (dualOrbitVonNeumann D.algebra)
        (scalarGaussianVacuum D))) := by
  apply (scalarGaussian_maps_graph D).closure
  exact (scalarGaussianGNSMap D).continuous.prodMap (scalarGaussianGNSMap D).continuous

/-- The original scalar-weight GNS graph is closable. The auxiliary graph is
used only through a continuous injective map of the original Hilbert space. -/
theorem scalarTomitaGraph_closure_vertical (D : Context H) (y : GNSHilbert D)
    (hy : (0,y) ∈ closure (scalarTomitaGraph D)) : y = 0 := by
  have hh := scalarGaussian_maps_graph_closure D hy
  have ht : (0,scalarGaussianGNSMap D y) ∈
      closure (vectorTomitaGraph (dualOrbitVonNeumann D.algebra)
        (scalarGaussianVacuum D)) := by
    simpa only [Prod.map_apply,map_zero] using hh
  have hz := vectorTomita_closure_vertical (dualOrbitVonNeumann D.algebra)
    (scalarGaussianVacuum D) (scalarGaussianImage_separating D) _ ht
  apply scalarGaussianGNSMap_injective D
  simpa only [map_zero] using hz

theorem scalarTomitaGraph_closure_single_valued (D : Context H)
    (x y z : GNSHilbert D)
    (hy : (x,y) ∈ closure (scalarTomitaGraph D))
    (hz : (x,z) ∈ closure (scalarTomitaGraph D)) : y = z := by
  apply scalarGaussianGNSMap_injective D
  exact vectorTomita_closure_single_valued (dualOrbitVonNeumann D.algebra)
    (scalarGaussianVacuum D) (scalarGaussianImage_separating D) _ _ _
    (scalarGaussian_maps_graph_closure D hy) (scalarGaussian_maps_graph_closure D hz)

#print axioms scalarGaussianImage_separating
#print axioms scalarGaussian_maps_graph
#print axioms scalarGaussian_maps_graph_closure
#print axioms scalarTomitaGraph_closure_vertical
#print axioms scalarTomitaGraph_closure_single_valued
end
end F1Fecho.RegularScalarTomitaClosure
