import Lean
import TGLExt.O16.ContratoQG_v31_Minimal
set_option autoImplicit false
noncomputable section
open scoped InnerProductSpace
namespace ChatgptAudit.FirstOrderReuse016
open Complex TGLExt.ContratoQGv31 TGL.SpecificAQFT TGL.ModularRealization
variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W} {N : KillingNormalization}

theorem Δit_vac (C : ContratoH2 W R N) (t : ℝ) : C.Δit t W.vac = W.vac := by
  rw [C.bw]; exact C.boost.V_vac _

theorem inner_vac_Δit (C : ContratoH2 W R N) (t : ℝ) (φ : W.H) :
    ⟪W.vac, C.Δit t φ⟫_ℂ = ⟪W.vac, φ⟫_ℂ := by
  have h := (C.Δit t).inner_map_map W.vac φ
  rw [Δit_vac] at h
  exact h

theorem bilateral_no_first_order (C : ContratoH2 W R N) {φ : W.H} {k : ℝ}
    (hk : HasModularEnergy C.Δit φ k) (ε : ℝ) :
    HasModularEnergy C.Δit (W.vac + (ε : ℂ) • φ) (ε ^ 2 * k) := by
  unfold HasModularEnergy at hk ⊢
  have hfun : (fun t : ℝ => ⟪W.vac + (ε : ℂ) • φ, C.Δit t (W.vac + (ε : ℂ) • φ)⟫_ℂ)
      = fun t : ℝ => (⟪W.vac, W.vac⟫_ℂ + (ε : ℂ) * ⟪W.vac, φ⟫_ℂ + (ε : ℂ) * ⟪φ, W.vac⟫_ℂ)
          + ((ε : ℂ) ^ 2) * ⟪φ, C.Δit t φ⟫_ℂ := by
    funext t
    rw [map_add, map_smul, Δit_vac, inner_add_left, inner_add_right, inner_add_right,
      inner_smul_left, inner_smul_left, inner_smul_right, inner_smul_right, inner_vac_Δit]
    simp only [Complex.conj_ofReal]
    ring
  rw [hfun]
  have h2 := (hk.const_mul ((ε : ℂ) ^ 2)).const_add
    (⟪W.vac, W.vac⟫_ℂ + (ε : ℂ) * ⟪W.vac, φ⟫_ℂ + (ε : ℂ) * ⟪φ, W.vac⟫_ℂ)
  refine h2.congr_deriv ?_
  push_cast
  ring

#print axioms Δit_vac
#print axioms inner_vac_Δit
#print axioms bilateral_no_first_order
end ChatgptAudit.FirstOrderReuse016


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
