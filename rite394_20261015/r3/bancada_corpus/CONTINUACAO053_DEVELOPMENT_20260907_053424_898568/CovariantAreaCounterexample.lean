import LocalPolarizerWitness

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Covariant053
open Matrix TGLExt ChatgptAudit ChatgptAudit.Thermal025 ChatgptAudit.Observable035
  ChatgptAudit.Orbit052 ChatgptAudit.Area045 ChatgptAudit.Angular034 ClosedSubmodule
noncomputable section

abbrev ReferenceOperator :=
  TowerHilbert thirdThermalReference →L[ℂ] TowerHilbert thirdThermalReference

/-- Both forms are normalized on the same first-site GNS orthonormal pair. -/
def normalizedCovariantForm (epsilon : ℝ) :
    ReferenceOperator →ₗ[ℝ] ReferenceOperator →ₗ[ℝ] ℝ :=
  (2 * (1 / 9 + epsilon / 81))⁻¹ • stateCovariantBilinear thirdThermalReference epsilon

theorem normalized_covariant_apply (epsilon : ℝ) (A B : ReferenceOperator) :
    normalizedCovariantForm epsilon A B =
      (2 * (1 / 9 + epsilon / 81))⁻¹ *
        stateCovariantBilinear thirdThermalReference epsilon A B := rfl

theorem normalization_positive (epsilon : ℝ) (he : 0 ≤ epsilon) :
    0 < (2 * (1 / 9 + epsilon / 81))⁻¹ := by
  apply inv_pos.mpr
  linarith

theorem normalized_covariant_symmetric (epsilon : ℝ) (A B : ReferenceOperator) :
    normalizedCovariantForm epsilon A B = normalizedCovariantForm epsilon B A := by
  rw [normalized_covariant_apply, normalized_covariant_apply,
    state_covariant_symmetric]

theorem normalized_covariant_nonneg (epsilon : ℝ) (he : 0 ≤ epsilon)
    (A : ReferenceOperator) : 0 ≤ normalizedCovariantForm epsilon A A := by
  rw [normalized_covariant_apply]
  exact mul_nonneg (normalization_positive epsilon he).le (state_covariant_nonneg _ _ he A)

/-- Covariance quantifies over every actual tower horizon, with the original adjoint action. -/
theorem normalized_covariant_invariant (epsilon : ℝ) (h : TowerHorizon thirdThermalReference)
    (A B : ReferenceOperator) (hA : A ∈ theFactorObject thirdThermalReference)
    (hAsa : IsSelfAdjoint A) (hB : B ∈ theFactorObject thirdThermalReference)
    (hBsa : IsSelfAdjoint B) :
    normalizedCovariantForm epsilon (adT h A) (adT h B) =
      normalizedCovariantForm epsilon A B := by
  rw [normalized_covariant_apply, normalized_covariant_apply,
    state_covariant_invariant _ _ h A B hA hAsa hB hBsa]

theorem normalized_covariant_kernel (epsilon : ℝ) (he : 0 ≤ epsilon)
    (A : ReferenceOperator) (hA : A ∈ theFactorObject thirdThermalReference)
    (hAsa : IsSelfAdjoint A) :
    normalizedCovariantForm epsilon A A = 0 ↔ A ∈ omegaCentralizer thirdThermalReference := by
  rw [normalized_covariant_apply, mul_eq_zero]
  have hn := ne_of_gt (normalization_positive epsilon he)
  simp only [hn, false_or]
  exact state_covariant_kernel _ _ he A hA hAsa

theorem normalized_covariant_positive_iff (epsilon : ℝ) (he : 0 ≤ epsilon)
    (A : ReferenceOperator) (hA : A ∈ theFactorObject thirdThermalReference)
    (hAsa : IsSelfAdjoint A) :
    0 < normalizedCovariantForm epsilon A A ↔
      A ∉ omegaCentralizer thirdThermalReference := by
  have hn := normalized_covariant_nonneg epsilon he A
  have hk := normalized_covariant_kernel epsilon he A hA hAsa
  constructor
  · intro hp hc
    rw [hk.mpr hc] at hp
    exact (lt_irrefl 0) hp
  · intro hc
    exact lt_of_le_of_ne hn (Ne.symm (mt hk.mp hc))

