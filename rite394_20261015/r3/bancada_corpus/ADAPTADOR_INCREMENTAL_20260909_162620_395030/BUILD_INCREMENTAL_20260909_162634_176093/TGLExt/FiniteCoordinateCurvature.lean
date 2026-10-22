import TGLExt.FiniteCurvatureAlgebra

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.FiniteCoordinateCurvature
open Matrix Filter Topology Set TGLExt ChatgptAudit.FiniteCoordinates
  ChatgptAudit.FiniteLeviCivita ChatgptAudit.FiniteCurvatureAlgebra
  ChatgptAudit.GeneralMetric ChatgptAudit.MetricLie
open scoped ContDiff Matrix.Norms.Elementwise
noncomputable section
variable {U W : Set Coordinate4}

def coordinateConnection (C : SmoothCoordinateChange U W) (Gamma : ConnectionField4) :
    ConnectionField4 :=
  fun x => coordinateConnectionJet (changeJacobian C x) (Gamma (C.forward x))

theorem inverse_change_jacobian_jet (C : SmoothCoordinateChange U W)
    (x : Coordinate4) (hx : x ∈ U) (i : Fin 4) :
    tensorFieldJet (inverseChangeJacobian C) x i =
      -inverseChangeJacobian C x * tensorFieldJet (changeJacobian C) x i *
        inverseChangeJacobian C x := by
  have hdiff (A : TensorField4) (hA : SmoothMatrixOn U A) :=
    smooth_matrix_differentiableAt U C.source_open A hA x hx
  have he : EqOn (fun y => inverseChangeJacobian C y * changeJacobian C y)
      (fun _ => (1 : Tensor4)) U :=
    fun y hy => inverse_jacobian_mul_jacobian C y hy
  have hd := congrFun (tensorFieldJet_congr_on U C.source_open _ _ he x hx) i
  have hz : tensorFieldJet (fun _ : Coordinate4 => (1 : Tensor4)) x i = 0 := by
    ext a b
    simp [tensorFieldJet,coordinatePartial]
  rw [tensorFieldJet_mul _ _ x (hdiff _ (inverse_change_jacobian_smooth C))
    (hdiff _ (change_jacobian_smooth C)) i,hz] at hd
  have hh := congrArg (fun M : Tensor4 => M * inverseChangeJacobian C x) hd
  have hc (X : Tensor4) : X * changeJacobian C x * inverseChangeJacobian C x = X := by
    rw [Matrix.mul_assoc,jacobian_mul_inverse_jacobian C x hx,mul_one]
  have heq : tensorFieldJet (inverseChangeJacobian C) x i +
      inverseChangeJacobian C x * tensorFieldJet (changeJacobian C) x i *
        inverseChangeJacobian C x = 0 := by
    simpa only [Matrix.add_mul,hc,zero_mul] using hh
  calc
    _ = -(inverseChangeJacobian C x * tensorFieldJet (changeJacobian C) x i *
      inverseChangeJacobian C x) := eq_neg_of_add_eq_zero_left heq
    _ = _ := by simp only [neg_mul]

theorem coordinate_connection_smooth (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma) :
    SmoothConnectionOn U (coordinateConnection C Gamma) := by
  intro i a b
  change ContDiffOn ℝ ∞
    (fun y => ∑ k : Fin 4, changeJacobian C y k i * Gamma (C.forward y) k a b) U
  exact ContDiffOn.sum (fun k _ =>
    (change_jacobian_smooth C k i).mul (matrix_composition_smooth C
      (fun y => Gamma y k) (hGamma k) a b))

theorem coordinate_connection_first_jet (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma)
    (x : Coordinate4) (hx : x ∈ U) (i j : Fin 4) :
    connectionFirstJet (coordinateConnection C Gamma) x i j =
      coordinateConnectionDerivative (changeJacobian C x)
        (tensorFieldJet (changeJacobian C) x) (Gamma (C.forward x))
        (connectionFirstJet Gamma (C.forward x)) i j := by
  have hcomp (a : Fin 4) := matrix_composition_smooth C
    (fun y => Gamma y a) (hGamma a)
  have hterm (a : Fin 4) :
      SmoothMatrixOn U (fun y => changeJacobian C y a j • Gamma (C.forward y) a) := by
    intro b c
    exact (change_jacobian_smooth C a j).mul (hcomp a b c)
  change tensorFieldJet
    (fun y => ∑ a : Fin 4, changeJacobian C y a j • Gamma (C.forward y) a) x i = _
  rw [tensor_jet_sum U C.source_open _ hterm x hx i]
  have he (a : Fin 4) :
      tensorFieldJet (fun y => changeJacobian C y a j • Gamma (C.forward y) a) x i =
        tensorFieldJet (changeJacobian C) x i a j • Gamma (C.forward x) a +
          ∑ b : Fin 4, (changeJacobian C x a j * changeJacobian C x b i) •
            connectionFirstJet Gamma (C.forward x) b a := by
    rw [tensor_jet_scalar_product U C.source_open _ _
      (change_jacobian_smooth C a j) (hcomp a) x hx i,
      tensor_jet_composition C (fun y => Gamma y a) (hGamma a) x hx i]
    simp only [Finset.smul_sum,smul_smul]
    rfl
  simp_rw [he]
  rw [Finset.sum_add_distrib]
  rfl

