import MaxwellStressJetAlgebraR3

/-! The polynomial stressJet is the genuine derivative of stress.
This removes a formal differentiation assumption before applying the
algebraic conservation identity to the constructed wave. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellStress
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem stress_hasDerivAt (s : ι→ℂ) (F : ℝ→ι→ι→ℂ) (dF : ι→ι→ℂ)
    (t : ℝ) (hf : ∀μ ν,HasDerivAt (fun u=>F u μ ν) (dF μ ν) t) (μ ν : ι) :
    HasDerivAt (fun u=>stress s (F u) μ ν)
      (-(∑ α,s α*(dF μ α*F t ν α+F t μ α*dF ν α))+
        (1/2:ℂ)*(if μ=ν then s μ else 0)*(∑ α,∑ β,s α*s β*F t α β*dF α β)) t := by
  have hfirst := HasDerivAt.fun_sum (u:=Finset.univ) (fun α _=>
    ((hf μ α).mul (hf ν α)).const_mul (s α))
  have hsq (α β : ι) : HasDerivAt (fun u=>s α*s β*F u α β*F u α β)
      (2*(s α*s β*F t α β*dF α β)) t := by
    have hr:=((hf α β).mul (hf α β)).const_mul (s α*s β)
    have he : (s α*s β)*(dF α β*F t α β+F t α β*dF α β)=
        2*(s α*s β*F t α β*dF α β) := by ring
    rw [he] at hr
    simpa only [Pi.mul_apply,mul_assoc] using hr
  have hsecond := HasDerivAt.fun_sum (u:=Finset.univ) (fun α _=>
    HasDerivAt.fun_sum (u:=Finset.univ) (fun β _=>hsq α β))
  have hout := hfirst.neg.add (hsecond.const_mul ((1/4:ℂ)*(if μ=ν then s μ else 0)))
  have htrace : ((1/4:ℂ)*(if μ=ν then s μ else 0))*
      (∑ α,∑ β,2*(s α*s β*F t α β*dF α β))=
      ((1/2:ℂ)*(if μ=ν then s μ else 0))*(∑ α,∑ β,s α*s β*F t α β*dF α β) := by
    simp only [← Finset.mul_sum]
    ring
  rw [htrace] at hout
  simpa only [stress,Pi.add_apply,Pi.neg_apply,Pi.mul_apply,mul_assoc] using hout

theorem stress_symmetric (s : ι→ℂ) (F : ι→ι→ℂ) (μ ν : ι) :
    stress s F μ ν=stress s F ν μ := by
  unfold stress
  have hc : (∑ α,s α*F μ α*F ν α)=(∑ α,s α*F ν α*F μ α) := by
    apply Finset.sum_congr rfl
    intro α _
    ring
  rw [hc]
  by_cases h : μ=ν
  · subst ν
    rfl
  · simp only [h,Ne.symm h,ite_false]

end F1Fecho.MaxwellStress
#print axioms F1Fecho.MaxwellStress.stress_hasDerivAt
#print axioms F1Fecho.MaxwellStress.stress_symmetric
