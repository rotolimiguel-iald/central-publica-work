import TGLExt.F1Fecho394.CFCIntertwiningR3
import TGLExt.V351ResolventImaginaryContinuity
/-! Damping-defined imaginary powers respect bounded intertwiners.
No invertibility or surjectivity of the intertwiner is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.ContinuousIntertwining
open TGLV350.Regular
variable {H K:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
variable (A:H→L[ℂ]H) (B:K→L[ℂ]K) (V:H→L[ℂ]K) (hV:V.comp A=B.comp V)

include hV in
lemma damping_intertwine (x:H) :
    V (resolventDampingOperator A x)=resolventDampingOperator B (V x) := by
  have h (y:H):V (A y)=B (V y):=congrArg (fun L:H→L[ℂ]K=>L y) hV
  change V (A ((1-A) x))=B ((1-B) (V x))
  rw [h]
  change B (V (x-A x))=B (V x-B (V x))
  rw [map_sub,h]

include hV in
lemma phase_intertwine (hA:IsSelfAdjoint A) (hB:IsSelfAdjoint B) (t:ℝ) (x:H) :
    V (resolventPhaseOperator A t x)=resolventPhaseOperator B t (V x) := by
  exact congrArg (fun L:H→L[ℂ]K=>L x)
    (cfc_intertwine A B hA hB V hV
      (fun z:ℂ=>resolventPhaseFunction t z.re)
      ((resolventPhaseFunction_continuous t).comp Complex.continuous_re))

include hV in
theorem imaginaryPower_intertwine (hA0:0≤A) (hA1:A≤1) (hAi:Function.Injective A)
    (hAj:Function.Injective (1-A:H→L[ℂ]H))
    (hB0:0≤B) (hB1:B≤1) (hBi:Function.Injective B)
    (hBj:Function.Injective (1-B:K→L[ℂ]K)) (t:ℝ) (x:H) :
    V (resolventImaginaryPower A hA0 hA1 hAi hAj t x)=
      resolventImaginaryPower B hB0 hB1 hBi hBj t (V x) := by
  refine (resolventDampingOperator_denseRange A hA0 hA1 hAi hAj).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  rw [damping_intertwine A B V hV,resolventImaginaryPower_damping,
    resolventImaginaryPower_damping]
  exact phase_intertwine A B V hV (IsSelfAdjoint.of_nonneg hA0)
    (IsSelfAdjoint.of_nonneg hB0) t y

end F1Fecho.ContinuousIntertwining
#print axioms F1Fecho.ContinuousIntertwining.damping_intertwine
#print axioms F1Fecho.ContinuousIntertwining.phase_intertwine
#print axioms F1Fecho.ContinuousIntertwining.imaginaryPower_intertwine
