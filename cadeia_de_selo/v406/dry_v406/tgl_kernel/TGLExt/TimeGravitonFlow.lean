import TGLExt.TimeGravitonScalar
import TGLExt.TimeGravitonMatrix

/-!
# Continuous time and the graviton reading in the specified M2 model

The two off-diagonal modes carry conjugate phases. The reading Eg is the
two-block pinching, never the corner PXP. This is a constructed flow for the
specified finite generator, not an inference of a unique interpolation from
discrete samples. Time is recovered from a nonzero decaying mode or an explicit
lift of its phase. A constant reading does not count elapsed time. Parameters
and calibration to seconds have their own physical contracts.

For positive rate the limit is Eg X. The fixed space contains both projectors;
no unique pure attractor or finite-time arrival is asserted. Negative times
occur in the algebraic group formula but are not claimed physical channels.
-/
set_option autoImplicit false
set_option maxHeartbeats 1600000
open Matrix Complex Filter Topology
namespace TGLExt.TimeGravitonFlow
open TimeGravitonMatrix RuleTruthContract
noncomputable section

@[simp] theorem Eg_blockPM (X : M2) : Eg (blockPM X) = 0 := by matrix_calc
@[simp] theorem Eg_blockMP (X : M2) : Eg (blockMP X) = 0 := by matrix_calc
@[simp] theorem blockPM_Eg (X : M2) : blockPM (Eg X) = 0 := by matrix_calc
@[simp] theorem blockMP_Eg (X : M2) : blockMP (Eg X) = 0 := by matrix_calc
@[simp] theorem blockPM_idem (X : M2) : blockPM (blockPM X) = blockPM X := by matrix_calc
@[simp] theorem blockMP_idem (X : M2) : blockMP (blockMP X) = blockMP X := by matrix_calc
@[simp] theorem blockPM_blockMP (X : M2) : blockPM (blockMP X) = 0 := by matrix_calc
@[simp] theorem blockMP_blockPM (X : M2) : blockMP (blockPM X) = 0 := by matrix_calc

def flow (rate omega time : ℝ) : M2 →ₗ[ℂ] M2 :=
  Eg + mode rate (2*omega) time • blockPM + mode rate (-2*omega) time • blockMP

theorem flow_apply (rate omega time : ℝ) (X : M2) :
    flow rate omega time X = Eg X + mode rate (2*omega) time • blockPM X +
      mode rate (-2*omega) time • blockMP X := rfl

@[simp] theorem reading_flow (rate omega time : ℝ) (X : M2) :
    Eg (flow rate omega time X) = Eg X := by
  simp [flow_apply, Eg_idem]

@[simp] theorem blockPM_flow (rate omega time : ℝ) (X : M2) :
    blockPM (flow rate omega time X) = mode rate (2*omega) time • blockPM X := by
  simp [flow_apply]

@[simp] theorem blockMP_flow (rate omega time : ℝ) (X : M2) :
    blockMP (flow rate omega time X) = mode rate (-2*omega) time • blockMP X := by
  simp [flow_apply]

theorem flow_zero (rate omega : ℝ) (X : M2) : flow rate omega 0 X = X := by
  simpa [flow_apply, mode_zero] using four_blocks X

theorem flow_add (rate omega s t : ℝ) (X : M2) :
    flow rate omega (s+t) X = flow rate omega s (flow rate omega t X) := by
  rw [flow_apply, flow_apply, reading_flow, blockPM_flow, blockMP_flow]
  simp only [mode_add, smul_smul]

theorem flow_reading (rate omega time : ℝ) (X : M2) :
    flow rate omega time (Eg X) = Eg X := by
  simp [flow_apply, Eg_idem]

theorem flow_continuous (rate omega : ℝ) (X : M2) :
    Continuous (fun time : ℝ => flow rate omega time X) := by
  simp only [flow_apply]
  exact (continuous_const.add ((mode_continuous rate (2*omega)).smul continuous_const)).add
    ((mode_continuous rate (-2*omega)).smul continuous_const)

