-- predecessor_sha256: 1e25134ede2f05c378e46e64b670992e282d12cb2aaa4dbf679384b69d3de3fc
import Lean
import TGLExt.O16.RecognitionGraph_v2

set_option autoImplicit false
namespace ORDEM016.D6
noncomputable section
open Set Topology
variable {H K : Type*}
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
variable {M : StarSubalgebra ℂ (H →L[ℂ] H)}
  {N : StarSubalgebra ℂ (K →L[ℂ] K)} {omega : H} {omega' : K}

def ReconhecimentoPeloConteudo.symm (R : ReconhecimentoPeloConteudo M N omega omega') :
    ReconhecimentoPeloConteudo N M omega' omega where
  U := R.U.symm
  reference := (congrArg R.U.symm R.reference.symm).trans (R.U.symm_apply_apply omega)
  algebra := by
    intro B
    have h := (R.algebra (R.U.conjStarAlgEquiv.symm B)).symm
    rw [R.U.conjStarAlgEquiv.apply_symm_apply B] at h
    exact h

theorem recognized_domains_equal (R : ReconhecimentoPeloConteudo M N omega omega')
    (D : Set H) (E : Set K) (S : D → H) (T : E → K)
    (hs : Set.range (fun x : D => ((x : H),S x)) = closure (pairTomitaGraph M omega))
    (ht : Set.range (fun y : E => ((y : K),T y)) = closure (pairTomitaGraph N omega')) :
    R.U '' D = E := by
  ext y
  constructor
  · rintro ⟨x,hx,rfl⟩
    obtain ⟨z,hz,_⟩ := recognition_identifies_closed_operator R D E S T hs ht ⟨x,hx⟩
    exact hz ▸ z.property
  · intro hy
    obtain ⟨x,hx,_⟩ := recognition_identifies_closed_operator R.symm E D T S ht hs ⟨y,hy⟩
    refine ⟨x,x.property,?_⟩
    change (x : H)=R.U.symm y at hx
    rw [hx]; exact R.U.apply_symm_apply y

#print axioms ReconhecimentoPeloConteudo.symm
#print axioms recognized_domains_equal
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
