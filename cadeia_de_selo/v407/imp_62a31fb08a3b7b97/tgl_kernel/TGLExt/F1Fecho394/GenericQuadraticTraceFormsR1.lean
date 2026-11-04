import TGLExt.V351QuadraticTrace
/-! Generic form lemmas reused verbatim from proofs incorporated in v393, with a sandbox namespace. They are not a new trace and assume the displayed balance and commutations. -/
set_option autoImplicit false
set_option maxHeartbeats 2400000
noncomputable section
namespace F1Fecho.QuadraticTraceForms
open TGLV350.Regular TGLExt Filter
open scoped Topology ComplexOrder
theorem root_quadratic_commutation {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (R A : H →L[ℂ] H) (hR : 0 ≤ R) (hc : Commute R A) (u : H) :
    inner ℂ (CFC.sqrt R u) (A (CFC.sqrt R u)) = inner ℂ u ((R*A) u) := by
  have hs := (ContinuousLinearMap.nonneg_iff_isPositive _).mp (CFC.sqrt_nonneg R)
  rw [hs.inner_left_eq_inner_right]
  have he : CFC.sqrt R * A * CFC.sqrt R = R*A := by
    rw [positive_sqrt_intertwines R R A hR hR hc.eq, mul_assoc,
      CFC.sqrt_mul_sqrt_self R hR, hc.eq]
  exact congrArg (fun B : H →L[ℂ] H => inner ℂ u (B u)) he

theorem bounded_root_form_balance {H : Type}
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
theorem double_cut_form_supremum {H : Type}
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

theorem represented_positive_root_norm {H K : Type}
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


end F1Fecho.QuadraticTraceForms
#print axioms F1Fecho.QuadraticTraceForms.root_quadratic_commutation
#print axioms F1Fecho.QuadraticTraceForms.bounded_root_form_balance
#print axioms F1Fecho.QuadraticTraceForms.double_cut_form_supremum
#print axioms F1Fecho.QuadraticTraceForms.represented_positive_root_norm
