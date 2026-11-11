import TGLExt.V350ScalarRightPairVector

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

private theorem rightGraphClosedContain {H A : Type*} [TopologicalSpace H]
    (D : Set H) (F : D → H) (v w : A → H)
    (hc : IsClosed (Set.range (fun y : D => ((y : H),F y))))
    (hv : ∀ a, ∃ ha : v a ∈ D, F ⟨v a,ha⟩ = w a) :
    closure (Set.range (fun a => (v a,w a))) ⊆
      Set.range (fun y : D => ((y : H),F y)) := by
  apply closure_minimal ?_ hc
  rintro _ ⟨a,rfl⟩
  obtain ⟨ha,he⟩ := hv a
  exact ⟨⟨v a,ha⟩,Prod.ext rfl he⟩

private theorem rightGraphNoVertical {H : Type*} [Zero H] [TopologicalSpace H]
    (D : Set H) (h0 : (0 : H) ∈ D) (F : D → H) (hF0 : F ⟨0,h0⟩ = 0)
    (G : Set (H × H)) (hG : closure G ⊆ Set.range (fun y : D => ((y : H),F y)))
    (z : H) (hz : (0,z) ∈ closure G) : z = 0 := by
  obtain ⟨y,hy⟩ := hG hz
  have hy0 : y = ⟨0,h0⟩ := Subtype.ext (congrArg Prod.fst hy)
  have he : F y = z := congrArg Prod.snd hy
  exact he.symm.trans ((congrArg F hy0).trans hF0)

/-- The vector norm is the GNS norm; the multiplier bound is its operator norm. -/
theorem scalarRightPairVector_product_bound (P : SiteProfile) (a b : scalarPairedRightAlgebra P) :
    ‖scalarRightPairVector P (a*b)‖ ≤ ‖a.val‖ * ‖scalarRightPairVector P b‖ := by
  exact (congrArg (fun x : ScalarGNSHilbert P => ‖x‖)
    (scalarRightPairVector_mul P a b)).le.trans (a.val.le_opNorm (scalarRightPairVector P b))

theorem scalarRightPairVector_inner_product (P : SiteProfile)
    (a b c : scalarPairedRightAlgebra P) :
    inner ℂ (scalarRightPairVector P (a*b)) (scalarRightPairVector P c) =
      inner ℂ (scalarRightPairVector P b) (scalarRightPairVector P (star a*c)) := by
  calc
    _ = inner ℂ (a.val (scalarRightPairVector P b)) (scalarRightPairVector P c) :=
      congrArg (fun x : ScalarGNSHilbert P => inner ℂ x (scalarRightPairVector P c))
        (scalarRightPairVector_mul P a b)
    _ = inner ℂ (scalarRightPairVector P b) (star a.val (scalarRightPairVector P c)) :=
      (a.val.adjoint_inner_right _ _).symm
    _ = _ := congrArg (fun x : ScalarGNSHilbert P => inner ℂ (scalarRightPairVector P b) x)
      (scalarRightPairVector_mul P (star a) c).symm

/-- Only the graph of the involution on actual right-pair vectors. -/
def scalarRightPairGraph (P : SiteProfile) : Set (ScalarGNSHilbert P × ScalarGNSHilbert P) :=
  Set.range (fun a : scalarPairedRightAlgebra P =>
    (scalarRightPairVector P a,scalarRightPairVector P (star a)))

/-- Inclusion in the original maximal graph is proved; equality is not asserted. -/
theorem scalarRightPairGraph_closure_subset_original (P : SiteProfile) :
    closure (scalarRightPairGraph P) ⊆ Set.range (fun y : scalarTomitaAdjointDomain P =>
      ((y : ScalarGNSHilbert P),scalarTomitaAdjoint P y)) := by
  exact rightGraphClosedContain (H := ScalarGNSHilbert P) (A := scalarPairedRightAlgebra P)
    (scalarTomitaAdjointDomain P : Set (ScalarGNSHilbert P)) (fun y => scalarTomitaAdjoint P y)
    (scalarRightPairVector P) (fun a => scalarRightPairVector P (star a))
    (scalarTomitaAdjoint_isClosed P) (scalarRightPairVector_original_adjoint P)

