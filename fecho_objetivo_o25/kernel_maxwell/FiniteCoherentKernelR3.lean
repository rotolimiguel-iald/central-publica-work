import Mathlib.Data.Finsupp.SMul
import Mathlib.Analysis.Complex.Basic
import Mathlib.Tactic

/-! Finite sesquilinear extension of an explicit coherent kernel. No
positivity assumption is added; Hermitian symmetry alone gives a real diagonal. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.CoherentKernel
variable {ι : Type*}

def finiteKernel (M : ι→ι→ℂ) (c d : ι→₀ℂ) : ℂ :=
  c.sum (fun i a=>d.sum (fun j b=>(starRingEnd ℂ) a*b*M i j))

theorem finiteKernel_single (M : ι→ι→ℂ) (i j : ι) (a b : ℂ) :
    finiteKernel M (Finsupp.single i a) (Finsupp.single j b)=(starRingEnd ℂ) a*b*M i j := by
  simp [finiteKernel]

theorem finiteKernel_hermitian (M : ι→ι→ℂ)
    (hM : ∀i j,(starRingEnd ℂ) (M i j)=M j i) (c d : ι→₀ℂ) :
    (starRingEnd ℂ) (finiteKernel M c d)=finiteKernel M d c := by
  unfold finiteKernel Finsupp.sum
  simp only [map_sum,map_mul,starRingEnd_self_apply,hM]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem finiteKernel_diagonal_real (M : ι→ι→ℂ)
    (hM : ∀i j,(starRingEnd ℂ) (M i j)=M j i) (c : ι→₀ℂ) :
    (finiteKernel M c c).im=0 := by
  have h:=congrArg Complex.im (finiteKernel_hermitian M hM c c)
  change -(finiteKernel M c c).im=(finiteKernel M c c).im at h
  linarith

theorem finiteKernel_add_right (M : ι→ι→ℂ) (c d e : ι→₀ℂ) :
    finiteKernel M c (d+e)=finiteKernel M c d+finiteKernel M c e := by
  have hi (i : ι) (a : ℂ) :
      (d+e).sum (fun j b=>(starRingEnd ℂ) a*b*M i j)=
        d.sum (fun j b=>(starRingEnd ℂ) a*b*M i j)+
        e.sum (fun j b=>(starRingEnd ℂ) a*b*M i j) :=
    Finsupp.sum_add_index' (fun _=>by simp) (fun _ _ _=>by ring)
  unfold finiteKernel
  simp_rw [hi]
  exact Finset.sum_add_distrib

theorem finiteKernel_smul_left (M : ι→ι→ℂ) (z : ℂ) (c d : ι→₀ℂ) :
    finiteKernel M (z • c) d=(starRingEnd ℂ) z*finiteKernel M c d := by
  unfold finiteKernel
  rw [Finsupp.sum_smul_index (fun _=>by simp)]
  unfold Finsupp.sum
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro j _
  rw [map_mul]
  ring

theorem finiteKernel_smul_right (M : ι→ι→ℂ) (z : ℂ) (c d : ι→₀ℂ) :
    finiteKernel M c (z • d)=z*finiteKernel M c d := by
  have hi (i : ι) (a : ℂ) :
      (z • d).sum (fun j b=>(starRingEnd ℂ) a*b*M i j)=
        z*d.sum (fun j b=>(starRingEnd ℂ) a*b*M i j) := by
    rw [Finsupp.sum_smul_index (fun _=>by simp)]
    unfold Finsupp.sum
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    ring
  unfold finiteKernel
  simp_rw [hi]
  simp only [Finsupp.sum,Finset.mul_sum]

end F1Fecho.CoherentKernel
#print axioms F1Fecho.CoherentKernel.finiteKernel_single
#print axioms F1Fecho.CoherentKernel.finiteKernel_hermitian
#print axioms F1Fecho.CoherentKernel.finiteKernel_diagonal_real
#print axioms F1Fecho.CoherentKernel.finiteKernel_add_right
#print axioms F1Fecho.CoherentKernel.finiteKernel_smul_left
#print axioms F1Fecho.CoherentKernel.finiteKernel_smul_right
