import Lean
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.Data.Int.Order.Units
import Mathlib.Tactic

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.PolarPeriod016

/-- Equality on the circle is exactly equality modulo P*Z. This is the
descent-and-injectivity criterion for the angular quotient, not a definition
of the value of the period. -/
def AngularQuotientFaithful (kappa period : ℝ) : Prop :=
  ∀ t u : ℝ, Circle.exp (kappa*t) = Circle.exp (kappa*u) ↔
    ∃ n : ℤ, t = u + (n : ℝ)*period

theorem faithful_period_forces_one_turn {kappa period : ℝ} (hk : kappa ≠ 0)
    (h : AngularQuotientFaithful kappa period) :
    kappa*period = 2*Real.pi ∨ kappa*period = -(2*Real.pi) := by
  have hp : Circle.exp (kappa*period) = 1 := by
    have hh := (h period 0).mpr ⟨1, by simp⟩
    simpa using hh
  obtain ⟨n, hn⟩ := Circle.exp_eq_one.mp hp
  have hr : Circle.exp (kappa*(2*Real.pi/kappa)) = Circle.exp (kappa*0) := by
    rw [mul_div_cancel₀ _ hk]
    simp
  obtain ⟨m, hm⟩ := (h (2*Real.pi/kappa) 0).mp hr
  have hm' : 2*Real.pi = (m : ℝ)*(kappa*period) := by
    have hh := congrArg (fun x : ℝ => kappa*x) hm
    rw [mul_div_cancel₀ _ hk] at hh
    calc
      2*Real.pi = kappa*(0+(m : ℝ)*period) := hh
      _ = (m : ℝ)*(kappa*period) := by ring
  have hmnR : (m : ℝ)*(n : ℝ) = 1 := by
    apply mul_right_cancel₀ (show (2*Real.pi : ℝ) ≠ 0 by positivity)
    calc
      (m : ℝ)*(n : ℝ)*(2*Real.pi) = (m : ℝ)*(kappa*period) := by rw [hn]; ring
      _ = 1*(2*Real.pi) := by simpa using hm'.symm
  have hmn : m*n = 1 := by exact_mod_cast hmnR
  have hnunit : IsUnit n := ⟨⟨n,m,by simpa [mul_comm] using hmn,hmn⟩,rfl⟩
  have hnabs : |n| = 1 := Int.isUnit_iff_abs_eq.mp hnunit
  have hnchoice : n = 1 ∨ n = -1 := by
    rcases le_total 0 n with hpos | hneg
    · left; simpa [abs_of_nonneg hpos] using hnabs
    · right
      have hh : -n = 1 := by simpa [abs_of_nonpos hneg] using hnabs
      omega
  rcases hnchoice with hn1 | hnm1
  · left; simpa [hn1] using hn
  · right; simpa [hnm1] using hn

theorem one_turn_gives_faithful_period {kappa period : ℝ} (hk : kappa ≠ 0)
    (hp : kappa*period = 2*Real.pi ∨ kappa*period = -(2*Real.pi)) :
    AngularQuotientFaithful kappa period := by
  intro t u
  rcases hp with hp | hp
  · constructor
    · intro hh
      obtain ⟨n, hn⟩ := Circle.exp_eq_exp.mp hh
      refine ⟨n, ?_⟩
      apply mul_left_cancel₀ hk
      calc
        kappa*t = kappa*u + (n : ℝ)*(2*Real.pi) := hn
        _ = kappa*(u+(n : ℝ)*period) := by rw [← hp]; ring
    · rintro ⟨n, hn⟩
      apply Circle.exp_eq_exp.mpr
      refine ⟨n, ?_⟩
      rw [hn, ← hp]
      ring
  · constructor
    · intro hh
      obtain ⟨n, hn⟩ := Circle.exp_eq_exp.mp hh
      refine ⟨-n, ?_⟩
      apply mul_left_cancel₀ hk
      calc
        kappa*t = kappa*u + (n : ℝ)*(2*Real.pi) := hn
        _ = kappa*(u+((-n : ℤ) : ℝ)*period) := by
          push_cast
          have hh := congrArg (fun x : ℝ => (n : ℝ)*x) hp
          nlinarith
    · rintro ⟨n, hn⟩
      apply Circle.exp_eq_exp.mpr
      refine ⟨-n, ?_⟩
      rw [hn]
      push_cast
      have hh := congrArg (fun x : ℝ => (n : ℝ)*x) hp
      nlinarith

theorem faithful_period_iff {kappa period : ℝ} (hk : kappa ≠ 0) :
    AngularQuotientFaithful kappa period ↔
      kappa*period = 2*Real.pi ∨ kappa*period = -(2*Real.pi) :=
  ⟨faithful_period_forces_one_turn hk, one_turn_gives_faithful_period hk⟩

theorem positive_faithful_period {kappa period : ℝ} (hk : 0 < kappa)
    (hp : 0 < period) (h : AngularQuotientFaithful kappa period) :
    period = 2*Real.pi/kappa := by
  rcases faithful_period_forces_one_turn (ne_of_gt hk) h with hh | hh
  · apply (eq_div_iff (ne_of_gt hk)).mpr
    simpa [mul_comm] using hh
  · have := mul_pos hk hp
    have := Real.pi_pos
    linarith

theorem reciprocal_temperature {kappa period : ℝ} (hk : 0 < kappa)
    (hp : 0 < period) (h : AngularQuotientFaithful kappa period) :
    1/period = kappa/(2*Real.pi) := by
  rw [positive_faithful_period hk hp h]
  field_simp

#print axioms faithful_period_forces_one_turn
#print axioms one_turn_gives_faithful_period
#print axioms faithful_period_iff
#print axioms positive_faithful_period
#print axioms reciprocal_temperature
end ChatgptAudit.PolarPeriod016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
