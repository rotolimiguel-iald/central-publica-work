import TGLExt.F1Fecho394.BosonicTwoParticle
import Mathlib.Analysis.InnerProductSpace.l2Space
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open UniformSpace
open scoped TensorProduct
namespace F1Rede.BosonicSectors
open TGLExt.ImportedSQ F1Rede.BosonicTwoParticle

/-- Recursively bracketed algebraic tensor powers. We complete each entire
power and take the closed span of diagonal pure powers as its symmetric sector.
The permutation-fixed presentation is not identified by a theorem in this file.
The zero algebraic sector is the scalar field. -/
structure PreHilbert where
  carrier : Type
  [instN : NormedAddCommGroup carrier]
  [instI : InnerProductSpace ℂ carrier]
attribute [instance] PreHilbert.instN PreHilbert.instI

def powerData : ℕ → PreHilbert
  | 0 => ⟨ℂ⟩
  | n+1 => ⟨H1 ⊗[ℂ] (powerData n).carrier⟩

abbrev Algebraic (n : ℕ) := (powerData n).carrier

def algebraicGamma (u : H1 ≃ₗᵢ[ℂ] H1) : (n : ℕ) → Algebraic n ≃ₗᵢ[ℂ] Algebraic n
  | 0 => LinearIsometryEquiv.refl ℂ ℂ
  | n+1 => TensorProduct.congrIsometry u (algebraicGamma u n)

def pureAlgebraic (x : H1) : (n : ℕ) → Algebraic n
  | 0 => (1 : ℂ)
  | n+1 => x ⊗ₜ[ℂ] pureAlgebraic x n

@[simp] theorem algebraicGamma_tmul (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : H1) (y : Algebraic n) :
    algebraicGamma u (n+1) (x ⊗ₜ[ℂ] y) = u x ⊗ₜ[ℂ] algebraicGamma u n y := by
  change TensorProduct.congrIsometry u (algebraicGamma u n) (x ⊗ₜ[ℂ] y) = _
  simp

theorem pureAlgebraic_norm (x : H1) (n : ℕ) :
    ‖pureAlgebraic x n‖ = ‖x‖ ^ n := by
  induction n with
  | zero => change ‖(1 : ℂ)‖ = ‖x‖^0; simp
  | succ n ih =>
    change ‖(x ⊗ₜ[ℂ] pureAlgebraic x n : H1 ⊗[ℂ] Algebraic n)‖ = _
    rw [TensorProduct.norm_tmul, ih, pow_succ, mul_comm]

theorem algebraicGamma_pure (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : H1) :
    algebraicGamma u n (pureAlgebraic x n) = pureAlgebraic (u x) n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change algebraicGamma u (n+1) (x ⊗ₜ[ℂ] pureAlgebraic x n) = _
    rw [algebraicGamma_tmul, ih]
    rfl

theorem algebraicGamma_refl (n : ℕ) (x : Algebraic n) :
    algebraicGamma (.refl ℂ H1) n x = x := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change TensorProduct.congrIsometry (.refl ℂ H1) (algebraicGamma (.refl ℂ H1) n) x = x
    induction x using TensorProduct.induction_on with
    | zero => simp
    | tmul x y => simp [ih]
    | add x y hx hy => simp only [map_add, hx, hy]

theorem algebraicGamma_trans (u v : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : Algebraic n) :
    algebraicGamma (u.trans v) n x = algebraicGamma v n (algebraicGamma u n x) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change TensorProduct.congrIsometry (u.trans v) (algebraicGamma (u.trans v) n) x =
      TensorProduct.congrIsometry v (algebraicGamma v n) (TensorProduct.congrIsometry u (algebraicGamma u n) x)
    induction x using TensorProduct.induction_on with
    | zero => simp
    | tmul x y => simp [ih]
    | add x y hx hy => simp only [map_add, hx, hy]

theorem algebraicGamma_inverse (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : Algebraic n) :
    algebraicGamma u.symm n (algebraicGamma u n x) = x := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change TensorProduct.congrIsometry u.symm (algebraicGamma u.symm n)
      (TensorProduct.congrIsometry u (algebraicGamma u n) x) = x
    induction x using TensorProduct.induction_on with
    | zero => simp
    | tmul x y => simp [ih]
    | add x y hx hy => simp only [map_add, hx, hy]

