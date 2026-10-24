import TGLExt.V350DualFixedWeightLaws
import TGLExt.V350PositiveResolvent

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 2200000

namespace TGLV350.Regular
open Filter MeasureTheory
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Order between self-adjoint operators is determined by all quadratic readings. -/
theorem selfAdjoint_le_of_quadratic_le (A B : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (h : ∀ v, (inner ℂ v (A v)).re ≤ (inner ℂ v (B v)).re) : A ≤ B := by
  apply sub_nonneg.mp
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  refine ⟨ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp (hB.sub hA), ?_⟩
  intro v
  change 0 ≤ (inner ℂ ((B-A) v) v).re
  rw [show (inner ℂ ((B-A) v) v).re = (inner ℂ v ((B-A) v)).re from
    inner_re_symm (𝕜 := ℂ) _ _]
  simp only [_root_.sub_apply, inner_sub_right, Complex.sub_re]
  exact sub_nonneg.mpr (h v)

theorem selfAdjoint_eq_of_quadratic_eq (A B : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (h : ∀ v, (inner ℂ v (A v)).re = (inner ℂ v (B v)).re) : A = B :=
  le_antisymm (selfAdjoint_le_of_quadratic_le A B hA hB (fun v => (h v).le))
    (selfAdjoint_le_of_quadratic_le B A hB hA (fun v => (h v).ge))

theorem positive_le_scalar_of_quadratic_bound (A : H →L[ℂ] H) (hA : 0 ≤ A)
    (C : ℝ) (h : ∀ v, (inner ℂ v (A v)).re ≤ C * ‖v‖ ^ 2) :
    A ≤ C • (1 : H →L[ℂ] H) := by
  have hs : IsSelfAdjoint (C • (1 : H →L[ℂ] H)) := by
    change IsSelfAdjoint ((C : ℂ) • (1 : H →L[ℂ] H))
    simp [IsSelfAdjoint]
  apply selfAdjoint_le_of_quadratic_le A _ (IsSelfAdjoint.of_nonneg hA) hs
  intro v
  change (inner ℂ v (A v)).re ≤ (inner ℂ v ((C : ℂ) • v)).re
  rw [inner_smul_right]
  simp only [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, zero_mul, sub_zero]
  have he : (inner ℂ v v).re = ‖v‖ ^ 2 := inner_self_eq_norm_sq (𝕜 := ℂ) v
  rw [he]
  exact h v

theorem normalizedDualCut_le_of_uniform_bound
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (C : ℝ) (hC : 0 ≤ C)
    (hbound : ∀ v, dualQuadraticIntegral A v ≤ ENNReal.ofReal (C * ‖v‖ ^ 2))
    (n : ℕ) : normalizedDualCut (n : ℝ) A ≤ C • 1 := by
  apply positive_le_scalar_of_quadratic_bound _
    (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA) C
  intro v
  have he : ENNReal.ofReal (inner ℂ v (normalizedDualCut (n : ℝ) A v)).re ≤
      ENNReal.ofReal (C * ‖v‖ ^ 2) := by
    rw [normalizedDualCut_quadratic, ENNReal.ofReal_mul dualHaarFactor_pos.le]
    exact (dualWeightCut_quadratic_le _ (Nat.cast_nonneg n) A hA v).trans (hbound v)
  have hr := ENNReal.toReal_mono ENNReal.ofReal_ne_top he
  have hp : 0 ≤ (inner ℂ v (normalizedDualCut (n : ℝ) A v)).re :=
    ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
      (normalizedDualCut_nonneg _ (Nat.cast_nonneg n) A hA)).re_inner_nonneg_right v
  simpa only [ENNReal.toReal_ofReal hp, ENNReal.toReal_ofReal (mul_nonneg hC (sq_nonneg _))] using hr

theorem exists_boundedDualCutLimit (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hm : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) (C : ℝ) (hC : 0 ≤ C)
    (hbound : ∀ v, dualQuadraticIntegral A v ≤ ENNReal.ofReal (C * ‖v‖ ^ 2)) :
    ∃ B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P),
      B ∈ regularCoreAlgebra P ∧ 0 ≤ B ∧ B ≤ C • 1 ∧
      (∀ v, Tendsto (fun n : ℕ => normalizedDualCut (n : ℝ) A v) atTop (𝓝 (B v))) ∧
      IsLUB (Set.range (fun n : ℕ => normalizedDualCut (n : ℝ) A)) B := by
  have hp := fun n : ℕ => normalizedDualCut_nonneg (n : ℝ) (Nat.cast_nonneg n) A hA
  have hmono : Monotone (fun n : ℕ => normalizedDualCut (n : ℝ) A) := by
    intro n m hnm
    exact normalizedDualCut_mono_radius (Nat.cast_nonneg n) (by exact_mod_cast hnm) A hA
  have hu := normalizedDualCut_le_of_uniform_bound A hA C hC hbound
  obtain ⟨B,hB,_,ht,hL⟩ := ChatgptAudit.Expectation047.monotone_operator_limit
    (fun n : ℕ => normalizedDualCut (n : ℝ) A) hp hmono ‖C • (1 :
      RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))‖
    (norm_nonneg _) (fun n => CStarAlgebra.norm_le_norm_of_nonneg_of_le (hp n) (hu n))
  refine ⟨B, vonNeumann_mem_of_strong_limit (regularCoreAlgebra P)
    (fun n : ℕ => normalizedDualCut (n : ℝ) A) B
    (Eventually.of_forall (fun n : ℕ => normalizedDualCut_mem P (n : ℝ) A hm)) ht,
    hB, hL.2 ?_, ht, hL⟩
  rintro _ ⟨n,rfl⟩
  exact hu n

