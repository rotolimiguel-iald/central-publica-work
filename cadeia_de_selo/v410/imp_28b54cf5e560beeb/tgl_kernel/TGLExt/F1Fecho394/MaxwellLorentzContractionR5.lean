import TGLExt.F1Fecho394.MaxwellBoostContractionR1

/-! General Lorentz transport of the physical Maxwell contraction. The real
screen cocycle is used with its actual inverse-transpose relation; no scalar
replacement of the photon representation is made. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix MeasureTheory
namespace F1Fecho.MaxwellLorentzContraction
open TGLExt F1Fecho.MaxwellGlobal F1Fecho.MaxwellOnShell
open F1Fecho.OrbitalSpatial F1Fecho.OrbitalScreen F1Fecho.CovariantTensor
open F1Fecho.MaxwellBoostContraction
open ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

theorem inverse_screen_coefficient (L:LorentzGrp) (x y:MomentumCoordinates) (i j:Fin 2) :
    screenCoefficient (lorentzLinear L⁻¹) y x i j=
      screenCoefficient (lorentzLinear L) x y j i := by
  unfold screenCoefficient
  congr 1
  have h:=orbitPairing_lorentz L (screen x i) (lorentzLinear L⁻¹ (screen y j))
  have hi:lorentzLinear L (lorentzLinear L⁻¹ (screen y j))=screen y j :=
    lorentz_mul_inverse_apply L _
  change orbitPairing (lorentzLinear L (screen x i))
    (lorentzLinear L (lorentzLinear L⁻¹ (screen y j)))=_ at h
  rw [hi] at h
  rw [←h,orbitPairing_symm]

theorem contraction_lorentz (L:LorentzGrp) (p q:MomentumCoordinates)
    (hp:p.1≠0) (hq:q.1≠0)
    (hm:lorentzLinear L⁻¹ (shellMomentum 0 p)=shellMomentum 0 q)
    (j:Fin 2) (T:TensorValue) :
    (∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*pull (L⁻¹.val.map Complex.ofReal) T μ ν)=
      ∑i:Fin 2,coefficientMatrix (lorentzLinear L)
        (inverseRapidityChart 0 q) (inverseRapidityChart 0 p) j i *
        (∑μ,∑ν,(cartesianStrength q i μ ν:ℂ)*T μ ν) := by
  have hpc:=chart_inverse_of_positive 0 p (transverseMass_pos_of_ne_zero 0 p.1 hp)
  have hqc:=chart_inverse_of_positive 0 q (transverseMass_pos_of_ne_zero 0 q.1 hq)
  have ht (μ ν:Fin 4):=
    real_strength_screen_transport (lorentzLinear L⁻¹)
      (inverseRapidityChart 0 p) (inverseRapidityChart 0 q) hp hq
      (by rw [hpc,hqc];exact hm) (orbitPairing_lorentz L⁻¹) j μ ν
  simp only [hpc,hqc] at ht
  simp_rw [cartesianStrength_inverse_chart p hp,cartesianStrength_inverse_chart q hq]
  rw [←real_contraction_eq_sum,contraction_pull,realLift_mulVec,realLift_mulVec,
    real_contraction_eq_sum]
  change (∑μ,∑ν,(realStrength (lorentzLinear L⁻¹ (shellMomentum 0 p))
      (lorentzLinear L⁻¹ (screen (inverseRapidityChart 0 p) j)) μ ν:ℂ)*T μ ν)=_
  simp_rw [ht,Complex.ofReal_add,Complex.ofReal_mul,inverse_screen_coefficient]
  simp only [Fin.sum_univ_two,coefficientMatrix,add_mul,Finset.sum_add_distrib,
    mul_assoc,←Finset.mul_sum]

theorem contraction_lorentz_ae (L:generatedLorentz) :
    ∀ᵐp ∂orbitalMeasure 0,∀j:Fin 2,∀T:TensorValue,
      (∑μ,∑ν,(cartesianStrength p j μ ν:ℂ)*pull (L⁻¹.val.val.map Complex.ofReal) T μ ν)=
        ∑i:Fin 2,transportMatrix L p j i *
          (∑μ,∑ν,(cartesianStrength (shellAction L⁻¹.val p) i μ ν:ℂ)*T μ ν) := by
  have hq:=(shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae regular_orbital_ae
  filter_upwards [regular_orbital_ae,hq,(shellAction_lift L⁻¹).2] with p hp hq hm
  intro j T
  exact contraction_lorentz L.val p (shellAction L⁻¹.val p) hp hq hm.symm j T

end F1Fecho.MaxwellLorentzContraction
#print axioms F1Fecho.MaxwellLorentzContraction.inverse_screen_coefficient
#print axioms F1Fecho.MaxwellLorentzContraction.contraction_lorentz
#print axioms F1Fecho.MaxwellLorentzContraction.contraction_lorentz_ae
