import TGLExt.V350L2Order
import TGLExt.V351ResolventImaginaryContinuity
import TGLExt.V350ResolventSquareRoot
import TGLExt.F1Fecho394.L2UnitaryMapR2

/-! Lebesgue L2 amplification of the actual resolvent calculus.
This module constructs the positive root and spectral flow on coefficients.
Identification with the weight-GNS Tomita operator is a separate obligation. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory
namespace F1Fecho.FibreModularCalculus
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem fibre_operator_injective (A : H →L[ℂ] H) (hA : Function.Injective A) :
    Function.Injective (fibre A) := by
  intro f g h
  apply Lp.ext
  filter_upwards [fibre_ae A f, fibre_ae A g] with x hf hg
  apply hA
  rw [←hf,←hg,h]

def fibreLinear : (H →L[ℂ] H) →L[ℂ] (RegularHilbert H →L[ℂ] RegularHilbert H) :=
  (fibreRepresentation (H:=H)).toLinearMap.mkContinuous 1 (by
    intro A
    change ‖fibre A‖≤1*‖A‖
    simpa only [one_mul] using fibre_norm_le A)

theorem fibre_continuous : Continuous (fibreRepresentation (H:=H)) :=
  fibreLinear.continuous

theorem fibre_cfc (A : H →L[ℂ] H) (hA : IsSelfAdjoint A)
    (f : ℂ → ℂ) (hf : Continuous f) :
    fibre (cfc f A)=cfc f (fibre A) := by
  have hs : IsSelfAdjoint (fibre A) := by
    change star (fibre A)=fibre A
    rw [←fibre_star,hA.star_eq]
  exact (fibreRepresentation (H:=H)).map_cfc f A hf.continuousOn
    fibre_continuous hA.isStarNormal hs.isStarNormal

theorem fibre_damping (R : H →L[ℂ] H) :
    fibre (resolventDampingOperator R)=resolventDampingOperator (fibre R) := by
  unfold resolventDampingOperator
  rw [fibre_mul]
  have h := map_sub (fibreRepresentation (H:=H)) (1:H→L[ℂ]H) R
  change fibre (1-R)=fibre 1-fibre R at h
  rw [h,fibre_one]

theorem fibre_phase (R : H →L[ℂ] H) (hR : 0≤R) (t : ℝ) :
    fibre (resolventPhaseOperator R t)=resolventPhaseOperator (fibre R) t :=
  fibre_cfc R (IsSelfAdjoint.of_nonneg hR) _
    ((resolventPhaseFunction_continuous t).comp Complex.continuous_re)

variable (R : H →L[ℂ] H) (hR : 0≤R) (h1 : R≤1)
  (hi : Function.Injective R) (hj : Function.Injective (1-R:H→L[ℂ]H))

include h1 in
theorem lifted_le_one : fibre R≤1 := by
  simpa only [fibre_one] using fibre_monotone h1

include hj in
theorem lifted_complement_injective : Function.Injective (1-fibre R:RegularHilbert H→L[ℂ]RegularHilbert H) := by
  have he : fibre (1-R)=1-fibre R := by
    have h := map_sub (fibreRepresentation (H:=H)) (1:H→L[ℂ]H) R
    change fibre (1-R)=fibre 1-fibre R at h
    simpa only [fibre_one] using h
  rw [←he]
  exact fibre_operator_injective _ hj

def liftedRoot : RegularHilbert H →ₗ.[ℂ] RegularHilbert H :=
  resolventSquareRoot (fibre R) (fibre_nonneg hR) (fibre_operator_injective R hi)

include h1 in
theorem liftedRoot_selfadjoint : IsSelfAdjoint (liftedRoot R hR hi) :=
  resolventSquareRoot_selfadjoint _ _ _ (lifted_le_one R h1)

include h1 in
theorem liftedRoot_square :
    partialOperatorSquare (liftedRoot R hR hi)=
      resolventGraphOperator (fibre R) (fibre_operator_injective R hi) :=
  resolventSquareRoot_square _ _ _ (lifted_le_one R h1)

def liftedFlow (t : ℝ) : RegularHilbert H ≃ₗᵢ[ℂ] RegularHilbert H :=
  resolventImaginaryPower (fibre R) (fibre_nonneg hR) (lifted_le_one R h1)
    (fibre_operator_injective R hi) (lifted_complement_injective R hj) t

theorem liftedFlow_eq_fibre (t : ℝ) (f : RegularHilbert H) :
    liftedFlow R hR h1 hi hj t f =
      fibre ((resolventImaginaryPower R hR h1 hi hj t).toLinearIsometry.toContinuousLinearMap) f := by
  let U := resolventImaginaryPower R hR h1 hi hj t
  have hd := resolventDampingOperator_denseRange (fibre R) (fibre_nonneg hR)
    (lifted_le_one R h1) (fibre_operator_injective R hi) (lifted_complement_injective R hj)
  refine hd.induction ?_ (isClosed_eq (liftedFlow R hR h1 hi hj t).continuous
    (fibre U.toLinearIsometry.toContinuousLinearMap).continuous) f
  rintro _ ⟨g,rfl⟩
  rw [show liftedFlow R hR h1 hi hj t (resolventDampingOperator (fibre R) g)=
    resolventPhaseOperator (fibre R) t g from resolventImaginaryPower_damping _ _ _ _ _ t g]
  rw [←fibre_damping,←fibre_phase R hR]
  have he : U.toLinearIsometry.toContinuousLinearMap * resolventDampingOperator R =
      resolventPhaseOperator R t := by
    ext1 x
    exact resolventImaginaryPower_damping R hR h1 hi hj t x
  exact congrArg (fun A : RegularHilbert H→L[ℂ]RegularHilbert H => A g)
    ((fibre_mul U.toLinearIsometry.toContinuousLinearMap (resolventDampingOperator R)).symm.trans
      (congrArg fibre he)).symm

end F1Fecho.FibreModularCalculus
#print axioms F1Fecho.FibreModularCalculus.fibre_operator_injective
#print axioms F1Fecho.FibreModularCalculus.fibre_cfc
#print axioms F1Fecho.FibreModularCalculus.liftedRoot_selfadjoint
#print axioms F1Fecho.FibreModularCalculus.liftedRoot_square
#print axioms F1Fecho.FibreModularCalculus.liftedFlow_eq_fibre
