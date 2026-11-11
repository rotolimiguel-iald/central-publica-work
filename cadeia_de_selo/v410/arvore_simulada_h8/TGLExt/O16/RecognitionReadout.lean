import Lean
import TGLExt.O16.RecognitionModular_v2

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ORDEM016.D6
noncomputable section
open Set Topology TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Independent modular readout, characterized on its own dense damped range.
This is an analytic obligation, not an equation between different horizons. -/
structure ModularReadout {G : Set (H × H)} (A : ModularGraphRealization G) where
  flow : ℝ → H ≃ₗᵢ[ℂ] H
  spectral_readout : ∀ t x, flow t (resolventDampingOperator A.R x) =
    resolventPhaseOperator A.R t x

theorem readout_eq_imaginary_power {G : Set (H × H)}
    (A : ModularGraphRealization G) (F : ModularReadout A) (t : ℝ) (x : H) :
    F.flow t x = resolventImaginaryPower A.R A.nonneg A.le_one
      A.injective A.complement_injective t x := by
  refine (resolventDampingOperator_denseRange A.R A.nonneg A.le_one
    A.injective A.complement_injective).induction ?_
    (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  rw [F.spectral_readout,resolventImaginaryPower_damping]

theorem recognizes_independent_readouts {G G' : Set (H × H)}
    (U : H ≃ₗᵢ[ℂ] H)
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (A : ModularGraphRealization G) (B : ModularGraphRealization G')
    (F : ModularReadout A) (F' : ModularReadout B) (t : ℝ) (x : H) :
    U (F.flow t x)=F'.flow t (U x) := by
  rw [readout_eq_imaginary_power A F,readout_eq_imaginary_power B F']
  exact recognizes_imaginary_powers U hg A B t x

/-- Proposed content clause to accompany, not masquerade as, definitional identity.
The result mentions the flows given before recognition, rather than renamed copies.
No physical KMS/BW hypotheses of ContratoH2 are discharged by this bridge. -/
theorem same_horizon_by_content_readout
    {M N : StarSubalgebra ℂ (H →L[ℂ] H)} {omega omega' : H}
    (C : ReconhecimentoPeloConteudo M N omega omega')
    (A : ModularGraphRealization (closure (pairTomitaGraph M omega)))
    (B : ModularGraphRealization (closure (pairTomitaGraph N omega')))
    (F : ModularReadout A) (F' : ModularReadout B) :
    (∀ x, C.U (A.J (C.U.symm x))=B.J x) ∧
    (∀ t x, C.U (F.flow t (C.U.symm x))=F'.flow t x) := by
  constructor
  · intro x
    simpa using recognizes_polar_factor C.U (recognition_closed_tomita_graph C) A B (C.U.symm x)
  · intro t x
    simpa using recognizes_independent_readouts C.U (recognition_closed_tomita_graph C)
      A B F F' t (C.U.symm x)

#print axioms readout_eq_imaginary_power
#print axioms recognizes_independent_readouts
#print axioms same_horizon_by_content_readout
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
