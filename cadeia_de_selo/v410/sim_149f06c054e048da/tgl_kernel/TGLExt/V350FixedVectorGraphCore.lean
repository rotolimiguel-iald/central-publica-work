import TGLExt.ClosedAntilinearStandardSubspace
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open ClosedSubmodule ChatgptAudit.Continuous049
noncomputable section

theorem realSubmodule_closure_of_positive_detection
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (E K : Submodule ℝ H) (hle : E ≤ K) (hK : IsClosed (K : Set H))
    (hdetect : ∀ x : H, x ∈ K → x ≠ 0 → ∃ v : H, v ∈ E ∧ 0 < inner ℝ x v) :
    E.topologicalClosure = K := by
  have hcl : E.topologicalClosure ≤ K := closure_minimal hle hK
  apply le_antisymm hcl
  intro x hx
  let L := E.topologicalClosure
  letI : CompleteSpace L := (show IsClosed (L : Set H) from isClosed_closure).completeSpace_coe
  have hzK : x - L.starProjection x ∈ K :=
    K.sub_mem hx (hcl (Submodule.starProjection_apply_mem L x))
  have hz : x - L.starProjection x = 0 := by
    by_contra hn
    obtain ⟨v,hv,hpos⟩ := hdetect _ hzK hn
    have ho := Submodule.sub_starProjection_mem_orthogonal (K := L) x
    have he : inner ℝ v (x-L.starProjection x) = 0 := ho v (E.le_topologicalClosure hv)
    have hs : inner ℝ (x-L.starProjection x) v = inner ℝ v (x-L.starProjection x) :=
      real_inner_comm _ _
    rw [hs,he] at hpos
    exact lt_irrefl _ hpos
  exact (congrArg (fun v : H => v ∈ L) (sub_eq_zero.mp hz)).mpr
    (Submodule.starProjection_apply_mem L x)

variable {H A : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [AddCommGroup A] [Module ℂ A] [StarAddMonoid A] [StarModule ℂ A]

def selfadjointVectorSubmodule (j : A →ₗ[ℂ] H) : Submodule ℝ H where
  carrier := {x | ∃ a : A, star a = a ∧ j a = x}
  zero_mem' := ⟨0,star_zero _,map_zero j⟩
  add_mem' := by
    rintro x y ⟨a,ha,rfl⟩ ⟨b,hb,rfl⟩
    exact ⟨a+b,by rw [star_add,ha,hb],map_add j a b⟩
  smul_mem' := by
    rintro c x ⟨a,ha,rfl⟩
    refine ⟨(c : ℂ) • a,?_,?_⟩
    · rw [star_smul,ha]
      simp
    · exact map_smul j (c : ℂ) a

theorem selfadjointVectorSubmodule_mem (j : A →ₗ[ℂ] H) (a : A) (ha : star a = a) :
    j a ∈ selfadjointVectorSubmodule j := ⟨a,ha,rfl⟩

theorem selfadjointVectorSubmodule_le_fixed (j : A →ₗ[ℂ] H)
    (D : Submodule ℂ H) (F : D →ₛₗ[starRingEnd ℂ] H)
    (hF : ∀ a : A, ∃ hv : j a ∈ D, F ⟨j a,hv⟩ = j (star a)) :
    selfadjointVectorSubmodule j ≤ fixedRealSubmodule D F := by
  rintro x ⟨a,ha,rfl⟩
  obtain ⟨hv,hv'⟩ := hF a
  exact ⟨hv,hv'.trans (congrArg j ha)⟩

theorem selfadjointVectorSubmodule_closure (j : A →ₗ[ℂ] H)
    (D : Submodule ℂ H) (F : D →ₛₗ[starRingEnd ℂ] H)
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H),F x))))
    (hF : ∀ a : A, ∃ hv : j a ∈ D, F ⟨j a,hv⟩ = j (star a))
    (hdetect : ∀ η : D, F η = (η : H) → (η : H) ≠ 0 →
      ∃ a : A, star a = a ∧ 0 < (inner ℂ (η : H) (j a)).re) :
    (selfadjointVectorSubmodule j).topologicalClosure = fixedRealSubmodule D F := by
  apply realSubmodule_closure_of_positive_detection _ _
    (selfadjointVectorSubmodule_le_fixed j D F hF) (fixedRealSubmodule_closed D F hclosed)
  rintro x ⟨hx,hFx⟩ hne
  obtain ⟨a,ha,hpos⟩ := hdetect ⟨x,hx⟩ hFx hne
  exact ⟨j a,selfadjointVectorSubmodule_mem j a ha,hpos⟩

