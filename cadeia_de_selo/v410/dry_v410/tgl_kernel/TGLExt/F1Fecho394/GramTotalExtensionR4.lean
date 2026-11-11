import Mathlib.Analysis.Normed.Operator.Extend
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.LinearAlgebra.Finsupp.LinearCombination
/-!
Gram-preserving transport on a total family, extended by the existing bounded
linear extension theorem. No linear independence, isometry, extension or inverse
is assumed. Totality of the target family is needed only for surjectivity.
-/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.GramExtension

variable {𝕜 : Type*} [RCLike 𝕜] {ι : Type*}
variable {E F : Type*}
variable [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]
variable [NormedAddCommGroup F] [InnerProductSpace 𝕜 F]

abbrev Total (f : ι → E) : Prop :=
  (Submodule.span 𝕜 (Set.range f)).topologicalClosure = ⊤

abbrev GramEqual (f : ι → E) (g : ι → F) : Prop :=
  ∀ i j, inner 𝕜 (g i) (g j) = inner 𝕜 (f i) (f j)

theorem linearCombination_inner (f : ι → E) (g : ι → F)
    (hg : GramEqual (𝕜 := 𝕜) f g) (a b : ι →₀ 𝕜) :
    inner 𝕜 (Finsupp.linearCombination 𝕜 g a) (Finsupp.linearCombination 𝕜 g b) =
      inner 𝕜 (Finsupp.linearCombination 𝕜 f a) (Finsupp.linearCombination 𝕜 f b) := by
  classical
  simp only [Finsupp.linearCombination_apply, Finsupp.sum, sum_inner, inner_sum,
    inner_smul_left, inner_smul_right, hg]

theorem linearCombination_norm (f : ι → E) (g : ι → F)
    (hg : GramEqual (𝕜 := 𝕜) f g) (a : ι →₀ 𝕜) :
    ‖Finsupp.linearCombination 𝕜 g a‖ = ‖Finsupp.linearCombination 𝕜 f a‖ := by
  rw [norm_eq_sqrt_re_inner (𝕜 := 𝕜), norm_eq_sqrt_re_inner (𝕜 := 𝕜)]
  rw [linearCombination_inner (𝕜 := 𝕜) f g hg]

theorem dense_linearCombination (f : ι → E) (hf : Total (𝕜 := 𝕜) f) :
    DenseRange (Finsupp.linearCombination 𝕜 f) := by
  have h : Dense (Submodule.span 𝕜 (Set.range f) : Set E) :=
    Submodule.dense_iff_topologicalClosure_eq_top.mpr hf
  change Dense (Set.range (Finsupp.linearCombination 𝕜 f))
  simpa only [← Finsupp.range_linearCombination, LinearMap.coe_range] using h

variable [CompleteSpace F]

def extensionMap (f : ι → E) (g : ι → F) : E →L[𝕜] F :=
  (Finsupp.linearCombination 𝕜 g).extendOfNorm (Finsupp.linearCombination 𝕜 f)

theorem extensionMap_linearCombination (f : ι → E) (g : ι → F)
    (hg : GramEqual (𝕜 := 𝕜) f g) (hf : Total (𝕜 := 𝕜) f) (a : ι →₀ 𝕜) :
    extensionMap (𝕜 := 𝕜) f g (Finsupp.linearCombination 𝕜 f a) = Finsupp.linearCombination 𝕜 g a := by
  apply LinearMap.extendOfNorm_eq (dense_linearCombination (𝕜 := 𝕜) f hf)
  exact ⟨1, fun b => by simpa [linearCombination_norm (𝕜 := 𝕜) f g hg b]⟩

theorem extensionMap_norm (f : ι → E) (g : ι → F)
    (hg : GramEqual (𝕜 := 𝕜) f g) (hf : Total (𝕜 := 𝕜) f) (x : E) : ‖extensionMap (𝕜 := 𝕜) f g x‖ = ‖x‖ := by
  refine (dense_linearCombination (𝕜 := 𝕜) f hf).induction ?_
    (isClosed_eq (extensionMap (𝕜 := 𝕜) f g).continuous.norm continuous_norm) x
  rintro _ ⟨a,rfl⟩
  rw [extensionMap_linearCombination (𝕜 := 𝕜) f g hg hf, linearCombination_norm (𝕜 := 𝕜) f g hg]

def isometry (f : ι → E) (g : ι → F) (hg : GramEqual (𝕜 := 𝕜) f g) (hf : Total (𝕜 := 𝕜) f) : E →ₗᵢ[𝕜] F where
  toLinearMap := (extensionMap (𝕜 := 𝕜) f g).toLinearMap
  norm_map' := extensionMap_norm (𝕜 := 𝕜) f g hg hf

theorem isometry_apply (f : ι → E) (g : ι → F)
    (hg : GramEqual (𝕜 := 𝕜) f g) (hf : Total (𝕜 := 𝕜) f) (i : ι) : isometry (𝕜 := 𝕜) f g hg hf (f i) = g i := by
  change extensionMap (𝕜 := 𝕜) f g (f i) = g i
  have h := extensionMap_linearCombination (𝕜 := 𝕜) f g hg hf (Finsupp.single i 1)
  simpa only [Finsupp.linearCombination_single, one_smul] using h

