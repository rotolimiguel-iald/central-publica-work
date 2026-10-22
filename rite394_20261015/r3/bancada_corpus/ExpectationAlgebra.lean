import CentralizerDensity
import AperiodicCentralizerExpectation

set_option autoImplicit false
set_option maxHeartbeats 1200000

namespace ChatgptAudit.Expectation047

open TGLExt ChatgptAudit.Density033 ChatgptAudit.Aperiodic046

noncomputable section

/-- The vector state takes adjoints to scalar conjugates. -/
theorem omega_state_star (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaState P (star A) = star (omegaState P A) := by
  change inner ℂ (hOmega P) (ContinuousLinearMap.adjoint A (hOmega P)) =
    star (inner ℂ (hOmega P) (A (hOmega P)))
  rw [ContinuousLinearMap.adjoint_inner_right]
  exact (inner_conj_symm (A (hOmega P)) (hOmega P)).symm

/-- The state centralizer is closed under adjoints. -/
theorem omega_centralizer_star (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ omegaCentralizer P) :
    star A ∈ omegaCentralizer P := by
  refine ⟨star_mem hA.1, ?_⟩
  intro B hB
  have h := hA.2 (star B) (star_mem hB)
  have hs : omegaState P (star (A * star B)) =
      omegaState P (star (star B * A)) := by
    simpa only [omega_state_star] using congrArg star h
  simpa only [star_mul, star_star] using hs.symm

/-- Orthogonality determines a single image, without positing a second expectation. -/
theorem expectation_eq_of_ortho (P : SiteProfile) (I : ExpectationInput P)
    (A C : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hC : C ∈ omegaCentralizer P)
    (h : ∀ B ∈ omegaCentralizer P, omegaState P (star B * (A-C)) = 0) :
    I.E A = C := by
  have hE := I.into A hA
  have hD : I.E A-C ∈ omegaCentralizer P := by
    refine ⟨sub_mem hE.1 hC.1, ?_⟩
    intro B hB
    rw [sub_mul, mul_sub, omegaState_sub, omegaState_sub, hE.2 B hB, hC.2 B hB]
  apply sub_eq_zero.mp
  apply omega_definite hD.1
  have hid : I.E A-C = (A-C)-(A-I.E A) := by abel
  calc
    omegaState P (star (I.E A-C) * (I.E A-C)) =
        omegaState P (star (I.E A-C) * ((A-C)-(A-I.E A))) :=
      congrArg (fun X => omegaState P (star (I.E A-C) * X)) hid
    _ = 0 := by
      rw [mul_sub, omegaState_sub, h _ hD, I.ortho A hA _ hD, sub_self]

theorem expectation_zero (P : SiteProfile) (I : ExpectationInput P) :
    I.E 0 = 0 :=
  I.fixes 0 (omega_centralizer_zero P)

theorem expectation_one (P : SiteProfile) (I : ExpectationInput P) :
    I.E 1 = 1 :=
  I.fixes 1 (omega_centralizer_one P)

theorem expectation_add (P : SiteProfile) (I : ExpectationInput P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P) :
    I.E (A+B) = I.E A+I.E B := by
  apply expectation_eq_of_ortho P I (A+B) (I.E A+I.E B) (add_mem hA hB)
    (omega_centralizer_add P (I.into A hA) (I.into B hB))
  intro C hC
  have hid : A+B-(I.E A+I.E B) = (A-I.E A)+(B-I.E B) := by abel
  rw [hid, mul_add, omega_state_add, I.ortho A hA C hC, I.ortho B hB C hC, add_zero]

theorem expectation_smul (P : SiteProfile) (I : ExpectationInput P) (c : ℂ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    I.E (c • A) = c • I.E A := by
  apply expectation_eq_of_ortho P I (c • A) (c • I.E A)
    ((theFactorObject P).toStarSubalgebra.smul_mem hA c)
    (omega_centralizer_smul P c (I.into A hA))
  intro B hB
  rw [← smul_sub, mul_smul_comm, omega_state_smul, I.ortho A hA B hB, mul_zero]

theorem expectation_sub (P : SiteProfile) (I : ExpectationInput P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P) :
    I.E (A-B) = I.E A-I.E B := by
  have hE : I.E A-I.E B ∈ omegaCentralizer P := by
    refine ⟨sub_mem (I.into A hA).1 (I.into B hB).1, ?_⟩
    intro C hC
    rw [sub_mul, mul_sub, omegaState_sub, omegaState_sub,
      (I.into A hA).2 C hC, (I.into B hB).2 C hC]
  apply expectation_eq_of_ortho P I (A-B) (I.E A-I.E B) (sub_mem hA hB) hE
  intro C hC
  have hid : A-B-(I.E A-I.E B) = (A-I.E A)-(B-I.E B) := by abel
  rw [hid, mul_sub, omegaState_sub, I.ortho A hA C hC, I.ortho B hB C hC, sub_self]

theorem expectation_preserves_omega (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    omegaState P (I.E A) = omegaState P A := by
  have h := I.ortho A hA 1 (omega_centralizer_one P)
  rw [star_one, one_mul, omegaState_sub] at h
  exact (sub_eq_zero.mp h).symm

/-- Adjoint preservation uses centralizer cyclicity and orthogonality. -/
theorem expectation_star (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    I.E (star A) = star (I.E A) := by
  apply expectation_eq_of_ortho P I (star A) (star (I.E A)) (star_mem hA)
    (omega_centralizer_star P (I.E A) (I.into A hA))
  intro B hB
  have h := I.ortho A hA (star B) (omega_centralizer_star P B hB)
  simp only [star_star] at h
  have hr : omegaState P ((A-I.E A)*B) = 0 :=
    (hB.2 (A-I.E A) (sub_mem hA (I.into A hA).1)).symm.trans h
  have hs : omegaState P (star ((A-I.E A)*B)) = 0 := by
    rw [omega_state_star, hr, star_zero]
  simpa only [star_mul, star_sub] using hs

theorem expectation_mul_left (P : SiteProfile) (I : ExpectationInput P)
    (C A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hC : C ∈ omegaCentralizer P) (hA : A ∈ theFactorObject P) :
    I.E (C*A) = C*I.E A := by
  apply expectation_eq_of_ortho P I (C*A) (C*I.E A) (mul_mem hC.1 hA)
    (omega_centralizer_mul P hC (I.into A hA))
  intro B hB
  have h := I.ortho A hA (star C*B)
    (omega_centralizer_mul P (omega_centralizer_star P C hC) hB)
  rw [star_mul, star_star] at h
  calc
    omegaState P (star B*(C*A-C*I.E A)) =
        omegaState P ((star B*C)*(A-I.E A)) := by
      congr 1
      noncomm_ring
    _ = 0 := h

theorem expectation_mul_right (P : SiteProfile) (I : ExpectationInput P)
    (A D : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hD : D ∈ omegaCentralizer P) :
    I.E (A*D) = I.E A*D := by
  apply expectation_eq_of_ortho P I (A*D) (I.E A*D) (mul_mem hA hD.1)
    (omega_centralizer_mul P (I.into A hA) hD)
  intro B hB
  have h := I.ortho A hA (B*star D)
    (omega_centralizer_mul P hB (omega_centralizer_star P D hD))
  rw [star_mul, star_star] at h
  calc
    omegaState P (star B*(A*D-I.E A*D)) =
        omegaState P ((star B*(A-I.E A))*D) := by
      congr 1
    _ = omegaState P (D*(star B*(A-I.E A))) :=
      (hD.2 (star B*(A-I.E A))
        (mul_mem (star_mem hB.1) (sub_mem hA (I.into A hA).1))).symm
    _ = omegaState P ((D*star B)*(A-I.E A)) := by rw [mul_assoc]
    _ = 0 := h

theorem expectation_bimodular (P : SiteProfile) (I : ExpectationInput P)
    (C A D : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hC : C ∈ omegaCentralizer P) (hA : A ∈ theFactorObject P)
    (hD : D ∈ omegaCentralizer P) :
    I.E (C*A*D) = C*I.E A*D := by
  rw [expectation_mul_right P I (C*A) D (mul_mem hC.1 hA) hD,
    expectation_mul_left P I C A hC hA]

/-- Any contract inherits the constructed norm estimate by uniqueness on the factor. -/
theorem expectation_norm_le (P : SiteProfile) (I : ExpectationInput P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    ‖I.E A‖ ≤ ‖A‖ := by
  rw [the_expectation_is_unique I (aperiodicExpectationInput P) A hA]
  exact aperiodic_expectation_contractive P A hA

/-- The expectation is linear on the factor; no assertion concerns external inputs. -/
def expectationLinearMap (P : SiteProfile) (I : ExpectationInput P) :
    (theFactorObject P).toStarSubalgebra →ₗ[ℂ]
      (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toFun := fun A => I.E A
  map_add' := fun A B => expectation_add P I A B A.property B.property
  map_smul' := fun c A => expectation_smul P I c A A.property

theorem expectation_linear_map_apply (P : SiteProfile) (I : ExpectationInput P)
    (A : (theFactorObject P).toStarSubalgebra) :
    expectationLinearMap P I A = I.E A := rfl

/-- Continuity follows from the norm bound, which was derived rather than added to the contract. -/
def expectationContinuousLinearMap (P : SiteProfile) (I : ExpectationInput P) :
    (theFactorObject P).toStarSubalgebra →L[ℂ]
      (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  (expectationLinearMap P I).mkContinuous 1 (fun A => by
    change ‖I.E A‖ ≤ 1*‖(A : TowerHilbert P →L[ℂ] TowerHilbert P)‖
    simpa only [one_mul] using expectation_norm_le P I A A.property)

theorem expectation_continuous_linear_map_apply (P : SiteProfile) (I : ExpectationInput P)
    (A : (theFactorObject P).toStarSubalgebra) :
    expectationContinuousLinearMap P I A = I.E A := rfl

theorem expectation_continuous_linear_map_norm_le_one (P : SiteProfile)
    (I : ExpectationInput P) :
    ‖expectationContinuousLinearMap P I‖ ≤ 1 := by
  apply ContinuousLinearMap.opNorm_le_bound _ (by norm_num)
  intro A
  change ‖I.E A‖ ≤ 1*‖(A : TowerHilbert P →L[ℂ] TowerHilbert P)‖
  simpa only [one_mul] using expectation_norm_le P I A A.property

#print axioms omega_state_star
#print axioms omega_centralizer_star
#print axioms expectation_eq_of_ortho
#print axioms expectation_zero
#print axioms expectation_one
#print axioms expectation_add
#print axioms expectation_smul
#print axioms expectation_sub
#print axioms expectation_preserves_omega
#print axioms expectation_star
#print axioms expectation_mul_left
#print axioms expectation_mul_right
#print axioms expectation_bimodular
#print axioms expectation_norm_le
#print axioms expectationLinearMap
#print axioms expectation_linear_map_apply
#print axioms expectationContinuousLinearMap
#print axioms expectation_continuous_linear_map_apply
#print axioms expectation_continuous_linear_map_norm_le_one

end

end ChatgptAudit.Expectation047
