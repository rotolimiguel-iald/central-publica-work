import Mathlib.Logic.Function.Iterate

/-!
# A reading-relative rule contract

The operator's short inscriptions, verbatim:

"Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)"
"A regra não deve nada, a não ser a figura da verdade"
"Exclusão irrestrita seria alcançar o zero absoluto, e isso não é possível. Portanto, a exclusão, ela é no tetelestai. Ela é segundo a mesma regra do acoplamento não minimal."

[INPUT/ONTO] The choice to represent admissibility by `reading y = target`
is an explicit mathematical interpretation. The theorems below prove its
logical consequences, not the universal truth or physical realization of the
chosen reading or target. A reading need not identify distinct objects.
Idempotence alone does not establish agreement with a target.

These implications are elementary logical consequences, not a discovery of
ontological truth. The main delivery pins the original inscriptions separately.
-/
set_option autoImplicit false
universe u v

namespace TGLExt.RuleTruthContract

/-- Explicit representation of admissibility relative to a reading and target. -/
def Admissible {Y : Type u} {O : Type v} (reading : Y → O) (target : O) (y : Y) : Prop :=
  reading y = target

def SoundRule {Y : Type u} {O : Type v} (reading : Y → O) (target : O)
    (C : Y → Prop) : Prop := ∀ y : Y, C y → reading y = target

def CompleteRule {Y : Type u} {O : Type v} (reading : Y → O) (target : O)
    (C : Y → Prop) : Prop := ∀ y : Y, reading y = target → C y

