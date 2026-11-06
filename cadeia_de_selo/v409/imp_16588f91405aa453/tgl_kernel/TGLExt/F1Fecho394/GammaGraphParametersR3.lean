import TGLExt.F1Fecho394.BoundedGammaPropertiesR2
import TGLExt.F1Fecho394.ExponentialLiftR2
/-! Concrete bounded graph parameters for the unbounded canonical Fock lift.
The one-particle square-sum identity is used only to bound WA and WB. Its
second-quantized analogue is NOT assumed and is not generally true. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.GammaGraph
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.Exponential F1Fecho.ExponentialLift F1Fecho.BoundedGamma
open ChatgptAudit.Continuous049

theorem WAB_norm_sq (c : ℝ) (f : H1) : ‖WA c f‖^2 + ‖WB c f‖^2 = ‖f‖^2 := by
  have h := congrArg (fun L : H1 →L[ℂ] H1 => inner ℂ f (L f)) (WAB_square_sum c)
  simp only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
    ContinuousLinearMap.one_apply,inner_add_right] at h
  have ha : inner ℂ (WA c f) (WA c f) = inner ℂ f (WA c (WA c f)) :=
    (WA_selfadjoint c).isSymmetric f (WA c f)
  have hb : inner ℂ (WB c f) (WB c f) = inner ℂ f (WB c (WB c f)) :=
    (WB_selfadjoint c).isSymmetric f (WB c f)
  rw [← ha,← hb] at h
  have hr := congrArg Complex.re h
  simpa [inner_self_eq_norm_sq_to_K,← Complex.ofReal_pow] using hr

theorem WA_norm_le (c : ℝ) : ‖WA c‖ ≤ 1 := by
  apply (WA c).opNorm_le_bound (by norm_num)
  intro f
  have h := WAB_norm_sq c f
  have hn := norm_nonneg (WA c f)
  have hf := norm_nonneg f
  nlinarith [sq_nonneg ‖WB c f‖]

theorem WB_norm_le (c : ℝ) : ‖WB c‖ ≤ 1 := by
  apply (WB c).opNorm_le_bound (by norm_num)
  intro f
  have h := WAB_norm_sq c f
  have hn := norm_nonneg (WB c f)
  have hf := norm_nonneg f
  nlinarith [sq_nonneg ‖WA c f‖]

theorem WA_denseRange (c : ℝ) : DenseRange (WA c) :=
  bounded_graph_domain_dense (WA c) (WB c) (WA_injective c) (WA_selfadjoint c)

def GA : F →L[ℂ] F := BoundedGamma.gamma (WA rootParameter) (WA_norm_le rootParameter)
def GB : F →L[ℂ] F := BoundedGamma.gamma (WB rootParameter) (WB_norm_le rootParameter)

theorem GA_selfadjoint : IsSelfAdjoint GA :=
  gamma_selfadjoint _ _ (WA_selfadjoint rootParameter)
theorem GB_selfadjoint : IsSelfAdjoint GB :=
  gamma_selfadjoint _ _ (WB_selfadjoint rootParameter)
theorem GAB_commute : GA * GB = GB * GA :=
  gamma_commute _ _ _ _ (WAB_commute rootParameter)
theorem GA_denseRange : DenseRange GA :=
  gamma_denseRange _ _ (WA_denseRange rootParameter)
theorem GA_injective : Function.Injective GA :=
  gamma_injective _ _ (WA_selfadjoint rootParameter) (WA_denseRange rootParameter)

theorem graph_parameters_exponential (f : H1) :
    (GA (exponential f),GB (exponential f)) ∈ closedGraph TW := by
  change (BoundedGamma.gamma _ _ (exponential f),BoundedGamma.gamma _ _ (exponential f)) ∈ _
  rw [BoundedGamma.gamma_exponential,BoundedGamma.gamma_exponential]
  apply (coreGraph TW).le_topologicalClosure
  apply Submodule.subset_span
  let v : TW.domain := boundedGraphLift (WA rootParameter) (WB rootParameter)
    (WA_injective rootParameter) f
  refine ⟨v,?_⟩
  apply Prod.ext
  · rfl
  · change exponential (TW v) = exponential (WB rootParameter f)
    congr 1
    exact bounded_graph_lift_apply _ _ _ f

theorem graph_parameters (x : F) : (GA x,GB x) ∈ canonicalLift.graph := by
  let L : F →L[ℂ] F × F := GA.prod GB
  let M := (closedGraph TW).comap L.toLinearMap
  have hs : Submodule.span ℂ (Set.range exponential) ≤ M := by
    apply Submodule.span_le.mpr
    rintro _ ⟨f,rfl⟩
    exact graph_parameters_exponential f
  have hc : IsClosed (M : Set F) :=
    (coreGraph TW).isClosed_topologicalClosure.preimage L.continuous
  have ht := (Submodule.span ℂ (Set.range exponential)).topologicalClosure_minimal hs hc
  rw [exponential_total] at ht
  have hx : (GA x,GB x) ∈ closedGraph TW := ht (Submodule.mem_top (x := x))
  change (GA x,GB x) ∈ (closedLift TW TW_selfadjoint).graph
  rw [closedLift_graph_eq]
  exact hx

end F1Fecho.GammaGraph
#print axioms F1Fecho.GammaGraph.WAB_norm_sq
#print axioms F1Fecho.GammaGraph.WA_norm_le
#print axioms F1Fecho.GammaGraph.WB_norm_le
#print axioms F1Fecho.GammaGraph.GA_selfadjoint
#print axioms F1Fecho.GammaGraph.GB_selfadjoint
#print axioms F1Fecho.GammaGraph.GAB_commute
#print axioms F1Fecho.GammaGraph.GA_injective
#print axioms F1Fecho.GammaGraph.graph_parameters
