import Mathlib.MeasureTheory.Function.Holder
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.MeasureTheory.Measure.Haar.Unique
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-! Concrete bounded multipliers on Lebesgue L².
No identification with a spacetime action or a functional-calculus modular phase is assumed. -/

noncomputable section
open MeasureTheory Filter
open scoped ENNReal ComplexConjugate

namespace ChatgptAudit.Continuous049

abbrev SpectralHilbert := Lp ℂ 2 (volume : Measure ℝ)

/-- The positive bounded graph coordinate. -/
def spectralWeightA (c x : ℝ) : ℝ :=
  Real.exp (c * x / 2) / Real.sqrt (Real.exp (c * x) + Real.exp (-c * x))

/-- The second bounded graph coordinate. -/
def spectralWeightB (c x : ℝ) : ℝ :=
  Real.exp (-c * x / 2) / Real.sqrt (Real.exp (c * x) + Real.exp (-c * x))

theorem spectral_weight_den_pos (c x : ℝ) :
    0 < Real.sqrt (Real.exp (c * x) + Real.exp (-c * x)) :=
  Real.sqrt_pos.2 (add_pos (Real.exp_pos _) (Real.exp_pos _))

theorem spectral_weightA_pos (c x : ℝ) : 0 < spectralWeightA c x :=
  div_pos (Real.exp_pos _) (spectral_weight_den_pos c x)

theorem spectral_weightB_pos (c x : ℝ) : 0 < spectralWeightB c x :=
  div_pos (Real.exp_pos _) (spectral_weight_den_pos c x)

theorem spectral_weight_square_sum (c x : ℝ) :
    spectralWeightA c x ^ 2 + spectralWeightB c x ^ 2 = 1 := by
  have ha : Real.exp (c * x / 2) ^ 2 = Real.exp (c * x) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  have hb : Real.exp (-c * x / 2) ^ 2 = Real.exp (-c * x) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring
  have hd := Real.sq_sqrt (le_of_lt (add_pos (Real.exp_pos (c * x))
    (Real.exp_pos (-c * x))))
  unfold spectralWeightA spectralWeightB
  rw [div_pow, div_pow, ← add_div, ha, hb, hd]
  exact div_self (ne_of_gt (add_pos (Real.exp_pos _) (Real.exp_pos _)))

theorem spectral_weightA_le_one (c x : ℝ) : spectralWeightA c x ≤ 1 := by
  have := spectral_weight_square_sum c x
  have := spectral_weightA_pos c x
  nlinarith [sq_nonneg (spectralWeightB c x)]

theorem spectral_weightB_le_one (c x : ℝ) : spectralWeightB c x ≤ 1 := by
  have := spectral_weight_square_sum c x
  have := spectral_weightB_pos c x
  nlinarith [sq_nonneg (spectralWeightA c x)]

theorem spectral_weightA_norm_le_one (c x : ℝ) : ‖spectralWeightA c x‖ ≤ 1 := by
  simpa only [Real.norm_eq_abs, abs_of_pos (spectral_weightA_pos c x)] using
    spectral_weightA_le_one c x

theorem spectral_weightB_norm_le_one (c x : ℝ) : ‖spectralWeightB c x‖ ≤ 1 := by
  simpa only [Real.norm_eq_abs, abs_of_pos (spectral_weightB_pos c x)] using
    spectral_weightB_le_one c x

theorem spectral_weightA_continuous (c : ℝ) : Continuous (spectralWeightA c) := by
  unfold spectralWeightA
  apply Continuous.div
  · fun_prop
  · fun_prop
  · intro x
    exact ne_of_gt (spectral_weight_den_pos c x)

theorem spectral_weightB_continuous (c : ℝ) : Continuous (spectralWeightB c) := by
  unfold spectralWeightB
  apply Continuous.div
  · fun_prop
  · fun_prop
  · intro x
    exact ne_of_gt (spectral_weight_den_pos c x)

theorem spectral_weight_reflection (c x : ℝ) :
    spectralWeightA c (-x) = spectralWeightB c x := by
  simp only [spectralWeightA, spectralWeightB, mul_neg, neg_mul, neg_neg, add_comm]

theorem spectral_weightB_reflection (c x : ℝ) :
    spectralWeightB c (-x) = spectralWeightA c x := by
  simpa only [neg_neg] using (spectral_weight_reflection c (-x)).symm

theorem spectral_weight_ratio (c x : ℝ) :
    spectralWeightB c x = Real.exp (-c * x) * spectralWeightA c x := by
  unfold spectralWeightA spectralWeightB
  rw [← mul_div_assoc, ← Real.exp_add]
  congr 2
  ring

