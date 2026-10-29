import Mathlib.Analysis.VonNeumannAlgebra.Basic
import Mathlib.Analysis.Normed.Operator.Extend
import TGLExt.V350PositiveRootIntertwining
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.Rpow.Basic
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order

set_option autoImplicit false

namespace TGLV354
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

private def closedRangeMap (a : H →L[ℂ] H) : H →ₗ[ℂ] a.range.topologicalClosure :=
  a.toLinearMap.codRestrict a.range.topologicalClosure
    (fun x => a.range.le_topologicalClosure ⟨x,rfl⟩)

omit [CompleteSpace H] in
private theorem closedRangeMap_dense (a : H →L[ℂ] H) : DenseRange (closedRangeMap a) := by
  change DenseRange (Set.inclusion subset_closure ∘ Set.rangeFactorization a)
  exact ((denseRange_inclusion_iff subset_closure).2 subset_rfl).comp
    Set.rangeFactorization_surjective.denseRange (continuous_inclusion subset_closure)

/-- Extend the factor on the closure of the range and set it to zero on the orthogonal complement. -/
private def rangeFactor (T a : H →L[ℂ] H) : H →L[ℂ] H :=
  (T.toLinearMap.extendOfNorm (closedRangeMap a)).comp
    a.range.topologicalClosure.orthogonalProjectionOnto

private theorem rangeFactor_apply (T a : H →L[ℂ] H)
    (hn : ∀ x, ‖T x‖ = ‖a x‖) (x : H) : rangeFactor T a (a x) = T x := by
  have hp : a.range.topologicalClosure.orthogonalProjectionOnto (a x) = closedRangeMap a x := by
    apply Subtype.ext
    exact Submodule.starProjection_eq_self_iff.mpr
      (a.range.le_topologicalClosure ⟨x,rfl⟩)
  change T.toLinearMap.extendOfNorm (closedRangeMap a)
    (a.range.topologicalClosure.orthogonalProjectionOnto (a x)) = T x
  rw [hp]
  apply LinearMap.extendOfNorm_eq (closedRangeMap_dense a)
  exact ⟨1, fun x => by change ‖T x‖ ≤ 1*‖a x‖; simpa only [one_mul] using (hn x).le⟩

private theorem rangeFactor_norm (T a : H →L[ℂ] H)
    (hn : ∀ x, ‖T x‖ = ‖a x‖) (x : H) :
    ‖rangeFactor T a x‖ = ‖a.range.topologicalClosure.starProjection x‖ := by
  have he : ∀ y : a.range.topologicalClosure,
      ‖T.toLinearMap.extendOfNorm (closedRangeMap a) y‖ = ‖y‖ := by
    intro y
    refine (closedRangeMap_dense a).induction_on y ?_ ?_
    · exact isClosed_eq (Continuous.norm (ContinuousLinearMap.continuous _)) continuous_norm
    · intro z
      rw [LinearMap.extendOfNorm_eq (closedRangeMap_dense a)
        ⟨1,fun x => by change ‖T x‖ ≤ 1*‖a x‖; simpa only [one_mul] using (hn x).le⟩]
      exact hn z
  exact he _

/-- The absolute value of a bounded operator preserves its image norms. -/
theorem boundedAbsolute_norm (T : H →L[ℂ] H) (x : H) :
    ‖CFC.sqrt (star T*T) x‖ = ‖T x‖ := by
  let a := CFC.sqrt (star T*T)
  have hs : star a = a := (CFC.sqrt_nonneg _).isSelfAdjoint.star_eq
  have ha : star a*a = star T*T := by rw [hs]; exact CFC.sqrt_mul_sqrt_self _ (star_mul_self_nonneg _)
  have hi : inner ℂ (a x) (a x) = inner ℂ (T x) (T x) := by
    calc
      _ = inner ℂ ((star a*a) x) x := (a.adjoint_inner_left x (a x)).symm
      _ = inner ℂ ((star T*T) x) x := by rw [ha]
      _ = _ := T.adjoint_inner_left x (T x)
  have hn := congrArg (RCLike.re : ℂ → ℝ) hi
  simp only [inner_self_eq_norm_sq] at hn
  dsimp [a] at hn
  nlinarith [norm_nonneg (CFC.sqrt (star T*T) x),norm_nonneg (T x)]

/-- The polar factor is constructed by extension, with no partial-isometry premise. -/
def boundedPolar (T : H →L[ℂ] H) : H →L[ℂ] H :=
  rangeFactor T (CFC.sqrt (star T*T))

theorem boundedPolar_mul_absolute (T : H →L[ℂ] H) :
    boundedPolar T * CFC.sqrt (star T*T) = T := by
  ext x
  exact rangeFactor_apply T _ (fun x => (boundedAbsolute_norm T x).symm) x

