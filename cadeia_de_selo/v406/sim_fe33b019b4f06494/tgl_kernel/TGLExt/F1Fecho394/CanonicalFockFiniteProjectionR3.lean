import TGLExt.F1Fecho394.CanonicalFockActualPositiveTracePackageR2
import TGLExt.V354SpectralThreshold

/-! DECLARADO / UNCOMPILED CANDIDATE, R51, 2026-10-16.
Finite nonzero projections for the existing inverse-supremum trace on the SAME
represented Fock core. The finite seed is supplied by actual semifiniteness;
the threshold is the existing generic spectral theorem, specialized on
RegularHilbert Fock. No trace, spectral projection, type-II, corner or split
is assumed. A finite subprojection below each nonzero projection is included
for the subsequent matrix-corner consumer. Actual dual scaling calibrates a
projection to trace one. Equal orthogonal faces remain a separate obligation.
The consumer is RemainingModularCoreInput on this very represented core.
Require EXIT0 and all five public axiom reports before integration. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
noncomputable section
namespace F1Fecho.CanonicalFockFiniteProjectionR3
open TGLExt TGLV350.Regular
open F1Fecho.CanonicalFockRegular (core)
open F1Fecho.CanonicalFockWeight (PositiveInput zero one scale positiveDual positive_cone_nontrivial)
open F1Fecho.CanonicalFockInverseSupremum (value value_zero value_scale value_mono value_faithful value_dual)
open F1Fecho.CanonicalFockActualInverseFinitenessR2 (value_finite_minorants)
open scoped ENNReal NNReal

