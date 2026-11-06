import TGLExt.F1Fecho394.CanonicalFockWeightDomainR1
import TGLExt.F1Fecho394.RegularRightAverageR3
import TGLExt.V350ShiftCharacterAverage
import TGLExt.F1Fecho394.CanonicalFockWeightInvarianceR4

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace F1Fecho.CanonicalFockRightAverage
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular MeasureTheory Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFiniteWeight F1Fecho.CanonicalFockWeightDomain F1Fecho.CanonicalFockWeightInvariance
open scoped Topology ENNReal
noncomputable section

theorem regularUnitary_vacuum_is_shift  (t : ℝ) :
    regularUnitary t regularFockVacuum = shift t regularFockVacuum :=
  F1Fecho.RegularRightAverage.regularUnitary_vacuum_is_shift fockFlow M regularFockVacuum
    fibre_boost_fixes_regularVacuum t

theorem scalarOrbit_right_regular 
    (A : (core).toStarSubalgebra) (s t : ℝ) :
    dualAmbient s (A.val * regularUnitary t) regularFockVacuum =
      characterPhase s t • shift t (dualAmbient s A.val regularFockVacuum) :=
  F1Fecho.RegularRightAverage.scalarOrbit_right_regular fockFlow M regularFockVacuum
    fibre_boost_fixes_regularVacuum A s t

theorem scalarOrbit_right_average 
    (A : (core).toStarSubalgebra) (s h : ℝ) :
    dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum =
      shiftCharacterAverage s h (dualAmbient s A.val regularFockVacuum) :=
  F1Fecho.RegularRightAverage.scalarOrbit_right_average fockFlow M regularFockVacuum
    fibre_boost_fixes_regularVacuum A s h

theorem scalarOrbit_right_average_norm_le 
    (A : (core).toStarSubalgebra) (s h : ℝ) :
    ‖dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum‖ ≤
      ‖dualAmbient s A.val regularFockVacuum‖ :=
  F1Fecho.RegularRightAverage.scalarOrbit_right_average_norm_le fockFlow M regularFockVacuum
    fibre_boost_fixes_regularVacuum A s h

theorem scalarOrbit_right_average_tendsto 
    (A : (core).toStarSubalgebra) (s : ℝ) :
    Tendsto (fun h : ℝ => dualAmbient s (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) regularFockVacuum)
      (𝓝[≠] 0) (𝓝 (dualAmbient s A.val regularFockVacuum)) :=
  F1Fecho.RegularRightAverage.scalarOrbit_right_average_tendsto fockFlow M regularFockVacuum
    fibre_boost_fixes_regularVacuum A s

theorem scalarWeight_right_average_le 
    (A : (core).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) * (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h))
      regularFockVacuum ≤ dualQuadraticIntegral (star A.val * A.val) regularFockVacuum :=
  F1Fecho.RegularRightAverage.scalarWeight_right_average_le fockFlow M regularFockVacuum
    fibre_boost_fixes_regularVacuum A h

def scalarWeightRightRegularization  (A : scalarWeightLeftIdeal ) (h : ℝ) :
    scalarWeightLeftIdeal :=
  ⟨⟨A.val.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h,
    (core).mul_mem A.val.property (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h)⟩,
    (scalarWeight_right_average_le A.val h).trans_lt A.property⟩

theorem scalarWeightRightRegularization_uniform 
    (A : scalarWeightLeftIdeal ) (h : ℝ) (hh : 0 < h) :
    (scalarWeightRightRegularization A h).val ∈ finiteLeftIdeal :=
  HasFiniteDualSquare.left_mul _ _ (F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow h hh)

end
end F1Fecho.CanonicalFockRightAverage
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockRightAverage).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
