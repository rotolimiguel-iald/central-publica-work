import TGLExt.F1Fecho394.ScreenChargeConjugationR2

/-! The fixed circular coordinate change carries real-screen conjugation to
the already constructed helicity-swapping conjugation, on the same fiber. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix Complex
namespace F1Fecho.OrbitalScreen
open F1Rede.FiberConjugation

theorem circularFiber_apply (v : Fiber) :
    circularFiber v=matrixFiberOperator circularMatrix v := rfl

theorem circularFiber_conjugation (v : Fiber) :
    fiberJ (circularFiber v)=circularFiber (fiberSwappedJ v) := by
  rw [circularFiber_apply,circularFiber_apply]
  ext i
  fin_cases i <;>
    simp [matrixFiberOperator,Matrix.ofLp_toEuclideanCLM,circularMatrix,
      Matrix.mulVec,dotProduct,Fin.sum_univ_two,fiberJ,fiberSwappedJ_apply,helicitySwap,
      Complex.star_def] <;> ring

theorem circularFiber_symm_conjugation (v : Fiber) :
    circularFiber.symm (fiberJ v)=fiberSwappedJ (circularFiber.symm v) := by
  apply circularFiber.injective
  rw [LinearIsometryEquiv.apply_symm_apply,←circularFiber_conjugation,
    LinearIsometryEquiv.apply_symm_apply]

end F1Fecho.OrbitalScreen
#print axioms F1Fecho.OrbitalScreen.circularFiber_conjugation
#print axioms F1Fecho.OrbitalScreen.circularFiber_symm_conjugation
