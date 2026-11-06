import TGLExt.F1Fecho394.ScreenHelicityDiagonalR3
import TGLExt.F1Fecho394.LorentzFutureRepresentationR1

/-! The concrete helicity action covers every Lorentz matrix with future time
column. Properness is the explicit determinant-one condition for the diagonal
positive and negative helicity phase formula. No localized net is inferred from this representation. -/
set_option autoImplicit false
noncomputable section
open MeasureTheory Filter
namespace F1Fecho.OrbitalScreen
open TGLExt TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016 F1Fecho.OrbitalSpatial

def futureHelicityUnitary (L : FutureLorentz) : H1 ≃ₗᵢ[ℂ] H1 :=
  helicityUnitary (futureToGenerated L)

theorem futureHelicityUnitary_strongly_continuous (f : H1) :
    Continuous (fun L : FutureLorentz => futureHelicityUnitary L f) :=
  (helicityUnitary_strongly_continuous f).comp futureToGenerated_continuous

theorem futureHelicityUnitary_U1 (L : FutureLorentz) (a : Fin 4 → ℝ) (f : H1) :
    futureHelicityUnitary L (U1 a f)=U1 (L.val.val.mulVec a) (futureHelicityUnitary L f) :=
  helicityUnitary_U1 (futureToGenerated L) a f

theorem futureHelicityUnitary_mul (L M : LorentzGrp)
    (hL : 0<lorentzLinear L timeBasis 0) (hM : 0<lorentzLinear M timeBasis 0)
    (hLM : 0<lorentzLinear (L*M) timeBasis 0) (f : H1) :
    futureHelicityUnitary ⟨L*M,hLM⟩ f=
      futureHelicityUnitary ⟨L,hL⟩ (futureHelicityUnitary ⟨M,hM⟩ f) := by
  exact helicityUnitary_mul (futureToGenerated ⟨L,hL⟩) (futureToGenerated ⟨M,hM⟩) f

theorem futureHelicityUnitary_diagonal_ae (L : FutureLorentz) (hd : L.val.val.det=1) (f : H1) :
    futureHelicityUnitary L f=ᵐ[orbitalMeasure 0] fun p =>
      matrixFiberOperator (phaseMatrix (transportPhase (futureToGenerated L) p))
        (f (shellAction (L.val⁻¹) p)) :=
  helicityUnitary_diagonal_ae (futureToGenerated L) hd f

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.futureHelicityUnitary_strongly_continuous
#print axioms F1Fecho.OrbitalScreen.futureHelicityUnitary_U1
#print axioms F1Fecho.OrbitalScreen.futureHelicityUnitary_mul
#print axioms F1Fecho.OrbitalScreen.futureHelicityUnitary_diagonal_ae
