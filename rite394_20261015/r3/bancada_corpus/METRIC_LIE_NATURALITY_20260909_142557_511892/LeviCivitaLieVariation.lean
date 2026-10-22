import LieMetricJets

set_option autoImplicit false
set_option maxHeartbeats 1800000
namespace ChatgptAudit.MetricLieConnection
open Matrix Filter Topology Set ChatgptAudit.Boost044
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci ChatgptAudit.MetricLie
  ChatgptAudit.CurvedConnection ChatgptAudit.JointCurvature
noncomputable section
open scoped ContDiff

def coordinateConnectionLie (Gamma : ConnectionField4) (V : VectorField4) :
    ConnectionField4 := fun x i =>
  matrixTransport V (fun y => Gamma y i) x +
    (∑ k : Fin 4, vectorJacobian V x k i • Gamma x k) +
    Gamma x i*vectorJacobian V x - vectorJacobian V x*Gamma x i +
    tensorFieldJet (vectorJacobian V) x i

#print axioms coordinateConnectionLie

theorem smooth_matrix_inverse (U : Set Coordinate4) (g : TensorField4)
    (hg : SmoothMatrixOn U g) (hi : ∀ x∈U, IsUnit (g x)) :
    SmoothMatrixOn U (fun x => (g x)⁻¹) := by
  let W : Set ParameterSpace := {z | z.2∈U}
  have hA : JointSmoothMatrixOn W (fun z => g z.2) := by
    intro a b
    exact (hg a b).comp contDiffOn_snd (fun z hz => hz)
  have hI := joint_matrix_inverse_smooth W (fun z => g z.2) hA
    (fun z hz => isUnit_iff_ne_zero.mp ((Matrix.isUnit_iff_isUnit_det (g z.2)).mp (hi z.2 hz)))
  intro a b
  have hE : ContDiffOn ℝ ∞ (fun x : Coordinate4 => ((0:ℝ),x)) U :=
    contDiffOn_const.prodMk contDiffOn_id
  exact (hI a b).comp hE (fun x hx => hx)

#print axioms smooth_matrix_inverse

theorem actual_inverse_left (g : Tensor4) (hi : IsUnit g) : g⁻¹*g=1 :=
  Matrix.nonsing_inv_mul g ((Matrix.isUnit_iff_isUnit_det g).mp hi)

#print axioms actual_inverse_left

theorem actual_inverse_right (g : Tensor4) (hi : IsUnit g) : g*g⁻¹=1 :=
  Matrix.mul_nonsing_inv g ((Matrix.isUnit_iff_isUnit_det g).mp hi)

#print axioms actual_inverse_right

theorem matrix_inverse_spatial_jet (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : SmoothMatrixOn U g) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (fun y => (g y)⁻¹) x i =
      -(g x)⁻¹*tensorFieldJet g x i*(g x)⁻¹ := by
  have hgi := smooth_matrix_inverse U g hg hi
  have hEq : EqOn (fun y => (g y)⁻¹*g y) (fun _ => (1:Tensor4)) U :=
    fun y hy => actual_inverse_left (g y) (hi y hy)
  have hJ := congrArg (fun J => J i)
    (tensorFieldJet_congr_on U hU _ _ hEq x hx)
  rw [tensorFieldJet_mul _ _ x
    (smooth_matrix_differentiableAt U hU _ hgi x hx)
    (smooth_matrix_differentiableAt U hU g hg x hx) i] at hJ
  have hz : tensorFieldJet (fun _ : Coordinate4 => (1:Tensor4)) x i=0 := by
    ext a b
    simp [tensorFieldJet,coordinatePartial]
  rw [hz] at hJ
  have hd := congrArg (fun M : Tensor4 => M*(g x)⁻¹) hJ
  simp only [Matrix.add_mul,mul_assoc,actual_inverse_right (g x) (hi x hx),
    mul_one,zero_mul] at hd
  simpa only [neg_mul,mul_assoc] using eq_neg_of_add_eq_zero_left hd

#print axioms matrix_inverse_spatial_jet

