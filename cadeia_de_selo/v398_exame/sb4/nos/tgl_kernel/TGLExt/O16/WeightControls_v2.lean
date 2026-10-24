-- predecessor_sha256: bfccca017ba7c45edb077304ba3fd9d21734d412ae4dae71a1ed323740e282ce
import Lean
import TGLExt.O16.PhotonContract_v2

set_option autoImplicit false
noncomputable section
namespace ORDEM016.Photon.WeightControls
open ORDEM016.Photon.SpecificAQFT

theorem massless_scalar_rejected (W : TGLSpecificAQFTWitness)
    (hm : W.m=0) (hh : W.helicity=0) : False := by
  have h := W.peso_do_nome
  simp [hm,hh] at h

/-- Admission of these spectral values is not existence of a photon AQFT net. -/
theorem photon_plus_weight : (0 : ℝ)<0 ∨ (1 : ℤ)≠0 := Or.inr (by decide)
theorem photon_minus_weight : (0 : ℝ)<0 ∨ (-1 : ℤ)≠0 := Or.inr (by decide)

theorem massless_requires_nonzero_helicity (W : TGLSpecificAQFTWitness) (hm : W.m=0) :
    W.helicity≠0 := by
  simpa [hm] using W.peso_do_nome

/-- Exact scope diagnostic: the requested disjunction alone does not prohibit
negative mass in a nonzero-helicity sector. No physical witness is asserted. -/
theorem disjunction_alone_allows_negative_mass :
    (0 : ℝ)< -1 ∨ (1 : ℤ)≠0 := Or.inr (by decide)

#print axioms massless_scalar_rejected
#print axioms photon_plus_weight
#print axioms photon_minus_weight
#print axioms massless_requires_nonzero_helicity
#print axioms disjunction_alone_allows_negative_mass
end ORDEM016.Photon.WeightControls


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
