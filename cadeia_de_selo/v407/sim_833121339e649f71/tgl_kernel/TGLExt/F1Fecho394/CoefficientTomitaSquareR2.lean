import TGLExt.F1Fecho394.FibreModularCalculusR2
import TGLExt.F1Fecho394.CoefficientTwistedConjugationR1
import TGLExt.O16.RecognitionModular_v2

/-! Exact maximal-adjoint square of the coefficient operator.
The coefficient Hilbert space is concrete Lebesgue L2. Identification with
the actual weight GNS map and the pointwise base Tomita remain separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.CoefficientTomitaSquare
open TGLV350.Regular ChatgptAudit.Continuous050 ORDEM016.D6
open F1Fecho.FibreModularCalculus F1Fecho.CoefficientTwistedConjugation
open F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def graph (T : H→ₗ.[ℂ]H) (J : H≃ₛₗᵢ[starRingEnd ℂ]H) : Set (H×H) :=
  Set.range (fun x:T.domain => ((x:H),genericTomita T J x))

theorem square_graph (T : H→ₗ.[ℂ]H) (hT : IsSelfAdjoint T)
    (J : H≃ₛₗᵢ[starRingEnd ℂ]H) (hJ : Function.Involutive J) :
    antilinearSquareGraph (graph T J)=(partialOperatorSquare T).graph := by
  ext p
  rcases p with ⟨x,z⟩
  constructor
  · rintro ⟨sx,⟨u,hu⟩,hp⟩
    have hx : (u:H)=x := congrArg Prod.fst hu
    have hsx : genericTomita T J u=sx := congrArg Prod.snd hu
    obtain ⟨ha,hv⟩ := generic_adjoint_maximal T hT J hJ (y:=genericTomita T J u) (z:=z)
      (fun v => by rw [hsx]; exact (hp v (genericTomita T J v) ⟨v,rfl⟩).symm)
    have hTu := (generic_composition_domain T J hJ u).mp ha
    have ht : T ⟨T u,hTu⟩=z := (generic_adjoint_comp T J hJ u hTu).symm.trans hv
    apply (partialOperatorSquare_graph_iff T x z).mpr
    refine ⟨T u,?_,?_⟩
    · exact (LinearPMap.mem_graph_iff T).mpr ⟨u,hx,rfl⟩
    · exact (LinearPMap.mem_graph_iff T).mpr ⟨⟨T u,hTu⟩,rfl,ht⟩
  · intro hp
    obtain ⟨y,hxy,hyz⟩ := (partialOperatorSquare_graph_iff T x z).mp hp
    obtain ⟨u,hu,hy⟩ := (LinearPMap.mem_graph_iff T).mp hxy
    obtain ⟨v,hv,hz⟩ := (LinearPMap.mem_graph_iff T).mp hyz
    change (u:H)=x at hu
    change (T u:H)=y at hy
    change (v:H)=y at hv
    change (T v:H)=z at hz
    have hTu : T u∈T.domain := by rw [hy,←hv]; exact v.property
    have htv : (⟨T u,hTu⟩:T.domain)=v := Subtype.ext (hy.trans hv.symm)
    have hadj : genericTomitaAdjoint T J
        ⟨genericTomita T J u,(generic_composition_domain T J hJ u).mpr hTu⟩=z := by
      rw [generic_adjoint_comp T J hJ u hTu,htv]
      exact hz
    refine ⟨genericTomita T J u,⟨u,Prod.ext hu rfl⟩,?_⟩
    intro q sq hq
    obtain ⟨w,hw⟩ := hq
    have hwq : (w:H)=q := congrArg Prod.fst hw
    have hws : genericTomita T J w=sq := congrArg Prod.snd hw
    rw [←hwq,←hws,←hadj]
    exact (generic_adjoint_pairing T hT J hJ w
      ⟨genericTomita T J u,(generic_composition_domain T J hJ u).mpr hTu⟩).symm

def coefficientS (R : H→L[ℂ]H) (hR : 0≤R) (hi : Function.Injective R)
    (B : UnitaryFlow H) (J : H≃ₛₗᵢ[starRingEnd ℂ]H) :
    RegularHilbert H→ₛₗ.[starRingEnd ℂ]RegularHilbert H :=
  genericTomita (liftedRoot R hR hi) (twist B J)

theorem coefficient_square_graph (R : H→L[ℂ]H) (hR : 0≤R) (h1 : R≤1)
    (hi : Function.Injective R) (B : UnitaryFlow H) (J : H≃ₛₗᵢ[starRingEnd ℂ]H)
    (hJ : Function.Involutive J) (hBJ : ∀ a x, J (B.U a x)=B.U a (J x)) :
    antilinearSquareGraph (graph (liftedRoot R hR hi) (twist B J))=
      (resolventGraphOperator (fibre R) (fibre_operator_injective R hi)).graph := by
  rw [square_graph _ (liftedRoot_selfadjoint R hR h1 hi) _ (twist_involutive B J hJ hBJ),
    liftedRoot_square R hR h1 hi]

end F1Fecho.CoefficientTomitaSquare
#print axioms F1Fecho.CoefficientTomitaSquare.square_graph
#print axioms F1Fecho.CoefficientTomitaSquare.coefficientS
#print axioms F1Fecho.CoefficientTomitaSquare.coefficient_square_graph