/-- A bounded measurable weight regarded as an L∞ vector. -/
def boundedSpectralWeight (w : ℝ → ℝ) (hw : Continuous w) (hb : ∀ x, ‖w x‖ ≤ 1) :
    Lp ℂ ∞ (volume : Measure ℝ) :=
  (memLp_top_of_bound (Complex.continuous_ofReal.comp hw).aestronglyMeasurable 1
    (Eventually.of_forall fun x => by simpa only [Function.comp_apply, Complex.norm_real] using hb x)).toLp _

theorem bounded_spectral_weight_ae (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) :
    boundedSpectralWeight w hw hb =ᵐ[volume] fun x => (w x : ℂ) :=
  MemLp.coeFn_toLp _

/-- Multiplication is constructed through the L∞ × L² Hölder map. -/
def boundedSpectralMultiplier (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) : SpectralHilbert →L[ℂ] SpectralHilbert :=
  (ContinuousLinearMap.lsmul ℂ ℂ).holderL volume ∞ 2 2
    (boundedSpectralWeight w hw hb)

theorem bounded_spectral_multiplier_ae (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) (f : SpectralHilbert) :
    boundedSpectralMultiplier w hw hb f =ᵐ[volume] fun x => (w x : ℂ) * f x := by
  have h := (ContinuousLinearMap.lsmul ℂ ℂ).coeFn_holder
    (r := 2) (boundedSpectralWeight w hw hb) f
  filter_upwards [h, bounded_spectral_weight_ae w hw hb] with x hx hwx
  simpa only [boundedSpectralMultiplier, ContinuousLinearMap.holderL_apply_apply,
    ContinuousLinearMap.lsmul_apply, smul_eq_mul, hwx] using hx

theorem bounded_spectral_multiplier_norm (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) (f : SpectralHilbert) :
    ‖boundedSpectralMultiplier w hw hb f‖ ≤ ‖f‖ := by
  apply Lp.norm_le_norm_of_ae_le
  filter_upwards [bounded_spectral_multiplier_ae w hw hb f] with x hx
  rw [hx, norm_mul, Complex.norm_real]
  exact (mul_le_mul_of_nonneg_right (hb x) (norm_nonneg (f x))).trans_eq (one_mul _)

theorem bounded_spectral_multiplier_selfadjoint (w : ℝ → ℝ) (hw : Continuous w)
    (hb : ∀ x, ‖w x‖ ≤ 1) : IsSelfAdjoint (boundedSpectralMultiplier w hw hb) := by
  apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.2
  intro f g
  simp only [L2.inner_def]
  apply integral_congr_ae
  filter_upwards [bounded_spectral_multiplier_ae w hw hb f,
    bounded_spectral_multiplier_ae w hw hb g] with x hf hg
  change inner ℂ ((boundedSpectralMultiplier w hw hb f) x) (g x) =
    inner ℂ (f x) ((boundedSpectralMultiplier w hw hb g) x)
  rw [hf, hg]
  simp [RCLike.inner_apply, mul_comm, mul_left_comm]

def spectralA (c : ℝ) : SpectralHilbert →L[ℂ] SpectralHilbert :=
  boundedSpectralMultiplier (spectralWeightA c) (spectral_weightA_continuous c)
    (spectral_weightA_norm_le_one c)

def spectralB (c : ℝ) : SpectralHilbert →L[ℂ] SpectralHilbert :=
  boundedSpectralMultiplier (spectralWeightB c) (spectral_weightB_continuous c)
    (spectral_weightB_norm_le_one c)

theorem spectralA_ae (c : ℝ) (f : SpectralHilbert) :
    spectralA c f =ᵐ[volume] fun x => (spectralWeightA c x : ℂ) * f x :=
  bounded_spectral_multiplier_ae _ _ _ f

theorem spectralB_ae (c : ℝ) (f : SpectralHilbert) :
    spectralB c f =ᵐ[volume] fun x => (spectralWeightB c x : ℂ) * f x :=
  bounded_spectral_multiplier_ae _ _ _ f

theorem spectralA_norm_le (c : ℝ) (f : SpectralHilbert) : ‖spectralA c f‖ ≤ ‖f‖ :=
  bounded_spectral_multiplier_norm _ _ _ f

theorem spectralB_norm_le (c : ℝ) (f : SpectralHilbert) : ‖spectralB c f‖ ≤ ‖f‖ :=
  bounded_spectral_multiplier_norm _ _ _ f

theorem spectralA_selfadjoint (c : ℝ) : IsSelfAdjoint (spectralA c) :=
  bounded_spectral_multiplier_selfadjoint _ _ _

theorem spectralB_selfadjoint (c : ℝ) : IsSelfAdjoint (spectralB c) :=
  bounded_spectral_multiplier_selfadjoint _ _ _