def generator (rate omega : ℝ) (X : M2) : M2 :=
  exponent rate (2*omega) • blockPM X + exponent rate (-2*omega) • blockMP X

theorem flow_hasDerivAt (rate omega time : ℝ) (X : M2) :
    HasDerivAt (fun s : ℝ => flow rate omega s X)
      (generator rate omega (flow rate omega time X)) time := by
  rw [generator, blockPM_flow, blockMP_flow]
  apply hasDerivAt_pi.mpr
  intro i
  apply hasDerivAt_pi.mpr
  intro j
  have h := ((hasDerivAt_const time (Eg X i j)).add
    ((mode_hasDerivAt rate (2*omega) time).mul_const (blockPM X i j))).add
    ((mode_hasDerivAt rate (-2*omega) time).mul_const (blockMP X i j))
  simpa only [flow_apply, Matrix.add_apply, Matrix.smul_apply, Pi.add_def, smul_eq_mul,
    zero_add, mul_assoc] using h

theorem generator_at_zero (rate omega : ℝ) (X : M2) :
    HasDerivAt (fun s : ℝ => flow rate omega s X) (generator rate omega X) 0 := by
  simpa only [flow_zero] using flow_hasDerivAt rate omega 0 X

theorem hamiltonian_commutator_blocks (V0 : ℝ) (X : M2) :
    Hg V0 * X - X * Hg V0 =
      (-2*(V0 : ℂ)) • blockPM X + (2*(V0 : ℂ)) • blockMP X := by
  matrix_calc

theorem generator_is_Hg_commutator (rate V0 hbar : ℝ) (X : M2) :
    generator rate (V0/hbar) X =
      (-Complex.I/(hbar : ℂ)) • (Hg V0 * X - X * Hg V0) +
      (rate : ℂ) • (Eg X-X) := by
  rw [hamiltonian_commutator_blocks]
  have he : Eg X-X = -blockPM X - blockMP X := by
    calc
      Eg X-X = Eg X-(Eg X+blockPM X+blockMP X) := by rw [four_blocks]
      _ = -blockPM X-blockMP X := by abel
  rw [he]
  unfold generator exponent
  push_cast
  module

theorem generator_is_GKLS (rate V0 hbar : ℝ) (hr : 0 ≤ rate) (X : M2) :
    generator rate (V0/hbar) X =
      (-Complex.I/(hbar : ℂ)) • (Hg V0 * X - X * Hg V0) +
      singleJump (Real.sqrt (2*rate)) X := by
  rw [generator_is_Hg_commutator, singleJump_rate]
  have hs : (Real.sqrt (2*rate))^2 = 2*rate := Real.sq_sqrt (by positivity)
  have hc : (Real.sqrt (2*rate) : ℂ)^2 = 2*(rate : ℂ) := by exact_mod_cast hs
  rw [hc]
  congr 2
  ring

theorem physical_flow_hasDerivAt (rate V0 hbar time : ℝ) (hr : 0 ≤ rate) (X : M2) :
    HasDerivAt (fun s : ℝ => flow rate (V0/hbar) s X)
      ((-Complex.I/(hbar : ℂ)) •
        (Hg V0 * flow rate (V0/hbar) time X - flow rate (V0/hbar) time X * Hg V0) +
       singleJump (Real.sqrt (2*rate)) (flow rate (V0/hbar) time X)) time := by
  rw [← generator_is_GKLS rate V0 hbar hr]
  exact flow_hasDerivAt rate (V0/hbar) time X

theorem flow_tendsto_reading (rate omega : ℝ) (hr : 0 < rate) (X : M2) :
    Tendsto (fun time : ℝ => flow rate omega time X) atTop (nhds (Eg X)) := by
  have h := ((tendsto_const_nhds (x:=Eg X)).add
    ((mode_tendsto_zero rate (2*omega) hr).smul (tendsto_const_nhds (x:=blockPM X)))).add
    ((mode_tendsto_zero rate (-2*omega) hr).smul (tendsto_const_nhds (x:=blockMP X)))
  simpa only [zero_smul, add_zero, flow_apply] using h

