import RuleTruthContract
import TGLExt.TheJudgedThing
import TGLExt.TheNonMinimalCoupling
import TGLExt.TheGeometricCostOfAbsoluteZero
import TGLExt.TheLedgerOfCharges
import Mathlib.Analysis.SpecificLimits.Basic

/-!
## Operator inscriptions — verbatim, original bytes pinned separately

OPERADOR_REGRA_NEGATIVIDADE_VERBATIM_20261014.txt
SHA256 acaeb291cb41fa4e97be7e08aced443bfc4dec0543e6cf9a2715bd328e0273a8

Agora eu consigo cunhar a última pedra que falta, que é a definição de regra. O que é regra? Regra é igual a direito, e isso parece uma contradição, porque direito parece ser uma aquisição. Não é, é uma negação. Regra é negar tudo aquilo que não pode ser, e isso é criar limite assintótico. Portanto, direito não é uma aquisição no sentido de uma autoafirmação como condição de suporte, mas é uma aquisição no sentido de haver um espaço possível de inscrição, de possibilidade, e isso só se dá pela delimitação, que é negativa, não positiva. Portanto o direito é negativo e não positivo. Cria-se aqui o domínio da negatividade jurídica.

OPERADOR_TETELESTAI_VERBATIM.txt
SHA256 c37fccba3b7f1c89e9930e11771b3ab5644da8e9a3d69a8419ef155970643484

Exclusão irrestrita seria alcançar o zero absoluto, e isso não é possível. Portanto, a exclusão, ela é no tetelestai. Ela é segundo a mesma regra do acoplamento não minimal.

OPERADOR_REGRA_SATISFACAO_VERBATIM.txt
SHA256 426b8ab01b5edf316b7ff5c93ba0d61c36729070c96897cf5b4a0bb6544047f8

Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)

OPERADOR_FIGURA_DA_VERDADE_VERBATIM.txt
SHA256 7ce148ad0d8149172cdae01df620641037f3829bc92196b263a78c8396bb41ae

A regra não deve nada, a não ser a figura da verdade

These inscriptions are ONTO; the formal interpretation and its assumptions are explicit below.
-/

set_option autoImplicit false

/-!
# The rule and the figure of truth — provisional candidate, F1.REGRA.P1

Formal model: the result to be compared literally with the target is a normalized
result in Fix(normalize). Raw finite-time trajectories are NOT declared equal to
that target. The identification with payment, legal truth, or physical realization
is the operator's ONTO reading. No theorem below proves universal philosophical
truth or a physical erasure law. The half-nat factor is reused from the existing
kernel; it is not identified with beta_TGL.

RuleTruthContract supplies the logical characterization for FIXED reading/target.
The concrete model below supplies a nonzero inhabitant, a genuine transformation,
an asymptotic trajectory, and rejected controls. It uses the real decay variable
of the face; no limit is requested of an angular orbit.
-/

noncomputable section
open Filter Topology

namespace TGLExt.RuleSatisfactionFace

abbrev Face := ℝ × ℝ

def normalize (x : Face) : Face := (x.1, 0)
def reading (x : Face) : ℝ := x.1
def target : Face := (1, 0)
def initial : Face := (1, 1)
def decay : ℝ := Real.exp (-(1 / 2) : ℝ)
def evolve (f : ℝ) (x : Face) : Face := (x.1, f * x.2)
def trajectory (f : ℝ) (n : ℕ) (x : Face) : Face := (x.1, f ^ n * x.2)

/-- The mathematical comparison is literal equality in the result's type. -/
def Satisfies (result : Face) : Prop := result = target

