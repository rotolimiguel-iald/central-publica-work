import Lean
import TGLExt.O16.OrbitalMeasureSupport_v2
import TGLExt.O16.PositiveEnergyIntegral_v4

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Set
namespace ChatgptAudit.WignerRapidityMeasure016
open ChatgptAudit.WignerOrbit016 ChatgptAudit.PositiveEnergy016

/-- Future-cone positivity in the already fixed (+---) convention. -/
theorem future_pairing_nonnegative (a p : Fin 4 → ℝ)
    (ha0 : 0 ≤ a 0) (hp0 : 0 ≤ p 0)
    (ha : a 1^2+a 2^2+a 3^2 ≤ a 0^2)
    (hp : p 1^2+p 2^2+p 3^2 ≤ p 0^2) : 0 ≤ orbitPairing a p := by
  have hcs : (a 1*p 1+a 2*p 2+a 3*p 3)^2 ≤
      (a 1^2+a 2^2+a 3^2)*(p 1^2+p 2^2+p 3^2) := by
    nlinarith [sq_nonneg (a 1*p 2-a 2*p 1), sq_nonneg (a 1*p 3-a 3*p 1),
      sq_nonneg (a 2*p 3-a 3*p 2)]
  have hprod : (a 1^2+a 2^2+a 3^2)*(p 1^2+p 2^2+p 3^2) ≤
      (a 0)^2*(p 0)^2 := mul_le_mul ha hp (by positivity) (sq_nonneg _)
  have hn := mul_nonneg ha0 hp0
  unfold orbitPairing
  nlinarith

theorem shellMomentum_future (m : ℝ) (y : MomentumCoordinates) :
    0 ≤ shellMomentum m y 0 ∧
    (shellMomentum m y 1)^2+(shellMomentum m y 2)^2+(shellMomentum m y 3)^2 ≤
      (shellMomentum m y 0)^2 := by
  constructor
  · exact Real.sqrt_nonneg _
  · change y.2^2+(y.1 0)^2+(y.1 1)^2 ≤ (energy (transverseMass m y.1) y.2)^2
    rw [energy, Real.sq_sqrt (by positivity), transverseMass_sq]
    nlinarith [sq_nonneg m]

theorem orbitalEnergy_nonnegative (m : ℝ) (a : Fin 4 → ℝ)
    (ha0 : 0 ≤ a 0) (ha : a 1^2+a 2^2+a 3^2 ≤ a 0^2)
    (y : MomentumCoordinates) : 0 ≤ orbitPairing a (shellMomentum m y) :=
  future_pairing_nonnegative a (shellMomentum m y) ha0 (shellMomentum_future m y).1
    ha (shellMomentum_future m y).2

theorem orbitalEnergy_measurable (m : ℝ) (a : Fin 4 → ℝ) :
    Measurable (fun y => orbitPairing a (shellMomentum m y)) := by
  unfold orbitPairing shellMomentum energy transverseMass
  fun_prop

/-- The finite measure is explicit input here; the following module will
specialize it to the density of a genuine L² state. -/
theorem orbitalSpectralIntegral_holomorphic (m : ℝ) (a : Fin 4 → ℝ)
    (ha0 : 0 ≤ a 0) (ha : a 1^2+a 2^2+a 3^2 ≤ a 0^2)
    (ν : Measure MomentumCoordinates) [IsFiniteMeasure ν] :
    DifferentiableOn ℂ (spectralIntegral ν (fun y => orbitPairing a (shellMomentum m y)))
      {z : ℂ | 0 < z.im} :=
  spectralIntegral_holomorphic ν _ (orbitalEnergy_measurable m a)
    (orbitalEnergy_nonnegative m a ha0 ha)

theorem orbitalSpectralIntegral_bound (m : ℝ) (a : Fin 4 → ℝ)
    (ha0 : 0 ≤ a 0) (ha : a 1^2+a 2^2+a 3^2 ≤ a 0^2)
    (ν : Measure MomentumCoordinates) [IsFiniteMeasure ν] (z : ℂ) (hz : 0 ≤ z.im) :
    ‖spectralIntegral ν (fun y => orbitPairing a (shellMomentum m y)) z‖ ≤ ν.real univ :=
  spectralIntegral_bound ν _ (orbitalEnergy_nonnegative m a ha0 ha) z hz

#print axioms future_pairing_nonnegative
#print axioms shellMomentum_future
#print axioms orbitalEnergy_nonnegative
#print axioms orbitalEnergy_measurable
#print axioms orbitalSpectralIntegral_holomorphic
#print axioms orbitalSpectralIntegral_bound
end ChatgptAudit.WignerRapidityMeasure016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
