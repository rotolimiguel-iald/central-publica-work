import TGLExt.SummableLikelihoodGenerator
import Mathlib.Analysis.Calculus.Deriv.Shift
import Mathlib.Analysis.Calculus.Deriv.Mul

set_option autoImplicit false
set_option maxHeartbeats 600000
namespace ChatgptAudit.CocycleDerivative
open TGLExt ChatgptAudit ChatgptAudit.Cocycle030
noncomputable section

def canonicalConjugationRealLinear (P : SiteProfile) (t : ℝ) :
    (TowerHilbert P →L[ℂ] TowerHilbert P) →L[ℝ]
      (TowerHilbert P →L[ℂ] TowerHilbert P) where
  toLinearMap := (modularConjugation P t).toLinearMap.restrictScalars ℝ
  cont := modular_conjugation_continuous P t

theorem canonical_conjugation_derivative (P : SiteProfile) (t : ℝ)
    (u : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (d : TowerHilbert P →L[ℂ] TowerHilbert P) (h0 : HasDerivAt u d 0) :
    HasDerivAt (fun r => modularConjugation P t (u r))
      (modularConjugation P t d) 0 := by
  exact (canonicalConjugationRealLinear P t).hasFDerivAt.comp_hasDerivAt 0 h0

theorem canonical_cocycle_hasDerivAt (P : SiteProfile)
    (u : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (d : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hc : ∀ s t : ℝ, u (s+t)=u s*modularConjugation P s (u t))
    (h0 : HasDerivAt u d 0) (t : ℝ) :
    HasDerivAt u (u t*modularConjugation P t d) t := by
  have hm := canonical_conjugation_derivative P t u d h0
  have hp := HasDerivAt.const_mul (u t) hm
  have he : (fun r => u (t+r))=(fun r => u t*modularConjugation P t (u r)) := by
    funext r
    exact hc t r
  rw [←he] at hp
  have hp0 : HasDerivAt (fun r => u (t+r))
      (u t*modularConjugation P t d) (t-t) := by
    simpa only [sub_self] using hp
  have ht := HasDerivAt.comp_sub_const t t hp0
  have hfun : (fun r => u (t+(r-t)))=u := by
    funext r
    congr 1
    ring
  rw [hfun] at ht
  exact ht

theorem canonical_cocycle_generator_equation (P : SiteProfile)
    (u : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (V : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hc : ∀ s t : ℝ, u (s+t)=u s*modularConjugation P s (u t))
    (h0 : HasDerivAt u (Complex.I • V) 0) (t : ℝ) :
    HasDerivAt u (u t*(Complex.I • modularConjugation P t V)) t := by
  simpa only [map_smul] using canonical_cocycle_hasDerivAt P u (Complex.I • V) hc h0 t

theorem canonical_cocycle_differentiable (P : SiteProfile)
    (u : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (d : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hc : ∀ s t : ℝ, u (s+t)=u s*modularConjugation P s (u t))
    (h0 : HasDerivAt u d 0) :
    Differentiable ℝ u :=
  fun t => (canonical_cocycle_hasDerivAt P u d hc h0 t).differentiableAt

#print axioms canonicalConjugationRealLinear
#print axioms canonical_conjugation_derivative
#print axioms canonical_cocycle_hasDerivAt
#print axioms canonical_cocycle_generator_equation
#print axioms canonical_cocycle_differentiable
end
end ChatgptAudit.CocycleDerivative
