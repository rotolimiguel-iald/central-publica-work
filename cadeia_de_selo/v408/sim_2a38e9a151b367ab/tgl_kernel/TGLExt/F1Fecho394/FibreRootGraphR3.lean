import TGLExt.F1Fecho394.FibreModularCalculusR2
import TGLExt.V350ResolventSquareRoot

/-! Exact bounded regularized graph cores for the coefficient positive root. -/
set_option autoImplicit false
set_option maxHeartbeats 1400000
set_option synthInstance.maxHeartbeats 200000
set_option maxRecDepth 4000
noncomputable section
namespace F1Fecho.FibreRootGraph
open TGLV350.Regular ChatgptAudit.Continuous049
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem sqrt_damping_product (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1) :
    CFC.sqrt (resolventDampingOperator R)=CFC.sqrt R*CFC.sqrt (1-R) := by
  apply CFC.sqrt_unique
  · calc
      (CFC.sqrt R*CFC.sqrt (1-R))*(CFC.sqrt R*CFC.sqrt (1-R)) =
          CFC.sqrt R*(CFC.sqrt (1-R)*CFC.sqrt R)*CFC.sqrt (1-R) := by noncomm_ring
      _ = CFC.sqrt R*(CFC.sqrt R*CFC.sqrt (1-R))*CFC.sqrt (1-R) := by
        rw [←resolvent_sqrt_pair_commute R]
      _ = (CFC.sqrt R*CFC.sqrt R)*(CFC.sqrt (1-R)*CFC.sqrt (1-R)) := by noncomm_ring
      _ = resolventDampingOperator R := by
        rw [CFC.sqrt_mul_sqrt_self R hR,CFC.sqrt_mul_sqrt_self (1-R) (sub_nonneg.mpr h1)]
        rfl
  · exact Commute.mul_nonneg (CFC.sqrt_nonneg R) (CFC.sqrt_nonneg (1-R))
      (show Commute (CFC.sqrt R) (CFC.sqrt (1-R)) from resolvent_sqrt_pair_commute R)

theorem root_regularized_graph (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (hi:Function.Injective R) (x:H) :
    (R x,CFC.sqrt (resolventDampingOperator R) x)∈(resolventSquareRoot R hR hi).graph := by
  apply (bounded_graph_param_iff _ _ _ _ _).mpr
  refine ⟨CFC.sqrt R x,?_,?_⟩
  · change (CFC.sqrt R*CFC.sqrt R) x=R x
    rw [CFC.sqrt_mul_sqrt_self R hR]
  · change (CFC.sqrt (1-R)*CFC.sqrt R) x=CFC.sqrt (resolventDampingOperator R) x
    rw [sqrt_damping_product R hR h1,resolvent_sqrt_pair_commute]

local instance operatorRealModule : Module ℝ (RegularHilbert H →L[ℂ] RegularHilbert H) :=
  Module.restrictScalars ℝ ℂ (RegularHilbert H →L[ℂ] RegularHilbert H)

theorem fibre_sqrt (R:H→L[ℂ]H) (hR:0≤R) :
    (fibre (H:=H) (CFC.sqrt R) : RegularHilbert H→L[ℂ]RegularHilbert H)=
      CFC.sqrt (fibre (H:=H) R : RegularHilbert H→L[ℂ]RegularHilbert H) := by
  symm
  apply CFC.sqrt_unique
  · rw [←fibre_mul,CFC.sqrt_mul_sqrt_self R hR]
  · exact fibre_nonneg (CFC.sqrt_nonneg R)

theorem coefficient_root_regularized (R:H→L[ℂ]H) (hR:0≤R) (h1:R≤1)
    (hi:Function.Injective R) (f:RegularHilbert H) :
    (fibre R f,fibre (CFC.sqrt (resolventDampingOperator R)) f)∈
      (FibreModularCalculus.liftedRoot R hR hi).graph := by
  rw [fibre_sqrt _ (resolventDampingOperator_nonneg R hR h1),FibreModularCalculus.fibre_damping]
  exact root_regularized_graph _ (fibre_nonneg hR) (FibreModularCalculus.lifted_le_one R h1)
    (FibreModularCalculus.fibre_operator_injective R hi) f

end F1Fecho.FibreRootGraph
#print axioms F1Fecho.FibreRootGraph.sqrt_damping_product
#print axioms F1Fecho.FibreRootGraph.root_regularized_graph
#print axioms F1Fecho.FibreRootGraph.fibre_sqrt
#print axioms F1Fecho.FibreRootGraph.coefficient_root_regularized
