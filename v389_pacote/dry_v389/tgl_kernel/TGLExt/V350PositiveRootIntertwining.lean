import TGLExt.V350ResolventGraphTransport
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Continuity

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open Filter
open scoped Topology ContinuousFunctionalCalculus
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Continuous functional calculus transports an intertwiner between two
different self-adjoint operators, using their common compact spectral union. -/
theorem real_cfc_intertwines (A B U : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (h : A*U=U*B)
    (f : ℝ → ℝ) (hf : Continuous f) : cfc f A * U = U * cfc f B := by
  let s : Set ℝ := spectrum ℝ A ∪ spectrum ℝ B
  have hs : IsCompact s := (spectrum.isCompact A).union (spectrum.isCompact B)
  haveI : CompactSpace s := isCompact_iff_compactSpace.mp hs
  have ha : spectrum ℝ A ⊆ s := Set.subset_union_left
  have hb : spectrum ℝ B ⊆ s := Set.subset_union_right
  have he (g : C(s,ℝ)) : cfcHomSuperset hA ha g * U = U * cfcHomSuperset hB hb g := by
    induction g using ContinuousMap.induction_on_of_compact with
    | const r =>
      change cfcHomSuperset hA ha (algebraMap ℝ C(s,ℝ) r) * U =
        U * cfcHomSuperset hB hb (algebraMap ℝ C(s,ℝ) r)
      rw [AlgHomClass.commutes,AlgHomClass.commutes]
      exact Algebra.commutes r U
    | id => simpa only [cfcHomSuperset_id] using h
    | star_id =>
      simpa only [map_star,cfcHomSuperset_id,hA.star_eq,hB.star_eq] using h
    | add g k hg hk => simp only [map_add,add_mul,mul_add,hg,hk]
    | mul g k hg hk =>
      simp only [map_mul]
      calc
        _ = cfcHomSuperset hA ha g * (cfcHomSuperset hA ha k * U) := mul_assoc _ _ _
        _ = cfcHomSuperset hA ha g * (U * cfcHomSuperset hB hb k) := by rw [hk]
        _ = (cfcHomSuperset hA ha g * U) * cfcHomSuperset hB hb k := (mul_assoc _ _ _).symm
        _ = _ := by rw [hg,mul_assoc]
    | frequently g hg =>
      exact (isClosed_eq ((cfcHomSuperset_continuous hA ha).mul continuous_const)
        (continuous_const.mul (cfcHomSuperset_continuous hB hb))).mem_of_frequently_of_tendsto
          hg tendsto_id
  have hh := he ⟨fun x : s => f x,hf.comp continuous_subtype_val⟩
  rw [cfcHomSuperset_apply,cfcHomSuperset_apply] at hh
  rw [cfc_apply f A hA hf.continuousOn,cfc_apply f B hB hf.continuousOn]
  convert hh using 2 <;> congr 1

theorem positive_sqrt_intertwines (A B U : H →L[ℂ] H)
    (hA : 0 ≤ A) (hB : 0 ≤ B) (h : A*U=U*B) :
    CFC.sqrt A * U = U * CFC.sqrt B := by
  rw [CFC.sqrt_eq_real_sqrt A hA,CFC.sqrt_eq_real_sqrt B hB,
    cfcₙ_eq_cfc,cfcₙ_eq_cfc]
  exact real_cfc_intertwines A B U (IsSelfAdjoint.of_nonneg hA)
    (IsSelfAdjoint.of_nonneg hB) h Real.sqrt Real.continuous_sqrt

theorem positive_square_intertwines_roots (A B U : H →L[ℂ] H)
    (hA : 0 ≤ A) (hB : 0 ≤ B) (h : (A*A)*U=U*(B*B)) : A*U=U*B := by
  have hh := positive_sqrt_intertwines (A*A) (B*B) U
    (Commute.mul_nonneg hA hA (Commute.refl A))
    (Commute.mul_nonneg hB hB (Commute.refl B)) h
  simpa only [CFC.sqrt_mul_self A hA,CFC.sqrt_mul_self B hB] using hh

#print axioms real_cfc_intertwines
#print axioms positive_sqrt_intertwines
#print axioms positive_square_intertwines_roots
end
end TGLV350.Regular
