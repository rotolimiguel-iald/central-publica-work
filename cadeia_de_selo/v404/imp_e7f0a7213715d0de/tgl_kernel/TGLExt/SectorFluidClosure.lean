import TGLExt.TheSameBetaReadsThreeFaces
import TGLExt.FLRWFieldEquations

set_option autoImplicit false

/-!
# Conserved finite fluid sectors (Order 012, B3)

H_sector_nonexchange is the explicitly supplied non-exchange law. Equation-of-state scalars
are constant in time. The metric equation and the horizon null balance are
not fields of SectorFluid. No cosmological integration constant is discarded.
Consumers: tgl_friedmann_from_sector_closure and the B4 comparison of routes.
-/

namespace ChatgptAudit.FLRW

open TGLExt
open scoped BigOperators ContDiff

structure SectorFluid (ι : Type*) [Fintype ι] (I : Set ℝ) (H : ℝ → ℝ) where
  rho : ι → ℝ → ℝ
  w : ι → ℝ
  rho_nonneg : ∀ i t, t ∈ I → 0 ≤ rho i t
  H_sector_nonexchange : ∀ i t, t ∈ I → HasDerivAt (rho i) (-3*H t*(1+w i)*rho i t) t

namespace SectorFluid

noncomputable section

variable {ι : Type*} [Fintype ι] {I : Set ℝ} {H : ℝ → ℝ}

def totalRho (F : SectorFluid ι I H) (t : ℝ) : ℝ := ∑ i, F.rho i t
def totalPressure (F : SectorFluid ι I H) (t : ℝ) : ℝ := ∑ i, F.w i*F.rho i t
def enthalpy (F : SectorFluid ι I H) (t : ℝ) : ℝ := ∑ i, (1+F.w i)*F.rho i t
def wEff (F : SectorFluid ι I H) (t : ℝ) : ℝ := F.totalPressure t/F.totalRho t
def correctedRho (F : SectorFluid ι I H) (c : TGLCoupling) (i : ι) (t : ℝ) : ℝ :=
  (1+c.beta*(1+F.w i))*F.rho i t
def correctedTotalRho (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) : ℝ :=
  ∑ i, F.correctedRho c i t
def correctedTotalPressure (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) : ℝ :=
  ∑ i, F.w i*F.correctedRho c i t

theorem enthalpy_eq (F : SectorFluid ι I H) (t : ℝ) :
    F.enthalpy t = F.totalRho t+F.totalPressure t := by
  simp [enthalpy, totalRho, totalPressure, add_mul, Finset.sum_add_distrib]

/-- Constant rescaling of the supplied non-exchange law, with the same w. -/
theorem sector_rescaling_preserves_continuity (F : SectorFluid ι I H)
    (c : TGLCoupling) (i : ι) (t : ℝ) (ht : t∈I) :
    HasDerivAt (F.correctedRho c i)
      (-3*H t*(1+F.w i)*F.correctedRho c i t) t := by
  convert! (F.H_sector_nonexchange i t ht).const_mul (1+c.beta*(1+F.w i)) using 1
  dsimp [correctedRho]
  ring

theorem corrected_closure (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) :
    F.correctedTotalRho c t = F.totalRho t+c.beta*F.enthalpy t := by
  unfold correctedTotalRho totalRho enthalpy
  simp only [Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  dsimp [correctedRho]
  ring

/-- A finite linear combination of conserved sectors is conserved. -/
theorem weighted_continuity (F : SectorFluid ι I H) (weights : ι → ℝ)
    (t : ℝ) (ht : t∈I) :
    HasDerivAt (fun u => ∑ i, weights i*F.rho i u)
      (-3*H t*((∑ i, weights i*F.rho i t)+(∑ i, F.w i*(weights i*F.rho i t)))) t := by
  have hs := HasDerivAt.fun_sum (u := Finset.univ)
    (fun i _ => (F.H_sector_nonexchange i t ht).const_mul (weights i))
  convert! hs using 1
  simp only [← Finset.sum_add_distrib, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem total_continuity (F : SectorFluid ι I H) (t : ℝ) (ht : t∈I) :
    deriv F.totalRho t+3*H t*(F.totalRho t+F.totalPressure t) = 0 := by
  have h := F.weighted_continuity (fun _ => 1) t ht
  simp only [one_mul] at h
  rw [show deriv F.totalRho t = -3*H t*(F.totalRho t+F.totalPressure t) from h.deriv]
  ring

theorem corrected_rho_deriv (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (ht : t∈I) :
    HasDerivAt (F.correctedTotalRho c)
      (-3*H t*(F.correctedTotalRho c t+F.correctedTotalPressure c t)) t :=
  F.weighted_continuity (fun i => 1+c.beta*(1+F.w i)) t ht

theorem corrected_pressure_differentiable (F : SectorFluid ι I H)
    (c : TGLCoupling) (t : ℝ) (ht : t∈I) :
    DifferentiableAt ℝ (F.correctedTotalPressure c) t := by
  exact (HasDerivAt.fun_sum (u := Finset.univ)
    (fun i _ => (F.sector_rescaling_preserves_continuity c i t ht).const_mul (F.w i))).differentiableAt

theorem corrected_continuity (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (ht : t∈I) :
    deriv (F.correctedTotalRho c) t+
      3*H t*(F.correctedTotalRho c t+F.correctedTotalPressure c t) = 0 := by
  rw [(F.corrected_rho_deriv c t ht).deriv]
  ring

/-- Total positivity and nonnegative enthalpy are the exact domain of this reading. -/
theorem effective_enthalpy (F : SectorFluid ι I H) (t : ℝ)
    (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    F.totalRho t*|1+F.wEff t| = F.enthalpy t := by
  have hw : 1+F.wEff t = F.enthalpy t/F.totalRho t := by
    rw [F.enthalpy_eq]
    unfold wEff
    field_simp
  rw [hw, abs_of_nonneg (div_nonneg he hr.le)]
  field_simp

theorem multiplicative_closure (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    F.correctedTotalRho c t = F.totalRho t*(1+c.beta*|1+F.wEff t|) := by
  rw [F.corrected_closure, ← F.effective_enthalpy t hr he]
  ring

/-- The original three-sector providers remain the algebraic source of this specialization. -/
theorem three_sector_closure (c : TGLCoupling) (rhoR rhoM rhoL : ℝ) :
    (rhoR+rhoM+rhoL)+c.beta*((rhoR+rhoR/3)+(rhoM+0)+(rhoL+(-rhoL))) =
      (1+4*c.beta/3)*rhoR+(1+c.beta)*rhoM+rhoL := by
  rw [TGLExt.closure_identity c.beta rhoR rhoM rhoL]
  exact TGLExt.hubble_form c.beta rhoR rhoM rhoL

end
end SectorFluid
end ChatgptAudit.FLRW
