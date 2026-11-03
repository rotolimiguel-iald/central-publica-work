import TGLExt.F1Fecho394.NoFiniteInvariantR3
/-! A genuine unitary representation supplies the adjoint, commutation and
norm hypotheses of the finite-invariant obstruction. No continuity premise
is needed for this intermediate theorem. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.UnitaryNoFiniteInvariant
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem inverse_eq (u : ℝ → H ≃ₗᵢ[ℂ] H)
    (h0 : u 0 = LinearIsometryEquiv.refl ℂ H)
    (hadd : ∀ s t, u (s+t) = (u t).trans (u s)) (s : ℝ) :
    (u s).symm = u (-s) := by
  ext x
  apply (u s).injective
  rw [(u s).apply_symm_apply]
  have h := congrArg (fun v : H ≃ₗᵢ[ℂ] H => v x) (hadd s (-s))
  simpa [h0] using h

theorem operators_commute (u : ℝ → H ≃ₗᵢ[ℂ] H)
    (hadd : ∀ s t, u (s+t) = (u t).trans (u s)) (s t : ℝ) :
    Commute (u s : H →L[ℂ] H) (u t : H →L[ℂ] H) := by
  apply ContinuousLinearMap.ext
  intro x
  change u s (u t x) = u t (u s x)
  calc
    _ = u (s+t) x := (congrArg (fun v : H ≃ₗᵢ[ℂ] H => v x) (hadd s t)).symm
    _ = u (t+s) x := by rw [add_comm s t]
    _ = _ := congrArg (fun v : H ≃ₗᵢ[ℂ] H => v x) (hadd t s)

theorem compact_symmetric_commutant_eq_zero (u : ℝ → H ≃ₗᵢ[ℂ] H)
    (h0 : u 0 = LinearIsometryEquiv.refl ℂ H)
    (hadd : ∀ s t, u (s+t) = (u t).trans (u s))
    (hno : ∀ x : H, (∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u s x = c • x) → x = 0)
    (B : H →L[ℂ] H) (hB : IsCompactOperator B) (hs : B.IsSymmetric)
    (hBA : ∀ s, Commute B (u s : H →L[ℂ] H)) : B = 0 := by
  apply NoFiniteInvariant.compact_symmetric_commutant_eq_zero
    (fun s => (u s : H →L[ℂ] H)) ?_ (operators_commute u hadd)
    (fun s x => (u s).norm_map x) hno B hB hs hBA
  intro s
  change (u s : H →L[ℂ] H).adjoint = (u (-s) : H →L[ℂ] H)
  rw [(u s).adjoint_eq_symm, inverse_eq u h0 hadd s]

end F1Fecho.UnitaryNoFiniteInvariant
#print axioms F1Fecho.UnitaryNoFiniteInvariant.inverse_eq
#print axioms F1Fecho.UnitaryNoFiniteInvariant.operators_commute
#print axioms F1Fecho.UnitaryNoFiniteInvariant.compact_symmetric_commutant_eq_zero