theorem quadratic_le_of_operator_le (A B : H →L[ℂ] H) (h : A ≤ B) (v : H) :
    (inner ℂ v (A v)).re ≤ (inner ℂ v (B v)).re := by
  have hp := ((ContinuousLinearMap.nonneg_iff_isPositive _).mp
    (sub_nonneg.mpr h)).re_inner_nonneg_right v
  change 0 ≤ (inner ℂ v ((B-A) v)).re at hp
  simpa only [_root_.sub_apply, inner_sub_right, Complex.sub_re, sub_nonneg] using hp

/-- The actual dual integral is represented by the bounded cut limit.
No conversion of an infinite extended value to a real number is used. -/
theorem dualQuadraticIntegral_eq_boundedCutLimit
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (ht : ∀ v, Tendsto (fun n : ℕ => normalizedDualCut (n : ℝ) A v) atTop (𝓝 (B v)))
    (hL : IsLUB (Set.range (fun n : ℕ => normalizedDualCut (n : ℝ) A)) B)
    (v : RegularHilbert H) :
    dualQuadraticIntegral A v = ENNReal.ofReal (inner ℂ v (B v)).re := by
  have hq : Tendsto (fun n : ℕ => ENNReal.ofReal
      (inner ℂ v (normalizedDualCut (n : ℝ) A v)).re) atTop
      (𝓝 (ENNReal.ofReal (inner ℂ v (B v)).re)) :=
    ENNReal.continuous_ofReal.continuousAt.tendsto.comp
      (Complex.continuous_re.continuousAt.tendsto.comp
        (tendsto_const_nhds.inner (ht v)))
  apply le_antisymm
  · rw [dualQuadraticIntegral_eq_iSup_normalized_cuts A hA v]
    exact iSup_le fun n => ENNReal.ofReal_le_ofReal
      (quadratic_le_of_operator_le _ B (hL.1 (Set.mem_range_self n)) v)
  · apply le_of_tendsto hq
    apply Eventually.of_forall
    intro n
    rw [dualQuadraticIntegral_eq_iSup_normalized_cuts A hA v]
    exact le_iSup (fun m : ℕ => ENNReal.ofReal
      (inner ℂ v (normalizedDualCut (m : ℝ) A v)).re) n

