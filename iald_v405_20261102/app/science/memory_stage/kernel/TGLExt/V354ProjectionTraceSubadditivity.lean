import TGLExt.V354CoreProjectionLattice
import TGLExt.V354BoundedPolar

set_option autoImplicit false

namespace TGLV354
open TGLExt TGLV350.Regular TGLV351
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The polar factor of (1-q)p gives the Kaplansky comparison needed for subadditivity. -/
theorem projection_join_comparison (N : VonNeumannAlgebra H) (p q : CoreProjection N) :
    ∃ u : H →L[ℂ] H, u ∈ N ∧
      star u*u ≤ p.operator ∧ u*star u = (p ⊔ q).operator-q.operator := by
  let P := p.operator
  let Q := q.operator
  let R := (p ⊔ q).operator
  let A := (1-Q)*P
  let F := R-Q
  have hp : IsStarProjection P := isStarProjection_starProjection
  have hq : IsStarProjection Q := isStarProjection_starProjection
  have hr : IsStarProjection R := isStarProjection_starProjection
  have hPR : P*R=P := (hp.le_iff_mul_eq_left hr).mp
    ((CoreProjection.operator_le_iff p (p ⊔ q)).mpr le_sup_left)
  have hQR : Q*R=Q := (hq.le_iff_mul_eq_left hr).mp
    ((CoreProjection.operator_le_iff q (p ⊔ q)).mpr le_sup_right)
  have hRQ : R*Q=Q := (hq.le_iff_mul_eq_right hr).mp
    ((CoreProjection.operator_le_iff q (p ⊔ q)).mpr le_sup_right)
  have hf : IsStarProjection F := hq.sub_of_mul_eq_left hr hQR
  have hsA : star A=P*(1-Q) := by
    simp only [A,star_mul,star_sub,star_one,hp.isSelfAdjoint.star_eq,hq.isSelfAdjoint.star_eq]
  have hAF : star A*F=star A := by
    rw [hsA]
    dsimp [F]
    calc
      _ = P*R-P*(Q*R)-P*Q+P*(Q*Q) := by noncomm_ring
      _ = _ := by rw [hPR,hQR,hq.isIdempotentElem]; noncomm_ring
  have hker : (star A).ker=F.ker := by
    ext x
    constructor
    · intro hx
      have hpz : P (x-Q x)=0 := by
        have h := hx
        change (star A) x=0 at h
        rw [hsA] at h
        exact h
      have hqz : Q (x-Q x)=0 := by
        have hqq := congrArg (fun B : H →L[ℂ] H => B x) hq.isIdempotentElem
        simpa only [map_sub,ContinuousLinearMap.mul_apply,sub_eq_zero] using hqq.symm
      have hz : R (x-Q x)=0 := CoreProjection.sup_apply_eq_zero p q _ hpz hqz
      have hrqx := congrArg (fun B : H →L[ℂ] H => B x) hRQ
      change R (Q x)=Q x at hrqx
      change R x-Q x=0
      simpa only [map_sub,hrqx] using hz
    · intro hx
      have h := congrArg (fun B : H →L[ℂ] H => B x) hAF
      change (star A) (F x)=(star A) x at h
      rw [show F x=0 from hx,map_zero] at h
      exact h.symm
  have hfinal : boundedPolar A*star (boundedPolar A)=F := by
    rw [boundedPolar_mul_star]
    have hclosure : A.range.topologicalClosure=F.range := by
      have h1 := (star A).orthogonal_ker
      have h2 := F.orthogonal_ker
      change (star A).kerᗮ = (star (star A)).range.topologicalClosure at h1
      change F.kerᗮ = (star F).range.topologicalClosure at h2
      rw [star_star,hker] at h1
      rw [hf.isSelfAdjoint.star_eq] at h2
      have hclosed := ContinuousLinearMap.IsIdempotentElem.isClosed_range hf.isIdempotentElem
      calc
        _ = F.kerᗮ := h1.symm
        _ = F.range.topologicalClosure := h2
        _ = F.range := hclosed.submodule_topologicalClosure_eq
    obtain ⟨hfp,he⟩ := isStarProjection_iff_eq_starProjection_range.mp hf
    simpa only [hclosure] using he.symm
  have hAP : A*(1-P)=0 := by
    dsimp [A]
    rw [mul_assoc,hp.mul_one_sub_self,mul_zero]
  have huP : boundedPolar A*P=boundedPolar A := by
    ext x
    have hz : boundedPolar A (x-P x)=0 :=
      (boundedPolar_apply_eq_zero_iff A _).mpr
        (congrArg (fun B : H →L[ℂ] H => B x) hAP)
    rw [map_sub,sub_eq_zero] at hz
    exact hz.symm
  have hinit : star (boundedPolar A)*boundedPolar A ≤ P := by
    have he : IsStarProjection (star (boundedPolar A)*boundedPolar A) := by
      rw [boundedPolar_star_mul]; exact isStarProjection_starProjection
    apply (he.le_iff_mul_eq_left hp).mpr
    rw [mul_assoc,huP]
  exact ⟨boundedPolar A,boundedPolar_mem N A
    (N.mul_mem (N.sub_mem N.one_mem q.operator_mem) p.operator_mem),hinit,hfinal⟩

/-- Subadditivity uses the actual A1 trace and a partial isometry in the same N. -/
theorem coreProjectionTrace_subadd (P : SiteProfile)
    (p q : CoreProjection (regularCoreAlgebra P)) :
    (coreProjectionTrace P).tau (p ⊔ q) ≤
      (coreProjectionTrace P).tau p + (coreProjectionTrace P).tau q := by
  obtain ⟨u,hum,hule,huf⟩ := projection_join_comparison (regularCoreAlgebra P) p q
  let U : (regularCoreAlgebra P).toStarSubalgebra := ⟨u,hum⟩
  let E := positiveSquare P U
  let F := positiveSquare P (star U)
  have hFE : scalarInverseLimitWeight P F=scalarInverseLimitWeight P E :=
    (scalarInverseLimitWeight_tracial P U).symm
  have hsum : F.add (q.positive P)=(p ⊔ q).positive P := by
    apply Subtype.ext
    change star (star u)*star u+q.operator=(p ⊔ q).operator
    rw [star_star,huf,sub_add_cancel]
  have hbound : scalarInverseLimitWeight P E ≤ scalarInverseLimitWeight P (p.positive P) :=
    scalarInverseLimitWeight_mono P E (p.positive P) hule
  change scalarInverseLimitWeight P ((p ⊔ q).positive P) ≤ _
  rw [← hsum,scalarInverseLimitWeight_add,hFE]
  change scalarInverseLimitWeight P E + scalarInverseLimitWeight P (q.positive P) ≤
    scalarInverseLimitWeight P (p.positive P) + scalarInverseLimitWeight P (q.positive P)
  exact add_le_add hbound le_rfl

/-- The legacy subadditive interface is now instantiated on all projections of N. -/
def coreProjectionTraceSubadditive (P : SiteProfile) :
    SubadditiveTraceData (CoreProjection (regularCoreAlgebra P)) where
  toSemifiniteTraceData := coreProjectionTrace P
  subadd := coreProjectionTrace_subadd P

#print axioms projection_join_comparison
#print axioms coreProjectionTrace_subadd
#print axioms coreProjectionTraceSubadditive
end
end TGLV354
