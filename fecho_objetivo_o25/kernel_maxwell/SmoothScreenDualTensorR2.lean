import MaxwellScreenDualTensorR2
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-! The explicit inverse tensor is smooth for smooth profiles vanishing near
the gauge axis, and retains compact support. No spacetime extension is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix Filter Set ChatgptAudit.WignerRapidityMeasure016
open scoped ContDiff Topology

theorem transverseMass_contDiffAt (y : MomentumCoordinates) (hy : y.1≠0) :
    ContDiffAt ℝ ∞ (fun p : MomentumCoordinates=>transverseMass 0 p.1) y := by
  unfold transverseMass
  apply ContDiffAt.sqrt
  · fun_prop
  · have h:=transverseMass_pos_of_ne_zero 0 y.1 hy
    have hs:=transverseMass_sq 0 y.1
    nlinarith

theorem screenRatio_smooth (g : MomentumCoordinates→Fin 2→ℂ)
    (hg : ContDiff ℝ ∞ g) (ε : ℝ) (hε : 0<ε)
    (hv : ∀y : MomentumCoordinates, ‖y.1‖≤ε → g y=0) (j : Fin 2) :
    ContDiff ℝ ∞ (fun y=>g y j/(transverseMass 0 y.1 : ℂ)) := by
  rw [contDiff_iff_contDiffAt]
  intro y
  by_cases hy : y.1=0
  · have hn : ∀ᶠz in 𝓝 y,‖z.1‖<ε := by
      apply (continuous_fst.norm.continuousAt.eventually_lt_const ?_)
      simpa [hy] using hε
    apply contDiffAt_const.congr_of_eventuallyEq
    filter_upwards [hn] with z hz
    simp [hv z hz.le]
  · apply ((contDiff_pi.mp hg j).contDiffAt).div
      (Complex.contDiff_ofReal.contDiffAt.comp y (transverseMass_contDiffAt y hy))
    exact Complex.ofReal_ne_zero.mpr (transverseMass_pos_of_ne_zero 0 y.1 hy).ne'

theorem screenDualProfile_smooth (g : MomentumCoordinates→Fin 2→ℂ)
    (hg : ContDiff ℝ ∞ g) (ε : ℝ) (hε : 0<ε)
    (hv : ∀y : MomentumCoordinates, ‖y.1‖≤ε → g y=0) :
    ContDiff ℝ ∞ (fun y μ ν=>screenDualTensor y.1 (g y) μ ν) := by
  apply contDiff_pi.mpr
  intro μ
  apply contDiff_pi.mpr
  intro ν
  have h0:=screenRatio_smooth g hg ε hε hv 0
  have h1:=screenRatio_smooth g hg ε hε hv 1
  fin_cases μ <;> fin_cases ν <;> simp only [screenDualTensor,
    Matrix.cons_val_zero',Matrix.cons_val_succ',neg_div] <;> fun_prop

theorem screenDualProfile_compact (g : MomentumCoordinates→Fin 2→ℂ)
    (hc : HasCompactSupport g) :
    HasCompactSupport (fun y μ ν=>screenDualTensor y.1 (g y) μ ν) := by
  apply hc.mono
  intro y hy
  contrapose! hy
  have hz : g y=0 := by simpa only [Function.mem_support,not_not] using hy
  simp [screenDualTensor,hz]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.screenRatio_smooth
#print axioms F1Fecho.MaxwellGlobal.screenDualProfile_smooth
#print axioms F1Fecho.MaxwellGlobal.screenDualProfile_compact
