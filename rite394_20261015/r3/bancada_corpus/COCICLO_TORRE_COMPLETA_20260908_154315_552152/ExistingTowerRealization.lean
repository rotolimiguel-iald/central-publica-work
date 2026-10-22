import InfiniteCocycleDecoding
import TGLExt.DensityStateUniqueness
import TGLExt.ExpectationPositive
set_option autoImplicit false
set_option maxHeartbeats 2400000
namespace ChatgptAudit.CocycleRealization
open Filter Topology Set TGLExt ChatgptAudit.Response028 ChatgptAudit.Cocycle030
  ChatgptAudit.Density033 ChatgptAudit.Thermal025
noncomputable section

def binarySite (b : Bool) : Fin 2 := if b then 0 else 1

def towerConfiguration (u : ℕ → Bool) : (N : ℕ) → chainIdx N
  | 0 => binarySite (u 0)
  | N+1 => (towerConfiguration u N,binarySite (u (N+1)))

theorem actual_site_log_reading (t : ℝ) (u : ℕ → Bool) (n : ℕ) :
    Real.log (siteW ((amplitudeProfile geometricAmplitude t).w n) (binarySite (u n))) -
      Real.log (siteW (thirdThermalReference.w n) (binarySite (u n))) =
        geometricSiteReading t u n := by
  have h := third_log_coefficients (geometricArgument t n)
    (geometric_argument_bounds t n).1 (geometric_argument_bounds t n).2
  cases hu : u n
  · simpa [binarySite,siteW,geometricSiteReading,hu,amplitudeProfile,
      thirdThermalReference,geometricArgument] using h.2
  · simpa [binarySite,siteW,geometricSiteReading,hu,amplitudeProfile,
      thirdThermalReference,geometricArgument] using h.1

theorem actual_prefix_log_reading (t : ℝ) (u : ℕ → Bool) (N : ℕ) :
    Real.log (towerW (amplitudeProfile geometricAmplitude t) N (towerConfiguration u N)) -
      Real.log (towerW thirdThermalReference N (towerConfiguration u N)) =
        ∑ n ∈ Finset.range (N+1), geometricSiteReading t u n := by
  induction N with
  | zero =>
    simpa only [towerW,towerConfiguration,Nat.zero_add,Finset.sum_range_one] using actual_site_log_reading t u 0
  | succ N ih =>
    change Real.log (towerW (amplitudeProfile geometricAmplitude t) N (towerConfiguration u N) *
        siteW ((amplitudeProfile geometricAmplitude t).w (N+1)) (binarySite (u (N+1)))) -
      Real.log (towerW thirdThermalReference N (towerConfiguration u N) *
        siteW (thirdThermalReference.w (N+1)) (binarySite (u (N+1)))) = _
    rw [Real.log_mul (ne_of_gt (towerW_pos _ _ _))
      (ne_of_gt (siteW_pos ((amplitudeProfile geometricAmplitude t).pos _)
        ((amplitudeProfile geometricAmplitude t).lt_one _) _))]
    rw [Real.log_mul (ne_of_gt (towerW_pos _ _ _))
      (ne_of_gt (siteW_pos (thirdThermalReference.pos _) (thirdThermalReference.lt_one _) _))]
    rw [Finset.sum_range_succ]
    have hs := actual_site_log_reading t u (N+1)
    linarith

theorem actual_prefix_matrix_diagonal (t : ℝ) (u : ℕ → Bool) (N : ℕ) :
    matrixLogRatio (towerW thirdThermalReference N)
      (towerW (amplitudeProfile geometricAmplitude t) N)
      (towerConfiguration u N) (towerConfiguration u N) =
      ((∑ n ∈ Finset.range (N+1), geometricSiteReading t u n : ℝ) : ℂ) := by
  simp only [matrixLogRatio,Matrix.diagonal_apply_eq,actual_prefix_log_reading]

theorem actual_prefix_scalar_limit (t : ℝ) (u : ℕ → Bool) :
    Tendsto (fun N => Real.log (towerW (amplitudeProfile geometricAmplitude t) N
        (towerConfiguration u N)) -
      Real.log (towerW thirdThermalReference N (towerConfiguration u N))) atTop
      (𝓝 (geometricLogReading t u)) := by
  simp only [actual_prefix_log_reading,geometric_log_reading_eq_actual_series]
  exact (geometric_site_reading_summable t u).hasSum.tendsto_sum_nat.comp
    (tendsto_add_atTop_nat 1)

theorem existing_operator_is_same_prefix (t : ℝ) (N : ℕ) :
    likelihoodPrefix geometricAmplitude t N = towerPi thirdThermalReference
      (matrixLogRatio (towerW thirdThermalReference N)
        (towerW (amplitudeProfile geometricAmplitude t) N)) :=
  likelihood_prefix_local geometricAmplitude t N

theorem existing_operator_norm_limit (t : ℝ) :
    Tendsto (likelihoodPrefix geometricAmplitude t) atTop
      (𝓝 (likelihoodGenerator geometricAmplitude t)) :=
  likelihood_prefix_tendsto geometricAmplitude t

theorem existing_density_is_prepared_state (t : ℝ)
    (A : TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference)
    (hA : A ∈ theFactorObject thirdThermalReference) :
    amplitudeState geometricAmplitude t A =
      omegaState thirdThermalReference (likelihoodDensity geometricAmplitude t*A) :=
  likelihood_density_state_left geometricAmplitude t A hA

theorem existing_site_projections_commute (n m : ℕ) :
    Commute (siteZeroProjection thirdThermalReference n)
      (siteZeroProjection thirdThermalReference m) :=
  site_zero_commute thirdThermalReference n m

theorem existing_finite_representation_faithful (N : ℕ) :
    Function.Injective (fun a : Matrix (chainIdx N) (chainIdx N) ℂ =>
      towerPi thirdThermalReference a) :=
  towerPi_injective thirdThermalReference N

#print axioms binarySite
#print axioms towerConfiguration
#print axioms actual_site_log_reading
#print axioms actual_prefix_log_reading
#print axioms actual_prefix_matrix_diagonal
#print axioms actual_prefix_scalar_limit
#print axioms existing_operator_is_same_prefix
#print axioms existing_operator_norm_limit
#print axioms existing_density_is_prepared_state
#print axioms existing_site_projections_commute
#print axioms existing_finite_representation_faithful

end
end ChatgptAudit.CocycleRealization
