import Lean
import TGLExt.O16.ModularBoostEnergyReuse_v2

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.ModularCharge016
open TGLExt.ContratoQGv31 TGL.SpecificAQFT TGL.ModularRealization MeasureTheory Matrix
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

/-- The exact unresolved contract field, explicitly named, not discharged by naming it. -/
def ModularChargeLink (C : ContratoH2 W R N) (T : StressTensorData W) (A : Set W.H) : Prop :=
  ∀ ψ ∈ A, ∀ k : ℝ, HasModularEnergy C.Δit ψ k →
    k = 2 * Real.pi * nullPlaneCharge T ψ

/-- A sufficient link from the chosen stress tensor to the actual boost expectation.
The hypothesis includes existence of this derivative for every admissible state. -/
theorem modular_charge_of_boost_charge (C : ContratoH2 W R N)
    (T : StressTensorData W) (A : Set W.H)
    (hboost : ∀ ψ ∈ A, HasBoostEnergy C.boost.V ψ (nullPlaneCharge T ψ)) :
    ModularChargeLink C T A := by
  intro ψ hψ k hk
  exact modularEnergy_unique hk (modularEnergy_of_boostEnergy C (hboost ψ hψ))

/-- This tensor meets only the weak vacuum/covariance type, not physical stress claims. -/
def zeroTensor (W : TGLSpecificAQFTWitness) : StressTensorData W where
  T := fun _ _ => 0
  T_vac := fun _ => rfl
  T_covariant := fun _ _ _ => rfl

theorem zero_tensor_charge (ψ : W.H) : nullPlaneCharge (zeroTensor W) ψ = 0 := by
  simp [nullPlaneCharge,nullEnergy,pairing,zeroTensor]

/-- Thus H2 together with the weak tensor type does not supply the link
for arbitrary tensors on a class with a nonzero modular energy witness. -/
theorem zero_tensor_rejects_nonzero_modular_energy (C : ContratoH2 W R N) (A : Set W.H)
    (hn : ∃ ψ ∈ A, ∃ k : ℝ, HasModularEnergy C.Δit ψ k ∧ k ≠ 0) :
    ¬ ModularChargeLink C (zeroTensor W) A := by
  intro hlink
  obtain ⟨ψ,hψ,k,hk,hne⟩ := hn
  have he := hlink ψ hψ k hk
  rw [zero_tensor_charge,mul_zero] at he
  exact hne he

#print axioms modular_charge_of_boost_charge
#print axioms zero_tensor_charge
#print axioms zero_tensor_rejects_nonzero_modular_energy
end ChatgptAudit.ModularCharge016


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
