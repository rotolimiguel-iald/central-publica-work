import TGLExt.F1Fecho394.PhysicalLocalizedSubspacesR3
import TGLExt.F1Fecho394.MaxwellLocalizedInclusionR2

/-! The two future null directions whose opposite semirays preserve the right
wedge. These are geometric support facts, not a locality or density assumption. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open F1Fecho.MaxwellGlobal TGLExt.ImportedSQ TGLExt.ContratoQGv31
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

def nullPlus : Fin 4→ℝ := ![1,1,0,0]
def nullMinus : Fin 4→ℝ := ![1,-1,0,0]
def nullShift (a:Fin 4→ℝ) (t:ℝ) : Spacetime := WithLp.toLp 2 (t • a)

theorem nullPlus_future : nullPlus∈forwardCone := by
  change 0 ≤ (1:ℝ) ∧ 0 ≤ (1:ℝ)^2 - 1^2 - 0^2 - 0^2
  norm_num
theorem nullMinus_future : nullMinus∈forwardCone := by
  change 0 ≤ (1:ℝ) ∧ 0 ≤ (1:ℝ)^2 - (-1)^2 - 0^2 - 0^2
  norm_num

theorem nullPlus_energy_bound (y:MomentumCoordinates) :
    orbitPairing nullPlus (shellMomentum 0 y)≤2*shellEnergy y := by
  have he:orbitPairing nullPlus (shellMomentum 0 y)=shellEnergy y-y.2 := by
    simp [orbitPairing,nullPlus,shellMomentum,shellEnergy]
  rw [he]
  linarith [(abs_le.mp (abs_spatial_le_energy y).2.2).1]

theorem nullMinus_energy_bound (y:MomentumCoordinates) :
    orbitPairing nullMinus (shellMomentum 0 y)≤2*shellEnergy y := by
  have he:orbitPairing nullMinus (shellMomentum 0 y)=shellEnergy y+y.2 := by
    simp [orbitPairing,nullMinus,shellMomentum,shellEnergy]
  rw [he]
  linarith [(abs_le.mp (abs_spatial_le_energy y).2.2).2]

theorem nullPlus_wedge (t:ℝ) (ht:0≤t) :
    translateRegion (nullShift nullPlus t) physicalRightWedge⊆physicalRightWedge := by
  intro x hx
  have hx':|x 0-t|<x 1-t := by
    simpa [translateRegion,physicalRightWedge,nullShift,nullPlus] using hx
  change |x 0|<x 1
  rcases abs_lt.mp hx' with ⟨h1,h2⟩
  exact abs_lt.mpr ⟨by linarith,by linarith⟩

theorem nullMinus_wedge (t:ℝ) (ht:t≤0) :
    translateRegion (nullShift nullMinus t) physicalRightWedge⊆physicalRightWedge := by
  intro x hx
  have hx':|x 0-t|<x 1-(-t) := by
    simpa [translateRegion,physicalRightWedge,nullShift,nullMinus] using hx
  change |x 0|<x 1
  rcases abs_lt.mp hx' with ⟨h1,h2⟩
  exact abs_lt.mpr ⟨by linarith,by linarith⟩

theorem nullPlus_generator (t:ℝ) (ht:0≤t) (ψ:H1)
    (hψ:ψ∈supportedGenerators physicalRightWedge) :
    U1 (t • nullPlus) ψ∈supportedGenerators physicalRightWedge := by
  obtain ⟨f,hr,hs,hf⟩:=translated_generator (nullShift nullPlus t) _ ψ hψ
  exact ⟨f,hr,hs.trans (nullPlus_wedge t ht),hf⟩

theorem nullMinus_generator (t:ℝ) (ht:t≤0) (ψ:H1)
    (hψ:ψ∈supportedGenerators physicalRightWedge) :
    U1 (t • nullMinus) ψ∈supportedGenerators physicalRightWedge := by
  obtain ⟨f,hr,hs,hf⟩:=translated_generator (nullShift nullMinus t) _ ψ hψ
  exact ⟨f,hr,hs.trans (nullMinus_wedge t ht),hf⟩

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.nullPlus_future
#print axioms F1Fecho.MaxwellLocalization.nullMinus_future
#print axioms F1Fecho.MaxwellLocalization.nullPlus_energy_bound
#print axioms F1Fecho.MaxwellLocalization.nullMinus_energy_bound
#print axioms F1Fecho.MaxwellLocalization.nullPlus_generator
#print axioms F1Fecho.MaxwellLocalization.nullMinus_generator
