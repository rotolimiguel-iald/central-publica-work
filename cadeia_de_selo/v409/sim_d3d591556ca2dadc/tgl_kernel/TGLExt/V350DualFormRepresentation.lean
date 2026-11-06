import TGLExt.V350DualSquareRootFormBound
import TGLExt.V350DualFormVariationalBound

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter ChatgptAudit.Continuous049
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem boundedPositiveSquareRoot_energy (R : H →L[ℂ] H) (hR : 0 ≤ R) (v : H) :
    ‖boundedPositiveSquareRoot R v‖^2 = (inner ℂ (R v) v).re := by
  have he := bounded_graph_selfadjoint_inner (CFC.sqrt R)
    (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg R)) ((CFC.sqrt R : H →L[ℂ] H) v) v
  have hs : (CFC.sqrt R : H →L[ℂ] H) ((CFC.sqrt R : H →L[ℂ] H) v) = R v :=
    congrArg (fun B : H →L[ℂ] H => B v) (CFC.sqrt_mul_sqrt_self R hR)
  rw [hs] at he
  have he' := congrArg Complex.re he
  have hself : (inner ℂ ((CFC.sqrt R : H →L[ℂ] H) v)
      ((CFC.sqrt R : H →L[ℂ] H) v)).re = ‖(CFC.sqrt R : H →L[ℂ] H) v‖^2 :=
    inner_self_eq_norm_sq (𝕜 := ℂ) _
  exact (he'.trans hself).symm

theorem resolvent_sqrt_pair_norm_sum (R : H →L[ℂ] H) (hR : 0 ≤ R)
    (hone : R ≤ 1) (v : H) :
    ‖boundedPositiveSquareRoot R v‖^2 + ‖boundedPositiveSquareRoot (1-R) v‖^2 = ‖v‖^2 := by
  rw [boundedPositiveSquareRoot_energy R hR,
    boundedPositiveSquareRoot_energy (1-R) (sub_nonneg.mpr hone)]
  change (inner ℂ (R v) v).re + (inner ℂ (v-R v) v).re = ‖v‖^2
  rw [inner_sub_left, Complex.sub_re]
  have hs : (inner ℂ v v).re = ‖v‖^2 := inner_self_eq_norm_sq (𝕜 := ℂ) v
  linarith

/-- The converse inclusion uses variational duality and a bounded Riesz
extension. No finite-form-domain equality is an input. -/
theorem resolventSquareRoot_form_lower_bound
    (R : H →L[ℂ] H) (hR : 0 ≤ R) (hi : Function.Injective R) (hone : R ≤ 1)
    (f : H → ℝ≥0∞) (w : H) (hw : f w < ⊤)
    (hv : ∀ v : H, 2*(inner ℂ w v).re ≤
      (inner ℂ (R v) v).re + ‖w‖^2 + (f w).toReal) :
    ∃ x : (resolventSquareRoot R hR hi).domain,
      (x : H) = w ∧ ENNReal.ofReal (‖resolventSquareRoot R hR hi x‖^2) ≤ f w := by
  let B := boundedPositiveSquareRoot R
  let C := boundedPositiveSquareRoot (1-R)
  let c := ‖w‖^2 + (f w).toReal
  have hc : 0 ≤ c := add_nonneg (sq_nonneg _) ENNReal.toReal_nonneg
  have hvar (v : H) : 2*(inner ℂ w v).re ≤ ‖B v‖^2+c := by
    rw [boundedPositiveSquareRoot_energy R hR]
    simpa only [c,add_assoc] using hv v
  have hb := inner_norm_bound_of_variational_bound B w c hc hvar
  have hd : DenseRange B := resolventSquareRoot_dense R hR hi
  obtain ⟨z,hz,hn⟩ := exists_preimage_of_inner_bound B
    (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg R)) hd w (Real.sqrt c)
    (Real.sqrt_nonneg c) hb
  let x := boundedGraphLift B C (positive_sqrt_injective R hR hi) z
  have hsq : ‖z‖^2 ≤ c := by
    have ht := Real.sq_sqrt hc
    nlinarith only [hn,ht,norm_nonneg z,Real.sqrt_nonneg c]
  have hsum := resolvent_sqrt_pair_norm_sum R hR hone z
  change ‖B z‖^2 + ‖C z‖^2 = ‖z‖^2 at hsum
  rw [hz] at hsum
  have hC : ‖C z‖^2 ≤ (f w).toReal := by
    dsimp only [c] at hsq
    linarith
  refine ⟨x,hz,?_⟩
  have happ : resolventSquareRoot R hR hi x = C z := bounded_graph_lift_apply _ _ _ _
  rw [happ]
  exact (ENNReal.ofReal_le_ofReal hC).trans_eq (ENNReal.ofReal_toReal (ne_of_lt hw))

theorem dualSupportSquareRoot_form_lower_bound
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (w : dualFormSupport A hA) (hw : dualQuadraticIntegral A w < ⊤) :
    ∃ x : (dualSupportSquareRoot A R hA hR hlim).domain,
      (x : dualFormSupport A hA) = w ∧
      ENNReal.ofReal (‖dualSupportSquareRoot A R hA hR hlim x‖^2) ≤ dualQuadraticIntegral A w := by
  apply resolventSquareRoot_form_lower_bound
    (dualSupportResolvent A R hA hlim) (dualSupportResolvent_nonneg A R hA hR hlim)
    (dualSupportResolvent_injective A R hA hR hlim)
    (dualSupportResolvent_le_one A R hA hone hlim)
    (fun u : dualFormSupport A hA => dualQuadraticIntegral A u) w hw
  intro v
  exact dualResolvent_variational_dual_bound A R hA hlim w hw v

