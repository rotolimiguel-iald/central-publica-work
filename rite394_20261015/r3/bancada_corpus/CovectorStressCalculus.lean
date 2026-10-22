import CoherentScalarStress

set_option autoImplicit false
set_option maxHeartbeats 10000000
namespace ChatgptAudit.Coherent023
open Matrix Filter Topology Set
open scoped ContDiff
noncomputable section

def covectorDerivative (Gamma : ConnectionField4) (w : CovectorField4)
    (x : Coordinate4) (i : Fin 4) : Coordinate4 :=
  vectorPartial w x i-(Gamma x i)ᵀ *ᵥ w x

def covectorDivergence (gInv : TensorField4) (Gamma : ConnectionField4)
    (w : CovectorField4) (x : Coordinate4) : ℝ :=
  ∑ i, ∑ k, gInv x i k*covectorDerivative Gamma w x i k

theorem outer_field_jet (w : CovectorField4) (x : Coordinate4)
    (hw : ∀ j, DifferentiableAt ℝ (fun y => w y j) x) (i : Fin 4) :
    tensorFieldJet (fun y => Matrix.vecMulVec (w y) (w y)) x i=
      Matrix.vecMulVec (vectorPartial w x i) (w x)+
        Matrix.vecMulVec (w x) (vectorPartial w x i) := by
  ext j k
  exact coordinatePartial_mul (fun y => w y j) (fun y => w y k) x (hw j) (hw k) i

theorem outer_field_covariant (Gamma : ConnectionField4) (w : CovectorField4) (x : Coordinate4)
    (hw : ∀ j, DifferentiableAt ℝ (fun y => w y j) x) (i : Fin 4) :
    covariantTensorJet (Matrix.vecMulVec (w x) (w x))
      (tensorFieldJet (fun y => Matrix.vecMulVec (w y) (w y)) x) (Gamma x) i=
      Matrix.vecMulVec (covectorDerivative Gamma w x i) (w x)+
        Matrix.vecMulVec (w x) (covectorDerivative Gamma w x i) := by
  unfold covariantTensorJet
  rw [outer_field_jet w x hw i]
  ext j k
  simp only [covectorDerivative,Matrix.sub_apply,Matrix.add_apply,Matrix.mul_apply,
    Matrix.transpose_apply,Matrix.vecMulVec,Matrix.of_apply,Pi.sub_apply,
    Matrix.mulVec,dotProduct,Fin.sum_univ_four]
  ring

theorem outer_field_divergence (gInv : TensorField4) (Gamma : ConnectionField4)
    (w : CovectorField4) (x : Coordinate4)
    (hw : ∀ j, DifferentiableAt ℝ (fun y => w y j) x) (j : Fin 4) :
    tensorFieldDivergence gInv Gamma (fun y => Matrix.vecMulVec (w y) (w y)) x j=
      covectorDivergence gInv Gamma w x*w x j+
        ∑ i, ∑ k, gInv x i k*w x k*covectorDerivative Gamma w x i j := by
  simp only [tensorFieldDivergence,tensorJetDivergence]
  simp only [outer_field_covariant Gamma w x hw]
  simp only [covectorDivergence,Matrix.add_apply,Matrix.vecMulVec,Matrix.of_apply,Fin.sum_univ_four]
  ring

theorem covector_squared_differentiable (gInv : TensorField4) (w : CovectorField4) (x : Coordinate4)
    (hgi : ∀ i j, DifferentiableAt ℝ (fun y => gInv y i j) x)
    (hw : ∀ j, DifferentiableAt ℝ (fun y => w y j) x) :
    DifferentiableAt ℝ (fun y => tensorQuad (gInv y) (w y)) x := by
  simp only [tensorQuad,Matrix.mulVec,dotProduct]
  fun_prop

theorem covector_squared_derivative (gInv : TensorField4) (Gamma : ConnectionField4)
    (w : CovectorField4) (x : Coordinate4)
    (hgi : ∀ i j, DifferentiableAt ℝ (fun y => gInv y i j) x)
    (hw : ∀ j, DifferentiableAt ℝ (fun y => w y j) x)
    (hs : (gInv x)ᵀ=gInv x) (i : Fin 4)
    (hd : tensorFieldJet gInv x i= -Gamma x i*gInv x-gInv x*(Gamma x i)ᵀ) :
    coordinatePartial (fun y => tensorQuad (gInv y) (w y)) x i=
      2*(∑ j, ∑ k, gInv x j k*w x k*covectorDerivative Gamma w x i j) := by
  rw [quad_coordinate_derivative gInv w x hgi hw i,hd]
  have hs' (j k : Fin 4) : gInv x k j=gInv x j k :=
    congrArg (fun A : Tensor4 => A j k) hs
  simp only [tensorPair,covectorDerivative,Matrix.sub_apply,Matrix.neg_apply,
    Matrix.mul_apply,Matrix.transpose_apply,Pi.sub_apply,Matrix.mulVec,dotProduct,
    Fin.sum_univ_four,hs' 0 1,hs' 0 2,hs' 0 3,hs' 1 2,hs' 1 3,hs' 2 3]
  ring

theorem coordinate_partial_half (f : Coordinate4 → ℝ) (x : Coordinate4)
    (hf : DifferentiableAt ℝ f x) (i : Fin 4) :
    coordinatePartial (fun y => f y/2) x i=coordinatePartial f x i/2 := by
  have he : (fun y => f y/2)=(fun y => (1/2:ℝ)*f y) := by
    funext y
    ring
  rw [he,coordinatePartial_mul (fun _ => (1/2:ℝ)) f x (differentiableAt_const _) hf i]
  simp [coordinatePartial,div_eq_mul_inv,mul_comm]

#print axioms outer_field_jet
#print axioms outer_field_covariant
#print axioms outer_field_divergence
#print axioms covector_squared_differentiable
#print axioms covector_squared_derivative
#print axioms coordinate_partial_half
end
end ChatgptAudit.Coherent023
