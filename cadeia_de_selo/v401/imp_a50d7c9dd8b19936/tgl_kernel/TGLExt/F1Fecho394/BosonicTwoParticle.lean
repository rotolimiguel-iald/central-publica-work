import TGLExt.LightNetStandardWedgeDataBGL
import Mathlib.Analysis.InnerProductSpace.TensorProduct
import Mathlib.Analysis.InnerProductSpace.Completion
import Mathlib.Analysis.Normed.Operator.Extend
/-!
Concrete first bosonic sector on the canonical v392 H1. The algebraic tensor
product is completed, and the two-particle space is the closed fixed subspace
of the flip. Unitaries act by the completed tensor square, restricted to that
subspace. This constructs an actual sector, not a FockCertificate, Weyl net,
Maxwell field, or general second-quantization theorem.
-/
set_option autoImplicit false
set_option maxHeartbeats 600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open scoped TensorProduct
open UniformSpace
namespace F1Rede.BosonicTwoParticle
open TGLExt.ImportedSQ

section CompletionEquiv
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]

def completionEquiv (u : E ≃ₗᵢ[ℂ] F) : Completion E ≃ₗᵢ[ℂ] Completion F :=
  u.toLinearEquiv.extendOfIsometry
    (Completion.toComplₗᵢ (𝕜 := ℂ) (E := E)).toLinearMap
    (Completion.toComplₗᵢ (𝕜 := ℂ) (E := F)).toLinearMap
    Completion.denseRange_coe Completion.denseRange_coe
    (fun x => by simp)

@[simp] theorem completionEquiv_coe (u : E ≃ₗᵢ[ℂ] F) (x : E) :
    completionEquiv u (x : Completion E) = (u x : Completion F) := by
  exact LinearEquiv.extendOfIsometry_eq _ _ _ _ _ _ x
end CompletionEquiv

abbrev AlgebraicTwo := H1 ⊗[ℂ] H1
abbrev CompletedTwo := Completion AlgebraicTwo

def flip : CompletedTwo ≃ₗᵢ[ℂ] CompletedTwo :=
  completionEquiv (TensorProduct.commIsometry ℂ H1 H1)

@[simp] theorem flip_coe (x : AlgebraicTwo) :
    flip (x : CompletedTwo) = (TensorProduct.comm ℂ H1 H1 x : CompletedTwo) := by
  simp [flip]

@[simp] theorem flip_flip (x : CompletedTwo) : flip (flip x) = x := by
  refine Completion.induction_on x (isClosed_eq (flip.continuous.comp flip.continuous) continuous_id) ?_
  intro a
  simp

def symmetricSector : Submodule ℂ CompletedTwo where
  carrier := {x | flip x = x}
  zero_mem' := by simp
  add_mem' := by intro x y hx hy; simp only [Set.mem_setOf_eq] at *; simp [hx, hy]
  smul_mem' := by intro c x hx; simp only [Set.mem_setOf_eq] at *; simp [hx]

@[simp] theorem mem_symmetricSector (x : CompletedTwo) :
    x ∈ symmetricSector ↔ flip x = x := Iff.rfl

theorem symmetricSector_closed : IsClosed (symmetricSector : Set CompletedTwo) :=
  isClosed_eq flip.continuous continuous_id

instance : CompleteSpace symmetricSector :=
  symmetricSector_closed.completeSpace_coe

def pair (x : H1) : symmetricSector :=
  ⟨((x ⊗ₜ[ℂ] x : AlgebraicTwo) : CompletedTwo), by simp⟩

@[simp] theorem pair_norm (x : H1) : ‖pair x‖ = ‖x‖ * ‖x‖ := by
  simp [pair]

theorem pair_ne_zero {x : H1} (hx : x ≠ 0) : pair x ≠ 0 := by
  intro h
  have hnorm := pair_norm x
  rw [h, norm_zero] at hnorm
  exact (mul_ne_zero (norm_ne_zero_iff.mpr hx) (norm_ne_zero_iff.mpr hx)) hnorm.symm

theorem symmetricSector_nontrivial : Nontrivial symmetricSector := by
  haveI := AuditF13v31.H1_nontrivial
  obtain ⟨x, hx⟩ := exists_ne (0 : H1)
  exact ⟨⟨pair x, 0, pair_ne_zero hx⟩⟩

def tensorSquare (u : H1 ≃ₗᵢ[ℂ] H1) : CompletedTwo ≃ₗᵢ[ℂ] CompletedTwo :=
  completionEquiv (TensorProduct.congrIsometry u u)

