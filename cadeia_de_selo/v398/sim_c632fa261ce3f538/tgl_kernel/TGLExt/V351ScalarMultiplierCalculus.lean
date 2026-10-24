import TGLExt.V351RegularPositiveGraph
import Mathlib.Analysis.CStarAlgebra.ContinuousMap
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Unique

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Bounded scalar data for the existing spatial field lift. -/
def compactScalarField (g : ℝ → unitInterval) (hg : Continuous g)
    (f : C(unitInterval, ℂ)) : StrongIntegral.Family (H := H) where
  op x := f (g x) • (1 : H →L[ℂ] H)
  continuous_apply v := (f.continuous.comp hg).smul continuous_const
  bound := ‖f‖
  bound_nonneg := norm_nonneg f
  norm_bound x := ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg f) (fun v => by
    change ‖f (g x) • v‖ ≤ ‖f‖ * ‖v‖
    rw [norm_smul]
    exact mul_le_mul_of_nonneg_right (f.norm_coe_le_norm (g x)) (norm_nonneg v))

/-- The existing lift, bundled to consume mathlib's naturality of CFC. -/
def compactScalarRepresentation (g : ℝ → unitInterval) (hg : Continuous g) :
    C(unitInterval, ℂ) →⋆ₐ[ℂ] (RegularHilbert H →L[ℂ] RegularHilbert H) where
  toFun f := operatorFieldLift (compactScalarField g hg f)
  map_one' := by
    rw [operatorFieldLift_constant _ (1 : H →L[ℂ] H) (by intro x; simp [compactScalarField])]
    exact fibre_one
  map_zero' := by
    ext1 u
    apply Lp.ext
    filter_upwards [operatorFieldLift_ae (compactScalarField g hg 0) u,
      Lp.coeFn_zero H 2 volume] with x hx hz
    simpa [compactScalarField, hz] using hx
  map_add' f k := operatorFieldLift_add _ _ _ (by
    intro x
    simp [compactScalarField, add_smul])
  map_mul' f k := operatorFieldLift_mul _ _ _ (by
    intro x
    simp [compactScalarField, smul_smul, mul_comm])
  commutes' c := by
    rw [operatorFieldLift_constant _ (c • (1 : H →L[ℂ] H)) (by intro x; rfl)]
    rw [fibre_smul, fibre_one]
    rfl
  map_star' f := operatorFieldLift_star _ _ (by
    intro x
    simp [compactScalarField])

theorem compactScalarRepresentation_ae (g : ℝ → unitInterval) (hg : Continuous g)
    (f : C(unitInterval, ℂ)) (u : RegularHilbert H) :
    compactScalarRepresentation g hg f u =ᵐ[volume] fun x => f (g x) • u x :=
  operatorFieldLift_ae (compactScalarField g hg f) u

theorem compactScalarRepresentation_coordinate (g : ℝ → unitInterval) (hg : Continuous g) :
    compactScalarRepresentation (H := H) g hg
      (⟨fun a => ((a : ℝ) : ℂ), by fun_prop⟩ : C(unitInterval, ℂ)) =
      realScalarMultiplier (fun x => (g x : ℝ)) (continuous_subtype_val.comp hg)
        (fun x => (g x).property.1) (fun x => (g x).property.2) := by
  ext1 u
  apply Lp.ext
  filter_upwards [compactScalarRepresentation_ae g hg
      (⟨fun a => ((a : ℝ) : ℂ), by fun_prop⟩ : C(unitInterval, ℂ)) u,
    realScalarMultiplier_ae (fun x => (g x : ℝ)) (continuous_subtype_val.comp hg)
      (fun x => (g x).property.1) (fun x => (g x).property.2) u] with x hx hy
  exact hx.trans hy.symm

/-- Continuous functional calculus of the existing positive scalar multiplier
acts pointwise on L² classes. The global continuity assumption covers the
resolventPhaseFunction used by the constructed imaginary powers. -/
theorem realScalarMultiplier_cfc_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1)
    (f : ℂ → ℂ) (hf : Continuous f) (u : RegularHilbert H) :
    cfc f (realScalarMultiplier g hg h0 h1) u =ᵐ[volume]
      fun x => f (g x : ℂ) • u x := by
  let gb : ℝ → unitInterval := fun x => ⟨g x, h0 x, h1 x⟩
  have hgb : Continuous gb := hg.subtype_mk _
  let F := compactScalarRepresentation (H := H) gb hgb
  let a : C(unitInterval, ℂ) := ⟨fun x => ((x : ℝ) : ℂ), by fun_prop⟩
  have ha : F a = realScalarMultiplier g hg h0 h1 :=
    compactScalarRepresentation_coordinate gb hgb
  have hcont : Continuous F :=
    (F.toLinearMap.mkContinuous 1 (by
      intro k
      change ‖operatorFieldLift (compactScalarField (H := H) gb hgb k)‖ ≤ 1 * ‖k‖
      simpa only [one_mul, compactScalarField] using
        operatorFieldLift_norm_le (compactScalarField (H := H) gb hgb k))).continuous
  have hc := F.map_cfc f a hf.continuousOn hcont
  rw [ha] at hc
  rw [← hc]
  have he (z : unitInterval) : (cfc f a) z = f ((z : ℝ) : ℂ) := by
    have hv := (ContinuousMap.evalStarAlgHom ℂ ℂ z).map_cfc f a hf.continuousOn
    change (cfc f a) z = cfc f ((z : ℝ) : ℂ) at hv
    exact hv.trans (by simpa using cfc_algebraMap (A := ℂ) ((z : ℝ) : ℂ) f)
  filter_upwards [compactScalarRepresentation_ae gb hgb (cfc f a) u] with x hx
  change F (cfc f a) u x = _
  rw [hx, he]

#print axioms compactScalarField
#print axioms compactScalarRepresentation
#print axioms compactScalarRepresentation_ae
#print axioms compactScalarRepresentation_coordinate
#print axioms realScalarMultiplier_cfc_ae
end
end TGLV350.Regular
