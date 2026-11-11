import Mathlib.Analysis.InnerProductSpace.StandardSubspace
import Mathlib.Analysis.InnerProductSpace.LinearMap

/-! Extend symplectic orthogonality of generators to their closed real spans. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.GenericSymplecticSpan
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

theorem swap_zero {x y : H} (h : (inner ℂ x y).im = 0) :
    (inner ℂ y x).im = 0 := by
  have he := congrArg Complex.im (inner_conj_symm (𝕜 := ℂ) y x)
  simpa only [Complex.conj_im,h,neg_zero] using he.symm

theorem closed_span_zero (S : Set H) (y : H)
    (h : ∀ x ∈ S, (inner ℂ x y).im = 0)
    (x : H) (hx : x ∈ (Submodule.span ℝ S).topologicalClosure) :
    (inner ℂ x y).im = 0 := by
  let L : H →L[ℝ] ℝ := Complex.imCLM.comp ((innerSL ℂ y).restrictScalars ℝ)
  have hs : Submodule.span ℝ S ≤ L.ker := by
    apply Submodule.span_le.mpr
    intro z hz
    exact swap_zero (h z hz)
  have hc : (Submodule.span ℝ S).topologicalClosure ≤ L.ker :=
    Submodule.topologicalClosure_minimal _ hs L.isClosed_ker
  exact swap_zero (hc hx)

theorem closed_spans_zero (S T : Set H)
    (h : ∀ x ∈ S, ∀ y ∈ T, (inner ℂ x y).im = 0)
    (x y : H) (hx : x ∈ (Submodule.span ℝ S).topologicalClosure)
    (hy : y ∈ (Submodule.span ℝ T).topologicalClosure) :
    (inner ℂ x y).im = 0 := by
  apply swap_zero
  exact closed_span_zero T x (fun z hz => swap_zero (closed_span_zero S z
    (fun w hw => h w hw z hz) x hx)) y hy

end F1Fecho.GenericSymplecticSpan
#print axioms F1Fecho.GenericSymplecticSpan.closed_spans_zero
