import Mathlib.Analysis.InnerProductSpace.l2Space
/-! The Hilbert sum and diagonal functor of an actual family of complete Hilbert
sectors. No assertion here supplies the bosonic sectors or Weyl algebras. Those
must be constructed separately before specializing this reusable operation. -/
set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section
open scoped ENNReal InnerProductSpace

namespace F1Rede.SectorDirectSum
variable {E : ℕ → Type*} [∀ n, NormedAddCommGroup (E n)]
  [∀ n, InnerProductSpace ℂ (E n)] [∀ n, CompleteSpace (E n)]

abbrev SumSpace (E : ℕ → Type*) [∀ n, NormedAddCommGroup (E n)] := lp E 2

def diagonalFun (u : ∀ n, E n ≃ₗᵢ[ℂ] E n) (f : SumSpace E) : SumSpace E :=
  ⟨fun n => u n (f n), Memℓp.mono (lp.memℓp f).norm (fun n => by simp)⟩

@[simp] theorem diagonalFun_apply (u : ∀ n, E n ≃ₗᵢ[ℂ] E n)
    (f : SumSpace E) (n : ℕ) : diagonalFun u f n = u n (f n) := rfl

/-- Componentwise unitary action on the completed Hilbert sum. -/
def diagonal (u : ∀ n, E n ≃ₗᵢ[ℂ] E n) : SumSpace E ≃ₗᵢ[ℂ] SumSpace E where
  toFun := diagonalFun u
  invFun := diagonalFun (fun n => (u n).symm)
  left_inv f := by ext n; simp
  right_inv f := by ext n; simp
  map_add' f g := by ext n; simp [diagonalFun]
  map_smul' c f := by ext n; simp [diagonalFun]
  norm_map' f := by
    rw [lp.norm_eq_tsum_rpow (by norm_num : 0 < (2 : ℝ≥0∞).toReal),
      lp.norm_eq_tsum_rpow (by norm_num : 0 < (2 : ℝ≥0∞).toReal)]
    simp

@[simp] theorem diagonal_apply (u : ∀ n, E n ≃ₗᵢ[ℂ] E n)
    (f : SumSpace E) (n : ℕ) : diagonal u f n = u n (f n) := rfl

theorem diagonal_refl :
    diagonal (fun n => LinearIsometryEquiv.refl ℂ (E n)) =
      LinearIsometryEquiv.refl ℂ (SumSpace E) := by
  ext f n
  rfl

theorem diagonal_trans (u v : ∀ n, E n ≃ₗᵢ[ℂ] E n) :
    diagonal (fun n => (u n).trans (v n)) = (diagonal u).trans (diagonal v) := by
  ext f n
  rfl

/-- Isometric inclusion of each genuine particle sector. -/
def sectorEmbedding (n : ℕ) : E n →ₗᵢ[ℂ] SumSpace E where
  toLinearMap := lp.lsingle 2 n
  norm_map' x := lp.norm_single (by norm_num) n x

@[simp] theorem sectorEmbedding_apply (n : ℕ) (x : E n) :
    sectorEmbedding n x = lp.single 2 n x := rfl

theorem diagonal_single (u : ∀ n, E n ≃ₗᵢ[ℂ] E n) (n : ℕ) (x : E n) :
    diagonal u (sectorEmbedding n x) = sectorEmbedding n (u n x) := by
  ext k
  by_cases h : k = n
  · subst k; simp
  · simp [lp.single_apply_ne, h]

theorem vacuum_fixed (u : ∀ n, E n ≃ₗᵢ[ℂ] E n) (e : E 0)
    (he : u 0 e = e) : diagonal u (sectorEmbedding 0 e) = sectorEmbedding 0 e := by
  rw [diagonal_single, he]

theorem vacuum_norm (e : E 0) (he : ‖e‖ = 1) : ‖sectorEmbedding 0 e‖ = 1 := by
  rw [(sectorEmbedding 0).norm_map, he]

theorem different_sectors_orthogonal (n m : ℕ) (hnm : n ≠ m) (x : E n) (y : E m) :
    ⟪sectorEmbedding n x, sectorEmbedding m y⟫_ℂ = 0 := by
  rw [sectorEmbedding_apply, sectorEmbedding_apply, lp.inner_single_left]
  simp [lp.single_apply_ne, hnm]

end F1Rede.SectorDirectSum

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
