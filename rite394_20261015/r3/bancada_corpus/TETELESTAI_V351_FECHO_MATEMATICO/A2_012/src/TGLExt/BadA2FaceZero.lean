import TGLExt.V354TraceReaderWall
open TGLExt TGLV350.Regular
example (P : SiteProfile) :
    (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).Pplus = 0 := by
  exact (regularContinuousCorner_readings P).2.1
