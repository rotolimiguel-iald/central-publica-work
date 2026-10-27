import Lean
import TGLExt.O16.RecognitionGraph_v2

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ORDEM016.D6
noncomputable section
open Set Topology
variable {H K : Type*}
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]

/-- Graph of S* S for an antilinear S, given by the adjoint pairing.
For an arbitrary relation this definition alone asserts neither density
nor selfadjointness. Those analytic properties are not hidden premises. -/
def antilinearSquareGraph (G : Set (H × H)) : Set (H × H) :=
  {p | ∃ sx : H, (p.1,sx) ∈ G ∧ ∀ y sy : H, (y,sy) ∈ G →
    inner ℂ p.2 y = inner ℂ sy sx}

theorem unitary_square_graph_forward (U : H ≃ₗᵢ[ℂ] K)
    (G : Set (H × H)) (G' : Set (K × K))
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (x z : H) (hx : (x,z) ∈ antilinearSquareGraph G) :
    (U x,U z) ∈ antilinearSquareGraph G' := by
  obtain ⟨sx,hsx,hpair⟩ := hx
  refine ⟨U sx,?_,?_⟩
  · rw [← hg]; exact ⟨(x,sx),hsx,rfl⟩
  · intro y' sy' hy
    rw [← hg] at hy
    obtain ⟨q,hq,he⟩ := hy
    have hy' : U q.1 = y' := congrArg Prod.fst he
    have hsy' : U q.2 = sy' := congrArg Prod.snd he
    rw [← hy',← hsy']
    simpa using hpair q.1 q.2 hq

theorem recognition_square_graph_forward
    {M : StarSubalgebra ℂ (H →L[ℂ] H)} {N : StarSubalgebra ℂ (K →L[ℂ] K)}
    {omega : H} {omega' : K} (R : ReconhecimentoPeloConteudo M N omega omega')
    (x z : H) (hx : (x,z) ∈ antilinearSquareGraph (closure (pairTomitaGraph M omega))) :
    (R.U x,R.U z) ∈ antilinearSquareGraph (closure (pairTomitaGraph N omega')) :=
  unitary_square_graph_forward R.U _ _ (recognition_closed_tomita_graph R) x z hx

/-- Resolvents supplied independently are identified using their graph
realizations. The intertwining equation is proved, not a record field. -/
theorem unitary_recognizes_square_resolvent (U : H ≃ₗᵢ[ℂ] K)
    (G : Set (H × H)) (G' : Set (K × K))
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (A : H →L[ℂ] H) (B : K →L[ℂ] K)
    (ha : ∀ z : H, (A z,z-A z) ∈ antilinearSquareGraph G)
    (hb : ∀ x y : K, (x,y) ∈ antilinearSquareGraph G' → B (x+y)=x)
    (z : H) : U (A z)=B (U z) := by
  have h := unitary_square_graph_forward U G G' hg (A z) (z-A z) (ha z)
  have he := hb (U (A z)) (U (z-A z)) h
  simpa only [map_sub,add_sub_cancel] using he.symm

#print axioms unitary_square_graph_forward
#print axioms recognition_square_graph_forward
#print axioms unitary_recognizes_square_resolvent
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
