import LeviCivitaLieVariation

set_option autoImplicit false
set_option maxHeartbeats 2200000
namespace ChatgptAudit.RicciLie
open Matrix Filter Topology Set ChatgptAudit.Boost044
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci ChatgptAudit.MetricLie
  ChatgptAudit.MetricLieConnection ChatgptAudit.CurvedConnection
noncomputable section
open scoped ContDiff

def baseConnectionLie (Gamma : ConnectionField4) (V : VectorField4) :
    ConnectionField4 := fun x i =>
  matrixTransport V (fun y => Gamma y i) x +
    ∑ k : Fin 4, vectorJacobian V x k i • Gamma x k

#print axioms baseConnectionLie

theorem base_connection_lie_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V) :
    SmoothConnectionOn U (baseConnectionLie Gamma V) := by
  intro i
  apply SmoothMatrixOn.add U _ _ (matrix_transport_smooth U hU V _ hV (hG i))
  intro a b
  change ContDiffOn ℝ ∞ (fun x => ∑ k : Fin 4, vectorJacobian V x k i*Gamma x k a b) U
  exact ContDiffOn.sum (fun k _ =>
    (vector_jacobian_smooth U hU V hV k i).mul (hG k a b))

#print axioms base_connection_lie_smooth

theorem connection_lie_split (Gamma : ConnectionField4) (V : VectorField4) :
    coordinateConnectionLie Gamma V = fun x i =>
      baseConnectionLie Gamma V x i + connectionGaugeDirection Gamma (vectorJacobian V) x i := by
  funext x i
  unfold coordinateConnectionLie baseConnectionLie connectionGaugeDirection mixedCovariantDerivative
  abel

#print axioms connection_lie_split

theorem connection_lie_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V) :
    SmoothConnectionOn U (coordinateConnectionLie Gamma V) := by
  rw [connection_lie_split]
  intro i
  exact SmoothMatrixOn.add U _ _ (base_connection_lie_smooth U hU Gamma V hG hV i)
    (gauge_direction_smooth U hU Gamma (vectorJacobian V) hG
      (vector_jacobian_smooth U hU V hV) i)

#print axioms connection_lie_smooth

theorem curvature_variation_add (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma C D : ConnectionField4)
    (hC : SmoothConnectionOn U C) (hD : SmoothConnectionOn U D)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    curvatureVariation Gamma (fun y k => C y k+D y k) x i j =
      curvatureVariation Gamma C x i j + curvatureVariation Gamma D x i j := by
  have hJ (a b : Fin 4) : connectionFirstJet (fun y k => C y k+D y k) x a b =
      connectionFirstJet C x a b+connectionFirstJet D x a b := by
    exact congrArg (fun J => J a) (tensorFieldJet_add _ _ x
      (smooth_matrix_differentiableAt U hU _ (hC b) x hx)
      (smooth_matrix_differentiableAt U hU _ (hD b) x hx))
  unfold curvatureVariation
  rw [hJ i j,hJ j i]
  noncomm_ring

#print axioms curvature_variation_add

