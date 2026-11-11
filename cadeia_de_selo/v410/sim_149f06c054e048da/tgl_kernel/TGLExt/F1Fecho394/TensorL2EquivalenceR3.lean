import TGLExt.F1Fecho394.GramTotalExtensionR4
import Mathlib.Analysis.InnerProductSpace.TensorProduct
import Mathlib.Analysis.InnerProductSpace.Completion
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.SimpleFuncDenseLp
/-! A constructed unitary from the completed scalar L2 tensor product to vector L2.
The scalar/vector product is first proved Gram preserving. Surjectivity follows
from the actual density of simple functions, not from an assumed tensor model. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory UniformSpace
open scoped TensorProduct ENNReal
namespace F1Fecho.TensorL2
variable {X E : Type*} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (μ : Measure X)
abbrev Scalar := Lp ℂ 2 μ
abbrev Vector := Lp E 2 μ
abbrev Completed := Completion (Scalar μ ⊗[ℂ] E)

def pure (p : Scalar μ × E) : Completed (E:=E) μ := (p.1 ⊗ₜ[ℂ] p.2 : Scalar μ ⊗[ℂ] E)
def pointwise (p : Scalar μ × E) : Vector (E:=E) μ :=
  (ContinuousLinearMap.toSpanSingleton ℂ p.2).compLp p.1
lemma pointwise_ae (p : Scalar μ × E) : pointwise μ p =ᵐ[μ] fun x => p.1 x • p.2 :=
  (ContinuousLinearMap.toSpanSingleton ℂ p.2).coeFn_compLp p.1

theorem gram : GramExtension.GramEqual (𝕜:=ℂ) (pure (E:=E) μ) (pointwise μ) := by
  intro p q
  rw [show inner ℂ (pure μ p) (pure μ q)=inner ℂ p.1 q.1 * inner ℂ p.2 q.2 by
    simp only [pure,Completion.inner_coe,TensorProduct.inner_tmul]]
  rw [L2.inner_def,L2.inner_def,← integral_mul_const]
  apply integral_congr_ae
  filter_upwards [pointwise_ae μ p,pointwise_ae μ q] with x hp hq
  rw [hp,hq]
  simp only [inner_smul_left,inner_smul_right,RCLike.inner_apply]
  ring

theorem pure_total : GramExtension.Total (𝕜:=ℂ) (pure (E:=E) μ) := by
  let S := (Submodule.span ℂ (Set.range (pure (E:=E) μ))).topologicalClosure
  apply top_unique
  intro x hx
  change x ∈ S
  refine Completion.induction_on x (Submodule.span ℂ (Set.range (pure (E:=E) μ))).isClosed_topologicalClosure ?_
  intro a
  induction a using TensorProduct.induction_on with
  | zero => simpa only [Completion.coe_zero] using S.zero_mem
  | tmul f e => exact Submodule.le_topologicalClosure _ (Submodule.subset_span ⟨(f,e),rfl⟩)
  | add a b ha hb => simpa only [Completion.coe_add] using S.add_mem ha hb

lemma pointwise_indicator (c : E) {s : Set X} (hs : MeasurableSet s) (hμs : μ s≠∞) :
    pointwise μ (indicatorConstLp 2 hs hμs (1:ℂ),c)=indicatorConstLp 2 hs hμs c := by
  apply Lp.ext
  filter_upwards [pointwise_ae μ (indicatorConstLp 2 hs hμs (1:ℂ),c),
    indicatorConstLp_coeFn (p:=2) (μ:=μ) (hs:=hs) (hμs:=hμs) (c:=(1:ℂ)),
    indicatorConstLp_coeFn (p:=2) (μ:=μ) (hs:=hs) (hμs:=hμs) (c:=c)] with x hp h1 hc
  rw [hp,hc]
  change indicatorConstLp 2 hs hμs (1:ℂ) x • c = _
  rw [h1]
  by_cases hx:x∈s <;> simp [hx]

theorem pointwise_total : GramExtension.Total (𝕜:=ℂ) (pointwise (E:=E) μ) := by
  let S := (Submodule.span ℂ (Set.range (pointwise (E:=E) μ))).topologicalClosure
  apply top_unique
  intro x hx
  change x∈S
  apply Lp.induction (by norm_num : (2:ENNReal)≠∞) (fun f => f∈S) ?_ ?_
      (Submodule.span ℂ (Set.range (pointwise (E:=E) μ))).isClosed_topologicalClosure x
  · intro c s hs hμs
    change indicatorConstLp 2 hs hμs.ne c ∈ S
    rw [← pointwise_indicator μ c hs hμs.ne]
    exact Submodule.le_topologicalClosure _ (Submodule.subset_span ⟨_,rfl⟩)
  · intro f g hf hg hd hSf hSg
    exact S.add_mem hSf hSg

def unitary : Completed (E:=E) μ ≃ₗᵢ[ℂ] Vector (E:=E) μ :=
  GramExtension.equivalence (pure μ) (pointwise μ) (gram μ) (pure_total μ) (pointwise_total μ)

theorem unitary_pure (f : Scalar μ) (e : E) : unitary μ (pure μ (f,e))=pointwise μ (f,e) :=
  GramExtension.equivalence_apply _ _ _ _ _ _

end F1Fecho.TensorL2
#print axioms F1Fecho.TensorL2.gram
#print axioms F1Fecho.TensorL2.pure_total
#print axioms F1Fecho.TensorL2.pointwise_total
#print axioms F1Fecho.TensorL2.unitary_pure
