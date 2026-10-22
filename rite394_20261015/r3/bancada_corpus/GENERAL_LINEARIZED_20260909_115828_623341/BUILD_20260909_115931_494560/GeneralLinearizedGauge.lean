import TGLExt.ContinuumTT
import Mathlib.Analysis.Calculus.FDeriv.Symmetric

set_option autoImplicit false
set_option maxHeartbeats 2400000

namespace ChatgptAudit.GeneralLinearized

open TGLExt
open scoped BigOperators

noncomputable section

abbrev Spacetime := Fin 4 → ℝ
abbrev TensorField := Fin 4 → Fin 4 → Spacetime → ℝ
abbrev CovectorField := Fin 4 → Spacetime → ℝ

theorem smooth_pd (f : Spacetime → ℝ) (hf : ContDiff ℝ ∞ f) (i : Fin 4) :
    ContDiff ℝ ∞ (pd i f) := by
  exact (hf.fderiv_right (by simp)).clm_apply contDiff_const

theorem pd_add_smooth (f g : Spacetime → ℝ)
    (hf : ContDiff ℝ ∞ f) (hg : ContDiff ℝ ∞ g) (i : Fin 4) :
    pd i (fun x => f x + g x) = fun x => pd i f x + pd i g x := by
  funext x
  simp only [pd, fderiv_add (hf.differentiable (by simp) x)
    (hg.differentiable (by simp) x), ContinuousLinearMap.add_apply]

theorem pd_mul_const_smooth (f : Spacetime → ℝ)
    (hf : ContDiff ℝ ∞ f) (c : ℝ) (i : Fin 4) :
    pd i (fun x => c * f x) = fun x => c * pd i f x := by
  funext x
  have hd := (hf.differentiable (by simp) x).hasFDerivAt.const_smul c
  simpa only [pd, smul_eq_mul, ContinuousLinearMap.smul_apply] using
    congrArg (fun L : Spacetime →L[ℝ] ℝ => L (Pi.single i 1)) hd.fderiv

theorem pd_pd_as_second (f : Spacetime → ℝ) (hf : ContDiff ℝ ∞ f)
    (i j : Fin 4) (x : Spacetime) :
    pd i (pd j f) x =
      fderiv ℝ (fderiv ℝ f) x (Pi.single i 1) (Pi.single j 1) := by
  have hdf : Differentiable ℝ (fderiv ℝ f) :=
    (hf.fderiv_right (m := ∞) (by simp)).differentiable (by simp)
  unfold pd
  rw [fderiv_clm_apply (hdf x) (differentiableAt_const (Pi.single j 1))]
  simp

theorem pd_commute_smooth (f : Spacetime → ℝ) (hf : ContDiff ℝ ∞ f)
    (i j : Fin 4) :
    pd i (pd j f) = pd j (pd i f) := by
  funext x
  rw [pd_pd_as_second f hf i j x, pd_pd_as_second f hf j i x]
  exact (hf.contDiffAt.isSymmSndFDerivAt (by simp)).eq _ _

#print axioms Spacetime
#print axioms TensorField
#print axioms CovectorField
#print axioms smooth_pd
#print axioms pd_add_smooth
#print axioms pd_mul_const_smooth
#print axioms pd_pd_as_second
#print axioms pd_commute_smooth

end
end ChatgptAudit.GeneralLinearized
