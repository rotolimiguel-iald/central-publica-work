import TGLExt.V354RegularMatrixCorner

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt TGLV351
noncomputable section

/-- Two orthogonal finite projections, with equal positive A1 trace, constructed
inside the regular core. The equality is A1 quadratic traciality applied to vq. -/
theorem scalarTrace_finite_equal_split (P : SiteProfile) :
    ∃ q r : PositiveCoreInput P,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val * r.val = 0 ∧
      scalarInverseLimitWeight P q = scalarInverseLimitWeight P r ∧
      0 < scalarInverseLimitWeight P q ∧ scalarInverseLimitWeight P q < ⊤ := by
  obtain ⟨e,v,he,hene,hv,hev⟩ := regularCore_matrix_corner P
  obtain ⟨q,hq,hpos,hfin,hqe⟩ := scalarTrace_finite_subprojection_exists P e he hene
  let a : (regularCoreAlgebra P).toStarSubalgebra := v * ⟨q.val,q.property.1⟩
  have hqs := hq.isSelfAdjoint.star_eq
  have hqq : q.val*q.val=q.val := hq.isIdempotentElem
  have ha2 : star a.val * a.val = q.val := by
    change star (v.val*q.val)*(v.val*q.val)=q.val
    calc
      _ = q.val*(star v.val*v.val)*q.val := by rw [star_mul,hqs]; noncomm_ring
      _ = q.val := by rw [hv,hqe,hqq]
  have haq : a.val*q.val=a.val := by
    change (v.val*q.val)*q.val=v.val*q.val
    rw [mul_assoc,hqq]
  have hqv : q.val*v.val=0 := by
    calc
      _ = (q.val*e.val)*v.val := by rw [hqe]
      _ = 0 := by rw [mul_assoc,hev,mul_zero]
  have hqa : q.val*a.val=0 := by
    change q.val*(v.val*q.val)=0
    rw [← mul_assoc,hqv,zero_mul]
  let r := positiveSquare P (star a)
  have hrv : r.val = a.val*star a.val := by
    simp only [r,positiveSquare,StarMemClass.coe_star,star_star]
  have hr : IsStarProjection r.val := by
    constructor
    · change r.val*r.val=r.val
      rw [hrv]
      calc
        _ = a.val*(star a.val*a.val)*star a.val := by noncomm_ring
        _ = a.val*star a.val := by rw [ha2,haq]
    · exact r.property.2.isSelfAdjoint
  have hqr : q.val*r.val=0 := by
    rw [hrv,← mul_assoc,hqa,zero_mul]
  have ht : scalarInverseLimitWeight P q = scalarInverseLimitWeight P r := by
    have hA : positiveSquare P a = q := Subtype.ext ha2
    simpa only [hA] using scalarInverseLimitWeight_tracial P a
  exact ⟨q,r,hq,hr,hqr,ht,hpos,hfin⟩

/-- The sum is a nonzero finite projection with two equal positive faces. -/
theorem scalarTrace_finite_split_support (P : SiteProfile) :
    ∃ q r : PositiveCoreInput P,
      IsStarProjection q.val ∧ IsStarProjection r.val ∧ q.val*r.val=0 ∧
      IsStarProjection (q.add r).val ∧
      0 < scalarInverseLimitWeight P (q.add r) ∧
      scalarInverseLimitWeight P (q.add r) < ⊤ ∧
      scalarInverseLimitWeight P q = scalarInverseLimitWeight P r ∧
      0 < scalarInverseLimitWeight P q := by
  obtain ⟨q,r,hq,hr,hqr,ht,hpos,hfin⟩ := scalarTrace_finite_equal_split P
  refine ⟨q,r,hq,hr,hqr,hq.add hr hqr,?_,?_,ht,hpos⟩
  · rw [scalarInverseLimitWeight_add]
    exact hpos.trans_le (le_add_right le_rfl)
  · rw [scalarInverseLimitWeight_add,← ht]
    exact ENNReal.add_lt_top.mpr ⟨hfin,hfin⟩

#print axioms scalarTrace_finite_equal_split
#print axioms scalarTrace_finite_split_support
end
end TGLV350.Regular
