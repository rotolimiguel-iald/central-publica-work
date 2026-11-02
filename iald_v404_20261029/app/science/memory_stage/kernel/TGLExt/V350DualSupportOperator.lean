import TGLExt.V350DualFormSupport
import TGLExt.V350ResolventGraph

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def dualFormSupport (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    Submodule ℂ (RegularHilbert H) := (dualClosedPositiveForm A hA).finiteDomain.topologicalClosure

instance dualFormSupport_complete (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    CompleteSpace (dualFormSupport A hA) := by
  unfold dualFormSupport
  infer_instance

theorem dualResolvent_maps_into_support
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) : R v ∈ dualFormSupport A hA :=
  Submodule.le_topologicalClosure _ (dualResolvent_limit_range_finite A R hA hlim v)

def dualSupportResolvent
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    dualFormSupport A hA →L[ℂ] dualFormSupport A hA :=
  R.restrict (fun v _ => dualResolvent_maps_into_support A R hA hlim v)

theorem dualSupportResolvent_apply
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : dualFormSupport A hA) :
    (dualSupportResolvent A R hA hlim v : RegularHilbert H) = R v := rfl

theorem dualSupportResolvent_nonneg
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    0 ≤ dualSupportResolvent A R hA hlim := by
  rw [ContinuousLinearMap.nonneg_iff_isPositive, ContinuousLinearMap.isPositive_iff_complex]
  intro v
  exact (ContinuousLinearMap.isPositive_iff_complex R).mp
    ((ContinuousLinearMap.nonneg_iff_isPositive R).mp hR) (v : RegularHilbert H)

theorem dualSupportResolvent_le_one
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    dualSupportResolvent A R hA hlim ≤ 1 := by
  rw [← sub_nonneg, ContinuousLinearMap.nonneg_iff_isPositive,
    ContinuousLinearMap.isPositive_iff_complex]
  intro v
  exact (ContinuousLinearMap.isPositive_iff_complex (1-R)).mp
    ((ContinuousLinearMap.nonneg_iff_isPositive _).mp (sub_nonneg.mpr hone)) (v : RegularHilbert H)

/-- Injectivity is proved only after restriction to the support constructed from q_A. -/
theorem dualSupportResolvent_injective
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    Function.Injective (dualSupportResolvent A R hA hlim) := by
  apply LinearMap.ker_eq_bot.mp
  apply eq_bot_iff.mpr
  intro v hv
  have hvzero : R (v : RegularHilbert H) = 0 := congrArg Subtype.val hv
  have hvker : (v : RegularHilbert H) ∈ R.ker := hvzero
  rw [dualResolvent_kernel_eq_finiteDomain_orthogonal A R hA hR hlim] at hvker
  have hvorth : (v : RegularHilbert H) ∈ (dualFormSupport A hA)ᗮ := by
    simpa only [dualFormSupport, Submodule.orthogonal_closure] using hvker
  have hinner := (dualFormSupport A hA).inner_right_of_mem_orthogonal v.property hvorth
  have hz : (v : RegularHilbert H) = 0 := inner_self_eq_zero.mp hinner
  exact Subtype.ext hz

/-- A densely defined positive self-adjoint operator on the actual support.
Its square-root form has not yet been identified with q_A. -/
def dualSupportOperator
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    dualFormSupport A hA →ₗ.[ℂ] dualFormSupport A hA :=
  resolventGraphOperator (dualSupportResolvent A R hA hlim)
    (dualSupportResolvent_injective A R hA hR hlim)

theorem dualSupportOperator_closed
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    (dualSupportOperator A R hA hR hlim).IsClosed := resolvent_graph_closed _ _

theorem dualSupportOperator_dense
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    Dense ((dualSupportOperator A R hA hR hlim).domain : Set (dualFormSupport A hA)) :=
  resolvent_graph_domain_dense _ _ (IsSelfAdjoint.of_nonneg (dualSupportResolvent_nonneg A R hA hR hlim))

theorem dualSupportOperator_selfadjoint
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    IsSelfAdjoint (dualSupportOperator A R hA hR hlim) :=
  resolvent_graph_selfadjoint _ _ (IsSelfAdjoint.of_nonneg (dualSupportResolvent_nonneg A R hA hR hlim))

theorem dualSupportOperator_positive
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R) (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportOperator A R hA hR hlim).domain) :
    0 ≤ (inner ℂ (x : dualFormSupport A hA) (dualSupportOperator A R hA hR hlim x)).re :=
  resolvent_graph_positive _ _ (dualSupportResolvent_nonneg A R hA hR hlim)
    (dualSupportResolvent_le_one A R hA hone hlim) x

theorem dualSupportOperator_resolvent_equation
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (u : dualFormSupport A hA) :
    ∃ x : (dualSupportOperator A R hA hR hlim).domain,
      (x : dualFormSupport A hA) = dualSupportResolvent A R hA hlim u ∧
      (x : dualFormSupport A hA) + dualSupportOperator A R hA hR hlim x = u :=
  resolvent_graph_resolvent_equation _ _ u

/-- Existence in the actual regular representation. No limit operator or domain
is supplied as a hypothesis. Identification of the square-root form remains open. -/
theorem exists_dualSupportOperator (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hmem : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :
    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P),
    ∃ T : dualFormSupport A hA →ₗ.[ℂ] dualFormSupport A hA,
      R ∈ regularCoreAlgebra P ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      T.IsClosed ∧ Dense (T.domain : Set (dualFormSupport A hA)) ∧
      IsSelfAdjoint T ∧
      (∀ x : T.domain, 0 ≤ (inner ℂ (x : dualFormSupport A hA) (T x)).re) ∧
      (∀ u : dualFormSupport A hA, ∃ x : T.domain,
        ((x : dualFormSupport A hA) : RegularHilbert (TGLExt.TowerHilbert P)) = R u ∧
        (x : dualFormSupport A hA) + T x = u) := by
  obtain ⟨R, hmR, hR, hone, hlim, _⟩ := exists_dualResolvent_limit P A hmem hA
  refine ⟨R, dualSupportOperator A R hA hR hlim, hmR, hR, hone, hlim,
    dualSupportOperator_closed A R hA hR hlim,
    dualSupportOperator_dense A R hA hR hlim,
    dualSupportOperator_selfadjoint A R hA hR hlim,
    dualSupportOperator_positive A R hA hR hone hlim, ?_⟩
  intro u
  obtain ⟨x, hx, heq⟩ := dualSupportOperator_resolvent_equation A R hA hR hlim u
  exact ⟨x, congrArg Subtype.val hx, heq⟩

#print axioms exists_dualSupportOperator
#print axioms dualResolvent_maps_into_support
#print axioms dualSupportResolvent_apply
#print axioms dualSupportResolvent_nonneg
#print axioms dualSupportResolvent_le_one
#print axioms dualSupportResolvent_injective
#print axioms dualSupportOperator_closed
#print axioms dualSupportOperator_dense
#print axioms dualSupportOperator_selfadjoint
#print axioms dualSupportOperator_positive
#print axioms dualSupportOperator_resolvent_equation
end
end TGLV350.Regular