theorem base_connection_lie_jet (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    connectionFirstJet (baseConnectionLie Gamma V) x i j =
      (∑ k : Fin 4, vectorJacobian V x k i • connectionFirstJet Gamma x k j) +
      (∑ k : Fin 4, V x k • connectionSecondJet Gamma x i k j) +
      (∑ k : Fin 4, tensorFieldJet (vectorJacobian V) x i k j • Gamma x k) +
      ∑ k : Fin 4, vectorJacobian V x k j • connectionFirstJet Gamma x i k := by
  have hP := vector_jacobian_smooth U hU V hV
  have hterm (k : Fin 4) :
      SmoothMatrixOn U (fun y => vectorJacobian V y k j • Gamma y k) := by
    intro a b
    exact (hP k j).mul (hG k a b)
  have hsum : SmoothMatrixOn U (fun y =>
      ∑ k : Fin 4, vectorJacobian V y k j • Gamma y k) := by
    intro a b
    change ContDiffOn ℝ ∞ (fun y => ∑ k : Fin 4, vectorJacobian V y k j*Gamma y k a b) U
    exact ContDiffOn.sum (fun k _ => (hP k j).mul (hG k a b))
  change tensorFieldJet (fun y => matrixTransport V (fun z => Gamma z j) y +
    ∑ k : Fin 4, vectorJacobian V y k j • Gamma y k) x i = _
  rw [tensorFieldJet_add _ _ x
    (smooth_matrix_differentiableAt U hU _
      (matrix_transport_smooth U hU V _ hV (hG j)) x hx)
    (smooth_matrix_differentiableAt U hU _ hsum x hx)]
  simp only [Pi.add_apply]
  rw [matrix_transport_jet U hU V _ hV (hG j) x hx i,
    tensor_jet_sum U hU (fun k y => vectorJacobian V y k j • Gamma y k) hterm x hx i]
  have hprod (k : Fin 4) := tensor_jet_scalar_product U hU
    (fun y => vectorJacobian V y k j) (fun y => Gamma y k)
    (hP k j) (hG k) x hx i
  simp_rw [hprod]
  simp only [Finset.sum_add_distrib,connectionFirstJet,connectionSecondJet,tensorFieldJet]
  abel

#print axioms base_connection_lie_jet

theorem base_curvature_lie_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    curvatureVariation Gamma (baseConnectionLie Gamma V) x i j =
      matrixTransport V (fun y => coordinateCurvature Gamma y i j) x +
      (∑ k : Fin 4, vectorJacobian V x k i • coordinateCurvature Gamma x k j) +
      ∑ k : Fin 4, vectorJacobian V x k j • coordinateCurvature Gamma x i k := by
  unfold curvatureVariation
  rw [base_connection_lie_jet U hU Gamma V hG hV x hx i j,
    base_connection_lie_jet U hU Gamma V hG hV x hx j i]
  have hdd (a b c : Fin 4) :
      connectionSecondJet Gamma x a b c=connectionSecondJet Gamma x b a c :=
    tensorFieldJet_commute U hU (fun y => Gamma y c) (hG c) x hx a b
  have hH := vector_jacobian_hessian_symmetry U hU V hV x hx
  unfold baseConnectionLie matrixTransport
  simp_rw [coordinate_curvature_derivative U hU Gamma hG x hx]
  simp only [coordinateCurvature,connectionCurvatureJet,curvatureDerivativeJet,
    Fin.sum_univ_four,Matrix.add_mul,Matrix.mul_add,
    Matrix.smul_mul,Matrix.mul_smul]
  simp only [hdd,hH,connectionFirstJet]
  module

#print axioms base_curvature_lie_variation

theorem curvature_connection_lie_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) (i j : Fin 4) :
    curvatureVariation Gamma (coordinateConnectionLie Gamma V) x i j =
      matrixTransport V (fun y => coordinateCurvature Gamma y i j) x +
      (∑ k : Fin 4, vectorJacobian V x k i • coordinateCurvature Gamma x k j) +
      (∑ k : Fin 4, vectorJacobian V x k j • coordinateCurvature Gamma x i k) +
      coordinateCurvature Gamma x i j*vectorJacobian V x -
      vectorJacobian V x*coordinateCurvature Gamma x i j := by
  rw [connection_lie_split,curvature_variation_add U hU Gamma _ _
    (base_connection_lie_smooth U hU Gamma V hG hV)
    (gauge_direction_smooth U hU Gamma _ hG (vector_jacobian_smooth U hU V hV)) x hx i j,
    base_curvature_lie_variation U hU Gamma V hG hV x hx i j,
    curvature_gauge_variation U hU Gamma _ hG (vector_jacobian_smooth U hU V hV) x hx i j]
  abel

#print axioms curvature_connection_lie_variation

theorem ricci_connection_lie_variation (U : Set Coordinate4) (hU : IsOpen U)
    (Gamma : ConnectionField4) (V : VectorField4)
    (hG : SmoothConnectionOn U Gamma) (hV : SmoothVectorOn U V)
    (x : Coordinate4) (hx : x∈U) :
    ricciVariation Gamma (coordinateConnectionLie Gamma V) x =
      coordinateMetricLie (coordinateRicci Gamma) V x := by
  ext b j
  rw [coordinate_metric_lie_matrix_formula]
  simp only [ricciVariation,curvature_connection_lie_variation U hU Gamma V hG hV x hx]
  simp only [matrixTransport,Matrix.add_apply,Matrix.sub_apply,Matrix.mul_apply,
    Matrix.transpose_apply,Fin.sum_univ_four,Matrix.smul_apply,smul_eq_mul]
  simp_rw [ricci_derivative_trace U hU Gamma hG x hx]
  simp only [coordinateRicci,Fin.sum_univ_four]
  ring

#print axioms ricci_connection_lie_variation

theorem actual_levi_civita_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : SmoothMatrixOn U g)
    (hi : ∀ x∈U, IsUnit (g x)) :
    SmoothConnectionOn U (leviCivitaField g (fun y => (g y)⁻¹)) := by
  intro i
  exact SmoothMatrixOn.mul U _ _ (smooth_matrix_inverse U g hg hi)
    (fun a b => lower_metric_jet_smooth U hU g hg i a b)

#print axioms actual_levi_civita_smooth

/-- Infinitesimal naturality for the real metric-induced Ricci, on an arbitrary curved chart. -/
theorem metric_lie_ricci_naturality
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) (b j : Fin 4) :
    HasDerivAt (fun t => coordinateRicci
      (perturbedLeviCivita g (coordinateMetricLie g V) t) x b j)
      (coordinateMetricLie
        (coordinateRicci (leviCivitaField g (fun y => (g y)⁻¹))) V x b j) 0 := by
  have H := metric_lie_ricci_reduced_to_connection U hU g V hg hV hs hi x hx b j
  rw [ricci_connection_lie_variation U hU _ V
    (actual_levi_civita_smooth U hU g hg hi) hV x hx] at H
  exact H

#print axioms metric_lie_ricci_naturality

end
end ChatgptAudit.RicciLie
