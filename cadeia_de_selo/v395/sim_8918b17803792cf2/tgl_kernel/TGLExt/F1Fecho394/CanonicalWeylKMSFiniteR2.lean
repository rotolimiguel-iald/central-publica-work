import TGLExt.F1Fecho394.WedgeOneParticleStripR2
import TGLExt.F1Fecho394.WeylStripFromCoefficientR3
import TGLExt.F1Fecho394.WeylFiniteAlgebraR4
/-! KMS is proved for the actual field-Weyl generators and their complex
finite span in the same Fock space. The one-particle continuation is derived
from the canonical multiplier and standard wedge, not assumed in this output.
Extension to the von Neumann closure is a separate graph-density argument. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.CanonicalWeylKMSFinite
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.WeylExponentialCore F1Fecho.WeylFiniteAlgebra

def boostFlow (t : ℝ) : F ≃ₗᵢ[ℂ] F := gamma (B0 (2*Real.pi*t))

theorem generator_pair (f g : H1) (hf : f ∈ K) (hg : g ∈ K) :
    KMSFiniteSpan.Pair vacuum boostFlow (FieldWeyl.W f) (FieldWeyl.W g) := by
  have hs := WedgeOneParticleStrip.wedge_strip
    (⟨f,hf⟩ : KWR.toClosedSubmodule) (⟨g,hg⟩ : KWR.toClosedSubmodule)
  apply WeylStripFromCoefficient.pair_from_coefficient
    (fun t => B0 (2*Real.pi*t)) f g (CanonicalH1Strip.coefficient f g)
  · exact hs.1
  · exact hs.2.1
  · exact hs.2.2.1
  · intro t
    simpa only [mul_neg] using hs.2.2.2 t

theorem finite_pair (A B : F →L[ℂ] F)
    (hA : A ∈ finiteAlgebra) (hB : B ∈ finiteAlgebra) :
    KMSFiniteSpan.Pair vacuum boostFlow A B := by
  apply KMSFiniteSpan.span_pair (F1Fecho.WeylNet.generators FieldWeyl.W K)
    (A := A) (B := B) (hA := hA) (hB := hB)
  rintro _ ⟨f,hf,rfl⟩ _ ⟨g,hg,rfl⟩
  exact generator_pair f g hf hg

end F1Fecho.CanonicalWeylKMSFinite

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalWeylKMSFinite).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