/-- Scalar cancellation is proved before specializing the Hilbert space.
This avoids reducing the concrete Fock scalar-action dictionaries. -/
private theorem scaled_projection_support {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (epsilon : ℝ) (he : 0 < epsilon) (e q : H →L[ℂ] H)
    (heproj : IsStarProjection e) (hq : 0 ≤ q) (hbound : epsilon • q ≤ e) :
    q * e = q := by
  have hh := (heproj.mul_right_and_mul_left_of_nonneg_of_le
    (smul_nonneg he.le hq) hbound).1
  rw [smul_mul_assoc] at hh
  exact smul_right_injective (H →L[ℂ] H) he.ne' hh

private abbrev AmbientHilbert := RegularHilbert F1Rede.BosonicFock.F
private abbrev ambientNormedAddCommGroup : NormedAddCommGroup AmbientHilbert := inferInstance
private abbrev ambientInnerProductSpace : InnerProductSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientNormedSpace : NormedSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientModule : Module ℂ AmbientHilbert := inferInstance
private abbrev ambientTopologicalSpace : TopologicalSpace AmbientHilbert := inferInstance
private abbrev ambientUniformSpace : UniformSpace AmbientHilbert := inferInstance
private abbrev ambientCompleteSpace : CompleteSpace AmbientHilbert := inferInstance
private abbrev ambientStar : Star (AmbientHilbert →L[ℂ] AmbientHilbert) := inferInstance
private abbrev ambientOrder : PartialOrder (AmbientHilbert →L[ℂ] AmbientHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := AmbientHilbert)
attribute [local instance] ambientNormedAddCommGroup ambientInnerProductSpace
  ambientNormedSpace ambientModule ambientTopologicalSpace ambientUniformSpace
  ambientCompleteSpace ambientStar ambientOrder

theorem finite_positive_below (X : PositiveInput) (hX : X ≠ zero) :
    ∃ Y : PositiveInput, Y.val ≤ X.val ∧ 0 < value Y ∧ value Y < ⊤ := by
  classical
  by_contra h
  have hz : value X = 0 := by
    rw [value_finite_minorants X]
    apply le_antisymm ?_ bot_le
    apply iSup_le
    intro Y
    apply iSup_le
    intro hYX
    apply iSup_le
    intro hf
    exact le_of_not_gt (fun hp => h ⟨Y,hYX,hp,hf⟩)
  exact hX (Subtype.ext ((value_faithful X).mp hz))
#print axioms finite_positive_below

theorem finite_subprojection_exists (e : PositiveInput)
    (heproj : IsStarProjection e.val) (hene : e ≠ zero) :
    ∃ q : PositiveInput, IsStarProjection q.val ∧
      0 < value q ∧ value q < ⊤ ∧ q.val * e.val = q.val := by
  obtain ⟨Y,hYle,hYpos,hYfin⟩ := finite_positive_below e hene
  have hYne : Y.val ≠ 0 := by
    intro hz
    have hv : value Y = 0 := (value_faithful Y).mpr hz
    exact hYpos.ne' hv
  obtain ⟨epsilon,q,he,hq,hqm,hqne,hbound⟩ :=
    @positive_operator_has_threshold_projection AmbientHilbert
      ambientNormedAddCommGroup ambientInnerProductSpace ambientCompleteSpace
      core Y.val Y.property.1 Y.property.2 hYne
  let Q : PositiveInput := ⟨q,hqm,hq.nonneg⟩
  have hQpos : 0 < value Q := by
    apply lt_of_le_of_ne zero_le
    intro hz
    exact hqne ((value_faithful Q).mp hz.symm)
  have hQfin : value Q < ⊤ := by
    have hl : value (scale ⟨epsilon,he.le⟩ Q) ≤ value Y := value_mono _ _ hbound
    rw [value_scale] at hl
    apply lt_top_iff_ne_top.mpr
    intro hinf
    rw [hinf,ENNReal.mul_top (by
      apply ENNReal.coe_ne_zero.mpr
      intro hz
      exact he.ne' (congrArg (fun r : ℝ≥0 => (r : ℝ)) hz))] at hl
    exact (not_le_of_gt hYfin) hl
  have hQe : q * e.val = q :=
    @scaled_projection_support AmbientHilbert ambientNormedAddCommGroup
      ambientInnerProductSpace ambientCompleteSpace epsilon he e.val q
      heproj hq.nonneg (hbound.trans hYle)
  exact ⟨Q,hq,hQpos,hQfin,hQe⟩
#print axioms finite_subprojection_exists

/-- Unconditional finite nonzero projection in the original Fock core. -/
theorem finite_projection_exists :
    ∃ q : PositiveInput, IsStarProjection q.val ∧ q.val ≠ 0 ∧
      0 < value q ∧ value q < ⊤ := by
  obtain ⟨q,hq,hpos,hfin,_⟩ := finite_subprojection_exists one
    (show IsStarProjection one.val from
      IsStarProjection.one (AmbientHilbert →L[ℂ] AmbientHilbert)) positive_cone_nontrivial
  have hne : q.val ≠ 0 := fun hz => hpos.ne' ((value_faithful q).mpr hz)
  exact ⟨q,hq,hne,hpos,hfin⟩
#print axioms finite_projection_exists

/-- Calibration uses the actual exp(-s)-scaling dual action, not a new trace. -/
theorem dual_calibration (X : PositiveInput) (hpos : 0 < value X) (hfin : value X < ⊤) :
    value (positiveDual (Real.log (value X).toReal) X) = 1 := by
  rw [value_dual]
  have hx0 := hpos.ne'
  have hxt := hfin.ne
  have hxr := ENNReal.toReal_pos hx0 hxt
  rw [Real.exp_neg,Real.exp_log hxr,ENNReal.ofReal_inv_of_pos hxr,
    ENNReal.ofReal_toReal hxt]
  exact ENNReal.inv_mul_cancel hx0 hxt
#print axioms dual_calibration

/-- A trace-one projection; no assertion of equal orthogonal halves yet. -/
theorem normalized_projection_exists :
    ∃ q : PositiveInput, IsStarProjection q.val ∧ q.val ≠ 0 ∧ value q = 1 := by
  obtain ⟨q,hq,_,hpos,hfin⟩ := finite_projection_exists
  let s := Real.log (value q).toReal
  let Q := positiveDual s q
  have hp : IsStarProjection Q.val := hq.map (dualAmbient s)
  have hv : value Q = 1 := dual_calibration q hpos hfin
  have hn : Q.val ≠ 0 := by
    intro hz
    have hzero := (value_faithful Q).mpr hz
    exact one_ne_zero (hv.symm.trans hzero)
  exact ⟨Q,hp,hn,hv⟩
#print axioms normalized_projection_exists

end F1Fecho.CanonicalFockFiniteProjectionR3
