-- Supersedes source SHA256: f3db85a3bac49c07f32340f09b73c6452c3a52949ca5ef9f7e81319f70f38a51
import Lean
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Topology.Homeomorph.Lemmas

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace ORDEM016.D6
noncomputable section
open Set Topology
variable {H K : Type*}
  [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]

/-- The pair is specified independently. Its algebra and reference vector
are transported; no modular intertwining equation is a field. -/
structure ReconhecimentoPeloConteudo
    (M : StarSubalgebra ℂ (H →L[ℂ] H))
    (N : StarSubalgebra ℂ (K →L[ℂ] K)) (omega : H) (omega' : K) where
  U : H ≃ₗᵢ[ℂ] K
  reference : U omega = omega'
  algebra : ∀ A : H →L[ℂ] H, A ∈ M ↔ U.conjStarAlgEquiv A ∈ N

def pairTomitaGraph (M : StarSubalgebra ℂ (H →L[ℂ] H)) (omega : H) :
    Set (H × H) := {p | ∃ A : H →L[ℂ] H, A ∈ M ∧ p = (A omega, (star A) omega)}

variable {M : StarSubalgebra ℂ (H →L[ℂ] H)}
  {N : StarSubalgebra ℂ (K →L[ℂ] K)} {omega : H} {omega' : K}

def pairTransport (R : ReconhecimentoPeloConteudo M N omega omega') :
    (H × H) ≃ₜ (K × K) := R.U.toHomeomorph.prodCongr R.U.toHomeomorph

theorem recognition_on_vector (R : ReconhecimentoPeloConteudo M N omega omega')
    (A : H →L[ℂ] H) : R.U.conjStarAlgEquiv A omega' = R.U (A omega) := by
  calc
    _ = R.U.conjStarAlgEquiv A (R.U omega) :=
      congrArg (fun y : K => R.U.conjStarAlgEquiv A y) R.reference.symm
    _ = R.U (A omega) := by simp

theorem recognition_on_star_vector (R : ReconhecimentoPeloConteudo M N omega omega')
    (A : H →L[ℂ] H) : (star (R.U.conjStarAlgEquiv A)) omega' = R.U ((star A) omega) := by
  rw [← map_star R.U.conjStarAlgEquiv A]
  exact recognition_on_vector R (star A)

/-- Recognition transports the Tomita graph of the independently given pair. -/
theorem recognition_tomita_graph (R : ReconhecimentoPeloConteudo M N omega omega') :
    pairTransport R '' pairTomitaGraph M omega = pairTomitaGraph N omega' := by
  ext p
  constructor
  · rintro ⟨q, ⟨A, hA, rfl⟩, rfl⟩
    refine ⟨R.U.conjStarAlgEquiv A, (R.algebra A).mp hA, ?_⟩
    change (R.U (A omega), R.U ((star A) omega)) = _
    rw [recognition_on_vector R A, recognition_on_star_vector R A]
  · rintro ⟨B, hB, rfl⟩
    let A := R.U.conjStarAlgEquiv.symm B
    have ha : R.U.conjStarAlgEquiv A = B := R.U.conjStarAlgEquiv.apply_symm_apply B
    have hm : A ∈ M := (R.algebra A).mpr (ha.symm ▸ hB)
    refine ⟨(A omega, (star A) omega), ⟨A, hm, rfl⟩, ?_⟩
    change (R.U (A omega), R.U ((star A) omega)) = (B omega', (star B) omega')
    rw [← recognition_on_vector R A, ← recognition_on_star_vector R A, ha]

theorem recognition_closed_tomita_graph (R : ReconhecimentoPeloConteudo M N omega omega') :
    pairTransport R '' closure (pairTomitaGraph M omega) = closure (pairTomitaGraph N omega') := by
  rw [(pairTransport R).image_closure, recognition_tomita_graph R]

theorem recognition_closed_graph_membership (R : ReconhecimentoPeloConteudo M N omega omega')
    (x y : H) (h : (x,y) ∈ closure (pairTomitaGraph M omega)) :
    (R.U x,R.U y) ∈ closure (pairTomitaGraph N omega') := by
  rw [← recognition_closed_tomita_graph R]
  exact ⟨(x,y),h,rfl⟩

/-- Independently constructed closed operators are identified by their graphs.
The graph realization hypotheses are explicit; no Delta/J equation is assumed. -/
theorem recognition_identifies_closed_operator
    (R : ReconhecimentoPeloConteudo M N omega omega')
    (D : Set H) (E : Set K) (S : D → H) (T : E → K)
    (source_graph : Set.range (fun x : D => ((x : H),S x)) = closure (pairTomitaGraph M omega))
    (target_graph : Set.range (fun y : E => ((y : K),T y)) = closure (pairTomitaGraph N omega'))
    (x : D) : ∃ y : E, (y : K) = R.U x ∧ T y = R.U (S x) := by
  have hx : ((x : H),S x) ∈ closure (pairTomitaGraph M omega) := by
    rw [← source_graph]; exact ⟨x,rfl⟩
  have hy := recognition_closed_graph_membership R x (S x) hx
  rw [← target_graph] at hy
  obtain ⟨y,hy⟩ := hy
  exact ⟨y, congrArg Prod.fst hy, congrArg Prod.snd hy⟩

def identityByConstruction (M : StarSubalgebra ℂ (H →L[ℂ] H)) (omega : H) :
    ReconhecimentoPeloConteudo M M omega omega where
  U := LinearIsometryEquiv.refl ℂ H
  reference := rfl
  algebra := by intro A; simp

#print axioms recognition_on_vector
#print axioms recognition_on_star_vector
#print axioms recognition_tomita_graph
#print axioms recognition_closed_tomita_graph
#print axioms recognition_closed_graph_membership
#print axioms recognition_identifies_closed_operator
#print axioms identityByConstruction
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
