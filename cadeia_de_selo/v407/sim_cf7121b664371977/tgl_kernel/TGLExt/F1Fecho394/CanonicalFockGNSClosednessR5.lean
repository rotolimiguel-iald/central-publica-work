import TGLExt.F1Fecho394.GenericCountableCutsR1
import TGLExt.F1Fecho394.CanonicalFockGNSCutsR2
import TGLExt.V350DualOrbitStrongLimits
/-! Closed graph of the actual full-weight Fock GNS inscription.
Countably many finite-interval cuts identify the vector. Both operator-strong
and GNS-norm convergence are required, exactly as in the incorporated v393 proof. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockGNSClosedness
open TGLExt.ImportedSQ F1Rede.BosonicFock MeasureTheory Filter
open TGLV350.Regular (RegularHilbert dualQuadraticIntegral dualHaarFactor dualHaarFactor_pos dualAmbient dualQuadraticIntegrand_star_mul measurableCut measurableCut_ae operatorFieldLift operatorFieldLift_ae dualOrbitRepresentation dualIntegralFamily dualOrbit_tendsto_of_uniformly_bounded)
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight F1Fecho.CanonicalFockGNS
open F1Fecho.CanonicalFockGNSRepresentation F1Fecho.CanonicalFockWeightDomain
open F1Fecho.CanonicalFockWeightOrbit F1Fecho.CanonicalFockWeightCompletion
open F1Fecho.CanonicalFockGNSCuts
open scoped Topology ENNReal NNReal
theorem hasFiniteScalarSquare_iff_memLp 
    (A : RegularHilbert F →L[ℂ] RegularHilbert F) :
    HasFiniteScalarSquare  A ↔ MemLp (fun s : ℝ => dualAmbient s A (regularFockVacuum)) 2 := by
  constructor
  · exact scalarWeightOrbit_memLp  A
  · intro hm
    have hi := hm.2
    rw [eLpNorm_lt_top_iff_lintegral_rpow_enorm_lt_top (by norm_num) (by norm_num)] at hi
    have he (s : ℝ) : ENNReal.ofReal (‖dualAmbient s A (regularFockVacuum)‖ ^ 2) =
        (‖dualAmbient s A (regularFockVacuum)‖₊ : ℝ≥0∞) ^ 2 := by
      rw [ENNReal.ofReal_pow (norm_nonneg _),ofReal_norm,enorm_eq_nnnorm]
    simp only [HasFiniteScalarSquare,dualQuadraticIntegral,dualQuadraticIntegrand_star_mul,he]
    apply ENNReal.mul_lt_top ENNReal.ofReal_lt_top
    simpa only [ENNReal.toReal_ofNat,ENNReal.rpow_two,enorm_eq_nnnorm,pow_two] using hi


/-- Extend the existing cut identity from the uniform finite ideal to all n_nu. -/
theorem scalarGNSCutMap_weight_embedding (r : ℝ)
    (A : scalarWeightLeftIdeal ) :
    scalarGNSCutMap  r (scalarWeightGNSEmbedding  A) =
      dualOrbitRepresentation A.val.val (scalarCutVacuum  r) := by
  apply Lp.ext
  filter_upwards [measurableCut_ae (Set.Ioc (-r) r) measurableSet_Ioc (scalarWeightOrbit  A),
    scalarWeightOrbit_ae  A,
    operatorFieldLift_ae (dualIntegralFamily A.val.val) (scalarCutVacuum  r),
    scalarCutVacuum_ae  r] with s h1 h2 h3 h4
  change measurableCut (Set.Ioc (-r) r) measurableSet_Ioc (scalarWeightOrbit  A) s =
    operatorFieldLift (dualIntegralFamily A.val.val) (scalarCutVacuum  r) s
  apply h1.trans
  apply Eq.trans ?_ (h3.trans (congrArg (dualAmbient s A.val.val) h4)).symm
  by_cases hs : s ∈ Set.Ioc (-r) r
  · simp only [Set.indicator_of_mem hs]
    exact h2.trans ((map_smul (dualAmbient s A.val.val) (↑(Real.sqrt dualHaarFactor) : ℂ) regularFockVacuum).symm)
  · simp only [Set.indicator_of_notMem hs,map_zero]


