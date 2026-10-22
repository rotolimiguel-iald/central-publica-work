import Lean
import TGLExt.O16.WindowCoefficientVerbatim
import TGLExt.O16.ProbeForgedStressContract

set_option autoImplicit false
set_option maxHeartbeats 2000000

/-!
[DERIVED / PROPOSAL] A-1.c. Typed requirements on expectation-valued tensors.
This does NOT construct operator-valued distributions or prove microcausality.
Conservation is a distributional requirement, with integrability explicit so
that the totalized Bochner integral cannot turn a missing integral into zero.
Metric convention (+---); covariant indices; boosts act with inverse pullback.
Original types and kernel files are not modified.
-/

namespace ChatgptAudit.LocalStress
open TGL.SpecificAQFT TGL.ModularRealization TGLExt
open TGLExt.ContratoQGv31 MeasureTheory Matrix
noncomputable section

abbrev Spacetime := Fin 4 → ℝ
def metricSign (μ : Fin 4) : ℝ := if μ = 0 then 1 else -1
def testDerivative (f : Spacetime → ℝ) (μ : Fin 4) (x : Spacetime) : ℝ :=
  fderiv ℝ f x (Pi.single μ 1)

structure StressTensorDataLocal (W : TGLSpecificAQFTWitness) (B : WedgeBoostRep W)
    extends StressTensorData W where
  symmetric : ∀ ψ x, (T ψ x).transpose = T ψ x
  test_integrable : ∀ (ψ : W.H) (ν μ : Fin 4) (f : Spacetime → ℝ),
    ContDiff ℝ (⊤ : ℕ∞) f → HasCompactSupport f →
    Integrable (fun x => metricSign μ * T ψ x μ ν * testDerivative f μ x)
  conserved : ∀ (ψ : W.H) (ν : Fin 4) (f : Spacetime → ℝ),
    ContDiff ℝ (⊤ : ℕ∞) f → HasCompactSupport f →
    (∑ μ : Fin 4, ∫ x : Spacetime,
      metricSign μ * T ψ x μ ν * testDerivative f μ x) = 0
  boost_covariant : ∀ (s : ℝ) (ψ : W.H) (x : Spacetime),
    T (B.V s ψ) x = (boostMat (-s)).transpose *
      T ψ (wedgeBoostMap (-s) x) * boostMat (-s)

variable {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
  {N : KillingNormalization} {B : WedgeBoostRep W}

/-- The SAME contract on the forgotten tensor; no replacement dynamics. -/
theorem first_law_inherited (L : StressTensorDataLocal W B)
    (C : ContratoH3 W R N L.toStressTensorData) {ψ : W.H}
    (hψ : ψ ∈ C.admissible) (x : Spacetime) (c d : ℝ)
    (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowArea (C.response ψ) x c d =
      8 * Real.pi * C.G * windowCharge L.toStressTensorData ψ x c d :=
  C.first_law_window hψ x c d hθ

theorem bekenstein_hawking_inherited (L : StressTensorDataLocal W B)
    (C : ContratoH3 W R N L.toStressTensorData) {ψ : W.H}
    (hψ : ψ ∈ C.admissible) (x : Spacetime) (c d : ℝ)
    (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowEntropy L.toStressTensorData ψ x c d =
      windowArea (C.response ψ) x c d / (4 * C.G) :=
  C.bekenstein_hawking_window hψ x c d hθ

theorem clausius_inherited (L : StressTensorDataLocal W B)
    (C : ContratoH3 W R N L.toStressTensorData) (ψ : W.H)
    (x : Spacetime) (c d : ℝ) :
    windowHeat C.H2.kappa L.toStressTensorData ψ x c d =
      C.H2.unruhTemperature * windowEntropy L.toStressTensorData ψ x c d :=
  C.clausius_window ψ x c d

theorem einstein_coefficient_inherited (L : StressTensorDataLocal W B)
    (C : ContratoH3 W R N L.toStressTensorData) {ψ : W.H}
    (hψ : ψ ∈ C.admissible) (x : Spacetime) (c d : ℝ)
    (hθ : C.theta ψ (x + d • nullDir) = 0) :
    windowHeat C.H2.kappa L.toStressTensorData ψ x c d =
      C.H2.kappa * windowArea (C.response ψ) x c d / (8 * Real.pi * C.G) :=
  C.einstein_coefficient_window hψ x c d hθ

theorem kappa_cancels_inherited (L : StressTensorDataLocal W B)
    (C : ContratoH3 W R N L.toStressTensorData) (ψ : W.H)
    (x : Spacetime) (c d : ℝ) :
    windowHeat C.H2.kappa L.toStressTensorData ψ x c d / C.H2.unruhTemperature =
      windowEntropy L.toStressTensorData ψ x c d :=
  C.kappa_cancels_window ψ x c d

theorem slope_wall_inherited (L : StressTensorDataLocal W B)
    (C : ContratoH3 W R N L.toStressTensorData) (c : W.H → ℝ)
    (M : Matrix (Fin 4) (Fin 4) ℝ)
    (h : ∀ ψ x, C.response ψ x = (c ψ * x 0) • M) : False :=
  C.slope_response_excluded c M h

theorem exponential_wall_inherited (L : StressTensorDataLocal W B)
    (C : ContratoH3 W R N L.toStressTensorData) (c : W.H → ℝ)
    (M : Matrix (Fin 4) (Fin 4) ℝ)
    (h : ∀ ψ x, C.response ψ x = (Real.exp (c ψ * x 0) - 1) • M) : False :=
  C.exp_response_excluded c M h

/-- b2 fails the symmetry field, even before conservation/locality is considered. -/
theorem forged_tensor_rejected {T : StressTensorData W}
    (C : ContratoH3 W R N T) (hsym : ∀ ψ x, (T.T ψ x).transpose = T.T ψ x) :
    ¬ ∃ L : StressTensorDataLocal W B,
      L.toStressTensorData = ForgedStressContract.forgedTensor T := by
  obtain ⟨ψ, _, x, hne⟩ :=
    ForgedStressContract.forgery_has_nonsymmetric_admissible_value C hsym
  rintro ⟨L, hL⟩
  apply hne
  have hs := L.symmetric ψ x
  change (L.toStressTensorData.T ψ x).transpose = L.toStressTensorData.T ψ x at hs
  rw [hL] at hs
  exact hs

#print axioms einstein_coefficient_inherited
#print axioms kappa_cancels_inherited
#print axioms first_law_inherited
#print axioms bekenstein_hawking_inherited
#print axioms clausius_inherited
#print axioms slope_wall_inherited
#print axioms exponential_wall_inherited
#print axioms forged_tensor_rejected
end
end ChatgptAudit.LocalStress


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
