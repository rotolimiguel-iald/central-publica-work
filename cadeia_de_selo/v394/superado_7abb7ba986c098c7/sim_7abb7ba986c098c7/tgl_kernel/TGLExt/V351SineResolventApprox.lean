import TGLExt.V351ScalarRightActionAlgebra
import TGLExt.V351RegularImaginaryPowers
import TGLExt.V351RegularGeneratorAffiliation
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Sinc
import Mathlib.Analysis.SpecificLimits.Basic

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory Filter
open scoped Topology
noncomputable section

private def sineWindow (m x : ℝ) : ℝ := (1+Real.sin (2*Real.pi*x/m))/2
private theorem sineWindow_continuous (m : ℝ) : Continuous (sineWindow m) := by
  unfold sineWindow
  fun_prop
private theorem sineWindow_nonneg (m x : ℝ) : 0 ≤ sineWindow m x := by
  unfold sineWindow
  linarith [Real.neg_one_le_sin (2*Real.pi*x/m)]
private theorem sineWindow_le_one (m x : ℝ) : sineWindow m x ≤ 1 := by
  unfold sineWindow
  linarith [Real.sin_le_one (2*Real.pi*x/m)]

/-- An explicit bounded combination of the original regular translations. -/
def regularSineWindowCore (P : SiteProfile) (m : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra :=
  (1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
    (regularRightCoreElement P (-1/m) - regularRightCoreElement P (1/m))

theorem regularSineWindowCore_right (P : SiteProfile) (m : ℝ) :
    regularSineWindowCore P m ∈ scalarPolarRightAlgebra P := by
  apply (scalarPolarRightAlgebra P).add_mem
  · exact (scalarPolarRightAlgebra P).smul_mem (scalarPolarRightAlgebra P).one_mem _
  · exact (scalarPolarRightAlgebra P).smul_mem ((scalarPolarRightAlgebra P).sub_mem
      (scalarPolarRightAlgebra_regular_mem P (-1/m))
      (scalarPolarRightAlgebra_regular_mem P (1/m))) _

private theorem sineWindow_character (m x : ℝ) :
    (1/2 : ℂ) + (1/(4*Complex.I) : ℂ) *
      (characterPhase (2*Real.pi*(-1/m)) x - characterPhase (2*Real.pi*(1/m)) x) =
      (sineWindow m x : ℂ) := by
  have hminus : -Complex.I * ((2*Real.pi*(-1/m) : ℝ) : ℂ) * (x : ℂ) =
      ((2*Real.pi*x/m : ℝ) : ℂ) * Complex.I := by push_cast; ring
  have hplus : -Complex.I * ((2*Real.pi*(1/m) : ℝ) : ℂ) * (x : ℂ) =
      (-((2*Real.pi*x/m : ℝ) : ℂ)) * Complex.I := by push_cast; ring
  simp only [characterPhase, hminus, hplus, Complex.exp_mul_I,
    Complex.cos_neg, Complex.sin_neg, sineWindow, Complex.ofReal_div,
    Complex.ofReal_add, Complex.ofReal_one, Complex.ofReal_ofNat,
    Complex.ofReal_sin]
  field_simp
  ring

private theorem sineWindow_multiplier
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] (m : ℝ) :
    realScalarMultiplier (H := H) (sineWindow m) (sineWindow_continuous m)
      (sineWindow_nonneg m) (sineWindow_le_one m) =
    (1/2 : ℂ) • 1 + (1/(4*Complex.I) : ℂ) •
      (characterMultiplier (2*Real.pi*(-1/m)) - characterMultiplier (2*Real.pi*(1/m))) := by
  ext1 u
  apply Lp.ext
  let a := characterMultiplier (H := H) (2*Real.pi*(-1/m)) u
  let b := characterMultiplier (H := H) (2*Real.pi*(1/m)) u
  filter_upwards [realScalarMultiplier_ae (sineWindow m) (sineWindow_continuous m)
      (sineWindow_nonneg m) (sineWindow_le_one m) u,
    characterMultiplier_ae (2*Real.pi*(-1/m)) u,
    characterMultiplier_ae (2*Real.pi*(1/m)) u,
    Lp.coeFn_add ((1/2 : ℂ) • u) ((1/(4*Complex.I) : ℂ) • (a-b)),
    Lp.coeFn_smul (1/2 : ℂ) u,
    Lp.coeFn_smul (1/(4*Complex.I) : ℂ) (a-b),
    Lp.coeFn_sub a b] with x hx ha hb hab hsu hsab hsub
  change _ = ((1/2 : ℂ) • u + (1/(4*Complex.I) : ℂ) • (a-b)) x
  simp only [hx, hab, Pi.add_apply, hsu, hsab, Pi.smul_apply, hsub, Pi.sub_apply]
  change (sineWindow m x : ℂ) • u x =
    (1/2 : ℂ) • u x + (1/(4*Complex.I) : ℂ) • (a x-b x)
  have hae : a x = characterPhase (2*Real.pi*(-1/m)) x • u x := ha
  have hbe : b x = characterPhase (2*Real.pi*(1/m)) x • u x := hb
  rw [hae,hbe, ← sub_smul,smul_smul, ← add_smul,sineWindow_character]

theorem regularSineWindowCore_spectral (P : SiteProfile) (m : ℝ) :
    (regularSineWindowCore P m).val =
      (regularSpectralCoordinates P).conjStarAlgEquiv
        (realScalarMultiplier (sineWindow m) (sineWindow_continuous m)
          (sineWindow_nonneg m) (sineWindow_le_one m)) := by
  have h (t : ℝ) : (regularSpectralCoordinates P).conjStarAlgEquiv
      (characterMultiplier (2*Real.pi*t)) = regularUnitary P t := by
    ext1 u
    exact (regularSpectralCoordinates_character P t ((regularSpectralCoordinates P).symm u)).trans
      (congrArg (regularUnitary P t) ((regularSpectralCoordinates P).apply_symm_apply u))
  rw [sineWindow_multiplier,map_add,map_smul,map_one,map_smul,map_sub,h,h]
  rfl

/-- Spectral approximants, subsequently identified with CFC of the actual
regular translation combinations. No new logarithm or unbounded operator. -/
def regularSineResolvent (P : SiteProfile) (m : ℝ) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) :=
  (regularSpectralCoordinates P).conjStarAlgEquiv
    (realScalarMultiplier (fun x => Real.sigmoid (m*Real.sin (2*Real.pi*x/m)))
      (by fun_prop) (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _))

