import NullCongruenceField

set_option autoImplicit false
set_option maxHeartbeats 7000000
namespace ChatgptAudit.Flow018
open Matrix Filter Topology Set ChatgptAudit.Flow016 ChatgptAudit.Flow017
  ChatgptAudit.Screen014 ChatgptAudit.Screen015
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem local_null_congruence_from_seed (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (Gamma : ConnectionField4) (hg : SmoothMatrixOn U g)
    (hG : SmoothConnectionOn U Gamma) (hm : MetricCompatibleOn U g Gamma)
    (W : VectorField4) (hW : ContDiffOn ℝ ∞ W U)
    (hn : ∀ x∈U, tensorQuad (g x) (W x)=0)
    (p v : Coordinate4) (hp : p∈U) (hv : v≠0) (hWp : W p=v) :
    ∃ N : Set Coordinate4, IsOpen N ∧ N⊆U ∧ p∈N ∧
      ∃ V : VectorField4, SmoothVectorOn N V ∧ V p=v ∧
        (∀ x∈N, V x≠0) ∧ (∀ x∈N, tensorQuad (g x) (V x)=0) ∧
        EqOn (vectorAcceleration Gamma V) (fun _ => 0) N := by
  obtain ⟨ell,hell⟩ := exists_normalized_covector v hv
  let F := variationalLocalFlow (regularPhaseDomain U) (regular_phase_domain_open U hU)
    (geodesicSpray Gamma) ((geodesic_spray_smooth U hU Gamma hG).mono (fun _ hz => hz.1))
    (p,v) ⟨hp,hv⟩
  let C := smoothLocalChart (shootingPosition F ell W) (shootingDomain F ell W)
    (shooting_domain_open F ell W) (shooting_phase_smooth F ell W hU hG hW).fst 0
    (shooting_domain_zero F ell W hU hW hp hWp)
    (shooting_position_derivative_zero F ell W hU hG hW hp hWp)
  refine ⟨C.chart.target,C.chart.open_target,congruence_target_subset F ell W C,
    congruence_base_mem F ell W C hWp,shootingCongruence F ell W C,
    congruence_smooth F ell W C hU hG hW,congruence_base_value F ell W C hWp,
    congruence_nonzero F ell W C,congruence_null F ell W C g hU hg hm hn,
    congruence_geodesic F ell W C hell hU hG hW⟩

theorem local_levi_civita_null_congruence (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (hAB : ∀ x∈U, A x*B x=1) (hBA : ∀ x∈U, B x*A x=1)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (p v : Coordinate4) (hp : p∈U) (hv : v≠0)
    (hn : tensorQuad (frameMetricField A p) v=0) :
    ∃ N : Set Coordinate4, IsOpen N ∧ N⊆U ∧ p∈N ∧
      ∃ V : VectorField4, SmoothVectorOn N V ∧ V p=v ∧
        (∀ x∈N, V x≠0) ∧ (∀ x∈N, tensorQuad (frameMetricField A x) (V x)=0) ∧
        EqOn (vectorAcceleration (frameLeviCivita A B) V) (fun _ => 0) N := by
  have hg := frame_metric_smooth U A hA
  have hG : SmoothConnectionOn U (frameLeviCivita A B) :=
    levi_civita_field_smooth U hU (frameMetricField A) (inverseFrameMetricField B)
      hg (inverse_frame_metric_smooth U B hB)
  have hm : MetricCompatibleOn U (frameMetricField A) (frameLeviCivita A B) :=
    levi_civita_field_metric_compatible U hU (frameMetricField A) (inverseFrameMetricField B)
      (fun x _ => frame_metric_symmetric A x)
      (fun x hx => inverse_frame_metric_left A B x (hAB x hx) (hBA x hx))
      (fun x hx => inverse_frame_metric_right A B x (hAB x hx) (hBA x hx))
  exact local_null_congruence_from_seed U hU (frameMetricField A) (frameLeviCivita A B)
    hg hG hm (transportedNullSeed A B p v) (transported_seed_smooth U A B hB p v)
    (fun x hx => transported_seed_null A B p v x (hAB x hx) hn)
    p v hp hv (transported_seed_initial A B p v (hBA p hp))

#print axioms local_null_congruence_from_seed
#print axioms local_levi_civita_null_congruence
end
end ChatgptAudit.Flow018
