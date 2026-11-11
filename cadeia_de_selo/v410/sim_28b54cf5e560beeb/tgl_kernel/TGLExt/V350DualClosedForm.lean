import TGLExt.V350DualQuadraticLaws

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

namespace TGLV350.Regular
open MeasureTheory
open scoped ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- A lower semicontinuous extended positive quadratic form. Its finite domain
need not be dense. No spectral representation theorem is built into this structure. -/
structure ClosedPositiveForm (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] where
  value : H → ℝ≥0∞
  map_zero : value 0 = 0
  map_smul : ∀ (c : ℂ) (v : H), value (c • v) = ENNReal.ofReal (‖c‖^2) * value v
  parallelogram : ∀ v w, value (v+w) + value (v-w) = 2*value v + 2*value w
  lowerSemicontinuous : LowerSemicontinuous value

namespace ClosedPositiveForm

theorem add_le (Q : ClosedPositiveForm H) (v w : H) :
    Q.value (v+w) ≤ 2*Q.value v + 2*Q.value w := by
  rw [← Q.parallelogram]
  exact le_self_add

/-- The finite domain is constructed from the form, not supplied as input. -/
def finiteDomain (Q : ClosedPositiveForm H) : Submodule ℂ H where
  carrier := {v | Q.value v < ⊤}
  zero_mem' := by simp only [Set.mem_setOf_eq, Q.map_zero, ENNReal.zero_lt_top]
  add_mem' := by
    intro v w hv hw
    exact lt_of_le_of_lt (Q.add_le v w)
      (ENNReal.add_lt_top.mpr ⟨ENNReal.mul_lt_top (by norm_num) hv,
        ENNReal.mul_lt_top (by norm_num) hw⟩)
  smul_mem' := by
    intro c v hv
    change Q.value (c • v) < ⊤
    rw [Q.map_smul]
    exact ENNReal.mul_lt_top ENNReal.ofReal_lt_top hv

theorem mem_finiteDomain (Q : ClosedPositiveForm H) (v : H) :
    v ∈ Q.finiteDomain ↔ Q.value v < ⊤ := Iff.rfl

theorem isClosed_sublevel (Q : ClosedPositiveForm H) (c : ℝ≥0∞) :
    IsClosed {v | Q.value v ≤ c} := Q.lowerSemicontinuous.isClosed_preimage c

end ClosedPositiveForm

def dualClosedPositiveForm
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    ClosedPositiveForm (RegularHilbert H) where
  value := dualQuadraticIntegral A
  map_zero := dualQuadraticIntegral_zero_vector A
  map_smul := fun c v => dualQuadraticIntegral_smul_vector A v c
  parallelogram := dualQuadraticIntegral_parallelogram A hA
  lowerSemicontinuous := dualQuadraticIntegral_lowerSemicontinuous A hA

theorem dualClosedPositiveForm_one_domain :
    (dualClosedPositiveForm (1 : RegularHilbert H →L[ℂ] RegularHilbert H)
      zero_le_one).finiteDomain = ⊥ := by
  ext v
  change dualQuadraticIntegral 1 v < ⊤ ↔ v = 0
  constructor
  · intro hv
    by_contra hne
    rw [dualQuadraticIntegral_one v hne] at hv
    exact (lt_irrefl _) hv
  · rintro rfl
    rw [dualQuadraticIntegral_zero_vector]
    exact ENNReal.zero_lt_top

theorem dualClosedPositiveForm_zero_domain :
    (dualClosedPositiveForm (0 : RegularHilbert H →L[ℂ] RegularHilbert H)
      le_rfl).finiteDomain = ⊤ := by
  ext v
  change dualQuadraticIntegral 0 v < ⊤ ↔ True
  simp only [dualQuadraticIntegral_zero, ENNReal.zero_lt_top, iff_self]

/-- Invariance under the full unitary commutant, expressed directly in this
representation. This does not assume a spectral operator realizing the form. -/
structure AffiliatedPositiveForm (N : VonNeumannAlgebra H) extends ClosedPositiveForm H where
  unitary_commutant_invariant : ∀ (U : unitary (H →L[ℂ] H)),
    (∀ B ∈ N, (U : H →L[ℂ] H) * B = B * (U : H →L[ℂ] H)) →
    ∀ v, value ((U : H →L[ℂ] H) v) = value v

theorem dualQuadraticIntegral_commutant_invariant
    (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) (hpos : 0 ≤ A)
    (U : unitary (RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P)))
    (hU : ∀ B ∈ regularCoreAlgebra P, U.val * B = B * U.val)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualQuadraticIntegral A (U.val v) = dualQuadraticIntegral A v := by
  rw [dualQuadraticIntegral_eq_iSup_cuts A hpos, dualQuadraticIntegral_eq_iSup_cuts A hpos]
  apply congrArg iSup
  funext n
  have hc := hU (dualWeightCut (n : ℝ) A) (dualWeightCut_mem P (n : ℝ) A hA)
  have hv : dualWeightCut (n : ℝ) A (U.val v) = U.val (dualWeightCut (n : ℝ) A v) :=
    (congrArg (fun B => B v) hc).symm
  rw [hv, Unitary.inner_map_map U]

def dualAffiliatedPositiveForm (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) (hpos : 0 ≤ A) :
    AffiliatedPositiveForm (regularCoreAlgebra P) where
  toClosedPositiveForm := dualClosedPositiveForm A hpos
  unitary_commutant_invariant := fun U hU v => dualQuadraticIntegral_commutant_invariant P A hA hpos U hU v

#print axioms ClosedPositiveForm.finiteDomain
#print axioms ClosedPositiveForm.isClosed_sublevel
#print axioms dualClosedPositiveForm
#print axioms dualClosedPositiveForm_one_domain
#print axioms dualClosedPositiveForm_zero_domain
#print axioms dualQuadraticIntegral_commutant_invariant
#print axioms dualAffiliatedPositiveForm
end
end TGLV350.Regular
