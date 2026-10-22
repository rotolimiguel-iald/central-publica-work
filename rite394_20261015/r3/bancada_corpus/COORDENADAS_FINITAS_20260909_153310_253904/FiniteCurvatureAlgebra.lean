import FiniteLeviCivita

set_option autoImplicit false
set_option maxHeartbeats 1400000
namespace ChatgptAudit.FiniteCurvatureAlgebra
open Matrix TGLExt ChatgptAudit.FiniteLeviCivita
noncomputable section

def coordinateConnectionJet (J : Tensor4) (Gamma : ConnectionMatrix4)
    (i : Fin 4) : Tensor4 := ∑ a : Fin 4, J a i • Gamma a

def coordinateConnectionDerivative (J : Tensor4) (H Gamma : ConnectionMatrix4)
    (dGamma : ConnectionDerivative4) (i j : Fin 4) : Tensor4 :=
  (∑ a : Fin 4, H i a j • Gamma a) +
    ∑ a : Fin 4, ∑ b : Fin 4, (J a j * J b i) • dGamma b a

def gaugeConnectionJet (J D : Tensor4) (A H : ConnectionMatrix4)
    (i : Fin 4) : Tensor4 := D*(A i*J+H i)

def gaugeConnectionDerivative (J D : Tensor4) (A H : ConnectionMatrix4)
    (dA dH : ConnectionDerivative4) (i j : Fin 4) : Tensor4 :=
  (-D*H i*D)*(A j*J+H j) + D*(dA i j*J+A j*H i+dH i j)

def pulledCurvatureJet (J : Tensor4) (R : Fin 4 → Fin 4 → Tensor4)
    (i j : Fin 4) : Tensor4 :=
  ∑ a : Fin 4, ∑ b : Fin 4, (J a i * J b j) • R a b

theorem swapped_weighted_sum (J : Tensor4) (F : Fin 4 → Fin 4 → Tensor4)
    (i j : Fin 4) :
    (∑ a : Fin 4, ∑ b : Fin 4, (J a j*J b i) • F b a) =
      ∑ a : Fin 4, ∑ b : Fin 4, (J a i*J b j) • F a b := by
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro b _
  rw [mul_comm]

theorem coordinate_connection_product (J : Tensor4) (Gamma : ConnectionMatrix4)
    (i j : Fin 4) :
    coordinateConnectionJet J Gamma i * coordinateConnectionJet J Gamma j =
      ∑ a : Fin 4, ∑ b : Fin 4, (J a i*J b j) • (Gamma a*Gamma b) := by
  simp only [coordinateConnectionJet,Matrix.sum_mul,Matrix.mul_sum,
    Matrix.smul_mul,Matrix.mul_smul,Finset.smul_sum,smul_smul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro a _
  apply Finset.sum_congr rfl
  intro b _
  rw [mul_comm]

theorem coordinate_curvature_jet_pullback (J : Tensor4) (H Gamma : ConnectionMatrix4)
    (dGamma : ConnectionDerivative4) (hH : ∀ i a j, H i a j = H j a i)
    (i j : Fin 4) :
    connectionCurvatureJet (coordinateConnectionJet J Gamma)
      (coordinateConnectionDerivative J H Gamma dGamma) i j =
      pulledCurvatureJet J (connectionCurvatureJet Gamma dGamma) i j := by
  have hswap :
      (∑ a : Fin 4, ∑ b : Fin 4, (J a j*J b i) • (Gamma a*Gamma b)) =
        ∑ a : Fin 4, ∑ b : Fin 4, (J a i*J b j) • (Gamma b*Gamma a) :=
    swapped_weighted_sum J (fun a b => Gamma b*Gamma a) i j
  unfold connectionCurvatureJet
  rw [coordinate_connection_product J Gamma i j,coordinate_connection_product J Gamma j i]
  unfold coordinateConnectionDerivative
  simp_rw [hH i]
  rw [swapped_weighted_sum J dGamma i j,hswap]
  simp only [pulledCurvatureJet,smul_add,smul_sub,
    Finset.sum_add_distrib,Finset.sum_sub_distrib]
  abel

theorem gauge_curvature_jet_identity (J D : Tensor4) (A H : ConnectionMatrix4)
    (dA dH : ConnectionDerivative4) (hJD : J*D = 1)
    (hH : ∀ i j, dH i j = dH j i) (i j : Fin 4) :
    connectionCurvatureJet (gaugeConnectionJet J D A H)
      (gaugeConnectionDerivative J D A H dA dH) i j =
      D*connectionCurvatureJet A dA i j*J := by
  have hc (X : Tensor4) : J*(D*X) = X := by rw [← Matrix.mul_assoc,hJD,one_mul]
  unfold connectionCurvatureJet gaugeConnectionJet gaugeConnectionDerivative
  rw [hH i j]
  noncomm_ring [hc]

theorem finite_curvature_jet_identity (J D : Tensor4) (H Gamma : ConnectionMatrix4)
    (dGamma dH : ConnectionDerivative4) (hJD : J*D = 1)
    (hH : ∀ i a j, H i a j = H j a i)
    (hdH : ∀ i j, dH i j = dH j i) (i j : Fin 4) :
    connectionCurvatureJet
      (gaugeConnectionJet J D (coordinateConnectionJet J Gamma) H)
      (gaugeConnectionDerivative J D (coordinateConnectionJet J Gamma) H
        (coordinateConnectionDerivative J H Gamma dGamma) dH) i j =
      D*pulledCurvatureJet J (connectionCurvatureJet Gamma dGamma) i j*J := by
  rw [gauge_curvature_jet_identity J D _ H _ dH hJD hdH i j,
    coordinate_curvature_jet_pullback J H Gamma dGamma hH i j]

#print axioms coordinateConnectionJet
#print axioms coordinateConnectionDerivative
#print axioms gaugeConnectionJet
#print axioms gaugeConnectionDerivative
#print axioms pulledCurvatureJet
#print axioms swapped_weighted_sum
#print axioms coordinate_connection_product
#print axioms coordinate_curvature_jet_pullback
#print axioms gauge_curvature_jet_identity
#print axioms finite_curvature_jet_identity
end
end ChatgptAudit.FiniteCurvatureAlgebra