abbrev TensorHilbert (n : ℕ) := Completion (Algebraic n)
def tensorGamma (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) : TensorHilbert n ≃ₗᵢ[ℂ] TensorHilbert n :=
  completionEquiv (algebraicGamma u n)

@[simp] theorem tensorGamma_coe (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : Algebraic n) :
    tensorGamma u n (x : TensorHilbert n) = (algebraicGamma u n x : TensorHilbert n) :=
  completionEquiv_coe _ _

def pureCompleted (n : ℕ) (x : H1) : TensorHilbert n := pureAlgebraic x n
def algebraicSymmetricSpan (n : ℕ) : Submodule ℂ (TensorHilbert n) :=
  Submodule.span ℂ (Set.range (pureCompleted n))
/-- Symmetric tensors are constructed as the closed span of diagonal tensor
powers. No assumed symmetry, density, or unitary action is a field of a contract. -/
def symmetricSpace (n : ℕ) : Submodule ℂ (TensorHilbert n) :=
  (algebraicSymmetricSpan n).topologicalClosure
abbrev Sector (n : ℕ) := symmetricSpace n
instance sectorComplete (n : ℕ) : CompleteSpace (Sector n) :=
  (algebraicSymmetricSpan n).isClosed_topologicalClosure.completeSpace_coe

theorem pureCompleted_mem (n : ℕ) (x : H1) : pureCompleted n x ∈ symmetricSpace n :=
  (algebraicSymmetricSpan n).le_topologicalClosure (Submodule.subset_span ⟨x, rfl⟩)

def pureTensor (n : ℕ) (x : H1) : Sector n := ⟨pureCompleted n x, pureCompleted_mem n x⟩

@[simp] theorem pureTensor_norm (n : ℕ) (x : H1) : ‖pureTensor n x‖ = ‖x‖ ^ n := by
  change ‖(pureAlgebraic x n : Completion (Algebraic n))‖ = _
  rw [Completion.norm_coe, pureAlgebraic_norm]

theorem sector_nontrivial (n : ℕ) : Nontrivial (Sector n) := by
  haveI := AuditF13v31.H1_nontrivial
  obtain ⟨x, hx⟩ := exists_ne (0 : H1)
  refine ⟨⟨pureTensor n x, 0, ?_⟩⟩
  intro h
  have hn := pureTensor_norm n x
  rw [h, norm_zero] at hn
  exact (pow_ne_zero n (norm_ne_zero_iff.mpr hx)) hn.symm

theorem tensorGamma_pure (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : H1) :
    tensorGamma u n (pureCompleted n x) = pureCompleted n (u x) := by
  simp only [pureCompleted, tensorGamma_coe, algebraicGamma_pure]

theorem tensorGamma_mem (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) {x : TensorHilbert n}
    (hx : x ∈ symmetricSpace n) : tensorGamma u n x ∈ symmetricSpace n := by
  let S := symmetricSpace n
  have hbase : algebraicSymmetricSpan n ≤ S.comap (tensorGamma u n).toLinearMap := by
    apply Submodule.span_le.mpr
    rintro _ ⟨y, rfl⟩
    change tensorGamma u n (pureCompleted n y) ∈ S
    rw [tensorGamma_pure]
    exact pureCompleted_mem n (u y)
  have hclosed : IsClosed (S.comap (tensorGamma u n).toLinearMap : Set (TensorHilbert n)) :=
    (algebraicSymmetricSpan n).isClosed_topologicalClosure.preimage (tensorGamma u n).continuous
  exact (algebraicSymmetricSpan n).topologicalClosure_minimal hbase hclosed hx

theorem tensorGamma_inverse (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : TensorHilbert n) :
    tensorGamma u.symm n (tensorGamma u n x) = x := by
  refine Completion.induction_on x (isClosed_eq
    ((tensorGamma u.symm n).continuous.comp (tensorGamma u n).continuous) continuous_id) ?_
  intro a
  simp [algebraicGamma_inverse]

