import FiniteCoherentKernelR3
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul

/-! Derivatives of the finite coherent extension, with only finite sums.
No limit over the Fock domain or distributional diagonal is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.CoherentKernel
variable {ι : Type*}

theorem finiteKernel_add_left_of_hermitian (M : ι→ι→ℂ)
    (hM : ∀i j,(starRingEnd ℂ) (M i j)=M j i) (c d e : ι→₀ℂ) :
    finiteKernel M (c+d) e=finiteKernel M c e+finiteKernel M d e := by
  apply (starRingEnd ℂ).injective
  rw [map_add,finiteKernel_hermitian M hM,finiteKernel_hermitian M hM,
    finiteKernel_hermitian M hM,finiteKernel_add_right]

theorem finiteKernel_hasDerivAt (M : ι→ι→ℝ→ℂ) (D : ι→ι→ℂ)
    (c d : ι→₀ℂ) (x : ℝ) (hM : ∀i j,HasDerivAt (M i j) (D i j) x) :
    HasDerivAt (fun t=>finiteKernel (fun i j=>M i j t) c d)
      (finiteKernel D c d) x := by
  have ht:=HasDerivAt.sum (u:=c.support) (fun i _=>
    HasDerivAt.sum (u:=d.support) (fun j _=>(hM i j).const_mul ((starRingEnd ℂ) (c i)*d j)))
  simpa only [finiteKernel,Finsupp.sum] using ht

theorem finiteKernel_weighted_sum {κ : Type*} [Fintype κ]
    (M : κ→ι→ι→ℂ) (s : κ→ℂ) (c d : ι→₀ℂ) :
    (∑μ,s μ*finiteKernel (M μ) c d)=finiteKernel (fun i j=>∑μ,s μ*M μ i j) c d := by
  unfold finiteKernel Finsupp.sum
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro μ _
  ring

theorem finiteKernel_zero (c d : ι→₀ℂ) : finiteKernel (fun _ _=>0) c d=0 := by
  simp [finiteKernel]

end F1Fecho.CoherentKernel
#print axioms F1Fecho.CoherentKernel.finiteKernel_add_left_of_hermitian
#print axioms F1Fecho.CoherentKernel.finiteKernel_hasDerivAt
#print axioms F1Fecho.CoherentKernel.finiteKernel_weighted_sum
#print axioms F1Fecho.CoherentKernel.finiteKernel_zero
