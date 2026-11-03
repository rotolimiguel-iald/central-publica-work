import TGLExt.F1Fecho394.FibreRootGraphR3
import TGLExt.F1Fecho394.PositiveRegularizedRootR3

/-! The positive resolvent root equals the original positive self-adjoint
operator: regularized graph density and maximality prove domain equality. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.ResolventRootIdentification
open TGLV350.Regular ChatgptAudit.Continuous049 ChatgptAudit.UnboundedTransform016
open F1Fecho.FibreRootGraph
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem root_graph_core (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (hi:Function.Injective R) :
    closure (Set.range (fun x:H => (R x,CFC.sqrt (resolventDampingOperator R) x)))=
      (resolventSquareRoot R hR hi).graph := by
  apply Set.Subset.antisymm
  · apply closure_minimal _ (resolventSquareRoot_closed R hR hi h1)
    rintro _ ⟨x,rfl⟩
    exact root_regularized_graph R hR h1 hi x
  · rintro ⟨x,y⟩ hxy
    obtain ⟨u,hx,hy⟩ := (bounded_graph_param_iff _ _ _ x y).mp hxy
    have hd : DenseRange (CFC.sqrt R : H→L[ℂ]H) := resolventSquareRoot_dense R hR hi
    have hh : (CFC.sqrt R u,CFC.sqrt (1-R) u)∈
        closure (Set.range (fun x:H => (R x,CFC.sqrt (resolventDampingOperator R) x))) := by
      refine hd.induction ?_ (isClosed_closure.preimage
        ((CFC.sqrt R:H→L[ℂ]H).continuous.prodMk (CFC.sqrt (1-R):H→L[ℂ]H).continuous)) u
      rintro _ ⟨v,rfl⟩
      apply subset_closure
      refine ⟨v,?_⟩
      apply Prod.ext
      · change R v=(CFC.sqrt R*CFC.sqrt R) v
        rw [CFC.sqrt_mul_sqrt_self R hR]
      · change CFC.sqrt (resolventDampingOperator R) v=(CFC.sqrt (1-R)*CFC.sqrt R) v
        rw [sqrt_damping_product R hR h1,resolvent_sqrt_pair_commute]
    rwa [hx,hy] at hh

theorem selfadjoint_eq_of_graph_subset (T D:H→ₗ.[ℂ]H)
    (hT:IsSelfAdjoint T) (hD:IsSelfAdjoint D) (hs:T.graph≤D.graph) : T=D := by
  apply le_antisymm (LinearPMap.le_of_le_graph hs)
  have hf : T.IsFormalAdjoint D := by
    intro u v
    obtain ⟨w,hw,hv⟩ := (LinearPMap.mem_graph_iff D).mp (hs (T.mem_graph u))
    change (w:H)=(u:H) at hw
    change D w=T u at hv
    calc
      inner ℂ (T u) (v:H)=inner ℂ (D w) (v:H) := congrArg (fun z:H=>inner ℂ z (v:H)) hv.symm
      _ = inner ℂ (w:H) (D v) := selfadjoint_formal D hD w v
      _ = inner ℂ (u:H) (D v) := congrArg (fun z:H=>inner ℂ z (D v)) hw
  have he : T.adjoint=T := hT
  simpa only [he] using hf.le_adjoint hT.dense_domain

theorem root_eq_positive (D:H→ₗ.[ℂ]H) (hs:IsSelfAdjoint D)
    (hp:∀x:D.domain,0≤(inner ℂ (x:H) (D x)).re) :
    resolventSquareRoot (selfadjointSquareResolvent D hs)
      (selfadjoint_square_resolvent_nonneg D hs)
      (selfadjoint_square_resolvent_injective D hs)=D := by
  apply selfadjoint_eq_of_graph_subset _ D
    (resolventSquareRoot_selfadjoint _ _ _ (selfadjoint_square_resolvent_le_one D hs)) hs
  change ((resolventSquareRoot (selfadjointSquareResolvent D hs)
    (selfadjoint_square_resolvent_nonneg D hs)
    (selfadjoint_square_resolvent_injective D hs)).graph : Set (H×H)) ⊆ D.graph
  rw [←root_graph_core _ _ (selfadjoint_square_resolvent_le_one D hs)]
  apply closure_minimal _ hs.isClosed
  rintro _ ⟨x,rfl⟩
  exact PositiveRegularized.regularized_graph D hs hp x
end F1Fecho.ResolventRootIdentification
#print axioms F1Fecho.ResolventRootIdentification.root_graph_core
#print axioms F1Fecho.ResolventRootIdentification.selfadjoint_eq_of_graph_subset
#print axioms F1Fecho.ResolventRootIdentification.root_eq_positive
