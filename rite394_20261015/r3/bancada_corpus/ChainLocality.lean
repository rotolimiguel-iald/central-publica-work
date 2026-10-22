import ChainSiteOperators

set_option autoImplicit false
set_option maxHeartbeats 800000
namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

theorem chain_local_mem_factor {I : Set ℕ} {x : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ chainLocalAlgebra P I) : x ∈ theFactorObject P := by
  have h : chainLocalAlgebra P I ≤ (theFactorObject P).toStarSubalgebra := by
    apply StarAlgebra.adjoin_le
    rintro a ⟨n,hn,b,rfl⟩
    exact siteOperator_mem_factor n b
  exact h hx

theorem chain_generators_commute {I J : Set ℕ} (h : Disjoint I J)
    {x y : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ chainGenerators P I) (hy : y ∈ chainGenerators P J) : x*y=y*x := by
  obtain ⟨n,hn,a,rfl⟩ := hx
  obtain ⟨m,hm,b,rfl⟩ := hy
  apply siteOperators_commute
  intro he
  subst m
  exact Set.disjoint_left.mp h hn hm

theorem chain_locality {I J : Set ℕ} (h : Disjoint I J)
    {x y : TowerHilbert P →L[ℂ] TowerHilbert P}
    (hx : x ∈ chainLocalAlgebra P I) (hy : y ∈ chainLocalAlgebra P J) : x*y=y*x := by
  have hI : chainLocalAlgebra P I ≤ StarSubalgebra.centralizer ℂ (chainGenerators P J) := by
    apply StarAlgebra.adjoin_le
    intro a ha
    change a ∈ StarSubalgebra.centralizer ℂ (chainGenerators P J)
    rw [StarSubalgebra.mem_centralizer_iff]
    intro b hb
    exact ⟨(chain_generators_commute h ha hb).symm,
      (chain_generators_commute h ha (chain_generators_star hb)).symm⟩
  have hJ : chainLocalAlgebra P J ≤ StarSubalgebra.centralizer ℂ (chainLocalAlgebra P I : Set _) := by
    apply StarAlgebra.adjoin_le
    intro b hb
    change b ∈ StarSubalgebra.centralizer ℂ (chainLocalAlgebra P I : Set _)
    rw [StarSubalgebra.mem_centralizer_iff]
    intro a ha
    have hc := hI ha
    have hs := hI (star_mem ha)
    rw [StarSubalgebra.mem_centralizer_iff] at hc hs
    exact ⟨(hc b hb).1.symm, (hs b hb).1.symm⟩
  have hc := hJ hy
  rw [StarSubalgebra.mem_centralizer_iff] at hc
  exact (hc x hx).1

theorem chain_empty : chainLocalAlgebra P ∅ = ⊥ := by
  unfold chainLocalAlgebra
  have hg : chainGenerators P ∅ = ∅ := by
    ext x
    simp [chainGenerators]
  rw [hg]
  exact le_antisymm (StarAlgebra.adjoin_le (Set.empty_subset _)) bot_le

#print axioms chain_local_mem_factor
#print axioms chain_locality
#print axioms chain_empty
end
end ChatgptAudit
