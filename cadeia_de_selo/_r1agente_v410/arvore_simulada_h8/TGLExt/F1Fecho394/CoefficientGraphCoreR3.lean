import TGLExt.F1Fecho394.LpPairTransportR3
import TGLExt.F1Fecho394.LpClosedSubspaceCoreR3
import TGLExt.F1Fecho394.RealTomitaGraphR3
import TGLExt.F1Fecho394.CoefficientPointwiseR1

/-! Interval vectors in a dense base Tomita graph are a coefficient graph core.
The target closed real graph is arbitrary. This proves a genuine graph-norm
core implication; it does not assert that a GNS graph has those generators. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open MeasureTheory
namespace F1Fecho.CoefficientGraphCore
open TGLV350.Regular ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
open F1Fecho.RegularCovariantCore LpPairTransport RealLpGraphCore
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
local instance : InnerProductSpace ℝ H := InnerProductSpace.complexToReal

theorem interval_lift {E F:Type} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]
    (A:E→L[ℝ]F) (a b:ℝ) (v:E) :
    A.compLpL 2 (volume:Measure ℝ) (intervalVector a b v)=intervalVector a b (A v) := by
  apply Lp.ext
  filter_upwards [A.coeFn_compLpL (intervalVector a b v),
    indicatorConstLp_coeFn (p:=2) (hs:=measurableSet_Ioc)
      (hμs:=by simp [Real.volume_Ioc]) (c:=v),
    indicatorConstLp_coeFn (p:=2) (hs:=measurableSet_Ioc)
      (hμs:=by simp [Real.volume_Ioc]) (c:=A v)] with t ht hv hw
  change intervalVector a b v t = _ at hv
  change intervalVector a b (A v) t = _ at hw
  rw [ht,hv,hw]
  by_cases h:t∈Set.Ioc a b
  · simp only [Set.indicator_of_mem h]
  · simp only [Set.indicator_of_notMem h,map_zero]

theorem decode_interval (B:UnitaryFlow H) (a b:ℝ) (v:PairH H) :
    decode B (intervalVector a b v)=
      (intervalVector a b (WithLp.ofLp v).1,
       CoefficientConjugation.reflection
        (CoefficientBoost.multiplier B (-1) (intervalVector a b (WithLp.ofLp v).2))) := by
  apply Prod.ext
  · exact interval_lift ((WithLp.fstL 2 ℂ H H).restrictScalars ℝ) a b v
  · change CoefficientConjugation.reflection
      (CoefficientBoost.multiplier B (-1) (sndMap (intervalVector a b v)))=_
    have hs : sndMap (intervalVector a b v)=intervalVector a b (WithLp.ofLp v).2 :=
      interval_lift ((WithLp.sndL 2 ℂ H H).restrictScalars ℝ) a b v
    rw [hs]

theorem coefficient_mem_of_dense_intervals
    (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1) (hi:Function.Injective R)
    (B:UnitaryFlow H) (J:H≃ₛₗᵢ[starRingEnd ℂ]H) (hJ:Function.Involutive J)
    (hBJ:∀a x,J (B.U a x)=B.U a (J x))
    (D:Set (PairH H))
    (hD:closure D=(RealTomitaGraph.graph (resolventSquareRoot R hR hi) J:Set (PairH H)))
    (N:Submodule ℝ (RegularHilbert H×RegularHilbert H))
    (hN:IsClosed (N:Set (RegularHilbert H×RegularHilbert H)))
    (hI:∀a b v,v∈D→decode B (intervalVector a b v)∈N)
    (f g:RegularHilbert H)
    (hfg:(f,g)∈CoefficientTomitaSquare.graph (FibreModularCalculus.liftedRoot R hR hi)
        (CoefficientTwistedConjugation.twist B J)) : (f,g)∈N := by
  let G:=RealTomitaGraph.graph (resolventSquareRoot R hR hi) J
  have hG:IsClosed (G:Set (PairH H)):=RealTomitaGraph.graph_closed _
    (resolventSquareRoot_closed R hR hi h1) J hJ
  letI : CompleteSpace G:=hG.completeSpace_coe
  let A:PairLp H→L[ℝ](RegularHilbert H×RegularHilbert H):=(decode B).restrictScalars ℝ
  have hg:∀ᵐ a:ℝ ∂volume,encode B f g a∈G := by
    have hh:=(CoefficientPointwise.graph_ae_direct R hR h1 hi B J hJ hBJ f g).mp hfg
    filter_upwards [hh,encode_ae B f g] with a ha hb
    change encode B f g a∈RealTomitaGraph.graph _ _
    rw [RealTomitaGraph.mem_graph,hb]
    exact ha
  have hm:=LpClosedSubspaceCore.mem_of_dense_interval_values G D hD
    (N.comap A.toLinearMap) (hN.preimage A.continuous) hI (encode B f g) hg
  change decode B (encode B f g)∈N at hm
  rwa [decode_encode] at hm

end F1Fecho.CoefficientGraphCore
#print axioms F1Fecho.CoefficientGraphCore.interval_lift
#print axioms F1Fecho.CoefficientGraphCore.decode_interval
#print axioms F1Fecho.CoefficientGraphCore.coefficient_mem_of_dense_intervals
