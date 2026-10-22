import TGLExt.V350ModularCertificate

set_option autoImplicit false
namespace TGLExt.V350Gate
noncomputable section

/-- Exact type bridges, independent of the names read by the Python parser. -/
def checkedConverse : (P : SiteProfile) → ConverseClauseContract P :=
  qgConverse_JMJ_contains_commutant
def checkedModular : ModularRealizationCertificate :=
  qgFrontier_modularRealization
def checkedActIII : ModularRealizationCertificate :=
  qgPrice_towerActIII_inhabitantConstructed

#print axioms checkedConverse
#print axioms checkedModular
#print axioms checkedActIII
end
end TGLExt.V350Gate