theorem flow_fixed_iff_reading (rate omega : ℝ) (hr : 0 < rate) (X : M2) :
    (∀ time : ℝ, flow rate omega time X = X) ↔ Eg X = X := by
  constructor
  · intro h
    exact tendsto_nhds_unique (flow_tendsto_reading rate omega hr X)
      (by simpa only [h] using (tendsto_const_nhds (x:=X) (f:=atTop)))
  · intro h time
    rw [← h, flow_reading]

theorem rootPlus_mode (rate omega time : ℝ) :
    flow rate omega time rootPlus = mode rate (2*omega) time • rootPlus := by
  simp [flow_apply, Eg_rootPlus, blockPM_rootPlus, blockMP_rootPlus]

theorem rootMinus_mode (rate omega time : ℝ) :
    flow rate omega time rootMinus = mode rate (-2*omega) time • rootMinus := by
  simp [flow_apply, Eg_rootMinus, blockPM_rootMinus, blockMP_rootMinus]

theorem rootPlus_entry (rate omega time : ℝ) :
    flow rate omega time rootPlus 0 0 = mode rate (2*omega) time := by
  rw [rootPlus_mode]
  simp [rootPlus, hPlusC, hCrossC]

theorem rootPlus_observed_clock (rate omega time : ℝ) (hr : rate ≠ 0) :
    -Real.log ‖flow rate omega time rootPlus 0 0‖ / rate = time := by
  rw [rootPlus_entry]
  exact module_clock rate (2*omega) time hr

theorem rootPlus_not_zero_at_finite_time (rate omega time : ℝ) :
    flow rate omega time rootPlus ≠ 0 := by
  intro h
  have h00 := congrFun (congrFun h 0) 0
  rw [rootPlus_entry] at h00
  exact mode_ne_zero rate (2*omega) time h00

def coherence (X : M2) : ℂ := blockPM X 0 0

theorem coherence_flow (rate omega time : ℝ) (X : M2) :
    coherence (flow rate omega time X) = mode rate (2*omega) time * coherence X := by
  unfold coherence
  rw [blockPM_flow]
  rfl

theorem coherence_ratio (rate omega time : ℝ) (X : M2) (hx : coherence X ≠ 0) :
    coherence (flow rate omega time X) / coherence X = mode rate (2*omega) time := by
  rw [coherence_flow]
  exact mul_div_cancel_right₀ _ hx

theorem coherence_clock (rate omega time : ℝ) (hr : rate ≠ 0) (X : M2)
    (hx : coherence X ≠ 0) :
    -Real.log ‖coherence (flow rate omega time X) / coherence X‖ / rate = time := by
  rw [coherence_ratio rate omega time X hx]
  exact module_clock rate (2*omega) time hr

theorem transported_coherence : coherence transportedRho = Complex.I/4 := by
  have h : blockPM transportedRho = (Complex.I/4) • rootPlus := by
    rw [density_transport]
    matrix_calc
  unfold coherence
  rw [h]
  simp [rootPlus, hPlusC, hCrossC]

theorem transported_clock (rate omega time : ℝ) (hr : rate ≠ 0) :
    -Real.log ‖coherence (flow rate omega time transportedRho) /
      coherence transportedRho‖ / rate = time := by
  apply coherence_clock rate omega time hr
  rw [transported_coherence]
  exact div_ne_zero Complex.I_ne_zero (by norm_num)

theorem fixed_projectors (rate omega time : ℝ) :
    flow rate omega time projPlus = projPlus ∧ flow rate omega time projMinus = projMinus := by
  constructor
  · rw [← Eg_projPlus, flow_reading]
  · rw [← Eg_projMinus, flow_reading]

theorem transported_limit (rate omega : ℝ) (hr : 0 < rate) :
    Tendsto (fun t : ℝ => flow rate omega t transportedRho) atTop
      (nhds ((1/2 : ℂ) • (1:M2))) := by
  simpa only [transported_reading] using flow_tendsto_reading rate omega hr transportedRho

theorem rule_preserved (target X : M2) (rate omega time : ℝ) :
    Admissible Eg target (flow rate omega time X) ↔ Admissible Eg target X := by
  unfold Admissible
  rw [reading_flow]