theorem scalarRightPairGraph_closable (P : SiteProfile) (z : ScalarGNSHilbert P)
    (hz : (0,z) ∈ closure (scalarRightPairGraph P)) : z = 0 := by
  exact rightGraphNoVertical (H := ScalarGNSHilbert P)
    (scalarTomitaAdjointDomain P : Set (ScalarGNSHilbert P)) (scalarTomitaAdjointDomain P).zero_mem
    (fun y => scalarTomitaAdjoint P y) (scalarTomitaAdjoint P).toFun.map_zero
    (scalarRightPairGraph P) (scalarRightPairGraph_closure_subset_original P) z hz

/-- Bounded approximate units from the already constructed commutant sandwiches. -/
def scalarRightPairApproximateUnit (P : SiteProfile) (h : ℝ) : scalarPairedRightAlgebra P :=
  if hh : 0 < h then
    ⟨scalarCommutantSandwich P 1 h,
      ⟨scalarCommutantSandwichPair P 1 (fun _ => Commute.one_left _) h hh⟩⟩
  else 0

theorem scalarRightPairApproximateUnit_tendsto (P : SiteProfile) (x : ScalarGNSHilbert P) :
    Tendsto (fun h : ℝ => (scalarRightPairApproximateUnit P h).val x)
      (𝓝[>] 0) (𝓝 x) := by
  have ht : Tendsto (fun h : ℝ => scalarCommutantSandwich P 1 h x)
      (𝓝[>] 0) (𝓝 x) := by
    simpa only [one_apply_eq_self] using scalarCommutantSandwich_tendsto P 1 x
  apply ht.congr'
  filter_upwards [self_mem_nhdsWithin] with h hh
  dsimp only [scalarRightPairApproximateUnit]
  split_ifs with hp
  · rfl
  · exact (hp hh).elim

/-- Products themselves are norm dense. This does not give a graph core for F. -/
theorem scalarRightPairVector_products_dense (P : SiteProfile) :
    Dense (Set.range (fun ab : scalarPairedRightAlgebra P × scalarPairedRightAlgebra P =>
      scalarRightPairVector P (ab.1*ab.2))) := by
  let products := Set.range (fun ab : scalarPairedRightAlgebra P × scalarPairedRightAlgebra P =>
    scalarRightPairVector P (ab.1*ab.2))
  have hr : Set.range (scalarRightPairVector P) ⊆ closure products := by
    rintro _ ⟨a,rfl⟩
    have ht : Tendsto (fun h : ℝ => scalarRightPairVector P (scalarRightPairApproximateUnit P h*a))
        (𝓝[>] 0) (𝓝 (scalarRightPairVector P a)) := by
      simpa only [scalarRightPairVector_mul] using
        scalarRightPairApproximateUnit_tendsto P (scalarRightPairVector P a)
    apply isClosed_closure.mem_of_tendsto ht
    exact Filter.Eventually.of_forall (fun h => subset_closure ⟨(scalarRightPairApproximateUnit P h,a),rfl⟩)
  intro x
  exact closure_minimal hr isClosed_closure ((scalarRightPairVector_denseRange P) x)

#print axioms scalarRightPairVector_product_bound
#print axioms scalarRightPairVector_inner_product
#print axioms scalarRightPairGraph
#print axioms scalarRightPairGraph_closure_subset_original
#print axioms scalarRightPairGraph_closable
#print axioms scalarRightPairApproximateUnit
#print axioms scalarRightPairApproximateUnit_tendsto
#print axioms scalarRightPairVector_products_dense
end
end TGLV350.Regular
