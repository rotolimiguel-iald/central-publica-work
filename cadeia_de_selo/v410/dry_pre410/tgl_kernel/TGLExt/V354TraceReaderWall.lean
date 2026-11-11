import TGLExt.V354PositiveTraceReader

set_option autoImplicit false

namespace TGLV350.Regular
open TGLExt TGLV351
noncomputable section

/-- Zero extension of A1's positive trace is NOT a cyclic function on all N.
This wall prevents the corner reader from being silently reused as the
canonicalTrace field of legacy ContinuousCoreData. It does not prove that
every possible compatible total extension is impossible. -/
theorem positiveTraceReader_not_cyclic (P : SiteProfile) :
    ¬ ∀ x y : (regularCoreAlgebra P).toStarSubalgebra,
      positiveTraceReader P (x*y) = positiveTraceReader P (y*x) := by
  obtain ⟨e,v,he,hene,hv,hev⟩ := regularCore_matrix_corner P
  have hes := he.isSelfAdjoint.star_eq
  have hee : e.val*e.val=e.val := he.isIdempotentElem
  have hvne : v.val ≠ 0 := by
    intro hz
    apply hene
    apply Subtype.ext
    change e.val = 0
    simpa only [hz,star_zero,zero_mul] using hv.symm
  have hve : v.val*e.val=v.val := by
    have hh : star (v.val-v.val*e.val)*(v.val-v.val*e.val)=0 := by
      calc
        _ = star v.val*v.val - (star v.val*v.val)*e.val -
            e.val*(star v.val*v.val) + e.val*(star v.val*v.val)*e.val := by
              rw [star_sub,star_mul,hes]
              noncomm_ring
        _ = 0 := by rw [hv,hee]; noncomm_ring [hee]
    exact (sub_eq_zero.mp ((CStarRing.star_mul_self_eq_zero_iff _).mp hh)).symm
  have hvse : star v.val*e.val=0 := by
    simpa only [star_mul,hes,star_zero] using congrArg star hev
  have hesv : e.val*star v.val=star v.val := by
    simpa only [star_mul,hes] using congrArg star hve
  have hbad : ¬ 0 ≤ e.val+star v.val := by
    intro hp
    have hs := hp.isSelfAdjoint.star_eq
    rw [star_add,hes,star_star] at hs
    have hvs : v.val=star v.val := add_left_cancel hs
    apply hvne
    calc
      _ = e.val*v.val := by rw [hvs,hesv]
      _ = 0 := hev
  let Y : (regularCoreAlgebra P).toStarSubalgebra := ⟨e.val,e.property.1⟩
  let X := Y + star v
  have hXY : X*Y=Y := by
    apply Subtype.ext
    change (e.val+star v.val)*e.val=e.val
    rw [add_mul,hee,hvse,add_zero]
  have hYX : (Y*X).val=e.val+star v.val := by
    change e.val*(e.val+star v.val)=e.val+star v.val
    rw [mul_add,hee,hesv]
  intro hc
  have hh := hc X Y
  rw [hXY] at hh
  have hy : positiveTraceReader P Y = scalarInverseLimitWeight P e :=
    positiveTraceReader_positive P e
  rw [hy] at hh
  have hz : positiveTraceReader P (Y*X)=0 := by
    unfold positiveTraceReader
    rw [dif_neg (by rwa [hYX])]
  rw [hz] at hh
  exact hene ((scalarInverseLimitWeight_faithful P e).mp hh)

#print axioms positiveTraceReader_not_cyclic
end
end TGLV350.Regular