theorem lower_metric_spatial_jet (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : SmoothMatrixOn U g)
    (x : Coordinate4) (hx : x∈U) (r i : Fin 4) :
    tensorFieldJet (fun y => lowerChristoffelJet (tensorFieldJet g y) i) x r =
      lowerChristoffelJet (fun k => tensorFieldJet (fun y => tensorFieldJet g y k) x r) i := by
  ext a b
  have hd (k c d : Fin 4) :=
    smooth_matrix_differentiableAt U hU _
      (tensorFieldJet_smooth U hU g hg k) x hx c d
  change coordinatePartial (fun y =>
    (tensorFieldJet g y i a b + tensorFieldJet g y b i a -
      tensorFieldJet g y a i b) / 2) x r =
    (coordinatePartial (fun y => tensorFieldJet g y i a b) x r +
      coordinatePartial (fun y => tensorFieldJet g y b i a) x r -
      coordinatePartial (fun y => tensorFieldJet g y a i b) x r) / 2
  simp only [div_eq_mul_inv]
  rw [coordinatePartial_mul
    (fun y => tensorFieldJet g y i a b + tensorFieldJet g y b i a - tensorFieldJet g y a i b)
    (fun _ => (2:ℝ)⁻¹) x
    (((hd i a b).add (hd b i a)).sub (hd a i b)) (differentiableAt_const _) r,
    coordinatePartial_sub
      (fun y => tensorFieldJet g y i a b + tensorFieldJet g y b i a)
      (fun y => tensorFieldJet g y a i b) x ((hd i a b).add (hd b i a)) (hd a i b) r,
    coordinatePartial_add (fun y => tensorFieldJet g y i a b)
      (fun y => tensorFieldJet g y b i a) x (hd i a b) (hd b i a) r]
  have hc : coordinatePartial (fun _ : Coordinate4 => (2:ℝ)⁻¹) x r=0 := by
    unfold coordinatePartial
    rw [(hasFDerivAt_const ((2:ℝ)⁻¹) x).fderiv]
    rfl
  rw [hc,mul_zero,add_zero]

#print axioms lower_metric_spatial_jet

theorem levi_civita_spatial_jet (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hg : SmoothMatrixOn U g) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) (r i : Fin 4) :
    connectionFirstJet (leviCivitaField g (fun y => (g y)⁻¹)) x r i =
      (-(g x)⁻¹*tensorFieldJet g x r*(g x)⁻¹)*
        lowerChristoffelJet (tensorFieldJet g x) i +
      (g x)⁻¹*lowerChristoffelJet
        (fun k => tensorFieldJet (fun y => tensorFieldJet g y k) x r) i := by
  change tensorFieldJet (fun y => (g y)⁻¹*lowerChristoffelJet (tensorFieldJet g y) i) x r = _
  rw [tensorFieldJet_mul _ _ x
    (smooth_matrix_differentiableAt U hU _ (smooth_matrix_inverse U g hg hi) x hx)
    (smooth_matrix_differentiableAt U hU _
      (fun a b => lower_metric_jet_smooth U hU g hg i a b) x hx) r,
    matrix_inverse_spatial_jet U hU g hg hi x hx r,
    lower_metric_spatial_jet U hU g hg x hx r i]

#print axioms levi_civita_spatial_jet

