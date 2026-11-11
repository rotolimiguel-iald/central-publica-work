import TGLExt.F1Fecho394.GeneralInverseCutoffWeightR3
import TGLExt.V350ResolventSquareRoot
import TGLExt.V350LevelExpectationUniformBound
/-! Faithful positive sandwich and positive-root membership reused from the
proofs incorporated in canonical v393. No trace law is inferred. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem sqrt_mem_core (N:VonNeumannAlgebra H) (X:H→L[ℂ]H)
    (hm:X∈N) (hX:0≤X) : hilbertPositiveSqrt X∈N := by
  letI:IsClosed (N.toStarSubalgebra:Set (H→L[ℂ]H)):=vonNeumann_norm_closed N
  rw [hilbertPositiveSqrt,CFC.sqrt_eq_real_sqrt X hX]
  exact cfcₙ_mem (𝕜':=ℂ) (s:=N.toStarSubalgebra) Real.sqrt hm

theorem sqrt_conjugation_faithful (R X:H→L[ℂ]H) (hR:0≤R)
    (hi:Function.Injective R)
    (hz:star (hilbertPositiveSqrt R)*X*hilbertPositiveSqrt R=0) : X=0 := by
  have hsi:Function.Injective (hilbertPositiveSqrt R):=positive_sqrt_injective R hR hi
  have hsd:DenseRange (hilbertPositiveSqrt R):=resolventSquareRoot_dense R hR hi
  have hs:star (hilbertPositiveSqrt R)=hilbertPositiveSqrt R:=
    (CFC.sqrt_nonneg R).isSelfAdjoint.star_eq
  have hzv (v:H):X (hilbertPositiveSqrt R v)=0 := by
    apply hsi
    have he:=congrArg (fun T:H→L[ℂ]H=>T v) hz
    simpa only [hs,mul_apply_eq_comp,zero_apply,map_zero] using he
  ext1 x
  change X x=0
  refine hsd.induction ?_ (isClosed_eq X.continuous continuous_const) x
  rintro _ ⟨v,rfl⟩
  exact hzv v
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.sqrt_mem_core
#print axioms F1Fecho.RegularInverseWeight.sqrt_conjugation_faithful
