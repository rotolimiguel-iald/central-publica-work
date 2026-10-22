import TGLExt.V350DualEnergyOnResolvent
import TGLExt.V350ResolventSquareRoot

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Elaborate CFC using only the generic complex Hilbert structure, as in
resolventSquareRoot, before specializing to the concrete Lp support. -/
def boundedPositiveSquareRoot (B : H →L[ℂ] H) : H →L[ℂ] H := CFC.sqrt B

theorem boundedPositiveSquareRoot_sq (B : H →L[ℂ] H) (hB : 0 ≤ B) :
    boundedPositiveSquareRoot B * boundedPositiveSquareRoot B = B :=
  CFC.sqrt_mul_sqrt_self B hB

def dualSupportSquareRoot
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    dualFormSupport A hA →ₗ.[ℂ] dualFormSupport A hA :=
  resolventSquareRoot (dualSupportResolvent A R hA hlim)
    (dualSupportResolvent_nonneg A R hA hR hlim)
    (dualSupportResolvent_injective A R hA hR hlim)

theorem dualSupportSquareRoot_domain
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    (dualSupportSquareRoot A R hA hR hlim).domain =
      (boundedPositiveSquareRoot (dualSupportResolvent A R hA hlim)).range := rfl

theorem dualSupportSquareRoot_closed
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    (dualSupportSquareRoot A R hA hR hlim).IsClosed :=
  resolventSquareRoot_closed _ _ _ (dualSupportResolvent_le_one A R hA hone hlim)

theorem dualSupportSquareRoot_dense
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    Dense ((dualSupportSquareRoot A R hA hR hlim).domain : Set (dualFormSupport A hA)) :=
  resolventSquareRoot_dense _ _ _

theorem dualSupportSquareRoot_selfadjoint
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    IsSelfAdjoint (dualSupportSquareRoot A R hA hR hlim) :=
  resolventSquareRoot_selfadjoint _ _ _ (dualSupportResolvent_le_one A R hA hone hlim)

theorem dualSupportSquareRoot_positive
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportSquareRoot A R hA hR hlim).domain) :
    0 ≤ (inner ℂ (x : dualFormSupport A hA) (dualSupportSquareRoot A R hA hR hlim x)).re :=
  resolventSquareRoot_positive _ _ _ x

theorem dualSupportSquareRoot_square
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    partialOperatorSquare (dualSupportSquareRoot A R hA hR hlim) =
      dualSupportOperator A R hA hR hlim :=
  resolventSquareRoot_square _ _ _ (dualSupportResolvent_le_one A R hA hone hlim)

/-- Agreement with the original dual form on D(T). Extension to all D(S)
and the converse inclusion of finite form domains are not asserted here. -/
theorem dualSupportSquareRoot_energy_on_operator_domain
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportOperator A R hA hR hlim).domain) :
    ∃ y : (dualSupportSquareRoot A R hA hR hlim).domain,
      (y : dualFormSupport A hA) = (x : dualFormSupport A hA) ∧
      dualQuadraticIntegral A (x : dualFormSupport A hA) =
        ENNReal.ofReal (‖dualSupportSquareRoot A R hA hR hlim y‖^2) := by
  let S := dualSupportSquareRoot A R hA hR hlim
  let T := dualSupportOperator A R hA hR hlim
  have hg : ((x : dualFormSupport A hA), T x) ∈ (partialOperatorSquare S).graph := by
    rw [dualSupportSquareRoot_square A R hA hR hone hlim]
    exact T.mem_graph x
  obtain ⟨z,hxz,hzT⟩ := (partialOperatorSquare_graph_iff S _ _).mp hg
  rw [LinearPMap.mem_graph_iff] at hxz hzT
  obtain ⟨u,hu,hSu⟩ := hxz
  obtain ⟨v,hv,hSv⟩ := hzT
  dsimp only [Prod.fst,Prod.snd] at hu hSu hv hSv
  have hf : S.IsFormalAdjoint S := resolventSquareRoot_formalAdjoint _ _ _
  have hin := hf u v
  rw [hSu,hv,hu,hSv] at hin
  have hr := congrArg Complex.re hin
  have hself : (inner ℂ z z).re = ‖z‖^2 := inner_self_eq_norm_sq (𝕜 := ℂ) z
  rw [hself] at hr
  refine ⟨u,hu,?_⟩
  rw [dualSupportOperator_energy_ennreal A R hA hR hlim x]
  change ENNReal.ofReal (inner ℂ (x : dualFormSupport A hA) (T x)).re =
    ENNReal.ofReal (‖S u‖^2)
  rw [hSu, hr]

theorem exists_dualSupportSquareRoot (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hmem : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :
    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P),
    ∃ T S : dualFormSupport A hA →ₗ.[ℂ] dualFormSupport A hA,
      R ∈ regularCoreAlgebra P ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      T.IsClosed ∧ Dense (T.domain : Set (dualFormSupport A hA)) ∧ IsSelfAdjoint T ∧
      S.IsClosed ∧ Dense (S.domain : Set (dualFormSupport A hA)) ∧ IsSelfAdjoint S ∧
      (∀ x : S.domain, 0 ≤ (inner ℂ (x : dualFormSupport A hA) (S x)).re) ∧
      partialOperatorSquare S = T ∧
      (∀ x : T.domain, ∃ y : S.domain,
        (y : dualFormSupport A hA) = (x : dualFormSupport A hA) ∧
        dualQuadraticIntegral A (x : dualFormSupport A hA) = ENNReal.ofReal (‖S y‖^2)) ∧
      (∀ u : dualFormSupport A hA, ∃ x : T.domain,
        ((x : dualFormSupport A hA) : RegularHilbert (TGLExt.TowerHilbert P)) = R u ∧
        (x : dualFormSupport A hA) + T x = u) := by
  obtain ⟨R,hmR,hR,hone,hlim,_⟩ := exists_dualResolvent_limit P A hmem hA
  refine ⟨R, dualSupportOperator A R hA hR hlim, dualSupportSquareRoot A R hA hR hlim,
    hmR,hR,hone,hlim, dualSupportOperator_closed A R hA hR hlim,
    dualSupportOperator_dense A R hA hR hlim, dualSupportOperator_selfadjoint A R hA hR hlim,
    dualSupportSquareRoot_closed A R hA hR hone hlim,
    dualSupportSquareRoot_dense A R hA hR hlim,
    dualSupportSquareRoot_selfadjoint A R hA hR hone hlim,
    dualSupportSquareRoot_positive A R hA hR hlim,
    dualSupportSquareRoot_square A R hA hR hone hlim,
    dualSupportSquareRoot_energy_on_operator_domain A R hA hR hone hlim, ?_⟩
  intro u
  obtain ⟨x,hx,heq⟩ := dualSupportOperator_resolvent_equation A R hA hR hlim u
  exact ⟨x,congrArg Subtype.val hx,heq⟩

#print axioms boundedPositiveSquareRoot
#print axioms boundedPositiveSquareRoot_sq
#print axioms dualSupportSquareRoot_domain
#print axioms dualSupportSquareRoot_closed
#print axioms dualSupportSquareRoot_dense
#print axioms dualSupportSquareRoot_selfadjoint
#print axioms dualSupportSquareRoot_positive
#print axioms dualSupportSquareRoot_square
#print axioms dualSupportSquareRoot_energy_on_operator_domain
#print axioms exists_dualSupportSquareRoot
end
end TGLV350.Regular
