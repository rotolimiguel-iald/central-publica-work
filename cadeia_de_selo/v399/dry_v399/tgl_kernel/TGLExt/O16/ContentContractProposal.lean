import Lean
import TGLExt.O16.RecognitionReadout
import TGLExt.O16.RecognitionInverse_v2

set_option autoImplicit false
namespace ORDEM016.D6
noncomputable section
open Set Topology TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Named remaining obligation for one independently specified physical pair.
It includes its own graph/resolvent/polar realization and dense spectral readout.
It contains no comparison with another pair and no U-intertwining conclusion. -/
def PairTomitaAnalyticRealizationMeasured
    (M : StarSubalgebra ℂ (H →L[ℂ] H)) (omega : H)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (flow : ℝ → H ≃ₗᵢ[ℂ] H) : Prop :=
  ∃ A : ModularGraphRealization (closure (pairTomitaGraph M omega)),
    A.J=J ∧ ∀ t x, flow t (resolventDampingOperator A.R x)=resolventPhaseOperator A.R t x

/-- A proposed contract consumer, conditional on the two named realization obligations.
The two flows and antiunitaries are parameters fixed before recognition.
No new inhabitant of the physical ContratoH2 is constructed here. -/
theorem same_horizon_by_content_from_realizations
    {M N : StarSubalgebra ℂ (H →L[ℂ] H)} {omega omega' : H}
    (C : ReconhecimentoPeloConteudo M N omega omega')
    (J J' : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (flow flow' : ℝ → H ≃ₗᵢ[ℂ] H)
    (source : PairTomitaAnalyticRealizationMeasured M omega J flow)
    (target : PairTomitaAnalyticRealizationMeasured N omega' J' flow') :
    (∀ x, C.U (J (C.U.symm x))=J' x) ∧
    (∀ t x, C.U (flow t (C.U.symm x))=flow' t x) := by
  obtain ⟨A,hJ,hF⟩ := source
  obtain ⟨B,hJ',hF'⟩ := target
  let F : ModularReadout A := ⟨flow,hF⟩
  let F' : ModularReadout B := ⟨flow',hF'⟩
  have h := same_horizon_by_content_readout C A B F F'
  change (∀ x, C.U (A.J (C.U.symm x))=B.J x) ∧
    (∀ t x, C.U (flow t (C.U.symm x))=flow' t x) at h
  simpa only [hJ,hJ'] using h

#print axioms PairTomitaAnalyticRealizationMeasured
#print axioms same_horizon_by_content_from_realizations
end
end ORDEM016.D6


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