theorem boundedDualValue_unique
    (A B D : RegularHilbert H →L[ℂ] RegularHilbert H) (hB : 0 ≤ B) (hD : 0 ≤ D)
    (hrepB : ∀ v, dualQuadraticIntegral A v = ENNReal.ofReal (inner ℂ v (B v)).re)
    (hrepD : ∀ v, dualQuadraticIntegral A v = ENNReal.ofReal (inner ℂ v (D v)).re) :
    B = D := by
  apply selfAdjoint_eq_of_quadratic_eq B D (IsSelfAdjoint.of_nonneg hB)
    (IsSelfAdjoint.of_nonneg hD)
  intro v
  have he := (hrepB v).symm.trans (hrepD v)
  have hpB : 0 ≤ (inner ℂ v (B v)).re :=
    ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hB).re_inner_nonneg_right v
  have hpD : 0 ≤ (inner ℂ v (D v)).re :=
    ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hD).re_inner_nonneg_right v
  have hr := congrArg ENNReal.toReal he
  simpa only [ENNReal.toReal_ofReal hpB, ENNReal.toReal_ofReal hpD] using hr

/-- A bounded representative of the dual integral is fixed by the same dual action. -/
theorem boundedDualValue_dual_fixed
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hB : 0 ≤ B)
    (hrep : ∀ v, dualQuadraticIntegral A v = ENNReal.ofReal (inner ℂ v (B v)).re)
    (s : ℝ) : dualAmbient s B = B := by
  apply boundedDualValue_unique A _ B (dualAmbient_nonneg s B hB) hB _ hrep
  intro v
  have hc := operatorQuadratic_conjugate B (star (characterMultiplier (H := H) s)) v
  simp only [characterMultiplier_star, neg_neg] at hc
  rw [dualAmbient_apply, characterMultiplier_star, hc]
  exact (dualQuadraticIntegral_vector_dual_invariant (-s) A v).symm.trans
    (hrep (characterMultiplier (-s) v))

/-- Every uniformly bounded positive dual form is represented by a unique positive
bounded operator in F, the fixed algebra of this particular regular core. -/
theorem exists_boundedDualValue_in_fixedCore (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hm : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) (C : ℝ) (hC : 0 ≤ C)
    (hbound : ∀ v, dualQuadraticIntegral A v ≤ ENNReal.ofReal (C * ‖v‖ ^ 2)) :
    ∃ B : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P),
      B ∈ dualFixedCore P ∧ 0 ≤ B ∧ B ≤ C • 1 ∧
      (∀ v, dualQuadraticIntegral A v = ENNReal.ofReal (inner ℂ v (B v)).re) := by
  obtain ⟨B,hmB,hB,hBC,ht,hL⟩ := exists_boundedDualCutLimit P A hm hA C hC hbound
  have hrep := dualQuadraticIntegral_eq_boundedCutLimit A B hA ht hL
  exact ⟨B,(dualFixedCore_mem_iff P B).mpr
    ⟨hmB,boundedDualValue_dual_fixed A B hB hrep⟩,hB,hBC,hrep⟩

#print axioms selfAdjoint_le_of_quadratic_le
#print axioms selfAdjoint_eq_of_quadratic_eq
#print axioms positive_le_scalar_of_quadratic_bound
#print axioms normalizedDualCut_le_of_uniform_bound
#print axioms exists_boundedDualCutLimit
#print axioms quadratic_le_of_operator_le
#print axioms dualQuadraticIntegral_eq_boundedCutLimit
#print axioms boundedDualValue_unique
#print axioms boundedDualValue_dual_fixed
#print axioms exists_boundedDualValue_in_fixedCore
end
end TGLV350.Regular
