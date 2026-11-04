import TGLExt.F1Fecho394.RegularCovariantCoreR3
import TGLExt.F1Fecho394.CanonicalWedgeFlowR2
import TGLExt.F1Fecho394.BosonicFockContinuity

/-!
The represented regular core of the concrete canonical Weyl wedge on the SAME
bosonic Fock space. The unitary flow is actually constructed as Gamma(B0(-2 pi t)).
Its restriction to R(KWR) is the already proved CanonicalWedgeFlow.flow. There
is no hypothetical LightNetData or FockCertificate in these constructions.
The algebra is the bicommutant generated on L2(R; Fock) by fibre R(KWR) and
regular unitaries. A faithful embedding, covariance and the dual character
action are provided. This is not a trace, a proof that the boost flow is the
vacuum modular group, an equivalence with the V351 tower core, or full duality.
-/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.CanonicalFockRegular
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open TGLV350.Regular

def fockFlow : F1Fecho.RegularCovariantCore.UnitaryFlow F where
  U t := gamma (B0 (-(2*Real.pi*t)))
  zero := by simp only [mul_zero,neg_zero,B0_zero,gamma_refl]
  add s t := by
    rw [show -(2*Real.pi*(s+t)) = -(2*Real.pi*s) + -(2*Real.pi*t) by ring,
      B0_add,gamma_trans]
  strong v := (boosts_strong v).comp (continuous_const.mul continuous_id |>.neg)

theorem fockFlow_inhabited : Nonempty (F1Fecho.RegularCovariantCore.UnitaryFlow F) := ⟨fockFlow⟩

abbrev M := F1Fecho.CanonicalWedgeFlow.M
abbrev regularUnitary := F1Fecho.RegularCovariantCore.regularUnitary fockFlow
abbrev core := F1Fecho.RegularCovariantCore.core fockFlow M
abbrev embedding := F1Fecho.RegularCovariantCore.embedding fockFlow M
abbrev dualAction := F1Fecho.RegularCovariantCore.dualAction fockFlow M

theorem embedding_injective : Function.Injective embedding :=
  F1Fecho.RegularCovariantCore.embedding_injective fockFlow M

theorem fibre_mem (A : F →L[ℂ] F) (hA : A ∈ M) : fibre A ∈ core :=
  F1Fecho.RegularCovariantCore.fibre_mem fockFlow M A hA

theorem regular_mem (t : ℝ) : regularUnitary t ∈ core :=
  F1Fecho.RegularCovariantCore.regular_mem fockFlow M t

theorem regular_zero : regularUnitary 0 = 1 := F1Fecho.RegularCovariantCore.regular_zero fockFlow

theorem regular_mul (s t : ℝ) :
    regularUnitary s * regularUnitary t = regularUnitary (s+t) :=
  F1Fecho.RegularCovariantCore.regular_mul fockFlow s t

theorem regular_star (t : ℝ) : star (regularUnitary t) = regularUnitary (-t) :=
  F1Fecho.RegularCovariantCore.regular_star fockFlow t

theorem regular_unitary (t : ℝ) :
    star (regularUnitary t) * regularUnitary t = 1 ∧
    regularUnitary t * star (regularUnitary t) = 1 :=
  F1Fecho.RegularCovariantCore.regular_unitary fockFlow t

theorem regular_strongly_continuous (f : RegularHilbert F) :
    Continuous (fun t : ℝ => regularUnitary t f) :=
  F1Fecho.RegularCovariantCore.regular_strongly_continuous fockFlow f

theorem automorphism_is_concrete_boost (t : ℝ) :
    F1Fecho.RegularCovariantCore.automorphism fockFlow t = F1Fecho.WeylFlow.boostAd t := rfl

theorem regular_covariance (t : ℝ) (A : M.toStarSubalgebra) :
    regularUnitary t * fibre (A : F →L[ℂ] F) * star (regularUnitary t) =
      fibre ((F1Fecho.CanonicalWedgeFlow.flow t A).val) := by
  change regularUnitary t * fibre (A : F →L[ℂ] F) * star (regularUnitary t) =
    fibre (F1Fecho.WeylFlow.boostAd t A.val)
  rw [← automorphism_is_concrete_boost]
  exact F1Fecho.RegularCovariantCore.regular_covariance fockFlow t A.val

theorem core_minimal (N : VonNeumannAlgebra (RegularHilbert F))
    (hM : ∀ A ∈ M, fibre A ∈ N) (hU : ∀ t : ℝ, regularUnitary t ∈ N) :
    core ≤ N := F1Fecho.RegularCovariantCore.core_minimal fockFlow M N hM hU

theorem dualAction_zero : dualAction 0 = StarAlgEquiv.refl :=
  F1Fecho.RegularCovariantCore.dualAction_zero fockFlow M

theorem dualAction_add (s t : ℝ) :
    dualAction (s+t) = (dualAction s).trans (dualAction t) :=
  F1Fecho.RegularCovariantCore.dualAction_add fockFlow M s t

theorem dual_fixes_embedding (s : ℝ) (A : M.toStarSubalgebra) :
    dualAction s (embedding A) = embedding A :=
  F1Fecho.RegularCovariantCore.dual_fixes_embedding fockFlow M s A

theorem dual_eigencharacter (s t : ℝ) :
    dualAction s ⟨regularUnitary t,regular_mem t⟩ =
      characterPhase s t • (⟨regularUnitary t,regular_mem t⟩ : core.toStarSubalgebra) := by
  apply Subtype.ext
  exact F1Fecho.RegularCovariantCore.dual_on_regular fockFlow s t

theorem dual_strongly_continuous (A : core.toStarSubalgebra) (f : RegularHilbert F) :
    Continuous (fun s : ℝ => (dualAction s A).val f) :=
  F1Fecho.RegularCovariantCore.dual_strongly_continuous fockFlow M A f

end F1Fecho.CanonicalFockRegular
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockRegular).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
