import TGLExt.V350ScalarTomitaPolarInvolution

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt ChatgptAudit.Continuous050
noncomputable section
variable (P : SiteProfile)

/-- The existing maximal adjoint domain is exactly the inverse image of the
original positive-root domain under the original polar antiunitary. -/
theorem scalarTomitaAdjoint_polar_domain_iff (y : ScalarGNSHilbert P) :
    y ∈ scalarTomitaAdjointDomain P ↔
      scalarTomitaPolarFactor P y ∈ (scalarTomitaPositiveRoot P).domain := by
  constructor
  · intro hy
    obtain ⟨h, _⟩ := generic_adjoint_maximal (scalarTomitaPositiveRoot P)
      (scalarTomitaPositiveRoot_selfadjoint P) (scalarTomitaPolarFactor P)
      (scalarTomitaPolarFactor_involutive P)
      (y := y) (z := scalarTomitaAdjoint P ⟨y, hy⟩) (by
        intro x
        change inner ℂ (scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P x)) y = _
        rw [scalarTomitaPolarFactor_root]
        exact scalarTomitaAdjoint_pairing P ⟨y, hy⟩ _)
    exact h
  · intro hy
    apply (scalarTomitaAdjoint_maximal P (z := genericTomitaAdjoint
      (scalarTomitaPositiveRoot P) (scalarTomitaPolarFactor P) ⟨y, hy⟩) ?_).choose
    intro x
    have h := generic_adjoint_pairing (scalarTomitaPositiveRoot P)
      (scalarTomitaPositiveRoot_selfadjoint P) (scalarTomitaPolarFactor P)
      (scalarTomitaPolarFactor_involutive P)
      (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x) ⟨y, hy⟩
    change inner ℂ (scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P
      (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) x))) y = _ at h
    exact (congrArg (fun v : ScalarGNSHilbert P => inner ℂ v y)
      (scalarTomitaPolarFactor_factorization P x)).symm.trans h

def scalarTomitaAdjointRootInput (y : scalarTomitaAdjointDomain P) :
    (scalarTomitaPositiveRoot P).domain :=
  ⟨scalarTomitaPolarFactor P (y : ScalarGNSHilbert P),
    (scalarTomitaAdjoint_polar_domain_iff P y).mp y.property⟩

/-- F = B J on the entire original maximal adjoint domain; B is the same
positive root that gave S = J B. No new adjoint or polar factor is defined. -/
theorem scalarTomitaAdjoint_polar_value (y : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjoint P y =
      scalarTomitaPositiveRoot P (scalarTomitaAdjointRootInput P y) := by
  apply (scalarClosedTomita_domain_dense (P := P)).eq_of_inner_left ℂ
  intro x hx
  have h := generic_adjoint_pairing (scalarTomitaPositiveRoot P)
    (scalarTomitaPositiveRoot_selfadjoint P) (scalarTomitaPolarFactor P)
    (scalarTomitaPolarFactor_involutive P)
    (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) ⟨x, hx⟩)
    ⟨y, (scalarTomitaAdjoint_polar_domain_iff P y).mp y.property⟩
  change inner ℂ (scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P
    (Submodule.inclusion (scalarClosedTomitaDomain_le_root P) ⟨x, hx⟩)))
    (y : ScalarGNSHilbert P) =
      inner ℂ (scalarTomitaPositiveRoot P (scalarTomitaAdjointRootInput P y)) x at h
  exact (scalarTomitaAdjoint_pairing P y ⟨x, hx⟩).symm.trans
    ((congrArg (fun v : ScalarGNSHilbert P => inner ℂ v (y : ScalarGNSHilbert P))
      (scalarTomitaPolarFactor_factorization P ⟨x, hx⟩)).symm.trans h)

theorem scalarTomitaAdjoint_conjugate_domain_iff (y : ScalarGNSHilbert P) :
    y ∈ scalarTomitaAdjointDomain P ↔
      scalarTomitaPolarFactor P y ∈ scalarClosedTomitaDomain P := by
  rw [scalarTomitaAdjoint_polar_domain_iff, scalarTomitaPositiveRoot_domain_eq]

def scalarTomitaAdjointConjugateInput (y : scalarTomitaAdjointDomain P) :
    scalarClosedTomitaDomain P :=
  ⟨scalarTomitaPolarFactor P (y : ScalarGNSHilbert P),
    (scalarTomitaAdjoint_conjugate_domain_iff P y).mp y.property⟩

