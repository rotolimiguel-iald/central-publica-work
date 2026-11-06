import TGLExt.V350AntilinearAdjointGraph
import TGLExt.V350ScalarClosedTomita

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable (P : SiteProfile)

def scalarTomitaAdjointDomain : Submodule ℂ (ScalarGNSHilbert P) :=
  maximalAntilinearAdjointDomain (scalarClosedTomitaDomain P) (scalarClosedTomita P)

/-- The maximal complex-antilinear adjoint of the same closed operator on H_I. -/
def scalarTomitaAdjoint : ScalarGNSHilbert P →ₛₗ.[starRingEnd ℂ] ScalarGNSHilbert P :=
  maximalAntilinearAdjoint (scalarClosedTomitaDomain P) (scalarClosedTomita P)
    (scalarClosedTomita_domain_dense (P := P))

theorem scalarTomitaAdjoint_pairing (y : scalarTomitaAdjointDomain P)
    (x : scalarClosedTomitaDomain P) :
    inner ℂ (scalarClosedTomita P x) (y : ScalarGNSHilbert P) =
      inner ℂ (scalarTomitaAdjoint P y) (x : ScalarGNSHilbert P) :=
  maximalAntilinearAdjoint_pairing _ _ _ y x

theorem scalarTomitaAdjoint_maximal {y z : ScalarGNSHilbert P}
    (h : ∀ x : scalarClosedTomitaDomain P,
      inner ℂ (scalarClosedTomita P x) y = inner ℂ z (x : ScalarGNSHilbert P)) :
    ∃ hy : y ∈ scalarTomitaAdjointDomain P, scalarTomitaAdjoint P ⟨y,hy⟩ = z :=
  maximalAntilinearAdjoint_maximal _ _ _ h

theorem scalarTomitaAdjoint_domain_iff (y : ScalarGNSHilbert P) :
    y ∈ scalarTomitaAdjointDomain P ↔ ∃ z : ScalarGNSHilbert P,
      ∀ x : scalarClosedTomitaDomain P,
        inner ℂ (scalarClosedTomita P x) y = inner ℂ z (x : ScalarGNSHilbert P) := Iff.rfl

theorem scalarTomitaAdjoint_isClosed :
    IsClosed (Set.range (fun y : scalarTomitaAdjointDomain P =>
      ((y : ScalarGNSHilbert P),scalarTomitaAdjoint P y))) :=
  maximalAntilinearAdjoint_isClosed _ _ _

/-- Pullback by the bounded Gaussian adjoint supplies actual domain vectors.
It uses no inverse of the Gaussian transport. -/
theorem scalarTomitaAdjoint_gaussian_pairing
    (B : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)))
    (hB : B ∈ (dualOrbitVonNeumann (regularCoreAlgebra P)).commutant)
    (x : scalarClosedTomitaDomain P) :
    inner ℂ (scalarClosedTomita P x)
        ((scalarGaussianGNSMap P).adjoint (B (scalarGaussianVacuum P))) =
      inner ℂ ((scalarGaussianGNSMap P).adjoint ((star B) (scalarGaussianVacuum P)))
        (x : ScalarGNSHilbert P) := by
  calc
    _ = inner ℂ (scalarGaussianGNSMap P (scalarClosedTomita P x))
        (B (scalarGaussianVacuum P)) :=
      (scalarGaussianGNSMap P).adjoint_inner_right _ _
    _ = inner ℂ ((star B) (scalarGaussianVacuum P))
        (scalarGaussianGNSMap P (x : ScalarGNSHilbert P)) :=
      vectorTomita_closure_pairing _ _ _
        (scalarGaussian_maps_graph_closure P (scalarClosedTomita_graph x)) B hB
    _ = _ := ((scalarGaussianGNSMap P).adjoint_inner_left _ _).symm

theorem scalarTomitaAdjoint_gaussian_domain
    (B : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)))
    (hB : B ∈ (dualOrbitVonNeumann (regularCoreAlgebra P)).commutant) :
    (scalarGaussianGNSMap P).adjoint (B (scalarGaussianVacuum P)) ∈
      scalarTomitaAdjointDomain P :=
  ⟨(scalarGaussianGNSMap P).adjoint ((star B) (scalarGaussianVacuum P)),
    scalarTomitaAdjoint_gaussian_pairing P B hB⟩

