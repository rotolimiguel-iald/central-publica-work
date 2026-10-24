import TGLExt.F1Fecho394.FubiniL2
import TGLExt.ContinuousModularReconstruction
import TGLExt.V350L2PositiveMultiplier
set_option autoImplicit false
set_option maxHeartbeats 500000
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace F1Rede.Wedge
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050 TGLV350.Regular

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
abbrev VH (H : Type) [NormedAddCommGroup H] := Lp H 2 (volume : Measure ℝ)

def A (c : ℝ) : VH H →L[ℂ] VH H :=
  realScalarMultiplier (spectralWeightA c) (spectral_weightA_continuous c)
    (fun x => (spectral_weightA_pos c x).le) (spectral_weightA_le_one c)
def B (c : ℝ) : VH H →L[ℂ] VH H :=
  realScalarMultiplier (spectralWeightB c) (spectral_weightB_continuous c)
    (fun x => (spectral_weightB_pos c x).le) (spectral_weightB_le_one c)
theorem A_ae (c : ℝ) (f : VH H) : A c f =ᵐ[volume] fun x => (spectralWeightA c x : ℂ) • f x :=
  realScalarMultiplier_ae _ _ _ _ f
theorem B_ae (c : ℝ) (f : VH H) : B c f =ᵐ[volume] fun x => (spectralWeightB c x : ℂ) • f x :=
  realScalarMultiplier_ae _ _ _ _ f

theorem scalar_selfadjoint (w : ℝ → ℝ) (hw : Continuous w) (h0 : ∀ x, 0 ≤ w x)
    (h1 : ∀ x, w x ≤ 1) : IsSelfAdjoint (realScalarMultiplier (H := H) w hw h0 h1) := by
  apply ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
  intro f g
  simp only [L2.inner_def]
  apply integral_congr_ae
  filter_upwards [realScalarMultiplier_ae w hw h0 h1 f,
    realScalarMultiplier_ae w hw h0 h1 g] with x hf hg
  change inner ℂ ((realScalarMultiplier w hw h0 h1 f) x) (g x) = inner ℂ (f x) ((realScalarMultiplier w hw h0 h1 g) x)
  rw [hf,hg]
  simp [inner_smul_left,inner_smul_right]

theorem A_selfadjoint (c : ℝ) : IsSelfAdjoint (A (H := H) c) := scalar_selfadjoint _ _ _ _
theorem B_selfadjoint (c : ℝ) : IsSelfAdjoint (B (H := H) c) := scalar_selfadjoint _ _ _ _
theorem A_injective (c : ℝ) : Function.Injective (A (H := H) c) :=
  realScalarMultiplier_injective _ _ _ _ (spectral_weightA_pos c)

theorem AB_commute (c : ℝ) : A (H := H) c * B c = B c * A c := by
  ext1 f
  apply Lp.ext
  filter_upwards [A_ae c (B c f), B_ae c (A c f), A_ae c f, B_ae c f] with x hab hba ha hb
  change (A c (B c f)) x = (B c (A c f)) x
  rw [hab,hba,ha,hb,smul_smul,smul_smul,mul_comm]

theorem AB_square_sum (c : ℝ) : A (H := H) c * A c + B c * B c = 1 := by
  ext1 f
  apply Lp.ext
  filter_upwards [A_ae c (A c f), B_ae c (B c f), A_ae c f, B_ae c f,
    Lp.coeFn_add (A c (A c f)) (B c (B c f))] with x haa hbb ha hb hadd
  change (A c (A c f) + B c (B c f)) x = f x
  rw [hadd]
  change (A c (A c f)) x + (B c (B c f)) x = f x
  rw [haa,hbb,ha,hb,smul_smul,smul_smul,← add_smul]
  have heq : (spectralWeightA c x : ℂ) * spectralWeightA c x +
      (spectralWeightB c x : ℂ) * spectralWeightB c x = 1 := by
    exact_mod_cast (by simpa only [pow_two] using spectral_weight_square_sum c x)
  rw [heq,one_smul]

theorem AB_positive (c : ℝ) (f : VH H) : 0 ≤ (inner ℂ (A c f) (B c f)).re := by
  rw [L2.inner_def]
  change 0 ≤ RCLike.re (∫ x : ℝ, inner ℂ (A c f x) (B c f x))
  rw [← integral_re (L2.integrable_inner (𝕜 := ℂ) (A c f) (B c f))]
  apply integral_nonneg_of_ae
  filter_upwards [A_ae c f,B_ae c f] with x ha hb
  change 0 ≤ (inner ℂ (A c f x) (B c f x)).re
  rw [ha,hb]
  have heq : (inner ℂ ((spectralWeightA c x : ℂ) • f x)
      ((spectralWeightB c x : ℂ) • f x)).re =
      spectralWeightA c x * spectralWeightB c x * ‖f x‖^2 := by
    simp [inner_self_eq_norm_sq_to_K, Complex.mul_re, ← Complex.ofReal_pow]
    <;> ring
  rw [heq]
  exact mul_nonneg (mul_nonneg (spectral_weightA_pos c x).le (spectral_weightB_pos c x).le) (sq_nonneg _)

def T (c : ℝ) : VH H →ₗ.[ℂ] VH H := boundedGraphOperator (A (H := H) c) (B (H := H) c) (A_injective (H := H) c)
theorem T_dense (c : ℝ) : Dense ((T (H := H) c).domain : Set (VH H)) :=
  bounded_graph_domain_dense (A (H := H) c) (B (H := H) c) (A_injective (H := H) c) (A_selfadjoint (H := H) c)
theorem T_selfadjoint (c : ℝ) : IsSelfAdjoint (T (H := H) c) :=
  bounded_graph_selfadjoint (A (H := H) c) (B (H := H) c) (A_injective (H := H) c) (A_selfadjoint (H := H) c) (B_selfadjoint (H := H) c)
    (AB_commute (H := H) c) (AB_square_sum (H := H) c)
theorem T_positive (c : ℝ) (f : (T (H := H) c).domain) :
    0 ≤ (inner ℂ (f : VH H) (T c f)).re :=
  bounded_graph_positive (A (H := H) c) (B (H := H) c) (A_injective (H := H) c) (AB_positive (H := H) c) f

theorem T_graph (c : ℝ) (f g : VH H) :
    (f,g) ∈ (T c).graph ↔ g =ᵐ[volume] fun x => (Real.exp (-c*x) : ℂ) • f x := by
  change (f,g) ∈ (boundedGraphOperator (A (H := H) c) (B (H := H) c) (A_injective (H := H) c)).graph ↔ _
  rw [bounded_graph_equation_iff (A (H := H) c) (B (H := H) c) (A_injective (H := H) c) (AB_commute (H := H) c) (AB_square_sum (H := H) c)]
  have hr (x : ℝ) : (spectralWeightB c x : ℂ) =
      (Real.exp (-c*x) : ℂ) * spectralWeightA c x := by exact_mod_cast spectral_weight_ratio c x
  constructor
  · intro hfg
    filter_upwards [B_ae c f,A_ae c g] with x hb ha
    have he := congrArg (fun u : VH H => u x) hfg
    rw [hb,ha,hr, mul_comm, mul_smul] at he
    exact (smul_right_injective H (Complex.ofReal_ne_zero.mpr (spectral_weightA_pos c x).ne')) he.symm
  · intro hfg
    apply Lp.ext
    filter_upwards [B_ae c f,A_ae c g,hfg] with x hb ha hg
    rw [hb,ha,hg,hr,smul_smul,mul_comm]

#print axioms T_selfadjoint
#print axioms T_positive
#print axioms T_graph
end F1Rede.Wedge