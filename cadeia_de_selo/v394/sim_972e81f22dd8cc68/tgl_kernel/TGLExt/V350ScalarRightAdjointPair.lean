import TGLExt.V350ScalarCommutantRegularization
import TGLExt.V350ScalarWeightTomitaIdentification
import TGLExt.V350ScalarTomitaAdjoint
import TGLExt.V350ScalarGNSStrongContinuity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- Both right-vector identities on the original full weight ideal.
The relation with the maximal Tomita adjoint is proved below, not a field. -/
structure ScalarRightAdjointPair (P : SiteProfile)
    (R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) where
  vector : ScalarGNSHilbert P
  adjointVector : ScalarGNSHilbert P
  right : ∀ a : scalarWeightLeftIdeal P,
    R (scalarWeightGNSEmbedding P a) = scalarGNSRepresentation P a.val vector
  adjoint : ∀ a : scalarWeightLeftIdeal P,
    star R (scalarWeightGNSEmbedding P a) = scalarGNSRepresentation P a.val adjointVector

theorem scalarRightAdjointPair_rightBounded {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P} (d : ScalarRightAdjointPair P R) :
    ScalarRightBounded P R := ⟨d.vector,d.right⟩

theorem scalarRightAdjointPair_adjoint_rightBounded {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P} (d : ScalarRightAdjointPair P R) :
    ScalarRightBounded P (star R) := ⟨d.adjointVector,d.adjoint⟩

theorem scalarGNSAverage_tendsto (P : SiteProfile) (x : ScalarGNSHilbert P) :
    Tendsto (fun h : ℝ => scalarGNSRepresentation P
      ⟨regularAverage P h,regularAverage_mem P h⟩ x) (𝓝[≠] 0) (𝓝 x) := by
  have ht := scalarGNSRepresentation_tendsto_of_uniformly_bounded P
    (fun h : ℝ => ⟨regularAverage P h,regularAverage_mem P h⟩) 1 1
    (regularAverage_norm_le_one P) (regularAverage_tendsto_identity P) x
  simpa only [map_one,one_apply_eq_self] using ht

theorem scalarRightAdjointPair_regularized_pairing {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P} (d : ScalarRightAdjointPair P R)
    (a : scalarWeightStarCore P) (h : ℝ) (hh : 0 < h) :
    inner ℂ (scalarWeightStarEmbedding P (star a))
      (scalarGNSRepresentation P ⟨regularAverage P h,regularAverage_mem P h⟩ d.vector) =
    inner ℂ d.adjointVector
      (scalarRightRegularization P h (scalarWeightStarEmbedding P a)) := by
  let e : scalarWeightLeftIdeal P := Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P)
    ⟨⟨regularAverage P h,regularAverage_mem P h⟩,regularAverage_hasFiniteDualSquare P h hh⟩
  have he : scalarWeightGNSEmbedding P e = scalarRegularizationVector P h hh :=
    scalarWeightGNSEmbedding_uniform P _
  let astar : scalarWeightLeftIdeal P := ⟨(star a).val,(star a).property.1⟩
  calc
    _ = inner ℂ (scalarWeightStarEmbedding P (star a))
        (R (scalarWeightGNSEmbedding P e)) :=
      congrArg (inner ℂ (scalarWeightStarEmbedding P (star a))) (d.right e).symm
    _ = inner ℂ (star R (scalarWeightStarEmbedding P (star a)))
        (scalarWeightGNSEmbedding P e) :=
      (R.adjoint_inner_left _ _).symm
    _ = inner ℂ (scalarGNSRepresentation P (star a).val d.adjointVector)
        (scalarWeightGNSEmbedding P e) :=
      congrArg (fun v => inner ℂ v (scalarWeightGNSEmbedding P e)) (d.adjoint astar)
    _ = inner ℂ d.adjointVector
        (scalarGNSRepresentation P a.val (scalarWeightGNSEmbedding P e)) := by
      change inner ℂ (scalarGNSRepresentation P (star a.val) d.adjointVector) _ = _
      have hp : (scalarGNSRepresentation P a.val).adjoint =
          scalarGNSRepresentation P (star a.val) :=
        (map_star (scalarGNSRepresentation P) a.val).symm
      exact (congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
        inner ℂ (B d.adjointVector) (scalarWeightGNSEmbedding P e)) hp.symm).trans
        ((scalarGNSRepresentation P a.val).adjoint_inner_left _ _)
    _ = _ := by
      rw [he]
      exact congrArg (inner ℂ d.adjointVector)
        (scalarRightRegularization_vector P h hh ⟨a.val,a.property.1⟩).symm

