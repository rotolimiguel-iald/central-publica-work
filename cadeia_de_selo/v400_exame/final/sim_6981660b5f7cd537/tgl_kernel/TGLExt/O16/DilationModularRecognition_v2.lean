-- predecessor_sha256: 73e246395dbac489311ed0eb5545ae98fd9bada14d4dcae00df6e7bafd950299
import Lean
import TGLExt.O16.DilationGeometry_v2
import TGLExt.O16.ContentContractProposal

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open ORDEM016.Photon.SpecificAQFT ORDEM016.D6
namespace ORDEM016.D5

/-- Net covariance and vacuum preservation recognize the SAME wedge pair, because
positive dilation maps the wedge onto itself. The implementing D is still an input. -/
theorem dilation_recognizes_modular_content
    (W : TGLSpecificAQFTWitness) (r : ℝ) (hr : 0<r)
    (D : W.H ≃ₗᵢ[ℂ] W.H) (hVac : D W.vac=W.vac)
    (hNet : ∀ (O : Set (Fin 4 → ℝ)) (A : W.H →L[ℂ] W.H),
      A ∈ W.net O ↔ D.conjStarAlgEquiv A ∈ W.net (dilation r '' O))
    (J : W.H ≃ₛₗᵢ[starRingEnd ℂ] W.H) (flow : ℝ → W.H ≃ₗᵢ[ℂ] W.H)
    (hReal : PairTomitaAnalyticRealizationMeasured (W.net rightWedge).toStarSubalgebra
      W.vac J flow) :
    (∀ x,D (J (D.symm x))=J x) ∧ (∀ t x,D (flow t (D.symm x))=flow t x) := by
  let C : ReconhecimentoPeloConteudo (W.net rightWedge).toStarSubalgebra
      (W.net rightWedge).toStarSubalgebra W.vac W.vac :=
    { U := D
      reference := hVac
      algebra := by
        intro A
        change A ∈ W.net rightWedge ↔ D.conjStarAlgEquiv A ∈ W.net rightWedge
        simpa only [dilation_wedge_image r hr] using hNet rightWedge A }
  exact same_horizon_by_content_from_realizations C J J flow flow hReal hReal

/-- Zero scaling is not an admissible wedge self-similarity. -/
theorem zero_dilation_rejected (x : Fin 4 → ℝ) : dilation 0 x ∉ rightWedge := by
  simp [dilation,rightWedge]

#print axioms dilation_recognizes_modular_content
#print axioms zero_dilation_rejected
end ORDEM016.D5


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
