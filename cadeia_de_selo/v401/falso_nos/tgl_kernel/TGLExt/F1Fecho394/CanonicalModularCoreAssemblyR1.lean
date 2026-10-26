import TGLExt.F1Fecho394.CanonicalWeylAssemblyR5
import TGLExt.F1Fecho394.CanonicalFockRegularCoreR2
import TGLExt.F1Fecho394.WedgeNonabelianR4
import TGLExt.F1Fecho394.CanonicalGammaPositiveR3
import TGLExt.F1Fecho394.CanonicalGammaNoFixedR4
import TGLExt.F1Fecho394.CanonicalWedgeKMSR4
import TGLExt.F1Fecho394.CanonicalFockBWR2
/-! Concrete core wiring after construction of canonical KMS and the
actual Weyl/vacuum Tomita modular-flow equality on the same Fock space.
The remaining record has 21 explicit trace/PF obligations; global net glue
remains in CanonicalNetInput. No inhabitant of that joint input is asserted. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.NetworkModularCore
open TGL.SpecificAQFT TGL.ModularRealization TGLExt.ImportedSQ
open F1Rede.BosonicFock F1Fecho.NetworkReuse F1Fecho.Antilinear
open TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open F1Fecho.NetworkWeyl

abbrev RepresentedCore := F1Fecho.CanonicalFockRegular.core.toStarSubalgebra

theorem wedge_le_canonical (D : CanonicalNetInput) :
    (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra ≤
    F1Fecho.CanonicalFockRegular.M.toStarSubalgebra := by
  rw [D.wedge_glue]
  exact le_rfl

def coreEmbedding (D : CanonicalNetInput) :
    (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra →⋆ₐ[ℂ] RepresentedCore :=
  F1Fecho.CanonicalFockRegular.embedding.comp
    (StarSubalgebra.inclusion (wedge_le_canonical D))

theorem coreEmbedding_injective (D : CanonicalNetInput) :
    Function.Injective (coreEmbedding D) :=
  F1Fecho.CanonicalFockRegular.embedding_injective.comp
    (StarSubalgebra.inclusion_injective (wedge_le_canonical D))

theorem dual_fixes_coreEmbedding (D : CanonicalNetInput) (s : ℝ)
    (A : (FieldWeyl.R (D.K rightWedge)).toStarSubalgebra) :
    F1Fecho.CanonicalFockRegular.dualAction s (coreEmbedding D A) = coreEmbedding D A :=
  F1Fecho.CanonicalFockRegular.dual_fixes_embedding s
    (StarSubalgebra.inclusion (wedge_le_canonical D) A)

structure RemainingModularCoreInput (D : CanonicalNetInput) where
  trace : RepresentedCore → ENNReal
  trace_zero : trace 0 = 0
  trace_tracial : ∀ x y : RepresentedCore, trace (x * y) = trace (y * x)
  trace_star : ∀ x : RepresentedCore, trace (star x) = trace x
  trace_dual_scaling : ∀ (s : ℝ) (x : RepresentedCore),
    trace ((F1Fecho.CanonicalFockRegular.dualAction s) x) = ENNReal.ofReal (Real.exp (-s)) * trace x
  /-- uma projeção finita não nula do núcleo II_∞, partida em duas metades de traço igual [Connes 1973]. -/
  PF : RepresentedCore
  PF_sa : star PF = PF
  PF_idem : PF * PF = PF
  PF_ne : PF ≠ 0
  PF_pos : 0 < trace PF
  PF_fin : trace PF < ⊤
  Pp : RepresentedCore
  Pm : RepresentedCore
  Pp_sa : star Pp = Pp
  Pp_idem : Pp * Pp = Pp
  Pm_sa : star Pm = Pm
  Pm_idem : Pm * Pm = Pm
  split : Pp + Pm = PF
  orth : Pp * Pm = 0
  trace_additive : trace PF = trace Pp + trace Pm
  equal_halves : trace Pp = trace Pm


def RemainingModularCoreInput.toRemainingWeyl {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) : RemainingWeylInput D where
  Core := RepresentedCore
  instCR := inferInstance
  instCS := inferInstance
  instCA := inferInstance
  embedding := coreEmbedding D
  embedding_injective := coreEmbedding_injective D
  dualAction := F1Fecho.CanonicalFockRegular.dualAction
  dualAction_zero := F1Fecho.CanonicalFockRegular.dualAction_zero
  dualAction_add := F1Fecho.CanonicalFockRegular.dualAction_add
  Γ_positive := F1Fecho.CanonicalGammaPositive.gamma_positive
  Γ_no_fixed := F1Fecho.CanonicalGammaNoFixed.gamma_no_fixed
  wedge_nonabelian := by
    rw [D.wedge_glue]
    exact F1Fecho.WedgeNonabelian.wedge_nonabelian
  bw_kms := by
    rw [D.wedge_glue]
    exact F1Fecho.CanonicalWedgeKMS.canonical_bw_kms
  tomita := by
    rw [D.wedge_glue]
    exact F1Fecho.CanonicalFockBW.canonical_pair_tomita
  trace := A.trace
  trace_zero := A.trace_zero
  trace_tracial := A.trace_tracial
  trace_star := A.trace_star
  trace_dual_scaling := A.trace_dual_scaling
  PF := A.PF
  PF_sa := A.PF_sa
  PF_idem := A.PF_idem
  PF_ne := A.PF_ne
  PF_pos := A.PF_pos
  PF_fin := A.PF_fin
  Pp := A.Pp
  Pm := A.Pm
  Pp_sa := A.Pp_sa
  Pp_idem := A.Pp_idem
  Pm_sa := A.Pm_sa
  Pm_idem := A.Pm_idem
  split := A.split
  orth := A.orth
  trace_additive := A.trace_additive
  equal_halves := A.equal_halves

def RemainingModularCoreInput.toCertificate {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) : FockCertificate D.toLightNetData.toLightOneParticle :=
  A.toRemainingWeyl.toCertificate

theorem assembled_core_is_concrete {D : CanonicalNetInput} (A : RemainingModularCoreInput D) :
    A.toCertificate.Core = RepresentedCore := rfl

theorem assembled_embedding_is_concrete {D : CanonicalNetInput} (A : RemainingModularCoreInput D) :
    A.toCertificate.embedding = coreEmbedding D := rfl

theorem assembled_dual_is_concrete {D : CanonicalNetInput} (A : RemainingModularCoreInput D) :
    A.toCertificate.dualAction = F1Fecho.CanonicalFockRegular.dualAction := rfl

end F1Fecho.NetworkModularCore
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.NetworkModularCore).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
