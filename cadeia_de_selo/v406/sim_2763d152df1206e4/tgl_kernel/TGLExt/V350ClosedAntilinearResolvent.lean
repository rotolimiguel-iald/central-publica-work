import TGLExt.V350AntilinearAdjointGraph
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.Tactic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open WithLp
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance realHilbert : InnerProductSpace ℝ H := InnerProductSpace.complexToReal
variable (D : Submodule ℂ H) (S : D →ₛₗ[starRingEnd ℂ] H)

/-- The graph is real linear in the Hilbert product; no false complex graph
structure with equal scalars on the two coordinates is imposed. -/
def antilinearL2Graph : Submodule ℝ (WithLp 2 (H × H)) where
  carrier := {p | ∃ x : D, ofLp p = ((x : H),S x)}
  zero_mem' := ⟨0,by simp; rfl⟩
  add_mem' := by
    rintro p q ⟨x,hx⟩ ⟨y,hy⟩
    refine ⟨x+y,?_⟩
    change ofLp p + ofLp q = _
    rw [hx,hy,map_add]
    rfl
  smul_mem' := by
    rintro c p ⟨x,hx⟩
    refine ⟨(c : ℂ) • x,?_⟩
    change c • ofLp p = _
    rw [hx,map_smulₛₗ]
    simp

theorem antilinearL2Graph_closed
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H),S x)))) :
    IsClosed (antilinearL2Graph D S : Set (WithLp 2 (H × H))) := by
  have heq : (antilinearL2Graph D S : Set (WithLp 2 (H × H))) =
      ofLp ⁻¹' Set.range (fun x : D => ((x : H),S x)) := by
    ext p
    constructor <;> rintro ⟨x,hx⟩ <;> exact ⟨x,hx.symm⟩
  rw [heq]
  exact hclosed.preimage (WithLp.prod_continuous_ofLp 2 H H)

/-- Projection on the closed real graph solves the weak resolvent equation.
This produces a vector of D; no density or boundedness of S is assumed. -/
theorem closedAntilinear_weak_resolvent
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H),S x)))) (z : H) :
    ∃ x : D, ∀ u : D,
      (inner ℂ (z-(x : H)) (u : H)).re = (inner ℂ (S x) (S u)).re := by
  let G := antilinearL2Graph D S
  letI : CompleteSpace G := (antilinearL2Graph_closed D S hclosed).completeSpace_coe
  let p := Submodule.starProjection (𝕜 := ℝ) G (toLp 2 (z,(0 : H)))
  obtain ⟨x,hx⟩ := Submodule.starProjection_apply_mem (𝕜 := ℝ) G (toLp 2 (z,(0 : H)))
  refine ⟨x,?_⟩
  intro u
  have hu : toLp 2 ((u : H),S u) ∈ G := ⟨u,rfl⟩
  have ho := Submodule.starProjection_inner_eq_zero (𝕜 := ℝ) (K := G) (toLp 2 (z,(0 : H)))
    (toLp 2 ((u : H),S u)) hu
  rw [WithLp.prod_inner_apply] at ho
  change inner ℝ (z-(ofLp p).1) (u : H) + inner ℝ (0-(ofLp p).2) (S u) = 0 at ho
  change ofLp p = ((x : H),S x) at hx
  rw [hx] at ho
  simp only [zero_sub,inner_neg_left] at ho
  change (inner ℂ (z-(x : H)) (u : H)).re - (inner ℂ (S x) (S u)).re = 0 at ho
  exact sub_eq_zero.mp ho

/-- The imaginary part follows by testing the real variational identity at iu. -/
theorem closedAntilinear_complex_resolvent
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H),S x)))) (z : H) :
    ∃ x : D, ∀ u : D,
      inner ℂ (S u) (S x) = inner ℂ (z-(x : H)) (u : H) := by
  obtain ⟨x,hx⟩ := closedAntilinear_weak_resolvent D S hclosed z
  refine ⟨x,?_⟩
  intro u
  apply Complex.ext
  · exact (inner_re_symm (𝕜 := ℂ) (S u) (S x)).trans (hx u).symm
  · have hi := hx (Complex.I • u)
    change (inner ℂ (z-(x : H)) (Complex.I • (u : H))).re =
      (inner ℂ (S x) (S (Complex.I • u))).re at hi
    rw [map_smulₛₗ,inner_smul_right,inner_smul_right] at hi
    simp only [Complex.conj_I,Complex.I_mul_re,neg_mul,Complex.neg_re] at hi
    have him := inner_im_symm (𝕜 := ℂ) (S u) (S x)
    change (inner ℂ (S u) (S x)).im = -(inner ℂ (S x) (S u)).im at him
    linarith only [hi,him]

#print axioms antilinearL2Graph
#print axioms antilinearL2Graph_closed
#print axioms closedAntilinear_weak_resolvent
#print axioms closedAntilinear_complex_resolvent
end
end TGLV350.Regular
