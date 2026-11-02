import TGLExt.V350DualSupportTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2000000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem selfadjoint_commutes_star_of_commute (R U : H →L[ℂ] H)
    (hR : IsSelfAdjoint R) (h : Commute R U) : Commute R (star U) := by
  change R * star U = star U * R
  simpa only [star_mul,hR.star_eq] using congrArg star h.eq.symm

theorem graph_transport_iff_of_left_inverse (T : H →ₗ.[ℂ] H) (U V : H →L[ℂ] H)
    (hVU : ∀ x, V (U x) = x)
    (hU : ∀ x y, (x,y) ∈ T.graph → (U x,U y) ∈ T.graph)
    (hV : ∀ x y, (x,y) ∈ T.graph → (V x,V y) ∈ T.graph)
    (x y : H) : (U x,U y) ∈ T.graph ↔ (x,y) ∈ T.graph := by
  constructor
  · intro hg
    simpa only [hVU] using hV (U x) (U y) hg
  · exact hU x y

theorem dualSupportCommutingMap_star_cancel
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (U : unitary (RegularHilbert H →L[ℂ] RegularHilbert H)) (h : Commute R U.val)
    (hs : Commute R (star U).val) (x : dualFormSupport A hA) :
    dualSupportCommutingMap A R (star U).val hA hR hlim hs
      (dualSupportCommutingMap A R U.val hA hR hlim h x) = x := by
  apply Subtype.ext
  exact congrArg (fun B : RegularHilbert H →L[ℂ] RegularHilbert H => B x)
    (Unitary.coe_star_mul_self U)

theorem dualSupportOperator_unitary_graph_iff
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (U : unitary (RegularHilbert H →L[ℂ] RegularHilbert H)) (h : Commute R U.val)
    (x y : dualFormSupport A hA) :
    (dualSupportCommutingMap A R U.val hA hR hlim h x,
      dualSupportCommutingMap A R U.val hA hR hlim h y) ∈
      (dualSupportOperator A R hA hR hlim).graph ↔
      (x,y) ∈ (dualSupportOperator A R hA hR hlim).graph := by
  have hs := selfadjoint_commutes_star_of_commute R U.val (IsSelfAdjoint.of_nonneg hR) h
  exact graph_transport_iff_of_left_inverse _ _
    (dualSupportCommutingMap A R (star U).val hA hR hlim hs)
    (dualSupportCommutingMap_star_cancel A R hA hR hlim U h hs)
    (dualSupportOperator_graph_transport A R U.val hA hR hlim h)
    (dualSupportOperator_graph_transport A R (star U).val hA hR hlim hs) x y

theorem dualSupportSquareRoot_unitary_graph_iff
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (U : unitary (RegularHilbert H →L[ℂ] RegularHilbert H)) (h : Commute R U.val)
    (x y : dualFormSupport A hA) :
    (dualSupportCommutingMap A R U.val hA hR hlim h x,
      dualSupportCommutingMap A R U.val hA hR hlim h y) ∈
      (dualSupportSquareRoot A R hA hR hlim).graph ↔
      (x,y) ∈ (dualSupportSquareRoot A R hA hR hlim).graph := by
  have hs := selfadjoint_commutes_star_of_commute R U.val (IsSelfAdjoint.of_nonneg hR) h
  exact graph_transport_iff_of_left_inverse _ _
    (dualSupportCommutingMap A R (star U).val hA hR hlim hs)
    (dualSupportCommutingMap_star_cancel A R hA hR hlim U h hs)
    (dualSupportSquareRoot_graph_transport A R U.val hA hR hlim h)
    (dualSupportSquareRoot_graph_transport A R (star U).val hA hR hlim hs) x y

