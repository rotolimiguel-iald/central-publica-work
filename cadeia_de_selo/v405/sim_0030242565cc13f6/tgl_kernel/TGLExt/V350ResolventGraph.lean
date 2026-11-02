import TGLExt.V350PositiveResolvent
import TGLExt.BoundedGraphOperator

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open ChatgptAudit.Continuous049
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def resolventGraphOperator (R : H →L[ℂ] H) (hi : Function.Injective R) : H →ₗ.[ℂ] H :=
  boundedGraphOperator R (1-R) hi

theorem resolvent_graph_commute (R : H →L[ℂ] H) : R*(1-R) = (1-R)*R := by
  simp only [mul_sub, sub_mul, mul_one, one_mul]

/-- The domain and graph are produced from the resolvent, not supplied as hypotheses. -/
theorem resolvent_graph_equation (R : H →L[ℂ] H) (hi : Function.Injective R) (x y : H) :
    (x,y) ∈ (resolventGraphOperator R hi).graph ↔ (1-R) x = R y := by
  rw [resolventGraphOperator, bounded_graph_param_iff]
  constructor
  · rintro ⟨u,rfl,rfl⟩
    exact (congrArg (fun B : H →L[ℂ] H => B u) (resolvent_graph_commute R)).symm
  · intro h
    have hx : R (x+y) = x := by
      change x-R x = R y at h
      rw [map_add, ← h]
      abel
    refine ⟨x+y,hx,?_⟩
    change x+y-R (x+y) = y
    rw [hx]
    abel

theorem resolvent_graph_closed (R : H →L[ℂ] H) (hi : Function.Injective R) :
    (resolventGraphOperator R hi).IsClosed := by
  have hg : ((resolventGraphOperator R hi).graph : Set (H×H)) =
      {p | (1-R) p.1 = R p.2} := by
    ext p
    exact resolvent_graph_equation R hi p.1 p.2
  change IsClosed ((resolventGraphOperator R hi).graph : Set (H×H))
  rw [hg]
  exact isClosed_eq ((1-R).continuous.comp continuous_fst) (R.continuous.comp continuous_snd)

theorem resolvent_graph_domain_dense (R : H →L[ℂ] H) (hi : Function.Injective R)
    (hR : IsSelfAdjoint R) : Dense ((resolventGraphOperator R hi).domain : Set H) :=
  bounded_graph_domain_dense R (1-R) hi hR

theorem resolvent_graph_selfadjoint (R : H →L[ℂ] H) (hi : Function.Injective R)
    (hR : IsSelfAdjoint R) : IsSelfAdjoint (resolventGraphOperator R hi) := by
  have hB : IsSelfAdjoint (1-R) := by
    change star (1-R) = 1-R
    rw [star_sub, star_one, hR.star_eq]
  have hd := resolvent_graph_domain_dense R hi hR
  have hf := bounded_graph_formal_adjoint R (1-R) hi hR hB (resolvent_graph_commute R)
  have ha : LinearPMap.adjoint (resolventGraphOperator R hi) ≤ resolventGraphOperator R hi := by
    apply LinearPMap.le_of_le_graph
    rintro ⟨x,y⟩ hp
    rw [LinearPMap.mem_graph_iff] at hp
    obtain ⟨u,hu,hv⟩ := hp
    apply (resolvent_graph_equation R hi x y).mpr
    apply ext_inner_right ℂ
    intro w
    have hh := LinearPMap.adjoint_isFormalAdjoint
      (T := resolventGraphOperator R hi) hd u (boundedGraphLift R (1-R) hi w)
    have hh' : inner ℂ y (R w) = inner ℂ x ((1-R) w) := by
      have hv' : (boundedGraphOperator R (1-R) hi).adjoint u = y := hv
      simpa only [resolventGraphOperator, bounded_graph_lift_coe,
        bounded_graph_lift_apply, hu, hv'] using hh
    calc
      inner ℂ ((1-R) x) w = inner ℂ x ((1-R) w) := bounded_graph_selfadjoint_inner _ hB x w
      _ = inner ℂ y (R w) := hh'.symm
      _ = inner ℂ (R y) w := (bounded_graph_selfadjoint_inner R hR y w).symm
  rw [LinearPMap.isSelfAdjoint_def]
  exact le_antisymm ha (hf.le_adjoint hd)

theorem resolvent_graph_positive (R : H →L[ℂ] H) (hi : Function.Injective R)
    (hR : 0 ≤ R) (hone : R ≤ 1) (x : (resolventGraphOperator R hi).domain) :
    0 ≤ (inner ℂ (x : H) (resolventGraphOperator R hi x)).re := by
  apply bounded_graph_positive R (1-R) hi
  intro u
  have hp := (ContinuousLinearMap.nonneg_iff_isPositive R).mp hR
  have hprod : 0 ≤ R*(1-R) := Commute.mul_nonneg hR (sub_nonneg.mpr hone)
    (show Commute R (1-R) from resolvent_graph_commute R)
  rw [hp.inner_left_eq_inner_right]
  exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hprod).re_inner_nonneg_right u

theorem resolvent_graph_resolvent_equation (R : H →L[ℂ] H) (hi : Function.Injective R)
    (u : H) : ∃ x : (resolventGraphOperator R hi).domain,
      (x : H) = R u ∧ (x : H) + resolventGraphOperator R hi x = u := by
  refine ⟨boundedGraphLift R (1-R) hi u, rfl, ?_⟩
  change R u + boundedGraphOperator R (1-R) hi (boundedGraphLift R (1-R) hi u) = u
  rw [bounded_graph_lift_apply]
  change R u + (u-R u) = u
  abel

#print axioms resolvent_graph_equation
#print axioms resolvent_graph_closed
#print axioms resolvent_graph_domain_dense
#print axioms resolvent_graph_selfadjoint
#print axioms resolvent_graph_positive
#print axioms resolvent_graph_resolvent_equation
end
end TGLV350.Regular
