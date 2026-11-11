import TGLExt.F1Fecho394.GeneralCutoffAverageCommutationR1
import TGLExt.F1Fecho394.GeneralInverseStrongFatouR1
import TGLExt.F1Fecho394.GeneralPositiveSandwichFaithfulR1
import TGLExt.F1Fecho394.RegularRightAverageR3
import TGLExt.F1Fecho394.RegularFiniteStarCoreR2
import TGLExt.F1Fecho394.GeneralRegularDomainCutR1
import TGLExt.F1Fecho394.RegularCoreFiniteWeightR3
set_option synthInstance.maxHeartbeats 500000
-- BEGIN EXACT BODY GeneralInverseRegularizationR5.lean
/-! Traciality reduces to the existing finite star core for the SAME inverse
supremum. Regular averages decrease both square values; Fatou gives extension.
The remaining finite-core tracial equality is an explicit obligation, not proved
by this reduction. The vacuum-fixed hypothesis is consumed in the weight bound. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open F1Fecho.RegularCovariantCore F1Fecho.RegularCoreAverage
open F1Fecho.RegularFiniteStarCore F1Fecho.RegularPositiveFlow
open scoped Topology ENNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:UnitaryFlow H) (M:VonNeumannAlgebra H) (zeta:RegularHilbert H)
variable (hzeta:∀t:ℝ,fibre (boostCLM B t) zeta=zeta)

include hzeta in
/-- The full dual square value is recovered from the same one-sided regular
averages. They need not be a monotone sequence: strong Fatou and the actual
right-contraction bound provide the two inequalities. -/
theorem dualSquare_eq_iSup_averages
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) :
    dualQuadraticIntegral (star A.val*A.val) zeta =
      ⨆n:ℕ,dualQuadraticIntegral
        (star (A.val*RegularCoreAverage.regularAverage B (1/((n:ℝ)+1)))*
          (A.val*RegularCoreAverage.regularAverage B (1/((n:ℝ)+1)))) zeta := by
  let d:ℕ→ℝ:=fun n=>1/((n:ℝ)+1)
  have hd:Tendsto d atTop (𝓝[≠] (0:ℝ)) := by
    refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
    exact Eventually.of_forall (fun n=>by change (1/((n:ℝ)+1):ℝ)≠0; positivity)
  apply le_antisymm
  · apply QuadraticTraceForms.dualSquare_le_of_strong
      (fun n=>A.val*RegularCoreAverage.regularAverage B (d n)) A.val zeta
      (fun v=>(A.val.continuous.tendsto v).comp
        ((RegularCoreAverage.regularAverage_tendsto_identity B v).comp hd))
    intro n
    exact le_iSup (fun n:ℕ=>dualQuadraticIntegral
      (star (A.val*RegularCoreAverage.regularAverage B (d n))*
        (A.val*RegularCoreAverage.regularAverage B (d n))) zeta) n
  · apply iSup_le
    intro n
    exact RegularRightAverage.scalarWeight_right_average_le B M zeta hzeta A _

