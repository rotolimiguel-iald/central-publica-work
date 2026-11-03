import TGLExt.V351ModularCutBalance
import TGLExt.V351InverseLimitTracialExtension
import TGLExt.V350PositiveRootIntertwining

set_option autoImplicit false
set_option maxHeartbeats 2400000

namespace TGLV350.Regular
open TGLExt TGLV351 Filter
open scoped Topology ComplexOrder
noncomputable section

private theorem root_quadratic_commutation {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (R A : H →L[ℂ] H) (hR : 0 ≤ R) (hc : Commute R A) (u : H) :
    inner ℂ (CFC.sqrt R u) (A (CFC.sqrt R u)) = inner ℂ u ((R*A) u) := by
  have hs := (ContinuousLinearMap.nonneg_iff_isPositive _).mp (CFC.sqrt_nonneg R)
  rw [hs.inner_left_eq_inner_right]
  have he : CFC.sqrt R * A * CFC.sqrt R = R*A := by
    rw [positive_sqrt_intertwines R R A hR hR hc.eq, mul_assoc,
      CFC.sqrt_mul_sqrt_self R hR, hc.eq]
  exact congrArg (fun B : H →L[ℂ] H => inner ℂ u (B u)) he

private theorem bounded_root_form_balance {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (T U V : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (hi : Function.Injective T)
    (hU : Commute T U) (hV : Commute T V)
    (hb : (1-T)*U = T*V) (x : (resolventSquareRoot T hT hi).domain) :
    inner ℂ (resolventSquareRoot T hT hi x) (U (resolventSquareRoot T hT hi x)) =
      inner ℂ (x : H) (V x) := by
  let u := ChatgptAudit.Continuous049.boundedGraphParameter (CFC.sqrt T)
    (positive_sqrt_injective T hT hi) x
  have hx : CFC.sqrt T u = (x : H) :=
    ChatgptAudit.Continuous049.bounded_graph_parameter_apply (CFC.sqrt T)
      (positive_sqrt_injective T hT hi) x
  have hy : CFC.sqrt (1-T) u = resolventSquareRoot T hT hi x :=
    (ChatgptAudit.Continuous049.bounded_graph_apply (CFC.sqrt T) (CFC.sqrt (1-T))
      (positive_sqrt_injective T hT hi) x).symm
  have he : inner ℂ (CFC.sqrt (1-T) u) (U (CFC.sqrt (1-T) u)) =
      inner ℂ (CFC.sqrt T u) (V (CFC.sqrt T u)) := by
    rw [root_quadratic_commutation (1-T) U (sub_nonneg.mpr h1)
      ((Commute.one_left U).sub_left hU),
      root_quadratic_commutation T V hT hV,hb]
  rw [hx,hy] at he
  exact he

/-- Remove one bounded contraction at a time. The suprema remain in ENNReal;
neither side is assumed finite and no unbounded product is formed. -/
private theorem double_cut_form_supremum {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (C D p q : ℕ → H →L[ℂ] H) (x y : H)
    (hC : ∀ n, 0 ≤ C n) (hD : ∀ n, 0 ≤ D n)
    (hp : ∀ n, 0 ≤ p n ∧ p n ≤ 1) (hq : ∀ n, 0 ≤ q n ∧ q n ≤ 1)
    (hCq : ∀ n m, Commute (C n) (q m))
    (hpD : ∀ n m, Commute (p n) (D m))
    (htp : ∀ v, Tendsto (fun n => p n v) atTop (𝓝 v))
    (htq : ∀ v, Tendsto (fun n => q n v) atTop (𝓝 v))
    (hbalance : ∀ n m, (inner ℂ y ((C n * q m) y)).re =
      (inner ℂ x ((p n * D m) x)).re) :
    (⨆ n, ENNReal.ofReal (inner ℂ y (C n y)).re) =
      ⨆ m, ENNReal.ofReal (inner ℂ x (D m x)).re := by
  have hCQ (n m : ℕ) : C n * q m ≤ C n := by
    apply sub_nonneg.mp
    simpa only [mul_sub,mul_one] using
      Commute.mul_nonneg (hC n) (sub_nonneg.mpr (hq m).2)
        ((Commute.one_right (C n)).sub_right (hCq n m))
  have hpDle (n m : ℕ) : p n * D m ≤ D m := by
    apply sub_nonneg.mp
    simpa only [sub_mul,one_mul] using
      Commute.mul_nonneg (sub_nonneg.mpr (hp n).2) (hD m)
        ((Commute.one_left (D m)).sub_left (hpD n m))
  apply le_antisymm
  · apply iSup_le
    intro n
    have ht : Tendsto (fun m => ENNReal.ofReal (inner ℂ y ((C n*q m) y)).re)
        atTop (𝓝 (ENNReal.ofReal (inner ℂ y (C n y)).re)) :=
      ENNReal.continuous_ofReal.continuousAt.tendsto.comp
        (Complex.continuous_re.continuousAt.tendsto.comp
          (tendsto_const_nhds.inner ((C n).continuous.continuousAt.tendsto.comp (htq y))))
    apply le_of_tendsto ht
    apply Eventually.of_forall
    intro m
    rw [hbalance n m]
    exact (ENNReal.ofReal_le_ofReal (quadratic_le_of_operator_le _ _ (hpDle n m) x)).trans
      (le_iSup (fun j => ENNReal.ofReal (inner ℂ x (D j x)).re) m)
  · apply iSup_le
    intro m
    have ht : Tendsto (fun n => ENNReal.ofReal (inner ℂ x ((p n*D m) x)).re)
        atTop (𝓝 (ENNReal.ofReal (inner ℂ x (D m x)).re)) :=
      ENNReal.continuous_ofReal.continuousAt.tendsto.comp
        (Complex.continuous_re.continuousAt.tendsto.comp
          (tendsto_const_nhds.inner (htp (D m x))))
    apply le_of_tendsto ht
    apply Eventually.of_forall
    intro n
    rw [← hbalance n m]
    exact (ENNReal.ofReal_le_ofReal (quadratic_le_of_operator_le _ _ (hCQ n m) y)).trans
      (le_iSup (fun j => ENNReal.ofReal (inner ℂ y (C j y)).re) n)

set_option maxHeartbeats 6000000 in
private theorem scalar_root_cut_supremum (P : SiteProfile)
    (x : (scalarTomitaPositiveRoot P).domain) :
    (⨆ n : ℕ, ENNReal.ofReal (inner ℂ (scalarTomitaPositiveRoot P x)
      (scalarGNSRepresentation P
        ⟨regularInverseGeneratorCutoff P (1/((n : ℝ)+1)),
          regularInverseGeneratorCutoff_mem P (1/((n : ℝ)+1))⟩
        (scalarTomitaPositiveRoot P x))).re) =
    ⨆ n : ℕ, ENNReal.ofReal (inner ℂ (x : ScalarGNSHilbert P)
      (antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P
          ⟨regularInverseGeneratorCutoff P (1/((n : ℝ)+1)),
            regularInverseGeneratorCutoff_mem P (1/((n : ℝ)+1))⟩) x)).re := by
  letI : NormedSpace ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := inferInstance
  letI : Module ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := ContinuousLinearMap.module
  let N := (regularCoreAlgebra P).toStarSubalgebra
  let π : N →⋆ₐ[ℂ] (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) := scalarGNSRepresentation P
  let J := scalarTomitaPolarFactor P
  let T := scalarTomitaResolvent P
  let δ (n : ℕ) : ℝ := 1/((n : ℝ)+1)
  have hδ (n : ℕ) : 0 < δ n := by dsimp [δ]; positivity
  let c (n : ℕ) : N := ⟨regularInverseGeneratorCutoff P (δ n),regularInverseGeneratorCutoff_mem P (δ n)⟩
  let C (n : ℕ) := π (c n)
  let D (n : ℕ) := antiunitaryConjugate J (C n)
  let p (n : ℕ) := π (regularDomainCut P (δ n))
  let q (n : ℕ) := antiunitaryConjugate J (p n)
  let y := scalarTomitaPositiveRoot P x
  change (⨆ n, ENNReal.ofReal (inner ℂ y (C n y)).re) =
    ⨆ m, ENNReal.ofReal (inner ℂ (x : ScalarGNSHilbert P) (D m x)).re
  have hC (n : ℕ) : 0 ≤ C n :=
    scalarGNSRepresentation_nonneg P (c n) (regularInverseGeneratorCutoff_nonneg P (δ n) (hδ n))
  have hD (n : ℕ) : 0 ≤ D n := antiunitaryConjugate_nonneg J (C n) (hC n)
  have hp (n : ℕ) : 0 ≤ p n ∧ p n ≤ 1 := by
    have hb := regularDomainCut_bounds P (δ n) (hδ n)
    refine ⟨scalarGNSRepresentation_nonneg P _ hb.1,?_⟩
    have hu := scalarGNSRepresentation_monotone P
      (show regularDomainCut P (δ n) ≤ 1 from hb.2)
    simpa only [map_one] using hu
  have hq (n : ℕ) : 0 ≤ q n ∧ q n ≤ 1 := by
    refine ⟨antiunitaryConjugate_nonneg J (p n) (hp n).1,?_⟩
    apply operator_le_of_sub_nonneg
    have hh := antiunitaryConjugate_nonneg J (1-p n)
      (hilbertComplement_nonneg (p n) (hp n).2)
    change 0 ≤ (antiunitaryConjugateRealHom J) (1-p n) at hh
    simp only [map_sub,map_one] at hh
    exact hh
  have htp (v : ScalarGNSHilbert P) : Tendsto (fun n => p n v) atTop (𝓝 v) := by
    have hn (n : ℕ) : ‖(regularDomainCut P (δ n)).val‖ ≤ 1 :=
      (CStarAlgebra.norm_le_norm_of_nonneg_of_le
        (regularDomainCut_bounds P (δ n) (hδ n)).1
        (regularDomainCut_bounds P (δ n) (hδ n)).2).trans ContinuousLinearMap.norm_id_le
    have hh := scalarGNSRepresentation_tendsto_of_uniformly_bounded P
      (fun n => regularDomainCut P (δ n)) 1 1 hn
      (fun v => regularDomainCut_tendsto_identity P v) v
    simpa only [map_one,one_apply_eq_self] using hh
  have htq (v : ScalarGNSHilbert P) : Tendsto (fun n => q n v) atTop (𝓝 v) := by
    have hh := J.continuous.continuousAt.tendsto.comp (htp (J.symm v))
    change Tendsto (fun n => J (p n (J.symm v))) atTop (𝓝 v)
    simpa only [LinearIsometryEquiv.apply_symm_apply,Function.comp_def] using hh
  have hCq (n m : ℕ) : Commute (C n) (q m) :=
    (scalarTomitaPolar_core_commutes P (regularDomainCut P (δ m)) (c n)).symm
  have hpD (n m : ℕ) : Commute (p n) (D m) :=
    (scalarTomitaPolar_core_commutes P (c m) (regularDomainCut P (δ n))).symm
  have hb (n m : ℕ) := scalarTomitaResolvent_double_cut_balance P (δ n) (δ m) (hδ n) (hδ m)
  have hTC (n : ℕ) : Commute T (C n) := (hb n n).1
  have hTD (n : ℕ) : Commute T (D n) := (hb n n).2.1
  have hTp (n : ℕ) : Commute T (p n) := by
    have he : p n = 1-(δ n : ℂ) • C n := by
      change π (1-(δ n : ℂ) • c n) = _
      simp only [map_sub,map_one,map_smul]
      rfl
    change T*p n = p n*T
    ext1 v
    rw [he]
    change T (v-(δ n : ℂ) • C n v) = T v-(δ n : ℂ) • C n (T v)
    rw [map_sub,map_smul]
    exact congrArg (fun z : ScalarGNSHilbert P => T v-(δ n : ℂ) • z)
      (congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => B v) (hTC n).eq)
  have hTq (n : ℕ) : Commute T (q n) := by
    have hh := (hTp n).map (antiunitaryConjugateRealHom J)
    change Commute (antiunitaryConjugate J T) (q n) at hh
    have he : antiunitaryConjugate J T = 1-T := by
      ext1 v
      change J (T (J.symm v)) = v-T v
      rw [scalarTomitaPolarFactor_resolvent,LinearIsometryEquiv.apply_symm_apply]
    rw [he] at hh
    simpa only [sub_sub_cancel] using (Commute.one_left (q n)).sub_left hh
  apply double_cut_form_supremum C D p q x y hC hD hp hq hCq hpD htp htq
  intro n m
  have he := bounded_root_form_balance T (C n*q m) (p n*D m)
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_le_one P)
    (scalarTomitaResolvent_injective P)
    ((hTC n).mul_right (hTq m)) ((hTp n).mul_right (hTD m))
    (by simpa only [mul_assoc] using (hb n m).2.2) x
  exact congrArg Complex.re he

private theorem represented_positive_root_norm {H K : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
    (N : StarSubalgebra ℂ (H →L[ℂ] H))
    (π : N →⋆ₐ[ℂ] (K →L[ℂ] K)) (a : N) (ha : 0 ≤ a.val)
    (hm : hilbertPositiveSqrt a.val ∈ N) (v : K) :
    ‖π (star (⟨hilbertPositiveSqrt a.val,hm⟩ : N)) v‖^2 =
      (inner ℂ v (π a v)).re := by
  let b : N := ⟨hilbertPositiveSqrt a.val,hm⟩
  have hs : star b = b := Subtype.ext (CFC.sqrt_nonneg a.val).isSelfAdjoint.star_eq
  have hbb : b * star b = a := by
    rw [hs]
    exact Subtype.ext (CFC.sqrt_mul_sqrt_self a.val ha)
  have he := ContinuousLinearMap.apply_norm_sq_eq_inner_adjoint_left
    (𝕜 := ℂ) (star (π b)) v
  have hn : ‖star (π b) v‖^2 = (inner ℂ ((π b*star (π b)) v) v).re := by
    simpa only [RCLike.re_eq_complex_re,ContinuousLinearMap.star_eq_adjoint,
      ContinuousLinearMap.adjoint_adjoint,ContinuousLinearMap.mul_def] using he
  change ‖π (star b) v‖^2 = _
  rw [map_star,hn,← map_star,← map_mul,hbb]
  exact inner_re_symm (𝕜 := ℂ) _ _

private theorem scalar_inverse_cutoff_weight_form (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (A : scalarWeightLeftIdeal P) :
    scalarInverseCutoffWeight P ε (positiveSquare P A.val) =
      ENNReal.ofReal (inner ℂ
        ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A))
        (scalarGNSRepresentation P
          ⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩
          ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A)))).re := by
  obtain ⟨hm,he⟩ := scalarWeight_inverseCutoff_perturbed_norm P ε hε A
  change scalarInverseCutoffWeight P ε (positiveSquare P A.val) = _ at he
  rw [he]
  congr 1
  exact represented_positive_root_norm (regularCoreAlgebra P).toStarSubalgebra
    (scalarGNSRepresentation P)
    ⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩
    (regularInverseGeneratorCutoff_nonneg P ε hε) hm _

