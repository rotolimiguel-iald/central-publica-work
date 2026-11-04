import TGLExt.V351ResolventImaginaryContinuity

/-! Imaginary powers commute with unitary transport between different Hilbert spaces. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.SpectralTransport
open TGLV350.Regular
variable {H E : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (V : H ≃ₗᵢ[ℂ] E) (R : H →L[ℂ] H)

def transported : E →L[ℂ] E := V.conjStarAlgEquiv R
lemma transported_apply (x : E) : transported V R x=V (R (V.symm x)) := rfl
lemma nonneg (h0 : 0 ≤ R) : 0 ≤ transported V R := map_nonneg V.conjStarAlgEquiv h0
lemma le_one (h1 : R ≤ 1) : transported V R ≤ 1 := by
  have h := map_nonneg V.conjStarAlgEquiv (sub_nonneg.mpr h1)
  simpa only [map_sub,map_one,transported,sub_nonneg] using h
lemma injective (hi : Function.Injective R) : Function.Injective (transported V R) := by
  intro x y h
  exact V.symm.injective (hi (V.injective h))
lemma complement_injective (hj : Function.Injective (1-R : H→L[ℂ]H)) :
    Function.Injective (1-transported V R : E→L[ℂ]E) := by
  have h := injective V (1-R) hj
  simpa only [transported,map_sub,map_one] using h

lemma damping (x : H) :
    V (resolventDampingOperator R x)=resolventDampingOperator (transported V R) (V x) := by
  have h : V.conjStarAlgEquiv (resolventDampingOperator R)=
      resolventDampingOperator (transported V R) := by
    simp only [resolventDampingOperator,map_mul,map_sub,map_one,transported]
  have he := congrArg (fun L : E→L[ℂ]E => L (V x)) h
  simpa only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
    LinearIsometryEquiv.symm_apply_apply] using he

lemma phase (h0 : 0 ≤ R) (t : ℝ) (x : H) :
    V (resolventPhaseOperator R t x)=resolventPhaseOperator (transported V R) t (V x) := by
  have h := StarAlgHomClass.map_cfc V.conjStarAlgEquiv
    (fun z : ℂ => resolventPhaseFunction t z.re) R
    ((resolventPhaseFunction_continuous t).comp Complex.continuous_re).continuousOn
    (StarAlgEquiv.isometry V.conjStarAlgEquiv).continuous
    (IsSelfAdjoint.of_nonneg h0).isStarNormal
    (IsSelfAdjoint.of_nonneg (nonneg V R h0)).isStarNormal
  have he := congrArg (fun L : E→L[ℂ]E => L (V x)) h
  simpa only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
    LinearIsometryEquiv.symm_apply_apply,resolventPhaseOperator,transported] using he

theorem imaginaryPower (h0 : 0 ≤ R) (h1 : R ≤ 1) (hi : Function.Injective R)
    (hj : Function.Injective (1-R : H→L[ℂ]H)) (t : ℝ) (x : H) :
    V (resolventImaginaryPower R h0 h1 hi hj t x)=
      resolventImaginaryPower (transported V R) (nonneg V R h0) (le_one V R h1)
        (injective V R hi) (complement_injective V R hj) t (V x) := by
  refine (resolventDampingOperator_denseRange R h0 h1 hi hj).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  rw [damping V R y,resolventImaginaryPower_damping,resolventImaginaryPower_damping]
  exact phase V R h0 t y
end F1Fecho.SpectralTransport
#print axioms F1Fecho.SpectralTransport.damping
#print axioms F1Fecho.SpectralTransport.phase
#print axioms F1Fecho.SpectralTransport.imaginaryPower
