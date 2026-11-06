import TGLExt.F1Fecho394.CoefficientFockConjugationR2
import TGLExt.F1Fecho394.FibreRootPointwiseR1
import TGLExt.F1Fecho394.ResolventRootIdentificationR2

/-! Exact AE graph of the coefficient Tomita on the SAME Fock.
This identifies its full L2 domain with the fibrewise Weyl-vacuum Tomita graph.
It does not assume or assert the weight-GNS identification. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory
namespace F1Fecho.CoefficientFockPointwise
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.ExponentialTomita
open F1Fecho.Antilinear F1Fecho.CanonicalFockPolar F1Fecho.ExponentialLift
open F1Fecho.CoefficientFockConjugation F1Fecho.CanonicalFockRegular
open TGLV350.Regular ChatgptAudit.Continuous049 ChatgptAudit.Continuous050

theorem generic_graph_iff {H:Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (T:H→ₗ.[ℂ]H)
    (J:H≃ₛₗᵢ[starRingEnd ℂ]H) (hJ:Function.Involutive J) (x y:H) :
    (x,y)∈CoefficientTomitaSquare.graph T J ↔ (x,J y)∈T.graph := by
  constructor
  · rintro ⟨u,hu⟩
    have hx:(u:H)=x := congrArg Prod.fst hu
    have hy:J (T u)=y := congrArg Prod.snd hu
    apply (LinearPMap.mem_graph_iff T).mpr
    refine ⟨u,hx,?_⟩
    rw [←hy,hJ]
  · intro h
    obtain ⟨u,hx,hy⟩ := (LinearPMap.mem_graph_iff T).mp h
    refine ⟨u,Prod.ext hx ?_⟩
    change J (T u)=y
    rw [hy,hJ]

theorem base_root_eq : resolventSquareRoot modularR modularR_nonneg modularR_injective=
    canonicalLift :=
  ResolventRootIdentification.root_eq_positive canonicalLift canonicalLift_selfadjoint
    ExponentialLiftPositive.canonicalLift_positive

theorem actual_graph_iff (x y:F) : (x,y)∈actualGraph ↔ (x,JF y)∈canonicalLift.graph := by
  rw [actualGraph_eq]
  exact generic_graph_iff canonicalLift JF canonicalFockJ_involutive x y

theorem coefficient_graph_ae_direct (f g:RegularHilbert F) :
    (f,g)∈CoefficientTomitaSquare.graph coefficientRoot coefficientJ ↔
      ∀ᵐ a:ℝ ∂volume,(f a,fockFlow.U a (g (-a)))∈actualGraph := by
  rw [generic_graph_iff _ _ coefficientJ_involutive]
  rw [FibreRootPointwise.root_graph_ae modularR modularR_nonneg modularR_le_one modularR_injective]
  rw [base_root_eq]
  constructor
  · intro h
    filter_upwards [h,CoefficientTwistedConjugation.twist_ae fockFlow JF g] with a ha hb
    apply (actual_graph_iff _ _).mpr
    rw [JF_boost]
    change coefficientJ g a=fockFlow.U a (JF (g (-a))) at hb
    rwa [←hb]
  · intro h
    filter_upwards [h,CoefficientTwistedConjugation.twist_ae fockFlow JF g] with a ha hb
    have hh:=(actual_graph_iff _ _).mp ha
    rw [JF_boost] at hh
    change coefficientJ g a=fockFlow.U a (JF (g (-a))) at hb
    rwa [hb]

theorem coefficient_graph_ae (f g:RegularHilbert F) :
    (f,g)∈CoefficientTomitaSquare.graph coefficientRoot coefficientJ ↔
      ∀ᵐ a:ℝ ∂volume,(f (-a),fockFlow.U (-a) (g a))∈actualGraph := by
  rw [coefficient_graph_ae_direct]
  constructor
  · intro h
    have hn := (Measure.measurePreserving_neg (volume:Measure ℝ)).quasiMeasurePreserving.ae h
    filter_upwards [hn] with a ha
    simpa only [neg_neg] using ha
  · intro h
    have hn := (Measure.measurePreserving_neg (volume:Measure ℝ)).quasiMeasurePreserving.ae h
    filter_upwards [hn] with a ha
    simpa only [neg_neg] using ha
end F1Fecho.CoefficientFockPointwise
#print axioms F1Fecho.CoefficientFockPointwise.generic_graph_iff
#print axioms F1Fecho.CoefficientFockPointwise.base_root_eq
#print axioms F1Fecho.CoefficientFockPointwise.actual_graph_iff
#print axioms F1Fecho.CoefficientFockPointwise.coefficient_graph_ae_direct
#print axioms F1Fecho.CoefficientFockPointwise.coefficient_graph_ae
