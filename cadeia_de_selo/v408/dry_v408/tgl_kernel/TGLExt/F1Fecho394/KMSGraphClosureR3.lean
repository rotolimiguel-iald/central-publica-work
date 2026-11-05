import TGLExt.F1Fecho394.StripBoundaryLimitR1
import TGLExt.F1Fecho394.UnitaryCoefficientsUniformR2
/-! The bounded KMS strip relation is closed in the graph vectors
(A Omega,A* Omega), separately in each algebra argument. Thus joint strong-star
vacuum density is sufficient; no operator-norm approximation is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Filter Set
open scoped Topology
namespace F1Fecho.KMSGraphClosure
open F1Fecho.StripMaximum F1Fecho.StripBoundaryLimit
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

def Pair (α : ℝ→H≃ₗᵢ[ℂ]H) (x y : H×H) : Prop :=
  ∃ G : ℂ→ℂ, DiffContOnCl ℂ G strip ∧
    (∃ C : ℝ, ∀ z∈closedStrip, ‖G z‖≤C) ∧
    (∀ t : ℝ, G t=inner ℂ x.2 (α t y.1)) ∧
    (∀ t : ℝ, G ((t:ℂ)+Complex.I)=inner ℂ y.2 (α (-t) x.1))

theorem closed_left (α : ℝ→H≃ₗᵢ[ℂ]H) (y : H×H) :
    IsClosed {x : H×H | Pair α x y} := by
  apply isSeqClosed_iff_isClosed.mp
  intro u x hu hx
  choose F hd hb hl ht using hu
  have hL := UnitaryCoefficientsUniform.left α y.1 (fun n => (u n).2) x.2 ((continuous_snd.tendsto x).comp hx)
  have hU := UnitaryCoefficientsUniform.right (fun t => α (-t)) y.2 (fun n => (u n).1) x.1 ((continuous_fst.tendsto x).comp hx)
  have hle : (fun (n : ℕ) (t : ℝ) => F n t) =
      (fun n t => inner ℂ (u n).2 (α t y.1)) := by funext n t; exact hl n t
  have hue : (fun (n : ℕ) (t : ℝ) => F n ((t:ℂ)+Complex.I)) =
      (fun n t => inner ℂ y.2 (α (-t) (u n).1)) := by funext n t; exact ht n t
  rw [←hle] at hL
  rw [←hue] at hU
  exact of_boundary_uniform F _ _ hd hb hL hU

theorem closed_right (α : ℝ→H≃ₗᵢ[ℂ]H) (x : H×H) :
    IsClosed {y : H×H | Pair α x y} := by
  apply isSeqClosed_iff_isClosed.mp
  intro u y hu hy
  choose F hd hb hl ht using hu
  have hL := UnitaryCoefficientsUniform.right α x.2 (fun n => (u n).1) y.1 ((continuous_fst.tendsto y).comp hy)
  have hU := UnitaryCoefficientsUniform.left (fun t => α (-t)) x.1 (fun n => (u n).2) y.2 ((continuous_snd.tendsto y).comp hy)
  have hle : (fun (n : ℕ) (t : ℝ) => F n t) =
      (fun n t => inner ℂ x.2 (α t (u n).1)) := by funext n t; exact hl n t
  have hue : (fun (n : ℕ) (t : ℝ) => F n ((t:ℂ)+Complex.I)) =
      (fun n t => inner ℂ (u n).2 (α (-t) x.1)) := by funext n t; exact ht n t
  rw [←hle] at hL
  rw [←hue] at hU
  exact of_boundary_uniform F _ _ hd hb hL hU

theorem of_dense_pairs (α : ℝ→H≃ₗᵢ[ℂ]H) (S : Set (H×H))
    (h : ∀ x∈S, ∀ y∈S, Pair α x y)
    (x y : H×H) (hx : x∈closure S) (hy : y∈closure S) : Pair α x y := by
  have hfirst : ∀ a∈S, Pair α a y := by
    intro a ha
    exact (closed_right α a).closure_subset_iff.mpr (h a ha) hy
  exact (closed_left α y).closure_subset_iff.mpr hfirst hx

end F1Fecho.KMSGraphClosure
#print axioms F1Fecho.KMSGraphClosure.closed_left
#print axioms F1Fecho.KMSGraphClosure.closed_right
#print axioms F1Fecho.KMSGraphClosure.of_dense_pairs
