import TGLExt.F1Fecho394.ScalarL2CalculusR4
import TGLExt.V351RegularImaginaryPowers
/-! Imaginary powers of a scalar resolvent multiplier for an arbitrary
measurable real spectral coordinate. Endpoint singularities are removed by
the existing damping/dense-range construction; no logarithm is applied by
continuous functional calculus directly at the endpoints. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.ScalarL2Spectral
open F1Fecho.ScalarL2 ChatgptAudit TGLV350.Regular
variable {X E : Type} [MeasurableSpace X]
  [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
variable (μ : Measure X) (h:X→ℝ) (hh:Measurable h)

def weight (x:X) : unitInterval :=
  ⟨Real.sigmoid (-h x),Real.sigmoid_nonneg _,Real.sigmoid_le_one _⟩
include hh in
lemma weight_measurable : Measurable (weight h) :=
  (continuous_sigmoid.measurable.comp hh.neg).subtype_mk

def R : Lp E 2 μ→L[ℂ]Lp E 2 μ :=
  ScalarL2.R μ (weight h) (weight_measurable h hh).aestronglyMeasurable

theorem R_nonneg : 0≤R (E:=E) μ h hh := by
  let F:=compactRepresentation (E:=E) μ (weight h)
    (weight_measurable h hh).aestronglyMeasurable
  let q:C(unitInterval,ℂ):=⟨fun x=>(Real.sqrt (x:ℝ):ℂ),by fun_prop⟩
  have he : star q*q=coordinate := by
    ext x
    change star (Real.sqrt (x:ℝ):ℂ)*(Real.sqrt (x:ℝ):ℂ)=((x:ℝ):ℂ)
    simp only [Complex.star_def,Complex.conj_ofReal]
    norm_cast
    exact Real.mul_self_sqrt x.2.1
  have hmap:=congrArg F he
  rw [map_mul,map_star] at hmap
  change star (F q)*F q=R (E:=E) μ h hh at hmap
  rw [←hmap]
  exact star_mul_self_nonneg _

theorem R_le_one : R (E:=E) μ h hh≤1 := by
  apply sub_nonneg.mp
  let F:=compactRepresentation (E:=E) μ (weight h)
    (weight_measurable h hh).aestronglyMeasurable
  let q:C(unitInterval,ℂ):=⟨fun x=>(Real.sqrt (1-(x:ℝ)):ℂ),by fun_prop⟩
  have he : star q*q=1-coordinate := by
    ext x
    change star (Real.sqrt (1-(x:ℝ)):ℂ)*(Real.sqrt (1-(x:ℝ)):ℂ)=1-((x:ℝ):ℂ)
    simp only [Complex.star_def,Complex.conj_ofReal]
    norm_cast
    exact Real.mul_self_sqrt (sub_nonneg.mpr x.2.2)
  have hmap:=congrArg F he
  rw [map_mul,map_star,map_sub,map_one] at hmap
  change star (F q)*F q=1-R (E:=E) μ h hh at hmap
  rw [←hmap]
  exact star_mul_self_nonneg _

theorem R_injective : Function.Injective (R (E:=E) μ h hh) := by
  apply op_injective
  intro x
  change (Real.sigmoid (-h x):ℂ)≠0
  exact_mod_cast (ne_of_gt (Real.sigmoid_pos (-h x)))

theorem complement_injective : Function.Injective (1-R (E:=E) μ h hh : Lp E 2 μ→L[ℂ]Lp E 2 μ) := by
  let F:=compactRepresentation (E:=E) μ (weight h)
    (weight_measurable h hh).aestronglyMeasurable
  have he : 1-R (E:=E) μ h hh=F (1-coordinate) := by
    rw [map_sub,map_one]
    rfl
  rw [he]
  apply op_injective
  intro x
  change (1:ℂ)-(Real.sigmoid (-h x):ℂ)≠0
  exact_mod_cast (ne_of_gt (sub_pos.mpr (Real.sigmoid_lt_one (-h x))))

def phaseData (t:ℝ) : Data μ where
  value x := modularPhase t (h x)
  measurable := (by unfold modularPhase; fun_prop : Continuous (modularPhase t)).measurable.comp hh |>.aestronglyMeasurable
  bound := 1
  nonneg := zero_le_one
  bounded x := le_of_eq (modularPhase_norm t (h x))

def phase (t:ℝ) : Lp E 2 μ→L[ℂ]Lp E 2 μ := op μ (phaseData μ h hh t)

theorem imaginaryPower_eq_phase (t:ℝ) (u:Lp E 2 μ) :
    resolventImaginaryPower (R (E:=E) μ h hh) (R_nonneg μ h hh) (R_le_one μ h hh)
      (R_injective μ h hh) (complement_injective μ h hh) t u=phase μ h hh t u := by
  refine (resolventDampingOperator_denseRange (R (E:=E) μ h hh) (R_nonneg μ h hh)
    (R_le_one μ h hh) (R_injective μ h hh) (complement_injective μ h hh)).induction
      ?_ (isClosed_eq (by fun_prop) (by fun_prop)) u
  rintro _ ⟨y,rfl⟩
  rw [resolventImaginaryPower_damping]
  have hd:=cfc_ae μ (weight h) (weight_measurable h hh).aestronglyMeasurable
    (fun z:ℂ=>(resolventDamping z.re:ℂ)) (by unfold resolventDamping; fun_prop) y
  change cfc (fun z:ℂ=>(resolventDamping z.re:ℂ)) (R (E:=E) μ h hh) y=ᵐ[μ] _ at hd
  rw [resolventDampingOperator_cfc _ (R_nonneg (E:=E) μ h hh).isSelfAdjoint] at hd
  have hp:=cfc_ae μ (weight h) (weight_measurable h hh).aestronglyMeasurable
    (fun z:ℂ=>resolventPhaseFunction t z.re)
    ((resolventPhaseFunction_continuous t).comp Complex.continuous_re) y
  change cfc (fun z:ℂ=>resolventPhaseFunction t z.re) (R (E:=E) μ h hh) y=ᵐ[μ] _ at hp
  apply Lp.ext
  filter_upwards [hp,hd,op_ae μ (phaseData μ h hh t)
    (resolventDampingOperator (R (E:=E) μ h hh) y)] with x hp hd hx
  change resolventPhaseOperator (R (E:=E) μ h hh) t y x=
    op μ (phaseData μ h hh t) (resolventDampingOperator (R (E:=E) μ h hh) y) x
  dsimp only [resolventPhaseOperator]
  rw [hp,hx,hd]
  simp only [weight,Complex.ofReal_re,phaseData,smul_smul,
    resolventPhaseFunction_sigmoid,neg_neg,mul_comm]

end F1Fecho.ScalarL2Spectral
#print axioms F1Fecho.ScalarL2Spectral.R_nonneg
#print axioms F1Fecho.ScalarL2Spectral.complement_injective
#print axioms F1Fecho.ScalarL2Spectral.imaginaryPower_eq_phase
