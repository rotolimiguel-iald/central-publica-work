import TGLExt.F1Fecho394.GeneralRegularPositiveGraphR2
import TGLExt.V351RegularSpectralGraph
/-! The exact graph of the generic regular positive generator is the same
exponential multiplication graph in its actual Fourier/boost coordinate. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular TGLExt ChatgptAudit MeasureTheory Filter
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem regularSpectralResolvent_coordinate (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (x : RegularHilbert (H)) :
    (regularSpectralCoordinates B).symm (regularSpectralResolvent B x) =
      realScalarMultiplier (fun ξ => Real.sigmoid (2*Real.pi*ξ)) (by fun_prop)
        (fun ξ => Real.sigmoid_nonneg _) (fun ξ => Real.sigmoid_le_one _)
        ((regularSpectralCoordinates B).symm x) := by
  simp only [regularSpectralResolvent,
    LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,
    LinearIsometryEquiv.symm_apply_apply]

/-- Exact graph identification on the existing regular Hilbert space. The
exponential is unbounded; the condition uses L² representatives almost everywhere. -/
theorem regularPositiveGenerator_graph_iff (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (x y : RegularHilbert (H)) :
    (x,y) ∈ (regularPositiveGenerator B).graph ↔
      ∀ᵐ ξ ∂volume, ((regularSpectralCoordinates B).symm y) ξ =
        (Real.exp (-(2*Real.pi*ξ)) : ℂ) •
          ((regularSpectralCoordinates B).symm x) ξ := by
  let V := regularSpectralCoordinates B
  let R := regularSpectralResolvent B
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
  have h0 : ∀ ξ, 0 ≤ g ξ := fun ξ => Real.sigmoid_nonneg _
  have h1 : ∀ ξ, g ξ ≤ 1 := fun ξ => Real.sigmoid_le_one _
  let M := realScalarMultiplier (H := H) g hg h0 h1
  have hx : V.symm (R x) = M (V.symm x) := regularSpectralResolvent_coordinate B x
  have hy : V.symm (R y) = M (V.symm y) := regularSpectralResolvent_coordinate B y
  change (x,y) ∈ (resolventGraphOperator R (regularSpectralResolvent_injective B)).graph ↔ _
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


end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.regularSpectralResolvent_coordinate
#print axioms F1Fecho.RegularPositiveFlow.regularPositiveGenerator_graph_iff
