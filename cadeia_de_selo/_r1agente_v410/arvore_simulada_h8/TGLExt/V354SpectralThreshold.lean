import TGLExt.V354FiniteTraceSupport
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt TGLV351
open scoped ENNReal NNReal
noncomputable section

-- The default 200000 budget timed out elaborating this CFC/projection proof.
-- This local budget is for elaboration only; the kernel and axioms are unchanged.
set_option maxHeartbeats 600000 in
/-- A threshold projection is obtained from the kernel of the negative part.
Its lower bound, rather than Hilbert rank, will control the semifinite trace. -/
theorem positive_operator_has_threshold_projection {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (M : VonNeumannAlgebra H) (X : H →L[ℂ] H)
    (hXm : X ∈ M) (hX : 0 ≤ X) (hXne : X ≠ 0) :
    ∃ (epsilon : ℝ) (q : H →L[ℂ] H), 0 < epsilon ∧
      IsStarProjection q ∧ q ∈ M ∧ q ≠ 0 ∧ epsilon • q ≤ X := by
  let epsilon : ℝ := ‖X‖/2
  have he : 0 < epsilon := half_pos (norm_pos_iff.mpr hXne)
  let Y : H →L[ℂ] H := X-epsilon • 1
  have hYs : IsSelfAdjoint Y := by
    change star (X-epsilon • 1) = X-epsilon • 1
    simp only [star_sub,star_smul,star_one,star_trivial,hX.isSelfAdjoint.star_eq]
  have hYm : Y ∈ M := M.sub_mem hXm
    (show epsilon • (1 : H →L[ℂ] H) ∈ M from
      M.toStarSubalgebra.smul_mem M.one_mem (epsilon : ℂ))
  letI : IsClosed (M.toStarSubalgebra : Set (H →L[ℂ] H)) := vonNeumann_norm_closed M
  have hZm : Y⁻ ∈ M := by
    rw [CFC.negPart_def]
    exact cfcₙ_mem (𝕜' := ℂ) (s := M.toStarSubalgebra) (fun x : ℝ => x⁻) hYm
  let q := Y⁻.ker.starProjection
  have hq : IsStarProjection q := isStarProjection_starProjection
  have hqm : q ∈ M := kernel_projection_mem_vonNeumann M Y⁻ hZm
  have hqZ : Y⁻*q = 0 := by
    ext v
    exact Submodule.starProjection_apply_mem Y⁻.ker v
  have hZq : q*Y⁻ = 0 := by
    simpa only [star_mul,star_zero,hq.isSelfAdjoint.star_eq,
      (CFC.negPart_nonneg Y).isSelfAdjoint.star_eq] using congrArg star hqZ
  have hqpos : q*Y⁺ = Y⁺ := by
    ext v
    apply Submodule.starProjection_eq_self_iff.mpr
    change Y⁻ (Y⁺ v) = 0
    exact congrArg (fun A : H →L[ℂ] H => A v) (CFC.negPart_mul_posPart Y)
  have hposq : Y⁺*q = Y⁺ := by
    simpa only [star_mul,hq.isSelfAdjoint.star_eq,
      (CFC.posPart_nonneg Y).isSelfAdjoint.star_eq] using congrArg star hqpos
  have hposne : Y⁺ ≠ 0 := by
    intro hz
    have hy : X ≤ epsilon • (1 : H →L[ℂ] H) :=
      sub_nonpos.mp ((CFC.posPart_eq_zero_iff Y hYs).mp hz)
    have hn : ‖X‖ ≤ epsilon :=
      (CStarAlgebra.norm_le_iff_le_algebraMap X he.le hX).mpr
        (by simpa only [Algebra.algebraMap_eq_smul_one] using hy)
    dsimp [epsilon] at hn
    linarith [norm_pos_iff.mpr hXne]
  have hqne : q ≠ 0 := by
    intro hz
    rw [hz,zero_mul] at hqpos
    exact hposne hqpos.symm
  have hdecomp : X = (Y⁺-Y⁻)+epsilon • 1 := by
    rw [CFC.posPart_sub_negPart Y hYs]
    dsimp [Y]
    abel
  have hleft : q*X = Y⁺+epsilon • q := by
    rw [hdecomp,mul_add,mul_sub,hqpos,hZq,mul_smul_comm,mul_one,sub_zero]
  have hright : X*q = Y⁺+epsilon • q := by
    rw [hdecomp,add_mul,sub_mul,hposq,hqZ,smul_mul_assoc,one_mul,sub_zero]
  have hc : q*X = X*q := hleft.trans hright.symm
  have hqq : q*q=q := hq.isIdempotentElem
  have hcompressed : q*X*q = q*X := by
    rw [mul_assoc,← hc,← mul_assoc,hqq]
  have hbound : q*X*q ≤ X := by
    apply sub_nonneg.mp
    have hp := star_left_conjugate_nonneg hX (1-q)
    have hd : star (1-q)*X*(1-q) = X-q*X*q := by
      rw [hq.one_sub.isSelfAdjoint.star_eq]
      calc
        _ = X-q*X-X*q+q*X*q := by noncomm_ring
        _ = _ := by rw [← hc,hcompressed]; abel
    rwa [hd] at hp
  refine ⟨epsilon,q,he,hq,hqm,hqne,?_⟩
  apply le_trans _ hbound
  rw [hcompressed,hleft]
  exact le_add_of_nonneg_left (CFC.posPart_nonneg Y)

/-- Finiteness is obtained for A1's trace from its own finite positive seed.
No projection, spectral witness or finite Hilbert dimension is an input. -/
theorem scalarTrace_finite_subprojection_exists (P : SiteProfile)
    (e : PositiveCoreInput P) (heproj : IsStarProjection e.val)
    (hene : e ≠ PositiveCoreInput.zero P) :
    ∃ q : PositiveCoreInput P, IsStarProjection q.val ∧
      0 < scalarInverseLimitWeight P q ∧ scalarInverseLimitWeight P q < ⊤ ∧
      q.val * e.val = q.val := by
  obtain ⟨Y,hYle,hYpos,hYfin⟩ := regularTrace_finite_positive_below P
    (scalarInverseLimitTraceData.{0} P) e hene
  change 0 < scalarInverseLimitWeight P Y at hYpos
  change scalarInverseLimitWeight P Y < ⊤ at hYfin
  have hYne : Y.val ≠ 0 := by
    intro hz
    have hzero : Y = PositiveCoreInput.zero P := Subtype.ext hz
    rw [hzero,scalarInverseLimitWeight_zero] at hYpos
    exact lt_irrefl _ hYpos
  obtain ⟨epsilon,q,he,hq,hqm,hqne,hbound⟩ :=
    positive_operator_has_threshold_projection (regularCoreAlgebra P)
      Y.val Y.property.1 Y.property.2 hYne
  let Q : PositiveCoreInput P := ⟨q,hqm,hq.nonneg⟩
  have hQpos : 0 < scalarInverseLimitWeight P Q := by
    apply lt_of_le_of_ne zero_le
    intro hz
    have hzero := (scalarInverseLimitWeight_faithful P Q).mp hz.symm
    exact hqne (congrArg Subtype.val hzero)
  have hQfin : scalarInverseLimitWeight P Q < ⊤ := by
    have hl : scalarInverseLimitWeight P (Q.scale ⟨epsilon,he.le⟩) ≤
        scalarInverseLimitWeight P Y := scalarInverseLimitWeight_mono P _ _ hbound
    rw [scalarInverseLimitWeight_scale] at hl
    apply lt_top_iff_ne_top.mpr
    intro hinf
    rw [hinf,ENNReal.mul_top (by
      apply ENNReal.coe_ne_zero.mpr
      intro hz
      exact he.ne' (congrArg (fun r : ℝ≥0 => (r : ℝ)) hz))] at hl
    exact (not_le_of_gt hYfin) hl
  have hQe : q * e.val = q := by
    have hh := (heproj.mul_right_and_mul_left_of_nonneg_of_le
      (Q.scale ⟨epsilon,he.le⟩).property.2 (hbound.trans hYle)).1
    change (epsilon • q) * e.val = epsilon • q at hh
    rw [smul_mul_assoc] at hh
    exact smul_right_injective _ he.ne' hh
  exact ⟨Q,hq,hQpos,hQfin,hQe⟩

#print axioms positive_operator_has_threshold_projection
#print axioms scalarTrace_finite_subprojection_exists
end
end TGLV350.Regular