/-- Countably many existing cuts identify a full weight vector; no finite
minorant formula for the nontracial weight is used. -/
theorem scalarWeightGNSEmbedding_of_cut_actions 
    (A : core.toStarSubalgebra) (v : GNSHilbert)
    (hcut : ∀ n : ℕ, scalarGNSCutMap  (n : ℝ) v =
      dualOrbitRepresentation A.val (scalarCutVacuum  (n : ℝ))) :
    ∃ hA : A ∈ scalarWeightLeftIdeal , scalarWeightGNSEmbedding  ⟨A,hA⟩ = v := by
  have he (n : ℕ) : ∀ᵐ s : ℝ, s ∈ Set.Ioc (-(n : ℝ)) (n : ℝ) →
      v.val s = (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val (regularFockVacuum) := by
    filter_upwards [measurableCut_ae (Set.Ioc (-(n : ℝ)) (n : ℝ)) measurableSet_Ioc v.val,
      operatorFieldLift_ae (dualIntegralFamily A.val) (scalarCutVacuum  (n : ℝ)),
      scalarCutVacuum_ae  (n : ℝ)] with s h1 h2 h3
    intro hs
    have h := congrArg (fun f : RegularHilbert (RegularHilbert F) => f s) (hcut n)
    change measurableCut (Set.Ioc (-(n : ℝ)) (n : ℝ)) measurableSet_Ioc v.val s =
      operatorFieldLift (dualIntegralFamily A.val) (scalarCutVacuum  (n : ℝ)) s at h
    have hh := h1.symm.trans (h.trans (h2.trans (congrArg (dualAmbient s A.val) h3)))
    simp only [Set.indicator_of_mem hs] at hh
    change v.val s = (↑(Real.sqrt dualHaarFactor) : ℂ) • dualAmbient s A.val regularFockVacuum
    exact hh.trans (map_smul (dualAmbient s A.val) (↑(Real.sqrt dualHaarFactor) : ℂ) regularFockVacuum)

  have hall : (v.val : ℝ → RegularHilbert F) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val (regularFockVacuum) := by
    exact F1Fecho.GenericCountableCuts.ae_eq_of_ioc _ _ he
  have hc : Real.sqrt dualHaarFactor ≠ 0 := ne_of_gt (Real.sqrt_pos.2 dualHaarFactor_pos)
  have hm : MemLp (fun s : ℝ => dualAmbient s A.val (regularFockVacuum)) 2 := by
    have hf : ((Real.sqrt dualHaarFactor)⁻¹ : ℝ) •
        (v.val : ℝ → RegularHilbert F) =ᵐ[volume]
        fun s => dualAmbient s A.val (regularFockVacuum) := by
      filter_upwards [hall] with s hs
      simp only [Pi.smul_apply,hs,smul_smul,inv_mul_cancel₀ hc,one_smul]
    exact (memLp_congr_ae hf).mp ((Lp.memLp v.val).const_smul ((Real.sqrt dualHaarFactor)⁻¹ : ℝ))
  have hA : A ∈ scalarWeightLeftIdeal  := (hasFiniteScalarSquare_iff_memLp  A.val).mpr hm
  refine ⟨hA,?_⟩
  apply Subtype.ext
  apply Lp.ext
  exact (scalarWeightOrbit_ae  ⟨A,hA⟩).trans hall.symm

/-- The two required convergences close the same GNS inscription. Strong
operator convergence alone is not asserted to imply convergence in GNS norm. -/
theorem scalarWeightGNSEmbedding_closed_of_bounded_strong 
    {ι : Type*} {l : Filter ι} [NeBot l]
    (T : ι → scalarWeightLeftIdeal )
    (A : core.toStarSubalgebra) (v : GNSHilbert) (C : ℝ)
    (hbound : ∀ i, ‖(T i).val.val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (T i).val.val x) l (𝓝 (A.val x)))
    (hgns : Tendsto (fun i => scalarWeightGNSEmbedding  (T i)) l (𝓝 v)) :
    ∃ hA : A ∈ scalarWeightLeftIdeal , scalarWeightGNSEmbedding  ⟨A,hA⟩ = v := by
  apply scalarWeightGNSEmbedding_of_cut_actions  A v
  intro n
  have h1 := (scalarGNSCutMap  (n : ℝ)).continuous.continuousAt.tendsto.comp hgns
  have h2 := dualOrbit_tendsto_of_uniformly_bounded
    (fun i => (T i).val.val) A.val C hbound hstrong (scalarCutVacuum  (n : ℝ))
  simp only [Function.comp_def,scalarGNSCutMap_weight_embedding] at h1
  exact tendsto_nhds_unique h1 h2


end F1Fecho.CanonicalFockGNSClosedness
#print axioms F1Fecho.CanonicalFockGNSClosedness.hasFiniteScalarSquare_iff_memLp
#print axioms F1Fecho.CanonicalFockGNSClosedness.scalarGNSCutMap_weight_embedding
#print axioms F1Fecho.CanonicalFockGNSClosedness.scalarWeightGNSEmbedding_of_cut_actions
#print axioms F1Fecho.CanonicalFockGNSClosedness.scalarWeightGNSEmbedding_closed_of_bounded_strong
