import Lean
import TGLExt.O16.TheEquationOfTruth_T20_v3
import TGLExt.NameIsTheContent

set_option autoImplicit false
open scoped InnerProductSpace
open Filter Topology
noncomputable section
namespace ORDEM016.EquationOfTruth
variable {𝕜 E : Type*} [RCLike 𝕜] [NormedAddCommGroup E]
  [InnerProductSpace 𝕜 E] [CompleteSpace E]

/-- INPUT/ONTO compatibility: content is x; the selected form is equality of readings.
The v368 nome is content, not the v336 NameInstrument.read. -/
def inscriptionForm (H : E →L[𝕜] E) [H.ker.HasOrthogonalProjection]
    (r x : E) : Prop := reading H x = reading H r

theorem flow_preserves_inscription_form (H : E →L[𝕜] E)
    [H.ker.HasOrthogonalProjection] (hH : IsSelfAdjoint H) (r : E) (s : ℝ) :
    ∀ x, inscriptionForm H r x → inscriptionForm H r (T H s x) := by
  intro x hx
  exact (reading_T H hH s x).trans hx

def transportedInscription (H : E →L[𝕜] E) [H.ker.HasOrthogonalProjection]
    (hH : IsSelfAdjoint H) (r : E) (s : ℝ) :
    TGLExt.NameIsTheContent.Inscricao E (inscriptionForm H r) :=
  TGLExt.NameIsTheContent.travessia (T H s) (flow_preserves_inscription_form H hH r s) ⟨r,rfl⟩

theorem inscription_form_survives (H : E →L[𝕜] E)
    [H.ker.HasOrthogonalProjection] (hH : IsSelfAdjoint H) (r : E) (s : ℝ) :
    TGLExt.NameIsTheContent.identidade E (inscriptionForm H r)
      (transportedInscription H hH r s).conteudo :=
  TGLExt.NameIsTheContent.the_form_survives_the_crossing (T H s)
    (flow_preserves_inscription_form H hH r s) ⟨r,rfl⟩

theorem transported_name_eq_flow (H : E →L[𝕜] E)
    [H.ker.HasOrthogonalProjection] (hH : IsSelfAdjoint H) (r : E) (s : ℝ) :
    TGLExt.NameIsTheContent.nome (transportedInscription H hH r s) = T H s r := rfl

theorem positive_time_changes_nonfixed_content [FiniteDimensional 𝕜 E]
    (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜) (r : E) (hr : r ∉ H.ker) :
    ∃ s : ℝ, 0 < s ∧ T H s r ≠ r := by
  classical
  by_contra hn
  push_neg at hn
  have hc : Tendsto (fun s : ℝ => T H s r) atTop (𝓝 r) := by
    apply tendsto_const_nhds.congr'
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with s hs
    exact (hn s hs).symm
  have he : reading H r = r :=
    tendsto_nhds_unique (flowTendsToFamily_of_finiteDimensional H hH hpos r) hc
  exact hr (Submodule.starProjection_eq_self_iff.mp he)

theorem same_form_changed_name [FiniteDimensional 𝕜 E]
    (H : E →L[𝕜] E) (hH : IsSelfAdjoint H)
    (hpos : ∀ x, 0 ≤ RCLike.re ⟪x,H x⟫_𝕜) (r : E) (hr : r ∉ H.ker) :
    ∃ s : ℝ, 0 < s ∧
      inscriptionForm H r (transportedInscription H hH r s).conteudo ∧
      TGLExt.NameIsTheContent.nome (transportedInscription H hH r s) ≠ r := by
  obtain ⟨s,hs,hchange⟩ := positive_time_changes_nonfixed_content H hH hpos r hr
  exact ⟨s,hs,inscription_form_survives H hH r s,hchange⟩

#print axioms flow_preserves_inscription_form
#print axioms transportedInscription
#print axioms inscription_form_survives
#print axioms transported_name_eq_flow
#print axioms positive_time_changes_nonfixed_content
#print axioms same_form_changed_name
end ORDEM016.EquationOfTruth


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