/-- Density is proved on H_I from Gaussian injectivity and the dense commutant
orbit of the auxiliary separating vector, not assumed as an adjoint property. -/
theorem scalarTomitaAdjoint_domain_dense :
    Dense (scalarTomitaAdjointDomain P : Set (ScalarGNSHilbert P)) := by
  have ho : (scalarTomitaAdjointDomain P).orthogonal = ⊥ := by
    apply le_antisymm ?_ bot_le
    intro v hv
    change v=0
    apply scalarGaussianGNSMap_injective P
    rw [map_zero]
    apply (separating_commutant_orbit_dense
      (dualOrbitVonNeumann (regularCoreAlgebra P)) (scalarGaussianVacuum P)
      (scalarGaussianImage_separating P)).eq_zero_of_inner_right (𝕜 := ℂ)
    intro B
    rw [← (scalarGaussianGNSMap P).adjoint_inner_left]
    exact hv _ (scalarTomitaAdjoint_gaussian_domain P B.val B.property)
  rw [dense_iff_closure_eq]
  exact congrArg (fun V : Submodule ℂ (ScalarGNSHilbert P) => (V : Set (ScalarGNSHilbert P)))
    ((scalarTomitaAdjointDomain P).topologicalClosure_eq_top_iff.mpr ho)

theorem scalarTomitaAdjoint_swap {y z : ScalarGNSHilbert P}
    (h : ∀ x : scalarClosedTomitaDomain P,
      inner ℂ (scalarClosedTomita P x) y = inner ℂ z (x : ScalarGNSHilbert P)) :
    ∀ x : scalarClosedTomitaDomain P,
      inner ℂ (scalarClosedTomita P x) z = inner ℂ y (x : ScalarGNSHilbert P) := by
  intro x
  have hh := h ⟨scalarClosedTomita P x,scalarClosedTomita_maps_domain x⟩
  rw [scalarClosedTomita_involutive] at hh
  have hc := congrArg (starRingEnd ℂ) hh
  calc
    _ = (starRingEnd ℂ) (inner ℂ z (scalarClosedTomita P x)) :=
      (inner_conj_symm (𝕜 := ℂ) (scalarClosedTomita P x) z).symm
    _ = (starRingEnd ℂ) (inner ℂ (x : ScalarGNSHilbert P) y) := hc.symm
    _ = _ := inner_conj_symm (𝕜 := ℂ) y (x : ScalarGNSHilbert P)

theorem scalarTomitaAdjoint_maps_domain (y : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjoint P y ∈ scalarTomitaAdjointDomain P :=
  ⟨(y : ScalarGNSHilbert P),scalarTomitaAdjoint_swap P (scalarTomitaAdjoint_pairing P y)⟩

theorem scalarTomitaAdjoint_involutive (y : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjoint P
        ⟨scalarTomitaAdjoint P y,scalarTomitaAdjoint_maps_domain P y⟩ = y := by
  apply antilinearAdjointRelation_unique (scalarClosedTomitaDomain P) (scalarClosedTomita P)
    (scalarClosedTomita_domain_dense (P := P))
  · exact scalarTomitaAdjoint_pairing P ⟨_,scalarTomitaAdjoint_maps_domain P y⟩
  · exact scalarTomitaAdjoint_swap P (scalarTomitaAdjoint_pairing P y)

#print axioms scalarTomitaAdjointDomain
#print axioms scalarTomitaAdjoint
#print axioms scalarTomitaAdjoint_pairing
#print axioms scalarTomitaAdjoint_maximal
#print axioms scalarTomitaAdjoint_domain_iff
#print axioms scalarTomitaAdjoint_isClosed
#print axioms scalarTomitaAdjoint_gaussian_pairing
#print axioms scalarTomitaAdjoint_gaussian_domain
#print axioms scalarTomitaAdjoint_domain_dense
#print axioms scalarTomitaAdjoint_swap
#print axioms scalarTomitaAdjoint_maps_domain
#print axioms scalarTomitaAdjoint_involutive
end
end TGLV350.Regular
