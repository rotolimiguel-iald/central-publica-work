import Lean
import TGLExt.O16.TheEquationOfTruth_T20_v3

set_option autoImplicit false
set_option maxHeartbeats 1400000
namespace ORDEM016.EquationOfTruth
open scoped InnerProductSpace
noncomputable section
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E] [InnerProductSpace 𝕜 E]

theorem diagonal_norm_bound {ι : Type*} [Fintype ι] (b : OrthonormalBasis ι 𝕜 E)
    (L : E →L[𝕜] E) (a : ι → 𝕜) (ha : ∀ i, L (b i) = a i • b i)
    (r : ℝ) (hr : 0 ≤ r) (hab : ∀ i, ‖a i‖ ≤ r) (x : E) : ‖L x‖ ≤ r*‖x‖ := by
  classical
  have hc (i : ι) : b.repr (L x) i = a i * b.repr x i := by
    conv_lhs => rw [← b.sum_repr x]
    simp [map_sum, map_smul, ha, Pi.single_apply, mul_ite, mul_comm]
  have hnorm (z : E) : ‖z‖^2 = ∑ i, ‖b.repr z i‖^2 := by
    rw [← b.repr.norm_map z, EuclideanSpace.norm_sq_eq]
  have hb : ‖L x‖^2 ≤ r^2*‖x‖^2 := by
    rw [hnorm (L x), hnorm x, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i _
    rw [hc, norm_mul, mul_pow]
    exact mul_le_mul_of_nonneg_right (pow_le_pow_left₀ (norm_nonneg _) (hab i) 2) (sq_nonneg _)
  nlinarith [norm_nonneg (L x), norm_nonneg x, mul_nonneg hr (norm_nonneg x)]

variable [FiniteDimensional 𝕜 E] [CompleteSpace E]

theorem reading_eigen_zero (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (v : E) (ev : ℝ) (hv : H v = (ev:𝕜) • v) (hev : ev ≠ 0) : reading H v = 0 := by
  have h2 : reading H (H v) = 0 := by
    have := congrArg (fun A : E →L[𝕜] E => A v) (proj_mul_H H hH)
    simpa using this
  rw [hv, map_smul] at h2
  exact (smul_eq_zero.1 h2).resolve_left (by exact_mod_cast hev)

/-- The gap refers to precisely the eigenvalues of the self-adjoint operator H. -/
theorem finite_gap_norm_rate (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (γ : ℝ) (hγ : 0 < γ)
    (hgap : ∀ i, hH.isSymmetric.eigenvalues (rfl : Module.finrank 𝕜 E = Module.finrank 𝕜 E) i = 0 ∨
      γ ≤ hH.isSymmetric.eigenvalues (rfl : Module.finrank 𝕜 E = Module.finrank 𝕜 E) i)
    (s : ℝ) (hs : 0 ≤ s) (x : E) :
    ‖T H s x - reading H x‖ ≤ Real.exp (-(s*γ))*‖x-reading H x‖ := by
  classical
  let b := hH.isSymmetric.eigenvectorBasis (rfl : Module.finrank 𝕜 E = Module.finrank 𝕜 E)
  let ev := hH.isSymmetric.eigenvalues (rfl : Module.finrank 𝕜 E = Module.finrank 𝕜 E)
  let a := fun i => if ev i = 0 then (0:𝕜) else (Real.exp (-(s*ev i)):𝕜)
  have hv (i) : H (b i) = (ev i:𝕜) • b i := hH.isSymmetric.apply_eigenvectorBasis _ i
  have ha : ∀ i, (T H s - reading H) (b i) = a i • b i := by
    intro i
    by_cases hi : ev i = 0
    · have hk : b i ∈ H.ker := by
        change H (b i) = 0
        rw [hv, hi]
        simp
      have hp : reading H (b i) = b i := Submodule.starProjection_eq_self_iff.mpr hk
      simp [a, hi, T_fix_of_mem_ker H s hk, hp]
    · have hp := reading_eigen_zero H hH (b i) (ev i) (hv i) hi
      simp [a, hi, hp, T_apply_eigen H (ev i) (b i) (hv i) s]
  have hab : ∀ i, ‖a i‖ ≤ Real.exp (-(s*γ)) := by
    intro i
    by_cases hi : ev i = 0
    · simp [a, hi, Real.exp_nonneg]
    · have hge : γ ≤ ev i := (hgap i).resolve_left hi
      have hex : Real.exp (-(s*ev i)) ≤ Real.exp (-(s*γ)) :=
        Real.exp_le_exp.mpr (neg_le_neg (mul_le_mul_of_nonneg_left hge hs))
      simpa [a, hi, RCLike.norm_ofReal, abs_of_pos (Real.exp_pos _)] using hex
  have hbound := diagonal_norm_bound b (T H s-reading H) a ha
    (Real.exp (-(s*γ))) (Real.exp_pos _).le hab (x-reading H x)
  have hmem : reading H x ∈ H.ker := H.ker.starProjection_apply_mem x
  have hp : reading H (reading H x) = reading H x := Submodule.starProjection_eq_self_iff.mpr hmem
  simpa [map_sub, T_fix_of_mem_ker H s hmem, hp] using hbound

#print axioms diagonal_norm_bound
#print axioms reading_eigen_zero
#print axioms finite_gap_norm_rate
end
end ORDEM016.EquationOfTruth


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
