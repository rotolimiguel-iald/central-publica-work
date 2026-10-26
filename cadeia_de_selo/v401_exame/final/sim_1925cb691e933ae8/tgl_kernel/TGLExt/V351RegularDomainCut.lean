import TGLExt.V351InverseLimitScaling
import Mathlib.Topology.MetricSpace.UniformConvergence

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

/-- A bounded domain cutoff made from the original inverse generator cutoff. -/
def regularDomainCut (P : SiteProfile) (δ : ℝ) : (regularCoreAlgebra P).toStarSubalgebra :=
  1 - (δ : ℂ) • ⟨regularInverseGeneratorCutoff P δ,regularInverseGeneratorCutoff_mem P δ⟩

private theorem hilbert_positive_smul {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : H →L[ℂ] H) (hA : 0 ≤ A) (r : ℝ) (hr : 0 ≤ r) : 0 ≤ (r : ℂ) • A := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply ((ContinuousLinearMap.nonneg_iff_isPositive _).mp hA).smul_of_nonneg
  exact_mod_cast hr

private theorem hilbert_contract_norm {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : H →L[ℂ] H) (hA : 0 ≤ A) (h1 : A ≤ 1) : ‖A‖ ≤ 1 :=
  (CStarAlgebra.norm_le_norm_of_nonneg_of_le hA h1).trans ContinuousLinearMap.norm_id_le

private theorem hilbert_positive_product {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A B : H →L[ℂ] H) (hA : 0 ≤ A) (hB : 0 ≤ B) (hc : Commute A B) :
    0 ≤ A*B := Commute.mul_nonneg hA hB hc

