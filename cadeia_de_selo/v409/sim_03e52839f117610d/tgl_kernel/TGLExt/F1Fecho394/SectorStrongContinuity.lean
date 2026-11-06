import TGLExt.F1Fecho394.SectorDirectSum
import Mathlib.Analysis.Normed.Group.Tannery
import Mathlib.Tactic
/-! Strong continuity of a diagonal family on the completed Hilbert sum.
The sectorwise continuity hypothesis is explicit; no uniform continuity in n is assumed.
The summable dominating sequence is exactly 4 * norm(f n)^2. -/
set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section
open Filter Topology
open scoped ENNReal

namespace F1Rede.SectorStrongContinuity
open F1Rede.SectorDirectSum
variable {E : ℕ → Type*} [∀ n, NormedAddCommGroup (E n)]
  [∀ n, InnerProductSpace ℂ (E n)] [∀ n, CompleteSpace (E n)]

theorem norm_sq_eq_tsum (f : SumSpace E) : ‖f‖^2 = ∑' n, ‖f n‖^2 := by
  simpa using lp.norm_rpow_eq_tsum (by norm_num : 0 < (2 : ℝ≥0∞).toReal) f

theorem summable_norm_sq (f : SumSpace E) : Summable (fun n => ‖f n‖^2) := by
  simpa using (lp.memℓp f).summable (by norm_num : 0 < (2 : ℝ≥0∞).toReal)

theorem sector_difference_bound (v w : ∀ n, E n ≃ₗᵢ[ℂ] E n) (f : SumSpace E) (n : ℕ) :
    ‖v n (f n) - w n (f n)‖^2 ≤ 4 * ‖f n‖^2 := by
  have hb : ‖v n (f n) - w n (f n)‖ ≤ 2 * ‖f n‖ := by
    calc
      _ ≤ ‖v n (f n)‖ + ‖w n (f n)‖ := norm_sub_le _ _
      _ = 2 * ‖f n‖ := by rw [(v n).norm_map,(w n).norm_map]; ring
  calc
    _ ≤ (2 * ‖f n‖)^2 := pow_le_pow_left₀ (norm_nonneg _) hb 2
    _ = 4 * ‖f n‖^2 := by ring

/-- Strong continuity sector by sector implies strong continuity on the entire Hilbert sum. -/
theorem diagonal_strongly_continuous {A : Type*} [TopologicalSpace A]
    (u : A → ∀ n, E n ≃ₗᵢ[ℂ] E n)
    (hu : ∀ n (x : E n), Continuous (fun a => u a n x))
    (f : SumSpace E) : Continuous (fun a => diagonal (u a) f) := by
  rw [continuous_iff_continuousAt]
  intro a0
  have ht := tendsto_tsum_of_dominated_convergence (𝓕 := 𝓝 a0)
    (f := fun a n => ‖u a n (f n) - u a0 n (f n)‖^2)
    (g := fun _ : ℕ => (0 : ℝ))
    (bound := fun n => 4 * ‖f n‖^2)
    ((summable_norm_sq f).mul_left 4)
    (fun n => by
      have hc : Continuous (fun a => u a n (f n) - u a0 n (f n)) :=
        (hu n (f n)).sub continuous_const
      simpa using (hc.norm.pow 2).tendsto a0)
    (Eventually.of_forall (fun a n => by
      rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
      exact sector_difference_bound (u a) (u a0) f n))
  have hsq : Tendsto (fun a => ‖diagonal (u a) f - diagonal (u a0) f‖^2)
      (𝓝 a0) (𝓝 (0 : ℝ)) := by
    simpa only [norm_sq_eq_tsum, lp.coeFn_sub, Pi.sub_apply, diagonal_apply, tsum_zero] using ht
  have hsqrt := Real.continuous_sqrt.continuousAt.tendsto.comp hsq
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [Function.comp_def, Real.sqrt_sq_eq_abs, abs_norm, Real.sqrt_zero, dist_eq_norm] using hsqrt

end F1Rede.SectorStrongContinuity

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    match ci with
    | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
    | _ => pure ()