/-- Finite-energy invariance is recovered from the same root graph.
No invariance of the form is assumed in this lemma. -/
theorem dualQuadraticIntegral_finite_unitary_commuting
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (U : unitary (RegularHilbert H →L[ℂ] RegularHilbert H)) (h : Commute R U.val)
    (w : RegularHilbert H) (hw : dualQuadraticIntegral A w < ⊤) :
    dualQuadraticIntegral A (U.val w) = dualQuadraticIntegral A w := by
  let S := dualSupportSquareRoot A R hA hR hlim
  let V := dualSupportCommutingMap A R U.val hA hR hlim h
  obtain ⟨x,hx⟩ := (dualQuadraticIntegral_finite_iff_squareRoot_domain
    A R hA hR hone hlim w).mp hw
  have hg := dualSupportSquareRoot_graph_transport A R U.val hA hR hlim h
    (x : dualFormSupport A hA) (S x) (S.mem_graph x)
  rw [LinearPMap.mem_graph_iff] at hg
  obtain ⟨z,hzx,hzs⟩ := hg
  change (z : dualFormSupport A hA) = V x at hzx
  change S z = V (S x) at hzs
  have hz : ((z : dualFormSupport A hA) : RegularHilbert H) = U.val w := by
    calc
      _ = ((V x : dualFormSupport A hA) : RegularHilbert H) := congrArg Subtype.val hzx
      _ = U.val w := congrArg U.val hx
  have hn : ‖S z‖ = ‖S x‖ := by
    rw [hzs]
    change ‖U.val ((S x : dualFormSupport A hA) : RegularHilbert H)‖ =
      ‖((S x : dualFormSupport A hA) : RegularHilbert H)‖
    exact Unitary.norm_map U _
  calc
    dualQuadraticIntegral A (U.val w) = dualQuadraticIntegral A (z : dualFormSupport A hA) :=
      congrArg (dualQuadraticIntegral A) hz.symm
    _ = ENNReal.ofReal (‖S z‖^2) := dualSupportSquareRoot_form_eq A R hA hR hone hlim z
    _ = ENNReal.ofReal (‖S x‖^2) := by rw [hn]
    _ = dualQuadraticIntegral A (x : dualFormSupport A hA) :=
      (dualSupportSquareRoot_form_eq A R hA hR hone hlim x).symm
    _ = dualQuadraticIntegral A w := congrArg (dualQuadraticIntegral A) hx

/-- The inverse unitary controls the infinite part as well: invariance is
an equality in ENNReal on the entire ambient Hilbert space. -/
theorem dualQuadraticIntegral_unitary_commuting
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (U : unitary (RegularHilbert H →L[ℂ] RegularHilbert H)) (h : Commute R U.val)
    (w : RegularHilbert H) :
    dualQuadraticIntegral A (U.val w) = dualQuadraticIntegral A w := by
  by_cases hw : dualQuadraticIntegral A w < ⊤
  · exact dualQuadraticIntegral_finite_unitary_commuting A R hA hR hone hlim U h w hw
  · have hstar : Commute R (star U).val :=
      selfadjoint_commutes_star_of_commute R U.val (IsSelfAdjoint.of_nonneg hR) h
    have hback : (star U).val (U.val w) = w :=
      congrArg (fun B : RegularHilbert H →L[ℂ] RegularHilbert H => B w)
        (Unitary.coe_star_mul_self U)
    have hUw : ¬ dualQuadraticIntegral A (U.val w) < ⊤ := by
      intro hfinite
      have he := dualQuadraticIntegral_finite_unitary_commuting A R hA hR hone hlim
        (star U) hstar (U.val w) hfinite
      rw [hback] at he
      exact hw (he.symm ▸ hfinite)
    exact (top_le_iff.mp (le_of_not_gt hUw)).trans (top_le_iff.mp (le_of_not_gt hw)).symm

/-- Invariance under the larger commutant of the fixed-point algebra,
not merely under the commutant of the continuous core. -/
theorem dualQuadraticIntegral_fixed_commutant_invariant (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hmem : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A)
    (U : unitary (RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P)))
    (hU : ∀ B ∈ dualFixedCore P, U.val * B = B * U.val)
    (w : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualQuadraticIntegral A (U.val w) = dualQuadraticIntegral A w := by
  obtain ⟨R,hmR,hR,hone,hlim,hfixed⟩ := exists_dualResolvent_fixed P A hmem hA
  have hmF : R ∈ dualFixedCore P := (dualFixedCore_mem_iff P R).mpr ⟨hmR,hfixed⟩
  exact dualQuadraticIntegral_unitary_commuting A R hA hR hone hlim U (hU R hmF).symm w

/-- A form-valued element affiliated with the actual fixed algebra.
Identification of that algebra with the original base remains separate. -/
def dualFixedAffiliatedPositiveForm (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hmem : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :
    AffiliatedPositiveForm (dualFixedCore P) where
  toClosedPositiveForm := dualClosedPositiveForm A hA
  unitary_commutant_invariant :=
    dualQuadraticIntegral_fixed_commutant_invariant P A hmem hA

theorem dualFixedAffiliatedPositiveForm_value (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hmem : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A)
    (w : RegularHilbert (TGLExt.TowerHilbert P)) :
    (dualFixedAffiliatedPositiveForm P A hmem hA).value w = dualQuadraticIntegral A w := rfl

#print axioms selfadjoint_commutes_star_of_commute
#print axioms graph_transport_iff_of_left_inverse
#print axioms dualSupportCommutingMap_star_cancel
#print axioms dualSupportOperator_unitary_graph_iff
#print axioms dualSupportSquareRoot_unitary_graph_iff
#print axioms dualQuadraticIntegral_finite_unitary_commuting
#print axioms dualQuadraticIntegral_unitary_commuting
#print axioms dualQuadraticIntegral_fixed_commutant_invariant
#print axioms dualFixedAffiliatedPositiveForm
#print axioms dualFixedAffiliatedPositiveForm_value
end
end TGLV350.Regular
