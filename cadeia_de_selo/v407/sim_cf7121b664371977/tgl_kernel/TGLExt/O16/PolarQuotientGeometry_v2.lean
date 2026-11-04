import Lean
import TGLExt.O16.PolarMinimalPeriod_v2

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.PolarPeriod016

def periodSetoid (period : ℝ) : Setoid ℝ where
  r t u := ∃ n : ℤ, t = u + (n : ℝ)*period
  iseqv := {
    refl := fun t => ⟨0, by simp⟩
    symm := by
      intro t u h
      obtain ⟨n, hn⟩ := h
      refine ⟨-n, ?_⟩
      push_cast
      linarith
    trans := by
      intro t u v htu huv
      obtain ⟨n, hn⟩ := htu
      obtain ⟨m, hm⟩ := huv
      refine ⟨m+n, ?_⟩
      push_cast
      nlinarith }

/-- General descent criterion, with an actual quotient map and injectivity. -/
theorem injective_quotient_factor_iff {A B : Type*} (s : Setoid A) (f : A → B) :
    (∃ F : Quotient s → B,
      (∀ t, F (Quotient.mk s t) = f t) ∧ Function.Injective F) ↔
      ∀ t u, f t = f u ↔ s.r t u := by
  constructor
  · rintro ⟨F, hF, hi⟩ t u
    constructor
    · intro hh
      apply Quotient.exact
      apply hi
      simpa only [hF] using hh
    · intro hh
      have he := congrArg F (Quotient.sound hh)
      simpa only [hF] using he
  · intro h
    let F : Quotient s → B := Quotient.lift f (fun t u hh => (h t u).mpr hh)
    refine ⟨F, fun t => rfl, ?_⟩
    intro x y
    refine Quotient.inductionOn₂ x y ?_
    intro t u hh
    exact Quotient.sound ((h t u).mp hh)

/-- Complex coordinates identify the ordinary Euclidean plane R^2. -/
def polarPoint (radius kappa t : ℝ) : ℂ :=
  (radius : ℂ) * (Circle.exp (kappa*t) : ℂ)

theorem polarPoint_eq_iff {radius kappa t u : ℝ} (hr : radius ≠ 0) :
    polarPoint radius kappa t = polarPoint radius kappa u ↔
      Circle.exp (kappa*t) = Circle.exp (kappa*u) := by
  unfold polarPoint
  constructor
  · intro hh
    apply Subtype.ext
    exact mul_left_cancel₀ (Complex.ofReal_ne_zero.mpr hr) hh
  · intro hh
    rw [hh]

theorem polar_descends_injectively_iff {radius kappa period : ℝ}
    (hr : 0 < radius) (hk : kappa ≠ 0) :
    (∃ F : Quotient (periodSetoid period) → ℂ,
      (∀ t, F (Quotient.mk (periodSetoid period) t) = polarPoint radius kappa t) ∧
      Function.Injective F) ↔
      kappa*period = 2*Real.pi ∨ kappa*period = -(2*Real.pi) := by
  rw [injective_quotient_factor_iff]
  have he : (∀ t u, polarPoint radius kappa t = polarPoint radius kappa u ↔
      (periodSetoid period).r t u) ↔ AngularQuotientFaithful kappa period := by
    simp only [polarPoint_eq_iff (ne_of_gt hr), AngularQuotientFaithful]
    rfl
  rw [he, faithful_period_iff hk]

/-- The positive-temperature reading follows from an injective polar quotient.
It is not, by itself, a KMS theorem for a Lorentzian quantum state. -/
theorem polar_quotient_reciprocal_temperature {radius kappa period : ℝ}
    (hr : 0 < radius) (hk : 0 < kappa) (hp : 0 < period)
    (h : ∃ F : Quotient (periodSetoid period) → ℂ,
      (∀ t, F (Quotient.mk (periodSetoid period) t) = polarPoint radius kappa t) ∧
      Function.Injective F) : 1/period = kappa/(2*Real.pi) := by
  apply reciprocal_temperature hk hp
  exact (faithful_period_iff (ne_of_gt hk)).mpr
    ((polar_descends_injectively_iff hr (ne_of_gt hk)).mp h)

#print axioms periodSetoid
#print axioms injective_quotient_factor_iff
#print axioms polarPoint_eq_iff
#print axioms polar_descends_injectively_iff
#print axioms polar_quotient_reciprocal_temperature
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
