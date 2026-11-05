import TGLExt.F1Fecho394.CanonicalFockFaithfulWeightR2
import TGLExt.F1Fecho394.RegularCoreConjugationR1
import TGLExt.V350ScalarModularInvariance
/-! The constructed Fock dual weight is invariant under the actual regular
boost conjugation. Invariance alone does NOT identify this candidate flow as
the modular group of the weight; no KMS premise is silently introduced. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.CanonicalFockWeightInvariance
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight

theorem regular_conjugation_eq_fibre (t : ℝ)
    (A : RegularHilbert F →L[ℂ] RegularHilbert F) (hA : A ∈ core) :
    star (regularUnitary t) * A * regularUnitary t =
      star (fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t)) * A *
      fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) :=
  F1Fecho.RegularCoreConjugation.regular_conjugation_eq_fibre fockFlow M t A hA

theorem fibre_boost_fixes_regularVacuum (t : ℝ) :
    fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) regularFockVacuum = regularFockVacuum := by
  change fibre (F1Fecho.RegularCovariantCore.boostCLM fockFlow t) (testVector vacuum) = testVector vacuum
  rw [fibre_testVector]
  change testVector (gamma (B0 (-(2*Real.pi*t))) vacuum) = testVector vacuum
  rw [gamma_vacuum]

def regularConjugate (A : PositiveInput) (t : ℝ) : PositiveInput :=
  ⟨star (regularUnitary t) * A.val * regularUnitary t,
    core.mul_mem (core.mul_mem
      (core.toStarSubalgebra.star_mem' (regular_mem t)) A.property.1) (regular_mem t),
    star_left_conjugate_nonneg A.property.2 _⟩

theorem weight_regular_invariant (A : PositiveInput) (t : ℝ) :
    weight (regularConjugate A t) = weight A := by
  change dualQuadraticIntegral (star (regularUnitary t) * A.val * regularUnitary t)
    regularFockVacuum = dualQuadraticIntegral A.val regularFockVacuum
  rw [regular_conjugation_eq_fibre t A.val A.property.1,
    dualQuadraticIntegral_bimodule,fibre_boost_fixes_regularVacuum]

end F1Fecho.CanonicalFockWeightInvariance
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockWeightInvariance).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
