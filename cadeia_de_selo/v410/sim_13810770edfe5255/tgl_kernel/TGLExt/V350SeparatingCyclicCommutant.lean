import TGLExt.V350RegularGeneratedAlgebra
import TGLExt.InvariantProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def vectorOrbitLinear (N : VonNeumannAlgebra H) (v : H) : N.toStarSubalgebra →ₗ[ℂ] H where
  toFun A := A.val v
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

def vectorOrbitSubspace (N : VonNeumannAlgebra H) (v : H) : Submodule ℂ H :=
  (vectorOrbitLinear N v).range.topologicalClosure

instance vectorOrbitSubspace_complete (N : VonNeumannAlgebra H) (v : H) :
    CompleteSpace (vectorOrbitSubspace N v) :=
  Submodule.topologicalClosure.completeSpace (vectorOrbitLinear N v).range

theorem vectorOrbitSubspace_invariant (N : VonNeumannAlgebra H) (v : H)
    (A : H →L[ℂ] H) (hA : A ∈ N) : Invariant A (vectorOrbitSubspace N v) := by
  have ht : Set.MapsTo A ((vectorOrbitLinear N v).range : Set H)
      ((vectorOrbitLinear N v).range : Set H) := by
    rintro _ ⟨B,rfl⟩
    exact ⟨(⟨A,hA⟩ : N.toStarSubalgebra) * B,rfl⟩
  exact ht.closure A.continuous

/-- Separating for N implies that the orbit of N' is norm dense. No cyclic
assumption on the original N-orbit is used. -/
theorem separating_commutant_orbit_top (N : VonNeumannAlgebra H) (v : H)
    (hsep : ∀ A ∈ N, A v = 0 → A = 0) : vectorOrbitSubspace N.commutant v = ⊤ := by
  let E := vectorOrbitSubspace N.commutant v
  have hp : E.starProjection ∈ N := by
    have hsub : N.commutant.commutant ≤ N := by
      rw [VonNeumannAlgebra.commutant_commutant]
    apply hsub
    rw [VonNeumannAlgebra.mem_commutant_iff]
    intro A hA
    ext1 x
    exact (starProjection_commutes_of_invariant A E
      (vectorOrbitSubspace_invariant N.commutant v A hA)
      (vectorOrbitSubspace_invariant N.commutant v (star A)
        (N.commutant.toStarSubalgebra.star_mem' hA)) x).symm
  have hv : v ∈ E :=
    (vectorOrbitLinear N.commutant v).range.le_topologicalClosure ⟨1,rfl⟩
  have hpv : E.starProjection v = v := Submodule.starProjection_eq_self_iff.mpr hv
  have hq : (1 - E.starProjection : H →L[ℂ] H) = 0 :=
    hsep (1-E.starProjection) (N.sub_mem N.one_mem hp) (by
      change v - E.starProjection v = 0
      rw [hpv,sub_self])
  have hp1 : E.starProjection = 1 := (sub_eq_zero.mp hq).symm
  apply top_unique
  intro x _
  have hx := Submodule.starProjection_apply_mem E x
  rwa [hp1,one_apply_eq_self] at hx

theorem separating_commutant_orbit_dense (N : VonNeumannAlgebra H) (v : H)
    (hsep : ∀ A ∈ N, A v = 0 → A = 0) :
    DenseRange (fun A : N.commutant.toStarSubalgebra => A.val v) := by
  have ht := separating_commutant_orbit_top N v hsep
  change (vectorOrbitLinear N.commutant v).range.topologicalClosure = ⊤ at ht
  change Dense (Set.range (fun A : N.commutant.toStarSubalgebra => A.val v))
  rw [dense_iff_closure_eq]
  exact congrArg (fun S : Submodule ℂ H => (S : Set H)) ht

#print axioms vectorOrbitLinear
#print axioms vectorOrbitSubspace
#print axioms vectorOrbitSubspace_complete
#print axioms vectorOrbitSubspace_invariant
#print axioms separating_commutant_orbit_top
#print axioms separating_commutant_orbit_dense
end
end TGLV350.Regular
