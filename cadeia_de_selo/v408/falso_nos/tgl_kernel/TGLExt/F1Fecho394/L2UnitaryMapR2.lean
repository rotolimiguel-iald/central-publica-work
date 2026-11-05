import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LpSpace.Complete
/-! Pointwise transport of L2 vectors by a prescribed Hilbert unitary. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
open MeasureTheory
namespace F1Fecho.L2UnitaryMap
variable {X E F : Type*} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]
variable (μ : Measure X) (U:E≃ₗᵢ[ℂ]F)

def map : Lp E 2 μ→ₗᵢ[ℂ]Lp F 2 μ where
  toLinearMap := (U.toLinearIsometry.toContinuousLinearMap.compLpL 2 μ).toLinearMap
  norm_map' f := by
    simp only [Lp.norm_def]
    congr 1
    apply eLpNorm_congr_norm_ae
    filter_upwards [U.toLinearIsometry.toContinuousLinearMap.coeFn_compLpL f] with x hx
    change ‖(U.toLinearIsometry.toContinuousLinearMap.compLpL 2 μ f) x‖=‖f x‖
    rw [hx]
    exact U.norm_map (f x)

theorem map_ae (f:Lp E 2 μ) : map μ U f =ᵐ[μ] fun x => U (f x) :=
  U.toLinearIsometry.toContinuousLinearMap.coeFn_compLpL f

theorem inverse (f:Lp E 2 μ) : map μ U.symm (map μ U f)=f := by
  apply Lp.ext
  filter_upwards [map_ae μ U.symm (map μ U f),map_ae μ U f] with x h1 h2
  rw [h1,h2,LinearIsometryEquiv.symm_apply_apply]

def unitary : Lp E 2 μ≃ₗᵢ[ℂ]Lp F 2 μ where
  toFun := map μ U
  map_add' := (map μ U).map_add
  map_smul' := (map μ U).map_smul
  norm_map' := (map μ U).norm_map
  invFun := map μ U.symm
  left_inv := inverse μ U
  right_inv := inverse μ U.symm

theorem unitary_ae (f:Lp E 2 μ) : unitary μ U f =ᵐ[μ] fun x => U (f x) := map_ae μ U f
end F1Fecho.L2UnitaryMap
#print axioms F1Fecho.L2UnitaryMap.inverse
#print axioms F1Fecho.L2UnitaryMap.unitary_ae
