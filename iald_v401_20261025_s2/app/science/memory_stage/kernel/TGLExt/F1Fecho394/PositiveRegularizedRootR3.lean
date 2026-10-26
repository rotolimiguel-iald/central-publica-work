import TGLExt.O16.SelfadjointSquareResolvent
import TGLExt.V351ResolventPhaseCalculus
/-! The regularized positive root of a prescribed positive selfadjoint operator.
Constructs L = D (1+D²)⁻¹ and proves L = sqrt(R(1-R)); no polar identity is input. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.PositiveRegularized
open TGLV350.Regular ChatgptAudit.UnboundedTransform016
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D)

def R : H →L[ℂ] H := selfadjointSquareResolvent D hs

theorem R_mem (x : H) : R D hs x ∈ D.domain := by
  obtain ⟨u,hu,_⟩ := selfadjoint_square_resolvent_equation D hs x
  change selfadjointSquareResolvent D hs x ∈ D.domain
  rw [← hu]
  exact u.property.choose

def input : H →ₗ[ℂ] D.domain := (R D hs).toLinearMap.codRestrict D.domain (R_mem D hs)

theorem image_mem (x : H) : D (input D hs x) ∈ D.domain := by
  obtain ⟨u,hu,_⟩ := selfadjoint_square_resolvent_equation D hs x
  have he : input D hs x = (⟨u,u.property.choose⟩ : D.domain) := Subtype.ext hu.symm
  rw [he]
  exact u.property.choose_spec

def second (x : H) : D.domain := ⟨D (input D hs x),image_mem D hs x⟩

theorem equation (x : H) : R D hs x + D (second D hs x) = x := by
  obtain ⟨u,hu,he⟩ := selfadjoint_square_resolvent_equation D hs x
  have hv : input D hs x = (⟨u,u.property.choose⟩ : D.domain) := Subtype.ext hu.symm
  have hw : second D hs x =
      (⟨D ⟨u,u.property.choose⟩,u.property.choose_spec⟩ : D.domain) :=
    Subtype.ext (congrArg D hv)
  change (R D hs x) + D (second D hs x) = x
  rw [hw]
  change selfadjointSquareResolvent D hs x + partialOperatorSquare D u = x
  rw [← hu]
  exact he

theorem image_bound (x : H) : ‖D (input D hs x)‖ ≤ ‖x‖ := by
  have hf := selfadjoint_formal D hs (input D hs x) (second D hs x)
  change inner ℂ (D (input D hs x)) (D (input D hs x)) =
    inner ℂ (R D hs x) (D (second D hs x)) at hf
  have he : D (second D hs x)=x-R D hs x := eq_sub_of_add_eq' (equation D hs x)
  rw [he,inner_sub_right] at hf
  have hr := congrArg Complex.re hf
  have hn1 : (inner ℂ (D (input D hs x)) (D (input D hs x))).re =
      ‖D (input D hs x)‖^2 := (norm_sq_eq_re_inner (𝕜:=ℂ) _).symm
  have hn2 : (inner ℂ (R D hs x) (R D hs x)).re = ‖R D hs x‖^2 :=
    (norm_sq_eq_re_inner (𝕜:=ℂ) _).symm
  have hc := re_inner_le_norm (𝕜:=ℂ) (R D hs x) x
  change (inner ℂ (R D hs x) x).re ≤ ‖R D hs x‖ * ‖x‖ at hc
  simp only [Complex.sub_re] at hr
  rw [hn1,hn2] at hr
  nlinarith [norm_nonneg x,norm_nonneg (D (input D hs x)),sq_nonneg (‖R D hs x‖-‖x‖/2)]

def L : H →L[ℂ] H := (D.toFun.comp (input D hs)).mkContinuous 1 (by
  intro x
  change ‖D (input D hs x)‖ ≤ 1 * ‖x‖
  rw [one_mul]
  exact image_bound D hs x)

