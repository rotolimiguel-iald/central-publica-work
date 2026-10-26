import TGLExt.V350DualClosedForm

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open scoped ENNReal NNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

@[ext] theorem ClosedPositiveForm.ext (Q R : ClosedPositiveForm H)
    (h : ∀ v, Q.value v = R.value v) : Q = R := by
  have he : Q.value = R.value := funext h
  cases Q
  cases R
  cases he
  rfl

def ClosedPositiveForm.zeroForm : ClosedPositiveForm H where
  value := fun _ => 0
  map_zero := rfl
  map_smul := by intros; simp
  parallelogram := by intros; simp
  lowerSemicontinuous := lowerSemicontinuous_const

def ClosedPositiveForm.addForm (Q R : ClosedPositiveForm H) : ClosedPositiveForm H where
  value := fun v => Q.value v + R.value v
  map_zero := by rw [Q.map_zero,R.map_zero,add_zero]
  map_smul := by intro c v; rw [Q.map_smul,R.map_smul,mul_add]
  parallelogram := by
    intro v w
    calc
      _ = (Q.value (v+w) + Q.value (v-w)) + (R.value (v+w) + R.value (v-w)) := by ac_rfl
      _ = _ := by rw [Q.parallelogram,R.parallelogram]; ring
  lowerSemicontinuous := Q.lowerSemicontinuous.add R.lowerSemicontinuous

/-- Only finite nonnegative scalars are used; zero times infinity is handled
by ENNReal multiplication, without taking toReal. -/
def ClosedPositiveForm.scaleForm (r : ℝ≥0) (Q : ClosedPositiveForm H) : ClosedPositiveForm H where
  value := fun v => (r : ℝ≥0∞) * Q.value v
  map_zero := by rw [Q.map_zero,mul_zero]
  map_smul := by intro c v; rw [Q.map_smul]; ac_rfl
  parallelogram := by intro v w; rw [← mul_add,Q.parallelogram]; ring
  lowerSemicontinuous :=
    (ENNReal.continuous_const_mul ENNReal.coe_ne_top).comp_lowerSemicontinuous
      Q.lowerSemicontinuous (fun _ _ h => mul_le_mul_right h (r : ℝ≥0∞))

def ClosedPositiveForm.precompose (Q : ClosedPositiveForm H) (B : H →L[ℂ] H) :
    ClosedPositiveForm H where
  value := fun v => Q.value (B v)
  map_zero := by rw [_root_.map_zero,Q.map_zero]
  map_smul := by intro c v; rw [_root_.map_smul,Q.map_smul]
  parallelogram := by intro v w; rw [map_add,map_sub,Q.parallelogram]
  lowerSemicontinuous := Q.lowerSemicontinuous.comp B.continuous

@[ext] theorem AffiliatedPositiveForm.ext {N : VonNeumannAlgebra H}
    (Q R : AffiliatedPositiveForm N) (h : ∀ v, Q.value v = R.value v) : Q = R := by
  have he : Q.toClosedPositiveForm = R.toClosedPositiveForm := ClosedPositiveForm.ext _ _ h
  cases Q
  cases R
  cases he
  rfl

instance (N : VonNeumannAlgebra H) : PartialOrder (AffiliatedPositiveForm N) :=
  PartialOrder.lift (fun Q => Q.value) (fun _ _ h => AffiliatedPositiveForm.ext _ _ (congrFun h))

theorem AffiliatedPositiveForm.le_iff {N : VonNeumannAlgebra H}
    (Q R : AffiliatedPositiveForm N) : Q ≤ R ↔ ∀ v, Q.value v ≤ R.value v := Iff.rfl

def AffiliatedPositiveForm.zeroForm (N : VonNeumannAlgebra H) : AffiliatedPositiveForm N where
  toClosedPositiveForm := ClosedPositiveForm.zeroForm
  unitary_commutant_invariant := by intros; rfl

def AffiliatedPositiveForm.addForm {N : VonNeumannAlgebra H}
    (Q R : AffiliatedPositiveForm N) : AffiliatedPositiveForm N where
  toClosedPositiveForm := Q.toClosedPositiveForm.addForm R.toClosedPositiveForm
  unitary_commutant_invariant := by
    intro U hU v
    change Q.value (U.val v) + R.value (U.val v) = Q.value v + R.value v
    rw [Q.unitary_commutant_invariant U hU,R.unitary_commutant_invariant U hU]

def AffiliatedPositiveForm.scaleForm {N : VonNeumannAlgebra H}
    (r : ℝ≥0) (Q : AffiliatedPositiveForm N) : AffiliatedPositiveForm N where
  toClosedPositiveForm := Q.toClosedPositiveForm.scaleForm r
  unitary_commutant_invariant := by
    intro U hU v
    change (r : ℝ≥0∞) * Q.value (U.val v) = (r : ℝ≥0∞) * Q.value v
    rw [Q.unitary_commutant_invariant U hU]