theorem spectralAB_commute (c : ℝ) : spectralA c * spectralB c = spectralB c * spectralA c := by
  apply ContinuousLinearMap.ext
  intro f
  apply Lp.ext
  filter_upwards [spectralA_ae c (spectralB c f), spectralB_ae c (spectralA c f),
    spectralA_ae c f, spectralB_ae c f] with x hab hba ha hb
  change (spectralA c (spectralB c f)) x = (spectralB c (spectralA c f)) x
  rw [hab, hba, ha, hb]
  ring

theorem spectralAB_square_sum (c : ℝ) :
    spectralA c * spectralA c + spectralB c * spectralB c = 1 := by
  apply ContinuousLinearMap.ext
  intro f
  apply Lp.ext
  filter_upwards [spectralA_ae c (spectralA c f), spectralB_ae c (spectralB c f),
    spectralA_ae c f, spectralB_ae c f,
    Lp.coeFn_add (spectralA c (spectralA c f)) (spectralB c (spectralB c f))]
      with x haa hbb ha hb hadd
  change (spectralA c (spectralA c f) + spectralB c (spectralB c f)) x = f x
  rw [hadd, haa, hbb, ha, hb]
  have hs : (spectralWeightA c x : ℂ) ^ 2 + (spectralWeightB c x : ℂ) ^ 2 = 1 := by
    exact_mod_cast spectral_weight_square_sum c x
  calc
    _ = ((spectralWeightA c x : ℂ) ^ 2 + (spectralWeightB c x : ℂ) ^ 2) * f x := by ring
    _ = f x := by rw [hs, one_mul]

theorem spectralA_injective (c : ℝ) : Function.Injective (spectralA c) := by
  intro f g hfg
  apply Lp.ext
  filter_upwards [spectralA_ae c f, spectralA_ae c g] with x hf hg
  have he := congrArg (fun u : SpectralHilbert => u x) hfg
  rw [hf, hg] at he
  have hn : (spectralWeightA c x : ℂ) ≠ 0 := by
    exact_mod_cast ne_of_gt (spectral_weightA_pos c x)
  exact mul_left_cancel₀ hn he

theorem spectralAB_quadratic_nonneg (c : ℝ) (h : SpectralHilbert) :
    0 ≤ (inner ℂ (spectralA c h) (spectralB c h)).re := by
  rw [L2.inner_def]
  change 0 ≤ RCLike.re (∫ x : ℝ, inner ℂ ((spectralA c h) x) ((spectralB c h) x))
  rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) (spectralA c h) (spectralB c h))]
  apply integral_nonneg_of_ae
  filter_upwards [spectralA_ae c h, spectralB_ae c h] with x ha hb
  rw [ha, hb]
  have he : (inner ℂ ((spectralWeightA c x : ℂ) * h x)
      ((spectralWeightB c x : ℂ) * h x)).re =
      spectralWeightA c x * spectralWeightB c x * ‖h x‖ ^ 2 := by
    simp [RCLike.inner_apply, Complex.mul_re, Complex.normSq_apply,
      Complex.sq_norm, mul_add, add_mul]
    <;> ring
  rw [he]
  positivity

/-- Scalar conjugation as a continuous semilinear map. -/
def spectralScalarConjugation : ℂ →SL[starRingEnd ℂ] ℂ where
  toFun := star
  map_add' := star_add
  map_smul' a z := by simp [smul_eq_mul]
  cont := continuous_star

/-- Reflection on the real spectral variable preserves Lebesgue measure. -/
def spectralReflection : SpectralHilbert →ₗᵢ[ℂ] SpectralHilbert :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun x : ℝ => -x) (Measure.measurePreserving_neg volume)

/-- Conjugation followed by reflection, before bundling its inverse. -/
def spectralJMap : SpectralHilbert →SL[starRingEnd ℂ] SpectralHilbert :=
  (spectralScalarConjugation.compLpL 2 volume).comp spectralReflection.toContinuousLinearMap

theorem spectralJMap_ae (f : SpectralHilbert) :
    spectralJMap f =ᵐ[volume] fun x => star (f (-x)) := by
  have hc := spectralScalarConjugation.coeFn_compLpL (spectralReflection f)
  have hr := Lp.coeFn_compMeasurePreserving f (Measure.measurePreserving_neg volume)
  filter_upwards [hc, hr] with x hx hrx
  change (spectralScalarConjugation.compLpL 2 volume (spectralReflection f)) x =
    star (f (-x))
  rw [hx]
  change star ((spectralReflection f) x) = _
  rw [hrx]
  rfl