/-- Full-domain identity F = J S J, with the original S, F, and J. -/
theorem scalarTomitaAdjoint_conjugate_value (y : scalarTomitaAdjointDomain P) :
    scalarTomitaAdjoint P y = scalarTomitaPolarFactor P
      (scalarClosedTomita P (scalarTomitaAdjointConjugateInput P y)) := by
  rw [scalarTomitaAdjoint_polar_value]
  have he : Submodule.inclusion (scalarTomitaRootDomain_le_closed P)
      (scalarTomitaAdjointRootInput P y) = scalarTomitaAdjointConjugateInput P y :=
    Subtype.ext rfl
  calc
    _ = scalarTomitaPolarFactor P (scalarTomitaPolarFactor P
        (scalarTomitaPositiveRoot P (scalarTomitaAdjointRootInput P y))) :=
      (scalarTomitaPolarFactor_involutive P _).symm
    _ = _ := congrArg (scalarTomitaPolarFactor P)
      ((scalarTomitaPolarFactor_root P _).trans (congrArg (scalarClosedTomita P) he))

theorem scalarTomitaPolar_closed_domain_iff (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P x ∈ scalarTomitaAdjointDomain P ↔
      x ∈ scalarClosedTomitaDomain P := by
  rw [scalarTomitaAdjoint_conjugate_domain_iff, scalarTomitaPolarFactor_involutive]

def scalarClosedTomitaConjugateInput (x : scalarClosedTomitaDomain P) :
    scalarTomitaAdjointDomain P :=
  ⟨scalarTomitaPolarFactor P (x : ScalarGNSHilbert P),
    (scalarTomitaPolar_closed_domain_iff P x).mpr x.property⟩

theorem scalarClosedTomita_conjugate_value (x : scalarClosedTomitaDomain P) :
    scalarClosedTomita P x = scalarTomitaPolarFactor P
      (scalarTomitaAdjoint P (scalarClosedTomitaConjugateInput P x)) := by
  rw [scalarTomitaAdjoint_conjugate_value, scalarTomitaPolarFactor_involutive]
  congr 1
  exact Subtype.ext (scalarTomitaPolarFactor_involutive P (x : ScalarGNSHilbert P)).symm

theorem scalarTomitaPolar_conjugates_closed_graph :
    (fun p : ScalarGNSHilbert P × ScalarGNSHilbert P =>
      (scalarTomitaPolarFactor P p.1, scalarTomitaPolarFactor P p.2)) ''
      Set.range (fun x : scalarClosedTomitaDomain P =>
        ((x : ScalarGNSHilbert P), scalarClosedTomita P x)) =
    Set.range (fun y : scalarTomitaAdjointDomain P =>
      ((y : ScalarGNSHilbert P), scalarTomitaAdjoint P y)) := by
  ext p
  constructor
  · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
    refine ⟨scalarClosedTomitaConjugateInput P x, Prod.ext rfl ?_⟩
    have h := congrArg (scalarTomitaPolarFactor P) (scalarClosedTomita_conjugate_value P x)
    rw [scalarTomitaPolarFactor_involutive] at h
    exact h.symm
  · rintro ⟨y, rfl⟩
    refine ⟨_, ⟨scalarTomitaAdjointConjugateInput P y, rfl⟩, Prod.ext ?_ ?_⟩
    · exact scalarTomitaPolarFactor_involutive P (y : ScalarGNSHilbert P)
    · exact (scalarTomitaAdjoint_conjugate_value P y).symm

#print axioms scalarTomitaAdjoint_polar_domain_iff
#print axioms scalarTomitaAdjointRootInput
#print axioms scalarTomitaAdjoint_polar_value
#print axioms scalarTomitaAdjoint_conjugate_domain_iff
#print axioms scalarTomitaAdjointConjugateInput
#print axioms scalarTomitaAdjoint_conjugate_value
#print axioms scalarTomitaPolar_closed_domain_iff
#print axioms scalarClosedTomitaConjugateInput
#print axioms scalarClosedTomita_conjugate_value
#print axioms scalarTomitaPolar_conjugates_closed_graph
end
end TGLV350.Regular
