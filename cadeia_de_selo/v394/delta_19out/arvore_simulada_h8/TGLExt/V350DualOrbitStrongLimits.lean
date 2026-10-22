import TGLExt.V350DualOrbitRepresentation
import TGLExt.V350L2BoundedStrongContinuity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open MeasureTheory Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def dualCharacterField (a : ℝ) : StrongIntegral.Family (H := RegularHilbert H) where
  op s := characterMultiplier (a*s)
  continuous_apply v := (characterMultiplier_strongly_continuous v).comp
    (continuous_const.mul continuous_id)
  bound := 1
  bound_nonneg := zero_le_one
  norm_bound s := ContinuousLinearMap.opNorm_le_bound _ zero_le_one (fun v => by
    rw [characterMultiplier_norm,one_mul])

/-- The varying dual field is a fixed conjugation of a constant-fibre lift.
This identity allows arbitrary bounded strong nets, without exchanging an
uncountable intersection of conull sets with a net limit. -/
theorem dualOrbit_factorization (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualOrbitRepresentation A = operatorFieldLift (dualCharacterField 1) *
      fibre A * operatorFieldLift (dualCharacterField (-1)) := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae (dualIntegralFamily A) f,
    operatorFieldLift_ae (dualCharacterField 1)
      (fibre A (operatorFieldLift (dualCharacterField (-1)) f)),
    fibre_ae A (operatorFieldLift (dualCharacterField (-1)) f),
    operatorFieldLift_ae (dualCharacterField (-1)) f] with s h1 h2 h3 h4
  change operatorFieldLift (dualIntegralFamily A) f s =
    operatorFieldLift (dualCharacterField 1)
      (fibre A (operatorFieldLift (dualCharacterField (-1)) f)) s
  rw [h1,h2,h3,h4]
  change dualAmbient s A (f s) = characterMultiplier (1*s)
    (A (characterMultiplier ((-1)*s) (f s)))
  rw [one_mul,neg_one_mul,dualAmbient_apply,characterMultiplier_star]
  rfl

theorem dualOrbit_tendsto_of_uniformly_bounded {ι : Type*} {l : Filter ι}
    (T : ι → (RegularHilbert H →L[ℂ] RegularHilbert H))
    (S : RegularHilbert H →L[ℂ] RegularHilbert H) (C : ℝ)
    (hbound : ∀ i, ‖T i‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => T i v) l (𝓝 (S v)))
    (f : RegularHilbert (RegularHilbert H)) :
    Tendsto (fun i => dualOrbitRepresentation (T i) f) l
      (𝓝 (dualOrbitRepresentation S f)) := by
  have h := fibre_tendsto_of_uniformly_bounded T S C hbound hT
    (operatorFieldLift (dualCharacterField (-1)) f)
  have ht := (operatorFieldLift (dualCharacterField (H := H) 1)).continuous.continuousAt.tendsto.comp h
  simpa only [dualOrbit_factorization,mul_apply_eq_comp,Function.comp_def] using ht

#print axioms dualCharacterField
#print axioms dualOrbit_factorization
#print axioms dualOrbit_tendsto_of_uniformly_bounded
end
end TGLV350.Regular
