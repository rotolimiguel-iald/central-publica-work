import Mathlib

/-! Algebraic Maxwell stress conservation from the actual first jet.
This is a reusable identity, not a MaxwellCertificate or an assumed charge.
The later wave consumer must prove antisymmetry, Bianchi and divergence. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellStress
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

def stress (s : ι→ℂ) (F : ι→ι→ℂ) (μ ν : ι) : ℂ :=
  -(∑ α,s α*F μ α*F ν α)+(1/4:ℂ)*(if μ=ν then s μ else 0)*
    (∑ α,∑ β,s α*s β*F α β*F α β)

def stressJet (s : ι→ℂ) (F : ι→ι→ℂ) (dF : ι→ι→ι→ℂ) (ρ μ ν : ι) : ℂ :=
  -(∑ α,s α*(dF ρ μ α*F ν α+F μ α*dF ρ ν α))+
    (1/2:ℂ)*(if μ=ν then s μ else 0)*(∑ α,∑ β,s α*s β*F α β*dF ρ α β)

theorem bianchi_contraction (s : ι→ℂ) (F : ι→ι→ℂ) (dF : ι→ι→ι→ℂ)
    (ha : ∀ μ ν,F ν μ= -F μ ν)
    (hd : ∀ ρ μ ν,dF ρ ν μ= -dF ρ μ ν)
    (hb : ∀ ρ μ ν,dF ρ μ ν+dF μ ν ρ+dF ν ρ μ=0) (ν : ι) :
    (2:ℂ)*(∑ μ,∑ α,s μ*s α*F μ α*dF μ ν α)=
      ∑ μ,∑ α,s μ*s α*F μ α*dF ν μ α := by
  have he (μ α : ι) : dF μ ν α=dF ν μ α+dF α ν μ := by
    have h:=hb μ ν α
    rw [hd ν μ α,hd α ν μ] at h
    linear_combination h
  have hswap : (∑ μ,∑ α,s μ*s α*F μ α*dF α ν μ)=
      -(∑ μ,∑ α,s μ*s α*F μ α*dF μ ν α) := by
    rw [Finset.sum_comm]
    simp only [← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro μ _
    apply Finset.sum_congr rfl
    intro α _
    rw [ha α μ]
    ring
  have hsum : (∑ μ,∑ α,s μ*s α*F μ α*dF μ ν α)=
      (∑ μ,∑ α,s μ*s α*F μ α*dF ν μ α)+
      (∑ μ,∑ α,s μ*s α*F μ α*dF α ν μ) := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro μ _
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro α _
    rw [he μ α]
    ring
  rw [hswap] at hsum
  linear_combination hsum

theorem stressJet_conserved (s : ι→ℂ) (hs : ∀ μ,s μ*s μ=1)
    (F : ι→ι→ℂ) (dF : ι→ι→ι→ℂ)
    (ha : ∀ μ ν,F ν μ= -F μ ν)
    (hd : ∀ ρ μ ν,dF ρ ν μ= -dF ρ μ ν)
    (hb : ∀ ρ μ ν,dF ρ μ ν+dF μ ν ρ+dF ν ρ μ=0)
    (hdiv : ∀ ν,∑ μ,s μ*dF μ μ ν=0) (ν : ι) :
    (∑ μ,s μ*stressJet s F dF μ μ ν)=0 := by
  have hz : (∑ μ,∑ α,s μ*s α*dF μ μ α*F ν α)=0 := by
    rw [Finset.sum_comm]
    calc
      _ = ∑ α,(s α*F ν α)*(∑ μ,s μ*dF μ μ α) := by
        simp only [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro α _
        apply Finset.sum_congr rfl
        intro μ _
        ring
      _ = 0 := by simp only [hdiv,mul_zero,Finset.sum_const_zero]
  have hm : (∑ μ,s μ*stressJet s F dF μ μ ν)=
      -(∑ μ,∑ α,s μ*s α*dF μ μ α*F ν α)-
      (∑ μ,∑ α,s μ*s α*F μ α*dF μ ν α)+
      (1/2:ℂ)*(∑ α,∑ β,s α*s β*F α β*dF ν α β) := by
    have hδ : (∑ μ,s μ*((1/2:ℂ)*(if μ=ν then s μ else 0)*
        (∑ α,∑ β,s α*s β*F α β*dF μ α β)))=
        (1/2:ℂ)*(∑ α,∑ β,s α*s β*F α β*dF ν α β) := by
      simp only [mul_ite,mul_zero,ite_mul,zero_mul,Finset.sum_ite_eq',
        Finset.mem_univ,ite_true]
      calc
        _ = (1/2:ℂ)*(s ν*s ν)*(∑ α,∑ β,s α*s β*F α β*dF ν α β) := by ring
        _ = _ := by rw [hs];ring
    have hprod (μ : ι) : s μ*(∑ α,s α*(dF μ μ α*F ν α+F μ α*dF μ ν α))=
        (∑ α,s μ*s α*dF μ μ α*F ν α)+(∑ α,s μ*s α*F μ α*dF μ ν α) := by
      rw [Finset.mul_sum,← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro α _
      ring
    simp only [stressJet,mul_add,mul_neg,Finset.sum_add_distrib]
    simp_rw [hprod]
    rw [Finset.sum_neg_distrib,Finset.sum_add_distrib,hδ]
    ring
  rw [hm,hz]
  have hh:=bianchi_contraction s F dF ha hd hb ν
  linear_combination -(1/2:ℂ)*hh

end F1Fecho.MaxwellStress
#print axioms F1Fecho.MaxwellStress.bianchi_contraction
#print axioms F1Fecho.MaxwellStress.stressJet_conserved
