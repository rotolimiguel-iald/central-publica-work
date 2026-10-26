import MaxwellOnShellBivectorR2
import Mathlib.Analysis.InnerProductSpace.PiL2

/-! Cartesian mass-shell geometry: properness and linear energy growth, before
any integrability conclusion. The spatial coordinates are the canonical ones. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open Matrix MeasureTheory
open ChatgptAudit.WignerRapidityMeasure016 ChatgptAudit.WignerOrbit016

def shellEnergy (y : MomentumCoordinates) : ℝ := energy (transverseMass 0 y.1) y.2
abbrev Spacetime := EuclideanSpace ℝ (Fin 4)
def shellEmbedding (y : MomentumCoordinates) : Spacetime := WithLp.toLp 2 (shellMomentum 0 y)

theorem shellEnergy_nonneg (y : MomentumCoordinates) : 0≤ shellEnergy y := Real.sqrt_nonneg _
theorem shellEnergy_sq (y : MomentumCoordinates) :
    shellEnergy y^2=y.1 0^2+y.1 1^2+y.2^2 := by
  rw [shellEnergy,energy,Real.sq_sqrt (by positivity),transverseMass_sq]
  ring

theorem shellEnergy_continuous : Continuous shellEnergy := by
  unfold shellEnergy energy transverseMass
  fun_prop

theorem abs_spatial_le_energy (y : MomentumCoordinates) :
    |y.1 0|≤ shellEnergy y ∧ |y.1 1|≤ shellEnergy y ∧ |y.2|≤ shellEnergy y := by
  have hs := shellEnergy_sq y
  have hn := shellEnergy_nonneg y
  constructor
  · rw [abs_le]; constructor <;> nlinarith [sq_nonneg (y.1 1),sq_nonneg y.2]
  constructor
  · rw [abs_le]; constructor <;> nlinarith [sq_nonneg (y.1 0),sq_nonneg y.2]
  · rw [abs_le]; constructor <;> nlinarith [sq_nonneg (y.1 0),sq_nonneg (y.1 1)]

theorem coordinate_norm_le_energy (y : MomentumCoordinates) : ‖y‖≤ shellEnergy y := by
  rw [Prod.norm_def]
  apply max_le
  · apply (pi_norm_le_iff_of_nonneg (shellEnergy_nonneg y)).mpr
    intro i
    fin_cases i
    · exact (abs_spatial_le_energy y).1
    · exact (abs_spatial_le_energy y).2.1
  · exact (abs_spatial_le_energy y).2.2

theorem energy_le_twice_coordinate_norm (y : MomentumCoordinates) : shellEnergy y≤2*‖y‖ := by
  have h0 : |y.1 0|≤‖y‖ := (norm_le_pi_norm y.1 0).trans (norm_fst_le y)
  have h1 : |y.1 1|≤‖y‖ := (norm_le_pi_norm y.1 1).trans (norm_fst_le y)
  have h2 : |y.2|≤‖y‖ := norm_snd_le y
  have hs := shellEnergy_sq y
  have hn := shellEnergy_nonneg y
  have hh := norm_nonneg y
  nlinarith [sq_abs (y.1 0),sq_abs (y.1 1),sq_abs y.2,
    sq_nonneg (‖y‖-|y.1 0|),sq_nonneg (‖y‖-|y.1 1|),sq_nonneg (‖y‖-|y.2|)]

theorem shellEmbedding_continuous : Continuous shellEmbedding :=
  (PiLp.continuous_toLp 2 (fun _ : Fin 4 => ℝ)).comp (shellMomentum_continuous 0)

theorem energy_le_embedding_norm (y : MomentumCoordinates) : shellEnergy y≤‖shellEmbedding y‖ := by
  have h := PiLp.norm_apply_le (shellEmbedding y) 0
  change |shellEnergy y| ≤ ‖shellEmbedding y‖ at h
  simpa [abs_of_nonneg (shellEnergy_nonneg y)] using h

theorem shellEmbedding_proper_bound (y : MomentumCoordinates) : ‖y‖≤‖shellEmbedding y‖ :=
  (coordinate_norm_le_energy y).trans (energy_le_embedding_norm y)

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.shellEnergy_sq
#print axioms F1Fecho.MaxwellGlobal.coordinate_norm_le_energy
#print axioms F1Fecho.MaxwellGlobal.energy_le_twice_coordinate_norm
#print axioms F1Fecho.MaxwellGlobal.shellEmbedding_proper_bound
