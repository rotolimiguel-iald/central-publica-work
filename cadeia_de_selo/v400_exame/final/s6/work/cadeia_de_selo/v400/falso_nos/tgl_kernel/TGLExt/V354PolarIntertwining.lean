import TGLExt.V354BoundedPolar
import TGLExt.V354SelfAdjointPowerKernel

set_option autoImplicit false

namespace TGLV354.TraceCompletion
open TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Transport through the constructed polar uses density on the initial
support, not an inverse of the possibly singular absolute value. -/
theorem boundedPolar_intertwines (A B r : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (hr : A*r=r*B) (hkr : r.ker ≤ B.ker) :
    A*boundedPolar r=boundedPolar r*B := by
  let d := CFC.sqrt (star r*r)
  let u := boundedPolar r
  let C := A*u-u*B
  have hstar : star r*A=B*star r := by
    have h := congrArg star hr
    simpa only [star_mul,hA.star_eq,hB.star_eq] using h
  have hcomm : (star r*r)*B=B*(star r*r) := by
    calc
      _ = star r*(r*B) := mul_assoc _ _ _
      _ = star r*(A*r) := by rw [hr]
      _ = (star r*A)*r := (mul_assoc _ _ _).symm
      _ = (B*star r)*r := by rw [hstar]
      _ = _ := mul_assoc _ _ _
  have hd : d*B=B*d :=
    positive_sqrt_intertwines (star r*r) (star r*r) B
      (star_mul_self_nonneg r) (star_mul_self_nonneg r) hcomm
  have hC : C*d=0 := by
    calc
      _ = A*(u*d)-u*(B*d) := by dsimp only [C]; noncomm_ring
      _ = A*(u*d)-u*(d*B) := by rw [hd]
      _ = A*(u*d)-(u*d)*B := by noncomm_ring
      _ = 0 := by rw [boundedPolar_mul_absolute,hr,sub_self]
  have hcR : r.kerᗮ ≤ C.ker := by
    rw [← boundedAbsolute_range]
    apply Submodule.topologicalClosure_minimal
    · rintro x ⟨y,rfl⟩
      exact congrArg (fun T : H →L[ℂ] H => T y) hC
    · exact C.isClosed_ker
  have hcK : r.ker ≤ C.ker := by
    intro x hx
    have hu : u x=0 := (boundedPolar_apply_eq_zero_iff r x).mpr hx
    have hb : B x=0 := hkr hx
    change A (u x)-u (B x)=0
    rw [hu,hb,map_zero,map_zero,sub_self]
  have hall : (⊤ : Submodule ℂ H) ≤ C.ker := by
    rw [← r.ker.isCompl_orthogonal.sup_eq_top]
    exact sup_le hcK hcR
  ext x
  exact sub_eq_zero.mp (hall (Submodule.mem_top : x ∈ (⊤ : Submodule ℂ H)))

/-- The actual polar provides the two support equations needed to consume
the positive trace. Equality of the full polar supports is not assumed. -/
theorem boundedPolar_transports_shift_factors (A B r s : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B)
    (n : ℕ) (hn : 0 < n) (hr : A*r=r*B)
    (hArs : A ^ n=r*s) (hBsr : B ^ n=s*r) :
    A=boundedPolar r*B*star (boundedPolar r) ∧
      (star (boundedPolar r)*boundedPolar r)*B=B := by
  obtain ⟨hk,hR⟩ := selfAdjoint_factor_supports A B r s hA hB n hn hArs hBsr
  have hu := boundedPolar_intertwines A B r hA hB hr hk
  have hBinitial : (star (boundedPolar r)*boundedPolar r)*B=B := by
    rw [boundedPolar_star_mul]
    ext x
    apply Submodule.starProjection_eq_self_iff.mpr
    have hx : B x ∈ B.kerᗮ := by
      rw [B.orthogonal_ker,hB.adjoint_eq]
      exact B.range.le_topologicalClosure ⟨x,rfl⟩
    exact Submodule.orthogonal_le hk hx
  have hAfinal : (boundedPolar r*star (boundedPolar r))*A=A := by
    rw [boundedPolar_mul_star]
    ext x
    apply Submodule.starProjection_eq_self_iff.mpr
    exact hR (A.range.le_topologicalClosure ⟨x,rfl⟩)
  have hAfinal' : A*(boundedPolar r*star (boundedPolar r))=A := by
    have h := congrArg star hAfinal
    simpa only [star_mul,hA.star_eq,star_star] using h
  refine ⟨?_,hBinitial⟩
  calc
    A = A*(boundedPolar r*star (boundedPolar r)) := hAfinal'.symm
    _ = (A*boundedPolar r)*star (boundedPolar r) := (mul_assoc _ _ _).symm
    _ = _ := by rw [hu]

#print axioms boundedPolar_intertwines
#print axioms boundedPolar_transports_shift_factors
end
end TGLV354.TraceCompletion
