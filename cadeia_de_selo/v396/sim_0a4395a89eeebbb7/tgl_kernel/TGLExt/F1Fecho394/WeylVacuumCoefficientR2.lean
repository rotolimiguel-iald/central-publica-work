import TGLExt.F1Fecho394.FieldWeylR3
/-! Actual vacuum matrix coefficient on the canonical Fock space.  The unitary
is second quantized by the existing construction; no correlation formula is
assumed.  The field convention is W(f)=D(i f), with no sqrt(2) rescaling. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.WeylVacuumCoefficient
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.WeylCoefficients F1Fecho.FieldWeyl

theorem rotate_norm (f : H1) : ‖rotate f‖ = ‖f‖ := by
  simp [rotate, norm_smul]

theorem rotate_unitary (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) :
    u (rotate f) = rotate (u f) := by
  exact u.map_smul Complex.I f

theorem vacuum_two_weyl (u : H1 ≃ₗᵢ[ℂ] H1) (f g : H1) :
    inner ℂ vacuum (W f (gamma u (W g vacuum))) =
      Complex.exp (-((‖f‖ : ℂ)^2)/2 - ((‖g‖ : ℂ)^2)/2 - inner ℂ f (u g)) := by
  rw [W_vacuum, map_smul, gamma_exponential, rotate_unitary]
  change inner ℂ vacuum
    (F1Fecho.ConcreteWeyl.W (rotate f)
      (amplitude (rotate g) 0 • exponential (rotate (u g)))) = _
  rw [map_smul, F1Fecho.ConcreteWeyl.W_exponential, inner_smul_right,
    inner_smul_right, ← exponential_zero, exponential_inner, inner_zero_left,
    Complex.exp_zero, mul_one, amplitude_norm_form, amplitude_norm_form,
    inner_zero_right, rotate_inner, rotate_norm, rotate_norm]
  rw [← Complex.exp_add]
  congr 1
  ring

theorem vacuum_two_weyl_identity (f g : H1) :
    inner ℂ vacuum (W f (W g vacuum)) =
      Complex.exp (-((‖f‖ : ℂ)^2)/2 - ((‖g‖ : ℂ)^2)/2 - inner ℂ f g) := by
  simpa only [gamma_refl, LinearIsometryEquiv.coe_refl, id_eq] using
    vacuum_two_weyl (LinearIsometryEquiv.refl ℂ H1) f g

end F1Fecho.WeylVacuumCoefficient

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.WeylVacuumCoefficient).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
