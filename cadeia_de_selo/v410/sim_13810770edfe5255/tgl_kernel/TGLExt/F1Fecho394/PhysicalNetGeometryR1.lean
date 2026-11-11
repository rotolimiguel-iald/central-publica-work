import TGLExt.F1Fecho394.PhysicalLocalizedBoostR2

/-! Coordinate adapter of the actual physical real-test net to LightNetData's
region type. Isotony and translation/boost covariance are supplied by terms.
No helicity label, causal locality or right-wedge equality is manufactured. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellLocalization
open TGLExt.ImportedSQ TGLExt.ContratoQGv31 F1Fecho.MaxwellGlobal
open F1Fecho.SpacetimeLorentz

def spacetimeOf (a:Fin 4→ℝ) : Spacetime := WithLp.toLp 2 a
def coordinateRegion (O:Set (Fin 4→ℝ)) : Set Spacetime :=
  {x | (fun i=>x i)∈O}
def physicalNet (O:Set (Fin 4→ℝ)) : Submodule ℝ H1 := localized (coordinateRegion O)

theorem physicalNet_mono (O P:Set (Fin 4→ℝ)) (h:O⊆P) :
    physicalNet O≤physicalNet P := localized_mono (fun _ hx=>h hx)

theorem coordinateRegion_translate (a:Fin 4→ℝ) (O:Set (Fin 4→ℝ)) :
    coordinateRegion (TGL.SpecificAQFT.translate a O)=
      translateRegion (spacetimeOf a) (coordinateRegion O) := by
  ext x
  constructor
  · rintro ⟨y,hy,he⟩
    have hx:(fun i=>(x-spacetimeOf a) i)=y := by
      funext i
      have hh:=congrFun he i
      change y i+a i=x i at hh
      change x i-a i=y i
      linarith
    change (fun i=>(x-spacetimeOf a) i)∈O
    rwa [hx]
  · intro hx
    refine ⟨(fun i=>(x-spacetimeOf a) i),hx,?_⟩
    funext i
    change x i-a i+a i=x i
    ring

theorem coordinateRegion_boost (s:ℝ) (O:Set (Fin 4→ℝ)) :
    coordinateRegion (wedgeBoostMap s '' O)=boostRegion s (coordinateRegion O) := by
  ext x
  constructor
  · rintro ⟨y,hy,he⟩
    refine ⟨spacetimeOf y,hy,?_⟩
    apply PiLp.ext
    intro i
    exact congrFun he i
  · rintro ⟨y,hy,he⟩
    refine ⟨(fun i=>y i),hy,?_⟩
    funext i
    exact congrArg (fun z:Spacetime=>z i) he

theorem physicalNet_translate (a:Fin 4→ℝ) (O:Set (Fin 4→ℝ)) (f:H1) :
    f∈physicalNet O ↔ U1 a f∈physicalNet (TGL.SpecificAQFT.translate a O) := by
  unfold physicalNet
  rw [coordinateRegion_translate]
  exact localized_translate_iff (spacetimeOf a) (coordinateRegion O) f

theorem physicalNet_boost (s:ℝ) (O:Set (Fin 4→ℝ)) (f:H1) :
    f∈physicalNet O ↔ B0 s f∈physicalNet (wedgeBoostMap s '' O) := by
  unfold physicalNet
  rw [coordinateRegion_boost]
  exact localized_boost_iff s (coordinateRegion O) f

theorem physicalNet_rightWedge :
    physicalNet TGL.SpecificAQFT.rightWedge=localized physicalRightWedge := rfl

end F1Fecho.MaxwellLocalization
#print axioms F1Fecho.MaxwellLocalization.physicalNet_mono
#print axioms F1Fecho.MaxwellLocalization.physicalNet_translate
#print axioms F1Fecho.MaxwellLocalization.physicalNet_boost
#print axioms F1Fecho.MaxwellLocalization.physicalNet_rightWedge