include hzeta in
theorem cutoffWeight_right_average_le
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) (e:ℝ) (he:0<e) (d:ℝ) :
    cutoffWeight B zeta e (star (A.val*RegularCoreAverage.regularAverage B d)*
      (A.val*RegularCoreAverage.regularAverage B d)) ≤ cutoffWeight B zeta e (star A.val*A.val) := by
  let b:=hilbertPositiveSqrt (cutoff B e)
  have hb:b∈RegularCovariantCore.core B M := sqrt_mem_core _ _
    (regularInverseGeneratorCutoff_mem B M e) (regularInverseGeneratorCutoff_nonneg B e he)
  have hc:=regularInverseCutoffSqrt_commutes_average B e he d
  have hprod:(A.val*RegularCoreAverage.regularAverage B d)*b=
      (A.val*b)*RegularCoreAverage.regularAverage B d := by
    rw [mul_assoc,←hc.eq,←mul_assoc]
  have h:=RegularRightAverage.scalarWeight_right_average_le B M zeta hzeta
    (A*⟨b,hb⟩) d
  change dualQuadraticIntegral
    (star b*(star (A.val*RegularCoreAverage.regularAverage B d)*
      (A.val*RegularCoreAverage.regularAverage B d))*b) zeta ≤
    dualQuadraticIntegral (star b*(star A.val*A.val)*b) zeta
  have hs:star b*(star (A.val*RegularCoreAverage.regularAverage B d)*
      (A.val*RegularCoreAverage.regularAverage B d))*b=
    star ((A.val*b)*RegularCoreAverage.regularAverage B d)*
      ((A.val*b)*RegularCoreAverage.regularAverage B d) := by
    rw [←hprod]
    simp only [star_mul,mul_assoc]
  rw [hs]
  simpa only [MulMemClass.coe_mul,star_mul,mul_assoc] using h

include hzeta in
theorem inverseSupremum_right_average_le
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) (d:ℝ) :
    inverseSupremum B zeta (star (A.val*RegularCoreAverage.regularAverage B d)*
      (A.val*RegularCoreAverage.regularAverage B d)) ≤ inverseSupremum B zeta (star A.val*A.val) := by
  apply iSup_le
  intro e
  exact (cutoffWeight_right_average_le B M zeta hzeta A e.val e.property d).trans
    (cutoffWeight_le_supremum B zeta e (star A.val*A.val))

private theorem star_norm_le_one {E:Type}
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    (c:E→L[ℂ]E) (hc:‖c‖≤1) : ‖star c‖≤1 := by
  rw [_root_.norm_star]
  exact hc

theorem contraction_left_square {E:Type}
    [NormedAddCommGroup E] [InnerProductSpace ℂ E] [CompleteSpace E]
    (c a:E→L[ℂ]E) (hc:‖c‖≤1) : star (c*a)*(c*a)≤ star a*a := by
  have hn:‖star c*c‖≤1 := by
    calc
      _ ≤ ‖star c‖*‖c‖ := norm_mul_le _ _
      _ = ‖c‖*‖c‖ := by rw [_root_.norm_star]
      _ ≤ 1*1 := mul_le_mul hc hc (norm_nonneg _) zero_le_one
      _ = 1 := one_mul 1
  have hs:star c*c≤1 :=
    (CStarAlgebra.norm_le_one_iff_of_nonneg (star c*c) (star_mul_self_nonneg c)).mp hn
  simpa only [star_mul,mul_assoc,one_mul] using star_left_conjugate_le_conjugate hs a

include hzeta in
theorem inverseSupremum_sandwich_le
    (A:(RegularCovariantCore.core B M).toStarSubalgebra) (d:ℝ) :
    inverseSupremum B zeta (star (RegularFiniteStarCore.regularSandwich B M A d).val*
      (RegularFiniteStarCore.regularSandwich B M A d).val) ≤
        inverseSupremum B zeta (star A.val*A.val) := by
  let e:=RegularCoreAverage.regularAverage B d
  have he:‖star e‖≤1 := star_norm_le_one e (RegularCoreAverage.regularAverage_norm_le_one B d)
  have ho:=contraction_left_square (star e) (A.val*e) he
  have hp:star (RegularFiniteStarCore.regularSandwich B M A d).val*
      (RegularFiniteStarCore.regularSandwich B M A d).val ≤ star (A.val*e)*(A.val*e) := by
    change star (star e*A.val*e)*(star e*A.val*e)≤ star (A.val*e)*(A.val*e)
    simpa only [mul_assoc] using ho
  exact (inverseSupremum_mono B zeta _ _ hp).trans
    (inverseSupremum_right_average_le B M zeta hzeta A d)

