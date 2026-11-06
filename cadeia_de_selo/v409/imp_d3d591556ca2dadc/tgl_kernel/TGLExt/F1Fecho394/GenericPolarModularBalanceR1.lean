import TGLExt.F1Fecho394.GeneralDampedPhaseBalanceR1
import TGLExt.V351ModularCutBalance
/-! The analytic balance needed by the cut trace, with every modular premise
explicit. Its concrete consumer must supply the actual J, resolvent, left and
right groups, and the full modular implementation; no trace is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.PolarModularBalance
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem balance (T A : H →L[ℂ] H) (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (hT0 : 0≤T) (hT1 : T≤1) (hiT : Function.Injective T)
    (hjT : Function.Injective (1-T : H →L[ℂ] H))
    (hA0 : 0≤A) (hA1 : A≤1) (hiA : Function.Injective A)
    (hjA : Function.Injective (1-A : H →L[ℂ] H))
    (L R : ℝ → H →L[ℂ] H)
    (hTA : Commute T A)
    (hflip : antiunitaryConjugate J T=1-T)
    (hAB : Commute A (antiunitaryConjugate J A))
    (hleft : ∀ t, L t * resolventDampingOperator A = resolventPhaseOperator A t)
    (hJleft : ∀ t, antiunitaryConjugate J (L t)=R (-t))
    (hRcomm : ∀ t, Commute (R t) A)
    (hmod : ∀ t x, resolventImaginaryPower T hT0 hT1 hiT hjT t x=L t (R (-t) x)) :
    let B := antiunitaryConjugate J A
    Commute T B ∧ Function.Injective B ∧
      (1-T)*A*(1-B)=T*(1-A)*B := by
  let B := antiunitaryConjugate J A
  change Commute T B ∧ Function.Injective B ∧ (1-T)*A*(1-B)=T*(1-A)*B
  have hcomp : antiunitaryConjugate J (1-A)=1-B := by
    change (antiunitaryConjugateRealHom J) (1-A)=1-B
    simp only [map_sub,map_one]
    rfl
  have hB0 : 0≤B := antiunitaryConjugate_nonneg J A hA0
  have hB1 : B≤1 := by
    apply operator_le_of_sub_nonneg B 1
    rw [← hcomp]
    exact antiunitaryConjugate_nonneg J (1-A) (hilbertComplement_nonneg A hA1)
  have hiB : Function.Injective B := J.injective.comp (hiA.comp J.symm.injective)
  have hjB : Function.Injective (1-B : H →L[ℂ] H) := by
    rw [← hcomp]
    exact J.injective.comp (hjA.comp J.symm.injective)
  have hTB : Commute T B := by
    have hh := hTA.map (antiunitaryConjugateRealHom J)
    change Commute (antiunitaryConjugate J T) B at hh
    rw [hflip] at hh
    simpa only [sub_sub_cancel] using (Commute.one_left B).sub_left hh
  have hphase (t : ℝ) :
      resolventPhaseOperator T t * resolventDampingOperator A * resolventDampingOperator B =
      resolventDampingOperator T * resolventPhaseOperator A t * resolventPhaseOperator B (-t) := by
    have hD : antiunitaryConjugate J (resolventDampingOperator A)=resolventDampingOperator B := by
      change (antiunitaryConjugateRealHom J) (A*(1-A))=B*(1-B)
      simp only [map_mul,map_sub,map_one]
      rfl
    have hF : antiunitaryConjugate J (resolventPhaseOperator A t)=resolventPhaseOperator B (-t) := by
      unfold resolventPhaseOperator
      rw [antiunitaryConjugate_complex_cfc J A (IsSelfAdjoint.of_nonneg hA0)
        _ (resolventPhaseFunction_continuous t)]
      simp only [resolventPhaseFunction_star]
      rfl
    have hR : R (-t)*resolventDampingOperator B=resolventPhaseOperator B (-t) := by
      have he := congrArg (antiunitaryConjugate J) (hleft t)
      rw [antiunitaryConjugate_mul,hJleft,hD,hF] at he
      exact he
    have hRd : Commute (R (-t)) (resolventDampingOperator A) :=
      (hRcomm (-t)).mul_right ((Commute.one_right (R (-t))).sub_right (hRcomm (-t)))
    ext1 x
    change resolventPhaseOperator T t (resolventDampingOperator A (resolventDampingOperator B x)) =
      resolventDampingOperator T (resolventPhaseOperator A t (resolventPhaseOperator B (-t) x))
    rw [← resolventImaginaryPower_damping T hT0 hT1 hiT hjT t]
    rw [resolventImaginaryPower_commutes_damping T hT0 hT1 hiT hjT t,hmod]
    have hrd := congrArg (fun W : H →L[ℂ] H => W (resolventDampingOperator B x)) hRd.eq
    change R (-t) (resolventDampingOperator A (resolventDampingOperator B x)) =
      resolventDampingOperator A (R (-t) (resolventDampingOperator B x)) at hrd
    rw [hrd]
    have hrx := congrArg (fun W : H →L[ℂ] H => W x) hR
    change R (-t) (resolventDampingOperator B x)=resolventPhaseOperator B (-t) x at hrx
    rw [hrx]
    have hlx := congrArg (fun W : H →L[ℂ] H => W (resolventPhaseOperator B (-t) x)) (hleft t)
    change L t (resolventDampingOperator A (resolventPhaseOperator B (-t) x)) =
      resolventPhaseOperator A t (resolventPhaseOperator B (-t) x) at hlx
    rw [hlx]
  refine ⟨hTB,hiB,?_⟩
  exact F1Fecho.ModularCutBalance.damped_phase_operator_balance T A B
    ⟨hT0,hT1⟩ ⟨hA0,hA1⟩ ⟨hB0,hB1⟩ hTA hTB hAB hiT hjT hiA hjA hiB hjB hphase
end F1Fecho.PolarModularBalance
#print axioms F1Fecho.PolarModularBalance.balance
