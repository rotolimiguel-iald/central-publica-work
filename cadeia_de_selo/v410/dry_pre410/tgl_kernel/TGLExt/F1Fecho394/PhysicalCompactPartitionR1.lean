import TGLExt.F1Fecho394.CompactSchwartzPartitionR3
import TGLExt.F1Fecho394.RealSchwartzTestsR1

/-! The finite smooth decomposition preserves the actual real Maxwell test
condition. No causal commutation or domain equality is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Function
variable {ι : Type} [Fintype ι]

theorem real_compact_partition (f : SchwartzTensor) (hr : IsRealTest f)
    (hf : HasCompactSupport (f : Spacetime → TensorValue))
    (U : ι → Set Spacetime) (ho : ∀ i, IsOpen (U i))
    (hcover : tsupport (f : Spacetime → TensorValue) ⊆ ⋃ i, U i) :
    ∃ parts : ι → SchwartzTensor, (∑ i, parts i) = f ∧
      ∀ i, IsRealTest (parts i) ∧ HasCompactSupport (parts i : Spacetime → TensorValue) ∧
        support (parts i : Spacetime → TensorValue) ⊆ U i ∩ support (f : Spacetime → TensorValue) := by
  obtain ⟨parts,hsum,hparts⟩ := F1Fecho.CompactSchwartzPartition.finite_partition f hf U ho hcover
  refine ⟨parts,hsum,?_⟩
  intro i
  refine ⟨?_,(hparts i).1,(hparts i).2.1⟩
  intro x μ ν
  obtain ⟨r,he⟩ := (hparts i).2.2 x
  rw [he]
  simp only [Pi.smul_apply,Complex.smul_im,hr x μ ν,smul_zero]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.real_compact_partition
