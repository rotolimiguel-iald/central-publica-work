import TGLExt.FiniteCoordinateCurvature

set_option autoImplicit false
set_option maxHeartbeats 1600000
namespace ChatgptAudit.FiniteRicciContraction
open Matrix TGLExt ChatgptAudit.FiniteCurvatureAlgebra
noncomputable section

theorem weighted_diagonal_contraction (J D : Tensor4) (B : Fin 4 → Tensor4)
    (hJD : J*D = 1) (b : Fin 4) :
    (∑ a : Fin 4, (D*(∑ p : Fin 4, J p a • B p)) a b) =
      ∑ p : Fin 4, B p p b := by
  let M : Tensor4 := fun l p => B p l b
  have he :
      (∑ a : Fin 4, (D*(∑ p : Fin 4, J p a • B p)) a b) =
        Matrix.trace (D*M*J) := by
    change (∑ a : Fin 4, _) = ∑ a : Fin 4, (D*M*J) a a
    apply Finset.sum_congr rfl
    intro a _
    simp only [Matrix.mul_apply,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul,
      Finset.mul_sum,Finset.sum_mul]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro p _
    apply Finset.sum_congr rfl
    intro l _
    dsimp [M]
    ring
  rw [he,Matrix.trace_mul_comm (D*M) J,← Matrix.mul_assoc,hJD,one_mul]
  rfl

theorem finite_ricci_contraction (J D : Tensor4) (R : Fin 4 → Fin 4 → Tensor4)
    (hJD : J*D = 1) :
    Matrix.of (fun b j => ∑ a : Fin 4, (D*pulledCurvatureJet J R a j*J) a b) =
      Jᵀ * Matrix.of (fun b j => ∑ a : Fin 4, R a j a b) * J := by
  apply Matrix.ext
  intro b j
  change (∑ a : Fin 4, (D*pulledCurvatureJet J R a j*J) a b) =
    (Jᵀ * Matrix.of (fun b j => ∑ a : Fin 4, R a j a b) * J) b j
  have he (a : Fin 4) :
      D*pulledCurvatureJet J R a j*J =
        D*(∑ p : Fin 4, J p a • ((∑ q : Fin 4, J q j • R p q)*J)) := by
    rw [Matrix.mul_assoc]
    congr 1
    simp only [pulledCurvatureJet,Matrix.sum_mul,Matrix.smul_mul,
      Finset.smul_sum,smul_smul]
  simp_rw [he]
  rw [weighted_diagonal_contraction J D _ hJD b]
  simp only [Matrix.mul_apply,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul,
    Matrix.transpose_apply,Matrix.of_apply,Finset.sum_mul,Finset.mul_sum]
  calc
    (∑ p : Fin 4, ∑ r : Fin 4, ∑ q : Fin 4, (J q j * R p q p r) * J r b) =
        ∑ r : Fin 4, ∑ q : Fin 4, ∑ p : Fin 4, (J q j * R p q p r) * J r b := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro r _
      rw [Finset.sum_comm]
    _ = ∑ q : Fin 4, ∑ r : Fin 4, ∑ p : Fin 4,
        (J r b * R p q p r) * J q j := by
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro q _
      apply Finset.sum_congr rfl
      intro r _
      apply Finset.sum_congr rfl
      intro p _
      ring

theorem finite_scalar_contraction (J D gi R : Tensor4)
    (hJD : J*D = 1) (hs : giᵀ = gi) :
    (∑ i : Fin 4, ∑ j : Fin 4, (D*gi*Dᵀ) i j * (Jᵀ*R*J) i j) =
      ∑ i : Fin 4, ∑ j : Fin 4, gi i j * R i j := by
  have ht : Dᵀ*Jᵀ = 1 := by rw [← Matrix.transpose_mul,hJD,Matrix.transpose_one]
  have hd : (D*gi*Dᵀ)ᵀ = D*gi*Dᵀ := by
    simp only [Matrix.transpose_mul,Matrix.transpose_transpose,hs,Matrix.mul_assoc]
  rw [matrix_contraction_eq_trace _ _ hd,matrix_contraction_eq_trace _ _ hs]
  have hm : (D*gi*Dᵀ)*(Jᵀ*R*J) = (D*(gi*R))*J := by
    calc
      _ = D*gi*(Dᵀ*Jᵀ)*R*J := by noncomm_ring
      _ = _ := by rw [ht]; noncomm_ring
  rw [hm,Matrix.trace_mul_comm _ J,← Matrix.mul_assoc,hJD,one_mul]

theorem finite_einstein_congruence (J g R : Tensor4) (s : ℝ) :
    Jᵀ*R*J - (s/2) • (Jᵀ*g*J) =
      Jᵀ*(R-(s/2) • g)*J := by
  simp only [Matrix.mul_sub,Matrix.sub_mul,Matrix.mul_smul,Matrix.smul_mul]

#print axioms weighted_diagonal_contraction
#print axioms finite_ricci_contraction
#print axioms finite_scalar_contraction
#print axioms finite_einstein_congruence
end
end ChatgptAudit.FiniteRicciContraction