/-- A calculation for any two vectors on which D acts as a real rotation times k. -/
theorem state_covariant_rotating_pair_gram (P : SiteProfile) (epsilon k n : ℝ)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hDA : statePolarizer P (A (hOmega P)) = k • B (hOmega P))
    (hDB : statePolarizer P (B (hOmega P)) = (-k) • A (hOmega P))
    (hAA : inner ℝ (A (hOmega P)) (A (hOmega P)) = n)
    (hBB : inner ℝ (B (hOmega P)) (B (hOmega P)) = n)
    (hAB : inner ℝ (A (hOmega P)) (B (hOmega P)) = 0)
    (hBA : inner ℝ (B (hOmega P)) (A (hOmega P)) = 0) :
    formGram (stateCovariantBilinear P epsilon) A B =
      !![(k^2 + epsilon * k^4) * n, 0; 0, (k^2 + epsilon * k^4) * n] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [formGram, state_covariant_apply, ← ClosedSubmodule.inner_real_eq_re_inner,
      hDA, hDB, map_smul, real_inner_smul_left, real_inner_smul_right,
      hAA, hBB, hAB, hBA] <;> ring

theorem first_pair_real_gram :
    inner ℝ (sitePauliX thirdThermalReference 0 (hOmega _))
      (sitePauliX thirdThermalReference 0 (hOmega _)) = 1 ∧
    inner ℝ (sitePauliY thirdThermalReference 0 (hOmega _))
      (sitePauliY thirdThermalReference 0 (hOmega _)) = 1 ∧
    inner ℝ (sitePauliX thirdThermalReference 0 (hOmega _))
      (sitePauliY thirdThermalReference 0 (hOmega _)) = 0 ∧
    inner ℝ (sitePauliY thirdThermalReference 0 (hOmega _))
      (sitePauliX thirdThermalReference 0 (hOmega _)) = 0 := by
  have hc : inner ℝ (sitePauliX thirdThermalReference 0 (hOmega _))
      (sitePauliY thirdThermalReference 0 (hOmega _)) = 0 := by
    rw [ClosedSubmodule.inner_real_eq_re_inner, pauli_xy_gns_pairing]
    norm_num [thirdThermalReference]
  refine ⟨?_, ?_, hc, ?_⟩
  · rw [real_inner_self_eq_norm_sq, pauli_x_gns_norm, one_pow]
  · rw [real_inner_self_eq_norm_sq, pauli_y_gns_norm, one_pow]
  · rw [real_inner_comm]
    exact hc

theorem first_pair_unnormalized_gram (epsilon : ℝ) :
    formGram (stateCovariantBilinear thirdThermalReference epsilon)
      (sitePauliX thirdThermalReference 0) (sitePauliY thirdThermalReference 0) =
      !![1 / 9 + epsilon / 81, 0; 0, 1 / 9 + epsilon / 81] := by
  rcases first_pair_real_gram with ⟨hxx, hyy, hxy, hyx⟩
  have h := state_covariant_rotating_pair_gram thirdThermalReference epsilon (1 / 3) 1
    (sitePauliX _ 0) (sitePauliY _ 0) first_pauli_polarizer_x
    (by simpa only [neg_div] using first_pauli_polarizer_y) hxx hyy hxy hyx
  convert h using 1 <;> ext i j <;> fin_cases i <;> fin_cases j <;> norm_num <;> ring

theorem double_pair_unnormalized_gram (epsilon : ℝ) :
    formGram (stateCovariantBilinear thirdThermalReference epsilon) doubleFlipX doubleFlipY =
      !![1 / 5 + 9 * epsilon / 125, 0; 0, 1 / 5 + 9 * epsilon / 125] := by
  rcases double_flip_real_gram with ⟨hxx, hyy, hxy, hyx⟩
  have h := state_covariant_rotating_pair_gram thirdThermalReference epsilon (3 / 5) (5 / 9)
    doubleFlipX doubleFlipY double_flip_polarizer_x
    (by simpa only [neg_div] using double_flip_polarizer_y)
    (by simpa only [ClosedSubmodule.inner_real_eq_re_inner] using hxx)
    (by simpa only [ClosedSubmodule.inner_real_eq_re_inner] using hyy)
    (by simpa only [ClosedSubmodule.inner_real_eq_re_inner] using hxy)
    (by simpa only [ClosedSubmodule.inner_real_eq_re_inner] using hyx)
  convert h using 1 <;> ext i j <;> fin_cases i <;> fin_cases j <;> norm_num <;> ring

/-- This fixed trace-one calibration is shared by the entire epsilon family. -/
theorem normalized_first_pair_gram (epsilon : ℝ) (he : 0 ≤ epsilon) :
    formGram (normalizedCovariantForm epsilon)
      (sitePauliX thirdThermalReference 0) (sitePauliY thirdThermalReference 0) =
      !![1 / 2, 0; 0, 1 / 2] := by
  rw [normalizedCovariantForm, form_gram_scale, first_pair_unnormalized_gram]
  have hd : 2 * (1 / 9 + epsilon / 81) ≠ 0 := by
    have hp : 0 < 2 * (1 / 9 + epsilon / 81) := by linarith
    exact ne_of_gt hp
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [Matrix.smul_apply] <;>
    field_simp [hd] <;> ring