theorem regularSineResolvent_cfc (P : SiteProfile) (m : ℝ) :
    regularSineResolvent P m =
      cfc (fun z : ℂ => (Real.sigmoid (m*(2*z.re-1)) : ℂ))
        (regularSineWindowCore P m).val := by
  let f : ℂ → ℂ := fun z => (Real.sigmoid (m*(2*z.re-1)) : ℂ)
  have hf : Continuous f := by fun_prop
  let M := realScalarMultiplier (H := TowerHilbert P) (sineWindow m)
    (sineWindow_continuous m) (sineWindow_nonneg m) (sineWindow_le_one m)
  have hM0 : 0 ≤ M := realScalarMultiplier_nonneg _ _ _ _
  have he : cfc f M =
      realScalarMultiplier (H := TowerHilbert P)
        (fun x => Real.sigmoid (m*Real.sin (2*Real.pi*x/m)))
        (by fun_prop) (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _) := by
    ext1 u
    apply Lp.ext
    filter_upwards [realScalarMultiplier_cfc_ae (sineWindow m) (sineWindow_continuous m)
        (sineWindow_nonneg m) (sineWindow_le_one m) f hf u,
      realScalarMultiplier_ae (fun x => Real.sigmoid (m*Real.sin (2*Real.pi*x/m)))
        (by fun_prop) (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _) u]
      with x hx hy
    rw [hx,hy]
    congr 2
    simp only [f,Complex.ofReal_re,sineWindow]
    congr 2
    ring
  rw [regularSineWindowCore_spectral]
  have hc := StarAlgHomClass.map_cfc (regularSpectralCoordinates P).conjStarAlgEquiv f M
    hf.continuousOn (StarAlgEquiv.isometry (regularSpectralCoordinates P).conjStarAlgEquiv).continuous
    (IsSelfAdjoint.of_nonneg hM0).isStarNormal
    (IsSelfAdjoint.of_nonneg (map_nonneg (regularSpectralCoordinates P).conjStarAlgEquiv hM0)).isStarNormal
  change _ = cfc f ((regularSpectralCoordinates P).conjStarAlgEquiv M)
  rw [← hc,he]
  rfl

theorem regularSineResolvent_right (P : SiteProfile) (m : ℝ) :
    ∃ h : regularSineResolvent P m ∈ regularCoreAlgebra P,
      (⟨regularSineResolvent P m,h⟩ : (regularCoreAlgebra P).toStarSubalgebra) ∈
        scalarPolarRightAlgebra P := by
  rw [regularSineResolvent_cfc]
  exact scalarRightAction_cfc P (regularSineWindowCore P m)
    (regularSineWindowCore_right P m) _

