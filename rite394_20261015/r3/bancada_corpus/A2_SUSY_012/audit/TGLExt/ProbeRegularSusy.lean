import TGLExt.V354RegularSusy
set_option autoImplicit false
namespace TGLV354.Probes
open TGLExt
noncomputable section

theorem removing_difference_is_false (P : SiteProfile) :
    ¬ (regularSusyData P).gapD ≤ (regularSusyData P).gapD0 ⊔ ⊥ := by
  change ¬ regularSupportProjection P ≤ (⊥ ⊔ ⊥ : CoreProjection (TGLV350.Regular.regularCoreAlgebra P))
  rw [bot_sup_eq]
  intro h
  exact (regularSusyData P).ker_ne_bot (bot_unique h)

theorem zero_kernel_trace_is_false (P : SiteProfile) :
    (coreProjectionTraceSubadditive P).tau (regularSusyData P).ker ≠ 0 :=
  ne_of_gt (regularSusy_gives_breuer P).1

#print axioms removing_difference_is_false
#print axioms zero_kernel_trace_is_false
end
end TGLV354.Probes
