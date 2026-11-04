import TGLExt.F1Fecho394.SpectralUnitaryTransportR1
import TGLExt.V350ResolventSquareRoot

/-! Unitary transport of the actual unbounded positive root, including its domain. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.UnitaryRootGraphTransport
open TGLV350.Regular ChatgptAudit.Continuous049 F1Fecho.SpectralTransport
variable {H E : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (V : H ≃ₗᵢ[ℂ] E) (R : H →L[ℂ] H)

theorem sqrt_operator (hR : 0 ≤ R) :
    V.conjStarAlgEquiv (CFC.sqrt R) = CFC.sqrt (transported V R) := by
  have hp : 0 ≤ V.conjStarAlgEquiv (CFC.sqrt R) :=
    map_nonneg V.conjStarAlgEquiv (CFC.sqrt_nonneg R)
  apply (CFC.mul_self_eq_mul_self_iff _ _ hp (CFC.sqrt_nonneg _)).mp
  rw [←map_mul,CFC.sqrt_mul_sqrt_self R hR,
    CFC.sqrt_mul_sqrt_self _ (nonneg V R hR)]
  rfl

theorem sqrt_apply (hR : 0 ≤ R) (x : H) :
    V (CFC.sqrt R x) = CFC.sqrt (transported V R) (V x) := by
  have h := congrArg (fun A : E→L[ℂ]E => A (V x)) (sqrt_operator V R hR)
  simpa only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
    LinearIsometryEquiv.symm_apply_apply] using h

theorem complement_sqrt_apply (h1 : R ≤ 1) (x : H) :
    V (CFC.sqrt (1-R) x) = CFC.sqrt (1-transported V R) (V x) := by
  have h := sqrt_apply V (1-R) (sub_nonneg.mpr h1) x
  simpa only [transported,map_sub,map_one] using h

theorem root_graph_iff (hR : 0 ≤ R) (h1 : R ≤ 1) (hi : Function.Injective R)
    (x y : H) :
    (V x,V y) ∈ (resolventSquareRoot (transported V R)
      (nonneg V R hR) (injective V R hi)).graph ↔
    (x,y) ∈ (resolventSquareRoot R hR hi).graph := by
  change (V x,V y) ∈ (boundedGraphOperator (CFC.sqrt (transported V R))
    (CFC.sqrt (1-transported V R)) _).graph ↔
    (x,y) ∈ (boundedGraphOperator (CFC.sqrt R) (CFC.sqrt (1-R)) _).graph
  rw [bounded_graph_param_iff,bounded_graph_param_iff]
  constructor
  · rintro ⟨z,hx,hy⟩
    obtain ⟨u,rfl⟩ := V.surjective z
    exact ⟨u,V.injective ((sqrt_apply V R hR u).trans hx),
      V.injective ((complement_sqrt_apply V R h1 u).trans hy)⟩
  · rintro ⟨u,hx,hy⟩
    exact ⟨V u,(sqrt_apply V R hR u).symm.trans (congrArg V hx),
      (complement_sqrt_apply V R h1 u).symm.trans (congrArg V hy)⟩
end F1Fecho.UnitaryRootGraphTransport
#print axioms F1Fecho.UnitaryRootGraphTransport.sqrt_operator
#print axioms F1Fecho.UnitaryRootGraphTransport.sqrt_apply
#print axioms F1Fecho.UnitaryRootGraphTransport.complement_sqrt_apply
#print axioms F1Fecho.UnitaryRootGraphTransport.root_graph_iff
