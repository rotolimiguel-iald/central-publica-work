import Mathlib.Analysis.InnerProductSpace.LinearPMap

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
variable (D : Submodule ℂ H) (S : D →ₛₗ[starRingEnd ℂ] H)

/-- All pairs satisfying the complex antilinear adjoint identity. -/
def antilinearAdjointRelation : Set (H × H) :=
  {p | ∀ x : D, inner ℂ (S x) p.1 = inner ℂ p.2 (x : H)}

/-- The maximal representable domain, without a boundedness assumption on S. -/
def maximalAntilinearAdjointDomain : Submodule ℂ H where
  carrier := {y | ∃ z, (y,z) ∈ antilinearAdjointRelation D S}
  zero_mem' := ⟨0,by intro x; simp⟩
  add_mem' := by
    rintro y w ⟨z,hz⟩ ⟨v,hv⟩
    refine ⟨z+v,?_⟩
    intro x
    simpa only [inner_add_right,inner_add_left] using congrArg₂ (·+·) (hz x) (hv x)
  smul_mem' := by
    rintro c y ⟨z,hz⟩
    refine ⟨(starRingEnd ℂ c) • z,?_⟩
    intro x
    simpa only [inner_smul_right,inner_smul_left,starRingEnd_apply,star_star] using
      congrArg (fun a : ℂ => c*a) (hz x)

def maximalAntilinearAdjointValue (y : maximalAntilinearAdjointDomain D S) : H :=
  Classical.choose y.property

theorem maximalAntilinearAdjointValue_pairing
    (y : maximalAntilinearAdjointDomain D S) (x : D) :
    inner ℂ (S x) (y : H) = inner ℂ (maximalAntilinearAdjointValue D S y) (x : H) :=
  Classical.choose_spec y.property x

variable (hD : Dense (D : Set H))

include hD in
theorem antilinearAdjointRelation_unique {y z w : H}
    (hz : (y,z) ∈ antilinearAdjointRelation D S)
    (hw : (y,w) ∈ antilinearAdjointRelation D S) : z=w := by
  apply hD.eq_of_inner_left ℂ
  intro x hx
  exact (hz ⟨x,hx⟩).symm.trans (hw ⟨x,hx⟩)

/-- A maximal partial antilinear adjoint, with density used for uniqueness. -/
def maximalAntilinearAdjoint : H →ₛₗ.[starRingEnd ℂ] H where
  domain := maximalAntilinearAdjointDomain D S
  toFun := {
    toFun := maximalAntilinearAdjointValue D S
    map_add' := by
      intro y z
      apply hD.eq_of_inner_left ℂ
      intro x hx
      rw [← maximalAntilinearAdjointValue_pairing D S (y+z) ⟨x,hx⟩]
      change inner ℂ (S ⟨x,hx⟩) ((y : H)+(z : H)) = _
      rw [inner_add_right,inner_add_left,
        maximalAntilinearAdjointValue_pairing D S y ⟨x,hx⟩,
        maximalAntilinearAdjointValue_pairing D S z ⟨x,hx⟩]
    map_smul' := by
      intro c y
      apply hD.eq_of_inner_left ℂ
      intro x hx
      rw [← maximalAntilinearAdjointValue_pairing D S (c • y) ⟨x,hx⟩]
      change inner ℂ (S ⟨x,hx⟩) (c • (y : H)) = _
      rw [inner_smul_right,inner_smul_left,
        maximalAntilinearAdjointValue_pairing D S y ⟨x,hx⟩]
      simp only [starRingEnd_apply,star_star]
  }

theorem maximalAntilinearAdjoint_pairing
    (y : maximalAntilinearAdjointDomain D S) (x : D) :
    inner ℂ (S x) (y : H) = inner ℂ (maximalAntilinearAdjoint D S hD y) (x : H) :=
  maximalAntilinearAdjointValue_pairing D S y x

theorem maximalAntilinearAdjoint_maximal {y z : H}
    (h : (y,z) ∈ antilinearAdjointRelation D S) :
    ∃ hy : y ∈ maximalAntilinearAdjointDomain D S,
      maximalAntilinearAdjoint D S hD ⟨y,hy⟩ = z := by
  have hy : y ∈ maximalAntilinearAdjointDomain D S := ⟨z,h⟩
  refine ⟨hy,antilinearAdjointRelation_unique D S hD ?_ h⟩
  exact fun x => maximalAntilinearAdjoint_pairing D S hD ⟨y,hy⟩ x

theorem maximalAntilinearAdjoint_graph_eq :
    Set.range (fun y : maximalAntilinearAdjointDomain D S =>
      ((y : H),maximalAntilinearAdjoint D S hD y)) = antilinearAdjointRelation D S := by
  ext p
  constructor
  · rintro ⟨y,rfl⟩ x
    exact maximalAntilinearAdjoint_pairing D S hD y x
  · intro hp
    obtain ⟨hy,heq⟩ := maximalAntilinearAdjoint_maximal D S hD hp
    exact ⟨⟨p.1,hy⟩,Prod.ext rfl heq⟩

theorem antilinearAdjointRelation_isClosed : IsClosed (antilinearAdjointRelation D S) := by
  have heq : antilinearAdjointRelation D S =
      ⋂ x : D, {p : H × H | inner ℂ (S x) p.1 = inner ℂ p.2 (x : H)} := by
    ext p
    simp only [antilinearAdjointRelation,Set.mem_setOf_eq,Set.mem_iInter]
  rw [heq]
  apply isClosed_iInter
  intro x
  apply isClosed_eq <;> fun_prop

theorem maximalAntilinearAdjoint_isClosed :
    IsClosed (Set.range (fun y : maximalAntilinearAdjointDomain D S =>
      ((y : H),maximalAntilinearAdjoint D S hD y))) := by
  rw [maximalAntilinearAdjoint_graph_eq]
  exact antilinearAdjointRelation_isClosed D S

#print axioms antilinearAdjointRelation
#print axioms maximalAntilinearAdjointDomain
#print axioms maximalAntilinearAdjointValue
#print axioms maximalAntilinearAdjointValue_pairing
#print axioms antilinearAdjointRelation_unique
#print axioms maximalAntilinearAdjoint
#print axioms maximalAntilinearAdjoint_pairing
#print axioms maximalAntilinearAdjoint_maximal
#print axioms maximalAntilinearAdjoint_graph_eq
#print axioms antilinearAdjointRelation_isClosed
#print axioms maximalAntilinearAdjoint_isClosed
end
end TGLV350.Regular