theorem metric_jet_symmetric (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (hs : ∀ x∈U, (g x)ᵀ=g x)
    (x : Coordinate4) (hx : x∈U) (i a b : Fin 4) :
    tensorFieldJet g x i a b=tensorFieldJet g x i b a := by
  have h := congrArg (fun J => J i a b)
    (tensorFieldJet_congr_on U hU (fun y => (g y)ᵀ) g (fun y hy => hs y hy) x hx)
  exact h.symm

#print axioms metric_jet_symmetric

theorem metric_lie_connection_variation (U : Set Coordinate4) (hU : IsOpen U)
    (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    metricConnectionVariation g (coordinateMetricLie g V) x i =
      coordinateConnectionLie (leviCivitaField g (fun y => (g y)⁻¹)) V x i := by
  have hsym (a b : Fin 4) : g x a b=g x b a :=
    (congrFun (congrFun (hs x hx) a) b).symm
  have hdd (r k : Fin 4) :
      (fun j => tensorFieldJet (fun y => tensorFieldJet g y j) x r) k =
        (fun j => tensorFieldJet (fun y => tensorFieldJet g y j) x k) r :=
    tensorFieldJet_commute U hU g hg x hx r k
  have hlow := lower_lie_jet_identity (g x) (tensorFieldJet g x)
    (fun r k => tensorFieldJet (fun y => tensorFieldJet g y k) x r)
    (V x) (vectorJacobian V x) (tensorFieldJet (vectorJacobian V) x)
    hsym (metric_jet_symmetric U hU g hs x hx) hdd
    (vector_jacobian_hessian_symmetry U hU V hV x hx) i
  have hj : tensorFieldJet (coordinateMetricLie g V) x =
      lieMetricJetDerivative (g x) (tensorFieldJet g x)
        (fun r k => tensorFieldJet (fun y => tensorFieldJet g y k) x r)
        (V x) (vectorJacobian V x) (tensorFieldJet (vectorJacobian V) x) := by
    funext r
    exact coordinate_metric_lie_jet U hU V g hV hg x hx r
  unfold metricConnectionVariation coordinateConnectionLie matrixTransport
  rw [hj,hlow,coordinate_metric_lie_matrix_formula]
  have hJ (k : Fin 4) := levi_civita_spatial_jet U hU g hg hi x hx k i
  simp only [connectionFirstJet] at hJ
  simp_rw [hJ]
  simp only [leviCivitaField,leviCivitaJet,matrixTransport,Fin.sum_univ_four,
    Matrix.add_mul,Matrix.mul_add,Matrix.smul_mul,Matrix.mul_smul,neg_mul,mul_assoc]
  have hleft (M : Tensor4) : (g x)⁻¹*(g x*M)=M := by
    rw [← mul_assoc,actual_inverse_left (g x) (hi x hx),one_mul]
  have hright (M : Tensor4) : g x*((g x)⁻¹*M)=M := by
    rw [← mul_assoc,actual_inverse_right (g x) (hi x hx),one_mul]
  simp only [hleft,hright]
  module

#print axioms metric_lie_connection_variation

theorem metric_lie_connection_first_derivative
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    HasDerivAt (fun t => perturbedLeviCivita g (coordinateMetricLie g V) t x i)
      (coordinateConnectionLie (leviCivitaField g (fun y => (g y)⁻¹)) V x i) 0 := by
  rw [← metric_lie_connection_variation U hU g V hg hV hs hi x hx i]
  exact levi_civita_metric_first_variation U hU g (coordinateMetricLie g V)
    hg (coordinate_metric_lie_smooth U hU V g hV hg) x hx (hi x hx) i

#print axioms metric_lie_connection_first_derivative

theorem metric_lie_ricci_reduced_to_connection
    (U : Set Coordinate4) (hU : IsOpen U) (g : TensorField4) (V : VectorField4)
    (hg : SmoothMatrixOn U g) (hV : SmoothVectorOn U V)
    (hs : ∀ x∈U, (g x)ᵀ=g x) (hi : ∀ x∈U, IsUnit (g x))
    (x : Coordinate4) (hx : x∈U) (b j : Fin 4) :
    HasDerivAt (fun t => coordinateRicci
      (perturbedLeviCivita g (coordinateMetricLie g V) t) x b j)
      (ricciVariation (leviCivitaField g (fun y => (g y)⁻¹))
        (coordinateConnectionLie (leviCivitaField g (fun y => (g y)⁻¹)) V) x b j) 0 := by
  have he : EqOn (metricConnectionVariation g (coordinateMetricLie g V))
      (coordinateConnectionLie (leviCivitaField g (fun y => (g y)⁻¹)) V) U := by
    intro y hy
    funext i
    exact metric_lie_connection_variation U hU g V hg hV hs hi y hy i
  have H := metric_ricci_first_variation U hU g (coordinateMetricLie g V)
    hg (coordinate_metric_lie_smooth U hU V g hV hg) hi x hx b j
  rw [ricci_variation_congr_on U hU _ _ _ he x hx] at H
  exact H

#print axioms metric_lie_ricci_reduced_to_connection

end
end ChatgptAudit.MetricLieConnection
