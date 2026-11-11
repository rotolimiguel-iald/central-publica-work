import TGLExt.F1Fecho394.GeneralInverseCutoffWeightR3
/-! Supremum over every positive regulator in the same regular representation.
The dual scaling is exact by reindexing; no regulator-order premise is hidden.
Additivity and traciality are deliberately not asserted here. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.RegularInverseWeight
open TGLExt TGLV350.Regular MeasureTheory Filter
open scoped Topology ENNReal NNReal
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B:RegularCovariantCore.UnitaryFlow H)
abbrev PositiveRegulator := {e:ℝ // 0<e}
def inverseSupremum (zeta:RegularHilbert H)
    (X:RegularHilbert H→L[ℂ]RegularHilbert H) : ℝ≥0∞ :=
  ⨆ e:PositiveRegulator, cutoffWeight B zeta e.val X

theorem inverseSupremum_zero (zeta:RegularHilbert H) :
    inverseSupremum B zeta 0=0 := by
  simp only [inverseSupremum,cutoffWeight_zero,iSup_const]

theorem cutoffWeight_le_supremum (zeta:RegularHilbert H) (e:PositiveRegulator)
    (X:RegularHilbert H→L[ℂ]RegularHilbert H) :
    cutoffWeight B zeta e.val X ≤ inverseSupremum B zeta X :=
  le_iSup (fun e:PositiveRegulator=>cutoffWeight B zeta e.val X) e

theorem inverseSupremum_scale (zeta:RegularHilbert H) (r:ℝ≥0)
    (X:RegularHilbert H→L[ℂ]RegularHilbert H) :
    inverseSupremum B zeta ((r:ℝ) • X)=(r:ℝ≥0∞)*inverseSupremum B zeta X := by
  simp only [inverseSupremum,cutoffWeight_scale]
  exact (ENNReal.mul_iSup _ _).symm

theorem inverseSupremum_mono (zeta:RegularHilbert H)
    (X Y:RegularHilbert H→L[ℂ]RegularHilbert H) (hXY:X ≤ Y) :
    inverseSupremum B zeta X ≤ inverseSupremum B zeta Y := by
  apply iSup_le
  intro e
  exact le_iSup_of_le e (cutoffWeight_mono B zeta e.val X Y hXY)

theorem inverseSupremum_subadditive (zeta:RegularHilbert H)
    (X Y:RegularHilbert H→L[ℂ]RegularHilbert H) (hX:0 ≤ X) (hY:0 ≤ Y) :
    inverseSupremum B zeta (X+Y) ≤ inverseSupremum B zeta X+inverseSupremum B zeta Y := by
  apply iSup_le
  intro e
  rw [cutoffWeight_add B zeta e.val X Y hX hY]
  exact add_le_add (cutoffWeight_le_supremum B zeta e X) (cutoffWeight_le_supremum B zeta e Y)

theorem inverseSupremum_normal (zeta:RegularHilbert H)
    {i:Type*} [Preorder i] [IsDirectedOrder i] [Nonempty i]
    (A:i→RegularHilbert H→L[ℂ]RegularHilbert H)
    (S:RegularHilbert H→L[ℂ]RegularHilbert H)
    (hpos:∀j,0 ≤ A j) (hmono:Monotone A)
    (hlim:∀v,Tendsto (fun j=>A j v) atTop (𝓝 (S v))) :
    inverseSupremum B zeta S=⨆j,inverseSupremum B zeta (A j) := by
  simp only [inverseSupremum,cutoffWeight_normal B zeta _ A S hpos hmono hlim]
  exact iSup_comm

theorem supremum_rescale (zeta:RegularHilbert H) (r:ℝ) (hr:0<r)
    (X:RegularHilbert H→L[ℂ]RegularHilbert H) :
    (⨆ e:PositiveRegulator,cutoffWeight B zeta (e.val*r) X)=inverseSupremum B zeta X := by
  apply le_antisymm
  · apply iSup_le
    intro e
    exact cutoffWeight_le_supremum B zeta ⟨e.val*r,mul_pos e.property hr⟩ X
  · apply iSup_le
    intro e
    let d:PositiveRegulator:=⟨e.val/r,div_pos e.property hr⟩
    have hd:d.val*r=e.val := div_mul_cancel₀ e.val (ne_of_gt hr)
    exact le_iSup_of_le d (by rw [hd])

theorem inverseSupremum_dual (zeta:RegularHilbert H) (s:ℝ)
    (X:RegularHilbert H→L[ℂ]RegularHilbert H) :
    inverseSupremum B zeta (dualAmbient s X)=
      ENNReal.ofReal (Real.exp (-s))*inverseSupremum B zeta X := by
  unfold inverseSupremum
  simp only [cutoffWeight_dual B zeta _ (Subtype.property _) s X]
  rw [← ENNReal.mul_iSup]
  exact congrArg (fun q:ℝ≥0∞=>ENNReal.ofReal (Real.exp (-s))*q)
    (supremum_rescale B zeta (Real.exp (-s)) (Real.exp_pos (-s)) X)
end F1Fecho.RegularInverseWeight
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_zero
#print axioms F1Fecho.RegularInverseWeight.cutoffWeight_le_supremum
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_scale
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_mono
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_subadditive
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_normal
#print axioms F1Fecho.RegularInverseWeight.supremum_rescale
#print axioms F1Fecho.RegularInverseWeight.inverseSupremum_dual
