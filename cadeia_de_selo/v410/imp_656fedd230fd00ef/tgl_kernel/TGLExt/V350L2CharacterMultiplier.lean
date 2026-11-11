import TGLExt.V350L2OperatorLift
import TGLExt.V350L2Translation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
The continuous character multiplier on Lebesgue L²(ℝ,H).
The conventions are D_s f(x) = exp(-i*s*x) • f(x) and S_t f(x) = f(x-t).
This constructs the implementing unitaries for a future dual action; it does not
construct a crossed product or a canonical trace.
-/
namespace TGLV350.Regular
open MeasureTheory Filter
open scoped Topology
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The negative-sign real character, with no discrete topology on the parameter. -/
def characterPhase (s x : ℝ) : ℂ := Complex.exp (-Complex.I * (s : ℂ) * (x : ℂ))

theorem characterPhase_norm (s x : ℝ) : ‖characterPhase s x‖ = 1 := by
  simp [characterPhase, Complex.norm_exp, Complex.mul_re, Complex.mul_im]

theorem characterPhase_continuous (s : ℝ) : Continuous (characterPhase s) := by
  unfold characterPhase
  fun_prop

theorem characterPhase_parameter_continuous (x : ℝ) :
    Continuous (fun s : ℝ => characterPhase s x) := by
  unfold characterPhase
  fun_prop

theorem characterPhase_zero (x : ℝ) : characterPhase 0 x = 1 := by
  simp [characterPhase]

theorem characterPhase_add (s t x : ℝ) :
    characterPhase s x * characterPhase t x = characterPhase (s+t) x := by
  unfold characterPhase
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem characterPhase_weyl (s t x : ℝ) :
    characterPhase s x * characterPhase (-s) (x-t) = characterPhase s t := by
  unfold characterPhase
  rw [← Complex.exp_add]
  congr 1
  push_cast
  ring

theorem characterMultiplier_memLp (s : ℝ) (f : RegularHilbert H) :
    MemLp (fun x : ℝ => characterPhase s x • f x) 2 volume := by
  apply (Lp.memLp f).of_le
    ((characterPhase_continuous s).aestronglyMeasurable.smul (Lp.aestronglyMeasurable f))
  exact Eventually.of_forall fun x => by simp [norm_smul, characterPhase_norm]

/-- The product is formed in the a.e. quotient, after proving square integrability. -/
def characterMultiplierLp (s : ℝ) (f : RegularHilbert H) : RegularHilbert H :=
  (characterMultiplier_memLp s f).toLp (fun x : ℝ => characterPhase s x • f x)

theorem characterMultiplierLp_ae (s : ℝ) (f : RegularHilbert H) :
    characterMultiplierLp s f =ᵐ[volume] fun x : ℝ => characterPhase s x • f x :=
  (characterMultiplier_memLp s f).coeFn_toLp

theorem characterMultiplierLp_norm (s : ℝ) (f : RegularHilbert H) :
    ‖characterMultiplierLp s f‖ = ‖f‖ := by
  rw [Lp.norm_def, Lp.norm_def]
  congr 1
  apply eLpNorm_congr_norm_ae
  filter_upwards [characterMultiplierLp_ae s f] with x hx
  simp [hx, norm_smul, characterPhase_norm]

def characterMultiplierIsometry (s : ℝ) : RegularHilbert H →ₗᵢ[ℂ] RegularHilbert H where
  toFun := characterMultiplierLp s
  map_add' f g := by
    apply Lp.ext
    filter_upwards [characterMultiplierLp_ae s (f+g),
      Lp.coeFn_add f g, characterMultiplierLp_ae s f, characterMultiplierLp_ae s g,
      Lp.coeFn_add (characterMultiplierLp s f) (characterMultiplierLp s g)]
      with x h1 h2 h3 h4 h5
    simp only [h1, h2, h5, h3, h4, Pi.add_apply, smul_add]
  map_smul' c f := by
    apply Lp.ext
    filter_upwards [characterMultiplierLp_ae s (c • f), Lp.coeFn_smul c f,
      characterMultiplierLp_ae s f, Lp.coeFn_smul c (characterMultiplierLp s f)]
      with x h1 h2 h3 h4
    simp only [h1, h2, h4, h3, Pi.smul_apply, RingHom.id_apply]
    exact smul_comm _ _ _
  norm_map' := characterMultiplierLp_norm s

