import TGLExt.F1Fecho394.CoefficientTomitaSquareR2
import TGLExt.F1Fecho394.FibreRootPointwiseR1
/-! Domain-exact coefficient graph for a general base resolvent. This avoids
unfolding the nested concrete Fock construction during the AE argument. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory
namespace F1Fecho.CoefficientPointwise
open TGLV350.Regular ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
open F1Fecho.RegularCovariantCore
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem graph_iff (T:H→ₗ.[ℂ]H) (J:H≃ₛₗᵢ[starRingEnd ℂ]H)
    (hJ:Function.Involutive J) (x y:H) :
    (x,y)∈CoefficientTomitaSquare.graph T J ↔ (x,J y)∈T.graph := by
  constructor
  · rintro ⟨u,hu⟩
    have hx:(u:H)=x:=congrArg Prod.fst hu
    have hy:J (T u)=y:=congrArg Prod.snd hu
    exact (LinearPMap.mem_graph_iff T).mpr ⟨u,hx,by rw [←hy,hJ]⟩
  · intro h
    obtain ⟨u,hx,hy⟩:=(LinearPMap.mem_graph_iff T).mp h
    refine ⟨u,Prod.ext hx ?_⟩
    change J (T u)=y
    rw [hy,hJ]

theorem graph_ae_direct (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1) (hi:Function.Injective R)
    (B:UnitaryFlow H) (J:H≃ₛₗᵢ[starRingEnd ℂ]H) (hJ:Function.Involutive J)
    (hBJ:∀a x,J (B.U a x)=B.U a (J x)) (f g:RegularHilbert H) :
    (f,g)∈CoefficientTomitaSquare.graph (FibreModularCalculus.liftedRoot R hR hi)
        (CoefficientTwistedConjugation.twist B J) ↔
      ∀ᵐ a:ℝ ∂volume,(f a,B.U a (g (-a)))∈
        CoefficientTomitaSquare.graph (resolventSquareRoot R hR hi) J := by
  rw [graph_iff _ _ (CoefficientTwistedConjugation.twist_involutive B J hJ hBJ)]
  rw [FibreRootPointwise.root_graph_ae R hR h1 hi]
  constructor
  · intro h
    filter_upwards [h,CoefficientTwistedConjugation.twist_ae B J g] with a ha hb
    apply (graph_iff _ _ hJ _ _).mpr
    rw [hBJ]
    rwa [←hb]
  · intro h
    filter_upwards [h,CoefficientTwistedConjugation.twist_ae B J g] with a ha hb
    have hh:=(graph_iff _ _ hJ _ _).mp ha
    rw [hBJ] at hh
    rwa [hb]

theorem graph_ae (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1) (hi:Function.Injective R)
    (B:UnitaryFlow H) (J:H≃ₛₗᵢ[starRingEnd ℂ]H) (hJ:Function.Involutive J)
    (hBJ:∀a x,J (B.U a x)=B.U a (J x)) (f g:RegularHilbert H) :
    (f,g)∈CoefficientTomitaSquare.graph (FibreModularCalculus.liftedRoot R hR hi)
        (CoefficientTwistedConjugation.twist B J) ↔
      ∀ᵐ a:ℝ ∂volume,(f (-a),B.U (-a) (g a))∈
        CoefficientTomitaSquare.graph (resolventSquareRoot R hR hi) J := by
  rw [graph_ae_direct R hR h1 hi B J hJ hBJ]
  constructor
  · intro h
    have hn:=(Measure.measurePreserving_neg (volume:Measure ℝ)).quasiMeasurePreserving.ae h
    filter_upwards [hn] with a ha
    simpa only [neg_neg] using ha
  · intro h
    have hn:=(Measure.measurePreserving_neg (volume:Measure ℝ)).quasiMeasurePreserving.ae h
    filter_upwards [hn] with a ha
    simpa only [neg_neg] using ha
end F1Fecho.CoefficientPointwise
#print axioms F1Fecho.CoefficientPointwise.graph_iff
#print axioms F1Fecho.CoefficientPointwise.graph_ae_direct
#print axioms F1Fecho.CoefficientPointwise.graph_ae
