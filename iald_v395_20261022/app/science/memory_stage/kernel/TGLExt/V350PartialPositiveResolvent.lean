import TGLExt.V350PositiveSurjectiveResolvent
import TGLExt.V350ResolventGraph

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (T : H →ₗ.[ℂ] H)
variable (hp : ∀ x : T.domain, 0 ≤ (inner ℂ (x : H) (T x)).re)
variable (hr : ∀ z : H, ∃ x : T.domain, (x : H)+T x=z)

include hp in
theorem partialPositiveResolvent_coercive (x : T.domain) :
    ‖(x : H)‖ ≤ ‖(x : H)+T x‖ := by
  have hc : (inner ℂ (x : H) ((x : H)+T x)).re ≤ ‖(x : H)‖*‖(x : H)+T x‖ :=
    re_inner_le_norm (𝕜 := ℂ) (x : H) ((x : H)+T x)
  rw [inner_add_right,Complex.add_re] at hc
  have hn : (inner ℂ (x : H) (x : H)).re = ‖(x : H)‖^2 :=
    (norm_sq_eq_re_inner (𝕜 := ℂ) (x : H)).symm
  have hx := hp x
  nlinarith [norm_nonneg (x : H),norm_nonneg ((x : H)+T x)]

def partialOneAdd : T.domain →ₗ[ℂ] H := T.domain.subtype + T.toFun

include hp in
theorem partialOneAdd_injective : Function.Injective (partialOneAdd T) := by
  intro x y h
  have he : partialOneAdd T (x-y)=0 := by rw [map_sub,h,sub_self]
  have hb := partialPositiveResolvent_coercive T hp (x-y)
  change ‖((x-y : T.domain) : H)‖ ≤ ‖partialOneAdd T (x-y)‖ at hb
  rw [he,norm_zero] at hb
  have hz : ((x-y : T.domain) : H)=0 := norm_eq_zero.mp (le_antisymm hb (norm_nonneg _))
  exact sub_eq_zero.mp (Subtype.ext hz)

def partialResolventEquiv : T.domain ≃ₗ[ℂ] H :=
  LinearEquiv.ofBijective (partialOneAdd T)
    ⟨partialOneAdd_injective T hp,hr⟩

/-- The inverse takes values in the actual domain; its inclusion in H is bounded. -/
def partialPositiveResolvent : H →L[ℂ] H :=
  (T.domain.subtype.comp (partialResolventEquiv T hp hr).symm.toLinearMap).mkContinuous 1
    (by
      intro z
      have hb := partialPositiveResolvent_coercive T hp ((partialResolventEquiv T hp hr).symm z)
      have he := (partialResolventEquiv T hp hr).apply_symm_apply z
      change partialOneAdd T ((partialResolventEquiv T hp hr).symm z)=z at he
      change ‖(((partialResolventEquiv T hp hr).symm z : T.domain) : H)‖ ≤ 1*‖z‖
      rw [one_mul]
      exact hb.trans_eq (congrArg norm he))

theorem partialPositiveResolvent_equation (z : H) :
    ∃ x : T.domain, (x : H)=partialPositiveResolvent T hp hr z ∧ (x : H)+T x=z := by
  refine ⟨(partialResolventEquiv T hp hr).symm z,rfl,?_⟩
  exact (partialResolventEquiv T hp hr).apply_symm_apply z

theorem partialPositiveResolvent_inverse (x : T.domain) :
    partialPositiveResolvent T hp hr ((x : H)+T x)=(x : H) := by
  change (((partialResolventEquiv T hp hr).symm ((partialResolventEquiv T hp hr) x) : T.domain) : H)=(x : H)
  rw [LinearEquiv.symm_apply_apply]

theorem partialPositiveResolvent_norm_le (z : H) :
    ‖partialPositiveResolvent T hp hr z‖ ≤ ‖z‖ := by
  obtain ⟨x,hx,he⟩ := partialPositiveResolvent_equation T hp hr z
  rw [← hx,← he]
  exact partialPositiveResolvent_coercive T hp x

theorem partialPositiveResolvent_injective :
    Function.Injective (partialPositiveResolvent T hp hr) := by
  intro z w h
  obtain ⟨x,hx,he⟩ := partialPositiveResolvent_equation T hp hr z
  obtain ⟨y,hy,hf⟩ := partialPositiveResolvent_equation T hp hr w
  have hxy : x=y := Subtype.ext (hx.trans (h.trans hy.symm))
  exact he.symm.trans (hxy ▸ hf)