theorem dualSupportSquareRoot_domain_iff_finite
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (w : dualFormSupport A hA) :
    w ∈ (dualSupportSquareRoot A R hA hR hlim).domain ↔ dualQuadraticIntegral A w < ⊤ := by
  constructor
  · intro hw
    exact dualSupportSquareRoot_domain_finite A R hA hR hone hlim ⟨w,hw⟩
  · intro hw
    obtain ⟨x,hx,_⟩ := dualSupportSquareRoot_form_lower_bound A R hA hR hone hlim w hw
    exact hx ▸ x.property

theorem dualSupportSquareRoot_form_eq
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (x : (dualSupportSquareRoot A R hA hR hlim).domain) :
    dualQuadraticIntegral A (x : dualFormSupport A hA) =
      ENNReal.ofReal (‖dualSupportSquareRoot A R hA hR hlim x‖^2) := by
  apply le_antisymm (dualSupportSquareRoot_form_upper_bound A R hA hR hone hlim x)
  obtain ⟨y,hy,he⟩ := dualSupportSquareRoot_form_lower_bound A R hA hR hone hlim x
    (dualSupportSquareRoot_domain_finite A R hA hR hone hlim x)
  have heq : y = x := Subtype.ext hy
  simpa only [heq] using he

/-- Extended-valued representation in the full ambient Hilbert space; vectors
of finite energy automatically lie in the constructed support. -/
theorem dualQuadraticIntegral_finite_iff_squareRoot_domain
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hR : 0 ≤ R)
    (hone : R ≤ 1)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (w : RegularHilbert H) :
    dualQuadraticIntegral A w < ⊤ ↔
      ∃ x : (dualSupportSquareRoot A R hA hR hlim).domain,
        ((x : dualFormSupport A hA) : RegularHilbert H) = w := by
  constructor
  · intro hw
    have hK : w ∈ dualFormSupport A hA :=
      Submodule.le_topologicalClosure (dualClosedPositiveForm A hA).finiteDomain hw
    let v : dualFormSupport A hA := ⟨w,hK⟩
    have hv := (dualSupportSquareRoot_domain_iff_finite A R hA hR hone hlim v).mpr hw
    exact ⟨⟨v,hv⟩,rfl⟩
  · rintro ⟨x,rfl⟩
    exact dualSupportSquareRoot_domain_finite A R hA hR hone hlim x

/-- Complete form representation on the same regular construction, starting
with a positive element of its core. No resolvent, root, or domain is an input. -/
theorem exists_dualFormRepresentation (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hmem : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :
    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P),
    ∃ T S : dualFormSupport A hA →ₗ.[ℂ] dualFormSupport A hA,
      R ∈ regularCoreAlgebra P ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      T.IsClosed ∧ Dense (T.domain : Set (dualFormSupport A hA)) ∧ IsSelfAdjoint T ∧
      S.IsClosed ∧ Dense (S.domain : Set (dualFormSupport A hA)) ∧ IsSelfAdjoint S ∧
      (∀ x : S.domain, 0 ≤ (inner ℂ (x : dualFormSupport A hA) (S x)).re) ∧
      partialOperatorSquare S = T ∧
      (∀ w : RegularHilbert (TGLExt.TowerHilbert P), dualQuadraticIntegral A w < ⊤ ↔
        ∃ x : S.domain, ((x : dualFormSupport A hA) : RegularHilbert (TGLExt.TowerHilbert P)) = w) ∧
      (∀ x : S.domain, dualQuadraticIntegral A (x : dualFormSupport A hA) =
        ENNReal.ofReal (‖S x‖^2)) ∧
      (∀ u : dualFormSupport A hA, ∃ x : T.domain,
        ((x : dualFormSupport A hA) : RegularHilbert (TGLExt.TowerHilbert P)) = R u ∧
        (x : dualFormSupport A hA) + T x = u) := by
  obtain ⟨R,hmR,hR,hone,hlim,_⟩ := exists_dualResolvent_limit P A hmem hA
  refine ⟨R, dualSupportOperator A R hA hR hlim, dualSupportSquareRoot A R hA hR hlim,
    hmR,hR,hone,hlim, dualSupportOperator_closed A R hA hR hlim,
    dualSupportOperator_dense A R hA hR hlim, dualSupportOperator_selfadjoint A R hA hR hlim,
    dualSupportSquareRoot_closed A R hA hR hone hlim,
    dualSupportSquareRoot_dense A R hA hR hlim,
    dualSupportSquareRoot_selfadjoint A R hA hR hone hlim,
    dualSupportSquareRoot_positive A R hA hR hlim,
    dualSupportSquareRoot_square A R hA hR hone hlim,
    dualQuadraticIntegral_finite_iff_squareRoot_domain A R hA hR hone hlim,
    dualSupportSquareRoot_form_eq A R hA hR hone hlim, ?_⟩
  intro u
  obtain ⟨x,hx,heq⟩ := dualSupportOperator_resolvent_equation A R hA hR hlim u
  exact ⟨x,congrArg Subtype.val hx,heq⟩

#print axioms boundedPositiveSquareRoot_energy
#print axioms resolvent_sqrt_pair_norm_sum
#print axioms resolventSquareRoot_form_lower_bound
#print axioms dualSupportSquareRoot_form_lower_bound
#print axioms dualSupportSquareRoot_domain_iff_finite
#print axioms dualSupportSquareRoot_form_eq
#print axioms dualQuadraticIntegral_finite_iff_squareRoot_domain
#print axioms exists_dualFormRepresentation
end
end TGLV350.Regular
