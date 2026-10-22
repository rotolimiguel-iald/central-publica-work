import MetricRicciVariation
import TGLExt.BoostMetricPullback

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.MetricLie
open Matrix Filter Topology Set ChatgptAudit.Boost044
  ChatgptAudit.MetricVariation ChatgptAudit.MetricRicci
noncomputable section
open scoped ContDiff

def vectorJacobian (V : VectorField4) : TensorField4 :=
  fun x a b => vectorPartial V x b a

#print axioms vectorJacobian

def matrixTransport (V : VectorField4) (g : TensorField4) : TensorField4 :=
  fun x => ∑ k : Fin 4, V x k • tensorFieldJet g x k

#print axioms matrixTransport

def lieMetricJetDerivative (g : Tensor4) (dg : Fin 4 → Tensor4)
    (ddg : Fin 4 → Fin 4 → Tensor4) (v : Coordinate4)
    (P : Tensor4) (H : Fin 4 → Tensor4) (i : Fin 4) : Tensor4 :=
  (∑ k : Fin 4, P k i • dg k) + (∑ k : Fin 4, v k • ddg i k) +
    (H i)ᵀ*g + Pᵀ*dg i + dg i*P + g*H i

#print axioms lieMetricJetDerivative

theorem vector_jacobian_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (hV : SmoothVectorOn U V) :
    SmoothMatrixOn U (vectorJacobian V) := by
  intro a b
  exact vectorPartial_smooth U hU V hV b a

#print axioms vector_jacobian_smooth

