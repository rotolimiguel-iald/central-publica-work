import TGLExt.V351ModularFixedVectors
import TGLExt.V351ScalarImaginaryCoreAction
import TGLExt.V350ScalarRegularPolarCommutation

set_option autoImplicit false
set_option maxHeartbeats 2200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- Equality of the actual implementers, proved using a total family of
existing average-square vectors. Covariance alone is not used as uniqueness. -/
theorem scalarTomitaImaginaryPower_eq_regular_implementation (P : SiteProfile)
    (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t x =
      scalarGNSRepresentation P (regularRightCoreElement P t) (regularRightGNS P (-t) x) := by
  let d : ℕ → ℝ := fun n => 1/((n : ℝ)+1)
  have hd (n : ℕ) : 0 < d n := by dsimp [d]; positivity
  let e (n : ℕ) : (regularCoreAlgebra P).toStarSubalgebra :=
    ⟨regularAverage P (d n),regularAverage_mem P (d n)⟩
  choose Z hZ hU using fun n => regularAverage_square_modular_fixed P (d n) (hd n)
  have hze (n : ℕ) : (Z n).val = star (e n)*e n := Subtype.ext (hZ n)
  have hzstar (n : ℕ) : star (Z n).val = (Z n).val := by
    rw [hze,star_mul,star_star]
  have hE (n : ℕ) : (Z n).val ∈ scalarPolarRightAlgebra P := by
    rw [hze]
    have he := regularAverage_mem_scalarPolarRightAlgebra P (d n) (hd n)
    exact (scalarPolarRightAlgebra P).mul_mem ((scalarPolarRightAlgebra P).star_mem' he) he
  have havg (δ s : ℝ) : regularUnitary P s * regularAverage P δ =
      regularAverage P δ * regularUnitary P s := by
    change regularUnitary P s * (((δ⁻¹ : ℝ) : ℂ) •
        StrongIntegral.operatorIntegral (regularIntegralFamily P) 0 δ) =
      (((δ⁻¹ : ℝ) : ℂ) • StrongIntegral.operatorIntegral (regularIntegralFamily P) 0 δ) *
        regularUnitary P s
    rw [mul_smul_comm,smul_mul_assoc]
    congr 1
    apply StrongIntegral.operatorIntegral_commutes
    intro u
    change regularUnitary P s * regularUnitary P u = regularUnitary P u * regularUnitary P s
    rw [regular_mul,regular_mul,add_comm s u]
  have hcomm (n : ℕ) : Commute (regularRightCoreElement P t) (Z n).val := by
    apply Subtype.ext
    change regularUnitary P t * (Z n).val.val = (Z n).val.val * regularUnitary P t
    rw [hZ n]
    have hs := congrArg star (havg (d n) (-t))
    simp only [star_mul,regular_star,neg_neg] at hs
    rw [← mul_assoc,← hs,mul_assoc,havg,mul_assoc]
  let W : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P :=
    scalarGNSRepresentation P (regularRightCoreElement P t) * regularRightGNS P (-t)
  have hW (n : ℕ) : W (scalarWeightStarEmbedding P (Z n)) =
      scalarWeightStarEmbedding P (Z n) := by
    let z : scalarWeightLeftIdeal P := ⟨(Z n).val,(Z n).property.1⟩
    have hr := regularRightGNS_intertwines P (-t) z
    have hl := scalarWeightGNSAction_intertwines P (regularRightCoreElement P t)
      (scalarRegularRightProduct P (-t) z)
    have heq : scalarWeightLeftProduct P (regularRightCoreElement P t)
        (scalarRegularRightProduct P (-t) z) = z := by
      apply Subtype.ext
      change regularRightCoreElement P t * ((Z n).val * regularRightCoreElement P (-t)) =
        (Z n).val
      rw [← regularRightCoreElement_star,← mul_assoc,(hcomm n).eq,mul_assoc]
      have hu : regularRightCoreElement P t * star (regularRightCoreElement P t) = 1 :=
        Subtype.ext (regular_unitary P t).2
      rw [hu,mul_one]
    exact (congrArg (scalarGNSRepresentation P (regularRightCoreElement P t)) hr).trans
      (hl.trans (congrArg (scalarWeightGNSEmbedding P) heq))
  have heq (n : ℕ) (a : (regularCoreAlgebra P).toStarSubalgebra) :
      scalarTomitaImaginaryPower P t (scalarGNSRepresentation P a (scalarWeightStarEmbedding P (Z n))) =
        W (scalarGNSRepresentation P a (scalarWeightStarEmbedding P (Z n))) := by
    have hu : scalarTomitaImaginaryPower P t
        (scalarGNSRepresentation P a (scalarWeightStarEmbedding P (Z n))) =
        scalarGNSRepresentation P (regularRightCoreElement P t*a*star (regularRightCoreElement P t))
          (scalarWeightStarEmbedding P (Z n)) :=
      (scalarTomitaImaginaryPower_core_conjugation P t a _).trans
        (congrArg (scalarGNSRepresentation P _) (hU n t))
    have hc := congrArg (fun T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
      T (scalarWeightStarEmbedding P (Z n))) (regularRightGNS_commutes_left P (-t) a).eq
    change regularRightGNS P (-t) (scalarGNSRepresentation P a (scalarWeightStarEmbedding P (Z n))) =
      scalarGNSRepresentation P a (regularRightGNS P (-t) (scalarWeightStarEmbedding P (Z n))) at hc
    have hz := congrArg (scalarGNSRepresentation P (star (regularRightCoreElement P t))) (hW n)
    have hunit : star (regularRightCoreElement P t)*regularRightCoreElement P t = 1 :=
      Subtype.ext (regular_unitary P t).1
    have hV : scalarGNSRepresentation P (star (regularRightCoreElement P t)) *
        scalarGNSRepresentation P (regularRightCoreElement P t) = 1 := by
      rw [← map_mul,hunit,map_one]
    change scalarGNSRepresentation P (star (regularRightCoreElement P t))
      (scalarGNSRepresentation P (regularRightCoreElement P t)
        (regularRightGNS P (-t) (scalarWeightStarEmbedding P (Z n)))) = _ at hz
    have hr : regularRightGNS P (-t) (scalarWeightStarEmbedding P (Z n)) =
        scalarGNSRepresentation P (star (regularRightCoreElement P t))
          (scalarWeightStarEmbedding P (Z n)) := by
      have hv := congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
        B (regularRightGNS P (-t) (scalarWeightStarEmbedding P (Z n)))) hV
      change scalarGNSRepresentation P (star (regularRightCoreElement P t))
        (scalarGNSRepresentation P (regularRightCoreElement P t)
          (regularRightGNS P (-t) (scalarWeightStarEmbedding P (Z n)))) =
          regularRightGNS P (-t) (scalarWeightStarEmbedding P (Z n)) at hv
      exact hv.symm.trans hz
    have hh : W (scalarGNSRepresentation P a (scalarWeightStarEmbedding P (Z n))) =
        scalarGNSRepresentation P (regularRightCoreElement P t*a*star (regularRightCoreElement P t))
          (scalarWeightStarEmbedding P (Z n)) := by
      have hm : scalarGNSRepresentation P
          (regularRightCoreElement P t*a*star (regularRightCoreElement P t)) =
          (scalarGNSRepresentation P (regularRightCoreElement P t) * scalarGNSRepresentation P a) *
            scalarGNSRepresentation P (star (regularRightCoreElement P t)) :=
        (map_mul (scalarGNSRepresentation P) _ _).trans
          (congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
            B * scalarGNSRepresentation P (star (regularRightCoreElement P t)))
            (map_mul (scalarGNSRepresentation P) _ _))
      exact (congrArg (scalarGNSRepresentation P (regularRightCoreElement P t)) hc).trans
        ((congrArg (fun y : ScalarGNSHilbert P =>
          scalarGNSRepresentation P (regularRightCoreElement P t) (scalarGNSRepresentation P a y)) hr).trans
          (congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P =>
            B (scalarWeightStarEmbedding P (Z n))) hm).symm)
    exact hu.trans hh.symm
  have ht : Tendsto d atTop (𝓝[≠] (0 : ℝ)) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
    exact Eventually.of_forall fun n => by
      simp only [Set.mem_compl_iff,Set.mem_singleton_iff]
      exact ne_of_gt (hd n)
  have hnorm (n : ℕ) : ‖(Z n).val.val‖ ≤ 1 := by
    rw [hZ n]
    exact (norm_mul_le _ _).trans (by
      simpa only [norm_star,one_mul] using
        mul_le_mul (regularAverage_norm_le_one P (d n))
          (regularAverage_norm_le_one P (d n)) (norm_nonneg _) zero_le_one)
  have hstrong (v : RegularHilbert (TowerHilbert P)) :
      Tendsto (fun n => (Z n).val.val v) atTop (𝓝 v) := by
    have hh := bounded_application_tendsto atTop (fun n => star (regularAverage P (d n))) 1
      (fun n => by simpa only [norm_star] using regularAverage_norm_le_one P (d n))
      (fun n => regularAverage P (d n) v) v v
      ((regularAverage_tendsto_identity P v).comp ht)
      ((regularAverage_star_tendsto_identity P v).comp ht)
    simpa only [hZ,mul_apply_eq_comp] using hh
  have hrho (y : ScalarGNSHilbert P) :
      Tendsto (fun n => antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (star (Z n).val)) y) atTop (𝓝 y) := by
    have hp := scalarGNSRepresentation_tendsto_of_uniformly_bounded P
      (fun n => (Z n).val) 1 1 hnorm
      (fun v => by
        change Tendsto (fun n => (Z n).val.val v) atTop (𝓝 v)
        exact hstrong v)
      ((scalarTomitaPolarFactor P).symm y)
    have hj := (scalarTomitaPolarFactor P).continuous.continuousAt.tendsto.comp hp
    simpa only [map_one,one_apply_eq_self,Function.comp_def,hzstar,antiunitaryConjugate_apply,
      LinearIsometryEquiv.apply_symm_apply] using hj
  refine (scalarWeightGNSEmbedding_denseRange P).induction ?_
    (isClosed_eq (scalarTomitaImaginaryPower P t).continuous W.continuous) x
  rintro _ ⟨a,rfl⟩
  have hright (n : ℕ) : scalarGNSRepresentation P a.val (scalarWeightStarEmbedding P (Z n)) =
      antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (star (Z n).val)) (scalarWeightGNSEmbedding P a) := by
    have hex : ∃ ha : a.val*(Z n).val ∈ scalarWeightLeftIdeal P,
        scalarWeightGNSEmbedding P ⟨a.val*(Z n).val,ha⟩ =
          antiunitaryConjugate (scalarTomitaPolarFactor P)
            (scalarGNSRepresentation P (star (Z n).val)) (scalarWeightGNSEmbedding P a) := (hE n).1 a
    obtain ⟨ha,hh⟩ := hex
    have hid : scalarWeightLeftProduct P a.val ⟨(Z n).val,(Z n).property.1⟩ =
        (⟨a.val*(Z n).val,ha⟩ : scalarWeightLeftIdeal P) := Subtype.ext rfl
    exact (scalarWeightGNSAction_intertwines P a.val ⟨(Z n).val,(Z n).property.1⟩).trans
      ((congrArg (scalarWeightGNSEmbedding P) hid).trans hh)
  have hv : Tendsto (fun n => scalarGNSRepresentation P a.val (scalarWeightStarEmbedding P (Z n)))
      atTop (𝓝 (scalarWeightGNSEmbedding P a)) := by
    simpa only [hright] using hrho (scalarWeightGNSEmbedding P a)
  exact tendsto_nhds_unique
    (((scalarTomitaImaginaryPower P t).continuous.continuousAt.tendsto.comp hv).congr'
      (Eventually.of_forall fun n => heq n a.val))
    (W.continuous.continuousAt.tendsto.comp hv)

end
end TGLV350.Regular