theorem regularDomainCut_right (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    regularDomainCut P δ ∈ scalarPolarRightAlgebra P :=
  (scalarPolarRightAlgebra P).sub_mem (scalarPolarRightAlgebra P).one_mem
    ((scalarPolarRightAlgebra P).smul_mem (regularInverseGeneratorCutoff_right P δ hδ) (δ : ℂ))

theorem regularDomainCut_bounds (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    0 ≤ (regularDomainCut P δ).val ∧ (regularDomainCut P δ).val ≤ 1 := by
  have hb := regularInverseGeneratorCutoff_nonneg P δ hδ
  have hu := sub_nonneg.mpr (regularInverseGeneratorCutoff_le P δ hδ)
  have hp := hilbert_positive_smul _ hu δ hδ.le
  have he : (δ : ℂ) * (δ⁻¹ : ℂ) = 1 := by exact_mod_cast mul_inv_cancel₀ hδ.ne'
  rw [smul_sub,smul_smul,he,one_smul] at hp
  refine ⟨hp,?_⟩
  change 1 - (δ : ℂ) • regularInverseGeneratorCutoff P δ ≤ 1
  exact sub_le_self _ (hilbert_positive_smul _ hb δ hδ.le)

theorem regularDomainCut_commutes (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    Commute (regularInverseGeneratorCutoff P ε) (regularDomainCut P δ).val := by
  have hc := (regularInverseGeneratorCutoff_commutes P ε δ hε hδ).eq
  change regularInverseGeneratorCutoff P ε * (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) =
    (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) * regularInverseGeneratorCutoff P ε
  simp only [mul_sub,sub_mul,mul_one,one_mul,mul_smul_comm,smul_mul_assoc,hc]

/-- Resolvent identity with no division by the difference of regulators. -/
theorem regularDomainCut_inverse_product (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    regularInverseGeneratorCutoff P ε * (regularDomainCut P δ).val =
      regularInverseGeneratorCutoff P δ - (ε : ℂ) •
        (regularInverseGeneratorCutoff P δ * regularInverseGeneratorCutoff P ε) := by
  have he := regularInverseGeneratorCutoff_resolvent_identity P ε δ hε hδ
  have hc := (regularInverseGeneratorCutoff_commutes P ε δ hε hδ).eq
  change regularInverseGeneratorCutoff P ε * (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) = _
  rw [mul_sub,mul_one,mul_smul_comm,hc]
  rw [Complex.ofReal_sub,sub_smul] at he
  simpa only [sub_add_cancel] using (show
    regularInverseGeneratorCutoff P ε - (δ : ℂ) •
      (regularInverseGeneratorCutoff P δ * regularInverseGeneratorCutoff P ε) =
    regularInverseGeneratorCutoff P δ - (ε : ℂ) •
      (regularInverseGeneratorCutoff P δ * regularInverseGeneratorCutoff P ε) by
        calc
          _ = (regularInverseGeneratorCutoff P ε - regularInverseGeneratorCutoff P δ) +
              regularInverseGeneratorCutoff P δ - (δ : ℂ) •
                (regularInverseGeneratorCutoff P δ * regularInverseGeneratorCutoff P ε) := by abel
          _ = _ := by rw [he]; abel)

private theorem hilbert_commuting_contract_product {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (B q : H →L[ℂ] H) (hB : 0 ≤ B) (hq : 0 ≤ q) (h1 : q ≤ 1) (hc : Commute B q) :
    B*q*q ≤ B*q := by
  have hp : 0 ≤ B*q := Commute.mul_nonneg hB hq hc
  have hcom : Commute (B*q) (1-q) := by
    change (B*q)*(1-q) = (1-q)*(B*q)
    simp only [mul_sub,sub_mul,mul_one,one_mul]
    congr 1
    rw [← mul_assoc,hc.eq,mul_assoc]
  have hh := Commute.mul_nonneg hp (sub_nonneg.mpr h1) hcom
  simpa only [mul_sub,mul_one,sub_nonneg] using hh

/-- Uniform in epsilon, with a bound depending only on the domain cutoff. -/
theorem regularDomainCut_product_bound (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    regularInverseGeneratorCutoff P ε * (regularDomainCut P δ).val *
      (regularDomainCut P δ).val ≤ (δ⁻¹ : ℂ) • 1 := by
  obtain ⟨hq,hq1⟩ := regularDomainCut_bounds P δ hδ
  have hs := hilbert_commuting_contract_product _ _
    (regularInverseGeneratorCutoff_nonneg P ε hε) hq hq1
    (regularDomainCut_commutes P ε δ hε hδ)
  have hp : 0 ≤ regularInverseGeneratorCutoff P δ * regularInverseGeneratorCutoff P ε :=
    hilbert_positive_product _ _ (regularInverseGeneratorCutoff_nonneg P δ hδ)
      (regularInverseGeneratorCutoff_nonneg P ε hε)
      (regularInverseGeneratorCutoff_commutes P δ ε hδ hε)
  have ho : regularInverseGeneratorCutoff P ε * (regularDomainCut P δ).val ≤
      regularInverseGeneratorCutoff P δ := by
    rw [regularDomainCut_inverse_product P ε δ hε hδ]
    exact sub_le_self _ (hilbert_positive_smul _ hp ε hε.le)
  exact hs.trans (ho.trans (regularInverseGeneratorCutoff_le P δ hδ))

/-- Strong convergence on the SAME Hilbert space. No operator-norm convergence
or spectral gap is assumed. -/
theorem regularDomainCut_tendsto_identity (P : SiteProfile)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => (regularDomainCut P (1/((n : ℝ)+1))).val v) atTop (𝓝 v) := by
  let R := regularSpectralResolvent P
  let S : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P) := 1-R
  let D (n : ℕ) := (1-(regularDomainCut P (1/((n : ℝ)+1))).val)
  have hnD (n : ℕ) : ‖D n‖ ≤ 1 := by
    obtain ⟨hq,hq1⟩ := regularDomainCut_bounds P (1/((n : ℝ)+1)) (by positivity)
    exact hilbert_contract_norm _ (sub_nonneg.mpr hq1) (sub_le_self _ hq)
  have hnq (n : ℕ) : ‖(regularDomainCut P (1/((n : ℝ)+1))).val‖ ≤ 1 := by
    obtain ⟨hq,hq1⟩ := regularDomainCut_bounds P (1/((n : ℝ)+1)) (by positivity)
    exact hilbert_contract_norm _ hq hq1
  have hnR : ‖R‖ ≤ 1 := hilbert_contract_norm _
    (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_le_one P)
  have hd : DenseRange S := ChatgptAudit.Continuous049.bounded_graph_domain_dense S 0
    (regularSpectralResolvent_complement_injective P)
    (IsSelfAdjoint.of_nonneg (sub_nonneg.mpr (regularSpectralResolvent_le_one P)))
  have heq (n : ℕ) : D n * S =
      ((1/((n : ℝ)+1) : ℝ) : ℂ) • (R * (regularDomainCut P (1/((n : ℝ)+1))).val) := by
    have hh := regularDomainCut_inverse_product P (1/((n : ℝ)+1)) 1 (by positivity) (by norm_num)
    simp only [regularDomainCut,Complex.ofReal_one,one_smul,regularInverseGeneratorCutoff_one] at hh
    change regularInverseGeneratorCutoff P (1/((n : ℝ)+1)) * (1-R) =
      R - ((1/((n : ℝ)+1) : ℝ) : ℂ) •
        (R * regularInverseGeneratorCutoff P (1/((n : ℝ)+1))) at hh
    change (1-(1-((1/((n : ℝ)+1) : ℝ) : ℂ) •
      regularInverseGeneratorCutoff P (1/((n : ℝ)+1)))) * (1-R) = _
    rw [sub_sub_cancel,smul_mul_assoc,hh]
    change _ = ((1/((n : ℝ)+1) : ℝ) : ℂ) •
      (R * (1-((1/((n : ℝ)+1) : ℝ) : ℂ) • regularInverseGeneratorCutoff P (1/((n : ℝ)+1))))
    rw [mul_sub,mul_one,mul_smul_comm]
  have he : Equicontinuous (fun n : ℕ => (D n : _ → _)) := by
    apply UniformEquicontinuous.equicontinuous
    apply LipschitzWith.uniformEquicontinuous _ 1
    intro n
    apply LipschitzWith.of_dist_le_mul
    intro x y
    simpa only [dist_eq_norm,← map_sub,NNReal.coe_one,one_mul] using
      (ContinuousLinearMap.le_opNorm (D n) (x-y)).trans
        (mul_le_mul_of_nonneg_right (hnD n) (norm_nonneg (x-y)))
  have hz : ∀ x, Tendsto (fun n => D n x) atTop (𝓝 0) := by
    intro x
    refine hd.induction ?_ (he.isClosed_setOf_tendsto continuous_const) x
    rintro _ ⟨y,rfl⟩
    have hb (n : ℕ) : ‖D n (S y)‖ ≤ (1/((n : ℝ)+1))*‖y‖ := by
      change ‖(D n*S) y‖ ≤ _
      rw [heq]
      simp only [smul_apply,norm_smul,Complex.norm_real,Real.norm_eq_abs,
        abs_of_pos (show 0 < 1/((n : ℝ)+1) by positivity),mul_apply_eq_comp]
      apply mul_le_mul_of_nonneg_left _ (by positivity)
      exact (ContinuousLinearMap.le_opNorm R _).trans
        ((mul_le_mul_of_nonneg_right hnR (norm_nonneg _)).trans (by
          simpa only [one_mul] using (ContinuousLinearMap.le_opNorm _ y).trans
            (mul_le_mul_of_nonneg_right (hnq n) (norm_nonneg y))))
    apply tendsto_zero_iff_norm_tendsto_zero.mpr
    exact squeeze_zero (fun n => norm_nonneg _) hb
      (by simpa only [zero_mul] using
        (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ)).mul_const ‖y‖)
  have hh := (tendsto_const_nhds : Tendsto (fun _ : ℕ => v) atTop (𝓝 v)).sub (hz v)
  simpa only [D,sub_apply,one_apply_eq_self,sub_sub_cancel,sub_zero] using hh

end
end TGLV350.Regular
