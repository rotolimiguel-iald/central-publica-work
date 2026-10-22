import TGLExt.V354RegularSusy
set_option autoImplicit false
namespace TGLV354.Probes
open TGLExt
noncomputable section
-- Deliberate replacement of the actual A1 kernel reading by zero.
example (P : SiteProfile) :
    (coreProjectionTraceSubadditive P).tau (regularSusyData P).ker=0 :=
  (regularSusy_operator_identifications P).2.2.2.2.2
end
end TGLV354.Probes