include hzeta in
theorem inverseSupremum_tracial_iff_core :
    (∀A:(RegularCovariantCore.core B M).toStarSubalgebra,
      inverseSupremum B zeta (star A.val*A.val)=inverseSupremum B zeta (A.val*star A.val)) ↔
    (∀A:(RegularCovariantCore.core B M).toStarSubalgebra,
      A∈RegularFiniteStarCore.finiteDualStarCore B M →
      inverseSupremum B zeta (star A.val*A.val)=inverseSupremum B zeta (A.val*star A.val)) := by
  constructor
  · exact fun h A _=>h A
  · intro hcore
    have hle (A:(RegularCovariantCore.core B M).toStarSubalgebra) :
        inverseSupremum B zeta (star A.val*A.val) ≤ inverseSupremum B zeta (A.val*star A.val) := by
      let d:ℕ→ℝ:=fun n=>1/((n:ℝ)+1)
      have hd:Tendsto d atTop (𝓝[>] (0:ℝ)) := by
        refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
        exact Eventually.of_forall (fun n=>by change (0:ℝ)<1/((n:ℝ)+1); positivity)
      apply inverseSupremum_square_le_of_strong B zeta
        (fun n=>(RegularFiniteStarCore.regularSandwich B M A (d n)).val) A.val
        (fun v=>(RegularFiniteStarCore.regularSandwich_tendsto B M A v).comp hd)
      intro n
      rw [hcore _ (RegularFiniteStarCore.regularSandwich_mem_finiteDualStarCore B M A (d n)
        (by dsimp [d]; positivity))]
      have h:=inverseSupremum_sandwich_le B M zeta hzeta (star A) (d n)
      rw [←RegularFiniteStarCore.regularSandwich_star] at h
      simpa only [StarMemClass.coe_star,star_star] using h
    intro A
    exact le_antisymm (hle A) (by simpa only [StarMemClass.coe_star,star_star] using hle (star A))
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_right_average_le
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_right_average_le
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_sandwich_le
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_tracial_iff_core

#print axioms F1Fecho.RegularInverseWeight.dualSquare_eq_iSup_averages
-- END EXACT BODY GeneralInverseRegularizationR5.lean
-- BEGIN EXACT BODY GeneralInverseFiniteMinorantsR3.lean
/-! Positive minorants in the same represented core. The tracial square law and
an actual finite-square approximate identity are explicit auxiliary hypotheses.
This lemma does not assert either hypothesis for the inverse weight. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open scoped Topology ENNReal NNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:RegularCovariantCore.UnitaryFlow H) (M:VonNeumannAlgebra H)
variable (zeta:RegularHilbert H)

private theorem square_norm_bound {E:Type} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] [CompleteSpace E] (a:E→L[ℂ]E) :
    star a*a ≤ (‖a‖^2:ℝ) • (1:E→L[ℂ]E) := by
  simpa only [Algebra.algebraMap_eq_smul_one] using
    (CStarAlgebra.star_mul_le_algebraMap_norm_sq (a:=a))

private theorem compressed_square_bound {E:Type} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] [CompleteSpace E] (a e:E→L[ℂ]E) :
    (e*a)*star (e*a) ≤ (‖a‖^2:ℝ) • (e*star e) := by
  have h:=star_left_conjugate_le_conjugate (square_norm_bound (star a)) (star e)
  simpa only [star_star,_root_.norm_star,star_mul,mul_assoc,
    mul_smul_comm,smul_mul_assoc,one_mul] using h

/-- A positive square in the existing core, using its actual CFC square root. -/
private theorem core_square_source {E:Type} [NormedAddCommGroup E]
    [InnerProductSpace ℂ E] [CompleteSpace E]
    (N:VonNeumannAlgebra E) (X:N.toStarSubalgebra)
    (hX:0≤X.val) : ∃a:N.toStarSubalgebra,
      star a.val*a.val=X.val := by
  let r:=hilbertPositiveSqrt X.val
  have hr:r∈N:=sqrt_mem_core _ _ X.property hX
  refine ⟨⟨r,hr⟩,?_⟩
  change star (CFC.sqrt X.val)*CFC.sqrt X.val=X.val
  rw [(CFC.sqrt_nonneg X.val).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self X.val hX]

