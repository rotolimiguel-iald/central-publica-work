import CollapseContract
import TGLExt.LocalHorizontalPauli

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ChatgptAudit.Collapse057
open TGLExt ChatgptAudit ChatgptAudit.Aperiodic046 ChatgptAudit.Expectation047
  ChatgptAudit.Observable035 ChatgptAudit.Orbit052

noncomputable section

/-- Restrict the domain to the actual factor; no arbitrary values outside M. -/
abbrev FactorCarrier (P : SiteProfile) :=
  {A : TowerHilbert P →L[ℂ] TowerHilbert P // A ∈ theFactorObject P}

def towerReduction (P : SiteProfile) (A : FactorCarrier P) : FactorCarrier P :=
  ⟨(aperiodicExpectationInput P).E A.val,
    ((aperiodicExpectationInput P).into A.val A.property).1⟩

theorem tower_reduction_idempotent (P : SiteProfile) (A : FactorCarrier P) :
    towerReduction P (towerReduction P A) = towerReduction P A := by
  apply Subtype.ext
  exact aperiodic_expectation_idempotent P A.val A.property

theorem tower_reduction_preserves_state (P : SiteProfile) (A : FactorCarrier P) :
    omegaState P (towerReduction P A).val = omegaState P A.val :=
  expectation_preserves_omega P (aperiodicExpectationInput P) A.val A.property

theorem tower_reduction_preserves_unit (P : SiteProfile) :
    towerReduction P ⟨1, (theFactorObject P).one_mem⟩ =
      ⟨1, (theFactorObject P).one_mem⟩ := by
  apply Subtype.ext
  exact expectation_one P (aperiodicExpectationInput P)

theorem tower_fixed_points_exactly_centralizer (P : SiteProfile) (A : FactorCarrier P) :
    towerReduction P A = A ↔ A.val ∈ omegaCentralizer P := by
  constructor
  · intro h
    have hi := (aperiodicExpectationInput P).into A.val A.property
    have he := congrArg Subtype.val h
    exact he ▸ hi
  · intro h
    exact Subtype.ext ((aperiodicExpectationInput P).fixes A.val h)

theorem tower_pauli_x_nonzero (P : SiteProfile) : sitePauliX P 0 ≠ 0 := by
  intro h
  have hn := pauli_x_gns_norm P
  rw [h] at hn
  norm_num at hn

theorem tower_reduction_effective (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    ∃ A : FactorCarrier P, towerReduction P A ≠ A := by
  refine ⟨⟨sitePauliX P 0, site_pauli_x_mem_factor P 0⟩, ?_⟩
  intro h
  have he := congrArg Subtype.val h
  change (aperiodicExpectationInput P).E (sitePauliX P 0) = sitePauliX P 0 at he
  rw [aperiodic_pauli_x_zero P hp] at he
  exact tower_pauli_x_nonzero P he.symm

/-- Constructed inhabitant for the nontracial first-site regime. -/
def actualTowerCollapse (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    IdentityCollapse (FactorCarrier P) ℂ where
  step := towerReduction P
  identity := fun A => omegaState P A.val
  stable := tower_reduction_idempotent P
  preserves := tower_reduction_preserves_state P
  effective := tower_reduction_effective P hp

theorem actual_tower_collapse_no_inverse (P : SiteProfile) (hp : P.w 0 ≠ 1 / 2) :
    ¬ ∃ R : FactorCarrier P → FactorCarrier P,
      Function.LeftInverse R (towerReduction P) :=
  collapse_has_no_left_inverse (actualTowerCollapse P hp)

/-- Negative control: the fully tracial profile gives no changed collapse event. -/
theorem tracial_tower_reduction_is_identity (P : SiteProfile)
    (hp : ∀ n, P.w n = 1 / 2) : towerReduction P = id := by
  funext A
  apply (tower_fixed_points_exactly_centralizer P A).mpr
  exact (half_profile_centralizer_is_factor hp A.val).mpr A.property

theorem tracial_tower_has_no_effective_witness (P : SiteProfile)
    (hp : ∀ n, P.w n = 1 / 2) :
    ¬ ∃ A : FactorCarrier P, towerReduction P A ≠ A := by
  rw [tracial_tower_reduction_is_identity P hp]
  simp

#print axioms FactorCarrier
#print axioms towerReduction
#print axioms tower_reduction_idempotent
#print axioms tower_reduction_preserves_state
#print axioms tower_reduction_preserves_unit
#print axioms tower_fixed_points_exactly_centralizer
#print axioms tower_pauli_x_nonzero
#print axioms tower_reduction_effective
#print axioms actualTowerCollapse
#print axioms actual_tower_collapse_no_inverse
#print axioms tracial_tower_reduction_is_identity
#print axioms tracial_tower_has_no_effective_witness
end
end ChatgptAudit.Collapse057
