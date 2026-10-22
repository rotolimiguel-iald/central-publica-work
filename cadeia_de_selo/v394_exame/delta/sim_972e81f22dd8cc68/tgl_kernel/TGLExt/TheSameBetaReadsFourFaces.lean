import TGLExt.TheSameBetaReadsThreeFaces

set_option autoImplicit false

/-!
# The fourth reading: a named field equation (Order 012, B1 prime)

The operators and curvature are imported data on a space of sections.
EOM is an explicit input, not a consequence of the three algebraic readings.
The linear operator called boxOperator is not constructed from a metric here.
K_boundary is not identified with towerFlow or a Stone/Tomita generator.
Xi has its own field and is not defined from, or identified with, beta.
Consumer proposed: ext_pb_same_beta_four_faces_kernel_proved.
-/

namespace TGLExt

/-- Real-linear operators on complex-valued sections, with independent curvature
    coefficient. Linearity is a declared scope restriction, not physical evidence. -/
structure ActionCouplingData (X : Type*) where
  boxOperator : (X → ℂ) →ₗ[ℝ] (X → ℂ)
  mass : ℝ
  xi : ℝ
  scalarCurvature : X → ℝ
  K_boundary : (X → ℂ) →ₗ[ℝ] (X → ℂ)

namespace ActionCouplingData
noncomputable section
variable {X : Type*}

def curvatureTerm (D : ActionCouplingData X) (psi : X → ℂ) : X → ℂ :=
  fun x => D.scalarCurvature x • psi x

def fieldOperator (D : ActionCouplingData X) (psi : X → ℂ) : X → ℂ :=
  D.boxOperator psi - D.mass ^ 2 • psi - D.xi • D.curvatureTerm psi

def modularSource (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) : X → ℂ := c.beta • D.K_boundary psi

/-- INPUT: the field equation; the data structure alone does not supply it. -/
def EOM (D : ActionCouplingData X) (c : TGLCoupling) (psi : X → ℂ) : Prop :=
  D.fieldOperator psi = D.modularSource c psi

/-- The same equation evaluated on a section at one point. -/
theorem eom_at (D : ActionCouplingData X) (c : TGLCoupling) (psi : X → ℂ)
    (hEOM : D.EOM c psi) (x : X) :
    D.boxOperator psi x - D.mass ^ 2 • psi x -
      (D.xi * D.scalarCurvature x) • psi x = c.beta • D.K_boundary psi x := by
  have h := congrFun hEOM x
  simpa [EOM, fieldOperator, modularSource, curvatureTerm, smul_smul, mul_assoc] using h

/-- Xi does not change the modular source. Its separate role is in fieldOperator. -/
theorem modular_source_ignores_xi (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (xi : ℝ) :
    ({ D with xi := xi } : ActionCouplingData X).modularSource c psi =
      D.modularSource c psi := rfl

/-- Identifiability requires a nonzero source vector, not merely positive beta. -/
theorem modular_coefficient_unique (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hK : D.K_boundary psi ≠ 0) (b : ℝ)
    (h : b • D.K_boundary psi = D.modularSource c psi) : b = c.beta := by
  exact smul_left_injective ℝ hK h

/-- A changed coefficient cannot satisfy the same EOM on a nonzero source. -/
theorem eom_rejects_changed_coefficient (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hEOM : D.EOM c psi) (hK : D.K_boundary psi ≠ 0)
    (b : ℝ) (hb : b ≠ c.beta) :
    D.fieldOperator psi ≠ b • D.K_boundary psi := by
  intro hbad
  exact hb (D.modular_coefficient_unique c psi hK b (hbad.symm.trans hEOM))

/-- A distinct imported generator value cannot be silently substituted. -/
theorem eom_rejects_changed_generator (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hEOM : D.EOM c psi)
    (K : (X → ℂ) →ₗ[ℝ] (X → ℂ)) (hK : K psi ≠ D.K_boundary psi) :
    D.fieldOperator psi ≠ c.beta • K psi := by
  intro hbad
  apply hK
  apply smul_right_injective (X → ℂ) (ne_of_gt c.beta_pos)
  exact hbad.symm.trans hEOM

/-- Omitting the curvature coupling is wrong when its evaluated term is nonzero. -/
theorem eom_rejects_missing_curvature (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hEOM : D.EOM c psi)
    (hcurv : D.xi • D.curvatureTerm psi ≠ 0) :
    D.boxOperator psi - D.mass ^ 2 • psi ≠ D.modularSource c psi := by
  intro hbad
  have h : (D.boxOperator psi - D.mass ^ 2 • psi) - D.xi • D.curvatureTerm psi =
      D.boxOperator psi - D.mass ^ 2 • psi := hEOM.trans hbad.symm
  exact hcurv (sub_eq_self.mp h)

/-- The degenerate source cannot identify a coefficient. -/
theorem zero_source_hides_coefficient (D : ActionCouplingData X) (c : TGLCoupling)
    (psi : X → ℂ) (hK : D.K_boundary psi = 0) (b : ℝ) :
    b • D.K_boundary psi = D.modularSource c psi := by
  simp [modularSource, hK]

end
end ActionCouplingData

/-- Exact extension of B1: its full conjunction is supplied by the existing
    theorem, and the named EOM input exposes the fourth occurrence of c.beta. -/
theorem the_same_beta_reads_four_faces {X : Type*}
    (c : TGLCoupling) (D : ActionCouplingData X) (psi : X → ℂ)
    (hEOM : D.EOM c psi) (ρr ρm ρΛ : ℝ) :
    (Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta
    ∧ (0 < c.alpha ∧ c.alpha < 1
      ∧ c.beta = c.alpha * Real.exp (1 / 2)
      ∧ c.beta = c.alpha * Real.sqrt (Real.exp 1))
    ∧ (c.beta * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
        = c.beta * ((4 / 3) * ρr + ρm))
    ∧ ((ρr + ρm + ρΛ) + c.beta * ((4 / 3) * ρr + ρm)
        = (1 + 4 * c.beta / 3) * ρr + (1 + c.beta) * ρm + ρΛ)
    ∧ (∀ t g : ℝ, 0 < t → 0 < g → Real.exp (-(t * c.beta * g)) < 1)
    ∧ (∀ b : ℝ, (∀ t : ℝ, Real.exp (-(t * b)) = Real.exp (-(t * c.beta)))
        → b = c.beta))
    ∧ (D.boxOperator psi - D.mass ^ 2 • psi -
        D.xi • (fun x => D.scalarCurvature x • psi x) =
        c.beta • D.K_boundary psi) := by
  exact ⟨the_same_beta_reads_three_faces c ρr ρm ρΛ, hEOM⟩

end TGLExt
