import TGLExt.F1Fecho394.RegularCoreFixedR3
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.RegularCoreConjugation
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem regular_conjugation_eq_fibre (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (M : VonNeumannAlgebra H) (t : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : A ∈ F1Fecho.RegularCovariantCore.core B M) :
    star (F1Fecho.RegularCovariantCore.regularUnitary B t) * A * F1Fecho.RegularCovariantCore.regularUnitary B t =
      star (fibre (F1Fecho.RegularCovariantCore.boostCLM B t)) * A *
      fibre (F1Fecho.RegularCovariantCore.boostCLM B t) := by
  have hs : shift (-t) * A = A * shift (-t) :=
    ((VonNeumannAlgebra.mem_commutant_iff.mp
      (F1Fecho.RegularCoreFixed.shift_mem_regularCommutant B M (-t))) A hA).symm
  rw [F1Fecho.RegularCovariantCore.regular_star]
  unfold F1Fecho.RegularCovariantCore.regularUnitary
  rw [← fibre_star,F1Fecho.RegularCovariantCore.boostCLM_star]
  calc
    _ = fibre (F1Fecho.RegularCovariantCore.boostCLM B (-t)) * (shift (-t) * A) *
        (fibre (F1Fecho.RegularCovariantCore.boostCLM B t) * shift t) := by simp only [mul_assoc]
    _ = fibre (F1Fecho.RegularCovariantCore.boostCLM B (-t)) * A *
        (shift (-t) * fibre (F1Fecho.RegularCovariantCore.boostCLM B t)) * shift t := by
      rw [hs]
      simp only [mul_assoc]
    _ = (fibre (F1Fecho.RegularCovariantCore.boostCLM B (-t)) * A *
         fibre (F1Fecho.RegularCovariantCore.boostCLM B t)) * (shift (-t) * shift t) := by
      rw [shift_commutes_fibre (-t) (F1Fecho.RegularCovariantCore.boostCLM B t)]
      simp only [mul_assoc]
    _ = _ := by rw [shift_mul (H := H) (-t) t, neg_add_cancel, shift_zero, mul_one]


end F1Fecho.RegularCoreConjugation
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.RegularCoreConjugation).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