private theorem boundedAbsolute_ker (T : H →L[ℂ] H) :
    (CFC.sqrt (star T*T)).ker = T.ker := by
  ext x
  change CFC.sqrt (star T*T) x=0 ↔ T x=0
  exact (norm_eq_zero.symm.trans ((boundedAbsolute_norm T x).congr_left.trans norm_eq_zero))

theorem boundedAbsolute_range (T : H →L[ℂ] H) :
    (CFC.sqrt (star T*T)).range.topologicalClosure = T.kerᗮ := by
  have h := (CFC.sqrt (star T*T)).orthogonal_ker
  rw [(CFC.sqrt_nonneg _).isSelfAdjoint.adjoint_eq, boundedAbsolute_ker] at h
  exact h.symm

theorem boundedPolar_norm (T : H →L[ℂ] H) (x : H) :
    ‖boundedPolar T x‖ = ‖T.kerᗮ.starProjection x‖ := by
  have h := rangeFactor_norm T (CFC.sqrt (star T*T))
    (fun x => (boundedAbsolute_norm T x).symm) x
  simpa only [boundedPolar,boundedAbsolute_range] using h

theorem boundedPolar_apply_eq_zero_iff (T : H →L[ℂ] H) (x : H) :
    boundedPolar T x = 0 ↔ T x = 0 := by
  rw [← norm_eq_zero,boundedPolar_norm,norm_eq_zero,
    Submodule.starProjection_apply_eq_zero_iff,Submodule.orthogonal_orthogonal]
  rfl

theorem boundedPolar_star_mul (T : H →L[ℂ] H) :
    star (boundedPolar T)*boundedPolar T = T.kerᗮ.starProjection := by
  let p := T.kerᗮ.starProjection
  have hp : star p*p=p := by
    rw [isSelfAdjoint_starProjection T.kerᗮ |>.star_eq]
    exact Submodule.isIdempotentElem_starProjection _
  change star (boundedPolar T)*boundedPolar T=p
  rw [← hp]
  apply ContinuousLinearMap.coe_injective
  apply (ext_inner_map _ _).mp
  intro x
  change inner ℂ ((star (boundedPolar T)) (boundedPolar T x)) x = inner ℂ ((star p) (p x)) x
  calc
    _ = inner ℂ (boundedPolar T x) (boundedPolar T x) :=
      (boundedPolar T).adjoint_inner_left x (boundedPolar T x)
    _ = inner ℂ (p x) (p x) := by
      rw [inner_self_eq_norm_sq_to_K,inner_self_eq_norm_sq_to_K,boundedPolar_norm]
    _ = _ := (p.adjoint_inner_left x (p x)).symm

theorem boundedPolar_initial_support (T : H →L[ℂ] H) :
    boundedPolar T * T.kerᗮ.starProjection = boundedPolar T := by
  ext x
  have hz : boundedPolar T (x-T.kerᗮ.starProjection x) = 0 := by
    apply norm_eq_zero.mp
    rw [boundedPolar_norm,map_sub]
    have hp : T.kerᗮ.starProjection (T.kerᗮ.starProjection x) = T.kerᗮ.starProjection x :=
      Submodule.starProjection_eq_self_iff.mpr (Submodule.starProjection_apply_mem _ _)
    rw [hp,sub_self,norm_zero]
  rw [map_sub,sub_eq_zero] at hz
  exact hz.symm

private theorem boundedPolar_range_le (T : H →L[ℂ] H) :
    (boundedPolar T).range ≤ T.range.topologicalClosure := by
  let a := CFC.sqrt (star T*T)
  have he : ∀ y : a.range.topologicalClosure,
      T.toLinearMap.extendOfNorm (closedRangeMap a) y ∈ T.range.topologicalClosure := by
    intro y
    refine (closedRangeMap_dense a).induction_on y ?_ ?_
    · exact (Submodule.isClosed_topologicalClosure _).preimage
        (ContinuousLinearMap.continuous _)
    · intro z
      rw [LinearMap.extendOfNorm_eq (closedRangeMap_dense a)
        ⟨1,fun x => by change ‖T x‖ ≤ 1*‖a x‖; simpa only [one_mul] using (boundedAbsolute_norm T x).symm.le⟩]
      exact T.range.le_topologicalClosure ⟨z,rfl⟩
  rintro x ⟨y,rfl⟩
  exact he _