theorem inscription_stationary (X : M2) (rate omega time : ℝ) :
    RuleContinuousMotor.inscribe Eg Eg_idem (flow rate omega time X) =
      RuleContinuousMotor.inscribe Eg Eg_idem X := by
  apply Subtype.ext
  exact reading_flow rate omega time X

theorem rule_is_equality_on_inscriptions
    (target X : RuleContinuousMotor.Inscription Eg) :
    Admissible (fun z : RuleContinuousMotor.Inscription Eg => Eg z.val) target.val X ↔ X=target :=
  RuleContinuousMotor.rule_on_inscriptions_is_equality Eg target X

theorem wrong_reading_rejected (target X : M2) (rate omega time : ℝ)
    (h : Eg X ≠ target) : ¬ Admissible Eg target (flow rate omega time X) := by
  simpa only [Admissible, reading_flow] using h

end
end TGLExt.TimeGravitonFlow
#print axioms TGLExt.TimeGravitonFlow.Eg_blockPM
#print axioms TGLExt.TimeGravitonFlow.Eg_blockMP
#print axioms TGLExt.TimeGravitonFlow.blockPM_Eg
#print axioms TGLExt.TimeGravitonFlow.blockMP_Eg
#print axioms TGLExt.TimeGravitonFlow.blockPM_idem
#print axioms TGLExt.TimeGravitonFlow.blockMP_idem
#print axioms TGLExt.TimeGravitonFlow.blockPM_blockMP
#print axioms TGLExt.TimeGravitonFlow.blockMP_blockPM
#print axioms TGLExt.TimeGravitonFlow.flow_apply
#print axioms TGLExt.TimeGravitonFlow.reading_flow
#print axioms TGLExt.TimeGravitonFlow.blockPM_flow
#print axioms TGLExt.TimeGravitonFlow.blockMP_flow
#print axioms TGLExt.TimeGravitonFlow.flow_zero
#print axioms TGLExt.TimeGravitonFlow.flow_add
#print axioms TGLExt.TimeGravitonFlow.flow_reading
#print axioms TGLExt.TimeGravitonFlow.flow_continuous
#print axioms TGLExt.TimeGravitonFlow.flow_hasDerivAt
#print axioms TGLExt.TimeGravitonFlow.generator_at_zero
#print axioms TGLExt.TimeGravitonFlow.hamiltonian_commutator_blocks
#print axioms TGLExt.TimeGravitonFlow.generator_is_Hg_commutator
#print axioms TGLExt.TimeGravitonFlow.generator_is_GKLS
#print axioms TGLExt.TimeGravitonFlow.physical_flow_hasDerivAt
#print axioms TGLExt.TimeGravitonFlow.flow_tendsto_reading
#print axioms TGLExt.TimeGravitonFlow.flow_fixed_iff_reading
#print axioms TGLExt.TimeGravitonFlow.rootPlus_mode
#print axioms TGLExt.TimeGravitonFlow.rootMinus_mode
#print axioms TGLExt.TimeGravitonFlow.rootPlus_entry
#print axioms TGLExt.TimeGravitonFlow.rootPlus_observed_clock
#print axioms TGLExt.TimeGravitonFlow.rootPlus_not_zero_at_finite_time
#print axioms TGLExt.TimeGravitonFlow.coherence_flow
#print axioms TGLExt.TimeGravitonFlow.coherence_ratio
#print axioms TGLExt.TimeGravitonFlow.coherence_clock
#print axioms TGLExt.TimeGravitonFlow.transported_coherence
#print axioms TGLExt.TimeGravitonFlow.transported_clock
#print axioms TGLExt.TimeGravitonFlow.fixed_projectors
#print axioms TGLExt.TimeGravitonFlow.transported_limit
#print axioms TGLExt.TimeGravitonFlow.rule_preserved
#print axioms TGLExt.TimeGravitonFlow.inscription_stationary
#print axioms TGLExt.TimeGravitonFlow.rule_is_equality_on_inscriptions
#print axioms TGLExt.TimeGravitonFlow.wrong_reading_rejected