theorem incompatible_not_admissible {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (y : Y) (h : reading y ≠ target) :
    ¬ Admissible reading target y := h

theorem sound_subset_admissible {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (C : Y → Prop)
    (hs : SoundRule reading target C) :
    ∀ y : Y, C y → Admissible reading target y := hs

theorem admissible_is_sound {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) :
    SoundRule reading target (Admissible reading target) := fun _ h => h

theorem admissible_is_complete {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) :
    CompleteRule reading target (Admissible reading target) := fun _ h => h

theorem sound_complete_iff {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (C : Y → Prop)
    (hs : SoundRule reading target C) (hc : CompleteRule reading target C) (y : Y) :
    C y ↔ Admissible reading target y := ⟨hs y, hc y⟩

theorem sound_complete_eq_admissible {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (C : Y → Prop)
    (hs : SoundRule reading target C) (hc : CompleteRule reading target C) :
    C = Admissible reading target := by
  funext y
  exact propext (sound_complete_iff reading target C hs hc y)

theorem sound_complete_unique {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (C D : Y → Prop)
    (hCs : SoundRule reading target C) (hCc : CompleteRule reading target C)
    (hDs : SoundRule reading target D) (hDc : CompleteRule reading target D) : C = D :=
  (sound_complete_eq_admissible reading target C hCs hCc).trans
    (sound_complete_eq_admissible reading target D hDs hDc).symm

/-- A selection is required to preserve the chosen reading; this is not inferred
from idempotence. The image is its fixed locus, as proved below. -/
structure ReadingRetraction {Y : Type u} {O : Type v} (reading : Y → O) (R : Y → Y) : Prop where
  idempotent : ∀ y : Y, R (R y) = R y
  preserves_reading : ∀ y : Y, reading (R y) = reading y

theorem admissible_retract_iff {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (R : Y → Y)
    (hR : ReadingRetraction reading R) (y : Y) :
    Admissible reading target (R y) ↔ Admissible reading target y := by
  unfold Admissible
  rw [hR.preserves_reading y]

theorem reading_iterate {Y : Type u} {O : Type v}
    (reading : Y → O) (R : Y → Y) (hR : ReadingRetraction reading R)
    (n : ℕ) (y : Y) : reading ((R^[n]) y) = reading y := by
  induction n generalizing y with
  | zero => rfl
  | succ n ih =>
    rw [Function.iterate_succ_apply, ih, hR.preserves_reading]

theorem admissible_iterate_iff {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (R : Y → Y)
    (hR : ReadingRetraction reading R) (n : ℕ) (y : Y) :
    Admissible reading target ((R^[n]) y) ↔ Admissible reading target y := by
  unfold Admissible
  rw [reading_iterate reading R hR n y]

theorem retract_iterate {Y : Type u} {O : Type v}
    (reading : Y → O) (R : Y → Y) (hR : ReadingRetraction reading R)
    (n : ℕ) (y : Y) : (R^[n + 1]) y = R y := by
  induction n generalizing y with
  | zero => rfl
  | succ n ih =>
    rw [Function.iterate_succ_apply, ih, hR.idempotent]

theorem fixed_iff_in_range {Y : Type u} {O : Type v}
    (reading : Y → O) (R : Y → Y) (hR : ReadingRetraction reading R) (y : Y) :
    R y = y ↔ ∃ x : Y, R x = y := by
  constructor
  · intro h
    exact ⟨y, h⟩
  · intro h
    cases h with
    | intro x hx =>
      subst y
      exact hR.idempotent x

/-- The kernel pair is equality of readings, not necessarily equality of objects. -/
def SameReading {Y : Type u} {O : Type v} (reading : Y → O) (y z : Y) : Prop :=
  reading y = reading z

theorem same_reading_admissible_iff {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (y z : Y) (h : SameReading reading y z) :
    Admissible reading target y ↔ Admissible reading target z := by
  unfold Admissible
  rw [h]

theorem admissible_iff_eq_of_injective {Y : Type u} {O : Type v}
    (reading : Y → O) (target : O) (hinj : Function.Injective reading)
    (y0 : Y) (h0 : reading y0 = target) (y : Y) :
    Admissible reading target y ↔ y = y0 := by
  constructor
  · intro hy
    exact hinj (hy.trans h0.symm)
  · intro hy
    cases hy
    exact h0

/-- Global injectivity plus reading preservation already forces the selection
to be the identity. Nontrivial normalizations require a weaker reading or a
restriction to the fixed locus. No idempotence hypothesis is needed here. -/
theorem reading_injective_preserving_eq_id {Y : Type u} {O : Type v}
    (reading : Y → O) (R : Y → Y) (hinj : Function.Injective reading)
    (hpres : ∀ y : Y, reading (R y) = reading y) : R = id := by
  funext y
  exact hinj (hpres y)

/-- Inhabited countermodel: the reading forgets the second Boolean coordinate. -/
def firstReading (y : Bool × Bool) : Bool := y.1
def firstRetraction (y : Bool × Bool) : Bool × Bool := (y.1, false)

theorem firstRetraction_contract : ReadingRetraction firstReading firstRetraction where
  idempotent := fun _ => rfl
  preserves_reading := fun _ => rfl

theorem firstRetraction_nonvacuous :
    Admissible firstReading true (true, false) ∧
    ¬ Admissible firstReading true (false, false) := by
  simp [Admissible, firstReading]

theorem same_reading_not_equal :
    SameReading firstReading (true, false) (true, true) ∧
    (true, false) ≠ ((true, true) : Bool × Bool) := by
  simp [SameReading, firstReading]

theorem same_reading_does_not_force_equality :
    ¬ (∀ y z : Bool × Bool, SameReading firstReading y z → y = z) := by
  intro h
  exact same_reading_not_equal.2 (h (true, false) (true, true) same_reading_not_equal.1)

/-- An idempotent constant reading that misses the independently fixed target. -/
def wrongConstant (_ : Bool) : Bool := false

theorem wrongConstant_idempotent (y : Bool) :
    wrongConstant (wrongConstant y) = wrongConstant y := rfl

theorem wrongConstant_never_admissible (y : Bool) :
    ¬ Admissible wrongConstant true y := by
  simp [Admissible, wrongConstant]

theorem idempotence_does_not_force_target :
    (∀ y : Bool, wrongConstant (wrongConstant y) = wrongConstant y) ∧
    (∀ y : Bool, ¬ Admissible wrongConstant true y) :=
  ⟨wrongConstant_idempotent, wrongConstant_never_admissible⟩

end TGLExt.RuleTruthContract

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    match ci with
    | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
    | _ => pure ()
