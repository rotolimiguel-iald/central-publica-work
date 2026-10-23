import Lean
import TGLExt.O16.PhotonModularRealization
import TGLExt.V354RegularLegacyWitness

set_option autoImplicit false
noncomputable section
namespace ORDEM016.Photon.Transport
def liftW (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) :
    ORDEM016.Photon.SpecificAQFT.TGLSpecificAQFTWitness where
  m := W.m
  H := W.H
  instNormed := W.instNormed
  instInner := W.instInner
  instComplete := W.instComplete
  net := W.net
  vac := W.vac
  U := W.U
  helicity := W.helicity
  peso_do_nome := W.peso_do_nome
  vac_norm := W.vac_norm
  isotony := W.isotony
  locality := W.locality
  U_zero := W.U_zero
  U_add := W.U_add
  U_star := W.U_star
  covariance := W.covariance
  vac_invariant := W.vac_invariant
  wedge_nonabelian := W.wedge_nonabelian
  vac_cyclic_wedge := W.vac_cyclic_wedge
  vac_separating_wedge := W.vac_separating_wedge

def liftD (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (d : TGL.ModularRealization.WedgeModularData W) : ORDEM016.Photon.ModularRealization.WedgeModularData (liftW W) where
  wedgeAlgebra := d.wedgeAlgebra
  wedgeAlgebra_eq := d.wedgeAlgebra_eq
  modularFlow := d.modularFlow
  modularFlow_zero := d.modularFlow_zero
  modularFlow_add := d.modularFlow_add
  modularConjugation := d.modularConjugation
  modularConjugation_involutive := d.modularConjugation_involutive
  modularConjugation_vac := d.modularConjugation_vac

def liftC (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (d : TGL.ModularRealization.WedgeModularData W) (c : TGL.ModularRealization.ContinuousCoreData W d) : ORDEM016.Photon.ModularRealization.ContinuousCoreData (liftW W) (liftD W d) where
  Core := c.Core
  instCoreRing := c.instCoreRing
  instCoreStarRing := c.instCoreStarRing
  instCoreAlgebra := c.instCoreAlgebra
  embedding := c.embedding
  embedding_injective := c.embedding_injective
  dualAction := c.dualAction
  dualAction_zero := c.dualAction_zero
  dualAction_add := c.dualAction_add
  canonicalTrace := c.canonicalTrace
  trace_zero := c.trace_zero
  trace_tracial := c.trace_tracial
  trace_star := c.trace_star
  trace_dual_scaling := c.trace_dual_scaling

def liftL (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (d : TGL.ModularRealization.WedgeModularData W) (c : TGL.ModularRealization.ContinuousCoreData W d) (l : TGL.ModularRealization.ThreeLocksCoreData W d c) : ORDEM016.Photon.ModularRealization.ThreeLocksCoreData (liftW W) (liftD W d) (liftC W d c) where
  H3Lt := l.H3Lt
  H3Lt_selfAdjoint := l.H3Lt_selfAdjoint
  PF := l.PF
  PF_selfAdjoint := l.PF_selfAdjoint
  PF_idempotent := l.PF_idempotent
  PF_locks := l.PF_locks
  PF_maximal := l.PF_maximal
  PF_nonzero := l.PF_nonzero
  PF_trace_pos := l.PF_trace_pos
  PF_trace_finite := l.PF_trace_finite
  Pplus := l.Pplus
  Pminus := l.Pminus
  Pplus_selfAdjoint := l.Pplus_selfAdjoint
  Pplus_idempotent := l.Pplus_idempotent
  Pminus_selfAdjoint := l.Pminus_selfAdjoint
  Pminus_idempotent := l.Pminus_idempotent
  split := l.split
  orthogonal := l.orthogonal
  trace_split_additive := l.trace_split_additive
  equal_face_trace := l.equal_face_trace

def liftR (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (R : TGL.ModularRealization.TGLModularRealization W) :
    ORDEM016.Photon.ModularRealization.TGLModularRealization (liftW W) where
  infiniteHilbert := R.infiniteHilbert
  modular := liftD W R.modular
  core := liftC W R.modular R.core
  threeLocks := liftL W R.modular R.core R.threeLocks
def legacyW := liftW TGLExt.theSpecificAQFTWitness
def legacyR := liftR TGLExt.theSpecificAQFTWitness TGLV354.TraceCompletion.regularModularRealization
#print axioms liftW
#print axioms liftD
#print axioms liftC
#print axioms liftL
#print axioms liftR
end ORDEM016.Photon.Transport


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
