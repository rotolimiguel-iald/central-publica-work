import TGLExt.F1Fecho394.PhysicalCompactNetCovarianceR1
import TGLExt.F1Fecho394.PhysicalNetGeometryR1

/-! Exact coordinate adapter and boost covariance for the compact-test
Maxwell net. The existing all-Schwartz coordinate net remains untouched. -/
set_option autoImplicit false
set_option maxHeartbeats 800000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open TGLExt.ImportedSQ TGLExt.ContratoQGv31 F1Fecho.MaxwellGlobal
open F1Fecho.OrbitalScreen F1Fecho.OrbitalSpatial

theorem compactLocalized_boost_iff (s : ℝ) (O : Set Spacetime) (v : H1) :
    v ∈ compactLocalized O ↔ B0 s v ∈ compactLocalized (boostRegion s O) := by
  have h := compactLocalized_lorentz_iff (generatedBoost s) O v
  rw [helicityUnitary_boost] at h
  exact h

def compactPhysicalNet (O : Set (Fin 4 → ℝ)) : Submodule ℝ H1 :=
  compactLocalized (coordinateRegion O)

theorem compactPhysicalNet_mono (O P : Set (Fin 4 → ℝ)) (h : O ⊆ P) :
    compactPhysicalNet O ≤ compactPhysicalNet P := compactLocalized_mono (fun _ hx => h hx)

theorem compactPhysicalNet_translate (a : Fin 4 → ℝ) (O : Set (Fin 4 → ℝ)) (f : H1) :
    f ∈ compactPhysicalNet O ↔ U1 a f ∈ compactPhysicalNet (TGL.SpecificAQFT.translate a O) := by
  unfold compactPhysicalNet
  rw [coordinateRegion_translate]
  exact compactLocalized_translate_iff (spacetimeOf a) (coordinateRegion O) f

theorem compactPhysicalNet_boost (s : ℝ) (O : Set (Fin 4 → ℝ)) (f : H1) :
    f ∈ compactPhysicalNet O ↔ B0 s f ∈ compactPhysicalNet (wedgeBoostMap s '' O) := by
  unfold compactPhysicalNet
  rw [coordinateRegion_boost]
  exact compactLocalized_boost_iff s (coordinateRegion O) f

theorem compactPhysicalNet_rightWedge :
    compactPhysicalNet TGL.SpecificAQFT.rightWedge=compactLocalized physicalRightWedge := rfl

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.compactPhysicalNet_mono
#print axioms F1Fecho.MaxwellLocalization.compactPhysicalNet_translate
#print axioms F1Fecho.MaxwellLocalization.compactPhysicalNet_boost