theorem normalized_double_pair_gram_zero :
    formGram (normalizedCovariantForm 0) doubleFlipX doubleFlipY =
      !![9 / 10, 0; 0, 9 / 10] := by
  rw [normalizedCovariantForm, form_gram_scale, double_pair_unnormalized_gram]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num

theorem normalized_double_pair_gram_one :
    formGram (normalizedCovariantForm 1) doubleFlipX doubleFlipY =
      !![1377 / 1250, 0; 0, 1377 / 1250] := by
  rw [normalizedCovariantForm, form_gram_scale, double_pair_unnormalized_gram]
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num

theorem normalized_double_pair_area_zero :
    formArea (normalizedCovariantForm 0) doubleFlipX doubleFlipY = 9 / 10 := by
  rw [formArea, normalized_double_pair_gram_zero]
  change Real.sqrt ((!![(9 / 10 : ℝ), 0; 0, 9 / 10] : ScreenMatrix).det) = 9 / 10
  rw [Matrix.det_fin_two]
  change Real.sqrt ((9 / 10 : ℝ) * (9 / 10) - 0 * 0) = 9 / 10
  rw [mul_zero, sub_zero, ← pow_two, Real.sqrt_sq_eq_abs]
  norm_num

theorem normalized_double_pair_area_one :
    formArea (normalizedCovariantForm 1) doubleFlipX doubleFlipY = 1377 / 1250 := by
  rw [formArea, normalized_double_pair_gram_one]
  change Real.sqrt ((!![(1377 / 1250 : ℝ), 0; 0, 1377 / 1250] : ScreenMatrix).det) = 1377 / 1250
  rw [Matrix.det_fin_two]
  change Real.sqrt ((1377 / 1250 : ℝ) * (1377 / 1250) - 0 * 0) = 1377 / 1250
  rw [mul_zero, sub_zero, ← pow_two, Real.sqrt_sq_eq_abs]
  norm_num

theorem normalized_area_gap :
    formArea (normalizedCovariantForm 1) doubleFlipX doubleFlipY -
      formArea (normalizedCovariantForm 0) doubleFlipX doubleFlipY = 126 / 625 := by
  rw [normalized_double_pair_area_one, normalized_double_pair_area_zero]
  norm_num

theorem normalized_forms_distinct : normalizedCovariantForm 0 ≠ normalizedCovariantForm 1 := by
  intro h
  have he := congrArg (fun F => formArea F doubleFlipX doubleFlipY) h
  rw [normalized_double_pair_area_zero, normalized_double_pair_area_one] at he
  norm_num at he

/-- The same calibration cannot make these two global forms scalar multiples. -/
theorem normalized_forms_not_global_rescaling (c : ℝ) :
    normalizedCovariantForm 1 ≠ c • normalizedCovariantForm 0 := by
  intro h
  have hg := congrArg (fun F => formGram F (sitePauliX thirdThermalReference 0)
    (sitePauliY thirdThermalReference 0)) h
  rw [form_gram_scale, normalized_first_pair_gram 1 (by norm_num),
    normalized_first_pair_gram 0 (by norm_num)] at hg
  have he := congrArg (fun G : ScreenMatrix => G 0 0) hg
  norm_num at he
  have hc : c = 1 := by linarith
  rw [hc, one_smul] at h
  exact normalized_forms_distinct h.symm

