import BoundedGraphOperator
import ClosedAntilinearStandardSubspace

set_option autoImplicit false
set_option maxHeartbeats 800000

namespace ChatgptAudit.Continuous049
open Complex ClosedSubmodule
noncomputable section
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- The anti-linear operator JT on the exact domain of the graph operator T. -/
def boundedGraphTomita (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    (boundedGraphOperator A B hAi).domain →ₛₗ[starRingEnd ℂ] H :=
  J.toLinearEquiv.toLinearMap.comp (boundedGraphOperator A B hAi).toFun

theorem bounded_graph_tomita_apply (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (x : (boundedGraphOperator A B hAi).domain) :
    boundedGraphTomita A B hAi J x = J (B (boundedGraphParameter A hAi x)) := rfl

theorem bounded_graph_tomita_lift (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJB : ∀ h, J (B h) = A (J h)) (h : H) :
    boundedGraphTomita A B hAi J (boundedGraphLift A B hAi h) = A (J h) := by
  rw [bounded_graph_tomita_apply, bounded_graph_parameter_lift, hJB]

theorem bounded_graph_tomita_maps_domain (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJB : ∀ h, J (B h) = A (J h))
    (x : (boundedGraphOperator A B hAi).domain) :
    boundedGraphTomita A B hAi J x ∈ (boundedGraphOperator A B hAi).domain := by
  refine ⟨J (boundedGraphParameter A hAi x), ?_⟩
  rw [bounded_graph_tomita_apply, hJB]
  rfl

theorem bounded_graph_tomita_involutive (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (hJB : ∀ h, J (B h) = A (J h)) (x : (boundedGraphOperator A B hAi).domain) :
    boundedGraphTomita A B hAi J
      ⟨boundedGraphTomita A B hAi J x, bounded_graph_tomita_maps_domain A B hAi J hJB x⟩
        = (x : H) := by
  have hy : (⟨boundedGraphTomita A B hAi J x,
      bounded_graph_tomita_maps_domain A B hAi J hJB x⟩ :
      (boundedGraphOperator A B hAi).domain) =
      boundedGraphLift A B hAi (J (boundedGraphParameter A hAi x)) := by
    apply Subtype.ext
    exact hJB (boundedGraphParameter A hAi x)
  rw [hy, bounded_graph_tomita_lift A B hAi J hJB, hJ, bounded_graph_parameter_apply]

theorem bounded_graph_tomita_closed (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (hcomm : A * B = B * A) (hsum : A * A + B * B = 1)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J) :
    IsClosed (Set.range (fun x : (boundedGraphOperator A B hAi).domain =>
      ((x : H), boundedGraphTomita A B hAi J x))) := by
  have heq : Set.range (fun x : (boundedGraphOperator A B hAi).domain =>
      ((x : H), boundedGraphTomita A B hAi J x)) =
      (fun p : H × H => (p.1, J p.2)) ⁻¹'
        ((boundedGraphOperator A B hAi).graph : Set (H × H)) := by
    ext p
    constructor
    · rintro ⟨x, rfl⟩
      change ((x : H), J (J (boundedGraphOperator A B hAi x))) ∈
        (boundedGraphOperator A B hAi).graph
      rw [hJ]
      exact (boundedGraphOperator A B hAi).mem_graph x
    · intro hp
      change (p.1, J p.2) ∈ (boundedGraphOperator A B hAi).graph at hp
      rw [LinearPMap.mem_graph_iff] at hp
      obtain ⟨x, hx, hy⟩ := hp
      refine ⟨x, Prod.ext hx ?_⟩
      change J (boundedGraphOperator A B hAi x) = p.2
      rw [hy, hJ]
  rw [heq]
  exact (bounded_graph_closed A B hAi hcomm hsum).preimage
    (continuous_fst.prodMk (J.continuous.comp continuous_snd))

theorem bounded_graph_J_tomita (A B : H →L[ℂ] H) (hAi : Function.Injective A)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (x : (boundedGraphOperator A B hAi).domain) :
    J (boundedGraphTomita A B hAi J x) = boundedGraphOperator A B hAi x :=
  hJ (boundedGraphOperator A B hAi x)

/-- A concrete standard subspace obtained from the bounded graph data. -/
def boundedGraphStandardSubspace [CompleteSpace H]
    (A B : H →L[ℂ] H) (hAi : Function.Injective A) (hA : IsSelfAdjoint A)
    (hcomm : A * B = B * A) (hsum : A * A + B * B = 1)
    (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (hJ : Function.Involutive J)
    (hJB : ∀ h, J (B h) = A (J h)) : StandardSubspace H :=
  closedAntilinearStandardSubspace
    (boundedGraphOperator A B hAi).domain (boundedGraphTomita A B hAi J)
    (bounded_graph_tomita_closed A B hAi hcomm hsum J hJ)
    (bounded_graph_tomita_maps_domain A B hAi J hJB)
    (bounded_graph_tomita_involutive A B hAi J hJ hJB)
    (bounded_graph_domain_dense A B hAi hA)

#print axioms boundedGraphTomita
#print axioms bounded_graph_tomita_apply
#print axioms bounded_graph_tomita_lift
#print axioms bounded_graph_tomita_maps_domain
#print axioms bounded_graph_tomita_involutive
#print axioms bounded_graph_tomita_closed
#print axioms bounded_graph_J_tomita
#print axioms boundedGraphStandardSubspace

end
end ChatgptAudit.Continuous049
