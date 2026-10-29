import TGLExt.TheSameBetaReadsFourFaces

set_option autoImplicit false

/-! Algebraic controls, not a physical realization of a wave operator. -/
namespace TGLExt.ActionCouplingControls
noncomputable section
open ActionCouplingData

/-- Independent xi and an independently chosen gain in the box operator. -/
def scalarModel (xi gain : ℝ) : ActionCouplingData Unit where
  boxOperator := (xi + gain) • LinearMap.id
  mass := 0
  xi := xi
  scalarCurvature := fun _ => 1
  K_boundary := LinearMap.id

def unitSection : Unit → ℂ := fun _ => 1

theorem unitSection_ne_zero : unitSection ≠ 0 := by
  intro h
  have h1 := congrFun h ()
  simpa [unitSection] using h1

theorem scalar_model_field (xi gain : ℝ) :
    (scalarModel xi gain).fieldOperator unitSection = gain • unitSection := by
  ext x
  simp [fieldOperator, curvatureTerm, scalarModel, unitSection, add_smul]

theorem scalar_model_eom (c : TGLCoupling) (xi : ℝ) :
    (scalarModel xi c.beta).EOM c unitSection := by
  change (scalarModel xi c.beta).fieldOperator unitSection = c.beta • unitSection
  exact scalar_model_field xi c.beta

/-- Nonzero section/source and arbitrary xi: the conditional type is inhabited. -/
theorem nonzero_model_for_every_xi (c : TGLCoupling) (xi : ℝ) :
    (scalarModel xi c.beta).xi = xi ∧
    (scalarModel xi c.beta).K_boundary unitSection ≠ 0 ∧
    (scalarModel xi c.beta).EOM c unitSection :=
  ⟨rfl, unitSection_ne_zero, scalar_model_eom c xi⟩

/-- Same data shape and nonzero source, but a different box gain refutes EOM. -/
theorem scalar_model_rejects_wrong_gain (c : TGLCoupling) (xi gain : ℝ)
    (hg : gain ≠ c.beta) : ¬ (scalarModel xi gain).EOM c unitSection := by
  intro h
  have heq : gain • unitSection = c.beta • unitSection :=
    (scalar_model_field xi gain).symm.trans h
  exact hg (smul_left_injective ℝ unitSection_ne_zero heq)

/-- In particular the three readings and the operator data do not supply EOM. -/
theorem data_alone_does_not_supply_eom (c : TGLCoupling) (xi : ℝ) :
    ¬ (scalarModel xi (-c.beta)).EOM c unitSection := by
  apply scalar_model_rejects_wrong_gain
  linarith [c.beta_pos]

theorem reject_sign_flip {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hEOM : D.EOM c psi) (hK : D.K_boundary psi ≠ 0) :
    D.fieldOperator psi ≠ (-c.beta) • D.K_boundary psi := by
  apply D.eom_rejects_changed_coefficient c psi hEOM hK
  linarith [c.beta_pos]

theorem reject_xi_as_beta {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hEOM : D.EOM c psi) (hK : D.K_boundary psi ≠ 0)
    (hxi : D.xi ≠ c.beta) : D.fieldOperator psi ≠ D.xi • D.K_boundary psi :=
  D.eom_rejects_changed_coefficient c psi hEOM hK D.xi hxi

theorem reject_bare_alpha {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hEOM : D.EOM c psi) (hK : D.K_boundary psi ≠ 0) :
    D.fieldOperator psi ≠ c.alpha • D.K_boundary psi := by
  apply D.eom_rejects_changed_coefficient c psi hEOM hK
  exact (c.reflection_rejects_bare_alpha ∘ fun h => c.reflection_weight.trans h.symm)

/-- Even after assuming EOM on a nonzero field, xi is not selected. -/
theorem xi_is_not_selected (c : TGLCoupling) (referenceXi : ℝ) :
    ∃ D : ActionCouplingData Unit, D.EOM c unitSection ∧
      D.K_boundary unitSection ≠ 0 ∧ D.xi ≠ referenceXi := by
  refine ⟨scalarModel (referenceXi + 1) c.beta,
    scalar_model_eom c (referenceXi + 1), unitSection_ne_zero, ?_⟩
  change referenceXi + 1 ≠ referenceXi
  linarith

/-- With a zero source distinct symbolic coefficients give the same result. -/
theorem zero_source_not_unique {X : Type*} (D : ActionCouplingData X)
    (c : TGLCoupling) (psi : X → ℂ) (hK : D.K_boundary psi = 0) :
    ∃ b : ℝ, b ≠ c.beta ∧ b • D.K_boundary psi = D.modularSource c psi := by
  refine ⟨-c.beta, ?_, D.zero_source_hides_coefficient c psi hK (-c.beta)⟩
  linarith [c.beta_pos]

end
end TGLExt.ActionCouplingControls
