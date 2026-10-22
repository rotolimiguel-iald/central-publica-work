import SmoothGeodesicFlow

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Flow017
open Filter Topology Set ChatgptAudit.Flow016 ChatgptAudit.Screen015 TGLExt
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

theorem zero_field_smooth_flow_control {E : Type*} [NormedAddCommGroup E]
    [NormedSpace ℝ E] [CompleteSpace E] (p : E) :
    ∃ F : LipschitzLocalFlow (fun _ : E => 0) univ p,
      ContDiffOn ℝ ∞ F.flow (Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius) ∧
      ∀ q∈Metric.ball p F.radius, ∀ t∈Ioo (-F.radius) F.radius, F.flow (q,t)=q := by
  let V := variationalLocalFlow univ isOpen_univ (fun _ : E => 0) contDiffOn_const p (mem_univ p)
  let F := projectedVariationalFlow V
  refine ⟨F,flow_smooth_on_domain F isOpen_univ contDiffOn_const,?_⟩
  intro q hq t ht
  exact zero_field_flow_constant V q hq t ht

theorem flat_geodesic_smooth_control (p : Phase4)
    (F : LocalPhaseFlow (geodesicSpray (fun _ => 0)) (regularPhaseDomain univ) p) :
    ContDiffOn ℝ ∞ F.flow (Metric.ball p F.radius ×ˢ Ioo (-F.radius) F.radius) := by
  have hpoly : ContDiff ℝ ∞
      (fun z : Phase4 × ℝ => (z.1.1+z.2 • z.1.2,z.1.2)) := by fun_prop
  apply hpoly.contDiffOn.congr
  intro z hz
  exact Prod.ext (zero_connection_position_affine p F z.1 hz.1 z.2 hz.2)
    (zero_connection_velocity_constant p F z.1 hz.1 z.2 hz.2)

theorem curved_smooth_null_flow_control :
    ∃ V : LocalPhaseFlow (geodesicSpray controlConformalConnection) (regularPhaseDomain univ)
      (0,horizonControlDirection),
      ContDiffOn ℝ ∞ V.flow
        (Metric.ball (0,horizonControlDirection) V.radius ×ˢ Ioo (-V.radius) V.radius) ∧
      (∀ t∈Ioo (-V.radius) V.radius,
        tensorQuad (controlConformalMetric (V.flow ((0,horizonControlDirection),t)).1)
          (V.flow ((0,horizonControlDirection),t)).2=0) ∧
      HasDerivAt (fun t => (V.flow ((0,horizonControlDirection),t)).2)
        ((-2:ℝ) • horizonControlDirection) 0 := by
  have hv : horizonControlDirection≠0 := by
    intro he
    have h0 := congrArg (fun v : Coordinate4 => v 0) he
    norm_num [horizonControlDirection] at h0
  let V := c1GeodesicFlow univ isOpen_univ controlConformalConnection
    Screen014.expanding_connection_smooth 0 horizonControlDirection (mem_univ _) hv
  have hp : ((0:Coordinate4),horizonControlDirection)∈
      Metric.ball ((0:Coordinate4),horizonControlDirection) V.radius :=
    Metric.mem_ball_self V.radius_positive
  have hn : tensorQuad (controlConformalMetric 0) horizonControlDirection=0 := by
    simpa [Screen014.expandingNullVelocity,Screen014.expandingFactor] using
      Screen014.expanding_velocity_null 0
  refine ⟨V,c1_geodesic_flow_smooth univ isOpen_univ controlConformalConnection
    Screen014.expanding_connection_smooth 0 horizonControlDirection (mem_univ _) hv,?_,?_⟩
  · intro t ht
    exact geodesic_flow_null_preserved univ isOpen_univ controlConformalMetric
      controlConformalConnection Screen014.expanding_metric_smooth Screen014.expanding_connection_compatible
      (0,horizonControlDirection) V (0,horizonControlDirection) hp hn t ht
  · have hd := geodesic_flow_velocity_derivative univ controlConformalConnection
      (0,horizonControlDirection) V (0,horizonControlDirection) hp 0
      ⟨neg_neg_of_pos V.radius_positive,V.radius_positive⟩
    rw [V.initial _ hp,conformal_spray_acceleration_zero] at hd
    exact hd

#print axioms zero_field_smooth_flow_control
#print axioms flat_geodesic_smooth_control
#print axioms curved_smooth_null_flow_control
end
end ChatgptAudit.Flow017
