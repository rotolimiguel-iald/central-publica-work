import TGLExt.TheSameBetaReadsFourFaces

set_option autoImplicit false

namespace IndependentB1Prime
open TGLExt TGLExt.ActionCouplingData
noncomputable section

def probe : Unit → ℂ := fun _ => 1

theorem probe_nonzero : probe ≠ 0 := by
  intro h
  have hx := congrFun h ()
  simpa [probe] using hx

/-- This algebraic test fixes the box and curvature before changing xi. -/
def fixedData (c : TGLCoupling) (xi : ℝ) : ActionCouplingData Unit where
  boxOperator := (xi + c.beta) • LinearMap.id
  mass := 0
  xi := xi
  scalarCurvature := fun _ => 1
  K_boundary := LinearMap.id

theorem changed_field (c : TGLCoupling) (xi eta : ℝ) :
    ({ fixedData c xi with xi := eta } : ActionCouplingData Unit).fieldOperator probe =
      (xi + c.beta - eta) • probe := by
  ext x
  simp [fieldOperator, curvatureTerm, fixedData, probe, add_smul, sub_smul]

theorem baseline (c : TGLCoupling) (xi : ℝ) : (fixedData c xi).EOM c probe := by
  change ({ fixedData c xi with xi := xi } : ActionCouplingData Unit).fieldOperator probe =
    c.beta • probe
  rw [changed_field]
  congr 1
  ring

/-- Same box, mass, curvature and generator: xi cannot silently change. -/
theorem xi_change_iff (c : TGLCoupling) (xi eta : ℝ) :
    ({ fixedData c xi with xi := eta } : ActionCouplingData Unit).EOM c probe ↔ eta = xi := by
  change ({ fixedData c xi with xi := eta } : ActionCouplingData Unit).fieldOperator probe =
    c.beta • probe ↔ eta = xi
  rw [changed_field, (smul_left_injective ℝ probe_nonzero).eq_iff]
  constructor <;> intro h <;> linarith

theorem beta_change_iff (c : TGLCoupling) (xi b : ℝ) :
    (fixedData c xi).fieldOperator probe = b • (fixedData c xi).K_boundary probe ↔
      b = c.beta := by
  have h := baseline c xi
  change (fixedData c xi).fieldOperator probe = c.beta • probe at h
  change (fixedData c xi).fieldOperator probe = b • probe ↔ b = c.beta
  rw [h, (smul_left_injective ℝ probe_nonzero).eq_iff]
  exact eq_comm

theorem xi_positive (c : TGLCoupling) (xi : ℝ) :
    ({ fixedData c xi with xi := xi } : ActionCouplingData Unit).EOM c probe :=
  (xi_change_iff c xi xi).2 rfl

theorem xi_negative_wall (c : TGLCoupling) (xi eta : ℝ) (h : eta ≠ xi) :
    ¬ ({ fixedData c xi with xi := eta } : ActionCouplingData Unit).EOM c probe := by
  intro hE
  exact h ((xi_change_iff c xi eta).1 hE)

theorem beta_positive (c : TGLCoupling) (xi : ℝ) :
    (fixedData c xi).fieldOperator probe = c.beta • (fixedData c xi).K_boundary probe :=
  (beta_change_iff c xi c.beta).2 rfl

theorem beta_negative_wall (c : TGLCoupling) (xi b : ℝ) (h : b ≠ c.beta) :
    (fixedData c xi).fieldOperator probe ≠ b • (fixedData c xi).K_boundary probe := by
  intro hE
  exact h ((beta_change_iff c xi b).1 hE)

/-- A kernel-visible vacuity boundary: every datum accepts the zero field. -/
theorem zero_field_eom {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling) :
    D.EOM c 0 := by
  have hz : D.curvatureTerm (0 : X → ℂ) = 0 := by
    ext x
    simp [curvatureTerm]
  simp [EOM, fieldOperator, modularSource, hz]

/-- The fourth conjunct is exactly the EOM input after unfolding definitions. -/
theorem fourth_projection {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hEOM : D.EOM c psi) (rr rm rl : ℝ) : D.EOM c psi :=
  (the_same_beta_reads_four_faces c D psi hEOM rr rm rl).2

/-- Distinct roles do not impose the numerical inequality xi != beta. -/
theorem equal_roles_admitted (c : TGLCoupling) :
    (fixedData c c.beta).xi = c.beta ∧ (fixedData c c.beta).EOM c probe ∧
      (fixedData c c.beta).K_boundary probe ≠ 0 :=
  ⟨rfl, baseline c c.beta, probe_nonzero⟩

end
end IndependentB1Prime

#print axioms IndependentB1Prime.probe_nonzero
#print axioms IndependentB1Prime.changed_field
#print axioms IndependentB1Prime.baseline
#print axioms IndependentB1Prime.xi_change_iff
#print axioms IndependentB1Prime.beta_change_iff
#print axioms IndependentB1Prime.xi_positive
#print axioms IndependentB1Prime.xi_negative_wall
#print axioms IndependentB1Prime.beta_positive
#print axioms IndependentB1Prime.beta_negative_wall
#print axioms IndependentB1Prime.zero_field_eom
#print axioms IndependentB1Prime.fourth_projection
#print axioms IndependentB1Prime.equal_roles_admitted