theorem inverseSupremum_finite_minorants_of_contractions
    (htr:∀a:(RegularCovariantCore.core B M).toStarSubalgebra,
      inverseSupremum B zeta (star a.val*a.val)=
        inverseSupremum B zeta (a.val*star a.val))
    (E:ℕ→(RegularCovariantCore.core B M).toStarSubalgebra)
    (hn:∀n,‖(E n).val‖≤1)
    (hf:∀n,inverseSupremum B zeta (star (E n).val*(E n).val)<⊤)
    (ht:∀v,Tendsto (fun n=>(E n).val v) atTop (𝓝 v))
    (X:(RegularCovariantCore.core B M).toStarSubalgebra) (hX:0≤X.val) :
    inverseSupremum B zeta X.val =
      ⨆ (Y:(RegularCovariantCore.core B M).toStarSubalgebra) (_:0≤Y.val)
        (_:Y.val≤X.val) (_:inverseSupremum B zeta Y.val<⊤),
        inverseSupremum B zeta Y.val := by
  obtain ⟨a,ha⟩:=core_square_source (RegularCovariantCore.core B M) X hX
  let Y (n:ℕ):(RegularCovariantCore.core B M).toStarSubalgebra :=
    star (E n*a)*(E n*a)
  have hy (n:ℕ): (Y n).val≤X.val := by
    have hp:=contraction_left_square (E n).val a.val (hn n)
    rw [←ha]
    exact hp
  have hfin (n:ℕ):inverseSupremum B zeta (Y n).val<⊤ := by
    let r:ℝ≥0:=⟨‖a.val‖^2,sq_nonneg _⟩
    have ho:=compressed_square_bound a.val (E n).val
    have hle:=inverseSupremum_mono B zeta _ _ ho
    change inverseSupremum B zeta ((E n).val*a.val*star ((E n).val*a.val)) ≤
      inverseSupremum B zeta ((r:ℝ) • ((E n).val*star (E n).val)) at hle
    rw [inverseSupremum_scale B zeta r,←htr (E n)] at hle
    have hfinite:=hle.trans_lt (ENNReal.mul_lt_top ENNReal.coe_lt_top (hf n))
    exact (htr (E n*a)).trans_lt hfinite
  apply le_antisymm
  · conv_lhs => rw [←ha]
    apply inverseSupremum_square_le_of_strong B zeta
      (fun n=>(E n).val*a.val) a.val (fun v=>ht (a.val v))
    intro n
    exact le_iSup_of_le (Y n) (le_iSup_of_le (star_mul_self_nonneg _)
      (le_iSup_of_le (hy n) (le_iSup_of_le (hfin n) le_rfl)))
  · apply iSup_le
    intro Y
    apply iSup_le
    intro _
    apply iSup_le
    intro hYX
    apply iSup_le
    intro _
    exact inverseSupremum_mono B zeta Y.val X.val hYX
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_finite_minorants_of_contractions
-- END EXACT BODY GeneralInverseFiniteMinorantsR3.lean
-- BEGIN EXACT BODY GeneralInverseFiniteContractionsR3.lean
/-! Construct the SAME regular-average/domain-cut approximate identity.
The domain-cut bound remains explicit here; its concrete polar-right proof is
a separate consumer. No trace or alternative representation is postulated. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular Filter
open F1Fecho.RegularPositiveFlow F1Fecho.RegularCovariantCore
open scoped Topology ENNReal NNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:UnitaryFlow H) (M:VonNeumannAlgebra H) (zeta:RegularHilbert H)

