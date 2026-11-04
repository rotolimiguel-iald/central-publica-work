import Lean
import TGLExt.O16.ContratoQG_v31_Minimal
set_option autoImplicit false
noncomputable section
open scoped InnerProductSpace
namespace ChatgptAudit.ModularCharge016
open Complex TGLExt.ContratoQGv31 TGL.SpecificAQFT TGL.ModularRealization
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}
theorem modularEnergy_of_boostEnergy (C : ContratoH2 W R N) {ψ : W.H} {b : ℝ}
    (h : HasBoostEnergy C.boost.V ψ b) : HasModularEnergy C.Δit ψ (2 * Real.pi * b) := by
  unfold HasBoostEnergy at h
  unfold HasModularEnergy
  have hg : HasDerivAt (fun t : ℝ => -(2 * Real.pi * t)) (-(2 * Real.pi)) 0 := by
    have h0 := (hasDerivAt_id (0:ℝ)).const_mul (-(2 * Real.pi))
    have e : (fun t : ℝ => -(2 * Real.pi * t)) = (fun y : ℝ => -(2 * Real.pi) * id y) := by
      funext t; simp [id]
    rw [e]
    exact h0.congr_deriv (by ring)
  have h' : HasDerivAt (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) (I * (b : ℂ)) (-(2 * Real.pi * 0)) := by
    simpa using h
  have hc := h'.scomp (0:ℝ) hg
  have hfun : (fun t : ℝ => ⟪ψ, C.Δit t ψ⟫_ℂ)
      = (fun s : ℝ => ⟪ψ, C.boost.V s ψ⟫_ℂ) ∘ (fun t : ℝ => -(2 * Real.pi * t)) := by
    funext t
    simp only [Function.comp, C.bw]
  rw [hfun]
  refine hc.congr_deriv ?_
  rw [Complex.real_smul]
  push_cast
  ring

theorem modularEnergy_unique {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {D : ℝ → (H ≃ₗᵢ[ℂ] H)} {ψ : H} {k k' : ℝ}
    (h : HasModularEnergy D ψ k) (h' : HasModularEnergy D ψ k') : k = k' := by
  have hu := h.unique h'
  have hI : I * (k : ℂ) = I * (k' : ℂ) := neg_inj.mp hu
  have : (k : ℂ) = k' := mul_left_cancel₀ Complex.I_ne_zero hI
  exact_mod_cast this

#print axioms modularEnergy_of_boostEnergy
#print axioms modularEnergy_unique
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
