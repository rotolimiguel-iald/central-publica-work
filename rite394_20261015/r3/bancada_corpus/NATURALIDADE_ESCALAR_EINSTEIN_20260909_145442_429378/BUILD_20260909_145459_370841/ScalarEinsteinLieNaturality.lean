import MetricEinsteinVariation
import RicciLieNaturality

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.EinsteinLie
open Matrix Filter Topology Set ChatgptAudit.Boost044
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci
  ChatgptAudit.MetricLie ChatgptAudit.MetricLieConnection
  ChatgptAudit.RicciLie ChatgptAudit.MetricEinsteinVariation
noncomputable section
open scoped ContDiff

def tensorPair (A B : Tensor4) : ℝ := ∑ i : Fin 4, ∑ j : Fin 4, A i j*B i j

theorem tensor_pair_add_left (A B C : Tensor4) :
    tensorPair (A+B) C=tensorPair A C+tensorPair B C := by
  simp [tensorPair,add_mul,Finset.sum_add_distrib]

theorem tensor_pair_add_right (A B C : Tensor4) :
    tensorPair A (B+C)=tensorPair A B+tensorPair A C := by
  simp [tensorPair,mul_add,Finset.sum_add_distrib]

theorem tensor_pair_sub_left (A B C : Tensor4) :
    tensorPair (A-B) C=tensorPair A C-tensorPair B C := by
  simp [tensorPair,sub_mul,Finset.sum_sub_distrib]

theorem tensor_pair_transpose_left (A P R : Tensor4) :
    tensorPair A (Pᵀ*R)=tensorPair (P*A) R := by
  simp only [tensorPair,Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_four]
  ring

theorem tensor_pair_transpose_right (A P R : Tensor4) :
    tensorPair A (R*P)=tensorPair (A*Pᵀ) R := by
  simp only [tensorPair,Matrix.mul_apply,Matrix.transpose_apply,Fin.sum_univ_four]
  ring

theorem tensor_pair_scalar_transport (U : Set Coordinate4) (hU : IsOpen U)
    (A B : TensorField4) (V : VectorField4)
    (hA : SmoothMatrixOn U A) (hB : SmoothMatrixOn U B)
    (x : Coordinate4) (hx : x∈U) :
    scalarAlong V (fun y => tensorPair (A y) (B y)) x =
      tensorPair (matrixTransport V A x) (B x) +
      tensorPair (A x) (matrixTransport V B x) := by
  have hprod (i j : Fin 4) : DifferentiableAt ℝ (fun y => A y i j*B y i j) x :=
    (smooth_matrix_differentiableAt U hU A hA x hx i j).mul
      (smooth_matrix_differentiableAt U hU B hB x hx i j)
  have hsum (i : Fin 4) : DifferentiableAt ℝ (fun y => ∑ j : Fin 4, A y i j*B y i j) x :=
    DifferentiableAt.sum (fun j _ => hprod i j)
  have hj (k : Fin 4) :
      coordinatePartial (fun y => tensorPair (A y) (B y)) x k =
        ∑ i : Fin 4, ∑ j : Fin 4,
          (tensorFieldJet A x k i j*B x i j+A x i j*tensorFieldJet B x k i j) := by
    unfold tensorPair
    rw [coordinatePartial_sum _ x hsum k]
    apply Finset.sum_congr rfl
    intro i _
    rw [coordinatePartial_sum _ x (hprod i) k]
    apply Finset.sum_congr rfl
    intro j _
    exact coordinatePartial_mul _ _ x
      (smooth_matrix_differentiableAt U hU A hA x hx i j)
      (smooth_matrix_differentiableAt U hU B hB x hx i j) k
  unfold scalarAlong
  simp_rw [hj]
  simp only [tensorPair,matrixTransport,Fin.sum_univ_four,
    Matrix.add_apply,Matrix.smul_apply,smul_eq_mul]
  ring

