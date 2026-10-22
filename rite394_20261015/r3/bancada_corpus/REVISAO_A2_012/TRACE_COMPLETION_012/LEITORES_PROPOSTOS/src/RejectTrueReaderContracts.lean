import TGLExt.V354RegularLegacyWitness
import TGLExt.V354RegularSusy

set_option autoImplicit false
open TGLExt TGLV350.Regular TGLExt.V350Continuous
open TGL.ModularRealization TGLV354 TGLV354.TraceCompletion

#check (True.intro : ContinuousCoreData theSpecificAQFTWitness towerWedgeData)
#check (True.intro :
  ThreeLocksCoreData theSpecificAQFTWitness towerWedgeData regularLegacyCore)
#check (True.intro : TGLModularRealization theSpecificAQFTWitness)
#check (True.intro : FullTGLWitness)
#check (True.intro : (P : SiteProfile) →
  SusyRelativeData (CoreProjection (regularCoreAlgebra P)) (coreProjectionTraceSubadditive P))