def gammaSector (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) : Sector n ≃ₗᵢ[ℂ] Sector n where
  toFun x := ⟨tensorGamma u n x, tensorGamma_mem u n x.property⟩
  invFun x := ⟨tensorGamma u.symm n x, tensorGamma_mem u.symm n x.property⟩
  left_inv x := by apply Subtype.ext; exact tensorGamma_inverse u n x
  right_inv x := by apply Subtype.ext; simpa using tensorGamma_inverse u.symm n (x : TensorHilbert n)
  map_add' x y := by apply Subtype.ext; exact (tensorGamma u n).map_add x y
  map_smul' c x := by apply Subtype.ext; exact (tensorGamma u n).map_smul c x
  norm_map' x := (tensorGamma u n).norm_map x

@[simp] theorem gammaSector_pure (u : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : H1) :
    gammaSector u n (pureTensor n x) = pureTensor n (u x) := by
  apply Subtype.ext
  exact tensorGamma_pure u n x

theorem tensorGamma_trans (u v : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) (x : TensorHilbert n) :
    tensorGamma (u.trans v) n x = tensorGamma v n (tensorGamma u n x) := by
  refine Completion.induction_on x (isClosed_eq (tensorGamma (u.trans v) n).continuous
    ((tensorGamma v n).continuous.comp (tensorGamma u n).continuous)) ?_
  intro a
  simp [algebraicGamma_trans]

theorem gammaSector_trans (u v : H1 ≃ₗᵢ[ℂ] H1) (n : ℕ) :
    gammaSector (u.trans v) n = (gammaSector u n).trans (gammaSector v n) := by
  ext x
  exact tensorGamma_trans u v n x

theorem gammaSector_refl (n : ℕ) : gammaSector (.refl ℂ H1) n = .refl ℂ (Sector n) := by
  ext x
  change tensorGamma (.refl ℂ H1) n (x : TensorHilbert n) = x
  refine Completion.induction_on (x : TensorHilbert n)
    (isClosed_eq (tensorGamma (.refl ℂ H1) n).continuous continuous_id) ?_
  intro a
  simp [algebraicGamma_refl]

def vacuumSector : Sector 0 := pureTensor 0 (0 : H1)
@[simp] theorem vacuumSector_norm : ‖vacuumSector‖ = 1 := by
  exact (pureTensor_norm 0 (0 : H1)).trans (pow_zero _)
@[simp] theorem gammaSector_vacuum (u : H1 ≃ₗᵢ[ℂ] H1) :
    gammaSector u 0 vacuumSector = vacuumSector := by simp [vacuumSector]

def oneParticleEmbedding : H1 →ₗᵢ[ℂ] Sector 1 where
  toFun x := pureTensor 1 x
  map_add' x y := by
    apply Subtype.ext
    change (Completion.toComplₗᵢ (𝕜 := ℂ)) ((x+y) ⊗ₜ[ℂ] (1:ℂ)) =
      (Completion.toComplₗᵢ (𝕜 := ℂ)) (x ⊗ₜ[ℂ] (1:ℂ)) +
      (Completion.toComplₗᵢ (𝕜 := ℂ)) (y ⊗ₜ[ℂ] (1:ℂ))
    rw [TensorProduct.add_tmul, map_add]
  map_smul' c x := by
    apply Subtype.ext
    change (Completion.toComplₗᵢ (𝕜 := ℂ)) ((c • x) ⊗ₜ[ℂ] (1:ℂ)) =
      c • (Completion.toComplₗᵢ (𝕜 := ℂ)) (x ⊗ₜ[ℂ] (1:ℂ))
    rw [← TensorProduct.smul_tmul', map_smul]
  norm_map' x := by exact (pureTensor_norm 1 x).trans (pow_one _)

theorem gammaSector_oneParticle (u : H1 ≃ₗᵢ[ℂ] H1) (x : H1) :
    gammaSector u 1 (oneParticleEmbedding x) = oneParticleEmbedding (u x) :=
  gammaSector_pure u 1 x

end F1Rede.BosonicSectors

#print axioms F1Rede.BosonicSectors.gammaSector
#print axioms F1Rede.BosonicSectors.gammaSector_trans
#print axioms F1Rede.BosonicSectors.gammaSector_refl
#print axioms F1Rede.BosonicSectors.sector_nontrivial
#print axioms F1Rede.BosonicSectors.oneParticleEmbedding
#print axioms F1Rede.BosonicSectors.gammaSector_oneParticle
#print axioms F1Rede.BosonicSectors.gammaSector_vacuum

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