theorem inverse_metric_lie_variation (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4) (hg : SmoothMatrixOn U g)
    (hi : ∀ x∈U, IsUnit (g x)) (x : Coordinate4) (hx : x∈U) :
    -(g x)⁻¹*coordinateMetricLie g V x*(g x)⁻¹ =
      matrixTransport V (fun y => (g y)⁻¹) x -
        vectorJacobian V x*(g x)⁻¹ - (g x)⁻¹*(vectorJacobian V x)ᵀ := by
  rw [coordinate_metric_lie_matrix_formula]
  unfold matrixTransport
  simp_rw [matrix_inverse_spatial_jet U hU g hg hi x hx]
  simp only [Fin.sum_univ_four,Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,
    Matrix.mul_smul,neg_mul,mul_assoc]
  have hL (M : Tensor4) : (g x)⁻¹*(g x*M)=M := by
    rw [←mul_assoc,actual_inverse_left (g x) (hi x hx),one_mul]
  have hR (M : Tensor4) : g x*((g x)⁻¹*M)=M := by
    rw [←mul_assoc,actual_inverse_right (g x) (hi x hx),one_mul]
  simp only [hL,hR,actual_inverse_right (g x) (hi x hx),mul_one]
  module

theorem metric_lie_ricci_operator (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) :
    ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
      (metricConnectionVariation g (coordinateMetricLie g V)) x =
      coordinateMetricLie (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹))) V x := by
  ext i j
  exact (metric_ricci_first_variation U hU g (coordinateMetricLie g V)
    hg (coordinate_metric_lie_smooth U hU V g hV hg) hi x hx i j).unique
      (metric_lie_ricci_naturality U hU g V hg hV hs hi x hx i j)

theorem metric_lie_scalar_operator (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) :
    scalarMetricVariation g (coordinateMetricLie g V) x =
      scalarAlong V (coordinateScalarCurvature (fun y => (g y)⁻¹)
        (leviCivitaField g (fun y => (g y)⁻¹))) x := by
  have hR := coordinate_ricci_smooth U hU _ (actual_levi_civita_smooth U hU g hg hi)
  change tensorPair (-(g x)⁻¹*coordinateMetricLie g V x*(g x)⁻¹)
      (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) x) +
    tensorPair ((g x)⁻¹) (ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
      (metricConnectionVariation g (coordinateMetricLie g V)) x) = _
  rw [metric_lie_ricci_operator U hU g V hg hV hs hi x hx,
    inverse_metric_lie_variation U hU g V hg hi x hx,
    coordinate_metric_lie_matrix_formula]
  change _ = scalarAlong V (fun y => tensorPair ((g y)⁻¹)
    (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹)) y)) x
  rw [tensor_pair_scalar_transport U hU _ _ V
    (smooth_matrix_inverse U g hg hi) hR x hx]
  simp only [tensor_pair_add_right,tensor_pair_sub_left,
    tensor_pair_transpose_left,tensor_pair_transpose_right]
  ring

theorem metric_lie_scalar_naturality (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) :
    HasDerivAt (fun t => coordinateScalarCurvature
      (perturbedMetricInverse g (coordinateMetricLie g V) t)
      (perturbedLeviCivita g (coordinateMetricLie g V) t) x)
      (scalarAlong V (coordinateScalarCurvature (fun y => (g y)⁻¹)
        (leviCivitaField g (fun y => (g y)⁻¹))) x) 0 := by
  rw [←metric_lie_scalar_operator U hU g V hg hV hs hi x hx]
  exact metric_scalar_first_variation U hU g (coordinateMetricLie g V)
    hg (coordinate_metric_lie_smooth U hU V g hV hg) hi x hx


#print axioms tensorPair
#print axioms tensor_pair_add_left
#print axioms tensor_pair_add_right
#print axioms tensor_pair_sub_left
#print axioms tensor_pair_transpose_left
#print axioms tensor_pair_transpose_right
#print axioms tensor_pair_scalar_transport
#print axioms inverse_metric_lie_variation
#print axioms metric_lie_ricci_operator
#print axioms metric_lie_scalar_operator
#print axioms metric_lie_scalar_naturality
end
end ChatgptAudit.EinsteinLie