theorem pullback_connection_smooth (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma) :
    SmoothConnectionOn U (pullbackConnection C Gamma) := by
  intro i
  exact SmoothMatrixOn.mul U _ _ (inverse_change_jacobian_smooth C)
    (SmoothMatrixOn.add U _ _
      (SmoothMatrixOn.mul U _ _ (coordinate_connection_smooth C Gamma hGamma i)
        (change_jacobian_smooth C))
      (tensorFieldJet_smooth U C.source_open _ (change_jacobian_smooth C) i))

theorem pullback_connection_first_jet (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma)
    (x : Coordinate4) (hx : x ∈ U) (i j : Fin 4) :
    connectionFirstJet (pullbackConnection C Gamma) x i j =
      gaugeConnectionDerivative (changeJacobian C x) (inverseChangeJacobian C x)
        (coordinateConnection C Gamma x) (tensorFieldJet (changeJacobian C) x)
        (connectionFirstJet (coordinateConnection C Gamma) x)
        (connectionFirstJet (fun y => tensorFieldJet (changeJacobian C) y) x) i j := by
  have hJ := change_jacobian_smooth C
  have hD := inverse_change_jacobian_smooth C
  have hA := coordinate_connection_smooth C Gamma hGamma j
  have hH := tensorFieldJet_smooth U C.source_open _ hJ j
  have hAJ := SmoothMatrixOn.mul U _ _ hA hJ
  have hdiff (A : TensorField4) (h : SmoothMatrixOn U A) :=
    smooth_matrix_differentiableAt U C.source_open A h x hx
  change tensorFieldJet (fun y =>
    inverseChangeJacobian C y *
      (coordinateConnection C Gamma y j * changeJacobian C y +
        tensorFieldJet (changeJacobian C) y j)) x i = _
  rw [tensorFieldJet_mul _ _ x (hdiff _ hD)
    (hdiff _ (SmoothMatrixOn.add U _ _ hAJ hH)) i]
  rw [tensorFieldJet_add _ _ x (hdiff _ hAJ) (hdiff _ hH)]
  simp only [Pi.add_apply]
  rw [tensorFieldJet_mul _ _ x (hdiff _ hA) (hdiff _ hJ) i,
    inverse_change_jacobian_jet C x hx i]
  rfl

theorem coordinate_curvature_finite_transformation (C : SmoothCoordinateChange U W)
    (Gamma : ConnectionField4) (hGamma : SmoothConnectionOn W Gamma)
    (x : Coordinate4) (hx : x ∈ U) (i j : Fin 4) :
    coordinateCurvature (pullbackConnection C Gamma) x i j =
      inverseChangeJacobian C x *
        pulledCurvatureJet (changeJacobian C x) (coordinateCurvature Gamma (C.forward x)) i j *
          changeJacobian C x := by
  have heA : connectionFirstJet (coordinateConnection C Gamma) x =
      coordinateConnectionDerivative (changeJacobian C x)
        (tensorFieldJet (changeJacobian C) x) (Gamma (C.forward x))
        (connectionFirstJet Gamma (C.forward x)) := by
    funext a b
    exact coordinate_connection_first_jet C Gamma hGamma x hx a b
  have heG : connectionFirstJet (pullbackConnection C Gamma) x =
      gaugeConnectionDerivative (changeJacobian C x) (inverseChangeJacobian C x)
        (coordinateConnection C Gamma x) (tensorFieldJet (changeJacobian C) x)
        (connectionFirstJet (coordinateConnection C Gamma) x)
        (connectionFirstJet (fun y => tensorFieldJet (changeJacobian C) y) x) := by
    funext a b
    exact pullback_connection_first_jet C Gamma hGamma x hx a b
  have hh (a b : Fin 4) :
      connectionFirstJet (fun y => tensorFieldJet (changeJacobian C) y) x a b =
        connectionFirstJet (fun y => tensorFieldJet (changeJacobian C) y) x b a :=
    tensorFieldJet_commute U C.source_open _ (change_jacobian_smooth C) x hx a b
  unfold coordinateCurvature
  rw [heG,heA]
  exact finite_curvature_jet_identity _ _ _ _ _ _
    (jacobian_mul_inverse_jacobian C x hx)
    (change_jacobian_hessian_symmetry C x hx) hh i j

#print axioms coordinateConnection
#print axioms inverse_change_jacobian_jet
#print axioms coordinate_connection_smooth
#print axioms coordinate_connection_first_jet
#print axioms pullback_connection_smooth
#print axioms pullback_connection_first_jet
#print axioms coordinate_curvature_finite_transformation
end
end ChatgptAudit.FiniteCoordinateCurvature