theorem partialPositiveResolvent_symmetric (hs : T.IsFormalAdjoint T) :
    (partialPositiveResolvent T hp hr).IsSymmetric := by
  intro z w
  obtain ⟨x,hx,he⟩ := partialPositiveResolvent_equation T hp hr z
  obtain ⟨y,hy,hf⟩ := partialPositiveResolvent_equation T hp hr w
  change inner ℂ (partialPositiveResolvent T hp hr z) w =
    inner ℂ z (partialPositiveResolvent T hp hr w)
  rw [← hx,← hy,← he,← hf,inner_add_right,inner_add_left,hs x y]

theorem partialPositiveResolvent_nonneg (hs : T.IsFormalAdjoint T) :
    0 ≤ partialPositiveResolvent T hp hr := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  refine ⟨partialPositiveResolvent_symmetric T hp hr hs,?_⟩
  intro z
  obtain ⟨x,hx,he⟩ := partialPositiveResolvent_equation T hp hr z
  change 0 ≤ (inner ℂ (partialPositiveResolvent T hp hr z) z).re
  rw [← hx,← he,inner_add_right,Complex.add_re]
  have hn : (inner ℂ (x : H) (x : H)).re = ‖(x : H)‖^2 :=
    (norm_sq_eq_re_inner (𝕜 := ℂ) (x : H)).symm
  have hxpos := hp x
  nlinarith [sq_nonneg ‖(x : H)‖]

theorem partialPositiveResolvent_le_one (hs : T.IsFormalAdjoint T) :
    partialPositiveResolvent T hp hr ≤ 1 := by
  apply sub_nonneg.mp
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  have hsa : IsSelfAdjoint (partialPositiveResolvent T hp hr) :=
    ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mpr
      (partialPositiveResolvent_symmetric T hp hr hs)
  apply ContinuousLinearMap.isPositive_def'.mpr
  refine ⟨?_,?_⟩
  · change star (1-partialPositiveResolvent T hp hr)=1-partialPositiveResolvent T hp hr
    rw [star_sub,star_one,hsa.star_eq]
  intro z
  change 0 ≤ (inner ℂ (z-partialPositiveResolvent T hp hr z) z).re
  rw [inner_sub_left,Complex.sub_re]
  have hn : (inner ℂ z z).re = ‖z‖^2 := (norm_sq_eq_re_inner (𝕜 := ℂ) z).symm
  have hc : (inner ℂ (partialPositiveResolvent T hp hr z) z).re ≤
      ‖partialPositiveResolvent T hp hr z‖*‖z‖ :=
    re_inner_le_norm (𝕜 := ℂ) (partialPositiveResolvent T hp hr z) z
  have hb := partialPositiveResolvent_norm_le T hp hr z
  nlinarith [norm_nonneg z]

/-- Equality of graphs, hence domains, with the operator produced from this resolvent. -/
theorem partialPositiveResolvent_graph :
    resolventGraphOperator (partialPositiveResolvent T hp hr)
      (partialPositiveResolvent_injective T hp hr) = T := by
  apply le_antisymm
  · apply LinearPMap.le_of_le_graph
    rintro ⟨x,y⟩ h
    have he := (resolvent_graph_equation _ _ x y).mp h
    obtain ⟨u,hu,hv⟩ := partialPositiveResolvent_equation T hp hr (x+y)
    have hx : (u : H)=x := by
      rw [hu,map_add]
      change x-partialPositiveResolvent T hp hr x=partialPositiveResolvent T hp hr y at he
      rw [← he]
      abel
    have hy : T u=y := by rw [hx] at hv; exact add_left_cancel hv
    exact (LinearPMap.mem_graph_iff T).mpr ⟨u,hx,hy⟩
  · apply LinearPMap.le_of_le_graph
    rintro ⟨x,y⟩ h
    obtain ⟨u,hu,hv⟩ := (LinearPMap.mem_graph_iff T).mp h
    apply (resolvent_graph_equation _ _ x y).mpr
    have he := partialPositiveResolvent_inverse T hp hr u
    rw [hu,hv,map_add] at he
    dsimp only [Prod.fst,Prod.snd] at he
    change x-partialPositiveResolvent T hp hr x=partialPositiveResolvent T hp hr y
    exact sub_eq_iff_eq_add.mpr (he.symm.trans (add_comm _ _))

#print axioms partialPositiveResolvent_coercive
#print axioms partialOneAdd_injective
#print axioms partialResolventEquiv
#print axioms partialPositiveResolvent
#print axioms partialPositiveResolvent_equation
#print axioms partialPositiveResolvent_inverse
#print axioms partialPositiveResolvent_norm_le
#print axioms partialPositiveResolvent_injective
#print axioms partialPositiveResolvent_symmetric
#print axioms partialPositiveResolvent_nonneg
#print axioms partialPositiveResolvent_le_one
#print axioms partialPositiveResolvent_graph
end
end TGLV350.Regular
