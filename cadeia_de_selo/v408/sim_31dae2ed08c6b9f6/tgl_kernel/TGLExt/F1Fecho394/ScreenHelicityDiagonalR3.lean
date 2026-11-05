import TGLExt.F1Fecho394.ScreenHelicityRepresentationR3

/-! Diagonal helicity positive and negative helicity action, derived from the real transverse cocycle
and the fixed normalized circular basis. -/
set_option autoImplicit false
set_option maxHeartbeats 2000000
noncomputable section
open Matrix Complex MeasureTheory Filter
namespace F1Fecho.OrbitalScreen
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016 F1Fecho.OrbitalSpatial

def phaseMatrix (z : ℂ) : Matrix (Fin 2) (Fin 2) ℂ := Matrix.diagonal ![z,star z]

theorem circularMatrix_intertwines (B : Matrix (Fin 2) (Fin 2) ℂ) (z : ℂ)
    (hp : B.mulVec (circularCoefficients 1)=z • circularCoefficients 1)
    (hm : B.mulVec (circularCoefficients (-1))=star z • circularCoefficients (-1)) :
    B*circularMatrix=circularMatrix*phaseMatrix z := by
  have hp0 := congrFun hp 0
  have hp1 := congrFun hp 1
  have hm0 := congrFun hm 0
  have hm1 := congrFun hm 1
  simp [Matrix.mulVec,dotProduct,Fin.sum_univ_two,circularCoefficients] at hp0 hp1 hm0 hm1
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply,Fin.sum_univ_two,circularMatrix,phaseMatrix] <;>
    first | linear_combination ((Real.sqrt 2 : ℂ)⁻¹)*hp0
          | linear_combination ((Real.sqrt 2 : ℂ)⁻¹)*hp1
          | linear_combination ((Real.sqrt 2 : ℂ)⁻¹)*hm0
          | linear_combination ((Real.sqrt 2 : ℂ)⁻¹)*hm1

theorem circularFiber_intertwines (B : Matrix (Fin 2) (Fin 2) ℂ) (z : ℂ)
    (hp : B.mulVec (circularCoefficients 1)=z • circularCoefficients 1)
    (hm : B.mulVec (circularCoefficients (-1))=star z • circularCoefficients (-1))
    (v : Fiber) :
    matrixFiberOperator B (circularFiber v)=circularFiber (matrixFiberOperator (phaseMatrix z) v) := by
  change matrixFiberOperator B (matrixFiberOperator circularMatrix v)=
    matrixFiberOperator circularMatrix (matrixFiberOperator (phaseMatrix z) v)
  rw [←matrixFiberOperator_mul, circularMatrix_intertwines B z hp hm,matrixFiberOperator_mul]

theorem helicityUnitary_diagonal_ae (L : generatedLorentz) (hd : L.val.val.det=1) (f : H1) :
    helicityUnitary L f=ᵐ[orbitalMeasure 0] fun p =>
      matrixFiberOperator (phaseMatrix (transportPhase L p)) (f (shellAction (L⁻¹).val p)) := by
  have he : circularH1 (helicityUnitary L f)=transverseUnitary L (circularH1 f) := by
    rw [helicityUnitary_apply,circularH1.apply_symm_apply]
  have hc := (shellAction_lift L⁻¹).1.quasiMeasurePreserving.ae (fiberLiftMap_ae circularFiber f)
  filter_upwards [fiberLiftMap_ae circularFiber (helicityUnitary L f),
    transverseAction_ae L (circularH1 f),hc,transportMatrix_circular_ae L hd]
      with p hp hq hr hphase
  have hev := congrArg (fun v : H1 => v p) he
  change fiberLiftMap circularFiber (helicityUnitary L f) p=transverseAction L (circularH1 f) p at hev
  rw [hp,hq] at hev
  change circularFiber (helicityUnitary L f p)=
    matrixFiberOperator (transportMatrix L p) (fiberLiftMap circularFiber f (shellAction (L⁻¹).val p)) at hev
  rw [hr,circularFiber_intertwines _ _ hphase.1 hphase.2] at hev
  exact circularFiber.injective hev

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.circularMatrix_intertwines
#print axioms F1Fecho.OrbitalScreen.circularFiber_intertwines
#print axioms F1Fecho.OrbitalScreen.helicityUnitary_diagonal_ae