theorem inverseSupremum_finite_contractions_of_domain_bound
    (hbound:∀(a:(core B M).toStarSubalgebra) (d:ℝ), 0<d →
      inverseSupremum B zeta
        (star (a.val*(regularDomainCut B M d).val)*(a.val*(regularDomainCut B M d).val)) ≤
          ENNReal.ofReal d⁻¹*dualQuadraticIntegral (star a.val*a.val) zeta) :
    ∃E:ℕ→(core B M).toStarSubalgebra,
      (∀n,‖(E n).val‖≤1) ∧
      (∀n,inverseSupremum B zeta (star (E n).val*(E n).val)<⊤) ∧
      (∀v,Tendsto (fun n=>(E n).val v) atTop (𝓝 v)) := by
  let d:ℕ→ℝ:=fun n=>1/((n:ℝ)+1)
  have hd(n:ℕ):0<d n:=by dsimp[d];positivity
  let e(n:ℕ):(core B M).toStarSubalgebra:=
    ⟨RegularCoreAverage.regularAverage B (d n),RegularCoreAverage.regularAverage_mem B M (d n)⟩
  let E(n:ℕ):=e n*regularDomainCut B M (d n)
  have hqn(n:ℕ):‖(regularDomainCut B M (d n)).val‖≤1:=by
    obtain ⟨h0,h1⟩:=regularDomainCut_bounds B M (d n) (hd n)
    exact (CStarAlgebra.norm_le_norm_of_nonneg_of_le h0 h1).trans ContinuousLinearMap.norm_id_le
  refine ⟨E,?_,?_,?_⟩
  · intro n
    exact (norm_mul_le _ _).trans (by
      simpa only [one_mul] using mul_le_mul (RegularCoreAverage.regularAverage_norm_le_one B (d n))
        (hqn n) (norm_nonneg _) zero_le_one)
  · intro n
    exact (hbound (e n) (d n) (hd n)).trans_lt
      (ENNReal.mul_lt_top ENNReal.ofReal_lt_top
        (RegularCoreFiniteWeight.regularAverage_dualQuadraticIntegral_lt_top B (d n) (hd n) zeta))
  · intro v
    have ht:Tendsto d atTop (𝓝[≠] (0:ℝ)):=by
      refine tendsto_nhdsWithin_iff.mpr ⟨tendsto_one_div_add_atTop_nhds_zero_nat,?_⟩
      exact Eventually.of_forall (fun n=>ne_of_gt (hd n))
    exact bounded_application_tendsto atTop (fun n=>(e n).val) 1
      (fun n=>RegularCoreAverage.regularAverage_norm_le_one B (d n))
      (fun n=>(regularDomainCut B M (d n)).val v) v v
      (regularDomainCut_tendsto_identity B M v)
      ((RegularCoreAverage.regularAverage_tendsto_identity B v).comp ht)

theorem inverseSupremum_finite_minorants_of_domain_bound
    (hbound:∀(a:(core B M).toStarSubalgebra) (d:ℝ), 0<d →
      inverseSupremum B zeta
        (star (a.val*(regularDomainCut B M d).val)*(a.val*(regularDomainCut B M d).val)) ≤
          ENNReal.ofReal d⁻¹*dualQuadraticIntegral (star a.val*a.val) zeta)
    (htr:∀a:(core B M).toStarSubalgebra,
      inverseSupremum B zeta (star a.val*a.val)=inverseSupremum B zeta (a.val*star a.val))
    (X:(core B M).toStarSubalgebra) (hX:0≤X.val) :
    inverseSupremum B zeta X.val =
      ⨆ (Y:(core B M).toStarSubalgebra) (_:0≤Y.val) (_:Y.val≤X.val)
        (_:inverseSupremum B zeta Y.val<⊤),inverseSupremum B zeta Y.val := by
  obtain ⟨E,hn,hf,ht⟩:=inverseSupremum_finite_contractions_of_domain_bound B M zeta hbound
  exact inverseSupremum_finite_minorants_of_contractions B M zeta htr E hn hf ht X hX
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_finite_contractions_of_domain_bound
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_finite_minorants_of_domain_bound
-- END EXACT BODY GeneralInverseFiniteContractionsR3.lean
