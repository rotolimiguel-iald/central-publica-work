import TGLExt.V350ScalarGNSStarDensity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 900000

namespace TGLV350.Regular
open TGLExt
noncomputable section

theorem scalarGNSStarEmbedding_injective (P : SiteProfile) :
    Function.Injective (scalarGNSStarEmbedding P) := by
  intro A B h
  have he := scalarGNSEmbedding_injective P h
  exact Subtype.ext (congrArg (fun a : finiteDualLeftIdeal P => a.val) he)

/-- The initial involutive graph is concrete; no closure is taken here. -/
def scalarTomitaGraph (P : SiteProfile) : Set (ScalarGNSHilbert P × ScalarGNSHilbert P) :=
  Set.range (fun A : finiteDualStarCore P =>
    (scalarGNSStarEmbedding P A, scalarGNSStarEmbedding P (star A)))

theorem scalarTomitaGraph_single_valued (P : SiteProfile) (x y z : ScalarGNSHilbert P)
    (hy : (x,y) ∈ scalarTomitaGraph P) (hz : (x,z) ∈ scalarTomitaGraph P) : y = z := by
  obtain ⟨A,hA⟩ := hy
  obtain ⟨B,hB⟩ := hz
  have hab : A = B := scalarGNSStarEmbedding_injective P
    ((congrArg Prod.fst hA).trans (congrArg Prod.fst hB).symm)
  exact (congrArg Prod.snd hA).symm.trans
    ((congrArg (fun C : finiteDualStarCore P => scalarGNSStarEmbedding P (star C)) hab).trans
      (congrArg Prod.snd hB))

theorem scalarTomitaGraph_swap (P : SiteProfile) (p : ScalarGNSHilbert P × ScalarGNSHilbert P)
    (hp : p ∈ scalarTomitaGraph P) : p.swap ∈ scalarTomitaGraph P := by
  obtain ⟨A,rfl⟩ := hp
  exact ⟨star A, by simp only [star_star,Prod.swap_prod_mk]⟩

theorem scalarTomitaGraph_domain_dense (P : SiteProfile) :
    Dense (Prod.fst '' scalarTomitaGraph P) := by
  apply (scalarGNSStarEmbedding_denseRange P).mono
  rintro x ⟨A,rfl⟩
  exact ⟨(scalarGNSStarEmbedding P A,scalarGNSStarEmbedding P (star A)),⟨A,rfl⟩,rfl⟩

#print axioms scalarGNSStarEmbedding_injective
#print axioms scalarTomitaGraph
#print axioms scalarTomitaGraph_single_valued
#print axioms scalarTomitaGraph_swap
#print axioms scalarTomitaGraph_domain_dense
end
end TGLV350.Regular
