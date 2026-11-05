import TGLExt.F1Fecho394.RegularScalarGNSR3
import Mathlib.Algebra.Star.NonUnitalSubalgebra
/-! The initial involutive scalar-weight graph, on the actual finite-square
star domain. Density and closure are distinct conclusions, not fields. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularScalarTomitaGraph
open TGLV350.Regular F1Fecho.RegularScalarGNS
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : Context H)

def finiteStarCore : NonUnitalStarSubalgebra ℂ D.algebra.toStarSubalgebra where
  carrier := {A | HasFiniteDualSquare A.val ∧ HasFiniteDualSquare (star A.val)}
  zero_mem' := by constructor <;> simpa using (HasFiniteDualSquare.zero (H := H))
  add_mem' := by
    intro A B hA hB
    change HasFiniteDualSquare (A.val+B.val) ∧ HasFiniteDualSquare (star (A.val+B.val))
    exact ⟨HasFiniteDualSquare.add _ _ hA.1 hB.1,
      by simpa only [star_add] using HasFiniteDualSquare.add _ _ hA.2 hB.2⟩
  mul_mem' := by
    intro A B hA hB
    change HasFiniteDualSquare (A.val*B.val) ∧ HasFiniteDualSquare (star (A.val*B.val))
    exact ⟨HasFiniteDualSquare.left_mul _ _ hB.1,
      by simpa only [star_mul] using HasFiniteDualSquare.left_mul (star B.val) (star A.val) hA.2⟩
  smul_mem' := by
    intro c A hA
    change HasFiniteDualSquare (c • A.val) ∧ HasFiniteDualSquare (star (c • A.val))
    exact ⟨HasFiniteDualSquare.smul c _ hA.1,
      by simpa only [star_smul] using HasFiniteDualSquare.smul (star c) _ hA.2⟩
  star_mem' := by
    intro A hA
    change HasFiniteDualSquare (star A.val) ∧ HasFiniteDualSquare (star (star A.val))
    exact ⟨hA.2,by simpa only [star_star] using hA.1⟩

def scalarGNSStarEmbedding (A : finiteStarCore D) : GNSHilbert D :=
  GNSEmbedding D ⟨A.val,A.property.1⟩

theorem scalarGNSStarEmbedding_injective : Function.Injective (scalarGNSStarEmbedding D) := by
  intro A B h
  have he := GNSEmbedding_injective D h
  exact Subtype.ext (congrArg (fun a : finiteIdeal D => a.val) he)

def scalarTomitaGraph : Set (GNSHilbert D × GNSHilbert D) :=
  Set.range (fun A : finiteStarCore D =>
    (scalarGNSStarEmbedding D A, scalarGNSStarEmbedding D (star A)))

theorem scalarTomitaGraph_single_valued (x y z : GNSHilbert D)
    (hy : (x,y) ∈ scalarTomitaGraph D) (hz : (x,z) ∈ scalarTomitaGraph D) : y=z := by
  obtain ⟨A,hA⟩ := hy
  obtain ⟨B,hB⟩ := hz
  have hab : A=B := scalarGNSStarEmbedding_injective D
    ((congrArg Prod.fst hA).trans (congrArg Prod.fst hB).symm)
  exact (congrArg Prod.snd hA).symm.trans
    ((congrArg (fun C : finiteStarCore D => scalarGNSStarEmbedding D (star C)) hab).trans
      (congrArg Prod.snd hB))

theorem scalarTomitaGraph_swap (p : GNSHilbert D × GNSHilbert D)
    (hp : p ∈ scalarTomitaGraph D) : p.swap ∈ scalarTomitaGraph D := by
  obtain ⟨A,rfl⟩ := hp
  exact ⟨star A,by simp only [star_star,Prod.swap_prod_mk]⟩

end F1Fecho.RegularScalarTomitaGraph
#print axioms F1Fecho.RegularScalarTomitaGraph.finiteStarCore
#print axioms F1Fecho.RegularScalarTomitaGraph.scalarGNSStarEmbedding
#print axioms F1Fecho.RegularScalarTomitaGraph.scalarGNSStarEmbedding_injective
#print axioms F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph
#print axioms F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph_single_valued
#print axioms F1Fecho.RegularScalarTomitaGraph.scalarTomitaGraph_swap
