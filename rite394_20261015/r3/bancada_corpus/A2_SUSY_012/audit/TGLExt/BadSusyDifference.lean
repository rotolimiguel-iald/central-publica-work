import TGLExt.V354RegularSusy
set_option autoImplicit false
namespace TGLV354.Probes
open TGLExt
noncomputable section
-- Deliberate ablation of the perturbation support on the same core.
example (P : SiteProfile) : (regularSusyData P).gapD ≤ (regularSusyData P).gapD0 ⊔ ⊥ :=
  (regularSusyData P).gap_relative
end
end TGLV354.Probes
