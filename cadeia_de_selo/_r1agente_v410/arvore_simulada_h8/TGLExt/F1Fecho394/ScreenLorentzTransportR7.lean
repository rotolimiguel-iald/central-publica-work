import TGLExt.F1Fecho394.ScreenCocycleMatrixR4
import TGLExt.F1Fecho394.LorentzFutureRepresentationR1

/-! The existing transverse cocycle evaluated at the actual Lorentz
mass-shell transport. Null chart axes are excluded only almost everywhere. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Matrix
namespace F1Fecho.OrbitalScreen
open TGLExt ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016
open F1Fecho.OrbitalSpatial

instance screenMatrixMeasurable : MeasurableSpace (Matrix (Fin 2) (Fin 2) ℂ) := by
  unfold Matrix
  infer_instance

instance screenMatrixBorel : BorelSpace (Matrix (Fin 2) (Fin 2) ℂ) := by
  change @BorelSpace (Fin 2 → Fin 2 → ℂ) Pi.topologicalSpace MeasurableSpace.pi
  infer_instance

theorem regular_orbital_ae : ∀ᵐ p ∂orbitalMeasure 0, p.1 ≠ (0 : Transverse) := by
  rw [ae_iff]
  have hs : {p : MomentumCoordinates | ¬p.1 ≠ (0 : Transverse)}=
      ({0} : Set Transverse) ×ˢ (Set.univ : Set ℝ) := by ext p; simp
  rw [hs]
  exact exceptional_axis_orbital_null 0

theorem screen_measurable (i : Fin 2) : Measurable (fun x => screen x i) := by
  apply measurable_pi_lambda
  intro j
  fin_cases i <;> fin_cases j
  all_goals
    dsimp [screen,screenOne,screenTwo,transverseMass]
    fun_prop

theorem coefficientMatrix_measurable (g : Vec4 →ₗ[ℝ] Vec4) :
    Measurable (fun p : MomentumCoordinates × MomentumCoordinates => coefficientMatrix g p.1 p.2) := by
  apply measurable_pi_lambda
  intro i
  apply measurable_pi_lambda
  intro j
  have hg : Continuous g := g.continuous_of_finiteDimensional
  have h1 : Measurable (fun p : MomentumCoordinates × MomentumCoordinates => screen p.2 i) := (screen_measurable i).comp measurable_snd
  have h2 : Measurable (fun p : MomentumCoordinates × MomentumCoordinates => g (screen p.1 j)) := hg.measurable.comp ((screen_measurable j).comp measurable_fst)
  have ha (k : Fin 4) : Measurable (fun p : MomentumCoordinates × MomentumCoordinates => screen p.2 i k) :=
    (measurable_pi_apply k).comp h1
  have hb (k : Fin 4) : Measurable (fun p : MomentumCoordinates × MomentumCoordinates => g (screen p.1 j) k) :=
    (measurable_pi_apply k).comp h2
  exact Complex.continuous_ofReal.measurable.comp
    (((((ha 0).mul (hb 0)).sub ((ha 1).mul (hb 1))).sub
      ((ha 2).mul (hb 2))).sub ((ha 3).mul (hb 3))).neg

def transportMatrix (L : generatedLorentz) (p : MomentumCoordinates) : Matrix (Fin 2) (Fin 2) ℂ :=
  coefficientMatrix (lorentzLinear L.val)
    (inverseRapidityChart 0 (shellAction (L⁻¹).val p)) (inverseRapidityChart 0 p)

theorem transportMatrix_measurable (L : generatedLorentz) : Measurable (transportMatrix L) := by
  have ha : Measurable (fun p : MomentumCoordinates => inverseRapidityChart 0 (shellAction (L⁻¹).val p)) :=
    (inverseRapidityChart_measurable 0).comp (shellAction_continuous _).measurable
  have hb : Measurable (fun p : MomentumCoordinates => inverseRapidityChart 0 p) := inverseRapidityChart_measurable 0
  change Measurable (fun p => coefficientMatrix (lorentzLinear L.val)
    (inverseRapidityChart 0 (shellAction (L⁻¹).val p)) (inverseRapidityChart 0 p))
  convert (coefficientMatrix_measurable (lorentzLinear L.val)).comp (ha.prodMk hb) using 1
  rfl

theorem inverse_shell_transport_ae (L : generatedLorentz) :
    ∀ᵐ p ∂orbitalMeasure 0,
      lorentzLinear L.val (shellMomentum 0 (shellAction (L⁻¹).val p))=shellMomentum 0 p := by
  filter_upwards [(shellAction_lift L⁻¹).2] with p hp
  change L.val.val.mulVec (shellMomentum 0 (shellAction (L⁻¹).val p))=shellMomentum 0 p
  rw [hp]
  exact lorentz_mul_inverse_apply L.val _

theorem transportMatrix_unitary_ae (L : generatedLorentz) :
    ∀ᵐ p ∂orbitalMeasure 0, transportMatrix L p ∈ Matrix.unitaryGroup (Fin 2) ℂ := by
  have hr := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae regular_orbital_ae
  have hc := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (chart_inverse_ae 0)
  filter_upwards [regular_orbital_ae,hr,chart_inverse_ae 0,hc,inverse_shell_transport_ae L]
    with p hp hq hpc hqc ht
  apply coefficientMatrix_unitary
  · exact hq
  · exact hp
  · rw [hqc,hpc]
    exact ht
  · exact orbitPairing_lorentz L.val

theorem lorentzLinear_one : lorentzLinear (1 : LorentzGrp)=LinearMap.id := by
  apply LinearMap.ext
  intro a
  change (1 : Matrix (Fin 4) (Fin 4) ℝ).mulVec a=a
  simp

theorem lorentzLinear_mul (L M : LorentzGrp) :
    lorentzLinear (L*M)=(lorentzLinear L).comp (lorentzLinear M) := by
  apply LinearMap.ext
  intro a
  change (L.val*M.val).mulVec a=L.val.mulVec (M.val.mulVec a)
  exact (Matrix.mulVec_mulVec a L.val M.val).symm

theorem transportMatrix_one_ae : transportMatrix 1=ᵐ[orbitalMeasure 0] fun _ => 1 := by
  filter_upwards [shellAction_one_ae,regular_orbital_ae] with p hp hr
  unfold transportMatrix
  simp only [inv_one,OneMemClass.coe_one,hp,id_eq,lorentzLinear_one]
  exact coefficientMatrix_id _ hr

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.transportMatrix_measurable
#print axioms F1Fecho.OrbitalScreen.transportMatrix_unitary_ae
#print axioms F1Fecho.OrbitalScreen.transportMatrix_one_ae