theorem vector_jacobian_hessian_symmetry (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (hV : SmoothVectorOn U V) (x : Coordinate4) (hx : x∈U)
    (i a b : Fin 4) :
    tensorFieldJet (vectorJacobian V) x i a b =
      tensorFieldJet (vectorJacobian V) x b a i := by
  exact congrFun (vectorPartial_commute U hU V hV x hx i b) a

#print axioms vector_jacobian_hessian_symmetry

theorem matrix_transport_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (g : TensorField4)
    (hV : SmoothVectorOn U V) (hg : SmoothMatrixOn U g) :
    SmoothMatrixOn U (matrixTransport V g) := by
  intro a b
  change ContDiffOn ℝ ∞ (fun x => ∑ k : Fin 4, V x k*tensorFieldJet g x k a b) U
  exact ContDiffOn.sum (fun k _ => (hV k).mul (tensorFieldJet_smooth U hU g hg k a b))

#print axioms matrix_transport_smooth

theorem coordinate_metric_lie_matrix_formula (g : TensorField4) (V : VectorField4)
    (x : Coordinate4) :
    coordinateMetricLie g V x = matrixTransport V g x +
      (vectorJacobian V x)ᵀ*g x + g x*vectorJacobian V x := by
  ext a b
  simp only [coordinateMetricLie,scalarAlong,matrixTransport,vectorJacobian,
    Matrix.add_apply,Matrix.mul_apply,Matrix.transpose_apply,
    ]
  congr 1
  congr 1
  apply Finset.sum_congr rfl
  intro k _
  ring

#print axioms coordinate_metric_lie_matrix_formula

theorem coordinate_metric_lie_smooth (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (g : TensorField4)
    (hV : SmoothVectorOn U V) (hg : SmoothMatrixOn U g) :
    SmoothMatrixOn U (coordinateMetricLie g V) := by
  have he : coordinateMetricLie g V = fun x => matrixTransport V g x +
      (vectorJacobian V x)ᵀ*g x + g x*vectorJacobian V x := by
    funext x
    exact coordinate_metric_lie_matrix_formula g V x
  rw [he]
  exact SmoothMatrixOn.add U _ _
    (SmoothMatrixOn.add U _ _ (matrix_transport_smooth U hU V g hV hg)
      (SmoothMatrixOn.mul U _ _
        (SmoothMatrixOn.transpose U _ (vector_jacobian_smooth U hU V hV)) hg))
    (SmoothMatrixOn.mul U _ _ hg (vector_jacobian_smooth U hU V hV))

#print axioms coordinate_metric_lie_smooth

theorem tensor_jet_sum (U : Set Coordinate4) (hU : IsOpen U)
    (A : Fin 4 → TensorField4) (hA : ∀ k, SmoothMatrixOn U (A k))
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (fun y => ∑ k : Fin 4, A k y) x i =
      ∑ k : Fin 4, tensorFieldJet (A k) x i := by
  ext a b
  change coordinatePartial (fun y => ∑ k : Fin 4, A k y a b) x i = _
  rw [coordinatePartial_sum _ x
    (fun k => smooth_matrix_differentiableAt U hU (A k) (hA k) x hx a b) i]
  rfl

#print axioms tensor_jet_sum

theorem tensor_jet_scalar_product (U : Set Coordinate4) (hU : IsOpen U)
    (f : Coordinate4 → ℝ) (A : TensorField4)
    (hf : ContDiffOn ℝ ∞ f U) (hA : SmoothMatrixOn U A)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (fun y => f y • A y) x i =
      coordinatePartial f x i • A x + f x • tensorFieldJet A x i := by
  ext a b
  exact coordinatePartial_mul f (fun y => A y a b) x
    ((hf.differentiableOn (by simp)).differentiableAt (hU.mem_nhds hx))
    (smooth_matrix_differentiableAt U hU A hA x hx a b) i

#print axioms tensor_jet_scalar_product

theorem matrix_transport_jet (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (g : TensorField4)
    (hV : SmoothVectorOn U V) (hg : SmoothMatrixOn U g)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (matrixTransport V g) x i =
      (∑ k : Fin 4, vectorJacobian V x k i • tensorFieldJet g x k) +
      ∑ k : Fin 4, V x k • tensorFieldJet (fun y => tensorFieldJet g y k) x i := by
  unfold matrixTransport
  have hterm (k : Fin 4) :
      SmoothMatrixOn U (fun y => V y k • tensorFieldJet g y k) := by
    intro a b
    exact (hV k).mul (tensorFieldJet_smooth U hU g hg k a b)
  rw [tensor_jet_sum U hU (fun k y => V y k • tensorFieldJet g y k) hterm x hx i]
  simp only [tensor_jet_scalar_product U hU _ _ (hV _)
    (tensorFieldJet_smooth U hU g hg _) x hx i,Finset.sum_add_distrib,
    vectorJacobian,vectorPartial]

#print axioms matrix_transport_jet

theorem coordinate_metric_lie_jet (U : Set Coordinate4) (hU : IsOpen U)
    (V : VectorField4) (g : TensorField4)
    (hV : SmoothVectorOn U V) (hg : SmoothMatrixOn U g)
    (x : Coordinate4) (hx : x∈U) (i : Fin 4) :
    tensorFieldJet (coordinateMetricLie g V) x i =
      lieMetricJetDerivative (g x) (tensorFieldJet g x)
        (fun i k => tensorFieldJet (fun y => tensorFieldJet g y k) x i)
        (V x) (vectorJacobian V x) (tensorFieldJet (vectorJacobian V) x) i := by
  have he : coordinateMetricLie g V = fun y => matrixTransport V g y +
      (vectorJacobian V y)ᵀ*g y + g y*vectorJacobian V y := by
    funext y
    exact coordinate_metric_lie_matrix_formula g V y
  have hP := vector_jacobian_smooth U hU V hV
  have hd (A : TensorField4) (hA : SmoothMatrixOn U A) :=
    smooth_matrix_differentiableAt U hU A hA x hx
  rw [he]
  rw [tensorFieldJet_add _ _ x
    (hd _ (SmoothMatrixOn.add U _ _ (matrix_transport_smooth U hU V g hV hg)
      (SmoothMatrixOn.mul U _ _ (SmoothMatrixOn.transpose U _ hP) hg)))
    (hd _ (SmoothMatrixOn.mul U _ _ hg hP))]
  simp only [Pi.add_apply]
  rw [tensorFieldJet_add _ _ x (hd _ (matrix_transport_smooth U hU V g hV hg))
    (hd _ (SmoothMatrixOn.mul U _ _ (SmoothMatrixOn.transpose U _ hP) hg))]
  simp only [Pi.add_apply]
  rw [tensorFieldJet_mul _ _ x (hd _ (SmoothMatrixOn.transpose U _ hP)) (hd _ hg) i,
    tensorFieldJet_mul _ _ x (hd _ hg) (hd _ hP) i,
    tensorFieldJet_transpose,matrix_transport_jet U hU V g hV hg x hx i]
  unfold lieMetricJetDerivative
  abel

#print axioms coordinate_metric_lie_jet

theorem lower_lie_jet_identity (g : Tensor4) (dg : Fin 4 → Tensor4)
    (ddg : Fin 4 → Fin 4 → Tensor4) (v : Coordinate4)
    (P : Tensor4) (H : Fin 4 → Tensor4)
    (hg : ∀ a b, g a b=g b a)
    (hdg : ∀ i a b, dg i a b=dg i b a)
    (hddg : ∀ i k, ddg i k=ddg k i)
    (hH : ∀ i a b, H i a b=H b a i) (i : Fin 4) :
    lowerChristoffelJet (lieMetricJetDerivative g dg ddg v P H) i =
      (∑ k : Fin 4, v k • lowerChristoffelJet (ddg k) i) +
      (∑ k : Fin 4, P k i • lowerChristoffelJet dg k) +
      Pᵀ*lowerChristoffelJet dg i + lowerChristoffelJet dg i*P + g*H i := by
  ext a b
  have hdd (i k a b : Fin 4) : ddg i k a b=ddg k i a b :=
    congrFun (congrFun (hddg i k) a) b
  simp only [lowerChristoffelJet,lieMetricJetDerivative,Matrix.add_apply,Matrix.mul_apply,
    Matrix.transpose_apply,Matrix.smul_apply,smul_eq_mul,
    Fin.sum_univ_four]
  simp only [hg,hdg,hdd,hH]
  ring

#print axioms lower_lie_jet_identity

end
end ChatgptAudit.MetricLie
