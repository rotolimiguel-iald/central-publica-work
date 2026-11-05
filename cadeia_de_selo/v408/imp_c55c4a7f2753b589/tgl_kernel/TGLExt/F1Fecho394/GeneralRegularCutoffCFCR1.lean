import TGLExt.F1Fecho394.GeneralRegularInverseCutoffR1
import TGLExt.V351InverseCutoffCFC
/-! Generalization of the inverse CFC proof incorporated in canonical v393. V351 is the historical source name. The actual graph, flow and cutoff are retained. -/
set_option autoImplicit false
set_option maxHeartbeats 2400000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
namespace F1Fecho.RegularPositiveFlow
open TGLV350.Regular TGLExt ChatgptAudit MeasureTheory Filter
open scoped Topology
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem regularResolvent_cfc_coordinate (B : F1Fecho.RegularCovariantCore.UnitaryFlow H)
    (f : ℂ → ℂ) (hf : Continuous f) (x : RegularHilbert H) :
    (regularSpectralCoordinates B).symm (cfc f (regularSpectralResolvent B) x) =ᵐ[volume]
      fun ξ => f (Real.sigmoid (2*Real.pi*ξ)) • ((regularSpectralCoordinates B).symm x) ξ := by
  let V := regularSpectralCoordinates B
  let M := realScalarMultiplier (H := H) (fun ξ => Real.sigmoid (2*Real.pi*ξ))
    (by fun_prop) (fun ξ => Real.sigmoid_nonneg _) (fun ξ => Real.sigmoid_le_one _)
  have hM : 0 ≤ M := realScalarMultiplier_nonneg _ _ _ _
  have hc := StarAlgHomClass.map_cfc V.conjStarAlgEquiv f M hf.continuousOn
    (StarAlgEquiv.isometry V.conjStarAlgEquiv).continuous
    (IsSelfAdjoint.of_nonneg hM).isStarNormal
    (IsSelfAdjoint.of_nonneg (map_nonneg V.conjStarAlgEquiv hM)).isStarNormal
  change V.symm (cfc f (V.conjStarAlgEquiv M) x) =ᵐ[volume] _
  rw [← hc]
  simp only [LinearIsometryEquiv.conjStarAlgEquiv_apply_apply,LinearIsometryEquiv.symm_apply_apply]
  exact realScalarMultiplier_cfc_ae _ _ _ _ f hf (V.symm x)

/-- Identify the existing inverse by its already proved graph equation.
There is no new inverse, generator, or change of representation. -/
theorem regularInverseGeneratorCutoff_cfc (B : F1Fecho.RegularCovariantCore.UnitaryFlow H) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff B ε =
      cfc (inverseCutoffFunction ε) (regularSpectralResolvent B) := by
  ext1 x
  let Y := cfc (inverseCutoffFunction ε) (regularSpectralResolvent B)
  let V := regularSpectralCoordinates B
  have hh : (Y x,x-(ε : ℂ) • Y x) ∈ (regularPositiveGenerator B).graph := by
    rw [regularPositiveGenerator_graph_iff,map_sub,map_smul]
    filter_upwards [regularResolvent_cfc_coordinate B (inverseCutoffFunction ε)
        (inverseCutoffFunction_continuous ε hε) x,
      Lp.coeFn_sub (V.symm x) ((ε : ℂ) • V.symm (Y x)),
      Lp.coeFn_smul (ε : ℂ) (V.symm (Y x))] with ξ hy hs hm
    change (V.symm x-(ε : ℂ) • V.symm (Y x)) ξ =
      (Real.exp (-(2*Real.pi*ξ)) : ℂ) • (V.symm (Y x)) ξ
    rw [hs,Pi.sub_apply,hm,Pi.smul_apply]
    change (V.symm x) ξ-(ε : ℂ) • (V.symm (Y x)) ξ =
      (Real.exp (-(2*Real.pi*ξ)) : ℂ) • (V.symm (Y x)) ξ
    have hy' : (V.symm (Y x)) ξ =
        inverseCutoffFunction ε (Real.sigmoid (2*Real.pi*ξ)) • (V.symm x) ξ := hy
    rw [hy',inverseCutoffFunction_sigmoid ε _ hε]
    have hc : (1 : ℂ)-(ε : ℂ)*(((ε+Real.exp (-(2*Real.pi*ξ)))⁻¹ : ℝ) : ℂ) =
        (Real.exp (-(2*Real.pi*ξ)) : ℂ) *
          (((ε+Real.exp (-(2*Real.pi*ξ)))⁻¹ : ℝ) : ℂ) := by
      have hn : (ε+Real.exp (-(2*Real.pi*ξ)) : ℂ) ≠ 0 := by
        exact_mod_cast ne_of_gt (add_pos hε (Real.exp_pos (-(2*Real.pi*ξ))))
      simp only [Complex.ofReal_inv,Complex.ofReal_add]
      field_simp [hn]
      ring
    simpa only [sub_smul,one_smul,smul_smul] using congrArg (fun c : ℂ => c • (V.symm x) ξ) hc
  have hi := (regularInverseGeneratorCutoff_graph_iff B ε hε (Y x) (x-(ε : ℂ) • Y x)).mp hh
  simpa only [sub_add_cancel] using hi


end F1Fecho.RegularPositiveFlow
#print axioms F1Fecho.RegularPositiveFlow.regularResolvent_cfc_coordinate
#print axioms F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_cfc