/-- Fixed state, factor, action, calibration and effective directions; two different areas. -/
theorem two_global_covariant_calibrated_forms :
    ∃ F G : ReferenceOperator →ₗ[ℝ] ReferenceOperator →ₗ[ℝ] ℝ,
      F ≠ G ∧
      (∀ A B, F A B = F B A ∧ G A B = G B A) ∧
      (∀ A, 0 ≤ F A A ∧ 0 ≤ G A A) ∧
      (∀ h : TowerHorizon thirdThermalReference, ∀ A B,
        A ∈ theFactorObject thirdThermalReference → IsSelfAdjoint A →
        B ∈ theFactorObject thirdThermalReference → IsSelfAdjoint B →
        F (adT h A) (adT h B) = F A B ∧ G (adT h A) (adT h B) = G A B) ∧
      (∀ A, A ∈ theFactorObject thirdThermalReference → IsSelfAdjoint A →
        (F A A = 0 ↔ A ∈ omegaCentralizer thirdThermalReference) ∧
        (G A A = 0 ↔ A ∈ omegaCentralizer thirdThermalReference)) ∧
      formGram F (sitePauliX thirdThermalReference 0) (sitePauliY thirdThermalReference 0) =
        !![1 / 2, 0; 0, 1 / 2] ∧
      formGram G (sitePauliX thirdThermalReference 0) (sitePauliY thirdThermalReference 0) =
        !![1 / 2, 0; 0, 1 / 2] ∧
      formArea F doubleFlipX doubleFlipY = 9 / 10 ∧
      formArea G doubleFlipX doubleFlipY = 1377 / 1250 ∧
      Function.Injective doubleFlipResponse := by
  refine ⟨normalizedCovariantForm 0, normalizedCovariantForm 1,
    normalized_forms_distinct, ?_, ?_, ?_, ?_,
    normalized_first_pair_gram 0 (by norm_num), normalized_first_pair_gram 1 (by norm_num),
    normalized_double_pair_area_zero, normalized_double_pair_area_one,
    double_flip_response_injective⟩
  · intro A B
    exact ⟨normalized_covariant_symmetric 0 A B, normalized_covariant_symmetric 1 A B⟩
  · intro A
    exact ⟨normalized_covariant_nonneg 0 (by norm_num) A,
      normalized_covariant_nonneg 1 (by norm_num) A⟩
  · intro h A B hA hAsa hB hBsa
    exact ⟨normalized_covariant_invariant 0 h A B hA hAsa hB hBsa,
      normalized_covariant_invariant 1 h A B hA hAsa hB hBsa⟩
  · intro A hA hAsa
    exact ⟨normalized_covariant_kernel 0 (by norm_num) A hA hAsa,
      normalized_covariant_kernel 1 (by norm_num) A hA hAsa⟩

/-- Adding a self-adjoint stationary direction changes neither argument of the form. -/
theorem normalized_covariant_add_centralizer_left (epsilon : ℝ)
    (A B C : ReferenceOperator) (hC : C ∈ omegaCentralizer thirdThermalReference)
    (hCsa : IsSelfAdjoint C) :
    normalizedCovariantForm epsilon (A + C) B = normalizedCovariantForm epsilon A B := by
  rw [normalized_covariant_apply, normalized_covariant_apply,
    state_covariant_add_centralizer _ epsilon A B C hC hCsa]

theorem normalized_covariant_add_centralizer_right (epsilon : ℝ)
    (A B C : ReferenceOperator) (hC : C ∈ omegaCentralizer thirdThermalReference)
    (hCsa : IsSelfAdjoint C) :
    normalizedCovariantForm epsilon A (B + C) = normalizedCovariantForm epsilon A B := by
  rw [normalized_covariant_symmetric epsilon A (B + C),
    normalized_covariant_add_centralizer_left epsilon B A C hC hCsa,
    normalized_covariant_symmetric epsilon B A]

/-- The radical is exactly the kernel of the already defined actual state response. -/
theorem normalized_covariant_response_kernel (epsilon : ℝ) (he : 0 ≤ epsilon)
    (A : ReferenceOperator) (hA : A ∈ theFactorObject thirdThermalReference)
    (hAsa : IsSelfAdjoint A) :
    normalizedCovariantForm epsilon A A = 0 ↔
      ∀ B : ReferenceOperator, B ∈ theFactorObject thirdThermalReference →
        IsSelfAdjoint B → realStateResponse thirdThermalReference A B = 0 :=
  (normalized_covariant_kernel epsilon he A hA hAsa).trans
    (state_response_kernel thirdThermalReference A hA hAsa).symm

#print axioms ReferenceOperator
#print axioms normalizedCovariantForm
#print axioms normalized_covariant_apply
#print axioms normalization_positive
#print axioms normalized_covariant_symmetric
#print axioms normalized_covariant_nonneg
#print axioms normalized_covariant_invariant
#print axioms normalized_covariant_kernel
#print axioms normalized_covariant_positive_iff
#print axioms state_covariant_rotating_pair_gram
#print axioms first_pair_real_gram
#print axioms first_pair_unnormalized_gram
#print axioms double_pair_unnormalized_gram
#print axioms normalized_first_pair_gram
#print axioms normalized_double_pair_gram_zero
#print axioms normalized_double_pair_gram_one
#print axioms normalized_double_pair_area_zero
#print axioms normalized_double_pair_area_one
#print axioms normalized_area_gap
#print axioms normalized_forms_distinct
#print axioms normalized_forms_not_global_rescaling
#print axioms two_global_covariant_calibrated_forms
#print axioms normalized_covariant_add_centralizer_left
#print axioms normalized_covariant_add_centralizer_right
#print axioms normalized_covariant_response_kernel
end
end ChatgptAudit.Covariant053
