import TGLExt.V350LocalBasePolarCommutation
import TGLExt.V351ResolventImaginaryContinuity
import TGLExt.V350AntiunitaryPositiveConjugation
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Unique

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open ChatgptAudit ChatgptAudit.Continuous050
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem resolventPhaseFunction_reflection (t x : ℝ) :
    star (resolventPhaseFunction t (1-x)) = resolventPhaseFunction t x := by
  have hb : resolventDamping (1-x) = resolventDamping x := by
    unfold resolventDamping
    ring
  have hl : Real.log ((1-(1-x))/(1-x)) = -Real.log ((1-x)/x) := by
    rw [sub_sub_cancel, ← inv_div, Real.log_inv]
  rw [resolventPhaseFunction_star]
  unfold resolventPhaseFunction modularPhase
  rw [hb, hl]
  congr 2
  push_cast
  ring

theorem antiunitaryConjugate_star (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (star T) = star (antiunitaryConjugate J T) := by
  change antiunitaryConjugate J T.adjoint = (antiunitaryConjugate J T).adjoint
  apply (ContinuousLinearMap.eq_adjoint_iff _ _).mpr
  intro x y
  calc
    inner ℂ (antiunitaryConjugate J T.adjoint x) y =
        star (inner ℂ (T.adjoint (J.symm x)) (J.symm y)) := by
      simpa only [antiunitaryConjugate_apply, J.apply_symm_apply] using
        antiunitary_inner_conj J (T.adjoint (J.symm x)) (J.symm y)
    _ = star (inner ℂ (J.symm x) (T (J.symm y))) :=
      congrArg star (T.adjoint_inner_left (J.symm y) (J.symm x))
    _ = inner ℂ x (antiunitaryConjugate J T y) := by
      simpa only [antiunitaryConjugate_apply, J.apply_symm_apply] using
        (antiunitary_inner_conj J (J.symm x) (T (J.symm y))).symm

/-- Antiunitary conjugation is a real, not complex, star algebra homomorphism. -/
def antiunitaryConjugateRealHom (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    (H →L[ℂ] H) →⋆ₐ[ℝ] (H →L[ℂ] H) where
  toFun := antiunitaryConjugate J
  map_one' := by ext x; simp [antiunitaryConjugate_apply]
  map_mul' := antiunitaryConjugate_mul J
  map_zero' := by ext x; simp [antiunitaryConjugate_apply]
  map_add' := antiunitaryConjugate_add J
  commutes' := by
    intro r
    ext x
    simp [antiunitaryConjugate_apply, Algebra.algebraMap_eq_smul_one]
    calc
      J (r • J.symm x) = J ((r : ℂ) • J.symm x) :=
        congrArg J (RCLike.real_smul_eq_coe_smul (K := ℂ) r (J.symm x))
      _ = (r : ℂ) • x := by
        rw [map_smulₛₗ]
        rw [J.apply_symm_apply]
        exact congrArg (fun c : ℂ => c • x) (Complex.conj_ofReal r)
      _ = r • x := (RCLike.real_smul_eq_coe_smul (K := ℂ) r x).symm
  map_star' := antiunitaryConjugate_star J

theorem antiunitaryConjugate_continuous (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    Continuous (antiunitaryConjugate J) := by
  have hc : Continuous (fun T : H →L[ℂ] H =>
      T.comp J.symm.toLinearIsometry.toContinuousLinearMap) :=
    continuous_id.clm_comp_const J.symm.toLinearIsometry.toContinuousLinearMap
  exact hc.const_clm_comp J.toLinearIsometry.toContinuousLinearMap

theorem antiunitaryConjugate_selfadjoint (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) : IsSelfAdjoint (antiunitaryConjugate J T) :=
  (antiunitaryConjugate_star J T).symm.trans (congrArg (antiunitaryConjugate J) hT.star_eq)

theorem antiunitaryConjugate_real_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℝ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc f T) = cfc f (antiunitaryConjugate J T) :=
  (antiunitaryConjugateRealHom J).map_cfc f T hf.continuousOn
    (antiunitaryConjugate_continuous J) hT (antiunitaryConjugate_selfadjoint J T hT)

theorem complex_cfc_real_imaginary (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (f : ℝ → ℂ) (hf : Continuous f) :
    cfc (fun z : ℂ => f z.re) T =
      cfc (fun x : ℝ => (f x).re) T + Complex.I • cfc (fun x : ℝ => (f x).im) T := by
  have hr : Continuous (fun z : ℂ => (((f z.re).re : ℝ) : ℂ)) := by fun_prop
  have hi : Continuous (fun z : ℂ => (((f z.re).im : ℝ) : ℂ)) := by fun_prop
  calc
    _ = cfc (fun z : ℂ => (((f z.re).re : ℝ) : ℂ) + Complex.I * (((f z.re).im : ℝ) : ℂ)) T :=
      cfc_congr fun z _ => by simpa only [mul_comm] using (Complex.re_add_im (f z.re)).symm
    _ = cfc (fun z : ℂ => (((f z.re).re : ℝ) : ℂ)) T +
        Complex.I • cfc (fun z : ℂ => (((f z.re).im : ℝ) : ℂ)) T := by
      rw [cfc_add _ _ _ hr.continuousOn (by fun_prop), cfc_const_mul _ _ _ hi.continuousOn]
    _ = _ := by
      rw [← cfc_real_eq_complex (fun x : ℝ => (f x).re) hT,
        ← cfc_real_eq_complex (fun x : ℝ => (f x).im) hT]

theorem antiunitaryConjugate_complex_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℂ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc (fun z : ℂ => f z.re) T) =
      cfc (fun z : ℂ => star (f z.re)) (antiunitaryConjugate J T) := by
  rw [complex_cfc_real_imaginary T hT f hf, antiunitaryConjugate_add,
    antiunitaryConjugate_smul,
    antiunitaryConjugate_real_cfc J T hT (fun x : ℝ => (f x).re) (Complex.continuous_re.comp hf),
    antiunitaryConjugate_real_cfc J T hT (fun x : ℝ => (f x).im) (Complex.continuous_im.comp hf)]
  rw [complex_cfc_real_imaginary _ (antiunitaryConjugate_selfadjoint J T hT)
    (fun x => star (f x)) hf.star]
  simp only [Complex.star_def, Complex.conj_re, Complex.conj_im, cfc_neg,
    Complex.conj_I, neg_smul, smul_neg]

theorem antiunitaryConjugate_resolventPhase (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) :
    antiunitaryConjugate J (resolventPhaseOperator T t) = resolventPhaseOperator T t := by
  unfold resolventPhaseOperator
  rw [antiunitaryConjugate_complex_cfc J T hT _ (resolventPhaseFunction_continuous t), hflip]
  have hc : Continuous (fun z : ℂ => star (resolventPhaseFunction t z.re)) :=
    ((resolventPhaseFunction_continuous t).comp Complex.continuous_re).star
  have he := cfc_comp' (fun z : ℂ => star (resolventPhaseFunction t z.re))
    (fun z : ℂ => 1-z) T hc.continuousOn (by fun_prop) hT.isStarNormal
  have hg : cfc (fun z : ℂ => 1-z) T = 1-T := by
    rw [cfc_sub _ _ _ (by fun_prop) (by fun_prop),
      cfc_const (1 : ℂ) T hT.isStarNormal, cfc_id' ℂ T hT.isStarNormal, map_one]
  rw [hg] at he
  rw [← he]
  apply cfc_congr
  intro z _
  simpa only [Complex.sub_re, Complex.one_re] using resolventPhaseFunction_reflection t z.re

theorem antiunitaryConjugate_resolventDamping (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) :
    antiunitaryConjugate J (resolventDampingOperator T) = resolventDampingOperator T := by
  rw [← resolventPhaseOperator_zero T hT]
  exact antiunitaryConjugate_resolventPhase J T hT hflip 0

theorem resolventImaginaryPower_antiunitary (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (hi : Function.Injective T) (hj : Function.Injective (1-T : H →L[ℂ] H))
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) (x : H) :
    J (resolventImaginaryPower T hT h1 hi hj t x) =
      resolventImaginaryPower T hT h1 hi hj t (J x) := by
  have hB (y : H) : J (resolventDampingOperator T y) = resolventDampingOperator T (J y) := by
    have h := congrArg (fun A : H →L[ℂ] H => A (J y))
      (antiunitaryConjugate_resolventDamping J T (IsSelfAdjoint.of_nonneg hT) hflip)
    simpa only [antiunitaryConjugate_apply, J.symm_apply_apply] using h
  have hC (y : H) : J (resolventPhaseOperator T t y) = resolventPhaseOperator T t (J y) := by
    have h := congrArg (fun A : H →L[ℂ] H => A (J y))
      (antiunitaryConjugate_resolventPhase J T (IsSelfAdjoint.of_nonneg hT) hflip t)
    simpa only [antiunitaryConjugate_apply, J.symm_apply_apply] using h
  refine (resolventDampingOperator_denseRange T hT h1 hi hj).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  rw [resolventImaginaryPower_damping, hB, resolventImaginaryPower_damping]
  exact hC y

#print axioms resolventPhaseFunction_reflection
#print axioms antiunitaryConjugate_star
#print axioms antiunitaryConjugate_add
#print axioms antiunitaryConjugate_smul
#print axioms antiunitaryConjugateRealHom
#print axioms antiunitaryConjugate_continuous
#print axioms antiunitaryConjugate_selfadjoint
#print axioms antiunitaryConjugate_real_cfc
#print axioms complex_cfc_real_imaginary
#print axioms antiunitaryConjugate_complex_cfc
#print axioms antiunitaryConjugate_resolventPhase
#print axioms antiunitaryConjugate_resolventDamping
#print axioms resolventImaginaryPower_antiunitary
end
end TGLV350.Regular
