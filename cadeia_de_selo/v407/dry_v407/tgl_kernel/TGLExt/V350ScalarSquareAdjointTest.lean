import TGLExt.V350ScalarRightSquareApproximation
import TGLExt.V350ScalarRightGraphCore
import TGLExt.V350ScalarTomitaBidual

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt Filter ChatgptAudit.Continuous049
open scoped Topology
noncomputable section

private theorem differencePairing {H B : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [AddCommGroup B] [Module ℂ B] [Mul B]
    (j : B →ₗ[ℂ] H) (a u v : B) (y z : H)
    (he : a = (1/4 : ℂ) • (u*u-v*v))
    (hu : inner ℂ (j (u*u)) y = inner ℂ z (j (u*u)))
    (hv : inner ℂ (j (v*v)) y = inner ℂ z (j (v*v))) :
    inner ℂ (j a) y = inner ℂ z (j a) := by
  have hq : (starRingEnd ℂ) (1/4 : ℂ) = (1/4 : ℂ) := by
    simp only [map_div₀,map_one,map_ofNat]
  rw [he,map_smul,map_sub,inner_smul_left,inner_smul_right,
    hq,inner_sub_left,inner_sub_right,hu,hv]

private theorem subalgebraDifferencePairing {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H))
    (j : E →ₗ[ℂ] H) (a u v : E) (y z : H)
    (he : a = (1/4 : ℂ) • (u*u-v*v))
    (hu : inner ℂ (j (u*u)) y = inner ℂ z (j (u*u)))
    (hv : inner ℂ (j (v*v)) y = inner ℂ z (j (v*v))) :
    inner ℂ (j a) y = inner ℂ z (j a) :=
  differencePairing j a u v y z he hu hv

private theorem pairingConstraintClosed {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] (y z : H) :
    IsClosed {v : H | inner ℂ v y = inner ℂ z v} :=
  isClosed_eq (continuous_id.inner continuous_const) (continuous_const.inner continuous_id)

