import TGLExt.F1Fecho394.OrbitalGeneratedCovarianceR3
import Mathlib.Analysis.InnerProductSpace.Projection.Reflection
import Mathlib.Analysis.SpecialFunctions.Arsinh
/-! A Lorentz element fixing the time basis vector is a spatial orthogonal
transformation. This is an algebraic decomposition lemma, not helicity. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open Matrix
namespace F1Fecho.OrbitalSpatial
open TGLExt ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

def timeBasis : Fin 4 → ℝ := ![1,0,0,0]

def spatialEmbed : Spatial →ₗ[ℝ] (Fin 4 → ℝ) where
  toFun v := let p:=spatialChart.symm v; ![0,p.2,p.1 0,p.1 1]
  map_add' x y := by ext i; fin_cases i <;> first | rfl | simp
  map_smul' c x := by ext i; fin_cases i <;> first | rfl | simp

def spatialPart : (Fin 4 → ℝ) →ₗ[ℝ] Spatial where
  toFun := spacetimeSpatial
  map_add' x y := by
    have hp : (![(x+y) 2,(x+y) 3],(x+y) 1)=
        (![x 2,x 3],x 1)+(![y 2,y 3],y 1) := by
      apply Prod.ext
      · funext i; fin_cases i <;> rfl
      · rfl
    change spatialChart (![(x+y) 2,(x+y) 3],(x+y) 1)=
      spatialChart (![x 2,x 3],x 1)+spatialChart (![y 2,y 3],y 1)
    rw [hp,spatialChart_add]
  map_smul' c x := by
    have hp : (![(c • x) 2,(c • x) 3],(c • x) 1)=c • (![x 2,x 3],x 1) := by
      apply Prod.ext
      · funext i; fin_cases i <;> rfl
      · rfl
    change spatialChart (![(c • x) 2,(c • x) 3],(c • x) 1)=c • spatialChart (![x 2,x 3],x 1)
    rw [hp,spatialChart_smul]

theorem spatialPart_embed (v : Spatial) : spatialPart (spatialEmbed v)=v := by
  change spatialChart (![(spatialChart.symm v).1 0,(spatialChart.symm v).1 1],
    (spatialChart.symm v).2)=v
  have hv (p : MomentumCoordinates) : (![p.1 0,p.1 1],p.2)=p := by
    apply Prod.ext
    · funext i; fin_cases i <;> first | rfl | simp
    · rfl
  rw [hv,spatialChart.apply_symm_apply]

theorem spatialEmbed_time (v : Spatial) : spatialEmbed v 0=0 := rfl

theorem spatialPart_timeBasis : spatialPart timeBasis=0 := by
  change spatialChart (![0,0],0)=0
  have hz : (![0,0] : Transverse)=0 := by funext i; fin_cases i <;> rfl
  rw [hz]
  rfl

theorem spacetime_decompose (a : Fin 4 → ℝ) :
    a=a 0 • timeBasis+spatialEmbed (spatialPart a) := by
  have hsp : spatialChart.symm (spatialPart a)=(![a 2,a 3],a 1) :=
    spatialChart.symm_apply_apply _
  change a=a 0 • timeBasis+![0,(spatialChart.symm (spatialPart a)).2,
    (spatialChart.symm (spatialPart a)).1 0,(spatialChart.symm (spatialPart a)).1 1]
  rw [hsp]
  ext i
  fin_cases i <;> simp [timeBasis]

def lorentzLinear (L : LorentzGrp) : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ) where
  toFun := L.val.mulVec
  map_add' a b := Matrix.mulVec_add _ _ _
  map_smul' c a := by simp [Matrix.mulVec_smul]

theorem lorentz_fixed_time_coordinate (L : LorentzGrp)
    (hL : lorentzLinear L timeBasis=timeBasis) (a : Fin 4 → ℝ) :
    lorentzLinear L a 0=a 0 := by
  have h := orbitPairing_lorentz L timeBasis a
  change orbitPairing (lorentzLinear L timeBasis) (lorentzLinear L a)=orbitPairing timeBasis a at h
  rw [hL] at h
  simpa [orbitPairing,timeBasis] using h

def spatialRestriction (L : LorentzGrp) : Spatial →ₗ[ℝ] Spatial :=
  spatialPart.comp ((lorentzLinear L).comp spatialEmbed)