/-- D_s, as a bounded complex-linear operator on the actual Lebesgue L² space. -/
def characterMultiplier (s : ℝ) : RegularHilbert H →L[ℂ] RegularHilbert H :=
  (characterMultiplierIsometry s).toContinuousLinearMap

theorem characterMultiplier_ae (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s f =ᵐ[volume]
      fun x : ℝ => Complex.exp (-Complex.I * (s : ℂ) * (x : ℂ)) • f x :=
  characterMultiplierLp_ae s f

theorem characterMultiplier_norm (s : ℝ) (f : RegularHilbert H) :
    ‖characterMultiplier s f‖ = ‖f‖ :=
  (characterMultiplierIsometry s).norm_map f

theorem characterMultiplier_zero : characterMultiplier (H := H) 0 = 1 := by
  ext1 f
  apply Lp.ext
  filter_upwards [characterMultiplierLp_ae 0 f] with x hx
  change characterMultiplierLp 0 f x = f x
  simpa [characterPhase_zero] using hx

theorem characterMultiplier_mul (s t : ℝ) :
    characterMultiplier (H := H) s * characterMultiplier t = characterMultiplier (s+t) := by
  ext1 f
  apply Lp.ext
  filter_upwards [characterMultiplierLp_ae s (characterMultiplier t f),
    characterMultiplierLp_ae t f, characterMultiplierLp_ae (s+t) f] with x h1 h2 h3
  change characterMultiplierLp s (characterMultiplier t f) x = characterMultiplierLp (s+t) f x
  change characterMultiplier t f x = _ at h2
  rw [h1, h2, h3, smul_smul, characterPhase_add]

theorem characterMultiplier_inverse (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s (characterMultiplier (-s) f) = f := by
  change (characterMultiplier (H := H) s * characterMultiplier (-s) :
    RegularHilbert H →L[ℂ] RegularHilbert H) f = f
  rw [characterMultiplier_mul, add_neg_cancel, characterMultiplier_zero]
  rfl

theorem characterMultiplier_star (s : ℝ) :
    star (characterMultiplier (H := H) s) = characterMultiplier (-s) := by
  rw [ContinuousLinearMap.star_eq_adjoint]
  ext1 y
  apply ext_inner_left ℂ
  intro x
  rw [ContinuousLinearMap.adjoint_inner_right]
  have h := (characterMultiplierIsometry s).inner_map_map x (characterMultiplier (-s) y)
  change inner ℂ (characterMultiplier s x)
    (characterMultiplier s (characterMultiplier (-s) y)) =
      inner ℂ x (characterMultiplier (-s) y) at h
  rw [characterMultiplier_inverse] at h
  exact h

theorem characterMultiplier_unitary (s : ℝ) :
    star (characterMultiplier (H := H) s) * characterMultiplier s = 1 ∧
      characterMultiplier (H := H) s * star (characterMultiplier (H := H) s) = 1 := by
  simp [characterMultiplier_star, characterMultiplier_mul, characterMultiplier_zero]

theorem characterMultiplier_commutes_fibre (s : ℝ) (T : H →L[ℂ] H) :
    characterMultiplier s * fibre T = fibre T * characterMultiplier s := by
  ext1 f
  apply Lp.ext
  filter_upwards [characterMultiplier_ae s (fibre T f), fibre_ae T f,
    fibre_ae T (characterMultiplier s f), characterMultiplier_ae s f] with x h1 h2 h3 h4
  change characterMultiplier s (fibre T f) x = fibre T (characterMultiplier s f) x
  rw [h1, h2, h3, h4, map_smul]

/-- Weyl covariance with precisely the signs of D_s and shift_t specified above. -/
theorem characterMultiplier_weyl (s t : ℝ) :
    characterMultiplier (H := H) s * shift t * star (characterMultiplier (H := H) s) =
      Complex.exp (-Complex.I * (s : ℂ) * (t : ℂ)) • shift t := by
  rw [characterMultiplier_star]
  ext1 f
  apply Lp.ext
  filter_upwards [characterMultiplierLp_ae s (shift t (characterMultiplier (-s) f)),
    shift_ae t (characterMultiplier (-s) f),
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae
      (characterMultiplierLp_ae (-s) f),
    Lp.coeFn_smul (characterPhase s t) (shift t f), shift_ae t f]
    with x h1 h2 h3 h4 h5
  change characterMultiplierLp s (shift t (characterMultiplier (-s) f)) x =
    (characterPhase s t • shift t f) x
  change characterMultiplier (-s) f (x-t) = _ at h3
  rw [h1, h2, h3, h4, Pi.smul_apply, h5, smul_smul, characterPhase_weyl]

/-- Matrix coefficients against a fixed orbit vector are continuous by dominated
convergence; the integrable majorant is exactly the square norm of f. -/
theorem characterMultiplier_inner_continuous (f : RegularHilbert H) (t : ℝ) :
    Continuous (fun s : ℝ => inner ℂ (characterMultiplier s f) (characterMultiplier t f)) := by
  have hcont : Continuous (fun s : ℝ => ∫ x : ℝ,
      inner ℂ (characterPhase s x • f x) (characterPhase t x • f x)) := by
    apply continuous_of_dominated (bound := fun x : ℝ => ‖f x‖ ^ 2)
    · intro s
      exact (characterMultiplier_memLp s f).1.inner (characterMultiplier_memLp t f).1
    · intro s
      exact Eventually.of_forall fun x => by
        calc
          ‖inner ℂ (characterPhase s x • f x) (characterPhase t x • f x)‖ ≤
              ‖characterPhase s x • f x‖ * ‖characterPhase t x • f x‖ :=
            norm_inner_le_norm _ _
          _ = ‖f x‖ ^ 2 := by simp [norm_smul, characterPhase_norm, pow_two]
    · exact (Lp.memLp f).norm.integrable_sq
    · exact Eventually.of_forall fun x =>
        ((characterPhase_parameter_continuous x).smul continuous_const).inner continuous_const
  apply hcont.congr
  intro s
  rw [L2.inner_def]
  apply integral_congr_ae
  filter_upwards [characterMultiplier_ae s f, characterMultiplier_ae t f] with x hs ht
  rw [hs, ht]
  rfl

/-- Strong continuity for each fixed L² vector, in the ordinary real topology.
No continuity in the operator norm is assumed or claimed. -/
theorem characterMultiplier_strongly_continuous (f : RegularHilbert H) :
    Continuous (fun s : ℝ => characterMultiplier s f) := by
  apply continuous_iff_continuousAt.mpr
  intro t
  have hsq : Continuous (fun s : ℝ => ‖characterMultiplier s f - characterMultiplier t f‖ ^ 2) := by
    have hinner := RCLike.continuous_re.comp (characterMultiplier_inner_continuous f t)
    have h : Continuous (fun s : ℝ => ‖f‖ ^ 2 -
        2 * RCLike.re (inner ℂ (characterMultiplier s f) (characterMultiplier t f)) + ‖f‖ ^ 2) :=
      (continuous_const.sub (continuous_const.mul hinner)).add continuous_const
    apply h.congr
    intro s
    simpa only [characterMultiplier_norm] using
      (norm_sub_sq (𝕜 := ℂ) (characterMultiplier s f) (characterMultiplier t f)).symm
  have hn : Continuous (fun s : ℝ => ‖characterMultiplier s f - characterMultiplier t f‖) := by
    simpa only [Function.comp_def, Real.sqrt_sq_eq_abs, abs_norm] using
      Real.continuous_sqrt.comp hsq
  apply tendsto_iff_dist_tendsto_zero.mpr
  simpa only [ContinuousAt, dist_eq_norm, sub_self, norm_zero] using
    (hn.continuousAt : ContinuousAt
      (fun s : ℝ => ‖characterMultiplier s f - characterMultiplier t f‖) t)

#print axioms characterPhase
#print axioms characterPhase_norm
#print axioms characterPhase_continuous
#print axioms characterPhase_parameter_continuous
#print axioms characterPhase_zero
#print axioms characterPhase_add
#print axioms characterPhase_weyl
#print axioms characterMultiplier_memLp
#print axioms characterMultiplierLp
#print axioms characterMultiplierLp_ae
#print axioms characterMultiplierLp_norm
#print axioms characterMultiplierIsometry
#print axioms characterMultiplier
#print axioms characterMultiplier_ae
#print axioms characterMultiplier_norm
#print axioms characterMultiplier_zero
#print axioms characterMultiplier_mul
#print axioms characterMultiplier_inverse
#print axioms characterMultiplier_star
#print axioms characterMultiplier_unitary
#print axioms characterMultiplier_commutes_fibre
#print axioms characterMultiplier_weyl
#print axioms characterMultiplier_inner_continuous
#print axioms characterMultiplier_strongly_continuous
end
end TGLV350.Regular
