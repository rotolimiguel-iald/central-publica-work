import TGLExt.F1Fecho394.CanonicalFockPolarR1
import TGLExt.F1Fecho394.PartialSquareClosedR3
/-! The actual S†S operator on canonical Fock is closed and selfadjoint.
Its bounded graph parameters are GA² and GB²; no false square-sum identity
for second quantization is used. Imaginary powers remain a separate task. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.CanonicalFockPolar
open F1Rede.BosonicFock F1Rede.CanonicalWedge F1Fecho.ExponentialLift F1Fecho.GammaGraph
open ChatgptAudit.Continuous049

def GA2 : F →L[ℂ] F := GA * GA
def GB2 : F →L[ℂ] F := GB * GB

theorem GA2_selfadjoint : IsSelfAdjoint GA2 := by
  apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
  intro x y
  change inner ℂ (GA (GA x)) y = inner ℂ x (GA (GA y))
  exact (GA_selfadjoint.isSymmetric (GA x) y).trans (GA_selfadjoint.isSymmetric x (GA y))
theorem GB2_selfadjoint : IsSelfAdjoint GB2 := by
  apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
  intro x y
  change inner ℂ (GB (GB x)) y = inner ℂ x (GB (GB y))
  exact (GB_selfadjoint.isSymmetric (GB x) y).trans (GB_selfadjoint.isSymmetric x (GB y))
theorem GAB2_commute : GA2 * GB2 = GB2 * GA2 := by
  have h : Commute GA GB := GAB_commute
  simpa only [GA2,GB2,pow_two] using (h.pow_pow 2 2).eq
theorem GA2_injective : Function.Injective GA2 := by
  intro x y h
  exact GA_injective (GA_injective h)

theorem delta_graph_parameters (x : F) : (GA2 x,GB2 x) ∈ Delta.graph := by
  apply (PartialSquare.square_graph_iff_two canonicalLift _ _).mpr
  have hc : GB (GA x) = GA (GB x) :=
    congrArg (fun L : F →L[ℂ] F => L x) GAB_commute.symm
  refine ⟨GA (GB x),?_,?_⟩
  · have h := graph_parameters (GA x)
    rw [hc] at h
    exact h
  · exact graph_parameters (GB x)

theorem delta_dense : Dense (Delta.domain : Set F) := by
  have hd := bounded_graph_domain_dense GA2 GB2 GA2_injective GA2_selfadjoint
  apply hd.mono
  rintro x ⟨y,rfl⟩
  obtain ⟨z,hz,_⟩ := (LinearPMap.mem_graph_iff Delta).mp (delta_graph_parameters y)
  have hz' : (z:F) = GA2 y := hz
  change GA2 y ∈ Delta.domain
  exact hz' ▸ z.property

theorem delta_closed : Delta.IsClosed :=
  PartialSquare.square_closed canonicalLift canonicalLift_closed
    (closedLift_isFormalAdjoint TW TW_selfadjoint)

theorem delta_selfadjoint : IsSelfAdjoint Delta :=
  BoundedGraphSelfAdjoint.selfAdjoint_of_bounded_pair Delta delta_closed
    (PartialSquare.square_formalAdjoint canonicalLift
      (closedLift_isFormalAdjoint TW TW_selfadjoint)) delta_dense
    GA2 GB2 GA2_selfadjoint GB2_selfadjoint GAB2_commute GA2_injective delta_graph_parameters

/-- Positive selfadjoint square root, with exact composition domain from the prior module. -/
theorem modular_positive_square_root :
    IsSelfAdjoint canonicalLift ∧
    (∀ x : canonicalLift.domain, 0 ≤ (inner ℂ (x:F) (canonicalLift x)).re) ∧
    PartialSquare.square canonicalLift = Delta ∧ IsSelfAdjoint Delta :=
  ⟨canonicalLift_selfadjoint,ExponentialLiftPositive.canonicalLift_positive,rfl,delta_selfadjoint⟩

end F1Fecho.CanonicalFockPolar
#print axioms F1Fecho.CanonicalFockPolar.delta_graph_parameters
#print axioms F1Fecho.CanonicalFockPolar.delta_dense
#print axioms F1Fecho.CanonicalFockPolar.delta_closed
#print axioms F1Fecho.CanonicalFockPolar.delta_selfadjoint
#print axioms F1Fecho.CanonicalFockPolar.modular_positive_square_root