/-- The output type explicitly carries the fixed-space condition. -/
abbrev Inscription := {x : Face // normalize x = x}

def inscribe (x : Face) : Inscription := ⟨normalize x, rfl⟩
def dueObject : Inscription := ⟨target, rfl⟩

theorem normalization_idempotent (x : Face) :
    normalize (normalize x) = normalize x := rfl

theorem normalization_preserves_reading (x : Face) :
    reading (normalize x) = reading x := rfl

theorem normalize_res_judicata : TGLExt.ResJudicata normalize :=
  normalization_idempotent

/-- This reuses the old Tetelestai lemma; it does not rebuild the induction. -/
theorem repeat_reading_adds_nothing (x : Face) (n : ℕ) :
    normalize^[n + 1] x = normalize x :=
  TGLExt.res_judicata_is_terminal normalize normalize_res_judicata x n

theorem inscription_reading_injective :
    Function.Injective (fun x : Inscription => reading x.val) := by
  intro x y h
  apply Subtype.ext
  calc
    x.val = normalize x.val := x.property.symm
    _ = normalize y.val := by
      exact Prod.ext h rfl
    _ = y.val := y.property

theorem inscription_admissible_iff_due (z : Inscription) :
    RuleTruthContract.Admissible (fun x : Inscription => reading x.val) 1 z ↔
      z = dueObject :=
  RuleTruthContract.admissible_iff_eq_of_injective
    (fun x : Inscription => reading x.val) 1 inscription_reading_injective
    dueObject rfl z

/-- Uniqueness for the fixed object and faithful reading on the fixed space.
    Soundness forbids false satisfactions; completeness forbids extra exclusions.
    Both conditions are explicit hypotheses, not consequences of the name. -/
theorem unique_rule_on_inscriptions (C : Inscription → Prop)
    (hs : RuleTruthContract.SoundRule (fun x : Inscription => reading x.val) 1 C)
    (hc : RuleTruthContract.CompleteRule (fun x : Inscription => reading x.val) 1 C) :
    C = (fun z => z = dueObject) := by
  calc
    C = RuleTruthContract.Admissible (fun x : Inscription => reading x.val) 1 :=
      RuleTruthContract.sound_complete_eq_admissible _ _ C hs hc
    _ = (fun z => z = dueObject) := by
      funext z
      exact propext (inscription_admissible_iff_due z)

theorem normalization_is_reading_retraction :
    RuleTruthContract.ReadingRetraction reading normalize :=
  ⟨normalization_idempotent, normalization_preserves_reading⟩

theorem reading_admissibility_is_preserved (x : Face) :
    RuleTruthContract.Admissible reading 1 (normalize x) ↔
      RuleTruthContract.Admissible reading 1 x :=
  RuleTruthContract.admissible_retract_iff reading 1 normalize
    normalization_is_reading_retraction x

theorem inscribe_eq_due_iff (x : Face) :
    inscribe x = dueObject ↔ reading x = 1 := by
  constructor
  · intro h
    exact congrArg (fun z : Inscription => reading z.val) h
  · intro h
    apply Subtype.ext
    exact Prod.ext h rfl

theorem normalized_satisfies_iff (x : Face) :
    Satisfies (normalize x) ↔ reading x = 1 := by
  constructor
  · intro h
    exact congrArg Prod.fst h
  · intro h
    exact Prod.ext h rfl

theorem normalize_after_evolve (f : ℝ) (x : Face) :
    normalize (evolve f x) = normalize x := rfl

theorem evolve_after_normalize (f : ℝ) (x : Face) :
    evolve f (normalize x) = normalize x := by
  simp [evolve, normalize]

/-- A genuine commuting square of the model; no homonym supplies this equality. -/
theorem evolution_normalization_commute (f : ℝ) :
    Function.Commute (evolve f) normalize := by
  intro x
  exact evolve_after_normalize f x

theorem evolve_iterate_eq_trajectory (f : ℝ) (n : ℕ) (x : Face) :
    (evolve f)^[n] x = trajectory f n x := by
  induction n with
  | zero => simp [trajectory]
  | succ n ih =>
    rw [Function.iterate_succ_apply', ih]
    apply Prod.ext
    · rfl
    · simp only [evolve, trajectory, pow_succ]
      ring

theorem normalize_trajectory (f : ℝ) (n : ℕ) (x : Face) :
    normalize (trajectory f n x) = normalize x := rfl

theorem trajectory_tends_to_inscription (f : ℝ) (h0 : 0 ≤ f) (h1 : f < 1)
    (x : Face) :
    Tendsto (fun n : ℕ => trajectory f n x) atTop (𝓝 (normalize x)) := by
  have hp : Tendsto (fun n : ℕ => f ^ n) atTop (𝓝 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one h0 h1
  simpa only [trajectory, normalize, zero_mul] using
    (tendsto_const_nhds.prodMk_nhds (hp.mul_const x.2))

theorem decay_strictly_interior : 0 < decay ∧ decay < 1 :=
  TGLExt.the_half_nat_gives_a_strictly_interior_factor

/-- The scalar balance is conditional arithmetic; it is not an energy measurement. -/
theorem decay_tetelestai_balance :
    0 < decay ∧ 0 < 1 - decay ∧ decay + (1 - decay) = 1 :=
  TGLExt.tetelestai_ledger decay decay_strictly_interior.1 decay_strictly_interior.2

theorem concrete_trajectory_converges :
    Tendsto (fun n : ℕ => trajectory decay n initial) atTop (𝓝 target) :=
  trajectory_tends_to_inscription decay decay_strictly_interior.1.le
    decay_strictly_interior.2 initial

theorem normalized_operation_satisfies (n : ℕ) :
    Satisfies (normalize ((evolve decay)^[n] initial)) := by
  rw [evolve_iterate_eq_trajectory]
  rfl

theorem typed_operation_satisfies (n : ℕ) :
    inscribe ((evolve decay)^[n] initial) = dueObject := by
  rw [evolve_iterate_eq_trajectory]
  rfl

theorem target_is_nonzero : target ≠ (0 : Face) := by
  intro h
  have hfst := congrArg Prod.fst h
  norm_num [target] at hfst

theorem normalization_is_effective : normalize initial ≠ initial := by
  intro h
  have hsnd := congrArg Prod.snd h
  norm_num [normalize, initial] at hsnd

theorem evolution_is_effective : evolve decay initial ≠ initial := by
  intro h
  have hsnd := congrArg Prod.snd h
  simp only [evolve, initial, mul_one] at hsnd
  exact ne_of_lt decay_strictly_interior.2 hsnd

/-- At no finite time is the raw trajectory certified as the literal target. -/
theorem finite_raw_trajectory_does_not_satisfy (n : ℕ) :
    ¬ Satisfies (trajectory decay n initial) := by
  intro h
  have hsnd := congrArg Prod.snd h
  simp only [trajectory, initial, target, mul_one] at hsnd
  exact (ne_of_gt (pow_pos decay_strictly_interior.1 n)) hsnd

theorem wrong_output_rejected : ¬ Satisfies (normalize (0, 1)) := by
  intro h
  have hfst := congrArg Prod.fst h
  norm_num [normalize, target] at hfst

/-- Unrestricted normalization is not enough: an accepted and a rejected input. -/
theorem the_concrete_contract_is_inhabited_and_discriminating :
    (∃ x : Face, Satisfies (normalize x)) ∧
    (∃ x : Face, ¬ Satisfies (normalize x)) ∧ target ≠ 0 := by
  exact ⟨⟨initial, rfl⟩, ⟨(0, 1), wrong_output_rejected⟩, target_is_nonzero⟩

/-- A strict mismatch remains possible while the comparison rule is unchanged. -/
theorem the_rule_does_not_guarantee_every_operation :
    (∃ op : Face → Face, ∀ x, Satisfies (op x)) ∧
    (∃ op : Face → Face, ∀ x, ¬ Satisfies (op x)) := by
  constructor
  · exact ⟨fun _ => target, fun _ => rfl⟩
  · exact ⟨fun _ => normalize (0, 1), fun _ => wrong_output_rejected⟩

def leftFace : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, 0]
def rightFace : Matrix (Fin 2) (Fin 2) ℂ := !![0, 0; 0, 1]
def complexCoordinates (x : Face) : Fin 2 → ℂ := ![(x.1 : ℂ), (x.2 : ℂ)]

/-- The projection used above is explicitly linked to the two-face matrix;
    this is a typed bridge, rather than matching two names. -/
theorem normalization_is_left_face (x : Face) :
    leftFace.mulVec (complexCoordinates x) = complexCoordinates (normalize x) := by
  funext i
  fin_cases i <;> simp [leftFace, complexCoordinates, normalize,
    Matrix.mulVec, dotProduct, Fin.sum_univ_two]

theorem concrete_faces_split : leftFace + rightFace = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [leftFace, rightFace, Matrix.one_apply]

theorem concrete_faces_orthogonal : leftFace * rightFace = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [leftFace, rightFace, Matrix.mul_apply, Fin.sum_univ_two]

theorem left_face_idempotent : leftFace * leftFace = leftFace := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [leftFace, Matrix.mul_apply, Fin.sum_univ_two]

theorem both_concrete_faces_nonzero : leftFace ≠ 0 ∧ rightFace ≠ 0 := by
  constructor
  · intro h
    have he := congrFun (congrFun h 0) 0
    norm_num [leftFace] at he
  · intro h
    have he := congrFun (congrFun h 1) 1
    norm_num [rightFace] at he

theorem nonminimal_split_applies_to_this_reading :
    leftFace * 1 = leftFace ∧ leftFace ≠ 1 ∧ leftFace ≠ 0 ∧ rightFace ≠ 0 := by
  have h := TGLExt.split_forbids_minimality (1 : Matrix (Fin 2) (Fin 2) ℂ)
    leftFace rightFace concrete_faces_split concrete_faces_orthogonal
    left_face_idempotent both_concrete_faces_nonzero.2
  exact ⟨h.1, h.2, both_concrete_faces_nonzero.1, both_concrete_faces_nonzero.2⟩

/-- No new minimality theorem is inferred from a zero subprojection. Both faces
    are explicitly nonzero in the existing finite witness. -/
theorem reuse_nontrivial_two_faces :
    ∃ e f g : Matrix (Fin 2) (Fin 2) ℂ,
      f + g = e ∧ f * g = 0 ∧ f * f = f ∧ g * g = g ∧
      f ≠ 0 ∧ g ≠ 0 ∧ f ≠ e :=
  TGLExt.the_split_is_inhabited

/-- Documentary bridge to the existing ledger: this is the same definitional
    independence already stated in that module, not an extra physical result. -/
theorem reuse_rule_independent_of_ledger
    (L L' : TGLExt.TheLedgerOfCharges.Ledger)
    (a : ℝ) (h0 : 0 < a) (h1 : a < Real.exp (-(1 / 2))) :
    TGLExt.TheLedgerOfCharges.ruleGiven L a h0 h1 =
      TGLExt.TheLedgerOfCharges.ruleGiven L' a h0 h1 :=
  TGLExt.TheLedgerOfCharges.the_rule_is_constant_in_the_ledger L L' a h0 h1

/-- Main concrete result: an actual nonzero target, a nontrivial operation,
    convergence, exact normalized satisfaction, and rejection of premature raw
    satisfaction. These conclusions have different types and are not conflated. -/
theorem the_rule_and_the_figure_of_truth :
    target ≠ 0 ∧ normalize initial ≠ initial ∧ evolve decay initial ≠ initial ∧
    (∀ n : ℕ, inscribe ((evolve decay)^[n] initial) = dueObject) ∧
    Tendsto (fun n : ℕ => trajectory decay n initial) atTop (𝓝 target) ∧
    (∀ n : ℕ, ¬ Satisfies (trajectory decay n initial)) := by
  exact ⟨target_is_nonzero, normalization_is_effective, evolution_is_effective,
    typed_operation_satisfies, concrete_trajectory_converges,
    finite_raw_trajectory_does_not_satisfy⟩

#print axioms normalization_idempotent
#print axioms normalization_preserves_reading
#print axioms normalize_res_judicata
#print axioms repeat_reading_adds_nothing
#print axioms inscription_reading_injective
#print axioms inscription_admissible_iff_due
#print axioms unique_rule_on_inscriptions
#print axioms normalization_is_reading_retraction
#print axioms reading_admissibility_is_preserved
#print axioms inscribe_eq_due_iff
#print axioms normalized_satisfies_iff
#print axioms normalize_after_evolve
#print axioms evolve_after_normalize
#print axioms evolution_normalization_commute
#print axioms evolve_iterate_eq_trajectory
#print axioms normalize_trajectory
#print axioms trajectory_tends_to_inscription
#print axioms decay_strictly_interior
#print axioms decay_tetelestai_balance
#print axioms concrete_trajectory_converges
#print axioms normalized_operation_satisfies
#print axioms typed_operation_satisfies
#print axioms target_is_nonzero
#print axioms normalization_is_effective
#print axioms evolution_is_effective
#print axioms finite_raw_trajectory_does_not_satisfy
#print axioms wrong_output_rejected
#print axioms the_concrete_contract_is_inhabited_and_discriminating
#print axioms the_rule_does_not_guarantee_every_operation
#print axioms normalization_is_left_face
#print axioms concrete_faces_split
#print axioms concrete_faces_orthogonal
#print axioms left_face_idempotent
#print axioms both_concrete_faces_nonzero
#print axioms nonminimal_split_applies_to_this_reading
#print axioms reuse_nontrivial_two_faces
#print axioms reuse_rule_independent_of_ledger
#print axioms the_rule_and_the_figure_of_truth

end TGLExt.RuleSatisfactionFace
