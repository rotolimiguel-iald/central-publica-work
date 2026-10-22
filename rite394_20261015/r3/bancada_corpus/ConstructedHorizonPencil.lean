import ScreenClausiusCoefficient

set_option autoImplicit false
set_option maxHeartbeats 7500000
namespace ChatgptAudit.Flow020
open Matrix Filter Topology Set ChatgptAudit.Flow019
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section

variable {U : Set Coordinate4} {g : TensorField4} {Gamma : ConnectionField4} {p v : Coordinate4}
  (P : EquilibriumScreenData U g Gamma p v) (T : TensorField4) (rate eta : ℝ)

def horizonPencilFromScreen (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (hrate : rate≠0)
    (hbalance : Tendsto (fun t => horizonBalancePrimitive rate eta
        (inducedArea g P.curve P.screen.vectors) (constructedHeat P T rate hU hg hT) t/t^2)
      (𝓝[<] 0) (𝓝 0)) :
    GeometricHorizonPencil U g Gamma T eta p v where
  neighborhood := P.neighborhood
  neighborhood_open := P.neighborhood_open
  neighborhood_subset := P.neighborhood_subset
  point_mem := P.point_mem
  velocity := P.velocity
  velocity_smooth := P.velocity_smooth
  velocity_at_point := P.velocity_at_point
  velocity_null := P.velocity_null
  geodesic := P.geodesic
  equilibrium_gradient := P.equilibrium_gradient
  curve := P.curve
  curve_zero := P.curve_zero
  curve_tangent := P.curve_tangent
  rate := rate
  rate_nonzero := hrate
  screen := P.screen
  area_positive_zero := by
    rw [P.screen_gram_zero]
    norm_num [Matrix.det_fin_two]
  heat := constructedHeat P T rate hU hg hT
  heat_continuous := (constructed_heat_continuous P T rate hU hg hT).continuousAt
  heat_zero := constructed_heat_zero P T rate hU hg hT
  heat_rate := constructed_heat_rate P T rate hU hg hT
  clausius_to_second_order := hbalance

include P in
theorem null_balance_produces_pencil (hU : IsOpen U) (hg : SmoothMatrixOn U g)
    (hG : SmoothConnectionOn U Gamma)
    (hT : ∀ a b, DifferentiableOn ℝ (fun y => T y a b) U)
    (ht : ∀ i j a, Gamma p i a j=Gamma p j a i)
    (hrate : rate≠0) (heta : eta≠0)
    (hbalance : tensorQuad (coordinateRicci Gamma p) v=(2*Real.pi/eta)*tensorQuad (T p) v) :
    Nonempty (GeometricHorizonPencil U g Gamma T eta p v) :=
  ⟨horizonPencilFromScreen P T rate eta hU hg hT hrate
    ((constructed_clausius_iff_null_balance P T rate eta hU hg hG hT ht hrate heta).mpr hbalance)⟩

#print axioms horizonPencilFromScreen
#print axioms null_balance_produces_pencil
end
end ChatgptAudit.Flow020
