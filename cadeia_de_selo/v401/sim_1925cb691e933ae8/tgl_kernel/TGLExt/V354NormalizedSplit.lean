import TGLExt.V354FiniteEqualSplit

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt TGLV351
noncomputable section

/-- The scalar calculation of VerbInhabitant.dual_calibration_exists, now
applied to A1's positive trace. The legacy theorem already requires complete
ThreeLocks, so applying it here would make the construction circular. -/
theorem scalarTrace_dual_calibration (P : SiteProfile) (X : PositiveCoreInput P)
    (hpos : 0 < scalarInverseLimitWeight P X)
    (hfin : scalarInverseLimitWeight P X < ⊤) :
    scalarInverseLimitWeight P
      (positiveDual P (Real.log (scalarInverseLimitWeight P X).toReal) X) = 1 := by
  rw [scalarInverseLimitWeight_dual]
  have hx0 := hpos.ne'
  have hxt := hfin.ne
  have hxr := ENNReal.toReal_pos hx0 hxt
  rw [Real.exp_neg,Real.exp_log hxr,ENNReal.ofReal_inv_of_pos hxr,
    ENNReal.ofReal_toReal hxt]
  exact ENNReal.inv_mul_cancel hx0 hxt

/-- The total support is calibrated by the ACTUAL dual action; the two faces
are transported together. Its trace is one, not its Hilbert dimension. -/
theorem scalarTrace_normalized_split_exists (P : SiteProfile) :
    ∃ q r : PositiveCoreInput P,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      scalarInverseLimitWeight P (q.add r) = 1 ∧
      scalarInverseLimitWeight P q = scalarInverseLimitWeight P r := by
  obtain ⟨q,r,hq,hr,hqr,_,hpos,hfin,ht,_⟩ := scalarTrace_finite_split_support P
  let s := Real.log (scalarInverseLimitWeight P (q.add r)).toReal
  let Q := positiveDual P s q
  let R := positiveDual P s r
  have hQ : IsStarProjection Q.val := hq.map (dualAmbient s)
  have hR : IsStarProjection R.val := hr.map (dualAmbient s)
  have hQR : Q.val*R.val=0 := by
    change dualAmbient s q.val * dualAmbient s r.val = 0
    rw [← map_mul,hqr,map_zero]
  have hadd : Q.add R = positiveDual P s (q.add r) := by
    apply Subtype.ext
    change dualAmbient s q.val + dualAmbient s r.val = dualAmbient s (q.val+r.val)
    exact (map_add (dualAmbient s) q.val r.val).symm
  refine ⟨Q,R,hQ,hR,hQR,?_,?_⟩
  · rw [hadd]
    exact scalarTrace_dual_calibration P (q.add r) hpos hfin
  · change scalarInverseLimitWeight P (positiveDual P s q) =
      scalarInverseLimitWeight P (positiveDual P s r)
    rw [scalarInverseLimitWeight_dual,scalarInverseLimitWeight_dual,ht]

#print axioms scalarTrace_dual_calibration
#print axioms scalarTrace_normalized_split_exists
end
end TGLV350.Regular
