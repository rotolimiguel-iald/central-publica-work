import TGLExt.F1Fecho394.ScreenLorentzRepresentationR3
import TGLExt.F1Fecho394.ScreenTransportContinuityR5
import TGLExt.F1Fecho394.ScreenMultiplierContinuityR3

/-! Strong continuity of the actual transverse representation. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter
open scoped Topology
namespace F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial

instance generatedLorentzFirstCountable : FirstCountableTopology generatedLorentz := by
  letI : FirstCountableTopology TGLExt.LorentzGrp := by
    change @FirstCountableTopology {A : Fin 4 → Fin 4 → ℝ // TGLExt.IsLorentz A}
      (TopologicalSpace.induced Subtype.val Pi.topologicalSpace)
    infer_instance
  exact TopologicalSpace.firstCountableTopology_induced generatedLorentz TGLExt.LorentzGrp
    (fun L : generatedLorentz => L.val)

theorem transverseUnitary_strongly_continuous (f : H1) :
    Continuous (fun L : generatedLorentz => transverseUnitary L f) := by
  rw [continuous_iff_continuousAt]
  intro L
  let A := fun M => matrixMultiplier (transportMatrix M) (transportMatrix_measurable M)
    (transportMatrix_unitary_ae M)
  have hm : ContinuousAt (fun M => A M (generatedUnitary L f)) L :=
    matrixMultiplier_continuousAt transportMatrix transportMatrix_measurable transportMatrix_unitary_ae
      L (transportMatrix_continuousAt_ae L) (generatedUnitary L f)
  have hu := (generatedUnitary_strongly_continuous f).continuousAt (x:=L)
  have hbound (M : generatedLorentz) :
      ‖transverseUnitary M f-transverseUnitary L f‖ ≤
      ‖generatedUnitary M f-generatedUnitary L f‖+
      ‖A M (generatedUnitary L f)-A L (generatedUnitary L f)‖ := by
    change ‖A M (generatedUnitary M f)-A L (generatedUnitary L f)‖≤_
    calc
      _ ≤ ‖A M (generatedUnitary M f)-A M (generatedUnitary L f)‖+
          ‖A M (generatedUnitary L f)-A L (generatedUnitary L f)‖ := norm_sub_le_norm_sub_add_norm_sub _ _ _
      _ = _ := by rw [←map_sub]; dsimp [A]; rw [matrixMultiplier_norm]
  have ht : Tendsto (fun M => ‖generatedUnitary M f-generatedUnitary L f‖+
      ‖A M (generatedUnitary L f)-A L (generatedUnitary L f)‖) (𝓝 L) (𝓝 (0:ℝ)) := by
    simpa only [sub_self,norm_zero,add_zero] using
      (hu.tendsto.sub (tendsto_const_nhds (x:=generatedUnitary L f))).norm.add
      (hm.tendsto.sub (tendsto_const_nhds (x:=A L (generatedUnitary L f)))).norm
  apply tendsto_iff_dist_tendsto_zero.mpr
  simp only [dist_eq_norm]
  exact squeeze_zero (fun M => norm_nonneg _) hbound ht

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.transverseUnitary_strongly_continuous