@[simp] theorem tensorSquare_coe (u : H1 ≃ₗᵢ[ℂ] H1) (x : AlgebraicTwo) :
    tensorSquare u (x : CompletedTwo) =
      (TensorProduct.congr u.toLinearEquiv u.toLinearEquiv x : CompletedTwo) := by
  rw [tensorSquare, completionEquiv_coe]
  rfl

theorem tensorSquare_flip (u : H1 ≃ₗᵢ[ℂ] H1) (x : CompletedTwo) :
    tensorSquare u (flip x) = flip (tensorSquare u x) := by
  refine Completion.induction_on x (isClosed_eq
    ((tensorSquare u).continuous.comp flip.continuous)
    (flip.continuous.comp (tensorSquare u).continuous)) ?_
  intro a
  simp only [flip_coe, tensorSquare_coe]
  congr 1
  induction a using TensorProduct.induction_on with
  | zero => simp
  | tmul x y => simp
  | add x y hx hy => simp only [map_add, hx, hy]

theorem tensorSquare_mem (u : H1 ≃ₗᵢ[ℂ] H1) {x : CompletedTwo}
    (hx : x ∈ symmetricSector) : tensorSquare u x ∈ symmetricSector := by
  rw [mem_symmetricSector] at hx ⊢
  rw [← tensorSquare_flip, hx]

theorem tensorSquare_inverse (u : H1 ≃ₗᵢ[ℂ] H1) (x : CompletedTwo) :
    tensorSquare u.symm (tensorSquare u x) = x := by
  refine Completion.induction_on x (isClosed_eq
    ((tensorSquare u.symm).continuous.comp (tensorSquare u).continuous) continuous_id) ?_
  intro a
  simp only [tensorSquare_coe]
  congr 1
  induction a using TensorProduct.induction_on with
  | zero => simp
  | tmul x y => simp
  | add x y hx hy => simp only [map_add, hx, hy]

def gammaTwo (u : H1 ≃ₗᵢ[ℂ] H1) : symmetricSector ≃ₗᵢ[ℂ] symmetricSector where
  toFun x := ⟨tensorSquare u x, tensorSquare_mem u x.property⟩
  invFun x := ⟨tensorSquare u.symm x, tensorSquare_mem u.symm x.property⟩
  left_inv x := by apply Subtype.ext; exact tensorSquare_inverse u x
  right_inv x := by apply Subtype.ext; simpa using tensorSquare_inverse u.symm (x : CompletedTwo)
  map_add' x y := by apply Subtype.ext; exact (tensorSquare u).map_add x y
  map_smul' c x := by apply Subtype.ext; exact (tensorSquare u).map_smul c x
  norm_map' x := (tensorSquare u).norm_map x

@[simp] theorem gammaTwo_pair (u : H1 ≃ₗᵢ[ℂ] H1) (x : H1) :
    gammaTwo u (pair x) = pair (u x) := by
  apply Subtype.ext
  change tensorSquare u ((x ⊗ₜ[ℂ] x : AlgebraicTwo) : CompletedTwo) = _
  simp [pair]

theorem tensorSquare_trans (u v : H1 ≃ₗᵢ[ℂ] H1) (x : CompletedTwo) :
    tensorSquare (u.trans v) x = tensorSquare v (tensorSquare u x) := by
  refine Completion.induction_on x (isClosed_eq
    (tensorSquare (u.trans v)).continuous
    ((tensorSquare v).continuous.comp (tensorSquare u).continuous)) ?_
  intro a
  simp only [tensorSquare_coe]
  congr 1
  induction a using TensorProduct.induction_on with
  | zero => simp
  | tmul x y => simp
  | add x y hx hy => simp only [map_add, hx, hy]

theorem gammaTwo_trans (u v : H1 ≃ₗᵢ[ℂ] H1) :
    gammaTwo (u.trans v) = (gammaTwo u).trans (gammaTwo v) := by
  ext x
  exact tensorSquare_trans u v x

theorem gammaTwo_refl : gammaTwo (.refl ℂ H1) = .refl ℂ symmetricSector := by
  ext x
  change tensorSquare (.refl ℂ H1) (x : CompletedTwo) = x
  refine Completion.induction_on (x : CompletedTwo)
    (isClosed_eq (tensorSquare (.refl ℂ H1)).continuous continuous_id) ?_
  intro a
  simp [tensorSquare, TensorProduct.congrIsometry_refl_refl]

end F1Rede.BosonicTwoParticle

#print axioms F1Rede.BosonicTwoParticle.symmetricSector_nontrivial
#print axioms F1Rede.BosonicTwoParticle.gammaTwo_trans
#print axioms F1Rede.BosonicTwoParticle.gammaTwo_refl
#print axioms F1Rede.BosonicTwoParticle.gammaTwo_pair

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
