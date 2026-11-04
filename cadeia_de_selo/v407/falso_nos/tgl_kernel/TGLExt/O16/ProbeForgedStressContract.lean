import Lean
import TGLExt.O16.ContratoQG_v31_Minimal
import TGLExt.O16.ProbeForgedStress_v2

set_option autoImplicit false
set_option maxHeartbeats 1000000

/-!
A-1.b2, conditional attack on the actual v3.1 definitions (unchanged body,
import-only variant). A supplied H3 and symmetric source are hypotheses;
this file does not construct a physical H2/H3 or claim nonvacuity.
The attack disproves enforcement of symmetry, not spacelike locality itself.
-/
namespace ChatgptAudit.ForgedStressContract
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ContratoQGv31
open TGLExt ChatgptAudit.ForgedStress MeasureTheory Matrix
noncomputable section

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
  {N : KillingNormalization}

def forgedTensor (T : StressTensorData W) : StressTensorData W where
  T := fun ψ x => forge (T.T ψ x) (nullEnergy T ψ x)
  T_vac := by
    intro x
    ext i j
    simp [forge, transverseSkew, nullEnergy, pairing, T.T_vac]
  T_covariant := by
    intro a ψ x
    simp only [nullEnergy, T.T_covariant]

theorem forged_nullEnergy (T : StressTensorData W) (ψ : W.H) (x : Fin 4 → ℝ) :
    nullEnergy (forgedTensor T) ψ x = nullEnergy T ψ x := by
  change nullRead (forge (T.T ψ x) (nullEnergy T ψ x)) = nullRead (T.T ψ x)
  exact forge_preserves_nullRead _ _

theorem forged_nullPlaneCharge (T : StressTensorData W) (ψ : W.H) :
    nullPlaneCharge (forgedTensor T) ψ = nullPlaneCharge T ψ := by
  simp only [nullPlaneCharge, forged_nullEnergy]

def symSource (f : (Fin 4 → ℝ) → Tensor) : (Fin 4 → ℝ) → Tensor :=
  fun x => symmetrize (f x)

theorem symSource_zero : symSource 0 = 0 := by
  funext x i j
  simp [symSource, symmetrize]

theorem symSource_forged (T : StressTensorData W)
    (hsym : ∀ ψ x, (T.T ψ x).transpose = T.T ψ x) (ψ : W.H) :
    symSource ((forgedTensor T).T ψ) = T.T ψ := by
  funext x
  exact (symmetrize_forge _ _).trans (symmetrize_of_symmetric _ (hsym ψ x))

def transportH3 {T : StressTensorData W} (C : ContratoH3 W R N T)
    (hsym : ∀ ψ x, (T.T ψ x).transpose = T.T ψ x) :
    ContratoH3 W R N (forgedTensor T) where
  H2 := C.H2
  G := C.G
  G_pos := C.G_pos
  admissible := C.admissible
  admissible_unit := C.admissible_unit
  vac_admissible := C.vac_admissible
  admissible_translate := C.admissible_translate
  modular_charge := by
    intro ψ hψ k hk
    simpa only [forged_nullPlaneCharge] using C.modular_charge ψ hψ k hk
  admissible_nontrivial := C.admissible_nontrivial
  energy_continuous := by
    intro ψ hψ x
    simpa only [forged_nullEnergy] using C.energy_continuous ψ hψ x
  background_screen_flat := C.background_screen_flat
  propagator := fun f => C.propagator (symSource f)
  propagator_zero := by rw [symSource_zero, C.propagator_zero]
  propagator_covariant := by
    intro a f
    exact C.propagator_covariant a (symSource f)
  response_symm := by
    intro ψ hψ x
    rw [symSource_forged T hsym ψ]
    exact C.response_symm ψ hψ x
  lightcone_gauge := by
    intro ψ hψ x
    rw [symSource_forged T hsym ψ]
    exact C.lightcone_gauge ψ hψ x
  theta := C.theta
  theta_is_expansion := by
    intro ψ hψ x
    rw [symSource_forged T hsym ψ]
    exact C.theta_is_expansion ψ hψ x
  raychaudhuri_einstein := by
    intro ψ hψ x
    simpa only [forged_nullEnergy] using C.raychaudhuri_einstein ψ hψ x

theorem same_response {T : StressTensorData W} (C : ContratoH3 W R N T)
    (hsym : ∀ ψ x, (T.T ψ x).transpose = T.T ψ x) (ψ : W.H) :
    (transportH3 C hsym).response ψ = C.response ψ := by
  change C.propagator (symSource ((forgedTensor T).T ψ)) = C.propagator (T.T ψ)
  rw [symSource_forged T hsym ψ]

theorem forgery_has_nonsymmetric_admissible_value {T : StressTensorData W}
    (C : ContratoH3 W R N T) (hsym : ∀ ψ x, (T.T ψ x).transpose = T.T ψ x) :
    ∃ ψ ∈ C.admissible, ∃ x : Fin 4 → ℝ,
      ((forgedTensor T).T ψ x).transpose ≠ (forgedTensor T).T ψ x := by
  obtain ⟨ψ, hψ, k, hk, hk0⟩ := C.admissible_nontrivial
  have hex : ∃ x : Fin 4 → ℝ, nullEnergy T ψ x ≠ 0 := by
    by_contra! hn
    have hz : nullPlaneCharge T ψ = 0 := by simp [nullPlaneCharge, hn]
    have he := C.modular_charge ψ hψ k hk
    rw [hz, mul_zero] at he
    exact hk0 he
  obtain ⟨x, hx⟩ := hex
  exact ⟨ψ, hψ, x, forge_not_symmetric _ (hsym ψ x) _ hx⟩

#print axioms forgedTensor
#print axioms forged_nullEnergy
#print axioms forged_nullPlaneCharge
#print axioms symSource_zero
#print axioms symSource_forged
#print axioms transportH3
#print axioms same_response
#print axioms forgery_has_nonsymmetric_admissible_value
end
end ChatgptAudit.ForgedStressContract


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
