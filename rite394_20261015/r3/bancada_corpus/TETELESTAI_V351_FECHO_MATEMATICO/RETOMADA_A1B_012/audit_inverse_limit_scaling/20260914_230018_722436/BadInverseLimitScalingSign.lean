import TGLExt.V351InverseLimitScaling
open TGLExt TGLV350.Regular
open scoped ENNReal
example (P : SiteProfile) (s : ℝ) (X : PositiveCoreInput P) :
    scalarInverseLimitWeight P (TGLV351.positiveDual P s X) =
      ENNReal.ofReal (Real.exp s) * scalarInverseLimitWeight P X := by
  exact scalarInverseLimitWeight_dual P s X
