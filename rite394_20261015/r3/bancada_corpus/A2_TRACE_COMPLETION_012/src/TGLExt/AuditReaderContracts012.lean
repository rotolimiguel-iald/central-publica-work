import TGLExt.V354RegularLegacyWitness
import TGLExt.V354RegularSusy

set_option autoImplicit false
open TGLExt TGLV350.Regular TGLExt.V350Continuous
open TGL.ModularRealization TGLV354 TGLV354.TraceCompletion

-- Add these casts to the existing canonical audit. No new aliases or theorem layer.
#check (regularLegacyCore : ContinuousCoreData theSpecificAQFTWitness towerWedgeData)
#check (regularLegacyThreeLocks :
  ThreeLocksCoreData theSpecificAQFTWitness towerWedgeData regularLegacyCore)
#check (regularModularRealization : TGLModularRealization theSpecificAQFTWitness)
#check (regularFullWitness : FullTGLWitness)
#check (regularSusyData : (P : SiteProfile) →
  SusyRelativeData (CoreProjection (regularCoreAlgebra P)) (coreProjectionTraceSubadditive P))

#print axioms regularLegacyCore
#print axioms regularLegacyThreeLocks
#print axioms regularModularRealization
#print axioms regularFullWitness
#print axioms regularSusyData

