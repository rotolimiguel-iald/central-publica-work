import TGLExt.V350RealPhaseVariational
import TGLExt.V350ScalarTomitaStandardSubspace
import TGLExt.V350ScalarTomitaAdjoint

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt ClosedSubmodule
noncomputable section
local instance scalarPhaseSpaceComplete (P : SiteProfile) :
    CompleteSpace (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule :=
  (ChatgptAudit.Continuous049.fixedRealSubmodule_closed
    (scalarClosedTomitaDomain P) (scalarClosedTomita P) scalarClosedTomita_is_closed).completeSpace_coe

/-- The solver acts in Fix S on the original scalar GNS Hilbert space. -/
def scalarPhaseVariational (P : SiteProfile) (z : ℂ) (hz : 0 < z.re) :
    ScalarGNSHilbert P →L[ℝ] (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule :=
  phaseVariationalSolution (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule z hz

theorem scalarPhaseVariational_fixed (P : SiteProfile) (z : ℂ) (hz : 0 < z.re)
    (x : ScalarGNSHilbert P) :
    ∃ hy : (scalarPhaseVariational P z hz x : ScalarGNSHilbert P) ∈ scalarClosedTomitaDomain P,
      scalarClosedTomita P ⟨(scalarPhaseVariational P z hz x : ScalarGNSHilbert P),hy⟩ =
        (scalarPhaseVariational P z hz x : ScalarGNSHilbert P) :=
  (scalarPhaseVariational P z hz x).property

theorem scalarPhaseVariational_equation (P : SiteProfile) (z : ℂ) (hz : 0 < z.re)
    (x : ScalarGNSHilbert P) (v : (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule) :
    (inner ℂ x (v : ScalarGNSHilbert P)).re =
      (z * inner ℂ (scalarPhaseVariational P z hz x : ScalarGNSHilbert P) (v : ScalarGNSHilbert P)).re :=
  phaseVariationalSolution_equation (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule z hz x v

theorem scalarPhaseVariational_unique (P : SiteProfile) (z : ℂ) (hz : 0 < z.re)
    (x : ScalarGNSHilbert P) (u : (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule)
    (hu : ∀ v : (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule,
      (inner ℂ x (v : ScalarGNSHilbert P)).re = (z * inner ℂ (u : ScalarGNSHilbert P) (v : ScalarGNSHilbert P)).re) :
    u = scalarPhaseVariational P z hz x :=
  phaseVariationalSolution_unique (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule z hz x u hu

/-- A bound on the vector; no bounded multiplication is claimed. -/
theorem scalarPhaseVariational_bound (P : SiteProfile) (z : ℂ) (hz : 0 < z.re)
    (x : ScalarGNSHilbert P) : z.re * ‖scalarPhaseVariational P z hz x‖ ≤ ‖x‖ :=
  phaseVariationalSolution_bound (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule z hz x

theorem scalarPhaseVariational_unit_real_bound (P : SiteProfile) (z : ℂ) (hz : z.re = 1)
    (x : ScalarGNSHilbert P) :
    ‖scalarPhaseVariational P z (by rw [hz]; norm_num) x‖ ≤ ‖x‖ :=
  phaseVariationalSolution_unit_real_bound (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule z hz x

theorem scalarPhaseVariational_one (P : SiteProfile) (x : ScalarGNSHilbert P) :
    scalarPhaseVariational P 1 (by norm_num) x =
      (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule.orthogonalProjectionOnto x :=
  phaseVariationalSolution_one (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule x

private theorem fixedPairReal {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (x v : H) (h : inner ℂ v x = inner ℂ x v) : (inner ℂ x v).im = 0 := by
  have hc := congrArg Complex.im ((inner_conj_symm (𝕜 := ℂ) v x).trans h)
  change -(inner ℂ x v).im = (inner ℂ x v).im at hc
  linarith

private theorem realPairComplexIdentity (a b z : ℂ) (ha : a.im = 0)
    (h : a.re = (z*b).re) : 2*a = z*b + (star z)*(star b) := by
  apply Complex.ext <;> simp [Complex.mul_re, Complex.mul_im, ha] at * <;> nlinarith

private theorem fixedComplexFromPairing {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (D : Submodule ℂ H) (S : D → H) (x v η : H) (z : ℂ)
    (hv : ∃ hv : v ∈ D, S ⟨v,hv⟩ = v)
    (hp : ∀ u : D, inner ℂ (S u) x = inner ℂ x (u : H))
    (he : (inner ℂ x v).re = (z * inner ℂ η v).re) :
    2 * inner ℂ x v = z * inner ℂ η v + (star z) * inner ℂ v η := by
  obtain ⟨hv,hSv⟩ := hv
  have hpv := hp ⟨v,hv⟩
  rw [hSv] at hpv
  have hr := fixedPairReal x v hpv
  have hh := realPairComplexIdentity (inner ℂ x v) (inner ℂ η v) z hr he
  have hc : star (inner ℂ η v) = inner ℂ v η := inner_conj_symm (𝕜 := ℂ) v η
  rw [hc] at hh
  exact hh

private theorem complexRelationFromDecomposition {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (x η h k u Su : H) (z : ℂ) (hu : u = h + Complex.I • k) (hSu : Su = h - Complex.I • k)
    (hh : 2 * inner ℂ x h = z * inner ℂ η h + (star z) * inner ℂ h η)
    (hk : 2 * inner ℂ x k = z * inner ℂ η k + (star z) * inner ℂ k η) :
    2 * inner ℂ x Su = z * inner ℂ η Su + (star z) * inner ℂ u η := by
  rw [hu, hSu]
  simp only [inner_sub_right, inner_add_left, inner_smul_right, inner_smul_left,
    Complex.conj_I]
  linear_combination hh - Complex.I * hk

/-- The adjoint fixed condition supplies the missing imaginary-part constraint. -/
theorem scalarPhaseVariational_fixed_complex_equation (P : SiteProfile)
    (z : ℂ) (hz : 0 < z.re) (x : scalarTomitaAdjointDomain P)
    (hx : scalarTomitaAdjoint P x = (x : ScalarGNSHilbert P))
    (v : (scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule) :
    2 * inner ℂ (x : ScalarGNSHilbert P) (v : ScalarGNSHilbert P) =
      z * inner ℂ (scalarPhaseVariational P z hz x : ScalarGNSHilbert P) (v : ScalarGNSHilbert P) +
      (star z) * inner ℂ (v : ScalarGNSHilbert P) (scalarPhaseVariational P z hz x : ScalarGNSHilbert P) := by
  refine fixedComplexFromPairing (scalarClosedTomitaDomain P) (fun u => scalarClosedTomita P u)
    (x : ScalarGNSHilbert P) (v : ScalarGNSHilbert P)
    (scalarPhaseVariational P z hz x : ScalarGNSHilbert P) z ?_ ?_ ?_
  · exact v.property
  · intro u
    exact (scalarTomitaAdjoint_pairing P x u).trans
      (congrArg (fun w : ScalarGNSHilbert P => inner ℂ w (u : ScalarGNSHilbert P)) hx)
  · exact scalarPhaseVariational_equation P z hz x v

private theorem graphEquationFromFixed {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (K : Set H) (x η u Su : H) (z : ℂ)
    (hd : ∃ h k : H, h ∈ K ∧ k ∈ K ∧ u = h + Complex.I • k ∧ Su = h - Complex.I • k)
    (hf : ∀ v ∈ K, 2 * inner ℂ x v = z * inner ℂ η v + (star z) * inner ℂ v η) :
    2 * inner ℂ x Su = z * inner ℂ η Su + (star z) * inner ℂ u η := by
  obtain ⟨h,k,hh,hk,hu,hSu⟩ := hd
  exact complexRelationFromDecomposition x η h k u Su z hu hSu (hf h hh) (hf k hk)

/-- The variational identity now holds on the whole original domain of S. -/
theorem scalarPhaseVariational_graph_equation (P : SiteProfile)
    (z : ℂ) (hz : 0 < z.re) (x : scalarTomitaAdjointDomain P)
    (hx : scalarTomitaAdjoint P x = (x : ScalarGNSHilbert P))
    (u : scalarClosedTomitaDomain P) :
    2 * inner ℂ (x : ScalarGNSHilbert P) (scalarClosedTomita P u) =
      z * inner ℂ (scalarPhaseVariational P z hz x : ScalarGNSHilbert P) (scalarClosedTomita P u) +
      (star z) * inner ℂ (u : ScalarGNSHilbert P) (scalarPhaseVariational P z hz x : ScalarGNSHilbert P) := by
  refine graphEquationFromFixed
    ((scalarTomitaStandardSubspace P).toClosedSubmodule.toSubmodule : Set (ScalarGNSHilbert P))
    (x : ScalarGNSHilbert P) (scalarPhaseVariational P z hz x : ScalarGNSHilbert P)
    (u : ScalarGNSHilbert P) (scalarClosedTomita P u) z ?_ ?_
  · exact scalarClosedTomita_fixed_decomposition P u
  · intro v hv
    exact scalarPhaseVariational_fixed_complex_equation P z hz x hx ⟨v,hv⟩

#print axioms scalarPhaseVariational
#print axioms scalarPhaseVariational_fixed
#print axioms scalarPhaseVariational_equation
#print axioms scalarPhaseVariational_unique
#print axioms scalarPhaseVariational_bound
#print axioms scalarPhaseVariational_unit_real_bound
#print axioms scalarPhaseVariational_one
#print axioms scalarPhaseVariational_fixed_complex_equation
#print axioms scalarPhaseVariational_graph_equation
end
end TGLV350.Regular
