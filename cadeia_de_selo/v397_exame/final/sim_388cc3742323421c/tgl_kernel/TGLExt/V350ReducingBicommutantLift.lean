import TGLExt.V350ReducingCommutantCompression

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Extension along the dense commutant orbit. Theorems below supply its bound;
the definition alone is not a membership or existence certificate. -/
def reducingBicommutantLift (M : VonNeumannAlgebra H)
    (S : Submodule ℂ H) [CompleteSpace S] (B : S →L[ℂ] S) (v : S) : H →L[ℂ] H :=
  (vectorOrbitLinear M.commutant (B v).val).extendOfNorm
    (vectorOrbitLinear M.commutant v.val)

variable (M : VonNeumannAlgebra H) (S : Submodule ℂ H) [CompleteSpace S]
variable (hS : ∀ a : M.toStarSubalgebra, ∀ x ∈ S, a.val x ∈ S)
variable (B : S →L[ℂ] S)
variable (hB : ∀ Q : S →L[ℂ] S,
  (∀ a : M.toStarSubalgebra,
    Commute Q (reducingStarRepresentation M.toStarSubalgebra.subtype S hS a)) → Commute B Q)
variable (v : S) (hsep : ∀ A ∈ M, A v.val = 0 → A = 0)
include hS hB hsep

theorem reducingBicommutantLift_apply (D : M.commutant.toStarSubalgebra) :
    reducingBicommutantLift M S B v (D.val v.val) = D.val (B v).val := by
  apply LinearMap.extendOfNorm_eq (separating_commutant_orbit_dense M v.val hsep)
  exact ⟨‖B‖,fun D => reducingBicommutant_orbit_bound M S hS B hB D.val D.property v⟩

theorem reducingBicommutantLift_norm : ‖reducingBicommutantLift M S B v‖ ≤ ‖B‖ := by
  apply LinearMap.opNorm_extendOfNorm_le
    (separating_commutant_orbit_dense M v.val hsep) (norm_nonneg B)
  exact fun D => reducingBicommutant_orbit_bound M S hS B hB D.val D.property v

theorem reducingBicommutantLift_mem : reducingBicommutantLift M S B v ∈ M := by
  have hm : reducingBicommutantLift M S B v ∈ M.commutant.commutant := by
    rw [VonNeumannAlgebra.mem_commutant_iff]
    intro D hD
    ext1 x
    refine (separating_commutant_orbit_dense M v.val hsep).induction ?_
      (isClosed_eq (by fun_prop) (by fun_prop)) x
    rintro _ ⟨E,rfl⟩
    change D (reducingBicommutantLift M S B v (E.val v.val)) =
      reducingBicommutantLift M S B v (D (E.val v.val))
    rw [reducingBicommutantLift_apply M S hS B hB v hsep E]
    exact (reducingBicommutantLift_apply M S hS B hB v hsep
      ((⟨D,hD⟩ : M.commutant.toStarSubalgebra) * E)).symm
  simpa only [VonNeumannAlgebra.commutant_commutant] using hm

theorem reducingCommutant_projectedOrbit_dense :
    DenseRange (fun D : M.commutant.toStarSubalgebra =>
      S.orthogonalProjectionOnto (D.val v.val)) := by
  have hp : Function.Surjective S.orthogonalProjectionOnto := by
    intro x
    exact ⟨x.val,Submodule.orthogonalProjectionOnto_mem_subspace_eq_self x⟩
  exact hp.denseRange.comp (separating_commutant_orbit_dense M v.val hsep)
    S.orthogonalProjectionOnto.continuous

theorem reducingBicommutantLift_restrict :
    reducingStarRepresentation M.toStarSubalgebra.subtype S hS
      ⟨reducingBicommutantLift M S B v,reducingBicommutantLift_mem M S hS B hB v hsep⟩ = B := by
  let a : M.toStarSubalgebra :=
    ⟨reducingBicommutantLift M S B v,reducingBicommutantLift_mem M S hS B hB v hsep⟩
  change reducingStarRepresentation M.toStarSubalgebra.subtype S hS a = B
  ext1 x
  refine (reducingCommutant_projectedOrbit_dense M S hS B hB v hsep).induction ?_
    (isClosed_eq (by fun_prop) B.continuous) x
  rintro _ ⟨D,rfl⟩
  calc
    _ = S.orthogonalProjectionOnto
        (reducingBicommutantLift M S B v (D.val v.val)) :=
      (reducing_projection_intertwines M.toStarSubalgebra.subtype S hS a (D.val v.val)).symm
    _ = S.orthogonalProjectionOnto (D.val (B v).val) :=
      congrArg S.orthogonalProjectionOnto (reducingBicommutantLift_apply M S hS B hB v hsep D)
    _ = B (S.orthogonalProjectionOnto (D.val v.val)) := by
      exact (congrArg (fun Q : S →L[ℂ] S => Q v)
        (hB (reducingOperatorCompression S D.val)
          (reducingCommutant_compression_commutes M S hS D.val D.property)).eq).symm

/-- A separating vector inside a reducing subspace yields an actual ambient
preimage of every restricted bicommutant operator, with controlled norm. -/
theorem reducingBicommutant_has_preimage :
    ∃ a : M.toStarSubalgebra,
      reducingStarRepresentation M.toStarSubalgebra.subtype S hS a = B ∧ ‖a.val‖ ≤ ‖B‖ :=
  ⟨⟨reducingBicommutantLift M S B v,reducingBicommutantLift_mem M S hS B hB v hsep⟩,
    reducingBicommutantLift_restrict M S hS B hB v hsep,
    reducingBicommutantLift_norm M S hS B hB v hsep⟩

#print axioms reducingBicommutantLift
#print axioms reducingBicommutantLift_apply
#print axioms reducingBicommutantLift_norm
#print axioms reducingBicommutantLift_mem
#print axioms reducingCommutant_projectedOrbit_dense
#print axioms reducingBicommutantLift_restrict
#print axioms reducingBicommutant_has_preimage
end
end TGLV350.Regular