/-- Both support projections are computed from the actual operator. -/
theorem boundedPolar_mul_star (T : H →L[ℂ] H) :
    boundedPolar T * star (boundedPolar T) = T.range.topologicalClosure.starProjection := by
  let u := boundedPolar T
  let q := u*star u
  have hq : IsStarProjection q := by
    constructor
    · change (u*star u)*(u*star u)=u*star u
      calc
        _ = (u*(star u*u))*star u := by noncomm_ring
        _ = _ := by rw [boundedPolar_star_mul,boundedPolar_initial_support]
    · change star (u*star u)=u*star u
      simp only [star_mul,star_star]
  have hqr : q.range = u.range := by
    apply le_antisymm
    · rintro x ⟨y,rfl⟩; exact ⟨star u y,rfl⟩
    · rintro x ⟨y,rfl⟩
      refine ⟨u y,?_⟩
      have h : q*u=u := by
        change (u*star u)*u=u
        rw [mul_assoc,boundedPolar_star_mul,boundedPolar_initial_support]
      exact congrArg (fun B : H →L[ℂ] H => B y) h
  have hr : q.range = T.range.topologicalClosure := by
    apply le_antisymm
    · rw [hqr]; exact boundedPolar_range_le T
    · apply Submodule.topologicalClosure_minimal
      · rintro x ⟨y,rfl⟩
        rw [hqr]
        refine ⟨CFC.sqrt (star T*T) y,?_⟩
        exact congrArg (fun B : H →L[ℂ] H => B y) (boundedPolar_mul_absolute T)
      · exact ContinuousLinearMap.IsIdempotentElem.isClosed_range hq.isIdempotentElem
  obtain ⟨hp,he⟩ := isStarProjection_iff_eq_starProjection_range.mp hq
  simpa only [hr] using he

/-- Commutation is transported through the constructed polar factor. -/
theorem boundedPolar_commutes (T B : H →L[ℂ] H)
    (hT : Commute T B) (hstar : Commute (star T) B) :
    Commute (boundedPolar T) B := by
  let a := CFC.sqrt (star T*T)
  let u := boundedPolar T
  let C := u*B-B*u
  have ha : Commute a B :=
    TGLV350.Regular.positive_sqrt_intertwines (star T*T) (star T*T) B
      (star_mul_self_nonneg T) (star_mul_self_nonneg T) (hstar.mul_left hT).eq
  have hC : C*a=0 := by
    calc
      _ = u*(B*a)-B*(u*a) := by dsimp [C]; noncomm_ring
      _ = u*(a*B)-B*(u*a) := by rw [ha.eq]
      _ = (u*a)*B-B*(u*a) := by noncomm_ring
      _ = 0 := by rw [boundedPolar_mul_absolute,hT.eq,sub_self]
  have hcR : T.kerᗮ ≤ C.ker := by
    rw [← boundedAbsolute_range]
    apply Submodule.topologicalClosure_minimal
    · rintro x ⟨y,rfl⟩
      exact congrArg (fun A : H →L[ℂ] H => A y) hC
    · exact C.isClosed_ker
  have hu : ∀ x ∈ T.ker, u x=0 := by
    intro x hx
    exact (boundedPolar_apply_eq_zero_iff T x).mpr hx
  have hcK : T.ker ≤ C.ker := by
    intro x hx
    have hb : B x ∈ T.ker := by
      change T (B x)=0
      have h := congrArg (fun A : H →L[ℂ] H => A x) hT.eq
      change T (B x)=B (T x) at h
      rw [h,show T x=0 from hx,map_zero]
    change u (B x)-B (u x)=0
    rw [hu _ hb,hu _ hx,map_zero,sub_self]
  have hall : (⊤ : Submodule ℂ H) ≤ C.ker := by
    rw [← T.ker.isCompl_orthogonal.sup_eq_top]
    exact sup_le hcK hcR
  change u*B=B*u
  ext x
  exact sub_eq_zero.mp (hall (Submodule.mem_top : x ∈ (⊤ : Submodule ℂ H)))

/-- A bounded operator in N has its constructed polar factor in the same N. -/
theorem boundedPolar_mem (N : VonNeumannAlgebra H) (T : H →L[ℂ] H) (hT : T ∈ N) :
    boundedPolar T ∈ N := by
  rw [← N.commutant_commutant]
  apply VonNeumannAlgebra.mem_commutant_iff.mpr
  intro B hB
  have hc := VonNeumannAlgebra.mem_commutant_iff.mp hB
  exact (boundedPolar_commutes T B (hc T hT)
    (hc (star T) (N.toStarSubalgebra.star_mem' hT))).eq.symm

#print axioms boundedAbsolute_norm
#print axioms boundedAbsolute_range
#print axioms boundedPolar
#print axioms boundedPolar_mul_absolute
#print axioms boundedPolar_norm
#print axioms boundedPolar_apply_eq_zero_iff
#print axioms boundedPolar_star_mul
#print axioms boundedPolar_initial_support
#print axioms boundedPolar_mul_star
#print axioms boundedPolar_commutes
#print axioms boundedPolar_mem
end
end TGLV354