theorem spatialRestriction_norm (L : LorentzGrp)
    (hL : lorentzLinear L timeBasis=timeBasis) (v : Spatial) :
    ‖spatialRestriction L v‖=‖v‖ := by
  have h := orbitPairing_lorentz L (spatialEmbed v) (spatialEmbed v)
  change orbitPairing (lorentzLinear L (spatialEmbed v)) (lorentzLinear L (spatialEmbed v))=
    orbitPairing (spatialEmbed v) (spatialEmbed v) at h
  rw [orbitPairing_spatial,orbitPairing_spatial,lorentz_fixed_time_coordinate L hL,
    spatialEmbed_time] at h
  change 0*0-inner ℝ (spatialRestriction L v) (spatialRestriction L v)=
    0*0-inner ℝ (spatialPart (spatialEmbed v)) (spatialPart (spatialEmbed v)) at h
  rw [spatialPart_embed,real_inner_self_eq_norm_sq,real_inner_self_eq_norm_sq] at h
  nlinarith [norm_nonneg (spatialRestriction L v),norm_nonneg v]

def spatialRestrictionIsometry (L : LorentzGrp)
    (hL : lorentzLinear L timeBasis=timeBasis) : Spatial →ₗᵢ[ℝ] Spatial where
  toLinearMap := spatialRestriction L
  norm_map' := spatialRestriction_norm L hL

def spatialRestrictionEquiv (L : LorentzGrp)
    (hL : lorentzLinear L timeBasis=timeBasis) : Spatial≃ₗᵢ[ℝ]Spatial :=
  LinearIsometryEquiv.ofSurjective (spatialRestrictionIsometry L hL)
    (LinearMap.injective_iff_surjective.mp (spatialRestrictionIsometry L hL).injective)

theorem spatialRestriction_all (L : LorentzGrp)
    (hL : lorentzLinear L timeBasis=timeBasis) (a : Fin 4 → ℝ) :
    spatialPart (lorentzLinear L a)=spatialRestriction L (spatialPart a) := by
  have h := congrArg (fun x => spatialPart (lorentzLinear L x)) (spacetime_decompose a)
  simpa only [map_add,map_smul,hL,spatialPart_timeBasis,smul_zero,zero_add,spatialRestriction,LinearMap.comp_apply] using h

theorem lorentz_fixed_time_spatial (L : LorentzGrp)
    (hL : lorentzLinear L timeBasis=timeBasis) :
    L=spatialLorentz (spatialRestrictionEquiv L hL) := by
  apply Subtype.ext
  have h (a : Fin 4 → ℝ) : L.val.mulVec a=
      spatialSpacetime (spatialRestrictionEquiv L hL) a := by
    apply spacetime_ext
    · exact lorentz_fixed_time_coordinate L hL a
    · rw [spacetimeSpatial_rotation]
      change spatialPart (lorentzLinear L a)=spatialRestriction L (spatialPart a)
      exact spatialRestriction_all L hL a
  change L.val=spatialMatrix (spatialRestrictionEquiv L hL)
  ext i j
  have hij := congrFun (h (Pi.single j 1)) i
  rw [←spatialMatrix_mulVec] at hij
  simpa only [Matrix.mulVec_single_one,Matrix.col_apply] using hij

theorem lorentz_fixed_time_mem_generated (L : LorentzGrp)
    (hL : lorentzLinear L timeBasis=timeBasis) : L ∈ generatedLorentz := by
  let q : SpatialOrthogonal := Unitary.linearIsometryEquiv.symm (spatialRestrictionEquiv L hL)
  have hq : orthogonalLorentzHom q=spatialLorentz (spatialRestrictionEquiv L hL) := by
    change spatialLorentz (Unitary.linearIsometryEquiv q)=_
    rw [show Unitary.linearIsometryEquiv q=spatialRestrictionEquiv L hL from
      Unitary.linearIsometryEquiv.apply_symm_apply _]
  rw [lorentz_fixed_time_spatial L hL,←hq]
  exact spatial_mem_generated q

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.spatialRestriction_norm
#print axioms F1Fecho.OrbitalSpatial.lorentz_fixed_time_spatial
#print axioms F1Fecho.OrbitalSpatial.lorentz_fixed_time_mem_generated
