import TGLExt.V350ScalarCutVacuum
import TGLExt.V350ScalarWeightCompletion
import TGLExt.V350ScalarHomogeneousRightOrbit

set_option autoImplicit false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt MeasureTheory Filter
open scoped Topology
noncomputable section

/-- Extend the existing cut identity from the uniform finite ideal to all n_nu. -/
theorem scalarGNSCutMap_weight_embedding (P : SiteProfile) (r : ℝ)
    (A : scalarWeightLeftIdeal P) :
    scalarGNSCutMap P r (scalarWeightGNSEmbedding P A) =
      dualOrbitRepresentation A.val.val (scalarCutVacuum P r) := by
  apply Lp.ext
  filter_upwards [measurableCut_ae (Set.Ioc (-r) r) measurableSet_Ioc (scalarWeightOrbit P A),
    scalarWeightOrbit_ae P A,
    operatorFieldLift_ae (dualIntegralFamily A.val.val) (scalarCutVacuum P r),
    scalarCutVacuum_ae P r] with s h1 h2 h3 h4
  change measurableCut (Set.Ioc (-r) r) measurableSet_Ioc (scalarWeightOrbit P A) s =
    operatorFieldLift (dualIntegralFamily A.val.val) (scalarCutVacuum P r) s
  rw [h1,h3,h4]
  by_cases hs : s ∈ Set.Ioc (-r) r
  · simp only [Set.indicator_of_mem hs,h2]
    change (↑(Real.sqrt dualHaarFactor) : ℂ) • dualAmbient s A.val.val (regularVacuum P) =
      dualAmbient s A.val.val ((↑(Real.sqrt dualHaarFactor) : ℂ) • regularVacuum P)
    exact (map_smul (dualAmbient s A.val.val) _ _).symm
  · simp only [Set.indicator_of_notMem hs,map_zero]

/-- Countably many existing cuts identify a full weight vector; no finite
minorant formula for the nontracial weight is used. -/
theorem scalarWeightGNSEmbedding_of_cut_actions (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P)
    (hcut : ∀ n : ℕ, scalarGNSCutMap P (n : ℝ) v =
      dualOrbitRepresentation A.val (scalarCutVacuum P (n : ℝ))) :
    ∃ hA : A ∈ scalarWeightLeftIdeal P, scalarWeightGNSEmbedding P ⟨A,hA⟩ = v := by
  have he (n : ℕ) : ∀ᵐ s : ℝ, s ∈ Set.Ioc (-(n : ℝ)) (n : ℝ) →
      v.val s = (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val (regularVacuum P) := by
    filter_upwards [measurableCut_ae (Set.Ioc (-(n : ℝ)) (n : ℝ)) measurableSet_Ioc v.val,
      operatorFieldLift_ae (dualIntegralFamily A.val) (scalarCutVacuum P (n : ℝ)),
      scalarCutVacuum_ae P (n : ℝ)] with s h1 h2 h3
    intro hs
    have h := congrArg (fun f : RegularHilbert (RegularHilbert (TowerHilbert P)) => f s) (hcut n)
    change measurableCut (Set.Ioc (-(n : ℝ)) (n : ℝ)) measurableSet_Ioc v.val s =
      operatorFieldLift (dualIntegralFamily A.val) (scalarCutVacuum P (n : ℝ)) s at h
    rw [h1,h2,h3] at h
    simp only [Set.indicator_of_mem hs] at h
    change v.val s = dualAmbient s A.val ((↑(Real.sqrt dualHaarFactor) : ℂ) • regularVacuum P) at h
    change v.val s = (↑(Real.sqrt dualHaarFactor) : ℂ) • dualAmbient s A.val (regularVacuum P)
    simpa only [map_smul] using h
  have hall : (v.val : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val (regularVacuum P) := by
    filter_upwards [ae_all_iff.mpr he] with s hs
    obtain ⟨n,hn⟩ := exists_nat_gt |s|
    apply hs n
    constructor
    · have hl := neg_abs_le s
      linarith
    · exact le_trans (le_abs_self s) hn.le
  have hc : Real.sqrt dualHaarFactor ≠ 0 := ne_of_gt (Real.sqrt_pos.2 dualHaarFactor_pos)
  have hm : MemLp (fun s : ℝ => dualAmbient s A.val (regularVacuum P)) 2 := by
    have hf : ((Real.sqrt dualHaarFactor)⁻¹ : ℝ) •
        (v.val : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
        fun s => dualAmbient s A.val (regularVacuum P) := by
      filter_upwards [hall] with s hs
      simp only [Pi.smul_apply,hs,smul_smul,inv_mul_cancel₀ hc,one_smul]
    exact (memLp_congr_ae hf).mp ((Lp.memLp v.val).const_smul ((Real.sqrt dualHaarFactor)⁻¹ : ℝ))
  have hA : A ∈ scalarWeightLeftIdeal P := (hasFiniteScalarSquare_iff_memLp P A.val).mpr hm
  refine ⟨hA,?_⟩
  apply Subtype.ext
  apply Lp.ext
  exact (scalarWeightOrbit_ae P ⟨A,hA⟩).trans hall.symm

/-- The two required convergences close the same GNS inscription. Strong
operator convergence alone is not asserted to imply convergence in GNS norm. -/
theorem scalarWeightGNSEmbedding_closed_of_bounded_strong (P : SiteProfile)
    {ι : Type*} {l : Filter ι} [NeBot l]
    (T : ι → scalarWeightLeftIdeal P)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val.val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (T i).val.val x) l (𝓝 (A.val x)))
    (hgns : Tendsto (fun i => scalarWeightGNSEmbedding P (T i)) l (𝓝 v)) :
    ∃ hA : A ∈ scalarWeightLeftIdeal P, scalarWeightGNSEmbedding P ⟨A,hA⟩ = v := by
  apply scalarWeightGNSEmbedding_of_cut_actions P A v
  intro n
  have h1 := (scalarGNSCutMap P (n : ℝ)).continuous.continuousAt.tendsto.comp hgns
  have h2 := dualOrbit_tendsto_of_uniformly_bounded
    (fun i => (T i).val.val) A.val C hbound hstrong (scalarCutVacuum P (n : ℝ))
  simp only [Function.comp_def,scalarGNSCutMap_weight_embedding] at h1
  exact tendsto_nhds_unique h1 h2

#print axioms scalarGNSCutMap_weight_embedding
#print axioms scalarWeightGNSEmbedding_of_cut_actions
#print axioms scalarWeightGNSEmbedding_closed_of_bounded_strong
end
end TGLV350.Regular