def conjugateGraphMix (x : H × H) : H × H :=
  (x.1 + Complex.I • x.2,x.1 - Complex.I • x.2)

theorem conjugateGraphMix_continuous : Continuous (conjugateGraphMix (H := H)) :=
  (continuous_fst.add (continuous_snd.const_smul Complex.I)).prodMk
    (continuous_fst.sub (continuous_snd.const_smul Complex.I))

theorem conjugateGraphMix_selfadjoint (j : A →ₗ[ℂ] H) (a b : A)
    (ha : star a = a) (hb : star b = b) :
    conjugateGraphMix (j a,j b) = (j (a + Complex.I • b),j (star (a + Complex.I • b))) := by
  unfold conjugateGraphMix
  rw [star_add,star_smul,ha,hb]
  simp only [map_add,map_smul,map_neg,Complex.star_def,Complex.conj_I,neg_smul]
  exact Prod.ext rfl (sub_eq_add_neg _ _)

/-- Norm density in the real fixed space upgrades to graph density for the
original closed antilinear involution. No continuity of F is assumed. -/
theorem conjugateGraph_closure_eq_original (j : A →ₗ[ℂ] H)
    (D : Submodule ℂ H) (F : D →ₛₗ[starRingEnd ℂ] H)
    (hclosed : IsClosed (Set.range (fun x : D => ((x : H),F x))))
    (hF : ∀ a : A, ∃ hv : j a ∈ D, F ⟨j a,hv⟩ = j (star a))
    (hmaps : ∀ x : D, F x ∈ D)
    (hinv : ∀ x : D, F ⟨F x,hmaps x⟩ = (x : H))
    (hdense : (selfadjointVectorSubmodule j).topologicalClosure = fixedRealSubmodule D F) :
    closure (Set.range (fun a : A => (j a,j (star a)))) =
      Set.range (fun x : D => ((x : H),F x)) := by
  apply Set.Subset.antisymm
  · apply closure_minimal ?_ hclosed
    rintro p ⟨a,rfl⟩
    obtain ⟨ha,ha'⟩ := hF a
    exact ⟨⟨j a,ha⟩,Prod.ext rfl ha'⟩
  · rintro p ⟨x,rfl⟩
    obtain ⟨h,k,hh,hk,hx,hFx⟩ := domain_fixed_decomposition D F hmaps hinv x
    let E := selfadjointVectorSubmodule j
    have hh' : h ∈ closure (E : Set H) := by
      change h ∈ E.topologicalClosure
      rw [hdense]
      exact hh
    have hk' : k ∈ closure (E : Set H) := by
      change k ∈ E.topologicalClosure
      rw [hdense]
      exact hk
    have hprod : (h,k) ∈ closure ((E : Set H) ×ˢ (E : Set H)) := by
      rw [closure_prod_eq]
      exact ⟨hh',hk'⟩
    have hsub : ((E : Set H) ×ˢ (E : Set H)) ⊆
        conjugateGraphMix ⁻¹' closure (Set.range (fun a : A => (j a,j (star a)))) := by
      rintro ⟨v,w⟩ ⟨⟨a,ha,rfl⟩,⟨b,hb,rfl⟩⟩
      exact subset_closure ⟨a+Complex.I • b,(conjugateGraphMix_selfadjoint j a b ha hb).symm⟩
    have hpre := closure_minimal hsub
      (isClosed_closure.preimage (conjugateGraphMix_continuous (H := H))) hprod
    change (h+Complex.I • k,h-Complex.I • k) ∈
      closure (Set.range (fun a : A => (j a,j (star a)))) at hpre
    exact (congrArg (fun z : H × H =>
      z ∈ closure (Set.range (fun a : A => (j a,j (star a))))) (Prod.ext hx hFx)).mpr hpre

#print axioms realSubmodule_closure_of_positive_detection
#print axioms selfadjointVectorSubmodule
#print axioms selfadjointVectorSubmodule_mem
#print axioms selfadjointVectorSubmodule_le_fixed
#print axioms selfadjointVectorSubmodule_closure
#print axioms conjugateGraphMix
#print axioms conjugateGraphMix_continuous
#print axioms conjugateGraphMix_selfadjoint
#print axioms conjugateGraph_closure_eq_original
end
end TGLV350.Regular
