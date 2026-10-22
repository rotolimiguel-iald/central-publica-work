import TGLExt.V354ProjectionTraceSubadditivity

set_option autoImplicit false

namespace TGLV354
open TGLExt TGLV350.Regular TGLV351
noncomputable section

/-- The A2 support, placed in the full concrete projection lattice. -/
def regularSupportProjection (P : SiteProfile) : CoreProjection (regularCoreAlgebra P) :=
  CoreProjection.ofOperator (regularCoreAlgebra P) (regularFiniteSupport P).val
    (regularFiniteSupport_projection P) (regularFiniteSupport P).property.1

private theorem regularSupportProjection_operator (P : SiteProfile) :
    (regularSupportProjection P).operator=(regularFiniteSupport P).val :=
  CoreProjection.operator_ofOperator _ _ _ _

private theorem regularSupportProjection_trace (P : SiteProfile) :
    (coreProjectionTraceSubadditive P).tau (regularSupportProjection P)=1 := by
  have he : (regularSupportProjection P).positive P=regularFiniteSupport P :=
    Subtype.ext (regularSupportProjection_operator P)
  change scalarInverseLimitWeight P ((regularSupportProjection P).positive P)=1
  rw [he,regularFiniteSupport_trace]

/-- Concrete bounded representative: D=Hmin, D0=1, perturbation support=PF.
The data use the same N and A1 trace; no microscopic identification is asserted. -/
def regularSusyData (P : SiteProfile) :
    SusyRelativeData (CoreProjection (regularCoreAlgebra P)) (coreProjectionTraceSubadditive P) where
  ker := regularSupportProjection P
  gapD := regularSupportProjection P
  gapD0 := ⊥
  diff := regularSupportProjection P
  free_gap_finite := by
    have he : (⊥ : CoreProjection (regularCoreAlgebra P)).positive P=PositiveCoreInput.zero P :=
      Subtype.ext (CoreProjection.operator_bot _)
    change scalarInverseLimitWeight P ((⊥ : CoreProjection (regularCoreAlgebra P)).positive P)<⊤
    rw [he,scalarInverseLimitWeight_zero]
    exact ENNReal.zero_lt_top
  gap_relative := le_sup_right
  diff_finite := by rw [regularSupportProjection_trace]; exact ENNReal.one_lt_top
  ker_le_gap := le_rfl
  ker_ne_bot := by
    intro h
    have hz := congrArg CoreProjection.operator h
    rw [regularSupportProjection_operator,CoreProjection.operator_bot] at hz
    exact regularFiniteSupport_ne_zero P hz

/-- The actual legacy consumer fires, with all lattice and trace data constructed. -/
theorem regularSusy_gives_breuer (P : SiteProfile) :
    0 < (coreProjectionTraceSubadditive P).tau (regularSusyData P).ker ∧
      (coreProjectionTraceSubadditive P).tau (regularSusyData P).ker < ⊤ :=
  susy_relative_gives_breuer (regularSusyData P)

/-- Concrete identities and the A2 gap accompany the certificate; names alone do not identify operators. -/
theorem regularSusy_operator_identifications (P : SiteProfile) :
    (regularSusyData P).ker.operator=(regularMinimalLock P).ker.starProjection ∧
    (regularSusyData P).gapD.operator=(regularMinimalLock P).ker.starProjection ∧
    (regularSusyData P).gapD0.operator=
      (1 : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)).ker.starProjection ∧
    (regularSusyData P).diff.operator=1-regularMinimalLock P ∧
    (∀ x ∈ (regularMinimalLock P).kerᗮ, ‖regularMinimalLock P x‖=‖x‖) ∧
    (coreProjectionTraceSubadditive P).tau (regularSusyData P).ker=1 := by
  have hs : (regularSupportProjection P).operator=(regularMinimalLock P).ker.starProjection :=
    (regularSupportProjection_operator P).trans (regularMinimalLock_spectral_zero P).symm
  refine ⟨hs,hs,?_,?_,regularMinimalLock_relative_gap P,regularSupportProjection_trace P⟩
  · change (⊥ : CoreProjection (regularCoreAlgebra P)).operator = _
    rw [CoreProjection.operator_bot]
    have hk : (1 : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)).ker=⊥ := by
      ext x
      rfl
    simp only [hk,Submodule.starProjection_bot]
  · change (regularSupportProjection P).operator=1-regularMinimalLock P
    rw [regularSupportProjection_operator]
    simp only [regularMinimalLock,sub_sub_cancel]

#print axioms regularSupportProjection
#print axioms regularSusyData
#print axioms regularSusy_gives_breuer
#print axioms regularSusy_operator_identifications
end
end TGLV354
