import TGLExt.F1Fecho394.PhysicalCanonicalNetCompleteR1
import TGLExt.F1Fecho394.CanonicalModularCoreAssemblyR1

/-! Actual Weyl field net on the compact Maxwell one-particle net, with the
same bosonic Fock, vacuum, antiunitary and modular boost. Every field below
is supplied by an existing construction; no trace/PF premise is used.
This is the R6 component, not a whole FockCertificate, a device reduction,
a curved H3 derivation, or a physical confirmation. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.PhysicalFockNet
open TGLExt.ImportedSQ TGL.SpecificAQFT TGL.ModularRealization
open F1Rede.BosonicFock F1Fecho.MaxwellLocalization F1Fecho.Antilinear
open F1Rede.CanonicalWedge

def net (O : Set (Fin 4 → ℝ)) : VonNeumannAlgebra F :=
  FieldWeyl.R (physicalCanonicalNet.K O)

theorem net_mono (O P : Set (Fin 4 → ℝ)) (h : O ⊆ P) :
    (net O : Set (F →L[ℂ] F)) ⊆ net P :=
  FieldWeyl.R_mono _ _ (physicalCanonicalNet.K_mono O P h)

theorem net_local (O P : Set (Fin 4 → ℝ)) (h : SpacelikeSep O P) :
    ∀ A ∈ net O, ∀ B ∈ net P, Commute A B :=
  FieldWeyl.R_local _ _ (physicalCanonicalNet.K_local O P h)

theorem net_wedge_eq :
    net rightWedge = FieldWeyl.R KWR.toClosedSubmodule.toSubmodule := by
  change FieldWeyl.R (compactPhysicalNet rightWedge) = _
  exact congrArg FieldWeyl.R compactPhysicalNet_wedge_glue

theorem weyl_ccr (f g : H1) :
    FieldWeyl.W f * FieldWeyl.W g =
      F1Fecho.WeylCoefficients.phase f g • FieldWeyl.W (f+g) :=
  FieldWeyl.W_ccr f g

theorem weyl_generator_mem (O : Set (Fin 4 → ℝ)) (f : H1)
    (hf : f ∈ physicalCanonicalNet.K O) : FieldWeyl.W f ∈ net O :=
  FieldWeyl.W_mem_R _ f hf

theorem weyl_regular (v : F) : Continuous (fun f : H1 => FieldWeyl.W f v) :=
  FieldWeyl.W_strongly_continuous v

theorem net_covariant (u : H1 ≃ₗᵢ[ℂ] H1) (O P : Set (Fin 4 → ℝ))
    (h : ∀ f, f ∈ physicalCanonicalNet.K O ↔ u f ∈ physicalCanonicalNet.K P)
    (A : F →L[ℂ] F) :
    A ∈ net O ↔ (gamma u).conjStarAlgEquiv A ∈ net P :=
  FieldWeyl.R_covariance u _ _ h A

theorem vacuum_cyclic :
    Dense ((Submodule.span ℂ
      ((fun A : F →L[ℂ] F => A vacuum) '' (net rightWedge : Set (F →L[ℂ] F))) :
        Submodule ℂ F) : Set F) := by
  rw [net_wedge_eq]
  exact F1Fecho.WedgeCyclic.vacuum_cyclic KWR

theorem vacuum_separating (A : F →L[ℂ] F) (hA : A ∈ net rightWedge)
    (h0 : A vacuum = 0) : A = 0 := by
  rw [net_wedge_eq] at hA
  exact F1Fecho.WedgeCyclic.vacuum_separating KWR A hA h0

theorem wedge_nonabelian :
    ∃ A ∈ net rightWedge, ∃ B ∈ net rightWedge, A*B ≠ B*A := by
  rw [net_wedge_eq]
  exact F1Fecho.WedgeNonabelian.wedge_nonabelian

theorem vacuum_bw_kms :
    KMSBody (net rightWedge) vacuum (fun t => gamma (B0 (2*Real.pi*t))) 1 := by
  rw [net_wedge_eq]
  exact F1Fecho.CanonicalWedgeKMS.canonical_bw_kms

theorem pair_tomita :
    ORDEM016.D6.PairTomitaAnalyticRealizationMeasured
      (net rightWedge).toStarSubalgebra vacuum canonicalFockJ
      (fun t => gamma (B0 (-(2*Real.pi*t)))) := by
  rw [net_wedge_eq]
  exact F1Fecho.CanonicalFockBW.canonical_pair_tomita

theorem modular_J_same_one_particle (x : H1) :
    canonicalFockJ (oneParticle x) = oneParticle (Jcandidate x) :=
  canonicalFockJ_oneParticle x

theorem modular_J_involutive : Function.Involutive canonicalFockJ :=
  canonicalFockJ_involutive

theorem modular_J_vacuum : canonicalFockJ vacuum = vacuum :=
  canonicalFockJ_vacuum

end F1Fecho.PhysicalFockNet

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.PhysicalFockNet).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
