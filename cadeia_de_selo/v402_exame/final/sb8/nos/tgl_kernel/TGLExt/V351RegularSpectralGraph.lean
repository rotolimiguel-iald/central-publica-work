import TGLExt.V351RegularPositiveGraph

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

omit [CompleteSpace H] in
theorem sigmoid_resolvent_equation_iff (a : ℝ) (u v : H) :
    ((1 - Real.sigmoid a : ℝ) : ℂ) • u = (Real.sigmoid a : ℂ) • v ↔
      v = (Real.exp (-a) : ℂ) • u := by
  have he : 1 - Real.sigmoid a = Real.sigmoid a * Real.exp (-a) := by
    rw [Real.sigmoid_mul_rexp_neg, Real.sigmoid_neg]
  rw [he, Complex.ofReal_mul, mul_smul]
  have hn : (Real.sigmoid a : ℂ) ≠ 0 :=
    Complex.ofReal_ne_zero.mpr (ne_of_gt (Real.sigmoid_pos a))
  constructor
  · intro h
    have hz : (Real.sigmoid a : ℂ) • ((Real.exp (-a) : ℂ) • u - v) = 0 := by
      rw [smul_sub, h, sub_self]
    exact (sub_eq_zero.mp ((smul_eq_zero.mp hz).resolve_left hn)).symm
  · intro h
    rw [h]

theorem regularSpectralResolvent_coordinate (P : SiteProfile)
    (x : RegularHilbert (TowerHilbert P)) :
    (regularSpectralCoordinates P).symm (regularSpectralResolvent P x) =
      realScalarMultiplier (fun ξ => Real.sigmoid (2*Real.pi*ξ)) (by fun_prop)
        (fun ξ => Real.sigmoid_nonneg _) (fun ξ => Real.sigmoid_le_one _)
        ((regularSpectralCoordinates P).symm x) := by
  simp only [regularSpectralResolvent,
    LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
    LinearIsometryEquiv.symm_apply_apply]

/-- Exact graph identification on the existing regular Hilbert space. The
exponential is unbounded; the condition uses L² representatives almost everywhere. -/
theorem regularPositiveGenerator_graph_iff (P : SiteProfile)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      ∀ᵐ ξ ∂volume, ((regularSpectralCoordinates P).symm y) ξ =
        (Real.exp (-(2*Real.pi*ξ)) : ℂ) •
          ((regularSpectralCoordinates P).symm x) ξ := by
  let V := regularSpectralCoordinates P
  let R := regularSpectralResolvent P
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
  have h0 : ∀ ξ, 0 ≤ g ξ := fun ξ => Real.sigmoid_nonneg _
  have h1 : ∀ ξ, g ξ ≤ 1 := fun ξ => Real.sigmoid_le_one _
  let M := realScalarMultiplier (H := TowerHilbert P) g hg h0 h1
  have hx : V.symm (R x) = M (V.symm x) := regularSpectralResolvent_coordinate P x
  have hy : V.symm (R y) = M (V.symm y) := regularSpectralResolvent_coordinate P y
  change (x,y) ∈ (resolventGraphOperator R (regularSpectralResolvent_injective P)).graph ↔ _
  rw [resolvent_graph_equation]
  constructor
  · intro h
    have hc := congrArg V.symm h
    change V.symm (x-R x) = V.symm (R y) at hc
    rw [map_sub, hx, hy] at hc
    have he := Lp.ext_iff.mp hc
    filter_upwards [he,
      Lp.coeFn_sub (V.symm x) (M (V.symm x)),
      realScalarMultiplier_ae g hg h0 h1 (V.symm x),
      realScalarMultiplier_ae g hg h0 h1 (V.symm y)] with ξ he hs hmx hmy
    have hp : ((1-g ξ : ℝ) : ℂ) • (V.symm x) ξ = (g ξ : ℂ) • (V.symm y) ξ := by
      rw [hs, Pi.sub_apply, hmx, hmy] at he
      simpa only [Pi.sub_apply, Complex.ofReal_sub, Complex.ofReal_one,
        sub_smul, one_smul] using he
    exact (sigmoid_resolvent_equation_iff (2*Real.pi*ξ) _ _).mp hp
  · intro h
    apply V.symm.injective
    change V.symm (x-R x) = V.symm (R y)
    rw [map_sub, hx, hy]
    apply Lp.ext
    filter_upwards [h,
      Lp.coeFn_sub (V.symm x) (M (V.symm x)),
      realScalarMultiplier_ae g hg h0 h1 (V.symm x),
      realScalarMultiplier_ae g hg h0 h1 (V.symm y)] with ξ he hs hmx hmy
    rw [hs, Pi.sub_apply, hmx, hmy]
    have hp := (sigmoid_resolvent_equation_iff (2*Real.pi*ξ)
      ((V.symm x) ξ) ((V.symm y) ξ)).mpr he
    simpa only [Pi.sub_apply, Complex.ofReal_sub, Complex.ofReal_one,
      sub_smul, one_smul] using hp

#print axioms sigmoid_resolvent_equation_iff
#print axioms regularSpectralResolvent_coordinate
#print axioms regularPositiveGenerator_graph_iff
end
end TGLV350.Regular
