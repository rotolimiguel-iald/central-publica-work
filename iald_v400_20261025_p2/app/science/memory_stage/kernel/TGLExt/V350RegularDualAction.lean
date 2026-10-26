import TGLExt.V350GeneratedEquivariance
import TGLExt.V350L2CharacterMultiplier

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open TGLExt ChatgptAudit
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def dualImplementer (s : ℝ) : unitary (RegularHilbert H →L[ℂ] RegularHilbert H) :=
  ⟨characterMultiplier s, by
    rw [Unitary.mem_iff]
    exact characterMultiplier_unitary s⟩

def dualAmbient (s : ℝ) :
    (RegularHilbert H →L[ℂ] RegularHilbert H) ≃⋆ₐ[ℂ]
      (RegularHilbert H →L[ℂ] RegularHilbert H) :=
  Unitary.conjStarAlgAut ℂ _ (dualImplementer s)

theorem dualAmbient_apply (s : ℝ) (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualAmbient s A = characterMultiplier s * A * star (characterMultiplier (H := H) s) := rfl

theorem dualAmbient_zero : dualAmbient (H := H) 0 = StarAlgEquiv.refl := by
  ext A
  simp [dualAmbient_apply, characterMultiplier_zero]

theorem dualAmbient_add (s t : ℝ) :
    dualAmbient (H := H) (s+t) = (dualAmbient (H := H) s).trans (dualAmbient (H := H) t) := by
  have hD : characterMultiplier (H := H) (s+t) = characterMultiplier t * characterMultiplier s := by
    rw [characterMultiplier_mul, add_comm]
  apply StarAlgEquiv.ext
  intro A
  change characterMultiplier (H := H) (s+t) * A * star (characterMultiplier (H := H) (s+t)) =
    characterMultiplier (H := H) t * (characterMultiplier (H := H) s * A * star (characterMultiplier (H := H) s)) *
      star (characterMultiplier (H := H) t)
  rw [hD, star_mul]
  simp only [mul_assoc]

theorem dualAmbient_symm (s : ℝ) :
    (dualAmbient (H := H) s).symm = dualAmbient (-s) := by
  apply StarAlgEquiv.ext
  intro A
  change star (characterMultiplier (H := H) s) * A * characterMultiplier s =
    characterMultiplier (-s) * A * star (characterMultiplier (H := H) (-s))
  rw [characterMultiplier_star, characterMultiplier_star, neg_neg]

theorem dualAmbient_fibre (s : ℝ) (A : H →L[ℂ] H) : dualAmbient s (fibre A) = fibre A := by
  rw [dualAmbient_apply, characterMultiplier_commutes_fibre, mul_assoc,
    (characterMultiplier_unitary s).2, mul_one]

theorem dualAmbient_regular (P : SiteProfile) (s t : ℝ) :
    dualAmbient s (regularUnitary P t) = characterPhase s t • regularUnitary P t := by
  rw [dualAmbient_apply]
  unfold regularUnitary
  calc
    _ = fibre (modularFlowCLM P t) *
        (characterMultiplier s * shift t * star (characterMultiplier (H := TowerHilbert P) s)) := by
      rw [← mul_assoc (characterMultiplier s), characterMultiplier_commutes_fibre]
      simp only [mul_assoc]
    _ = _ := by rw [characterMultiplier_weyl, mul_smul_comm]; rfl

theorem dualAmbient_preserves_generators (P : SiteProfile) (s : ℝ) :
    ∀ A ∈ regularGenerators P, dualAmbient s A ∈ regularCoreAlgebra P := by
  intro A hA
  rcases hA with ⟨B, hB, rfl⟩ | ⟨t, rfl⟩
  · rw [dualAmbient_fibre]
    exact amplified_factor_mem P B hB
  · rw [dualAmbient_regular]
    exact (regularCoreAlgebra P).toStarSubalgebra.smul_mem (regularUnitary_mem P t) _

/-- The dual action is an automorphism of the whole generated algebra, not merely
an assignment on a formal list of generators. No trace is supplied here. -/
def regularDualAction (P : SiteProfile) (s : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra ≃⋆ₐ[ℂ] (regularCoreAlgebra P).toStarSubalgebra :=
  generatedAutomorphism (dualAmbient s) (regularGenerators P)
    (dualAmbient_preserves_generators P s) (by
      rw [dualAmbient_symm]
      exact dualAmbient_preserves_generators P (-s))

theorem regularDualAction_apply (P : SiteProfile) (s : ℝ)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    ((regularDualAction P s A) : RegularHilbert (TowerHilbert P) →L[ℂ]
      RegularHilbert (TowerHilbert P)) = dualAmbient s A := rfl

theorem regularDualAction_zero (P : SiteProfile) : regularDualAction P 0 = StarAlgEquiv.refl := by
  apply StarAlgEquiv.ext
  intro A
  apply Subtype.ext
  change dualAmbient (H := TowerHilbert P) 0
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) = A
  rw [dualAmbient_zero]
  rfl

theorem regularDualAction_add (P : SiteProfile) (s t : ℝ) :
    regularDualAction P (s+t) = (regularDualAction P s).trans (regularDualAction P t) := by
  apply StarAlgEquiv.ext
  intro A
  apply Subtype.ext
  change dualAmbient (H := TowerHilbert P) (s+t)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) =
    dualAmbient (H := TowerHilbert P) t (dualAmbient (H := TowerHilbert P) s A)
  rw [dualAmbient_add]
  rfl

