import TGLExt.F1Fecho394.LorentzTimeStabilizerR4
/-! Every Lorentz transformation with a future time column belongs to the
already represented subgroup. The proof uses an explicit boost and a spatial
reflection, followed by the proved time stabilizer. The action stays scalar. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix
namespace F1Fecho.OrbitalSpatial
open TGLExt ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

def longitudinalUnit : Spatial := spatialChart (0,1)

theorem longitudinalUnit_norm : ‖longitudinalUnit‖=1 := by
  have h := spatialChart_norm_sq ((0 : Transverse),1)
  change ‖longitudinalUnit‖^2=0^2+0^2+1^2 at h
  nlinarith [norm_nonneg longitudinalUnit]

theorem lorentz_time_column_norm (L : LorentzGrp) :
    (lorentzLinear L timeBasis 0)^2=1+‖spatialPart (lorentzLinear L timeBasis)‖^2 := by
  have h := orbitPairing_lorentz L timeBasis timeBasis
  rw [orbitPairing_spatial] at h
  change (lorentzLinear L timeBasis 0)*(lorentzLinear L timeBasis 0)-
    inner ℝ (spatialPart (lorentzLinear L timeBasis)) (spatialPart (lorentzLinear L timeBasis))=
    orbitPairing timeBasis timeBasis at h
  rw [real_inner_self_eq_norm_sq] at h
  have hb : orbitPairing timeBasis timeBasis=1 := by
    change (1:ℝ)*1-0*0-0*0-0*0=1
    norm_num
  rw [hb] at h
  nlinarith

theorem boost_time_column (s : ℝ) :
    (theBoost s).val.mulVec timeBasis=![Real.cosh s,Real.sinh s,0,0] := by
  ext i
  fin_cases i <;> simp [theBoost,boostMat,timeBasis,Matrix.mulVec,dotProduct,Fin.sum_univ_four]

theorem spatialPart_boost_time (r : ℝ) :
    spatialPart ((theBoost (Real.arsinh r)).val.mulVec timeBasis)=r • longitudinalUnit := by
  rw [boost_time_column,Real.sinh_arsinh]
  change spatialChart (![0,0],r)=r • spatialChart ((0 : Transverse),1)
  have hz : (![0,0] : Transverse)=0 := by funext i; fin_cases i <;> rfl
  rw [hz,←spatialChart_smul]
  congr 1
  simp

theorem spatialLorentz_mem_generated (Q : Spatial≃ₗᵢ[ℝ]Spatial) :
    spatialLorentz Q ∈ generatedLorentz := by
  let q : SpatialOrthogonal := Unitary.linearIsometryEquiv.symm Q
  have hq : Unitary.linearIsometryEquiv q=Q := Unitary.linearIsometryEquiv.apply_symm_apply Q
  have h := spatial_mem_generated q
  change spatialLorentz (Unitary.linearIsometryEquiv q) ∈ generatedLorentz at h
  rwa [hq] at h

theorem future_lorentz_mem_generated (L : LorentzGrp)
    (hf : 0 < lorentzLinear L timeBasis 0) : L ∈ generatedLorentz := by
  let v := spatialPart (lorentzLinear L timeBasis)
  let r := ‖v‖
  let s := Real.arsinh r
  let w := r • longitudinalUnit
  have hn : ‖w‖=‖v‖ := by
    simp only [w,norm_smul,Real.norm_eq_abs,abs_of_nonneg (norm_nonneg v),longitudinalUnit_norm,mul_one,r]
  let Q : Spatial≃ₗᵢ[ℝ]Spatial := (ℝ ∙ (w-v))ᗮ.reflection
  have hQ : Q w=v := Submodule.reflection_sub hn
  have hc : Real.cosh s=lorentzLinear L timeBasis 0 := by
    rw [Real.cosh_arsinh]
    have ht : 1+r^2=(lorentzLinear L timeBasis 0)^2 := (lorentz_time_column_norm L).symm
    rw [ht,Real.sqrt_sq hf.le]
  let B : LorentzGrp := spatialLorentz Q*theBoost s
  have hB : B ∈ generatedLorentz :=
    generatedLorentz.mul_mem (spatialLorentz_mem_generated Q) (boost_mem_generated s)
  have hcol : B.val.mulVec timeBasis=L.val.mulVec timeBasis := by
    change (spatialMatrix Q*boostMat s).mulVec timeBasis=L.val.mulVec timeBasis
    rw [←Matrix.mulVec_mulVec,spatialMatrix_mulVec]
    apply spacetime_ext
    · change (boostMat s).mulVec timeBasis 0=lorentzLinear L timeBasis 0
      change ((theBoost s).val.mulVec timeBasis) 0=_
      rw [boost_time_column]
      exact hc
    · rw [spacetimeSpatial_rotation]
      change Q (spatialPart ((theBoost (Real.arsinh r)).val.mulVec timeBasis))=v
      rw [spatialPart_boost_time]
      exact hQ
  have hfix : lorentzLinear (B⁻¹*L) timeBasis=timeBasis := by
    change ((B⁻¹).val*L.val).mulVec timeBasis=timeBasis
    rw [←Matrix.mulVec_mulVec,←hcol,Matrix.mulVec_mulVec,←lorentzGrp_mul_val,
      inv_mul_cancel,lorentzGrp_one_val,Matrix.one_mulVec]
  have hrest := lorentz_fixed_time_mem_generated (B⁻¹*L) hfix
  have h := generatedLorentz.mul_mem hB hrest
  simpa only [←mul_assoc,mul_inv_cancel,one_mul] using h

def futureLorentzUnitary (L : LorentzGrp) (hf : 0 < lorentzLinear L timeBasis 0) :=
  generatedUnitary ⟨L,future_lorentz_mem_generated L hf⟩

theorem futureLorentzUnitary_U1 (L : LorentzGrp) (hf : 0 < lorentzLinear L timeBasis 0)
    (a : Fin 4 → ℝ) (f : TGLExt.ImportedSQ.H1) :
    futureLorentzUnitary L hf (TGLExt.ImportedSQ.U1 a f)=
      TGLExt.ImportedSQ.U1 (L.val.mulVec a) (futureLorentzUnitary L hf f) :=
  generatedUnitary_U1 ⟨L,future_lorentz_mem_generated L hf⟩ a f

end F1Fecho.OrbitalSpatial
#print axioms F1Fecho.OrbitalSpatial.lorentz_time_column_norm
#print axioms F1Fecho.OrbitalSpatial.future_lorentz_mem_generated
#print axioms F1Fecho.OrbitalSpatial.futureLorentzUnitary_U1
