import TGLExt.O16.PhotonContractTheorems_v2
import TGLExt.O16.ContentContractProposal
import TGLExt.TheGravitonIsTheConjugatedPhase
import Lean

set_option autoImplicit false
noncomputable section
namespace ORDEM016.ContractV32Proposal
open ORDEM016.Photon.SpecificAQFT ORDEM016.Photon.ModularRealization
open ORDEM016.Photon.Contract MeasureTheory Matrix

/- INPUT/PROPOSAL, not ratified and no physical inhabitant claimed.
   W0 is the light field's net, not an additional spin-2 particle net.
   D4's peso_do_nome belongs to W0. The massless helicity restriction is
   stated explicitly, since peso_do_nome alone also admits massive models.
   This file consolidates types; it does not discharge their fields. -/
structure ContratoH2 (W0 : TGLSpecificAQFTWitness)
    (R0 : TGLModularRealization W0) (N0 : KillingNormalization)
    extends ORDEM016.Photon.Contract.ContratoH2 W0 R0 N0 where
  photon_mass : W0.m = 0
  photon_helicity : W0.helicity = 1 ∨ W0.helicity = -1
  pair_realization : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (W0.net rightWedge).toStarSubalgebra W0.vac
    R0.modular.modularConjugation Δit

abbrev Spacetime := Fin 4 → ℝ
def metricSign (μ : Fin 4) : ℝ := if μ = 0 then 1 else -1
def testDerivative (f : Spacetime → ℝ) (μ : Fin 4) (x : Spacetime) : ℝ :=
  fderiv ℝ f x (Pi.single μ 1)

/- Same explicit clauses as A1/StressTensorDataLocal_v2, retyped on D4's
   photon witness. No inference of operator locality from this tensor type. -/
structure StressTensorDataLocal_v2 (W0 : TGLSpecificAQFTWitness)
    (B : WedgeBoostRep W0) extends StressTensorData W0 where
  symmetric : ∀ ψ x, (T ψ x).transpose = T ψ x
  test_integrable : ∀ (ψ : W0.H) (ν μ : Fin 4) (f : Spacetime → ℝ),
    ContDiff ℝ (⊤ : ℕ∞) f → HasCompactSupport f →
    Integrable (fun x => metricSign μ * T ψ x μ ν * testDerivative f μ x)
  conserved : ∀ (ψ : W0.H) (ν : Fin 4) (f : Spacetime → ℝ),
    ContDiff ℝ (⊤ : ℕ∞) f → HasCompactSupport f →
    (∑ μ : Fin 4, ∫ x : Spacetime,
      metricSign μ * T ψ x μ ν * testDerivative f μ x) = 0
  boost_covariant : ∀ (s : ℝ) (ψ : W0.H) (x : Spacetime),
    T (B.V s ψ) x = (TGLExt.boostMat (-s)).transpose *
      T ψ (wedgeBoostMap (-s) x) * TGLExt.boostMat (-s)

/- The finite conjugated form of D3', INPUT/ONTO as interpretation.
   Its embedding into the physical net remains the named D3' obligation. -/
def conjugatedLightForm : Matrix (Fin 2) (Fin 2) ℂ :=
  vecMulVec (fun i => star (TGLExt.lightPlus i)) (fun i => star (TGLExt.lightPlus i))

structure ContratoH3 (W0 : TGLSpecificAQFTWitness) (R0 : TGLModularRealization W0)
    (N0 : KillingNormalization) (B : WedgeBoostRep W0)
    (T0 : StressTensorDataLocal_v2 W0 B)
    extends ORDEM016.Photon.Contract.ContratoH3 W0 R0 N0 T0.toStressTensorData where
  light_horizon : ContratoH2 W0 R0 N0
  same_stress_boost : light_horizon.boost = B
  same_local_horizon : H2 = light_horizon.toContratoH2

/- The source h2 is no longer a phantom index. The result and source have
   independently specified modular data; D6 proves their intertwining from
   recognition + the two analytic realizations. No equality of target flows
   is put into same_horizon. This is transport, not v3.1's literal H2 equality. -/
structure ContratoImportH3 (W0 : TGLSpecificAQFTWitness)
    (R0 : TGLModularRealization W0) (N0 : KillingNormalization)
    (B : WedgeBoostRep W0) (T0 : StressTensorDataLocal_v2 W0 B)
    (h2 : ContratoH2 W0 R0 N0) where
  produce : ContratoH3 W0 R0 N0 B T0
  same_horizon : ORDEM016.D6.ReconhecimentoPeloConteudo
    (W0.net rightWedge).toStarSubalgebra (W0.net rightWedge).toStarSubalgebra
    W0.vac W0.vac
  source_realization : ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
    (W0.net rightWedge).toStarSubalgebra W0.vac R0.modular.modularConjugation h2.Δit

-- Type-check the existing D6 consumer on the actual source/produced indices.
-- This query creates no declaration and assumes no intertwining equality.
#check fun (W0 : TGLSpecificAQFTWitness) (R0 : TGLModularRealization W0)
  (N0 : KillingNormalization) (B : WedgeBoostRep W0)
  (T0 : StressTensorDataLocal_v2 W0 B) (h2 : ContratoH2 W0 R0 N0)
  (c : ContratoImportH3 W0 R0 N0 B T0 h2) =>
  ORDEM016.D6.same_horizon_by_content_from_realizations c.same_horizon
    R0.modular.modularConjugation R0.modular.modularConjugation
    h2.Δit c.produce.light_horizon.Δit
    c.source_realization c.produce.light_horizon.pair_realization

-- Audit only, no new theorem in this consolidation.
#print axioms ContratoH2
#print axioms StressTensorDataLocal_v2
#print axioms conjugatedLightForm
#print axioms ContratoH3
#print axioms ContratoImportH3
end ORDEM016.ContractV32Proposal

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
