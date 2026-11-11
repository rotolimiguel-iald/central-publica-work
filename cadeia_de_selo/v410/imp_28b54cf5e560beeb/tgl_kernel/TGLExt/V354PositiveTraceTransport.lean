import TGLExt.V351RegularCoreTraceConstruction
import TGLExt.V350PositiveRootIntertwining

set_option autoImplicit false

namespace TGLV354.TraceCompletion
open TGLExt TGLV350.Regular TGLV351
noncomputable section

private theorem transport_square_pair {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : VonNeumannAlgebra H) (p q u : N.toStarSubalgebra) (hq : 0 ≤ q.val)
    (htransport : p.val = u.val*q.val*star u.val)
    (hsupport : (star u.val*u.val)*q.val = q.val) :
    ∃ a : N.toStarSubalgebra,
      star a.val*a.val=q.val ∧ a.val*star a.val=p.val := by
  let e := star u.val*u.val
  let d := CFC.sqrt q.val
  have hqs := hq.isSelfAdjoint.star_eq
  have hqe : q.val*e=q.val := by
    have h := congrArg star hsupport
    simpa only [star_mul,hqs,star_star] using h
  have hzero : q.val*(e-1)=(e-1)*0 := by
    rw [mul_sub,hqe,mul_one,sub_self,mul_zero]
  have hroot : d*(e-1)=0 := by
    have h := positive_sqrt_intertwines q.val 0 (e-1) hq le_rfl hzero
    simpa only [CFC.sqrt_zero,mul_zero] using h
  have hde : d*e=d := by
    rw [mul_sub,mul_one,sub_eq_zero] at hroot
    exact hroot
  letI : IsClosed (N.toStarSubalgebra : Set (H →L[ℂ] H)) := vonNeumann_norm_closed N
  have hdmem : d ∈ N := by
    dsimp [d]
    rw [CFC.sqrt_eq_real_sqrt q.val hq]
    exact cfcₙ_mem (𝕜' := ℂ) (s := N.toStarSubalgebra) Real.sqrt q.property
  let a : N.toStarSubalgebra := u*⟨d,hdmem⟩
  have hds : star d=d := (CFC.sqrt_nonneg q.val).isSelfAdjoint.star_eq
  have hdd : d*d=q.val := CFC.sqrt_mul_sqrt_self q.val hq
  have haa : star a.val*a.val=q.val := by
    change star (u.val*d)*(u.val*d)=q.val
    calc
      _ = d*(star u.val*u.val)*d := by rw [star_mul,hds]; noncomm_ring
      _ = d*d := by rw [hde]
      _ = q.val := hdd
  have haa' : a.val*star a.val=p.val := by
    change (u.val*d)*star (u.val*d)=p.val
    calc
      _ = u.val*(d*d)*star u.val := by rw [star_mul,hds]; noncomm_ring
      _ = p.val := by rw [hdd,← htransport]
  exact ⟨a,haa,haa'⟩

/-- The final analytic step consumes A1 quadratic traciality, not a hypothetical
cyclic trace. The transporting operator belongs to the SAME core. -/
theorem scalarTrace_transport_of_support (P : SiteProfile)
    (p q : PositiveCoreInput P) (u : (regularCoreAlgebra P).toStarSubalgebra)
    (htransport : p.val = u.val*q.val*star u.val)
    (hsupport : (star u.val*u.val)*q.val = q.val) :
    scalarInverseLimitWeight P p = scalarInverseLimitWeight P q := by
  obtain ⟨a,haa,haa'⟩ := transport_square_pair (regularCoreAlgebra P)
    ⟨p.val,p.property.1⟩ ⟨q.val,q.property.1⟩ u q.property.2 htransport hsupport
  have hq : positiveSquare P a=q := Subtype.ext haa
  have hp : positiveSquare P (star a)=p := by
    apply Subtype.ext
    simpa only [positiveSquare,StarMemClass.coe_star,star_star] using haa'
  have ht := scalarInverseLimitWeight_tracial P a
  rw [hq,hp] at ht
  exact ht.symm

#print axioms scalarTrace_transport_of_support
end
end TGLV354.TraceCompletion
