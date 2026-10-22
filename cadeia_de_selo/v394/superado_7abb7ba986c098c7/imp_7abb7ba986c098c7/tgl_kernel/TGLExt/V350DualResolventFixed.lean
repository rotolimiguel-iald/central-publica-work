import TGLExt.V350FormMinimizerUniqueness
import TGLExt.V350DualFormTransport
import TGLExt.V350DualFormRepresentation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem ClosedPositiveForm.minimizer_transport (Q : ClosedPositiveForm H)
    (e : H ≃ₗᵢ[ℂ] H) (hQ : ∀ w : H, Q.value (e w) = Q.value w)
    (v r : H)
    (hr : ∀ w : H, ENNReal.ofReal (‖r-v‖^2) + Q.value r ≤
      ENNReal.ofReal (‖w-v‖^2) + Q.value w) (w : H) :
    ENNReal.ofReal (‖e r-e v‖^2) + Q.value (e r) ≤
      ENNReal.ofReal (‖w-e v‖^2) + Q.value w := by
  rw [← e.map_sub,e.norm_map,hQ r]
  have hw := hr (e.symm w)
  have hn : ‖e.symm w-v‖ = ‖w-e v‖ := by
    rw [← e.norm_map (e.symm w-v),e.map_sub,e.apply_symm_apply]
  have he := hQ (e.symm w)
  rw [e.apply_symm_apply] at he
  simpa only [hn,← he] using hw

/-- Equivariance follows from uniqueness of the variational minimizer.
Linearity of R is not needed in this abstract lemma. -/
theorem ClosedPositiveForm.resolvent_equivariant (Q : ClosedPositiveForm H)
    (R : H → H) (e : H ≃ₗᵢ[ℂ] H)
    (hQ : ∀ w : H, Q.value (e w) = Q.value w)
    (hmin : ∀ v w : H, ENNReal.ofReal (‖R v-v‖^2) + Q.value (R v) ≤
      ENNReal.ofReal (‖w-v‖^2) + Q.value w) (v : H) :
    R (e v) = e (R v) :=
  Q.minimizer_unique (e v) (R (e v)) (e (R v))
    (hmin (e v)) (Q.minimizer_transport e hQ v (R v) (hmin v))

theorem dualResolvent_limit_commutes_character
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (s : ℝ) (v : RegularHilbert H) :
    R (characterMultiplier s v) = characterMultiplier s (R v) := by
  exact (dualClosedPositiveForm A hA).resolvent_equivariant R
    (Unitary.linearIsometryEquiv (dualImplementer s))
    (dualQuadraticIntegral_vector_dual_invariant s A)
    (dualResolvent_limit_minimizes_energy A R hA hlim) v

theorem dualResolvent_limit_dual_fixed
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (s : ℝ) : dualAmbient s R = R := by
  have hc : characterMultiplier s * R = R * characterMultiplier s := by
    apply ContinuousLinearMap.ext
    intro v
    exact (dualResolvent_limit_commutes_character A R hA hlim s v).symm
  rw [dualAmbient_apply,hc,mul_assoc,(characterMultiplier_unitary s).2,mul_one]

theorem dualResolvent_limit_commutes_unitary_commutant
    (P : TGLExt.SiteProfile)
    (A R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) (hpos : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (U : unitary (RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P)))
    (hU : ∀ B ∈ regularCoreAlgebra P, U.val * B = B * U.val)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) : R (U.val v) = U.val (R v) := by
  exact (dualClosedPositiveForm A hpos).resolvent_equivariant R
    (Unitary.linearIsometryEquiv U)
    (dualQuadraticIntegral_commutant_invariant P A hA hpos U hU)
    (dualResolvent_limit_minimizes_energy A R hpos hlim) v

/-- The output resolvent is fixed by the full dual action. Identifying the
entire fixed-point algebra with the original base is a separate obligation. -/
theorem exists_dualResolvent_fixed (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) (hpos : 0 ≤ A) :
    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P),
      R ∈ regularCoreAlgebra P ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      (∀ s : ℝ, dualAmbient s R = R) := by
  obtain ⟨R,hmR,hR,hone,hlim,_⟩ := exists_dualResolvent_limit P A hA hpos
  exact ⟨R,hmR,hR,hone,hlim,dualResolvent_limit_dual_fixed A R hpos hlim⟩

#print axioms ClosedPositiveForm.minimizer_transport
#print axioms ClosedPositiveForm.resolvent_equivariant
#print axioms dualResolvent_limit_commutes_character
#print axioms dualResolvent_limit_dual_fixed
#print axioms dualResolvent_limit_commutes_unitary_commutant
#print axioms exists_dualResolvent_fixed
end
end TGLV350.Regular