theorem scalarRightAdjointPair_starCore_pairing {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P} (d : ScalarRightAdjointPair P R)
    (a : scalarWeightStarCore P) :
    inner ℂ (scalarWeightStarEmbedding P (star a)) d.vector =
      inner ℂ d.adjointVector (scalarWeightStarEmbedding P a) := by
  have hl : Tendsto (fun h : ℝ => inner ℂ (scalarWeightStarEmbedding P (star a))
      (scalarGNSRepresentation P ⟨regularAverage P h,regularAverage_mem P h⟩ d.vector))
      (𝓝[>] 0) (𝓝 (inner ℂ (scalarWeightStarEmbedding P (star a)) d.vector)) :=
    (tendsto_const_nhds.inner (scalarGNSAverage_tendsto P d.vector)).mono_left
    (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  have hr : Tendsto (fun h : ℝ => inner ℂ d.adjointVector
      (scalarRightRegularization P h (scalarWeightStarEmbedding P a)))
      (𝓝[>] 0) (𝓝 (inner ℂ d.adjointVector (scalarWeightStarEmbedding P a))) :=
    (tendsto_const_nhds.inner
    (scalarRightRegularization_tendsto P (scalarWeightStarEmbedding P a))).mono_left
      (nhdsWithin_mono (0 : ℝ) (by intro h hh; exact ne_of_gt hh))
  have he : (fun h : ℝ => inner ℂ (scalarWeightStarEmbedding P (star a))
      (scalarGNSRepresentation P ⟨regularAverage P h,regularAverage_mem P h⟩ d.vector)) =ᶠ[𝓝[>] 0]
    (fun h : ℝ => inner ℂ d.adjointVector
      (scalarRightRegularization P h (scalarWeightStarEmbedding P a))) := by
    filter_upwards [self_mem_nhdsWithin] with h hh
    exact scalarRightAdjointPair_regularized_pairing d a h hh
  exact tendsto_nhds_unique (hl.congr' he) hr

private theorem rightPairing_closure {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] (y z : H) (G : Set (H × H))
    (hG : ∀ p ∈ G, inner ℂ p.2 y = inner ℂ z p.1)
    {p : H × H} (hp : p ∈ closure G) : inner ℂ p.2 y = inner ℂ z p.1 := by
  have hl : Continuous (fun q : H × H => inner ℂ q.2 y) := by fun_prop
  have hr : Continuous (fun q : H × H => inner ℂ z q.1) := by fun_prop
  exact closure_minimal hG (isClosed_eq hl hr) hp

theorem scalarRightAdjointPair_closed_pairing {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P} (d : ScalarRightAdjointPair P R)
    (x : scalarClosedTomitaDomain P) :
    inner ℂ (scalarClosedTomita P x) d.vector =
      inner ℂ d.adjointVector (x : ScalarGNSHilbert P) := by
  have hs : scalarWeightTomitaGraph P ⊆ {p : ScalarGNSHilbert P × ScalarGNSHilbert P |
      inner ℂ p.2 d.vector = inner ℂ d.adjointVector p.1} := by
    rintro _ ⟨a,rfl⟩
    exact scalarRightAdjointPair_starCore_pairing d a
  have hx : ((x : ScalarGNSHilbert P),scalarClosedTomita P x) ∈
      closure (scalarWeightTomitaGraph P) :=
    (scalarClosedTomita_graph_eq_weight P).subset ⟨x,rfl⟩
  exact rightPairing_closure (H := ScalarGNSHilbert P)
    d.vector d.adjointVector (scalarWeightTomitaGraph P) hs
    (p := ((x : ScalarGNSHilbert P),scalarClosedTomita P x)) hx

/-- Every actual bounded right pair belongs to the SAME maximal F=S†.
No Gaussian state or new modular conjugation is substituted. -/
theorem scalarRightAdjointPair_maximal {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P} (d : ScalarRightAdjointPair P R) :
    ∃ hv : d.vector ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨d.vector,hv⟩ = d.adjointVector :=
  scalarTomitaAdjoint_maximal P (scalarRightAdjointPair_closed_pairing d)

#print axioms ScalarRightAdjointPair
#print axioms scalarRightAdjointPair_rightBounded
#print axioms scalarRightAdjointPair_adjoint_rightBounded
#print axioms scalarGNSAverage_tendsto
#print axioms scalarRightAdjointPair_regularized_pairing
#print axioms scalarRightAdjointPair_starCore_pairing
#print axioms scalarRightAdjointPair_closed_pairing
#print axioms scalarRightAdjointPair_maximal
end
end TGLV350.Regular
