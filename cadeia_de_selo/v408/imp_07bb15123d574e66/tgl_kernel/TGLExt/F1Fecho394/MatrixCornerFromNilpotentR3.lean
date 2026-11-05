import TGLExt.V354BoundedPolar

/-! R50 auxiliary candidate. Reuse the actual bounded polar factor to extract
an orthogonal matrix corner from a nonzero square-zero operator in the same
von Neumann algebra. This is an auxiliary implication, not yet a concrete
Fock supplier: construction of the square-zero operator remains required.
No trace, finiteness, factor type or matrix embedding is hypothesized here.
The finite positive trace and its split are separate consumers. -/
set_option autoImplicit false
set_option Elab.async false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.MatrixCornerFromNilpotent
open TGLV354
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Square-zero forces the closed range into the kernel. -/
theorem rangeClosure_le_ker (T : H →L[ℂ] H) (hTT : T*T=0) :
    T.range.topologicalClosure ≤ T.ker := by
  apply Submodule.topologicalClosure_minimal
  · rintro x ⟨y,rfl⟩
    exact congrArg (fun A : H →L[ℂ] H => A y) hTT
  · exact T.isClosed_ker
#print axioms rangeClosure_le_ker

/-- The polar has the same closed range; this support identity uses only
the already constructed polar, not a chosen partial isometry. -/
theorem polar_range_support (T : H →L[ℂ] H) :
    T.range.topologicalClosure.starProjection * boundedPolar T = boundedPolar T := by
  rw [← boundedPolar_mul_star, mul_assoc, boundedPolar_star_mul,
    boundedPolar_initial_support]
#print axioms polar_range_support

theorem initial_support_mul_polar_zero (T : H →L[ℂ] H) (hTT : T*T=0) :
    T.kerᗮ.starProjection * boundedPolar T = 0 := by
  ext x
  change T.kerᗮ.starProjection (boundedPolar T x) = 0
  rw [Submodule.starProjection_apply_eq_zero_iff]
  have hr : boundedPolar T x ∈ T.range.topologicalClosure := by
    have hs := congrArg (fun A : H →L[ℂ] H => A x) (polar_range_support T)
    rw [← hs]
    exact Submodule.starProjection_apply_mem _ _
  have hk := rangeClosure_le_ker T hTT hr
  simpa only [Submodule.orthogonal_orthogonal] using hk
#print axioms initial_support_mul_polar_zero

/-- A nonzero square-zero element supplies exactly the corner used by the
finite-split construction. Existence of such an element in the Fock core
is not asserted by this auxiliary theorem. -/
theorem matrix_corner_of_square_zero (N : VonNeumannAlgebra H)
    (T : H →L[ℂ] H) (hTm : T ∈ N) (hT : T ≠ 0) (hTT : T*T=0) :
    ∃ (e v : H →L[ℂ] H), e ∈ N ∧ v ∈ N ∧ IsStarProjection e ∧
      e ≠ 0 ∧ star v * v = e ∧ e * v = 0 := by
  let v := boundedPolar T
  let e := T.kerᗮ.starProjection
  have hvm : v ∈ N := boundedPolar_mem N T hTm
  have hve : star v*v=e := boundedPolar_star_mul T
  have hem : e ∈ N := by
    rw [← hve]
    exact N.mul_mem (N.toStarSubalgebra.star_mem' hvm) hvm
  have hen : e ≠ 0 := by
    intro he
    have hu : v=0 := by
      have hs : v*e=v := boundedPolar_initial_support T
      rw [he,mul_zero] at hs
      exact hs.symm
    apply hT
    have ht := boundedPolar_mul_absolute T
    change v * CFC.sqrt (star T*T)=T at ht
    rw [hu,zero_mul] at ht
    exact ht.symm
  exact ⟨e,v,hem,hvm,isStarProjection_starProjection,hen,hve,
    initial_support_mul_polar_zero T hTT⟩
#print axioms matrix_corner_of_square_zero
end F1Fecho.MatrixCornerFromNilpotent
