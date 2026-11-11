import TGLExt.ThermodynamicFriedmann

set_option autoImplicit false

/-!
# Total-factor versus sector closure (Order 012, B4)

The nonnegative difference is an enthalpy difference. The difference of Hdot
has the additional negative factor -4*pi*G. Equality is determined by the
support of density, including vacuum sectors. No cosmological route is chosen.
-/

namespace ChatgptAudit.FLRW
open TGLExt
open scoped BigOperators
noncomputable section
variable {ι : Type*} [Fintype ι] {I : Set ℝ} {H : ℝ → ℝ}

namespace SectorFluid

def secondMoment (F : SectorFluid ι I H) (t : ℝ) : ℝ :=
  ∑ i, (1+F.w i)^2*F.rho i t
def sectorVariance (F : SectorFluid ι I H) (t : ℝ) : ℝ :=
  F.secondMoment t-(F.enthalpy t)^2/F.totalRho t
def fluxFactor (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) : ℝ :=
  1+c.beta*F.secondMoment t/F.enthalpy t

theorem corrected_enthalpy (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ) :
    F.correctedTotalRho c t+F.correctedTotalPressure c t =
      F.enthalpy t+c.beta*F.secondMoment t := by
  unfold correctedTotalRho correctedTotalPressure enthalpy secondMoment
  simp only [Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  dsimp [correctedRho]
  ring

theorem centered_variance (F : SectorFluid ι I H) (t : ℝ) (hr : F.totalRho t ≠ 0) :
    F.sectorVariance t = ∑ i, F.rho i t*((1+F.w i)-F.enthalpy t/F.totalRho t)^2 := by
  symm
  calc
    _ = F.secondMoment t-2*(F.enthalpy t/F.totalRho t)*F.enthalpy t+
        (F.enthalpy t/F.totalRho t)^2*F.totalRho t := by
      unfold secondMoment enthalpy totalRho
      simp only [Finset.mul_sum, ← Finset.sum_sub_distrib,
        ← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro i _
      ring
    _ = _ := by unfold sectorVariance; field_simp; ring

theorem sector_variance_nonneg (F : SectorFluid ι I H) (t : ℝ) (ht : t∈I)
    (hr : F.totalRho t ≠ 0) : 0 ≤ F.sectorVariance t := by
  rw [F.centered_variance t hr]
  exact Finset.sum_nonneg (fun i _ => mul_nonneg (F.rho_nonneg i t ht) (sq_nonneg _))

/-- Equality uses the density support; zero enthalpy does not remove a vacuum density. -/
theorem sector_variance_zero_iff (F : SectorFluid ι I H) (t : ℝ) (ht : t∈I)
    (hr : F.totalRho t ≠ 0) :
    F.sectorVariance t = 0 ↔ ∃ commonW : ℝ, ∀ i, 0 < F.rho i t → F.w i = commonW := by
  rw [F.centered_variance t hr]
  rw [Finset.sum_eq_zero_iff_of_nonneg
    (fun i _ => mul_nonneg (F.rho_nonneg i t ht) (sq_nonneg _))]
  constructor
  · intro hz
    refine ⟨F.enthalpy t/F.totalRho t-1, fun i hi => ?_⟩
    have hs := (mul_eq_zero.mp (hz i (Finset.mem_univ i))).resolve_left hi.ne'
    have he := sq_eq_zero_iff.mp hs
    linarith
  · rintro ⟨w,hw⟩
    have hm : F.enthalpy t = (1+w)*F.totalRho t := by
      unfold enthalpy totalRho
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i _
      by_cases hi : 0 < F.rho i t
      · rw [hw i hi]
      · have hz : F.rho i t = 0 := le_antisymm (le_of_not_gt hi) (F.rho_nonneg i t ht)
        simp [hz]
    intro i _
    by_cases hi : 0 < F.rho i t
    · rw [hw i hi, hm]
      field_simp
      ring
    · have hz : F.rho i t = 0 := le_antisymm (le_of_not_gt hi) (F.rho_nonneg i t ht)
      simp [hz]

end SectorFluid

/-- The sign here belongs to the source; Hdot has a negative gravitational prefactor. -/
theorem the_two_routes_differ (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (ht : t∈I) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    (F.correctedTotalRho c t+F.correctedTotalPressure c t)-
      entropyFactor c (F.wEff t)*F.enthalpy t = c.beta*F.sectorVariance t ∧
    0 ≤ c.beta*F.sectorVariance t := by
  have hw : |1+F.wEff t| = F.enthalpy t/F.totalRho t := by
    apply (eq_div_iff hr.ne').mpr
    nlinarith [F.effective_enthalpy t hr he]
  constructor
  · rw [F.corrected_enthalpy]
    unfold entropyFactor SectorFluid.sectorVariance
    rw [hw]
    ring
  · exact mul_nonneg c.beta_pos.le (F.sector_variance_nonneg t ht hr.ne')

theorem the_two_routes_equal_iff (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (ht : t∈I) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    F.correctedTotalRho c t+F.correctedTotalPressure c t =
      entropyFactor c (F.wEff t)*F.enthalpy t ↔
      ∃ commonW : ℝ, ∀ i, 0 < F.rho i t → F.w i = commonW := by
  rw [← F.sector_variance_zero_iff t ht hr.ne']
  have h := (the_two_routes_differ F c t ht hr he).1
  constructor
  · intro hz
    have hm : c.beta*F.sectorVariance t = 0 := by rw [hz] at h; linarith
    exact (mul_eq_zero.mp hm).resolve_left c.beta_pos.ne'
  · intro hz
    rw [hz] at h
    linarith

theorem the_two_hubble_rates_differ (F : SectorFluid ι I H) (c : TGLCoupling)
    (t G : ℝ) (ht : t∈I) (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    (-4*Real.pi*G*(F.correctedTotalRho c t+F.correctedTotalPressure c t))-
      (-4*Real.pi*G*entropyFactor c (F.wEff t)*F.enthalpy t) =
      -4*Real.pi*G*c.beta*F.sectorVariance t := by
  have h := (the_two_routes_differ F c t ht hr he).1
  linear_combination (-4*Real.pi*G)*h

theorem the_entropy_factor_that_reproduces_the_sector_closure
    (F : SectorFluid ι I H) (c : TGLCoupling) (t : ℝ)
    (he : F.enthalpy t ≠ 0) (factor : ℝ) :
    factor*F.enthalpy t = F.correctedTotalRho c t+F.correctedTotalPressure c t ↔
      factor = F.fluxFactor c t := by
  rw [F.corrected_enthalpy]
  unfold SectorFluid.fluxFactor
  field_simp

/-- The factor identity is consumed by the actual Clausius-to-Hdot theorem. -/
theorem sector_clausius_matches_closed_rate (F : SectorFluid ι I H)
    (c : TGLCoupling) (t G : ℝ) (he : F.enthalpy t ≠ 0)
    (D : HubbleHorizonInput H t G (F.fluxFactor c t) (F.enthalpy t)) :
    deriv H t = -4*Real.pi*G*
      (F.correctedTotalRho c t+F.correctedTotalPressure c t) := by
  rw [tgl_second_friedmann_from_clausius H t G _ _ D, mul_assoc]
  rw [(the_entropy_factor_that_reproduces_the_sector_closure F c t he _).mpr rfl]

theorem common_w_flux_factor (F : SectorFluid ι I H) (c : TGLCoupling) (t w : ℝ)
    (ht : t∈I) (he : F.enthalpy t ≠ 0)
    (hw : ∀ i, 0 < F.rho i t → F.w i = w) (hn : 0 ≤ 1+w) :
    F.fluxFactor c t = entropyFactor c w := by
  have hm : F.secondMoment t = (1+w)*F.enthalpy t := by
    unfold SectorFluid.secondMoment SectorFluid.enthalpy
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    by_cases hi : 0 < F.rho i t
    · rw [hw i hi]; ring
    · have hz := le_antisymm (le_of_not_gt hi) (F.rho_nonneg i t ht)
      simp [hz]
  unfold SectorFluid.fluxFactor entropyFactor
  rw [hm, abs_of_nonneg hn]
  field_simp

/-- At zero total enthalpy, matching cannot uniquely select a scalar factor. -/
theorem zero_flux_has_no_unique_factor (F : SectorFluid ι I H) (c : TGLCoupling)
    (t : ℝ) (he : F.enthalpy t = 0) :
    ¬ ∃! factor : ℝ, factor*F.enthalpy t =
      F.correctedTotalRho c t+F.correctedTotalPressure c t := by
  rintro ⟨factor,hf,hu⟩
  have ha : (factor+1)*F.enthalpy t =
      F.correctedTotalRho c t+F.correctedTotalPressure c t := by simpa [he] using hf
  have h := hu (factor+1) ha
  linarith

/-- Positive matter and vacuum have a positive variance despite only matter carrying flux.
    This refutes replacing density support by nonzero-enthalpy support. -/
theorem matter_vacuum_variance (rhoM rhoL : ℝ) (hm : 0 < rhoM) (hl : 0 < rhoL) :
    rhoM-rhoM^2/(rhoM+rhoL) = rhoM*rhoL/(rhoM+rhoL) ∧
    0 < rhoM-rhoM^2/(rhoM+rhoL) := by
  have hs : 0 < rhoM+rhoL := add_pos hm hl
  have h : rhoM-rhoM^2/(rhoM+rhoL) = rhoM*rhoL/(rhoM+rhoL) := by
    field_simp
    ring
  exact ⟨h, h ▸ div_pos (mul_pos hm hl) hs⟩

/-- An actual finite family satisfies the proposed nonzero-flux support condition
    while its density-weighted variance is strictly positive. -/
theorem nonzero_flux_support_does_not_characterize_equality
    (rhoM rhoL : ℝ) (hm : 0 < rhoM) (hl : 0 < rhoL) :
    ∃ rho w : Fin 2 → ℝ,
      (∀ i, 0 < rho i) ∧
      (∀ i j, (1+w i)*rho i ≠ 0 → (1+w j)*rho j ≠ 0 → w i = w j) ∧
      0 < (∑ i, (1+w i)^2*rho i)-(∑ i, (1+w i)*rho i)^2/(∑ i, rho i) := by
  refine ⟨![rhoM,rhoL],![0,-1],?_,?_,?_⟩
  · intro i; fin_cases i <;> assumption
  · intro i j hi hj
    fin_cases i <;> fin_cases j <;> norm_num at *
  · simpa [Fin.sum_univ_two] using (matter_vacuum_variance rhoM rhoL hm hl).2

end
end ChatgptAudit.FLRW