#print axioms represented_positive_root_norm
#print axioms scalar_inverse_cutoff_weight_form

set_option maxHeartbeats 6000000 in
/-- Traciality of the original inverse-cutoff supremum on the same regular core.
The finite star-core equality is paid by the original Tomita graph and bounded
cut balance; the previously proved extension supplies every bounded element. -/
theorem scalarInverseLimitWeight_tracial (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    scalarInverseLimitWeight P (positiveSquare P A) =
      scalarInverseLimitWeight P (positiveSquare P (star A)) := by
  apply (scalarInverseLimitWeight_tracial_iff_core P).2 ?_ A
  intro a ha
  let b : finiteDualStarCore P := ⟨a,ha⟩
  let J := scalarTomitaPolarFactor P
  let X : scalarClosedTomitaDomain P :=
    ⟨scalarGNSStarEmbedding P b,scalarStarCore_mem_closedTomitaDomain b⟩
  let x : (scalarTomitaPositiveRoot P).domain :=
    Submodule.inclusion (scalarClosedTomitaDomain_le_root P) X
  let y := scalarTomitaPositiveRoot P x
  let C (n : ℕ) := scalarGNSRepresentation P
    ⟨regularInverseGeneratorCutoff P (1/((n : ℝ)+1)),
      regularInverseGeneratorCutoff_mem P (1/((n : ℝ)+1))⟩
  have hx : (x : ScalarGNSHilbert P) = scalarGNSStarEmbedding P b := rfl
  have hJy : J.symm (scalarGNSStarEmbedding P (star b)) = y := by
    apply J.injective
    rw [LinearIsometryEquiv.apply_symm_apply]
    exact (scalarClosedTomita_extends_star b).symm.trans
      (scalarTomitaPolarFactor_factorization P X).symm
  have hw (d : finiteDualStarCore P) :
      scalarInverseLimitWeight P (positiveSquare P d.val) =
        ⨆ n : ℕ, ENNReal.ofReal (inner ℂ (J.symm (scalarGNSStarEmbedding P d))
          (C n (J.symm (scalarGNSStarEmbedding P d)))).re := by
    unfold scalarInverseLimitWeight
    congr 1
    funext n
    let dw : scalarWeightLeftIdeal P :=
      Submodule.inclusion (finiteDualLeftIdeal_le_scalarWeight P) ⟨d.val,d.property.1⟩
    have he := scalar_inverse_cutoff_weight_form P (1/((n : ℝ)+1)) (by positivity) dw
    simp only [dw,scalarWeightGNSEmbedding_uniform] at he
    exact he
  symm
  calc
    scalarInverseLimitWeight P (positiveSquare P (star a)) =
        ⨆ n : ℕ, ENNReal.ofReal (inner ℂ y (C n y)).re := by
      have he := hw (star b)
      rw [hJy] at he
      exact he
    _ = ⨆ n : ℕ, ENNReal.ofReal (inner ℂ (x : ScalarGNSHilbert P)
        (antiunitaryConjugate J (C n) x)).re := scalar_root_cut_supremum P x
    _ = ⨆ n : ℕ, ENNReal.ofReal (inner ℂ (J.symm (scalarGNSStarEmbedding P b))
        (C n (J.symm (scalarGNSStarEmbedding P b)))).re := by
      congr 1
      funext n
      congr 1
      have he := ChatgptAudit.Continuous050.antiunitary_inner_conj J
        (J.symm (x : ScalarGNSHilbert P)) (C n (J.symm x))
      simp only [LinearIsometryEquiv.apply_symm_apply] at he
      have hr := congrArg Complex.re he
      simpa only [antiunitaryConjugate_apply,hx,Complex.star_def,Complex.conj_re] using hr
    _ = scalarInverseLimitWeight P (positiveSquare P a) := (hw b).symm

#print axioms scalarInverseLimitWeight_tracial

#print axioms scalar_root_cut_supremum
#print axioms root_quadratic_commutation
#print axioms bounded_root_form_balance
#print axioms double_cut_form_supremum
end
end TGLV350.Regular
