import TGLExt.V350FixedCoreBaseIdentification
import TGLExt.V350DualFixedWeightLaws
import TGLExt.V350DualEnergyOnResolvent
import TGLExt.RightMult

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology ENNReal
noncomputable section

def regularVacuum (P : SiteProfile) : RegularHilbert (TowerHilbert P) :=
  testVector (hOmega P)

theorem regularVacuum_norm (P : SiteProfile) : ‖regularVacuum P‖ = 1 := by
  rw [regularVacuum, testVector_norm, hOmega_norm]

/-- The interval vacuum is separating for F, using the original tower's
separating vector and the proved fixed-base identification. -/
theorem fixedCore_regularVacuum_separating (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hB : B ∈ dualFixedCore P) (hzero : B (regularVacuum P) = 0) : B = 0 := by
  obtain ⟨C,hC,he⟩ := (dualFixedCore_eq_amplified_base P B).mp hB
  subst B
  change fibre C (testVector (hOmega P)) = 0 at hzero
  rw [fibre_testVector] at hzero
  have hc0 : C (hOmega P) = 0 := by
    apply norm_eq_zero.mp
    rw [← testVector_norm, hzero, norm_zero]
  rw [factor_omega_separating hC hc0]
  exact map_zero fibreRepresentation

theorem dualResolvent_fixes_zero_form_vector
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) (hv : dualQuadraticIntegral A v = 0) : R v = v := by
  have hm := dualResolvent_limit_minimizes_energy A R hA hlim v v
  have he : dualEnergy A v v = 0 := by
    simp only [dualEnergy, sub_self, norm_zero, hv]
    norm_num
  rw [he] at hm
  have hn : ENNReal.ofReal (‖R v-v‖^2) = 0 :=
    le_antisymm ((le_add_right le_rfl).trans hm) bot_le
  have hsq : ‖R v-v‖^2 ≤ 0 := ENNReal.ofReal_eq_zero.mp hn
  have hnorm : ‖R v-v‖ = 0 := by nlinarith [norm_nonneg (R v-v)]
  exact sub_eq_zero.mp (norm_eq_zero.mp hnorm)

/-- Evaluating the dual form at the interval vacuum is faithful on N+.
Finitude is checked before toReal is used; the resolvent is in F. -/
theorem dualQuadraticIntegral_vacuum_faithful (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
    (hm : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :
    dualQuadraticIntegral A (regularVacuum P) = 0 ↔ A = 0 := by
  constructor
  · intro hv
    obtain ⟨R,hmR,hR,hone,hlim,hfix⟩ := exists_dualResolvent_fixed P A hm hA
    have hf : R ∈ dualFixedCore P := (dualFixedCore_mem_iff P R).mpr ⟨hmR,hfix⟩
    have hz : (R-1) (regularVacuum P) = 0 := by
      change R (regularVacuum P) - regularVacuum P = 0
      exact sub_eq_zero.mpr (dualResolvent_fixes_zero_form_vector A R hA hlim _ hv)
    have hRone : R = 1 := sub_eq_zero.mp
      (fixedCore_regularVacuum_separating P (R-1)
        ((dualFixedCore P).sub_mem hf (dualFixedCore P).one_mem) hz)
    apply (dualQuadraticIntegral_faithful A hA).mp
    intro v
    have hfinite := dualResolvent_limit_range_finite A R hA hlim v
    have hid := dualResolvent_limit_energy_identity A R hA hlim v
    rw [hRone] at hfinite hid
    change dualQuadraticIntegral A v < ⊤ at hfinite
    change (dualQuadraticIntegral A v).toReal = (inner ℂ v (v-v)).re at hid
    simp only [sub_self, inner_zero_right, Complex.zero_re] at hid
    calc
      dualQuadraticIntegral A v = ENNReal.ofReal (dualQuadraticIntegral A v).toReal :=
        (ENNReal.ofReal_toReal (ne_of_lt hfinite)).symm
      _ = 0 := by rw [hid, ENNReal.ofReal_zero]
  · rintro rfl
    exact dualQuadraticIntegral_zero _

#print axioms regularVacuum_norm
#print axioms fixedCore_regularVacuum_separating
#print axioms dualResolvent_fixes_zero_form_vector
#print axioms dualQuadraticIntegral_vacuum_faithful
end
end TGLV350.Regular