theorem L_symmetric : (L D hs).IsSymmetric := by
  intro x y
  change inner ℂ (D (input D hs x)) y = inner ℂ x (D (input D hs y))
  have h1 := selfadjoint_formal D hs (input D hs x) (input D hs y)
  have h2 := selfadjoint_formal D hs (second D hs x) (second D hs y)
  calc
    _ = inner ℂ (D (input D hs x)) (R D hs y + D (second D hs y)) :=
      congrArg (inner ℂ (D (input D hs x))) (equation D hs y).symm
    _ = inner ℂ (R D hs x) (D (input D hs y)) +
        inner ℂ (D (second D hs x)) (D (input D hs y)) := by
      rw [inner_add_right]
      exact congrArg₂ (·+·) h1 h2.symm
    _ = inner ℂ (R D hs x + D (second D hs x)) (D (input D hs y)) :=
      (inner_add_left _ _ _).symm
    _ = _ := congrArg (fun z => inner ℂ z (D (input D hs y))) (equation D hs x)

theorem L_selfadjoint : IsSelfAdjoint (L D hs) :=
  ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr (L_symmetric D hs)

variable (hp : ∀ x : D.domain, 0 ≤ (inner ℂ (x:H) (D x)).re)

include hp in
theorem L_nonneg : 0 ≤ L D hs := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  refine ⟨L_symmetric D hs,?_⟩
  intro x
  change 0 ≤ (inner ℂ (D (input D hs x)) x).re
  have he : (inner ℂ (D (input D hs x)) x).re =
      (inner ℂ (D (input D hs x)) (R D hs x)).re +
      (inner ℂ (D (input D hs x)) (D (second D hs x))).re := by
    calc
      _ = (inner ℂ (D (input D hs x)) (R D hs x + D (second D hs x))).re :=
        congrArg (fun z => (inner ℂ (D (input D hs x)) z).re) (equation D hs x).symm
      _ = _ := by rw [inner_add_right,Complex.add_re]
  rw [he]
  have h1 := hp (input D hs x)
  have h2 := hp (second D hs x)
  have hswap : (inner ℂ (D (input D hs x)) (R D hs x)).re =
      (inner ℂ (R D hs x) (D (input D hs x))).re := by
    simpa only [Complex.conj_re] using (congrArg Complex.re (inner_conj_symm (𝕜:=ℂ) (D (input D hs x)) (R D hs x))).symm
  change 0 ≤ (inner ℂ (R D hs x) (D (input D hs x))).re at h1
  change 0 ≤ (inner ℂ (D (input D hs x)) (D (second D hs x))).re at h2
  rw [hswap]
  exact add_nonneg h1 h2

theorem L_square : L D hs * L D hs = resolventDampingOperator (R D hs) := by
  ext y
  apply ext_inner_left ℂ
  intro x
  change inner ℂ x (L D hs (L D hs y)) = inner ℂ x (R D hs (y-R D hs y))
  calc
    _ = inner ℂ (L D hs x) (L D hs y) := ((L_symmetric D hs) x (L D hs y)).symm
    _ = _ := by
      change inner ℂ (D (input D hs x)) (D (input D hs y)) = _
      have hf := selfadjoint_formal D hs (input D hs x) (second D hs y)
      change inner ℂ (D (input D hs x)) (D (input D hs y)) =
        inner ℂ (R D hs x) (D (second D hs y)) at hf
      rw [hf,eq_sub_of_add_eq' (equation D hs y)]
      exact (selfadjoint_square_resolvent_nonneg D hs).isSelfAdjoint.isSymmetric x (y-R D hs y)

include hp in
theorem sqrt_damping : CFC.sqrt (resolventDampingOperator (R D hs)) = L D hs :=
  CFC.sqrt_unique (L_square D hs) (L_nonneg D hs hp)

include hp in
theorem regularized_graph (x : H) :
    (R D hs x,CFC.sqrt (resolventDampingOperator (R D hs)) x) ∈ D.graph := by
  rw [sqrt_damping D hs hp]
  exact (LinearPMap.mem_graph_iff D).mpr ⟨input D hs x,rfl,rfl⟩

end F1Fecho.PositiveRegularized
#print axioms F1Fecho.PositiveRegularized.image_bound
#print axioms F1Fecho.PositiveRegularized.L_symmetric
#print axioms F1Fecho.PositiveRegularized.L_nonneg
#print axioms F1Fecho.PositiveRegularized.L_square
#print axioms F1Fecho.PositiveRegularized.sqrt_damping
#print axioms F1Fecho.PositiveRegularized.regularized_graph
