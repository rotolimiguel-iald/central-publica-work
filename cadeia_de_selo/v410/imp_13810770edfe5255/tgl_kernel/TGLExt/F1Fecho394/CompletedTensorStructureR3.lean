import TGLExt.F1Fecho394.GramTotalExtensionR4
import TGLExt.F1Fecho394.BosonicTwoParticle
/-! Completion, associativity and factor transport on the existing Hilbert tensor norm.
All maps are defined from Gram-preserving dense algebraic families. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open UniformSpace
open scoped TensorProduct
namespace F1Fecho.CompletedTensor
open F1Rede.BosonicTwoParticle
variable {E F G E' F' : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
  [NormedAddCommGroup G] [InnerProductSpace ℂ G]
  [NormedAddCommGroup E'] [InnerProductSpace ℂ E']
  [NormedAddCommGroup F'] [InnerProductSpace ℂ F']
abbrev CT (E F : Type*) [NormedAddCommGroup E] [InnerProductSpace ℂ E]
    [NormedAddCommGroup F] [InnerProductSpace ℂ F] := Completion (E⊗[ℂ]F)
def pure (p : E×F) : CT E F := (p.1⊗ₜ[ℂ]p.2 : E⊗[ℂ]F)

def bilinear : E→L[ℂ]F→L[ℂ](E⊗[ℂ]F) :=
  (TensorProduct.mk ℂ E F).mkContinuous₂ 1 (by
    intro x y
    simp only [TensorProduct.mk_apply,TensorProduct.norm_tmul,one_mul,le_refl])

theorem pure_total : GramExtension.Total (𝕜:=ℂ) (pure (E:=E) (F:=F)) := by
  let S := (Submodule.span ℂ (Set.range (pure (E:=E) (F:=F)))).topologicalClosure
  apply top_unique
  intro x hx
  change x∈S
  refine Completion.induction_on x
    (Submodule.span ℂ (Set.range (pure (E:=E) (F:=F)))).isClosed_topologicalClosure ?_
  intro a
  induction a using TensorProduct.induction_on with
  | zero => simpa only [Completion.coe_zero] using S.zero_mem
  | tmul x y => exact Submodule.le_topologicalClosure _ (Submodule.subset_span ⟨(x,y),rfl⟩)
  | add a b ha hb => simpa only [Completion.coe_add] using S.add_mem ha hb

def leftDense (p : E×F) : CT (Completion E) F := pure ((p.1:Completion E),p.2)

theorem leftDense_total : GramExtension.Total (𝕜:=ℂ) (leftDense (E:=E) (F:=F)) := by
  let S := (Submodule.span ℂ (Set.range (leftDense (E:=E) (F:=F)))).topologicalClosure
  have hS : IsClosed (S:Set (CT (Completion E) F)) :=
    (Submodule.span ℂ (Set.range (leftDense (E:=E) (F:=F)))).isClosed_topologicalClosure
  apply top_unique
  intro z hz
  change z∈S
  refine Completion.induction_on z hS ?_
  intro a
  induction a using TensorProduct.induction_on with
  | zero => simpa only [Completion.coe_zero] using S.zero_mem
  | tmul x y =>
    have hc : Continuous (fun v : Completion E => (v⊗ₜ[ℂ]y : CT (Completion E) F)) :=
      (Completion.continuous_coe _).comp ((bilinear (E:=Completion E) (F:=F)).flip y).continuous
    refine Completion.induction_on x (hS.preimage hc) ?_
    intro v
    exact Submodule.le_topologicalClosure _ (Submodule.subset_span ⟨(v,y),rfl⟩)
  | add a b ha hb => simpa only [Completion.coe_add] using S.add_mem ha hb

theorem left_gram : GramExtension.GramEqual (𝕜:=ℂ)
    (leftDense (E:=E) (F:=F)) pure := by
  intro p q
  simp only [leftDense,pure,Completion.inner_coe,TensorProduct.inner_tmul]

def collapseLeft : CT (Completion E) F ≃ₗᵢ[ℂ] CT E F :=
  GramExtension.equivalence leftDense pure left_gram leftDense_total pure_total

theorem collapseLeft_pure (x:E) (y:F) :
    collapseLeft (pure ((x:Completion E),y))=pure (x,y) :=
  GramExtension.equivalence_apply _ _ _ _ _ (x,y)

def congr (u:E≃ₗᵢ[ℂ]E') (v:F≃ₗᵢ[ℂ]F') : CT E F≃ₗᵢ[ℂ]CT E' F' :=
  completionEquiv (TensorProduct.congrIsometry u v)
def comm : CT E F≃ₗᵢ[ℂ]CT F E := completionEquiv (TensorProduct.commIsometry ℂ E F)
def assoc : CT (E⊗[ℂ]F) G≃ₗᵢ[ℂ]CT E (F⊗[ℂ]G) :=
  completionEquiv (TensorProduct.assocIsometry ℂ E F G)

theorem congr_pure (u:E≃ₗᵢ[ℂ]E') (v:F≃ₗᵢ[ℂ]F') (x:E) (y:F) :
    congr u v (pure (x,y))=pure (u x,v y) := by
  simp [congr,pure]
theorem comm_pure (x:E) (y:F) : comm (pure (x,y))=pure (y,x) := by
  simp [comm,pure]
theorem assoc_pure (x:E) (y:F) (z:G) : assoc (pure (x⊗ₜ[ℂ]y,z))=pure (x,y⊗ₜ[ℂ]z) := by
  simp [assoc,pure]

def completeRight : CT E F≃ₗᵢ[ℂ]CT E (Completion F) :=
  (comm (E:=E) (F:=F)).trans ((collapseLeft (E:=F) (F:=E)).symm.trans comm)

theorem completeRight_pure (x:E) (y:F) :
    completeRight (pure (x,y))=pure (x,(y:Completion F)) := by
  change comm ((collapseLeft (E:=F) (F:=E)).symm (comm (pure (x,y))))=_
  rw [comm_pure,← collapseLeft_pure y x,LinearIsometryEquiv.symm_apply_apply,comm_pure]
end F1Fecho.CompletedTensor
#print axioms F1Fecho.CompletedTensor.pure_total
#print axioms F1Fecho.CompletedTensor.leftDense_total
#print axioms F1Fecho.CompletedTensor.collapseLeft_pure
#print axioms F1Fecho.CompletedTensor.completeRight_pure