private theorem pairingLimit {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (y z : H) (f : ℕ → H) (v : H) (ht : Tendsto f atTop (𝓝 v))
    (hf : ∀ n, inner ℂ (f n) y = inner ℂ z (f n)) :
    inner ℂ v y = inner ℂ z v :=
  (isClosed_eq (continuous_id.inner continuous_const)
    (continuous_const.inner continuous_id)).mem_of_tendsto ht (Eventually.of_forall hf)

private theorem starSumFixed {B : Type} [AddCommGroup B] [StarAddMonoid B]
    (a d : B) (ha : star a=a) (hd : star d=d) : star (a+d)=a+d :=
  (star_add a d).trans (congrArg₂ (fun x y : B => x+y) ha hd)

private theorem starDifferenceFixed {B : Type} [AddCommGroup B] [StarAddMonoid B]
    (a d : B) (ha : star a=a) (hd : star d=d) : star (a-d)=a-d :=
  (star_sub a d).trans (congrArg₂ (fun x y : B => x-y) ha hd)

/-- Tests on selfadjoint squares suffice for every selfadjoint right vector. -/
theorem scalarSelfadjointPairing_of_squarePairing (P : SiteProfile)
    (y z : ScalarGNSHilbert P)
    (hsq : ∀ b : scalarPairedRightAlgebra P, star b=b →
      inner ℂ (scalarRightPairVector P (b*b)) y =
        inner ℂ z (scalarRightPairVector P (b*b)))
    (a : scalarPairedRightAlgebra P) (ha : star a=a) :
    inner ℂ (scalarRightPairVector P a) y = inner ℂ z (scalarRightPairVector P a) := by
  refine pairingLimit y z
    (fun n => scalarRightPairVector P (scalarRightSquareApproximation P a ha n))
    (scalarRightPairVector P a) (scalarRightSquareApproximation_vector_tendsto P a ha) ?_
  intro n
  have hp := hsq (a+scalarRightSquareCutoff P a ha n)
    (starSumFixed a _ ha (scalarRightSquareCutoff_star P a ha n))
  have hm := hsq (a-scalarRightSquareCutoff P a ha n)
    (starDifferenceFixed a _ ha (scalarRightSquareCutoff_star P a ha n))
  exact subalgebraDifferencePairing (H := ScalarGNSHilbert P) (scalarPairedRightAlgebra P)
    (scalarRightPairVector P)
    (scalarRightSquareApproximation P a ha n)
    (a+scalarRightSquareCutoff P a ha n) (a-scalarRightSquareCutoff P a ha n) y z
    (scalarRightSquareApproximation_difference_of_squares P a ha n) hp hm

/-- The limit is in the fixed space of the already defined F, not an auxiliary operator. -/
theorem scalarFixedPairing_of_squarePairing (P : SiteProfile)
    (y z : ScalarGNSHilbert P)
    (hsq : ∀ b : scalarPairedRightAlgebra P, star b=b →
      inner ℂ (scalarRightPairVector P (b*b)) y =
        inner ℂ z (scalarRightPairVector P (b*b)))
    (x : ScalarGNSHilbert P)
    (hx : ∃ hx : x ∈ scalarTomitaAdjointDomain P, scalarTomitaAdjoint P ⟨x,hx⟩=x) :
    inner ℂ x y = inner ℂ z x := by
  have hcl : closure {v : ScalarGNSHilbert P | ∃ a : scalarPairedRightAlgebra P,
      star a=a ∧ scalarRightPairVector P a=v} ⊆
      {v : ScalarGNSHilbert P | inner ℂ v y = inner ℂ z v} := by
    apply closure_minimal
    · rintro _ ⟨a,ha,rfl⟩
      exact scalarSelfadjointPairing_of_squarePairing P y z hsq a ha
    · exact pairingConstraintClosed y z
  apply hcl
  exact (congrArg (fun T : Set (ScalarGNSHilbert P) => x ∈ T)
    (scalarRightSelfadjointVectors_closure P)).mpr hx

private theorem pairingViaFixedDecomposition {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] (D : Submodule ℂ H) (F : D →ₛₗ[starRingEnd ℂ] H)
    (hm : ∀ x : D, F x ∈ D) (hi : ∀ x : D, F ⟨F x,hm x⟩=(x:H))
    (y z : H) (hf : ∀ x : H, x ∈ fixedRealSubmodule D F → inner ℂ x y = inner ℂ z x)
    (x : D) : inner ℂ (F x) y = inner ℂ z (x:H) := by
  obtain ⟨h,k,hh,hk,hx,hFx⟩ := domain_fixed_decomposition D F hm hi x
  rw [hFx,hx,inner_sub_left,inner_smul_left,inner_add_right,inner_smul_right,hf h hh,hf k hk]
  simp

/-- Membership and value in the original S follow from square tests alone. -/
theorem scalarClosedTomita_of_squarePairing (P : SiteProfile)
    (y z : ScalarGNSHilbert P)
    (hsq : ∀ b : scalarPairedRightAlgebra P, star b=b →
      inner ℂ (scalarRightPairVector P (b*b)) y =
        inner ℂ z (scalarRightPairVector P (b*b))) :
    ∃ hy : y ∈ scalarClosedTomitaDomain P, scalarClosedTomita P ⟨y,hy⟩=z := by
  apply scalarClosedTomita_bidual_maximal P y z
  refine pairingViaFixedDecomposition (scalarTomitaAdjointDomain P)
    (scalarTomitaAdjoint P).toFun ?_ ?_ y z ?_
  · intro x; exact scalarTomitaAdjoint_maps_domain P x
  · intro x; exact scalarTomitaAdjoint_involutive P x
  · intro x hx; exact scalarFixedPairing_of_squarePairing P y z hsq x hx

private theorem fixedVectorTest {H B : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [AddCommGroup B] [Module ℂ B] [Star B]
    (j : B →ₗ[ℂ] H) (D : Submodule ℂ H) (F : D → H)
    (hj : ∀ a : B, ∃ ha : j a ∈ D, F ⟨j a,ha⟩=j (star a))
    (y z : H) (hp : ∀ x : D, inner ℂ (F x) y = inner ℂ z (x:H))
    (a : B) (ha : star a=a) : inner ℂ (j a) y = inner ℂ z (j a) := by
  obtain ⟨hx,hf⟩ := hj a
  have he := hf.trans (congrArg j ha)
  exact (congrArg (fun v : H => inner ℂ v y) he).symm.trans (hp ⟨j a,hx⟩)

private theorem subalgebraFixedVectorTest {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H))
    (j : E →ₗ[ℂ] H) (D : Submodule ℂ H) (F : D →ₛₗ[starRingEnd ℂ] H)
    (hj : ∀ a : E, ∃ ha : j a ∈ D, F ⟨j a,ha⟩=j (star a))
    (y z : H) (hp : ∀ x : D, inner ℂ (F x) y = inner ℂ z (x:H))
    (a : E) (ha : star a=a) : inner ℂ (j a) y = inner ℂ z (j a) :=
  fixedVectorTest j D (fun x => F x) hj y z hp a ha

/-- Exact test characterization. It does not postulate graph density of squares. -/
theorem scalarClosedTomita_squarePairing_iff (P : SiteProfile) (y z : ScalarGNSHilbert P) :
    (∃ hy : y ∈ scalarClosedTomitaDomain P, scalarClosedTomita P ⟨y,hy⟩=z) ↔
    ∀ b : scalarPairedRightAlgebra P, star b=b →
      inner ℂ (scalarRightPairVector P (b*b)) y =
        inner ℂ z (scalarRightPairVector P (b*b)) := by
  constructor
  · intro h b hb
    have hs : star (b*b)=b*b := (star_mul b b).trans
      (congrArg₂ (fun u v : scalarPairedRightAlgebra P => u*v) hb hb)
    refine subalgebraFixedVectorTest (H := ScalarGNSHilbert P) (scalarPairedRightAlgebra P)
      (scalarRightPairVector P) (scalarTomitaAdjointDomain P)
      (scalarTomitaAdjoint P).toFun ?_ y z ?_ (b*b) hs
    · intro a
      exact scalarRightPairVector_original_adjoint P a
    · exact (scalarClosedTomita_bidual_graph_iff P y z).mp h
  · exact scalarClosedTomita_of_squarePairing P y z

private theorem boundedActionSquarePairing {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (A K : H →L[ℂ] H)
    (hA : star A=A) (v y z : H) (hk : K v=A y) (hks : star K v=A z) :
    inner ℂ (A v) y = inner ℂ z (A v) := by
  have hs := ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp hA
  calc
    _ = inner ℂ v (A y) := hs v y
    _ = inner ℂ v (K v) := congrArg (inner ℂ v) hk.symm
    _ = inner ℂ (star K v) v := (K.adjoint_inner_left v v).symm
    _ = inner ℂ (A z) v := congrArg (fun w : H => inner ℂ w v) hks
    _ = _ := hs z v

/-- A bounded operator and its adjoint implementing both right actions force
the vector pair into the original S graph. No replacement of S or J occurs. -/
theorem scalarClosedTomita_of_boundedPairAction (P : SiteProfile)
    (K : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (y z : ScalarGNSHilbert P)
    (hk : ∀ a : scalarPairedRightAlgebra P, K (scalarRightPairVector P a)=a.val y)
    (hks : ∀ a : scalarPairedRightAlgebra P, star K (scalarRightPairVector P a)=a.val z) :
    ∃ hy : y ∈ scalarClosedTomitaDomain P, scalarClosedTomita P ⟨y,hy⟩=z := by
  apply scalarClosedTomita_of_squarePairing P y z
  intro a ha
  have hs : star a.val=a.val := congrArg (fun b : scalarPairedRightAlgebra P => b.val) ha
  calc
    _ = inner ℂ (a.val (scalarRightPairVector P a)) y :=
      congrArg (fun w : ScalarGNSHilbert P => inner ℂ w y) (scalarRightPairVector_mul P a a)
    _ = inner ℂ z (a.val (scalarRightPairVector P a)) :=
      boundedActionSquarePairing a.val K hs (scalarRightPairVector P a) y z (hk a) (hks a)
    _ = _ := congrArg (inner ℂ z) (scalarRightPairVector_mul P a a).symm

#print axioms scalarSelfadjointPairing_of_squarePairing
#print axioms scalarFixedPairing_of_squarePairing
#print axioms scalarClosedTomita_of_squarePairing
#print axioms scalarClosedTomita_squarePairing_iff
#print axioms scalarClosedTomita_of_boundedPairAction
end
end TGLV350.Regular
