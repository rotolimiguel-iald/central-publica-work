import TGLExt.F1Fecho394.RegularCovariantCoreR3
import TGLExt.V350RegularApproximation
/-! Generic strong regular averages, ported from V350 to the supplied actual
unitary flow; membership is in its actual generated bicommutant. -/
set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.RegularCoreAverage
open MeasureTheory Filter TGLV350 TGLV350.Regular F1Fecho.RegularCovariantCore
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
def regularBundledUnitary (B : UnitaryFlow H) (t : ℝ) :
    unitary (RegularHilbert H →L[ℂ]
      RegularHilbert H) :=
  ⟨regularUnitary B t, Unitary.mem_iff.mpr (regular_unitary B t)⟩

theorem regular_norm_map (B : UnitaryFlow H) (t : ℝ)
    (v : RegularHilbert H) :
    ‖regularUnitary B t v‖ = ‖v‖ := Unitary.norm_map (regularBundledUnitary B t) v

def regularIntegralFamily (B : UnitaryFlow H) :
    StrongIntegral.Family (H := RegularHilbert H) where
  op := regularUnitary B
  continuous_apply := regular_strongly_continuous B
  bound := 1
  bound_nonneg := zero_le_one
  norm_bound := fun t => ContinuousLinearMap.opNorm_le_bound _ zero_le_one
    (fun v => by rw [regular_norm_map, one_mul])

/-- One-sided normalized averages of the actual regular unitaries. The value
at h=0 is zero; convergence is asserted on the punctured neighborhood. -/
def regularAverage (B : UnitaryFlow H) (h : ℝ) :
    RegularHilbert H →L[ℂ]
      RegularHilbert H :=
  (h⁻¹ : ℝ) • StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h

theorem regularAverage_apply (B : UnitaryFlow H) (h : ℝ)
    (v : RegularHilbert H) :
    regularAverage B h v = h⁻¹ • ∫ t in 0..h, regularUnitary B t v := rfl

theorem regularAverage_mem (B : UnitaryFlow H) (M : VonNeumannAlgebra H) (h : ℝ) :
    regularAverage B h ∈ core B M := by
  change ((h⁻¹ : ℝ) : ℂ) • StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h ∈ _
  apply (core B M).toStarSubalgebra.smul_mem
  exact StrongIntegral.operatorIntegral_mem _ _ _ _ (regular_mem B M)

theorem regularAverage_norm_le_one (B : UnitaryFlow H) (h : ℝ) :
    ‖regularAverage B h‖ ≤ 1 := by
  by_cases hh : h = 0
  · subst h
    simp [regularAverage]
  · have hb := StrongIntegral.operatorIntegral_norm_le (regularIntegralFamily B) 0 h
    change ‖StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h‖ ≤ 1 * |h-0| at hb
    simp only [sub_zero, one_mul] at hb
    calc
      ‖regularAverage B h‖ = |h⁻¹| * ‖StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h‖ := by
        change ‖((h⁻¹ : ℝ) : ℂ) • StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h‖ = _
        rw [norm_smul, Complex.norm_real, Real.norm_eq_abs]
      _ ≤ |h⁻¹| * |h| := mul_le_mul_of_nonneg_left hb (abs_nonneg _)
      _ = 1 := by rw [abs_inv, inv_mul_cancel₀ (abs_ne_zero.mpr hh)]

/-- The fundamental theorem of calculus gives strong convergence without
operator-norm continuity of the unitary group. -/
theorem regularAverage_tendsto_identity (B : UnitaryFlow H)
    (v : RegularHilbert H) :
    Tendsto (fun h : ℝ => regularAverage B h v) (𝓝[≠] 0) (𝓝 v) := by
  have hc := regular_strongly_continuous B v
  have hd := intervalIntegral.integral_hasDerivAt_right
    (hc.intervalIntegrable 0 0) hc.stronglyMeasurable.stronglyMeasurableAtFilter hc.continuousAt
  have ht := hd.tendsto_slope_zero
  simpa only [zero_add, intervalIntegral.integral_same, sub_zero,
    F1Fecho.RegularCovariantCore.regular_zero B, one_apply_eq_self, regularAverage_apply] using ht

theorem regularAverage_mul_tendsto (B : UnitaryFlow H)
    (A : RegularHilbert H →L[ℂ]
      RegularHilbert H)
    (v : RegularHilbert H) :
    Tendsto (fun h : ℝ => (A * regularAverage B h) v) (𝓝[≠] 0) (𝓝 (A v)) :=
  A.continuous.continuousAt.tendsto.comp (regularAverage_tendsto_identity B v)

/-- The dual orbit of the average is the Fourier-modulated vector integral
of the same regular unitary group. -/
theorem regularAverage_dual_apply (B : UnitaryFlow H) (s h : ℝ)
    (v : RegularHilbert H) :
    dualAmbient s (regularAverage B h) v =
      h⁻¹ • ∫ t in 0..h, characterPhase s t • regularUnitary B t v := by
  unfold regularAverage
  rw [dualAmbient_real_smul]
  change h⁻¹ • (dualAmbient s (StrongIntegral.operatorIntegral (regularIntegralFamily B) 0 h) v) = _
  rw [dualAmbient_strongIntegral_apply]
  congr 1
  apply intervalIntegral.integral_congr
  intro t _
  change dualAmbient s (regularUnitary B t) v = _
  rw [dual_on_regular B]
  rfl


end F1Fecho.RegularCoreAverage
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.RegularCoreAverage).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
