import TGLExt.F1Fecho394.GeneralInverseSupremumR3
import TGLExt.F1Fecho394.GenericDualSquareFatouR1
/-! Strong lower semicontinuity on squares for the same inverse supremum.
No adjoint convergence, finite upper bound, or traciality is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLV350.Regular Filter
open scoped Topology ENNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:RegularCovariantCore.UnitaryFlow H)

theorem inverseSupremum_square_le_of_strong
    (zeta:RegularHilbert H)
    (A:ℕ→RegularHilbert H→L[ℂ]RegularHilbert H)
    (S:RegularHilbert H→L[ℂ]RegularHilbert H)
    (hlim:∀v,Tendsto (fun n=>A n v) atTop (𝓝 (S v)))
    (C:ℝ≥0∞) (hb:∀n,inverseSupremum B zeta (star (A n)*A n) ≤ C) :
    inverseSupremum B zeta (star S*S) ≤ C := by
  apply iSup_le
  intro e
  let b:=hilbertPositiveSqrt (cutoff B e.val)
  have h := QuadraticTraceForms.dualSquare_le_of_strong
    (fun n=>A n*b) (S*b) zeta (fun v=>hlim (b v)) C (fun n=>?_)
  · simpa only [cutoffWeight,star_mul,mul_assoc,b] using h
  · have hh := (cutoffWeight_le_supremum B zeta e (star (A n)*A n)).trans (hb n)
    simpa only [cutoffWeight,star_mul,mul_assoc,b] using hh
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_square_le_of_strong
