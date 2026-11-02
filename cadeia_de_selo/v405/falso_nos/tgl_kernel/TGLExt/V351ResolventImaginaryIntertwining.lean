import TGLExt.V351ResolventImaginaryPowers
import TGLExt.V350PositiveRootIntertwining

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Complex continuous functions of two selfadjoint operators transport a bounded intertwiner. -/
theorem complex_cfc_selfadjoint_intertwines (A B R : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (h : A*R=R*B)
    (f : ℂ → ℂ) (hf : Continuous f) : cfc f A * R = R * cfc f B := by
  let s : Set ℂ := spectrum ℂ A ∪ spectrum ℂ B
  have hs : IsCompact s := (spectrum.isCompact A).union (spectrum.isCompact B)
  haveI : CompactSpace s := isCompact_iff_compactSpace.mp hs
  have ha : spectrum ℂ A ⊆ s := Set.subset_union_left
  have hb : spectrum ℂ B ⊆ s := Set.subset_union_right
  have he (g : C(s,ℂ)) :
      cfcHomSuperset hA.isStarNormal ha g * R = R * cfcHomSuperset hB.isStarNormal hb g := by
    induction g using ContinuousMap.induction_on_of_compact with
    | const r =>
      change cfcHomSuperset hA.isStarNormal ha (algebraMap ℂ C(s,ℂ) r) * R =
        R * cfcHomSuperset hB.isStarNormal hb (algebraMap ℂ C(s,ℂ) r)
      rw [AlgHomClass.commutes,AlgHomClass.commutes]
      exact Algebra.commutes r R
    | id => simpa only [cfcHomSuperset_id] using h
    | star_id =>
      simpa only [map_star,cfcHomSuperset_id,hA.star_eq,hB.star_eq] using h
    | add g k hg hk => simp only [map_add,add_mul,mul_add,hg,hk]
    | mul g k hg hk =>
      simp only [map_mul]
      calc
        _ = cfcHomSuperset hA.isStarNormal ha g * (cfcHomSuperset hA.isStarNormal ha k * R) := mul_assoc _ _ _
        _ = cfcHomSuperset hA.isStarNormal ha g * (R * cfcHomSuperset hB.isStarNormal hb k) := by rw [hk]
        _ = (cfcHomSuperset hA.isStarNormal ha g * R) * cfcHomSuperset hB.isStarNormal hb k := (mul_assoc _ _ _).symm
        _ = _ := by rw [hg,mul_assoc]
    | frequently g hg =>
      exact (isClosed_eq ((cfcHomSuperset_continuous hA.isStarNormal ha).mul continuous_const)
        (continuous_const.mul (cfcHomSuperset_continuous hB.isStarNormal hb))).mem_of_frequently_of_tendsto
          hg tendsto_id
  have hh := he ⟨fun x : s => f x,hf.comp continuous_subtype_val⟩
  rw [cfcHomSuperset_apply,cfcHomSuperset_apply] at hh
  rw [cfc_apply f A hA.isStarNormal hf.continuousOn,cfc_apply f B hB.isStarNormal hf.continuousOn]
  convert hh using 2 <;> congr 1

theorem resolventDampingOperator_intertwines (T Q R : H →L[ℂ] H)
    (h : T*R=R*Q) : resolventDampingOperator T * R = R * resolventDampingOperator Q := by
  unfold resolventDampingOperator
  simp only [mul_sub,sub_mul,mul_one,mul_assoc,h]
  rw [← mul_assoc T R Q,h,mul_assoc]

theorem resolventPhaseOperator_intertwines (T Q R : H →L[ℂ] H)
    (hT : IsSelfAdjoint T) (hQ : IsSelfAdjoint Q) (h : T*R=R*Q) (t : ℝ) :
    resolventPhaseOperator T t * R = R * resolventPhaseOperator Q t :=
  complex_cfc_selfadjoint_intertwines T Q R hT hQ h
    (fun z : ℂ => resolventPhaseFunction t z.re)
    ((resolventPhaseFunction_continuous t).comp Complex.continuous_re)

theorem resolventImaginaryPower_intertwines (T Q R : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1T : T ≤ 1) (hiT : Function.Injective T)
    (hjT : Function.Injective (1-T : H →L[ℂ] H))
    (hQ : 0 ≤ Q) (h1Q : Q ≤ 1) (hiQ : Function.Injective Q)
    (hjQ : Function.Injective (1-Q : H →L[ℂ] H)) (h : T*R=R*Q)
    (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1T hiT hjT t (R x) =
      R (resolventImaginaryPower Q hQ h1Q hiQ hjQ t x) := by
  refine (resolventDampingOperator_denseRange Q hQ h1Q hiQ hjQ).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  have hb := congrArg (fun A : H →L[ℂ] H => A y) (resolventDampingOperator_intertwines T Q R h)
  change resolventDampingOperator T (R y)=R (resolventDampingOperator Q y) at hb
  rw [← hb,resolventImaginaryPower_damping,resolventImaginaryPower_damping]
  exact congrArg (fun A : H →L[ℂ] H => A y)
    (resolventPhaseOperator_intertwines T Q R (IsSelfAdjoint.of_nonneg hT)
      (IsSelfAdjoint.of_nonneg hQ) h t)

#print axioms complex_cfc_selfadjoint_intertwines
#print axioms resolventDampingOperator_intertwines
#print axioms resolventPhaseOperator_intertwines
#print axioms resolventImaginaryPower_intertwines
end
end TGLV350.Regular
