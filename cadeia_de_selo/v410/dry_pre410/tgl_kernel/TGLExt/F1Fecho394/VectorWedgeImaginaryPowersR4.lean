import TGLExt.F1Fecho394.VectorSquare
import TGLExt.V351ScalarMultiplierCalculus
import TGLExt.V351RegularImaginaryPowers

/-! CFC imaginary powers of the actual vector-valued one-particle multiplier.
This is the reusable spectral-coordinate step; it is not yet second quantized. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.VectorWedgePowers
open F1Rede.Wedge ChatgptAudit ChatgptAudit.Continuous049 TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def weight (c x : ℝ) : ℝ := spectralWeightA c x ^ 2
lemma weight_continuous (c : ℝ) : Continuous (weight c) := (spectral_weightA_continuous c).pow 2
lemma weight_nonneg (c x : ℝ) : 0 ≤ weight c x := sq_nonneg _
lemma weight_le_one (c x : ℝ) : weight c x ≤ 1 := by
  have h := spectral_weight_square_sum c x
  dsimp [weight]
  nlinarith [sq_nonneg (spectralWeightB c x)]

def R (c : ℝ) : VH H →L[ℂ] VH H :=
  realScalarMultiplier (weight c) (weight_continuous c) (weight_nonneg c) (weight_le_one c)

theorem R_eq (c : ℝ) : R (H:=H) c = A c * A c := by
  ext1 f
  apply Lp.ext
  filter_upwards [realScalarMultiplier_ae (weight c) (weight_continuous c)
      (weight_nonneg c) (weight_le_one c) f,A_ae c (A c f),A_ae c f] with x hR hA hA'
  change R c f x=(A c (A c f)) x
  change R c f x = _ at hR
  rw [hR,hA,hA',smul_smul]
  congr 1
  simp only [weight,pow_two,Complex.ofReal_mul]

theorem complement_eq (c : ℝ) : 1-R (H:=H) c = B c * B c := by
  rw [R_eq]
  exact sub_eq_iff_eq_add.mpr (by simpa only [add_comm] using (AB_square_sum (H:=H) c).symm)

theorem R_nonneg (c : ℝ) : 0 ≤ R (H:=H) c := realScalarMultiplier_nonneg _ _ _ _
theorem R_le_one (c : ℝ) : R (H:=H) c ≤ 1 := realScalarMultiplier_le_one _ _ _ _
theorem R_injective (c : ℝ) : Function.Injective (R (H:=H) c) := by
  rw [R_eq]
  exact (A_injective c).comp (A_injective c)
theorem complement_injective (c : ℝ) : Function.Injective (1-R (H:=H) c : VH H→L[ℂ]VH H) := by
  rw [complement_eq]
  have hi : Function.Injective (B (H:=H) c) :=
    realScalarMultiplier_injective _ _ _ _ (spectral_weightB_pos c)
  exact hi.comp hi

theorem square_is_resolvent_graph (c : ℝ) :
    partialOperatorSquare (T (H:=H) c)=resolventGraphOperator (R (H:=H) c) (R_injective (H:=H) c) := by
  exact boundedGraph_square_eq_resolvent (H:=VH H) (A (H:=H) c) (B (H:=H) c) (R (H:=H) c) (A_injective c) (R_injective (H:=H) c)
    (AB_commute c) (R_eq (H:=H) c).symm (complement_eq (H:=H) c).symm

theorem phase_at_weight (c t x : ℝ) :
    resolventPhaseFunction t (weight c x) =
      (resolventDamping (weight c x) : ℂ) * characterPhase (2*c*t) x := by
  have hr : (1-weight c x)/weight c x = Real.exp (-2*c*x) := by
    apply (div_eq_iff (ne_of_gt (sq_pos_of_pos (spectral_weightA_pos c x)))).mpr
    have he : Real.exp (-2*c*x)=(Real.exp (-c*x))^2 := by
      rw [pow_two,← Real.exp_add]
      congr 1
      ring
    rw [he]
    have hb := spectral_weight_square_sum c x
    rw [spectral_weight_ratio] at hb
    dsimp [weight]
    nlinarith
  rw [resolventPhaseFunction,hr,Real.log_exp]
  congr 1
  unfold modularPhase characterPhase
  congr 1
  push_cast
  ring

theorem imaginaryPower_eq_character (c t : ℝ) (u : VH H) :
    resolventImaginaryPower (R (H:=H) c) (R_nonneg (H:=H) c) (R_le_one (H:=H) c) (R_injective (H:=H) c)
      (complement_injective (H:=H) c) t u = characterMultiplier (2*c*t) u := by
  refine (resolventDampingOperator_denseRange (R (H:=H) c) (R_nonneg (H:=H) c) (R_le_one (H:=H) c)
    (R_injective (H:=H) c) (complement_injective (H:=H) c)).induction ?_ (isClosed_eq (by fun_prop) (by fun_prop)) u
  rintro _ ⟨y,rfl⟩
  rw [resolventImaginaryPower_damping]
  have hd := realScalarMultiplier_cfc_ae (weight c) (weight_continuous c)
    (weight_nonneg c) (weight_le_one c) (fun z : ℂ => (resolventDamping z.re : ℂ))
    (by unfold resolventDamping; fun_prop) y
  change cfc (fun z : ℂ => (resolventDamping z.re : ℂ)) (R (H:=H) c) y =ᵐ[volume] _ at hd
  rw [resolventDampingOperator_cfc (R (H:=H) c) (R_nonneg (H:=H) c).isSelfAdjoint] at hd
  have hp := realScalarMultiplier_cfc_ae (weight c) (weight_continuous c)
    (weight_nonneg c) (weight_le_one c) (fun z : ℂ => resolventPhaseFunction t z.re)
    ((resolventPhaseFunction_continuous t).comp Complex.continuous_re) y
  change cfc (fun z : ℂ => resolventPhaseFunction t z.re) (R (H:=H) c) y =ᵐ[volume] _ at hp
  apply Lp.ext
  filter_upwards [hp,hd,characterMultiplier_ae (2*c*t) (resolventDampingOperator (R (H:=H) c) y)]
    with x hp hd hc
  change resolventPhaseOperator (R (H:=H) c) t y x = characterMultiplier (2*c*t) (resolventDampingOperator (R (H:=H) c) y) x
  dsimp only [resolventPhaseOperator]
  rw [hp,hc,hd]
  simp only [Complex.ofReal_re]
  rw [phase_at_weight,smul_smul,mul_comm]
  rfl

end F1Fecho.VectorWedgePowers
#print axioms F1Fecho.VectorWedgePowers.R_eq
#print axioms F1Fecho.VectorWedgePowers.square_is_resolvent_graph
#print axioms F1Fecho.VectorWedgePowers.phase_at_weight
#print axioms F1Fecho.VectorWedgePowers.imaginaryPower_eq_character