def AffiliatedPositiveForm.conjugate {N : VonNeumannAlgebra H}
    (Q : AffiliatedPositiveForm N) (B : H →L[ℂ] H) (hB : B ∈ N) : AffiliatedPositiveForm N where
  toClosedPositiveForm := Q.toClosedPositiveForm.precompose B
  unitary_commutant_invariant := by
    intro U hU v
    change Q.value (B (U.val v)) = Q.value (B v)
    have he : B (U.val v) = U.val (B v) :=
      (congrArg (fun T : H →L[ℂ] H => T v) (hU B hB)).symm
    rw [he,Q.unitary_commutant_invariant U hU]

theorem AffiliatedPositiveForm.add_comm {N : VonNeumannAlgebra H}
    (Q R : AffiliatedPositiveForm N) : Q.addForm R = R.addForm Q := by
  apply AffiliatedPositiveForm.ext
  intro v
  exact _root_.add_comm _ _

theorem AffiliatedPositiveForm.add_assoc {N : VonNeumannAlgebra H}
    (Q R S : AffiliatedPositiveForm N) : (Q.addForm R).addForm S = Q.addForm (R.addForm S) := by
  apply AffiliatedPositiveForm.ext
  intro v
  exact _root_.add_assoc _ _ _

theorem AffiliatedPositiveForm.zero_add {N : VonNeumannAlgebra H}
    (Q : AffiliatedPositiveForm N) : (AffiliatedPositiveForm.zeroForm N).addForm Q = Q := by
  apply AffiliatedPositiveForm.ext
  intro v
  exact _root_.zero_add _

theorem AffiliatedPositiveForm.scale_laws {N : VonNeumannAlgebra H}
    (r s : ℝ≥0) (Q R : AffiliatedPositiveForm N) :
    Q.scaleForm 1 = Q ∧ Q.scaleForm 0 = AffiliatedPositiveForm.zeroForm N ∧
    (Q.scaleForm s).scaleForm r = Q.scaleForm (r*s) ∧
    (Q.addForm R).scaleForm r = (Q.scaleForm r).addForm (R.scaleForm r) ∧
    Q.scaleForm (r+s) = (Q.scaleForm r).addForm (Q.scaleForm s) := by
  refine ⟨?_,?_,?_,?_,?_⟩ <;> apply AffiliatedPositiveForm.ext <;> intro v
  · exact one_mul _
  · exact zero_mul _
  · change (r : ℝ≥0∞)*((s : ℝ≥0∞)*Q.value v) = ((r*s : ℝ≥0) : ℝ≥0∞)*Q.value v
    rw [ENNReal.coe_mul,mul_assoc]
  · exact mul_add _ _ _
  · change ((r+s : ℝ≥0) : ℝ≥0∞)*Q.value v =
      (r : ℝ≥0∞)*Q.value v + (s : ℝ≥0∞)*Q.value v
    rw [ENNReal.coe_add,add_mul]

theorem AffiliatedPositiveForm.zero_le {N : VonNeumannAlgebra H}
    (Q : AffiliatedPositiveForm N) : AffiliatedPositiveForm.zeroForm N ≤ Q :=
  fun _ => bot_le

theorem AffiliatedPositiveForm.add_mono {N : VonNeumannAlgebra H}
    (Q R S T : AffiliatedPositiveForm N) (hQR : Q ≤ R) (hST : S ≤ T) :
    Q.addForm S ≤ R.addForm T :=
  fun v => add_le_add (hQR v) (hST v)

theorem AffiliatedPositiveForm.scale_mono {N : VonNeumannAlgebra H}
    (r : ℝ≥0) (Q R : AffiliatedPositiveForm N) (hQR : Q ≤ R) :
    Q.scaleForm r ≤ R.scaleForm r :=
  fun v => mul_le_mul_right (hQR v) (r : ℝ≥0∞)

#print axioms ClosedPositiveForm.ext
#print axioms ClosedPositiveForm.zeroForm
#print axioms ClosedPositiveForm.addForm
#print axioms ClosedPositiveForm.scaleForm
#print axioms ClosedPositiveForm.precompose
#print axioms AffiliatedPositiveForm.ext
#print axioms AffiliatedPositiveForm.le_iff
#print axioms AffiliatedPositiveForm.zeroForm
#print axioms AffiliatedPositiveForm.addForm
#print axioms AffiliatedPositiveForm.scaleForm
#print axioms AffiliatedPositiveForm.conjugate
#print axioms AffiliatedPositiveForm.add_comm
#print axioms AffiliatedPositiveForm.add_assoc
#print axioms AffiliatedPositiveForm.zero_add
#print axioms AffiliatedPositiveForm.scale_laws
#print axioms AffiliatedPositiveForm.zero_le
#print axioms AffiliatedPositiveForm.add_mono
#print axioms AffiliatedPositiveForm.scale_mono
end
end TGLV350.Regular