variable [CompleteSpace E]

def equivalence (f : ι → E) (g : ι → F)
    (hg : GramEqual (𝕜 := 𝕜) f g) (hf : Total (𝕜 := 𝕜) f) (ht : Total (𝕜 := 𝕜) g) : E ≃ₗᵢ[𝕜] F :=
  (LinearEquiv.refl 𝕜 (ι →₀ 𝕜)).extendOfIsometry
    (Finsupp.linearCombination 𝕜 f) (Finsupp.linearCombination 𝕜 g)
    (dense_linearCombination (𝕜 := 𝕜) f hf) (dense_linearCombination (𝕜 := 𝕜) g ht)
    (linearCombination_norm (𝕜 := 𝕜) f g hg)

theorem equivalence_apply (f : ι → E) (g : ι → F)
    (hg : GramEqual (𝕜 := 𝕜) f g) (hf : Total (𝕜 := 𝕜) f) (ht : Total (𝕜 := 𝕜) g) (i : ι) :
    equivalence (𝕜 := 𝕜) f g hg hf ht (f i) = g i := by
  unfold equivalence
  have h := LinearEquiv.extendOfIsometry_eq
    (LinearEquiv.refl 𝕜 (ι →₀ 𝕜))
    (Finsupp.linearCombination 𝕜 f) (Finsupp.linearCombination 𝕜 g)
    (dense_linearCombination (𝕜 := 𝕜) f hf) (dense_linearCombination (𝕜 := 𝕜) g ht)
    (linearCombination_norm (𝕜 := 𝕜) f g hg) (Finsupp.single i 1)
  simpa only [LinearEquiv.refl_apply, Finsupp.linearCombination_single, one_smul] using h


/-- Uniqueness among continuous linear maps follows from the total source family. -/
theorem extensionMap_unique (f : ι → E) (g : ι → F)
    (hg : GramEqual (𝕜 := 𝕜) f g) (hf : Total (𝕜 := 𝕜) f)
    (T : E →L[𝕜] F) (hT : ∀ i, T (f i) = g i) :
    T = extensionMap (𝕜 := 𝕜) f g := by
  apply ContinuousLinearMap.ext
  intro x
  refine (dense_linearCombination (𝕜 := 𝕜) f hf).induction ?_
    (isClosed_eq T.continuous (extensionMap (𝕜 := 𝕜) f g).continuous) x
  rintro _ ⟨a,rfl⟩
  rw [extensionMap_linearCombination (𝕜 := 𝕜) f g hg hf]
  classical
  simp only [Finsupp.linearCombination_apply, Finsupp.sum, map_sum, map_smul, hT]

/-- A surjective reindexing and nonzero weights do not change the algebraic span. -/
theorem span_weighted_reindex (v : ι → E) (c : ι → 𝕜) (σ : ι → ι)
    (hc : ∀ i, c i ≠ 0) (hσ : Function.Surjective σ) :
    Submodule.span 𝕜 (Set.range (fun i => c i • v (σ i))) =
      Submodule.span 𝕜 (Set.range v) := by
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro _ ⟨i,rfl⟩
    exact (Submodule.span 𝕜 (Set.range v)).smul_mem (c i)
      (Submodule.subset_span ⟨σ i,rfl⟩)
  · apply Submodule.span_le.mpr
    rintro _ ⟨j,rfl⟩
    obtain ⟨i,hi⟩ := hσ j
    have h : c i • v j ∈ Submodule.span 𝕜 (Set.range (fun i => c i • v (σ i))) := by
      rw [← hi]
      exact Submodule.subset_span ⟨i,rfl⟩
    have h' := (Submodule.span 𝕜 (Set.range (fun i => c i • v (σ i)))).smul_mem (c i)⁻¹ h
    change v j ∈ Submodule.span 𝕜 (Set.range (fun i => c i • v (σ i)))
    simpa only [smul_smul, inv_mul_cancel₀ (hc i), one_smul] using h'

theorem total_weighted_reindex (v : ι → E) (c : ι → 𝕜) (σ : ι → ι)
    (hc : ∀ i, c i ≠ 0) (hσ : Function.Surjective σ) (hv : Total (𝕜 := 𝕜) v) :
    Total (𝕜 := 𝕜) (fun i => c i • v (σ i)) := by
  unfold Total at hv ⊢
  rw [span_weighted_reindex v c σ hc hσ]
  exact hv

end F1Fecho.GramExtension

#print axioms F1Fecho.GramExtension.linearCombination_inner
#print axioms F1Fecho.GramExtension.linearCombination_norm
#print axioms F1Fecho.GramExtension.dense_linearCombination
#print axioms F1Fecho.GramExtension.extensionMap_linearCombination
#print axioms F1Fecho.GramExtension.extensionMap_norm
#print axioms F1Fecho.GramExtension.isometry
#print axioms F1Fecho.GramExtension.isometry_apply
#print axioms F1Fecho.GramExtension.equivalence
#print axioms F1Fecho.GramExtension.equivalence_apply

#print axioms F1Fecho.GramExtension.extensionMap_unique
#print axioms F1Fecho.GramExtension.span_weighted_reindex
#print axioms F1Fecho.GramExtension.total_weighted_reindex
