import TGLExt.F1Fecho394.BosonicFock
/-! Concrete translations and the canonical one-parameter wedge boosts on the
bosonic Hilbert space. Functoriality transports the existing H1 group laws and
boost/translation covariance. Strong continuity, positive energy, CCR and local
algebras are separate obligations and are not claimed in this file. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section

namespace F1Rede.BosonicFockGroupActions
open TGLExt.ImportedSQ F1Rede.BosonicFock
open TGLExt.ContratoQGv31
open ChatgptAudit.WignerGeometry016

def UF (a : Fin 4 → ℝ) : F ≃ₗᵢ[ℂ] F := gamma (U1 a)
def VF (s : ℝ) : F ≃ₗᵢ[ℂ] F := gamma (B0 s)

theorem gamma_symm (u : H1 ≃ₗᵢ[ℂ] H1) : gamma u.symm = (gamma u).symm := by
  have h := gamma_trans u u.symm
  rw [LinearIsometryEquiv.self_trans_symm, gamma_refl] at h
  apply LinearIsometryEquiv.ext
  intro f
  have hf := congrArg (fun e : F ≃ₗᵢ[ℂ] F => e ((gamma u).symm f)) h
  simp only [LinearIsometryEquiv.coe_trans, Function.comp_apply,
    LinearIsometryEquiv.apply_symm_apply] at hf
  exact hf.symm

theorem UF_zero : UF 0 = LinearIsometryEquiv.refl ℂ F := by
  rw [UF, U1_zero, gamma_refl]

theorem UF_add (a b : Fin 4 → ℝ) : UF (a + b) = (UF b).trans (UF a) := by
  unfold UF
  rw [U1_add, gamma_trans]

theorem UF_neg (a : Fin 4 → ℝ) : UF (-a) = (UF a).symm := by
  unfold UF
  rw [U1_neg, gamma_symm]

theorem VF_zero : VF 0 = LinearIsometryEquiv.refl ℂ F := by
  rw [VF, B0_zero, gamma_refl]

theorem VF_add (s t : ℝ) : VF (s + t) = (VF t).trans (VF s) := by
  unfold VF
  rw [B0_add, gamma_trans]

theorem UF_vacuum (a : Fin 4 → ℝ) : UF a vacuum = vacuum := gamma_vacuum (U1 a)
theorem VF_vacuum (s : ℝ) : VF s vacuum = vacuum := gamma_vacuum (B0 s)

theorem UF_oneParticle (a : Fin 4 → ℝ) (x : H1) :
    UF a (oneParticle x) = oneParticle (U1 a x) := gamma_oneParticle (U1 a) x

theorem VF_oneParticle (s : ℝ) (x : H1) :
    VF s (oneParticle x) = oneParticle (B0 s x) := gamma_oneParticle (B0 s) x

theorem VF_conjugates_UF (s : ℝ) (a : Fin 4 → ℝ) :
    ((VF s).symm.trans (UF a)).trans (VF s) = UF (wedgeBoostMap s a) := by
  have hB : U1 (wedgeBoostMap s a) = (((B0 s).symm).trans (U1 a)).trans (B0 s) := by
    apply LinearIsometryEquiv.ext
    intro f
    have h := congrArg (fun T : H1 →L[ℂ] H1 => T f) (B0_conj s a)
    simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply] at h
    exact h.symm
  unfold UF VF
  rw [hB, gamma_trans, gamma_trans, gamma_symm]

theorem VF_UF_VF_symm (s : ℝ) (a : Fin 4 → ℝ) (f : F) :
    VF s (UF a ((VF s).symm f)) = UF (wedgeBoostMap s a) f := by
  exact congrArg (fun e : F ≃ₗᵢ[ℂ] F => e f) (VF_conjugates_UF s a)

end F1Rede.BosonicFockGroupActions

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