theorem spectralJMap_involutive : Function.Involutive spectralJMap := by
  intro f
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (spectralJMap_ae f)
  filter_upwards [spectralJMap_ae (spectralJMap f), hr] with x hx hy
  rw [hx, hy, neg_neg, star_star]

theorem spectralJMap_norm (f : SpectralHilbert) : ‖spectralJMap f‖ = ‖f‖ := by
  have hbound : ∀ g : SpectralHilbert, ‖spectralJMap g‖ ≤ ‖g‖ := by
    intro g
    calc
      ‖spectralJMap g‖ ≤ ‖spectralReflection g‖ := by
        apply Lp.norm_le_norm_of_ae_le
        filter_upwards [spectralScalarConjugation.coeFn_compLpL (spectralReflection g)]
          with x hx
        change ‖(spectralScalarConjugation.compLpL 2 volume (spectralReflection g)) x‖ ≤ _
        rw [hx]
        change ‖star ((spectralReflection g) x)‖ ≤ _
        simp
      _ = ‖g‖ := spectralReflection.norm_map g
  exact le_antisymm (hbound f) (by simpa only [spectralJMap_involutive f] using hbound (spectralJMap f))

/-- The concrete antiunitary Jf(ξ)=conj(f(-ξ)). -/
def spectralJ : SpectralHilbert ≃ₛₗᵢ[starRingEnd ℂ] SpectralHilbert where
  toLinearEquiv :=
    { spectralJMap.toLinearMap with
      invFun := spectralJMap
      left_inv := spectralJMap_involutive
      right_inv := spectralJMap_involutive }
  norm_map' := spectralJMap_norm

theorem spectralJ_ae (f : SpectralHilbert) :
    spectralJ f =ᵐ[volume] fun x => star (f (-x)) :=
  spectralJMap_ae f

theorem spectralJ_involutive : Function.Involutive spectralJ :=
  spectralJMap_involutive

theorem spectralJA_eq_BJ (c : ℝ) (f : SpectralHilbert) :
    spectralJ (spectralA c f) = spectralB c (spectralJ f) := by
  apply Lp.ext
  have hr := (Measure.measurePreserving_neg (volume : Measure ℝ)).quasiMeasurePreserving.ae
    (spectralA_ae c f)
  filter_upwards [spectralJ_ae (spectralA c f), spectralB_ae c (spectralJ f),
    spectralJ_ae f, hr] with x hj hb hf ha
  rw [hj, hb, hf, ha, spectral_weight_reflection]
  simp [mul_comm]

theorem spectralJB_eq_AJ (c : ℝ) (f : SpectralHilbert) :
    spectralJ (spectralB c f) = spectralA c (spectralJ f) := by
  have h := spectralJA_eq_BJ c (spectralJ f)
  apply spectralJ.injective
  simpa only [spectralJ_involutive f, spectralJ_involutive (spectralB c f)] using h.symm

#print axioms SpectralHilbert
#print axioms spectralWeightA
#print axioms spectralWeightB
#print axioms spectral_weight_den_pos
#print axioms spectral_weightA_pos
#print axioms spectral_weightB_pos
#print axioms spectral_weight_square_sum
#print axioms spectral_weightA_le_one
#print axioms spectral_weightB_le_one
#print axioms spectral_weightA_norm_le_one
#print axioms spectral_weightB_norm_le_one
#print axioms spectral_weightA_continuous
#print axioms spectral_weightB_continuous
#print axioms spectral_weight_reflection
#print axioms spectral_weightB_reflection
#print axioms spectral_weight_ratio
#print axioms boundedSpectralWeight
#print axioms bounded_spectral_weight_ae
#print axioms boundedSpectralMultiplier
#print axioms bounded_spectral_multiplier_ae
#print axioms bounded_spectral_multiplier_norm
#print axioms bounded_spectral_multiplier_selfadjoint
#print axioms spectralA
#print axioms spectralB
#print axioms spectralA_ae
#print axioms spectralB_ae
#print axioms spectralA_norm_le
#print axioms spectralB_norm_le
#print axioms spectralA_selfadjoint
#print axioms spectralB_selfadjoint
#print axioms spectralAB_commute
#print axioms spectralAB_square_sum
#print axioms spectralA_injective
#print axioms spectralAB_quadratic_nonneg
#print axioms spectralScalarConjugation
#print axioms spectralReflection
#print axioms spectralJMap
#print axioms spectralJMap_ae
#print axioms spectralJMap_involutive
#print axioms spectralJMap_norm
#print axioms spectralJ
#print axioms spectralJ_ae
#print axioms spectralJ_involutive
#print axioms spectralJA_eq_BJ
#print axioms spectralJB_eq_AJ

end ChatgptAudit.Continuous049