theorem sine_rescaled_tendsto (x : ℝ) :
    Tendsto (fun n : ℕ => ((n : ℝ)+1)*Real.sin (x/((n : ℝ)+1))) atTop (𝓝 x) := by
  have hz : Tendsto (fun n : ℕ => x/((n : ℝ)+1)) atTop (𝓝 (0 : ℝ)) := by
    simpa only [mul_zero,mul_one_div] using
      tendsto_const_nhds.mul (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))
  have he (n : ℕ) : ((n : ℝ)+1)*Real.sin (x/((n : ℝ)+1)) =
      x*Real.sinc (x/((n : ℝ)+1)) := by
    by_cases hx : x=0
    · simp [hx]
    · have hm : (n : ℝ)+1 ≠ 0 := by positivity
      rw [Real.sinc_of_ne_zero (div_ne_zero hx hm)]
      field_simp
  simp_rw [he]
  simpa only [Function.comp_def,Real.sinc_zero,mul_one] using
    tendsto_const_nhds.mul (Real.continuous_sinc.continuousAt.tendsto.comp hz)

private theorem scalarMultiplier_sequence_tendsto
    {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (g : ℕ → ℝ → ℝ) (g0 : ℝ → ℝ) (hg : ∀ n, Continuous (g n)) (hg0 : Continuous g0)
    (hlo : ∀ n x, 0 ≤ g n x) (hhi : ∀ n x, g n x ≤ 1)
    (hlo0 : ∀ x, 0 ≤ g0 x) (hhi0 : ∀ x, g0 x ≤ 1)
    (ht : ∀ x, Tendsto (fun n => g n x) atTop (𝓝 (g0 x))) (u : RegularHilbert H) :
    Tendsto (fun n => realScalarMultiplier (g n) (hg n) (hlo n) (hhi n) u) atTop
      (𝓝 (realScalarMultiplier g0 hg0 hlo0 hhi0 u)) := by
  let M (n : ℕ) := realScalarMultiplier (H := H) (g n) (hg n) (hlo n) (hhi n)
  let M0 := realScalarMultiplier (H := H) g0 hg0 hlo0 hhi0
  let phi (n : ℕ) (x : ℝ) := (g n x-g0 x)^2 * ‖u x‖^2
  have hI : Tendsto (fun n => ∫ x : ℝ, phi n x) atTop (𝓝 (∫ _x : ℝ, (0 : ℝ))) := by
    apply tendsto_integral_of_dominated_convergence (fun x : ℝ => ‖u x‖^2)
    · intro n
      exact (((hg n).sub hg0).pow 2).aestronglyMeasurable.mul
        ((Lp.aestronglyMeasurable u).norm.pow 2)
    · exact (memLp_two_iff_integrable_sq_norm (Lp.aestronglyMeasurable u)).mp (Lp.memLp u)
    · intro n
      exact Eventually.of_forall fun x => by
        have ha : |g n x-g0 x| ≤ 1 := abs_le.mpr ⟨by linarith [hlo n x,hhi0 x],by linarith [hhi n x,hlo0 x]⟩
        have hsq : (g n x-g0 x)^2 ≤ 1 := by
          simpa only [sq_abs,one_pow] using pow_le_pow_left₀ (abs_nonneg _) ha 2
        change ‖(g n x-g0 x)^2 * ‖u x‖^2‖ ≤ _
        rw [Real.norm_eq_abs,abs_of_nonneg (mul_nonneg (sq_nonneg _) (sq_nonneg _))]
        simpa only [one_mul] using mul_le_mul_of_nonneg_right hsq (sq_nonneg ‖u x‖)
    · exact Eventually.of_forall fun x => by
        simpa only [phi,sub_self,zero_pow (by decide : (2 : ℕ) ≠ 0),zero_mul]
          using (((ht x).sub (tendsto_const_nhds (x := g0 x))).pow 2).mul_const (‖u x‖^2)
  have he (n : ℕ) : ‖M n u-M0 u‖^2 = ∫ x : ℝ, phi n x := by
    rw [← TGLV350.Fourier.L2_integral_norm_sq]
    apply integral_congr_ae
    filter_upwards [Lp.coeFn_sub (M n u) (M0 u),
      realScalarMultiplier_ae (g n) (hg n) (hlo n) (hhi n) u,
      realScalarMultiplier_ae g0 hg0 hlo0 hhi0 u] with x hs hn hz
    change ‖(M n u-M0 u) x‖^2 = _
    simp only [hs,Pi.sub_apply]
    rw [hn,hz, ← sub_smul, ← Complex.ofReal_sub,norm_smul,Complex.norm_real,
      Real.norm_eq_abs,mul_pow,sq_abs]
  have hn := Real.continuous_sqrt.continuousAt.tendsto.comp
    (show Tendsto (fun n => ‖M n u-M0 u‖^2) atTop (𝓝 (0 : ℝ)) by
      simpa only [he,integral_zero] using hI)
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [Function.comp_def,Real.sqrt_sq_eq_abs,abs_norm,Real.sqrt_zero,dist_eq_norm] using hn

theorem regularSineResolvent_nonneg (P : SiteProfile) (m : ℝ) :
    0 ≤ regularSineResolvent P m :=
  map_nonneg (regularSpectralCoordinates P).conjStarAlgEquiv
    (realScalarMultiplier_nonneg _ _ _ _)

theorem regularSineResolvent_norm_le (P : SiteProfile) (m : ℝ) :
    ‖regularSineResolvent P m‖ ≤ 1 := by
  unfold regularSineResolvent
  rw [StarAlgEquiv.norm_map]
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro u
  simpa only [one_mul] using realScalarMultiplier_norm_le
    (H := TowerHilbert P) _ _ _ _ u

theorem regularSineResolvent_tendsto (P : SiteProfile) (u : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => regularSineResolvent P ((n : ℝ)+1) u) atTop
      (𝓝 (regularSpectralResolvent P u)) := by
  have ht := scalarMultiplier_sequence_tendsto
    (fun n x => Real.sigmoid (((n : ℝ)+1)*Real.sin (2*Real.pi*x/((n : ℝ)+1))))
    (fun x => Real.sigmoid (2*Real.pi*x))
    (fun n => by fun_prop) (by fun_prop)
    (fun n x => Real.sigmoid_nonneg _) (fun n x => Real.sigmoid_le_one _)
    (fun x => Real.sigmoid_nonneg _) (fun x => Real.sigmoid_le_one _)
    (fun x => (show Continuous Real.sigmoid by fun_prop).continuousAt.tendsto.comp
      (sine_rescaled_tendsto (2*Real.pi*x)))
    ((regularSpectralCoordinates P).symm u)
  exact (regularSpectralCoordinates P).continuous.continuousAt.tendsto.comp ht

theorem regularSpectralResolvent_right (P : SiteProfile) :
    (⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P := by
  let b (n : ℕ) : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨regularSineResolvent P ((n : ℝ)+1),(regularSineResolvent_right P ((n : ℝ)+1)).choose⟩
  let B : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩
  have hb (n : ℕ) : b n ∈ scalarPolarRightAlgebra P :=
    (regularSineResolvent_right P ((n : ℝ)+1)).choose_spec
  have hs (n : ℕ) : star (b n) = b n :=
    Subtype.ext (IsSelfAdjoint.of_nonneg (regularSineResolvent_nonneg P ((n : ℝ)+1))).star_eq
  have hB : star B = B :=
    Subtype.ext (IsSelfAdjoint.of_nonneg (regularSpectralResolvent_nonneg P)).star_eq
  have hright : ScalarPolarRight P B := by
    intro A
    have ha : ∀ x, Tendsto (fun n => (star (b n)).val x) atTop (𝓝 ((star B).val x)) := by
      intro x
      simpa only [hs,hB] using regularSineResolvent_tendsto P x
    exact scalarRightAction_closed_of_bounded_strongStar P b B 1
      (fun n => regularSineResolvent_norm_le P ((n : ℝ)+1))
      (fun x => regularSineResolvent_tendsto P x) ha A (fun n => (hb n).1 A)
  change ScalarPolarRight P B ∧ ScalarPolarRight P (star B)
  rw [hB]
  exact ⟨hright,hright⟩


#print axioms regularSineWindowCore
#print axioms regularSineWindowCore_right
#print axioms regularSineWindowCore_spectral
#print axioms regularSineResolvent
#print axioms regularSineResolvent_cfc
#print axioms regularSineResolvent_right
#print axioms sine_rescaled_tendsto
#print axioms regularSineResolvent_nonneg
#print axioms regularSineResolvent_norm_le
#print axioms regularSineResolvent_tendsto
#print axioms regularSpectralResolvent_right
end
end TGLV350.Regular