theorem regularDualAction_fixes_embedding (P : SiteProfile) (s : ℝ)
    (A : (theFactorObject P).toStarSubalgebra) :
    regularDualAction P s (regularCoreEmbedding P A) = regularCoreEmbedding P A := by
  apply Subtype.ext
  change dualAmbient (H := TowerHilbert P) s (fibre (A : TowerHilbert P →L[ℂ] TowerHilbert P)) =
    fibre (A : TowerHilbert P →L[ℂ] TowerHilbert P)
  exact dualAmbient_fibre (H := TowerHilbert P) s (A : TowerHilbert P →L[ℂ] TowerHilbert P)

theorem characterMultiplier_jointly_continuous :
    Continuous (fun p : RegularHilbert H × ℝ => characterMultiplier p.2 p.1) := by
  exact continuous_prod_of_continuous_lipschitzWith _ 1
    characterMultiplier_strongly_continuous
    (fun s => (characterMultiplierIsometry s).isometry.lipschitz)

theorem dualAmbient_strongly_continuous
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (f : RegularHilbert H) :
    Continuous (fun s : ℝ => dualAmbient s A f) := by
  have hi : Continuous (fun s : ℝ => A (characterMultiplier (-s) f)) :=
    A.continuous.comp ((characterMultiplier_strongly_continuous f).comp continuous_neg)
  have hc := (characterMultiplier_jointly_continuous (H := H)).comp
    (hi.prodMk continuous_id)
  refine hc.congr ?_
  intro s
  change characterMultiplier s (A (characterMultiplier (-s) f)) = dualAmbient s A f
  rw [dualAmbient_apply, characterMultiplier_star]
  rfl

/-- Fixed dual automorphisms preserve strong continuity of arbitrary operator families. -/
theorem dualAmbient_preserves_strong_continuity {Z : Type} [TopologicalSpace Z]
    (s : ℝ) (A : Z → (RegularHilbert H →L[ℂ] RegularHilbert H))
    (hA : ∀ f : RegularHilbert H, Continuous (fun z => A z f))
    (f : RegularHilbert H) : Continuous (fun z => dualAmbient s (A z) f) := by
  have hc := (characterMultiplier (H := H) s).continuous.comp
    (hA (star (characterMultiplier (H := H) s) f))
  exact hc

theorem regularDualAction_strongly_continuous (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (f : RegularHilbert (TowerHilbert P)) :
    Continuous (fun s : ℝ => (regularDualAction P s A).val f) :=
  dualAmbient_strongly_continuous A f

#print axioms regularDualAction
#print axioms regularDualAction_add
#print axioms regularDualAction_fixes_embedding
#print axioms dualAmbient_regular
#print axioms regularDualAction_strongly_continuous
#print axioms dualAmbient_preserves_strong_continuity
end
end TGLV350.Regular
