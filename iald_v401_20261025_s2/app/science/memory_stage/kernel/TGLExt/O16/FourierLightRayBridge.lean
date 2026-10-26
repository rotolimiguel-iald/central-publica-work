import Lean
import TGLExt.O16.RetaDeLuzBorchersAudited
import TGLExt.V351FourierTranslation
import TGLExt.ContinuousModularReconstruction

/-!
A2.2: explicit Fourier bridge to the existing continuous modular graph.
No physical identification, half-sided isotony, or uniqueness of 2*pi is assumed proved.
-/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
open FormaInscrita.RetaDeLuz TGLV350.Regular
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050

namespace ChatgptAudit.FourierBridge016

abbrev fourierUnitary : L2R ≃ₗᵢ[ℂ] L2R := Lp.fourierTransformₗᵢ ℝ ℂ

theorem dilation_eq_shift (s : ℝ) (f : L2R) : D s f = shift s f := by
  apply Lp.ext
  filter_upwards [D_ae s f, shift_ae s f] with x hd hs
  rw [hd, hs]
  rfl

theorem fourier_dilation (s : ℝ) (f : L2R) :
    fourierUnitary (D s f) = characterMultiplier (2 * Real.pi * s) (fourierUnitary f) := by
  rw [dilation_eq_shift]
  exact fourier_shift s f

def c0 : ℝ := 2 * Real.pi ^ 2

theorem c0_pos : 0 < c0 := by
  unfold c0
  positivity

theorem fourier_bw_candidate (t : ℝ) (f : L2R) :
    fourierUnitary (D (2 * Real.pi * t) f) =
      characterMultiplier (2 * c0 * t) (fourierUnitary f) := by
  rw [fourier_dilation]
  congr 2
  unfold c0
  ring

def deltaSymbol (c x : ℝ) : ℝ := Real.exp (-(2 * c) * x)

theorem deltaSymbol_pos (c x : ℝ) : 0 < deltaSymbol c x := Real.exp_pos _

theorem phase_eq_log_delta (c t x : ℝ) :
    characterPhase (2 * c * t) x =
      Complex.exp ((t : ℂ) * Complex.I * (Real.log (deltaSymbol c x) : ℂ)) := by
  unfold characterPhase deltaSymbol
  rw [Real.log_exp]
  congr 1
  push_cast
  ring

theorem delta_graph_symbol (c : ℝ) (f g : SpectralHilbert) :
    (f, g) ∈ (continuousModularDelta c).graph ↔
      g =ᵐ[volume] fun x => (deltaSymbol c x : ℂ) * f x := by
  rw [continuous_delta_eq_double]
  exact continuous_modular_graph_iff (2 * c) f g

theorem delta_domain_symbol (c : ℝ) (f : SpectralHilbert) :
    f ∈ (continuousModularDelta c).domain ↔
      MemLp (fun x => (deltaSymbol c x : ℂ) * f x) 2 (volume : Measure ℝ) := by
  rw [continuous_delta_eq_double]
  exact continuous_modular_domain_iff (2 * c) f

theorem fourier_bw_log_phase (t : ℝ) (f : L2R) :
    fourierUnitary (D (2 * Real.pi * t) f) =ᵐ[volume]
      fun x => Complex.exp ((t : ℂ) * Complex.I *
        (Real.log (deltaSymbol c0 x) : ℂ)) * fourierUnitary f x := by
  rw [fourier_bw_candidate]
  filter_upwards [characterMultiplier_ae (2 * c0 * t) (fourierUnitary f)] with x hx
  simpa only [← phase_eq_log_delta, characterPhase, smul_eq_mul] using hx

theorem c0_unique_coefficient (c : ℝ) (h : 2 * c = 4 * Real.pi ^ 2) : c = c0 := by
  unfold c0
  linarith

theorem standard_membership_fourier (c : ℝ) (f : L2R) :
    fourierUnitary f ∈ (continuousStandardSubspace c).toClosedSubmodule ↔
      ∃ hf : fourierUnitary f ∈ (continuousModularOperator c).domain,
        continuousModularTomita c ⟨fourierUnitary f, hf⟩ = fourierUnitary f :=
  continuous_standard_fixed_iff c (fourierUnitary f)

#print axioms dilation_eq_shift
#print axioms fourier_dilation
#print axioms c0_pos
#print axioms fourier_bw_candidate
#print axioms deltaSymbol_pos
#print axioms phase_eq_log_delta
#print axioms delta_graph_symbol
#print axioms delta_domain_symbol
#print axioms fourier_bw_log_phase
#print axioms c0_unique_coefficient
#print axioms standard_membership_fourier

end ChatgptAudit.FourierBridge016


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
